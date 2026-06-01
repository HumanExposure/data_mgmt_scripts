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
    # clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('','').replace('','').replace('®','').replace('','')#.replace('α','alpha').replace('ω','omega').replace('β','beta').replace('γ','gamma')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
    # cline =clean(cline)
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
        


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chempoint\BASF') #Folder pdfs are in
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
template = csv.reader(open('Factotum_Chempoint_BASF_SDS_unextracted_documents_20260526.csv')) 
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
    betweenPages=False
    
    #Product name
    if 'product identifier used on the label' in cleaned: 
        prodname = cleaned.split('product identifier used on the label')[1]

    elif 'product identifier' in cleaned: 
        prodname = cleaned.split('product identifier')[1]

    else:
        print('prodname',ID,filename)
    prodname = prodname.split('other means of')[0].split('recommended use')[0].split('the substance')[0].split('chemical name')[0].split('relevant identified')[0]
    prodname = (prodname).replace('$','s').replace('\n',' ').strip(':.~ -') 
    prodname = re.sub(' +', ' ', prodname)
 
    
    #Date 
    if 'revision date' in cleaned:
        date = cleaned.split('revision date')[1]
        
    elif 'date / revised:' in cleaned:
        date = cleaned.split('date / revised:')[1]
    
    else: 
        print('date',ID,filename)
    date=date.split('\n')[0].split('page')[0].split('version')[0].strip(':. |,')
    date = re.sub(' +', ' ', date)
    
    
    #version
    if 'version:' in cleaned:
        rev = cleaned.split('version:')[1]
  
    else: 
        print('rev',ID,filename)
    rev=rev.split('\n')[0].split('product')[0].split('(')[0].split('date')[0].strip(':. |e')
    rev = re.sub(' +', ' ', rev)
        
        
    #Raw category
    if 'recommended use of the chemical and restriction on use' in cleaned:
        cat = cleaned.split('recommended use of the chemical and restriction on use')[1]
    elif 'elevant identified uses of the substance or mixture and uses advised against' in cleaned:
        cat = cleaned.split('elevant identified uses of the substance or mixture and uses advised against')[1]

    else:
        print('raw category',ID,filename) 
    cat = cat.replace('“','"').split('the "recommended use')[0].split('details')[0].split('The “recommended use')[0].split('unsuitable for')[0].split('the recommended use')[0]
    cat = cat.replace('recommended use',', ').replace('relevant identified uses',', ').replace('suitable for use in industrial sector',', ').replace('*','').replace(':','').replace(' , ',', ')
    cat = (cat).replace('\n',' ').strip(':.-| ,*')
    cat = re.sub(' +', ' ', cat)
 
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    chemname=''
    casrn=''
    weight=''
    if 'information on ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on ingredients')[1:])
   
    else: print('sec3',ID,filename)
    sec3=sec3.split('4. first')[0].split('section 4')[0]
    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    
    # # print(ID,filename)
    for line in lines:
        if 'this product does not contain any components' in sec3: break
        line = line.split('skin corr')[0].split('acute tox')[0].split('eye dam')[0].split('skin sens')[0].split('aquatic acute')[0].split('aquatic chronic')[0].split('h318')[0]
        line=line.strip()
        if line=='':continue
        
        if any(x in line for x in ['according to regulation','according to hazardous','synonym:','ghs criteria','lupasol','safety data sheet','cas number weight %','under the referenced regulation','hazards above the','version:','revision date','for the classifications','3.1. substances','3.2. mixtures']):   
            # print(ID,line)  
            continue #skip these lines
        
        if line in ['mixtures','not applicable','substances','chemical nature','hazardous ingredients (ghs)']:   
            # print(ID,line)  
            continue #skip these lines
        
        
        if 'cas number weight %' in sec3:
            casrns = findcas(line)
            if len(casrns)==1:
                line=line.replace(casrns[0],'').replace('not available','').strip()
                sline=line.split(' ')
            
                comp = ''
                for x in sline:
                    if all(y in '0123456789-%<>.~=' for y in x) and x.count('.')<3 and x.count('-')<2:
                        comp = (comp+' '+x).strip()
                    else:
                        break
                comp=comp.strip(' -')
                centC.append(comp)
                chem.append(line.replace(comp,'').strip())
                cas.append(casrns[0])
                components.append(component)
            else:
                chem.append(line)
                centC.append('')
                cas.append('')
                components.append(component)
            # print(ID,line)
        
        else:
            if 'cas number:' in line:
                casrn=line.split('cas number:')[1].strip("' ")
                print(ID,casrn)
                
                centC.append(weight)
                chem.append(chemname)
                cas.append(casrn)
                components.append(component)
               
            
            elif 'content (w/w):' in line:
                weight=line.split('content (w/w):')[1]
                if len(centC) > 0 and centC[-1] =='':
                    centC[-1]=weight
                print(ID,weight)
            else:
                chemname=(chemname+' '+line).strip()
                print(ID,line,file)
                
                
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
    rankList.extend(ranks)
    
    if chem == ['']:
        rankList.extend([''])
    else:
        rankList.extend(list(range(1,n+1)))
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})

df.to_csv('chempoint basf extracted text.csv',index=False, header=True)
