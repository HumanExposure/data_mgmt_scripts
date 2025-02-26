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
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return


def ocrPdf(files):
    """
    Converts files into jpegs, uses pytesseract to OCR the jpegs, and writes the text into a txt file
    files: list of filenames
    """
        
  
    
    config = r'--psm 4 -c preserve_interword_spaces=1'
    pytesseract.pytesseract.tesseract_cmd = r'c:\Users\alarger\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    for p in files:
        num = p.split('.pdf')[0]
        pages = convert_from_path(p,500, poppler_path = r"C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\poppler-0.68.0_x86\bin")
        image_counter = 1
        
        #Make jpeg of each page
        jpegs = []
        for page in pages: 
            filename = num+"page"+str(image_counter)+"_ocr.jpg"
            page.save(filename, 'JPEG') 
            image_counter = image_counter + 1
            jpegs.append(filename)
        filelimit = image_counter-1
        
        #Make text file
        outfile = num+'_ocr.txt'
        f = open(outfile, "a") 
        
        #Perform OCR on jpegs and write to text file 
        for i in range(1, filelimit + 1): 
            # print(i)
            filename = num+"page"+str(i)+"_ocr.jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename), config = config))))    
            # print(text)
            text=clean(text)
            f.write(text) 
            f.write('\n')
        
        f.close() 
        
        #Delete jpegs
        # for j in jpegs:
        #     os.remove(j)

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('ﬁ','fi').replace('','')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Blick') #Folder pdfs are in
pdfs = glob("*.pdf")
txts = glob("*.txt")


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
unextractedids = []
template = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Factotum_Blick_(M)SDS_(2024)_unextracted_documents_20250218.csv'))
for row in template:
    unextractedids.append(row[0])
    
template = csv.reader(open(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Blick/Factotum_Blick_(M)SDS_documents_20240705.csv')) 
for row in template:
    if clean(row[7].split('_')[0].replace(' ','').lower()) in ['mayco'] and row[0] in unextractedids:
        filename=row[6]
        ID = row[0]
    else: continue
    
    if filename == 'file name': continue
    if filename.replace('.pdf','_ocr.txt') not in txts:
        ocrPdf([filename]) 

    file=filename.replace('.pdf','_ocr.txt')    
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
    if 'product name:' in cleaned:
        prodname = cleaned.split('product name:')[1]
    elif 'section 1: product identification' in cleaned:
        prodname = cleaned.split('section 1: product identification')[1].split('all products')[0]
        continue #these docs performed poorly
    else: 
        print('prodname',ID)
    prodname = prodname.split('company information')[0].split('product us')[0].split('product description')[0].split('section 2')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    
    #Date
    if 'date of issue:' in cleaned:
        date = cleaned.split('date of issue:')[1]
    elif 'prepared:' in cleaned:
        date = cleaned.split('prepared:')[1]
    else: 
        print('date',ID,filename)
    date=date.split('according to')[0].split('supersedes')[0].split('section')[0].strip('# .*:,')
    date = clean(date).replace('\n',' ').strip(':. ')
    date = re.sub(' +', ' ', date)
    
    #version
    if 'version:' in cleaned:
        rev = cleaned.split('version:')[1].split('according to')[0].split('date')[0].strip()
    else: 
        print('version',ID,filename)
    rev = clean(rev).replace('\n',' ').strip(':. ')
    rev = re.sub(' +', ' ', rev)
 
    #Raw category
    if 'relevant identified use(s)' in cleaned: 
        cat = cleaned.split('relevant identified use(s)')[1]
    else: 
        print('raw cat',ID,filename)
    cat=clean(cat).split('page')[0].split('item number')[0].split('1.3')[0].replace('\n',' ').strip(': .,')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'section 3' in cleaned:
        sec3=cleaned.split('section 3')[1].split('section 4')[0]
    else: print('HELP',ID)

    lines = sec3.split('\n')
    lines = list(filter(None,lines))

    for line in lines:
        line=line.strip()
        if betweenPages == True:
            
            if 'safety data sheet' in line or 'msds' in line:
                betweenPages=False
            
            continue
        if ('page' in line or 'item numbers' in line) and 'version' not in line and 'contd' not in line:
            betweenPages=True
            continue
        
        if any(x in line for x in ['information on ingredients','chemical name cas','the remaining ingredients','concentration limits','concentrations are calculated']): 
        
            continue #skip these lines
        
        if line in ['mixture']: 
            continue #skip these lines
  
            
        casrns = findcas(line)
        if len(casrns) == 1:
            chem.append(line.split(casrns[0])[0].strip('" '))
            cas.append(casrns[0])
            centC.append(line.split('up to')[-1].strip(' %'))
        else:
            print(ID,line)
      
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        if chem[c] == 'zinc oxide p': chem[c]='zinc oxide'
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip()
        centC[c] = centC[c].strip(' na/')
        if ' ' in centC[c] and '-' not in centC[c]:
            centC[c] = centC[c].split(' ')[-1]
        if '~' in centC[c] and '-' not in centC[c] and centC[c][0] != '~':
            centC[c]=centC[c].replace('~','-')
        if centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip('> ')
            maxC[c] = centC[c].split('-')[1].strip(' <')
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
    filenameList.extend([filename]*n)
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\mayco ocr extracted text.csv',index=False, header=True)
