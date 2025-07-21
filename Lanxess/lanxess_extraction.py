import os, string, csv, re
import pandas as pd
from glob import glob
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import locale
import numpy as np



def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\Documents\\xpdf-tools-win-4.05\\xpdf-tools-win-4.05\\bin64\\' #Path to execfile
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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('','').replace('','')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
    cline =clean(cline)
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Lanxess') #Folder pdfs are in
pdfs = glob("*.pdf")
txts = glob("*.txt")

unconverted = []
for p in pdfs: 
    if p.replace('.pdf','.txt') not in txts:
        unconverted.append(p)
pdfToText(unconverted)

fileList = glob("*.txt")       
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
findcas = lambda text: re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",text) #finds cas number     
findecs = lambda text: re.findall("[0-9]{3}\-[0-9]{3}\-[0-9]",text) #finds ec number
findreachs = lambda text: re.findall("[0-9]{2}\-[0-9]{10}\-[0-9]{2}\-",text) #finds reach number
    
    
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
template = csv.reader(open('Factotum_Lanxess_SDS_unextracted_documents_20250718.csv')) 
for row in template:
    filename=row[1]
    ID = row[0]
    
    
    if filename == 'data_document_filename': continue
    

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
    if 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
    else:
        print('prodname',filename)
    prodname = prodname.split('product code')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
 
    
    #Date and version
    if 'date of last issue' in cleaned:
        dateline = cleaned.split('date of last issue')[1]
        dateline=' '.join(dateline.split('\n')[1:])
        dateline=dateline.split('section 1')[0].strip()
        dateline = re.sub(' +', ' ', dateline)
        rev = dateline.split(' ')[0]
        date=dateline.split(' ')[1]
    else: 
        print('date',ID,filename)
        
    #Raw category
    if 'recommended use :' in cleaned: 
        cat = cleaned.split('recommended use :')[1].split('section 2')[0]
    else:
        print('raw category',filename)
    cat = clean(cat).replace('\n',' ').strip(':. ')
    cat = re.sub(' +', ' ', cat)
 
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'information on ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on ingredients')[1:]).split('section 4')[0]

    else: print('sec3',ID,filename)

    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    

    for line in lines:
        
        line=line.strip()
        if any(x in line for x in ['safety data sheet','substance / mixture','country / language','print date','chemical nature','substance name','any concentration shown as','chemical name cas-no','revision date','no hazardous ingredients','chemical name cas no','osha hazard','* indicates that the']): 
            continue #skip these lines
        
        if line in ['components','no hazardous ingredients','contains']: continue
        
        if line==prodname: continue
        
        if line.count('/') == 1 and all(x in '1234567890/ ' for x in line): continue
        
   

        casrns = findcas(line)
        if len(casrns) == 0 and 'trade secret' in line: 
            casrns.append('trade secret')
        if len(casrns)==1:
            cas.append(casrns[0])
            chem.append(line.split(casrns[0])[0])
            centC.append(line.split(casrns[0])[1])
        elif len(chem)>0:
            chem[-1] = chem[-1] + ' ' + line
        # else:
        #     print(filename,line)
  
  
            
    if len(chem)==0 and 'chemical nature' in sec3:
        # if filename=='LEWATIT VP OC 1600.pdf':print(sec3)
        line = sec3.split('chemical nature')[1]
        line=line.split('components')[0].split('chemical name')[0].split('1 / 1')[0]
        line = line.replace('substance name :','')
        line = line.replace('contains',' ')
        line = line.replace('\n',' ').strip(':. ')
        line = re.sub(' +', ' ', line)
        if line != 'to be reviewed':
            chem.append(line)
            cas.append('')
            centC.append('')
        print(filename, line)
        
    elif len(chem)==0 and 'substance name' in sec3:
        line = sec3.split('substance name')[1]
        line=line.split('components')[0].split('chemical name')[0].split('1 / 1')[0]
        line = line.replace('substance name :','')
        line = line.replace('contains',' ')
        line = line.replace('\n',' ').strip(':. ')
        line = re.sub(' +', ' ', line)
        if line != 'to be reviewed':
            chem.append(line)
            cas.append('')
            centC.append('')
        print(filename, line)
        
    
    
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = chem[c].strip(' ,.')
        chem[c] = re.sub(' +', ' ', chem[c])
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip()
        if '~' in centC[c] and '-' not in centC[c] and centC[c][0] != '~':
            centC[c]=centC[c].replace('~','-')
        if centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip('>= ')
            maxC[c] = centC[c].split('-')[1].strip(' <=')
            centC[c] = ''
        if minC[c]=='' and maxC[c]!='':
            centC[c]=maxC[c]
            minC[c]=''
            maxC[c]=''
 
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

df.to_csv(r'lanxess extracted text.csv',index=False, header=True)
