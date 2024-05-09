import os, string, csv, re
import pandas as pd
from glob import glob
import camelot

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


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\P&G\P&G pro') #Folder pdfs are in
pdfs = glob("*sds.pdf")
txts = glob("*.txt")


unconverted = []
for p in pdfs: 
    if p.replace('.pdf','.txt') not in txts:
        unconverted.append(p)
# pdfToText(unconverted)

fileList = glob("*sds.txt")       
    
    
    
    
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
    
    i+=1
    print(i)
    
    #Get ID numbers for unextracted documents
    ID = ''
    template = csv.reader(open('Factotum_Proctor_&_Gamble_Pro_SDS_unextracted_documents_20240426.csv')) 
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
    cleaned = re.sub(' +', ' ', cleaned)
    if cleaned == '':
        print('blank: ',file)
 
  
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
    
    #get product data
    if 'product name' in cleaned:
        prodname = cleaned.split('product name')[1].split('product code')[0].split('product identifier')[0].split('1.2 relevant')[0].split('other means')[0].replace('\n',' ').strip()
        prodname = re.sub(' +', ' ', prodname)
    else: continue #These are blank sds with no info
    date = cleaned.split('revision date')[1].split('version')[0].split('revision')[0].strip(' :')
    if date=='new': date=date = cleaned.split('issuing date')[1].split('revision')[0].strip(' :')
    if 'revision number' in cleaned:
        rev = cleaned.split('revision number')[1].split('\n')[0].strip(' .:')
    elif 'version' in cleaned:
        rev = cleaned.split('version')[1].split('\n')[0].strip(' .:')
    if 'recommended use' in cleaned:
        cat = cleaned.split('recommended use')[-1].split('details of the')[0].split('synonyms')[0].split('manufacturer')[0].split('uses advised against')[0].split('restrictions on use')[0].split('1.3')[0].replace('\n',' ').strip(':. ')
    cat = re.sub(' +', ' ', cat)
    
    
  
    #find section 3
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    section3 = '\n'.join(cleaned.split('composition/information on ingredients')[1:]).split('first aid measures')[0].strip()
    lines = section3.split('\n')
    lines = list(filter(None,lines))
    
 
    inTable=False   
 
    #Extract chemical data
    for line in lines: #Extract ingredient section
        line = line.strip()
        if 'chemical name' in line:
            inTable=True
            continue
        if inTable==True:
            if 'additional information' in line: 
                inTable=False
                break
            
            # print(ID,line)
            
    try: tables = (camelot.read_pdf(file.replace('.txt','.pdf'),pages='all', flavor='lattice'))
    except: 
        tables=[]
        print(ID)
    
    for t in tables:
        t=t.df
        if t.iloc[0,0].lower().strip()=='chemical name' and len(t.columns)>=3 and 'lc50' not in t.iloc[0,-1].lower().strip() and 'ld50' not in t.iloc[0,-1].lower().strip():
            print(t)
            t = t.drop(t.index[0])
            chem=t.iloc[:,0].tolist()
            cas=t.iloc[:,-2].tolist()
            centC=t.iloc[:,-1].tolist()
            break
            print(ID,t)

    
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c]=chem[c].replace('\n',' ')
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
df.to_csv('pg pro Extracted Text.csv',index=False, header=True)

  
