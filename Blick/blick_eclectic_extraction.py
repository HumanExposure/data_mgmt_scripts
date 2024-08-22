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
    line=line.replace('é','e').replace('≤','<=').replace('≥','>=').replace('–','-').replace('－','-')
    cline = clean(line)
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Blick') #Folder pdfs are in
pdfs = glob("*.pdf")
txts = glob("*.txt")

unconverted = []
for p in pdfs: 
    if p.replace('.pdf','.txt') not in txts:
        unconverted.append(p)
pdfToText(unconverted)

fileList = glob("*.txt")       
    
findcas = lambda text: re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",text)
    
    
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

i=0
template = csv.reader(open('C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Blick/Factotum_Blick_(M)SDS_documents_20240705.csv')) 
for row in template:
    filename=row[6]
    ID = row[0]
     
    

    file=filename.replace('.pdf','.txt')  
    if filename == 'file name': continue
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n')
    if cleaned == '':
        print('blank: ',file)
    
    if 'eclectic products' not in cleaned:
        continue
 
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    use = ''
    component = ''
    chem = []
    cas = []
    minC = []
    maxC = []
    centC = []
    unit = []
    
    #Product name
    if 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
    prodname = prodname.split('relevant identified uses')[0].split('product code')[0].split('trade name')[0]
    prodname = prodname.replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'date of revision' in cleaned:
        date = cleaned.split('date of revision')[1].split('version')[0].split('\n')[0].strip(' :')
    elif 'date of issue/date of' in cleaned:
        date = cleaned.split('date of issue/date of')[1].split('version')[0].split('\n')[0].strip(' :')
   
        
        
    #Revision number
    if 'version' in cleaned:
        rev = cleaned.split('version')[1]
    rev=rev.split('page')[0].split('\n')[0].strip('# .:')
    
    #Raw category
    if '\nidentified uses' in cleaned: 
        cat = cleaned.split('\nidentified uses')[1]
   
    cat=cat.split('supplier')[0].split('section 2')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
   
    if 'section 3. composition/information on ingredients' in cleaned: 
        sec3=cleaned.split('section 3. composition/information on ingredients')[1].split('section 4')[0].split('any concentration shown')[0]
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        
        for line in lines:
            if any(x in line for x in ['substance/mixture','ingredient name % cas number']): continue #these lines don't have useful info
            print(ID, line)
            casnums = findcas(line)
            line=line.replace(casnums[0],'').strip()
            if len(casnums) == 1:
                
                sline = reversed(line.split(' '))
                comp = ''
                breaknext=False
                for x in sline:
                    if all(y in '0123456789-%<>.~=/' for y in x) or (x.strip(' *.') == 'proprietary' and comp == ''):
                        comp = (x+' '+comp).strip()
                    else:
                        break
                chem.append(line.replace(comp,'').strip())
                cas.append(casnums[0])
                centC.append(comp)
                # pass
            else: 
                print(ID, line,len(casnums))
      
            
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip()
        if centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip('> ')
            maxC[c] = centC[c].split('-')[1].strip(' <')
            centC[c] = ''
 
    #If no chems, leave fields blank
    if chem == []:
        chem = ['']
        cas = ['']
        minC = ['']
        maxC = ['']
        centC = ['']
        unit = ['']
        
    n = len(chem)
    idList.extend([ID]*n)
    filenameList.extend([file.replace('.txt','.pdf')]*n)
    prodnameList.extend([prodname]*n)
    dateList.extend([date]*n)
    revList.extend([rev]*n)
    catList.extend([cat]*n)
    casList.extend(cas)
    chemList.extend(chem)
    useList.extend([use]*n)
    minList.extend(minC)
    maxList.extend(maxC)
    unitList.extend(unit)
    centList.extend(centC)
    componentList.extend([component]*n)
    
    if chem == ['']:
        rankList.extend([''])
    else:
        rankList.extend(list(range(1,n+1)))
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\eclectic Extracted Text.csv',index=False, header=True)

  