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
        


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Univar') #Folder pdfs are in
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
template = csv.reader(open('Factotum_Univar_SDS_unextracted_documents_20250724.csv')) 
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
        cleaned=cleaned.replace('\n ','\n')
      
    
    if 'dow.com' not in cleaned.replace(' ',''): 
        continue
    # i+=1
    # print(i, filename)
    if ID in ['1797763']: continue
   
  
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
    subchem=''
    subcas=''
    
    
    #Product name
    if 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
    else:
        print('prodname',filename)
    prodname = prodname.split('recommended use')[0].split('product code')[0].split('issue date')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ') 
    prodname = re.sub(' +', ' ', prodname)
 
    
    #Date 
    if 'date of first issue' in cleaned:
        print('date',ID,filename)
        date = cleaned.split('date of first issue')[0]
        date=date.split('\n')[-1].strip(':. ')
        rev=date.split(' ')[0]
        date=date.split(' ')[1]
        date = re.sub(' +', ' ', date)
    elif 'issue date' in cleaned:
        date = cleaned.split('issue date')[1]
        date=date.split('\n')[0].strip(':. ')
        date = re.sub(' +', ' ', date)
    else: 
        print('date',ID,filename)
    
        
        
    #Raw category
    if 'identified uses' in cleaned: 
        cat = cleaned.split('identified uses')[1].split('company identification')[0]
    else:
        print('raw category',filename)
    cat = clean(cat).replace('\n',' ').strip(':. ')
    cat = cat.split('we recommend')[0].strip(':. ')
    cat = re.sub(' +', ' ', cat)
 
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'information on ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on ingredients')[1:])
    elif 'component casrn concentration' in cleaned:
        sec3='\n'.join(cleaned.split('component casrn concentration')[1:])
    else: print('sec3',ID,filename)
    sec3=sec3.split('4. first')[0].split('description of first aid')[0]
    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    

    for line in lines:
        
        line=line.strip()
        
        if line == 'note':
            break
        
        if 'first aid measures' in line: 
            break
                
                
        if any(x in line for x in ['synonyms:','component casrn','page ','product name:','issue date','this product is a','casrn:','substance name:','contains no hazardous ingredients','trademark of the dow','company of dow','chemical nature:']):     
            continue #skip these lines
        

        casrns = findcas(line)
        if len(casrns) == 0 and 'trade secret' in line: 
            casrns.append('trade secret')
        elif len(casrns) == 0 and 'not required' in line: 
            casrns.append('not required')
        elif len(casrns) == 0 and 'not assigned' in line: 
            casrns.append('not assigned')
        elif len(casrns) == 0 and 'not hazardous' in line: 
            casrns.append('not hazardous')
        elif len(casrns) == 0 and 'not available' in line: 
            casrns.append('not available')
        elif len(casrns) == 0 and '556-6 7-2' in line: 
            casrns.append('556-6 7-2')
            
        if len(casrns)==1:
            # print(ID,filename,line)
            centC.append(line.split(casrns[0])[-1])
            chem.append(line.split(casrns[0])[0])
            cas.append(casrns[0])
        
        elif len(casrns)==0 and len(chem)>0:
            if ('%' in line or 'ppm' in line) and all(x in '1234567890. <>=-%pm' for x in line):
                centC[-1]=centC[-1]+' '+line
            else:
                chem[-1] = chem[-1] + ' ' + line
        else:
            print(ID,filename,line)
  
     
    #chem and cas if sds is for a substance, not mixture
    if len(chem)==0:
        if 'substance name:' in cleaned: 
            subchem = cleaned.split('substance name:')[1]
        elif 'synonyms:' in cleaned: 
            subchem = cleaned.split('msynonyms:')[1]
        elif 'chemical nature:' in cleaned: 
            subchem = cleaned.split('chemical nature:')[1]
        else:
            print('synonym',ID,filename)
            
        subchem=subchem.split('casrn')[0].split('this product is a mixture')[0].split('trademark')[0].split('page ')[0]
        
        if 'casrn:' in cleaned:
            subcas = cleaned.split('casrn:')[1]
            subcas = subcas.split('component')[0].split('contains no hazardous')[0].split('trademark')[0].split('page ')[0]
        
        subchem = clean(subchem).replace('\n',' ').strip(':. ')
        subchem = re.sub(' +', ' ', subchem)  
        centC.append('')
        chem.append(subchem)
        cas.append(subcas)
        # print(ID,filename,'substance',subchem)
    
    
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

df.to_csv('Univar Dow extracted text.csv',index=False, header=True)
