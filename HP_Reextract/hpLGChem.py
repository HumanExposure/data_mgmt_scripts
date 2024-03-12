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


os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/HP') #Folder pdfs are in
pdfs = glob("*.pdf")
txts = glob("*.txt")

unconverted = []
for p in pdfs: 
    if p.replace('.pdf','.txt') not in txts:
        unconverted.append(p)
# pdfToText(unconverted)

fileList = glob("*.txt")       
    
    
    
    
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
    template = csv.reader(open('Factotum_Hewlett-Packard_1_unextracted_documents_20240312.csv')) 
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
    if 'lgchem' not in cleaned:
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
    
    
    #get product data
    prodname = cleaned.split('product identification')[1].split('manufacturer')[0].split('msds')[0].replace('\n',' ').strip(': ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Get version number and date of last version
    lines = cleaned.split('\n') 
    lines = reversed(lines)
    for line in lines: 
        line = line.strip()
        if len(line) > 1 and line[0]== 'v' and line[1] in '1234567890':
            rev = line.split('v')[1].split(' ')[0]
            date = line.split(' ')[-1]
            break
    
    
  
    #find section 2
    section2 = '\n'.join(cleaned.split('2. composition information')[1:]).split('3. hazards identification')[0].strip()
    lines = section2.split('\n')
    lines = list(filter(None,lines))
 
    
    #Extract chemical data
    for line in lines: #Extract ingredient section
        line = line.strip()
        if line[0] == '*': continue
        if any(x in line for x in ['msds','lgchem','hazardous ingredients','emergency overview','may explode in a fire','use extinguishing media']): continue
        
        casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",line) #Regular expression to find cas numbers
        if len(casrn)>1: print(ID,line, file)
        elif len(casrn) == 1: 
            casrn = casrn[0]
            line = ' '.join(line.split(casrn)[:-1])
        elif line.split(' ')[-1] in ['n/a']: 
            casrn = line.split(' ')[-1]
            line = ' '.join(line.split(casrn)[:-1])
        else: casrn = ''
            # print(ID,line)
    
        line = reversed(line.split(' '))
        name = ''
        comp = ''
        inComp=True
        for x in line:
            if inComp == True and (all(y in '0123456789-%<>.~' for y in x) or x == 'remainder'):
                comp = (x+' '+comp).strip()
            else:
                inComp = False
                name = (x+' '+name).strip()
        centC.append(comp)
        chem.append(name)
        cas.append(casrn)

  
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        chem[c] = chem[c].strip()
        cas[c] = cas[c].strip()
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

df.to_csv('HP lgchem Extracted Text.csv',index=False, header=True)