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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('','').replace('','').replace('®','')#.replace('α','alpha').replace('ω','omega').replace('β','beta').replace('γ','gamma')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
    cline =clean(cline)
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)

# def ocrPdf(files):
#     """
#     Converts files into jpegs, uses pytesseract to OCR the jpegs, and writes the text into a txt file
#     files: list of filenames
#     """
        
  
    
#     config = r'--psm 4 -c preserve_interword_spaces=1'
#     pytesseract.pytesseract.tesseract_cmd = r'c:\Users\alarger\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

#     for p in files:
#         num = p.split('.pdf')[0]
#         pages = convert_from_path(p,500, poppler_path = r"C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\poppler-0.68.0_x86\bin")
#         image_counter = 1
        
#         #Make jpeg of each page
#         jpegs = []
#         for page in pages: 
#             filename = num+"page"+str(image_counter)+"_ocr.jpg"
#             page.save(filename, 'JPEG') 
#             image_counter = image_counter + 1
#             jpegs.append(filename)
#         filelimit = image_counter-1
        
#         #Make text file
#         outfile = num+'_ocr.txt'
#         f = open(outfile, "a") 
        
#         #Perform OCR on jpegs and write to text file 
#         for i in range(1, filelimit + 1): 
#             # print(i)
#             filename = num+"page"+str(i)+"_ocr.jpg"
#             text = str(((pytesseract.image_to_string(Image.open(filename), config = config))))    
#             # print(text)
#             text=clean(text)
#             f.write(text) 
#             f.write('\n')
        
#         f.close() 
        


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Lion Elastomers') #Folder pdfs are in
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
template = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Lion Elastomers\Factotum_Lion_Elastomers_SDS_unextracted_documents_20260707.csv')) 
for row in template:
    filename=row[1]
    ID = row[0]
    
    
    if filename == 'data_document_filename': continue

    file=filename.replace('.pdf','.txt')    
    try: ifile = open(file, encoding = 'utf8')
    except: continue
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n')
    # if cleaned == '':

    #     if os.path.isfile((file.replace('.txt','_ocr.txt'))) == False:
    #         ocrPdf([filename])
        
    #     ifile = open((file.replace('.txt','_ocr.txt')), encoding = 'utf8')
    #     text = ifile.read()
    #     cleaned = cleanLine(text)
    #     cleaned = re.sub(' +', ' ', cleaned)
        # cleaned=cleaned.replace('\n ','\n')
      
    

  
  
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
    components = []
    ranks=[]
    rank=1
    subchem=''
    subcas=''
    betweenPages=False
    
    #Product name
    if 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
    elif 'substance name' in cleaned: 
        prodname = cleaned.split('substance name')[1]

    else:
        print('prodname',ID,filename)
    prodname = prodname.split('1.2. recommended')[0].split('1.2. other')[0].split('other means of')[0].split('recommended use')[0].split('chemical name:')[0].split('revision')[0].split('version')[0].split('product code')[0].split('lion elastomers')[0].split('cas-no')[0]
    prodname = (prodname).replace('\n',' ').strip(':. -') 
    prodname = re.sub(' +', ' ', prodname)
 
    
    #Date 
    if 'revision date:' in cleaned:
        date = cleaned.split('revision date:')[1]
        
    elif 'issue date:' in cleaned:
        date = cleaned.split('issue date:')[1]
    
    else: 
        print('date',ID,filename)
    date=date.split('\n')[0].split('supersedes')[0].split('version')[0].strip(':. ')
    date = re.sub(' +', ' ', date)
 

    
    #version
    if 'version' in cleaned:
        rev = cleaned.split('version')[1]
    else: 
        print('rev',ID,filename)
    rev=rev.split('\n')[0].split('revision')[0].split('safety')[0].split('print')[0].strip(':. ')
    rev = re.sub(' +', ' ', rev)
        
        
    #Raw category
    if 'recommended use and restrictions on use' in cleaned:
        cat = cleaned.split('recommended use and restrictions on use')[1]
    elif 'recommended use of the chemical and restrictions on use' in cleaned:
        cat = cleaned.split('recommended use of the chemical and restrictions on use')[1]
    # else:
    #     print('raw category',ID,filename)
    cat = cat.split('restrictions')[0]
    cat = (cat).replace('recommended use','').replace('use of the substance/mixture','').replace('\n',' ').strip(':.- ')
    cat = cat.split(':')[0].strip(':.- ')
    cat = re.sub(' +', ' ', cat)
 
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'information on ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on ingredients')[1:])
    else: print('sec3',ID,filename)
    sec3=sec3.split('section 4')[0].split('section4')[0].split('4. first')[0]
    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    
    for line in lines:
        
        line=line.strip()
        if line==prodname: continue
        
        
        if any(x in line for x in ['revision date','this mixture does not contain','safety data sheet','according to federal register','name :','product identifier','full text of hazard','substance type :','29cfr 1910.1200','substance cas registry','this material is not hazardous','royalene 505, 510,','this product in not','communication standard','hazardous components cas no']):     
            continue #skip these lines
        
        if line in ['3.1. substances','3.2. mixtures','not applicable','0','8','591']: 
            continue
        
        if line.split(' ')[0]=='cas-no.': continue
        
        endwords = ['not classified',' acute','flam.','eye irrit','repr. 1b','skin irrit','repr.','aquatic','stot se','(central','skin sens','asp. tox','m-factor','met. corr','stot re','skin corr','press. gas','eye dam','inhalation','oral ate','dermal ate','carc.','h332','comb. dust']
        for word in endwords:
            line=line.split(word)[0].strip()
        
        line = line.replace('110553-27- ','110553-27-0 ')
        line = line.replace('112926-00- ','112926-00-8 ')
        if line=='': continue
    
        
        
        casrns = findcas(line)

        if len(casrns)==1:
            centC.append(line.split(casrns[0])[-1].strip())
            chem.append(line.split(casrns[0])[0].replace('cas-no.','').replace('()','').strip(' :'))
            cas.append(casrns[0])
            components.append('')
        
        elif len(casrns)==0 and len(chem)>0:
            chem[-1]=(chem[-1]+' '+line).strip()
        else:
            print(ID,line)

    
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = chem[c].replace('\n',' ').strip(' ,.:')
        chem[c] = re.sub(' +', ' ', chem[c])
        cas[c] = cas[c].replace('\n',' ').strip(' ,.:')
        cas[c] = re.sub(' +', ' ', cas[c])
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip()
        if '~' in centC[c] and '-' not in centC[c] and centC[c][0] != '~':
            centC[c]=centC[c].replace('~','-')
        if 'ppm' in centC[c]:
            unit.append('4')
            centC[c]=centC[c].replace('ppm','').strip()
        elif centC[c] != '':
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
        components = ['']
        
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
    componentList.extend(components)
    
    if chem == ['']:
        rankList.extend([''])
    else:
        rankList.extend(list(range(1,n+1)))
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})

df.to_csv('lion extracted text.csv',index=False, header=True)
