import os, string, csv, re
import pandas as pd
from glob import glob


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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
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
    if clean(row[7].split('_')[0].replace(' ','').lower()) in ['smooth-on'] or row[0] in ['1761674','1756986','1755024','1748968']:
        filename=row[6]
        ID = row[0]
        # i+=1
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
    if 'trade name:' in cleaned: 
        prodname = cleaned.split('trade name:')[1]
    elif 'product name and/or code:' in cleaned: 
        prodname = cleaned.split('product name and/or code:')[1]
    elif 'date:' in cleaned: 
        prodname = cleaned.split('date:')[1]
    prodname = prodname.split('1.2')[0].split('relevant')[0].split('effective date')[0].split('smooth-on, inc')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'revision date:' in cleaned:
        date = cleaned.split('revision date:')[1]
    elif 'effective date:' in cleaned:
        date = cleaned.split('effective date:')[1]
    elif 'date prepared:' in cleaned:
        date = cleaned.split('date prepared:')[1]
    elif 'date:' in cleaned:
        date = cleaned.split('date:')[1]
    elif 'date of preparation or latest :' in cleaned:
        date = cleaned.split('date of preparation or latest :')[1]
    date=date.split('version')[0].split('ghs')[0].split('1.2')[0].split('safety data')[0].split('other information')[0]
    date=date.replace('\n',' ').strip('# .:')
    date = re.sub(' +', ' ', date)


    #Version
    if 'version:' in cleaned:
        rev= cleaned.split('version:')[1]
    elif 'revision:' in cleaned:
        rev= cleaned.split('revision:')[1]
    rev=rev.split('\n')[0].split('ghs')[0].split('\n')[0]
    rev=rev.replace('\n',' ').strip('# .:')
    rev = re.sub(' +', ' ', rev)
    
    
    #Raw category
    if 'general use:' in cleaned: 
        cat = cleaned.split('general use:')[1]
    elif 'product use:' in cleaned:
        cat = cleaned.split('product use:')[1]
    elif 'intended use of the product' in cleaned: 
        cat = cleaned.split('intended use of the product')[1]
    cat=clean(cat).split('restrictions on use')[0].split('1.3')[0].split('2. hazards')[0]
    cat=cat.replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if '3.composition' in cleaned:
        sec3=cleaned.split('3.composition')[1].split('4. first')[0]
    elif '\nsection 3' in cleaned: 
        sec3=cleaned.split('\nsection 3')[1].split('section 4')[0]
    
    else: print('help',ID)
    
    if 'mixture of the following chemicals' in sec3 or 'no ingredients are hazardous according to' in sec3: 
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            line = line.replace('mixture of the following chemicals:','')
            line = line.replace('flam. liq. 2','').replace('aspir. tox. 1','').replace('skin irrit.','').replace('hazard classification: carcinogen cat 2','').replace('hazard classification: carcinogen cat 1a','')
            line = line.strip()
           
            if any(x in line for x in ['ingredients are marked according','no ingredients are hazardous','the remainder of the formulation is composed of']):
                break
            if any(x in line for x in ['composition/information','page ','3.1 substances','3.2 mixtures','item numbers','safety data sheet','3.1. substance','3.2. mixture','sds no', 'composition / information','chemical name cas','information on ingredients:','the following ingredients are hazardous','communication standard:','cas component concentration']):
                continue
            if line == prodname:
                continue
        
            casrns = findcas(line)
            if len(casrns) == 1:
                chem.append(line.split(casrns[0])[0].replace('(cas no.','').strip())
                cas.append(casrns[0])
                centC.append(line.split(casrns[0])[-1].strip(') '))
                
            elif all(x in '1234567890. %<>' for x in line):
                centC[-1]=centC[-1]+line
                
            else:
                chem.append(line.split('<')[0].strip())
                cas.append('')
                centC.append('<'+line.split('<')[-1].strip())
        
    else: 
        continue
      
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\smooth on extracted text.csv',index=False, header=True)
