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
template = csv.reader(open('C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Blick/Factotum_Blick_(M)SDS_documents_20240705.csv')) 
for row in template:
    if (clean(row[7].split('_')[0].replace(' ','').lower()) in ["general's",'themasters','ritmo']):
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
        
    if 'section' not in cleaned and 'cas' not in cleaned:
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
    if 'identity (as used on label and list)' in cleaned: 
        prodname = cleaned.split('identity (as used on label and list)')[1]
    else:
        continue
    prodname = prodname.split('section i')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    prodname = prodname.replace('note: blank spaces are not permitted. if','').replace('any item is not applicable, or no','').replace('information is available, the space must be','').replace('marked to indicate that','').replace('administration (non-mandatory form) form approved omb no. 1218-0072 >','').replace('deere blank gna as gg permitted','')
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'date prepared' in cleaned:
        date = cleaned.split('date prepared')[1]
    else: 
        print('date',ID,filename)
    date=date.split('signature')[0]
    date = clean(date).replace('\n',' ').strip('# .*:,()')
    date = re.sub(' +', ' ', date)
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'section ii' in cleaned:
        sec3='\n'.join(cleaned.split('section ii')[1:]).split('section iii')[0].split('physical/chemical characteristics')[0]

    else: print('sec3',ID,filename)

    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    

    for line in lines:
        if betweenPages == True:
            if 'msds for' in line:
                betweenPages=False
            continue
        if 'page' in line or 'item numbers' in line:
            betweenPages=True
            continue
        if 'section' in line: 
            break
        
        line=line.strip()
        if any(x in line for x in ['hazardous ingredients/identity information','physical and chemical characteristics','hazardous components osha acgih','specific chemical identity; common name(s)','no acute or chronic health labeling is required','astm standard','fire and explosion information','vapor pressure','boiling point','vapor density','unusual fire and explosion hazards','special fire fighting procedures','not combustible','general pencil company, inc','not explosive','not explosive','articles, not chemicals','pencil products bearing the pma certification mark','contain no materials in sufficient','evaluation by a medical expert','within the scope of the osha','appearance and odor','solubility in water','chronic health problems','conforms to astm','this product is not considered','communication standard','hazardous ingredients/','chemical name and synonyms']): 
            continue #skip these lines
        
        if line in ['i -','n/a','- hazardous ingredients','%','does not contain latex and lanolin.','(optional)','i - physical data','2.0','0.05']: 
            continue

        if line == 'formula': break
        casrns = findcas(line)
        if len(casrns)==1:
            cas.append(casrns[0])
            chem.append(line.split(' ')[0])
            if all(x in '1234567890.-' for x in line.split(',')[0].split(' ')[-1]):
                centC.append(line.split(',')[0].split(' ')[-1])
            else: centC.append('')
        else:
            words = line.replace('mixed with',',').replace('and','').split(',')
            for w in words:
                chem.append(w.strip())
                cas.append('')
                centC.append('')
        print(ID,line)
  
            
        
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\general pencil co extracted text.csv',index=False, header=True)
