import os, string, csv, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
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
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)


def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    sline = clean(line.replace('–','-'))
    sline = sline.lower()
    sline = sline.strip()
    sline = sline.split("  ")
    sline = [x.strip() for x in sline if x != ""]
    
    return(sline)


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
    kit = []
    
    i=0
    for file in fileList:
        
        
        
        #Get ID numbers for unextracted documents
        ID = ''
        template = csv.reader(open('Factotum_Hewlett-Packard_1_unextracted_documents_20240123.csv')) 
        for row in template:
            if row[1] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
        
        #Identify the HP SDS files
        ifile = open(file, encoding = 'utf8')
        text = ifile.read()
        cleaned = cleanLine(text)
        if cleaned == '':
            print('blank: ',file)
        if 'material safety data sheet' not in cleaned or 'hewlett-packard' not in cleaned:
            continue
        
                
        #split up documents that have multiple msds
        documents = cleaned.split('product and company identification')[1:] 
        documents = [x for x in documents if '3. composition / information on ingredients' in x]
        for d in documents: 
            prodname = ''
            issueDate = ''
            revDate = ''
            rev = ''
            cat = ''
            use = ''
            component = []
            chem = []
            cas = []
            minC = []
            maxC = []
            centC = []
            unit = []
            cleaned = d
            compt=''
            
            if 'identification of the' in cleaned:
                prodname = cleaned.split('identification of the')[1].split('preparation')[0].strip()
            else:
                prodname = cleaned.split('material name')[1].split('version')[0].split('msds')[0].split('product use')[0].split('use of')[0].replace('\n',' ').strip(' :')
            if len(documents)!=1: 
                compt = prodname
                prodname = prodname.split('[')[0]
                print(len(documents),ID,prodname)
            rev = cleaned.split('version #')[1].split('revision')[0].split('issue')[0].replace('\n',' ').strip(' :')
            if 'revision date' in cleaned:
                revDate = cleaned.split('revision date')[1].split('product')[0].split('supersedes')[0].split('cas')[0].split('company')[0].split('synonym')[0].replace('\n',' ').strip(' :')
            else:
                issueDate = cleaned.split('issue date')[1].split('product')[0].split('cas')[0].split('company')[0].split('synonym')[0].replace('\n',' ').strip(' :')
            if 'product use' in cleaned:
                cat = cleaned.split('product use')[1].split('version')[0].split('cas')[0].split('company')[0].split('synonym')[0].split('manufacturer')[0].replace('\n',' ').strip(' :')
            elif 'use of the preparation' in cleaned:
                cat = cleaned.split('use of the preparation')[1].split('version')[0].split('cas')[0].split('company')[0].split('synonym')[0].split('manufacturer')[0].replace('\n',' ').strip(' :')
            cat = re.sub(' +', ' ', cat)
            
            
      
                    
            # cleaned = cleanLine(text)
            # cleaned = re.sub(' +', ' ', cleaned)
            section3 = '\n'.join(cleaned.split('3. composition / information on ingredients')[1:]).split('4. first aid measures')[0].strip()
            lines = section3.split('\n')
            lines = list(filter(None,lines))
         
            
            
            for line in lines: #Extract ingredient section
            
                if 'component' in line and 'cas' in line: continue #skip table header
                if 'material name' in line or 'revision date' in line or 'material safety data sheet' in line or 'version number' in line: continue #skip footers
                if 'reportable hazardous ingredients' in line or 'sds_north america -' in line or 'revision date:' in line or 'chemical identity' in line or 'version #' in line: continue
                if line == 'mixtures': continue
                casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",line) #Regular expression to find cas numbers
                
                if 'composition comments' in line: break #notes at end of table
                if 'the components are not hazardous or are below required disclosure limits' in line: break #no chemicals
                
                if len(casrn) == 0 and any(x in line for x in ['proprietary','trade secret','not available','mixture','n/a','no data']): #cas numbers that are just words
                    r = re.compile(r'PROPRIETARY|TRADE SECRET|NOT AVAILABLE|MIXTURE|N/A|NO DATA', flags=re.I)
                    casrn=r.findall(line)
                if len(casrn) == 0 and 'ink' in line: 
                    compt=line.strip()
                    continue
                if len(casrn) == 1:
                    chem.append(line.split(casrn[0])[0].strip())
                    cas.append(casrn[0])
                    centC.append(line.split(casrn[0])[1].strip())
                    component.append(compt)
                elif len(casrn) >1:
                    chem.append(casrn[-1].join(line.split(casrn[-1])[:-1]).strip())
                    cas.append(casrn[-1])
                    centC.append(line.split(casrn[-1])[-1].strip())
                    component.append(compt)
                else: 
                    print(ID,line)
                    words = line.split(' ')
                    conc = ''
                    for w in reversed(words):
                        if all(x in '1235467890<>=-.,' for x in w):
                            conc = (w + ' ' + conc).strip()
                        else: break
                    chem.append(line.split(conc)[0].strip())
                    cas.append('')
                    centC.append(conc)
                    component.append(compt)
               
                
            #clean up concentrations and names    
            for c in range(0,len(chem)): 
                chem[c] = re.sub(' +', ' ', chem[c])
                minC.append('')
                maxC.append('')
                centC[c]=centC[c].replace('%','').strip()
                if centC[c] != '':
                    unit.append('3')
                else:
                    unit.append('')
                if '-' in centC[c]:
                    minC[c] = centC[c].split('-')[0].strip()
                    maxC[c] = centC[c].split('-')[1].strip()
                    centC[c] = ''
     
            #If no chems, leave fields blank
            if chem == []:
                chem = ['']
                cas = ['']
                minC = ['']
                maxC = ['']
                centC = ['']
                unit = ['']
                component = [compt]
                
            n = len(chem)
            idList.extend([ID]*n)
            filenameList.extend([file.replace('.txt','.pdf')]*n)
            prodnameList.extend([prodname]*n)
            if revDate != '':
                dateList.extend([revDate]*n)
            else:
                dateList.extend([issueDate]*n)
            revList.extend([rev]*n)
            catList.extend([cat]*n)
            casList.extend(cas)
            chemList.extend(chem)
            useList.extend([use]*n)
            minList.extend(minC)
            maxList.extend(maxC)
            unitList.extend(unit)
            centList.extend(centC)
            componentList.extend(component)
            
            if chem == ['']:
                rankList.extend([''])
            else:
                rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    # print(kit)
    i=-1
    for index, row in df.iterrows():
        i+=1
        
        if row['data_document_filename'] in kit:
            df.loc[i,'component'] = df.loc[i,'prod_name']
            df.loc[i,'prod_name'] = df.loc[i,'prod_name'].split('[')[0]
            print('kit',row['data_document_filename'])
    df.to_csv('HP MSDS Extracted Text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/HP') #Folder pdfs are in
    pdfs = glob("*.pdf")
    txts = glob("*.txt")
    
    unconverted = []
    for p in pdfs: 
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    # pdfToText(unconverted)
    
    fileList = glob("*.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
