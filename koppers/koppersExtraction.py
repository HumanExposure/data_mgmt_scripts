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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=').replace('','').replace('','').replace('®','')#.replace('α','alpha').replace('ω','omega').replace('β','beta').replace('γ','gamma')
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
        


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Koppers') #Folder pdfs are in
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
template = csv.reader(open('Factotum_Koppers_SDS_unextracted_documents_20251006.csv')) 
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
    subchem=''
    subcas=''
    betweenPages=False
    
    #Product name
    if 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
        if 'sds id' in prodname: 
            prodname = cleaned.split('product name')[2]
    elif 'material name' in cleaned: 
        prodname = cleaned.split('material name')[1]
        if 'sds id' in prodname: 
            prodname = cleaned.split('material name')[2]
    else:
        print('prodname',ID,filename)
    prodname = prodname.split('synonym')[0].split('chemical name')[0].split('section 1')[0].split('1. product')[0].split('trade name')[0].split('product use')[0]
    prodname = (prodname).replace('\n',' ').strip(':. -') 
    prodname = re.sub(' +', ' ', prodname)
 
    
    #Date 
    if 'revisiondate:' in cleaned.replace(' ',''):
        date = cleaned.replace(' ','').split('revisiondate:')[1]
        
    elif 'issuedate:' in cleaned.replace(' ',''):
        date = cleaned.replace(' ','').split('issuedate:')[1]
    
    else: 
        print('date',ID,filename)
    date=date.split('\n')[0].split('revision')[0].split('safety')[0].split('p')[0].split('c')[0].strip(':. ')
    date = re.sub(' +', ' ', date)
    
    if date =='na':
        if 'issuedate:' in cleaned.replace(' ',''):
            date = cleaned.replace(' ','').split('issuedate:')[1]
        else: 
            print('date',ID,filename)
        date=date.split('\n')[0].split('revision')[0].split('safety')[0].split('p')[0].split('c')[0].strip(':. ')
        date = re.sub(' +', ' ', date)
    
    #version
    if 'version no' in cleaned:
        rev = cleaned.split('version no')[1]
    elif 'revision' in cleaned:
        for x in cleaned.split('revision'):
            x=x.strip()
            if all(y in '1234567890.' for y in x.split(' ')[0]):
                rev = x.split(' ')[0]
    else: 
        print('rev',ID,filename)
    rev=rev.split('\n')[0].split('revision')[0].split('safety')[0].split('print')[0].strip(':. ')
    rev = re.sub(' +', ' ', rev)
        
        
    #Raw category
    if 'description/use' in cleaned:
        cat = cleaned.split('description/use')[1]
    elif 'relevant identified uses' in cleaned:
        cat = cleaned.split('relevant identified uses')[1]
    elif 'product use' in cleaned:
        cat = 'product use'.join(cleaned.split('product use')[1:])
    else:
        print('raw category',ID,filename)
    cat = cat.split('kopper')[0].split('details')[0].split('restrictions')[0]
    cat = (cat).replace('\n',' ').strip(':.- ')
    cat = re.sub(' +', ' ', cat)
 
 
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'information on ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on ingredients')[1:])
    elif 'informationon ingredients' in cleaned:
        sec3='\n'.join(cleaned.split('informationon ingredients')[1:])
    elif 'information on indgredients' in cleaned:
        sec3='\n'.join(cleaned.split('information on indgredients')[1:])
    else: print('sec3',ID,filename)
    sec3=sec3.split('section 4')[0].split('section4')[0].split('4. first')[0]
    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    
    # print(ID,filename)
    for line in lines:
        
        line=line.strip()
        
        
        if any(x in line for x in ['page ','issue date','material name','safety data sheet','_________________','cas component name percent','cas no %','see section above for','see section below for','cas constituent name percent','version no','print date','the specific chemical identity','hazardous ingredients cas #']):     
            continue #skip these lines
        
        if 'component related regulatory information' in line: break
        if 'legend:' in line: break
        if 'notes:' in line: break
        
        if 'the above listed complex substance contains' in line or line=='not available as' or 'a complex hydrocarbon mixture which includes' in line or 'a complex substance containing' in line: #components
            if len(chem)==1:
                component=chem[-1]
            elif len(chem)>1:
                component=', '.join(chem)
            else: print('component',chem,ID,filename,line,ifile)
            rank=1
            continue
        
        if line in ['following constituents','substances','mixtures','continued...','wood','applications)','further information','not available constituents']: continue
        
        # print(line)
        
        if line[0]=='*': continue
 
    #     # print(ID,filename,line,ifile)
        
        
        casrns = findcas(line)
        if '85-01-08' in line:
            casrns=['85-01-08']

        if len(casrns)!=1:
            if 'n/a' in line: casrns.append('n/a')
            elif 'proprietary ' in line: casrns.append('proprietary ')
            elif 'not available' in line: casrns.append('not available')
            else:
                print(ID,line)
        
        if len(casrns)==1:
            line=line.replace(casrns[0],'').replace('not available','').strip()
            sline=line.split(' ')
            if all(x in '1234567890<>=-.' for x in sline[-1]) and not all(x in '1234567890<>=-.' for x in sline[0]):
                sline = reversed(sline)
                comp = ''
                for x in sline:
                    if all(y in '0123456789-%<>.~=' for y in x) and x.count('.')<3 and x.count('-')<2:
                        comp = (x+' '+comp).strip()
                    else:
                        break
                comp=comp.strip(' -')
                centC.append(comp)
                chem.append(line.replace('cas','').replace(comp,'').strip())
                cas.append(casrns[0])
                components.append(component)
                ranks.append(rank)
                rank+=1
            elif all(x in '1234567890<>=-.' for x in sline[0]) and not all(x in '1234567890<>=-.' for x in sline[-1]):
                comp = ''
                for x in sline:
                    if all(y in '0123456789-%<>.~=' for y in x) and x.count('.')<3 and x.count('-')<2:
                        comp = (x+' '+comp).strip()
                    else:
                        break
                comp=comp.strip(' -')
                centC.append(comp)
                chem.append(line.replace('cas','').replace(comp,'').strip())
                cas.append(casrns[0])
                components.append(component)
                ranks.append(rank)
                rank+=1
            else: 
                print(casrns)
                print(ID,line)
                comp=''
                centC.append(comp)
                chem.append(line.replace('cas','').replace('trace','').strip())
                cas.append(casrns[0])
                components.append(component)
                ranks.append(rank)
                rank+=1

    
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
        ranks=['']
        
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
    
    # if chem == ['']:
    #     rankList.extend([''])
    # else:
    #     rankList.extend(list(range(1,n+1)))
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})

df.to_csv('koppers extracted text.csv',index=False, header=True)
