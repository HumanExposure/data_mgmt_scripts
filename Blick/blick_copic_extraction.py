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
    cline = clean(line.replace('–','-').replace('－','-'))
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
    if row[7].split('_')[0].lower() == 'copic':
        filename=row[6]
        ID = row[0]
        if ID in ['1731312','1727476']: continue #these are different formats. skip.
    else: continue
    

    
    file=filename.replace('.pdf','.txt')    
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n')
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
    
    #Product name
    if '\nproduct name' in cleaned: 
        prodname = cleaned.split('\nproduct name')[1].split('other means')[0].split('product description')[0].split('ean')[0].split('sds')[0].split('1.2')[0].split('recommended use')[0].replace('\n',' ').strip(': ')
        prodname = re.sub(' +', ' ', prodname)
    elif 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1].split('other means')[0].split('product description')[0].split('ean')[0].split('sds')[0].split('1.2')[0].split('recommended use')[0].replace('\n',' ').strip(': ')
        prodname = re.sub(' +', ' ', prodname)
    elif 'trade name' in cleaned: 
        prodname = cleaned.split('trade name')[1].split('other means')[0].split('product description')[0].split('ean')[0].split('sds')[0].split('1.2')[0].split('recommended use')[0].replace('\n',' ').strip(': ')
        prodname = re.sub(' +', ' ', prodname)
    
    
    #Date
    if 'date of issue' in cleaned:
        date = cleaned.split('date of issue')[1].split('\n')[0].strip(' :')
    elif 'date issued' in cleaned: 
        date = cleaned.split('date issued')[1].split('\n')[0].strip(' :')
    elif 'msds creation date' in cleaned: 
        date = cleaned.split('msds creation date')[1].split('\n')[0].strip(' :')
        
    #Revision number
    if 'revision number' in cleaned:
        rev = cleaned.split('revision number')[1].split('\n')[0].strip(' .:')
    elif 'version' in cleaned:
        rev = cleaned.split('version')[1].split('date')[0].split('\n')[0].strip(' .:')
    
    #Raw category
    if 'recommended use(s)' in cleaned:
        cat = cleaned.split('recommended use(s)')[1].split('restrictions on use')[0].split('manufacturer')[0].split('synonym')[0].split('1.3')[0].replace('\n',' ').strip(': .')
        cat = re.sub(' +', ' ', cat)
    elif '\nrecommended use' in cleaned:
        cat = cleaned.split('\nrecommended use')[1].split('restrictions on use')[0].split('manufacturer')[0].split('synonym')[0].split('1.3')[0].replace('\n',' ').strip(': .')
        cat = re.sub(' +', ' ', cat)
    elif 'product description' in cleaned:
        cat = cleaned.split('product description')[1].split('restrictions on use')[0].split('manufacturer')[0].split('synonym')[0].split('1.3')[0].split('1.2')[0].replace('\n',' ').strip(': .')
        cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    if 'chemical name cas no. concentration' in cleaned:
        sec3=cleaned.split('chemical name cas no. concentration')[1].split('section 4')[0].strip()
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines: 
            if any(x in line for x in ['page ','item number','safety data sheet','msds','date of issue']): continue #between lines
            casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",line) #Regular expression to find cas numbers
            if len(casrn)==1:
                chem.append(line.split(casrn[0])[0])
                centC.append(line.split(casrn[0])[-1])
                cas.append(casrn[0])
            else: print(ID,line)
            
    elif 'chemical name % weight cas no' in cleaned or 'chemical name weight% cas no' in cleaned:
        if 'chemical name % weight cas no' in cleaned:
            sec3=cleaned.split('chemical name % weight cas no')[1]
        else: sec3=cleaned.split('chemical name weight% cas no')[1]
        sec3=sec3.split('section 4')[0]
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines: 
            
            if any(x in line for x in ['page ','item number','safety data sheet','msds','date of issue','withheld as a trade secret','the specific chemical identity','composition has been withheld as a']): continue #between lines
            if line.replace('only','').strip('. ')=='': continue
            casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",line) #Regular expression to find cas numbers
            if ')' in line and '(' not in line:
                continue
            line=line.replace('(as a dye containing','').replace('(as a dye','')
            if casrn==[] and 'confidential' in line: casrn.append('confidential')
            if len(casrn)==1:
                line=line.split(casrn[0])[0]
                # print(ID,line,casrn)
                sline = reversed(line.split(' '))
                comp = ''
                for x in sline:
                    if all(y in '0123456789-%<>.~=' for y in x):
                        comp = (x+' '+comp).strip()
                    else:
                        inComp = False
                        break
                name=line.split(comp)[0]
                centC.append(comp)
                chem.append(name)
                cas.append(casrn[0])
                print(ID,name,comp,casrn[0])
 
    elif 'the composition of the material is reserved as a trade secret' in cleaned:
        #this document has no chemicals
        pass
  
        
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Copic Extracted Text.csv',index=False, header=True)

  
