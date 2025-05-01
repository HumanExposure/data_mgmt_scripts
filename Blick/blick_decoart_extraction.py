import os, string, csv, re
import pandas as pd
from glob import glob
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('','').replace('','')
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
        
  
    
    config = r'--psm 3 -c preserve_interword_spaces=1'
    pytesseract.pytesseract.tesseract_cmd = r'c:\Users\alarger\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    pics = glob("*.jpg")

    for p in files:
        num = p.split('.pdf')[0]
        pages = convert_from_path(p,500, poppler_path = r"C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\poppler-0.68.0_x86\bin")
        image_counter = 1
        
        #Make jpeg of each page
        jpegs = []
        for page in pages: 
            filename = num+"page"+str(image_counter)+"_ocr.jpg"
            if filename not in pics:
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

os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Blick') #Folder pdfs are in
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
unextractedids = []
template = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Factotum_Blick_(M)SDS_(2024)_unextracted_documents_20250410.csv'))
for row in template:
    unextractedids.append(row[0])
    
template = csv.reader(open('C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Blick/Factotum_Blick_(M)SDS_documents_20240705.csv')) 
for row in template:
    if (clean(row[7].split('_')[0].replace(' ','').lower()) in ['decoart', 'paintthetownbynumbers'] and row[0] in unextractedids):
        filename=row[6]
        ID = row[0]
    else: continue
    
    
    if filename == 'file name': continue
    

    file=filename.replace('.pdf','.txt')    
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n')
    if cleaned == '':
        print('blank: ',file)
   
    if 'section' not in cleaned:
        file=file.replace('.txt','_ocr.txt') 
        if file not in fileList: 
            ocrPdf([filename])
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
    if 'trade name (as labeled)' in cleaned: 
        prodname = cleaned.split('trade name (as labeled)')[1]
    elif 'product name:' in cleaned:
        prodname=cleaned.split('product name:')[1]
    else:
        print('prodname',ID,filename)
    prodname = prodname.split('part number')[0].split('product color')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'date of preparation:' in cleaned:
        date = cleaned.split('date of preparation:')[1]
    elif 'date of issue' in cleaned:
        date = cleaned.split('date of issue')[1]
    elif 'creation date' in cleaned:
        date = cleaned.split('creation date')[1]
    else: 
        print('date',ID,filename)
    date=date.split('2. hazard')[0].split('page')[0].split('according to')[0]
    date = clean(date).replace('\n',' ').strip('# .*:,()')
    date = re.sub(' +', ' ', date)
    
    #version
    if 'version:' in cleaned:
        rev = cleaned.split('version:')[1]
    rev = rev.split('date')[0].split('according to')[0].replace('\n',' ')
    rev = rev.replace('\n',' ').strip(':., p')
    rev = re.sub(' +', ' ', rev)
 
    #Raw category
    if 'product use:' in cleaned: 
        cat = cleaned.split('product use:')[1]
    elif 'product description:' in cleaned: 
        cat = cleaned.split('product description:')[1]
    elif 'relevant identified use(s)' in cleaned: 
        cat = cleaned.split('relevant identified use(s)')[1]
    else: print('raw cat',ID,filename)
    cat=clean(cat).split('chemical name')[0].split('1.3')[0].split('1.2')[0]
    cat=cat.replace('\n',' ').strip(':*_ .,')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'information on ingredients' in cleaned:
        sec3=cleaned.split('information on ingredients')[1].split('4. first')[0]
    else: print('sec3',ID,filename)

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
            
        line=line.split('hazard classification')[0].strip()

        
        if any(x in line for x in ['specific colorants and','balance of other ingredients are','concentrations are calculated as a maximum']):
            break #end of ingredient section
        if any(x in line for x in ['cas #','ingredients #','safety data sheet','the product is a mixture','casno.','.1 substances','.2 mixture','exposure, category 2']): 
            continue #skip these lines
        line=line.split('h351')[0].split('h350')[0].split('h372')[0].split('h371')[0].split('h302')[0].split('h411')[0]
        line=line.strip('| ')
        if line in ['#','','# # phrases','# #','ingredients']:
            continue #skip these lines
        
        
        line=line.replace('10f-21-1','107-21-1')
        casrns = findcas(line)  
        
        line=line.replace('up to','<')
        if '<' in line:
            if len(casrns)==0:
                if 'non-hazardous mixture' in line:
                    casrns.append('non-hazardous mixture')
                elif 'mixture' in line:
                    casrns.append('mixture')
            if len(casrns)==1:
                chem.append(line.split(casrns[0])[0].strip())
                cas.append(casrns[0])
                centC.append('<'+line.split('<')[-1].split('a')[0].strip('none '))
            else: 
                chem.append(line.split('<')[0].strip())
                cas.append('')
                centC.append('<'+line.split('<')[-1].split('a')[0].strip('none '))

        else:
            line = line.split('listed')[0].split('risk')[0].split('none')[0].split('phrases')[0].split('exposure')[0]
            line=line.strip('1234567890- ')
            if line == '': continue
            if len(chem)>0:
                chem[-1]=chem[-1]+' '+line
            else:
                print(ID,line)
        
            
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\decoart extracted text.csv',index=False, header=True)
