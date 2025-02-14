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
    if clean(row[7].split('_')[0].replace(' ','').lower()) in ['mayco']:
        filename=row[6]
        ID = row[0]
    else: continue
    
    if ID in ['1761830','1730306','1747815','1761832','1747559']: continue
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
    if 'product identification:' in cleaned: 
        prodname = cleaned.split('product identification:')[1]
    elif 'material name' in cleaned: 
        prodname = cleaned.split('material name')[1]
    elif 'product id#:' in cleaned:
        prodname = cleaned.split('product id#:')[1]
    else: continue #some documents are scanned and need ocr
    prodname = prodname.split('company information')[0].split('product us')[0].split('product description')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    
    #Date
    if 'updated:' in cleaned:
        date = cleaned.split('updated:')[1]
    elif 'last revision date:' in cleaned:
        date = cleaned.split('last revision date:')[1]
    elif 'prepared:' in cleaned:
        date = cleaned.split('prepared:')[1]
    elif 'reviewed on' in cleaned:
        date = cleaned.split('reviewed on')[1]
    date = date.replace('wednesday','').replace('16:49','')
    date=date.split('item number')[0].split('prepared by')[0].split('1 identi')[0].split('print')[0].split('reviewed')[0].strip('# .*:')
    
    #version
    if 'version' in cleaned:
        rev = cleaned.split('version')[1].split('reviewed on')[0].strip()
 
 
    #Raw category
    if 'product usage:' in cleaned: 
        cat = cleaned.split('product usage:')[1]
    elif 'product use:' in cleaned: 
        cat = cleaned.split('product use:')[1]
    cat=clean(cat).split('product id')[0].split('details')[0].split('manufacturer')[0].replace('\n',' ').strip(': .,')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'section 3:' in cleaned:
        sec3=cleaned.split('section 3:')[1].split('section 4:')[0]
    elif '3 composition' in cleaned:
        
        i+=1
        sec3=cleaned.split('3 composition')[1].split('4 first')[0]
    elif 'section iii' in cleaned: 
        sec3=cleaned.split('section iii')[1].split('section iv')[0]
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
        
        if any(x in line for x in ['composition/information','ingredients cas # ranges','each glaze family contain proprietary mixtures','classified as non-hazardous','hazardous ingredients cas','information on ingredient','chemical characterization: mixtures','mixture of the substances listed below','contd. on page','contd. of page','product id#:','h335','description:','h227','nlp','h332','exposure','h311']): 
            continue #skip these lines
        
        if line in ['none','- hazardous ingredients','pel/tlv max','us','acc. to osha hcs','safety data sheet']: 
            continue #skip these lines
        
        
        if 'einecs' in line:
            line=line.split('einecs')[0].strip()
            if line=='': continue
            
        if 'rtecs' in line:
            line=line.split('rtecs')[0].strip()
            if line=='': continue
            
        casrns = findcas(line)
        if len(casrns) == 0:
            if 'varies' in line:
                chem.append(line.split('varies')[0].strip())
                cas.append('varies')
                centC.append('varies'.join(line.split('varies')[1:]).strip())
            elif 'n/a' in line:
                chem.append(line.split('n/a')[0].strip())
                cas.append('n/a')
                centC.append('n/a'.join(line.split('n/a')[1:]).strip())
            elif len(chem)>0:
                chem[-1]=chem[-1]+' '+line
            else:
                print(ID,line)
                
  
        elif len(casrns) == 1:
            if '1302-78-91' in line:
                casrns[0] = '1302-78-91'
            chem.append(line.split(casrns[0])[0].strip())
            cas.append(casrns[0])
            centC.append(line.split(casrns[0])[-1].strip())
        else:
            print(ID,line)
      
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\mayco extracted text.csv',index=False, header=True)
