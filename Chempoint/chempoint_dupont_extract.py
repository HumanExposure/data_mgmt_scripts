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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('','').replace('','').replace('α','alpha').replace('ω','omega')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
    cline =clean(cline)
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)

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
        


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chempoint\DuPont') #Folder pdfs are in
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
findreachs = lambda text: re.findall("[0-9]{2}\-[0-9]{10}\-[0-9]{2}",text) #finds reach number
    
    
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
template = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chempoint\DuPont\Factotum_Chempoint_DuPont_SDS_unextracted_documents_20260611.csv')) 
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
    if cleaned == '':

        if os.path.isfile((file.replace('.txt','_ocr.txt'))) == False:
            ocrPdf([filename])
       
        ifile = open((file.replace('.txt','_ocr.txt')), encoding = 'utf8')
        text = ifile.read()
        cleaned = cleanLine(text)
        cleaned = re.sub(' +', ' ', cleaned)
        cleaned=cleaned.replace('\n ','\n').replace(' \n','\n')
   
  
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

    
    sec1=''
    if '1. identification' in cleaned:
        sec1=cleaned.split('1. identification')[1].split('2. hazard')[0]
    elif '1.1 product identifier' in cleaned:
        sec1=cleaned.split('1.1 product identifier')[1].split('section 2')[0]
    else:
        print('section 1',ID)    
    
    #Product name
    if 'product name' in sec1: 
        prodname = sec1.split('product name')[1]
    else:
        print('prodname',filename)
    prodname = prodname.split('recommended use')[0].split('product code')[0].split('1.2 relevant')[0].split('chemical name of the substance')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ') 
    prodname = re.sub(' +', ' ', prodname)
 
    
    #Date 
    if 'revision date :' in cleaned:
        date = cleaned.split('revision date :')[1]
        date=date.split('\n')[0].strip(':. ')
        date = re.sub(' +', ' ', date)
    elif 'revision date:' in cleaned:
        date = cleaned.split('revision date:')[1]
        date=date.split('\n')[0].strip(':. ')
        date = re.sub(' +', ' ', date)
    elif 'issue date:' in cleaned:
        date = cleaned.split('issue date:')[1]
        date=date.split('\n')[0].strip(':. ')
        date = re.sub(' +', ' ', date)
    else: 
        print('date',ID,filename)
    
    #Version
    if 'version:' in cleaned:
        rev = cleaned.split('version:')[1]
        rev = rev.split('print date')[0].split('\n')[0].strip(':. ')
        rev = re.sub(' +', ' ', rev)
    elif 'date of last issue:' in cleaned and 'date of first issue' in cleaned:
        rev = cleaned.split('date of last issue:')[1].split('date of first issue')[0].strip()
        rev = rev.split('\n')
        rev = ' '.join(rev[1:]).strip()
        rev = rev.split(' ')[0]
    else: 
        print('version',ID,filename)
        
        
    #Raw category
    if 'identified uses:' in cleaned: 
        cat = cleaned.split('identified uses:')[1]
    elif 'recommended use of the chemical and restrictions on use' in cleaned: 
        cat = cleaned.split('recommended use of the chemical and restrictions on use')[1]
    else:
        print('raw category',filename)
    cat = clean(cat).replace('recommended use','').replace('\n',' ').strip(':. ')
    cat = cat.split('company identification')[0].split('section 2')[0].split('1.3')[0].strip(':. ')
    cat = re.sub(' +', ' ', cat)
 
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    weird=False
    reach=[]
    if 'information on ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on ingredients')[1:])
    else: print('sec3',ID,filename)
    sec3=sec3.split('section 4')[0].split('4. first')[0]
    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    

    for line in lines:
        
        line=line.strip()
        
                
        if any(x in line for x in ['synonyms:','component casrn','page ','product name:','issue date','this product is a','casrn:','substance name:','contains no hazardous ingredients','trademark of the dow','company of dow','chemical nature:','3.2 mixtures','registration concentration component regulation','component cas-no. concentration','1910.1200)','this product is','casrn /','ec-no. /','version','index-no. number','substances with a workplace','3.1 substance','chemical name common name','pbt and vpvb substance','synonym (w/w)','chemical name cas-no','chemical nature :','substance / mixture','component cas no','the actual concentration or concentration range','identification classification','number component to regulation','1272/2008 (clp)','logo trademark of affiliates','number component to gb-clp','this product does not contain','workplace exposure limit at','substance name :','cas-no :']):
                 
            continue #skip these lines
        
        if line in ['mixture','hazardous ingredients','in synthetic oil','grease','secret','synthetic grease','coating) compound','no hazardous ingredients','acute toxicity estimate','in mineral oil','(w/w)']:
            continue
        
        
        if line.split(' ')[0]=='casrn':
            weird=True
        
        if weird==False:
            casrns = findcas(line)
            
            if len(casrns) == 0 and 'not available' in line: 
                casrns.append('not available')
    
                
            if len(casrns)==1:
                centC.append(line.split(casrns[0])[-1])
                chem.append(line.split(casrns[0])[0])
                cas.append(casrns[0])
                
            
            elif len(casrns)==0 and len(chem)>0:
                if ('%' in line or 'ppm' in line) and all(x in '1234567890., <>=-%pm' for x in line):
                    centC[-1]=centC[-1]+' '+line
                else:
                    chem[-1] = chem[-1] + ' ' + line
   
            else:
                print(ID,line)
                
        if weird==True:
            reach = findreachs(line)
            if len(reach)==1: line=line.replace(reach[0],'') #remove reach number from line
            findconc = lambda text: re.findall("[>=]{2}[ ,.0-9]{1,10}[-][ ,.<=0-9]{1,10}",text) #finds concentration
            if 'casrn' in line:
                comp = findconc(line)[0]
                line=line.replace(comp,' ')
                
            endwords = ['not classified',' acute','flam.','eye irrit','repr. 1b','skin irrit','repr.','aquatic','stot se','(central','skin sens','asp. tox','m-factor','met. corr','stot re','skin corr','press. gas','eye dam','inhalation','oral ate','dermal ate','carc.']
            for word in endwords:
                line=line.split(word)[0].strip()
                
            line=line.replace('index -no','index-no')
            
            if len(chem)>len(cas):
                if line.split(' ')[0]=='not':
                    cas.append('not available')
                    line=line.replace('not available','notavailable')
                else:
                    cas.append(line.split(' ')[0])
                
            if line.split(' ')[0]=='casrn': 
                line=line.replace('casrn','').strip(' _-%')
                centC.append(comp)
                chem.append(line.strip())
                inchemname=True
            elif inchemname==True:
                line=' '.join(line.split(' ')[1:])
                line=line.strip(' _%')
                if line=='':
                    inchemname=False
                else:
                    chem[-1]=chem[-1]+' '+line.strip()
                
               
    
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = chem[c].replace('\n',' ').strip(' ,.:')
        chem[c] = re.sub(' +', ' ', chem[c])
        cas[c] = cas[c].replace('\n',' ').strip(' ,.:')
        cas[c] = re.sub(' +', ' ', cas[c])
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').replace('tsc','').strip()
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

df.to_csv('Chempoint dupont extracted text.csv',index=False, header=True)
