import os, string, csv, re
import pandas as pd
from glob import glob


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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=')
    cline = (line.replace('–','-').replace('－','-').replace('’',"'"))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\custom building products') #Folder pdfs are in
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

template = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\custom building products\Factotum_Custom_Building_Products_SDS_registered_documents_20250116.csv')) 
for row in template:
    filename=row[1]
    ID = row[0]
    
    if ID in ['1796541']: continue
    
    if filename == 'filename': continue
    

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
    if 'product name:' in cleaned: 
        prodname = cleaned.split('product name:')[1]
    prodname = prodname.split('product code')[0].split('product use')[0].split('1.2')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'revision date:' in cleaned:
        date = cleaned.split('revision date:')[1]
        date=date.split('version')[0].split('disclaimer')[0].split('section')[0].replace('\n','').strip('# .:')
    if date == 'not applicable' or date == 'n/a':
        date = date = cleaned.split('date of preparation:')[1]
        date=date.split('version')[0].split('disclaimer')[0].strip('# .:')

    #Version
    if 'version:' in cleaned:
        rev= cleaned.split('version:')[1]
    elif 'version #:' in cleaned:
        rev= cleaned.split('version #:')[1]
   
    rev=rev.split('revision')[0].split('prepared')[0].split('trade name')[0].replace('\n','').strip('# -.:')

    #Raw category
    if 'product use:' in cleaned: 
        cat = cleaned.split('product use:')[1]
    elif 'use:' in cleaned:
        cat = cleaned.split('use:')[1]
    cat=clean(cat).split('1.3')[0].split('details of the')[0].split('manufacturer')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'section 3' in cleaned: 
        sec3=cleaned.split('section 3')[1].split('section 4')[0].split('*means that')[0]
  
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            # print(ID,line)
            if line=='': continue
            if line[0] == '*': #footnotes at end of ingredient table
                break
            if betweenPages == True:
                if 'safety data sheet' in line:
                    betweenPages=False
                continue
            if 'page ' in line:
                betweenPages=True
                continue
            if any(x in line for x in ['composition/information','page','3.1 substances','3.1 mixtures','3.2 mixtures','item numbers','safety data sheet','for full text of','3.1. substance','3.2. mixture','this product ','osha hazard communication','no components need','cfr 1910','osha criteria']):
                continue
            if 'composition' in line and 'information' in line: 
                continue
            if ('chemical name' in line or 'ingredient' in line) and 'cas' in line: continue
            
            if 'the exact percentage ' in line: break
            casrns = findcas(line)
            if casrns == [] and 'proprietary' in line: casrns = ['proprietary']
            if len(casrns) == 1:
                chem.append(line.split(casrns[0])[0].strip())
                cas.append(casrns[0])
                centC.append(line.split(casrns[0])[-1].strip())
            elif len(casrns) > 1:
                for c in casrns[1:]: 
                    line = line.replace(c,' ').replace('/',' ')
                casrns=[casrns[0]]
                chem.append(line.split(casrns[0])[0].strip())
                cas.append(casrns[0])
                centC.append(line.split(casrns[0])[-1].strip())
            elif all(x in '1234567890 /' for x in line): 
                betweenPages = True
                continue
            elif line == 'megaflex': continue
            elif len(chem)>0:
                print('check',filename,line)
                chem[-1] = (chem[-1]+' '+line).strip()
            else:
                print('help',filename,line)
            
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        chem[c] = chem[c].strip(' *')
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip()
        if centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip('> ')
            maxC[c] = centC[c].split('-')[1].strip(' <')
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

df.to_csv(r'cbp extracted text.csv',index=False, header=True)
