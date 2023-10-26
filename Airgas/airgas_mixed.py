import os, string, csv, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.03\\bin64\\' #Path to execfile
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return


def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    # clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('–','-').replace('≤','<=')
    cline = cline.lower()
    # cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)



def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    idList = [] #list of product IDs
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    casList = [] #list of CAS numbers
    chemList = [] #list of chemical names
    useList = [] #list of functional uses of each chemical
    minList = [] #list of minimum concentrations
    maxList = [] #list of maximum concentrations
    unitList = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...)
    rankList = [] #list of ingredient ranks
    centList = [] #list of central concentrations
    componentList = [] #List of components
    
    msds = []
    
    for file in fileList:
        
        ifile = open(file, encoding = 'utf8')
        text=ifile.read()
        if 'materialsafetydatasheet' in text.lower().replace(' ',''): #document is in a different format
            # print(file)
            msds.append(file)
            continue
        
            
        ifile = open(file, encoding = 'utf8')
        text = ifile.read()
        
        cleaned = cleanLine(text)
        cleaned = re.sub(' +', ' ', cleaned)        
    
        if cleaned == '': print(file)
                
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        filename = ''
        use = []
        component = []
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
        
        
        template = csv.reader(open(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Mixed/Factotum_Airgas_MixedGases_documents_20231016.csv')) #Get factotum document ids
        ID = file.split('_')[-1].split('.')[0]
        for row in template:
            if row[0] == ID:
                filename = row[6]
                break
        if filename == '':
            print(file)
            continue
        
        
        prodname = cleaned.split('ghs product identifier :')[-1].split('other means of')[0].replace('\n',' ').strip() #get product name
        prodname = re.sub(' +', ' ', prodname) #get rid of extra spaces
        date = cleaned.split('date of issue/date of revision :')[-1].strip(': ').split(' ')[0].strip('. ') #get date
        rev = cleaned.split('version :')[-1].strip(': ').split(' ')[0].strip() #Get revision number
    
        cat = cleaned.split('product use :')[-1].split('synonym')[0].split('sds')[0].replace('\n',' ').strip(': ') #Get raw category
        cat = re.sub(' +', ' ', cat) #get rid of extra spaces
        
        
        cleaned = cleanLine(text)
        if 'section 3' in cleaned and 'cas number' in cleaned: 
            section3 = ' '.join(cleaned.split('section 3')[1:]).split('section 4')[0].split('any concentration')[0].split('there are no')[0].split('occupational exposure limits')[0]
        else: 
            print(file)
            continue
        
        if date.strip('. ')=='***' or rev.strip('. ')=='***': continue #skip draft files
        
        lines = section3.split('\n')
        betweenPages = False
        for line in lines: #Extract ingredient section
           
            if 'date of issue' in line: #Skip header and footer lines if ingredients section spans two pages
                betweenPages = True
                continue

            
            if betweenPages == True:
                if 'cas number' in line and 'name' in line:
                    betweenPages = False
                    if len(chem)  > 0: print(file)
                continue

            if len(line.strip()) == 0: continue #skip blank lines

            if 'cas number' in line or (':' in line and 'not applicable' in line) or 'substance/mixture' in line or 'other means of' in line or 'product code' in line or 'composition/information' in line:
                continue
            
            line = line.split('  ')
            line = list(filter(None,line))
            
            if line[0].strip() == 'identification': continue
            
            elif len(line)>3: # Fix lines that don't have three columns
                # print(len(line),file, line)
                while len(line) > 3:
                    if all(x in '0123456789. -%<>=' for x in line[-3]):
                        line = line[:-3]+[line[-3]+line[-2]]+[line[-1]]
                    else: 
                        line = [line[0]+' '+line[1]]+line[2:-1]+[line[-1]]
            elif len(line) ==1:
                if all(x in '0123456789. -%<>=' for x in line[0]): centC[-1]=centC[-1]+line[0].strip()
                else: chem[-1] = chem[-1]+' '+line[0]
                # print(len(line),file, line)
            elif len(line) == 2:
                print(len(line),file, line)
                
            if len(line)==3: #save columns as chem, conc, and casrn
                # print(file, line)
                chem.append(line[0])
                cas.append(line[2])
                centC.append(line[1])
                use.append('')
                
                
        if chem == []: #If there are no chemicals in the document, save empty strings in the chemical fields
            chem = ['']
            cas = ['']
            centC = ['']
            use = ['']
      
        for c in range(0,len(chem)): #clean up concentrations and names
            chem[c] = re.sub(' +', ' ', chem[c])
            minC.append('')
            maxC.append('')
            # use.append('')
            component.append('')
            centC[c] = re.sub(' +', ' ', centC[c])
            if centC[c] != '':
                unit.append('3')
            else:
                unit.append('')
            if '-' in centC[c]:
                minC[c] = centC[c].split('-')[0].strip()
                maxC[c] = centC[c].split('-')[1].strip()
                centC[c] = ''

    
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([filename]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend(use)
        minList.extend(minC)
        maxList.extend(maxC)
        unitList.extend(unit)
        centList.extend(centC)
        componentList.extend(component)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    
   # Make csv
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Mixed/airgas mixed extracted text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Mixed/mixed gases docs') #Folder pdfs are in

        
    pdfs = glob("*.pdf")
    txts = glob("*.txt")
    unconverted = []
    for p in pdfs:  #Convert to txt
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    pdfToText(unconverted)
    
    fileList = glob("*.txt") #extract text
    extractData(fileList)    


if __name__ == "__main__": main()