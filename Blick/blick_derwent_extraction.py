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
    line=line.replace('é','e').replace('≤','<=').replace('≥','>=')
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
    if row[7].split('_')[0].lower() == 'derwent':
        filename=row[6]
        ID = row[0]
    else: continue
    
    if ID in ['1727138','1739480','1729894','1733329','1733331','1758808','1758792','1756724','1756207','1753890','1751221','1747970','1747878','1745463']: continue
    
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
    if 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
    prodname = prodname.split('synonym')[0].split('product code')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'revision date' in cleaned:
        date = cleaned.split('revision date')[1]
    else:
        dates = re.findall('\d{2}[/-]\d{2}[/-]\d{4}',cleaned)
        if len(dates) > 0: date=dates[0]
    date=date.split('version')[0].split('\n')[0].strip('# .:')

    #Version
    if 'version:' in cleaned:
        rev= cleaned.split('version')[1]
    elif 'revision:' in cleaned:
        rev= cleaned.split('revision:')[1]
        if rev.count('-')>0:
            rev= cleaned.split('revision:')[2]
    rev=rev.split('\n')[0].split('replaces')[0].strip('# -.:')

    #Raw category
    if 'identified use(s)' in cleaned: 
        cat = cleaned.split('identified use(s)')[1]
    elif 'use of the substance/mixture' in cleaned: 
        cat = cleaned.split('use of the substance/mixture')[1]
    cat=clean(cat).split('uses advised against')[0].split('1.2')[0].split('1.3')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'section 3' in cleaned: 
        sec3=cleaned.split('section 3')[1].split('section 4')[0].split('contains no non-classified vpvb substances')[0]
  
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            # print(ID,line)
            if betweenPages == True:
                if 'safety data sheet' in line:
                    betweenPages=False
                continue
            if 'page:' in line or 'item numbers' in line or 'www.acco.co.uk' in line:
                betweenPages=True
                continue
            if any(x in line for x in ['composition/information','page','3.1 substances','3.2 mixtures','item numbers','safety data sheet','for full text of','derwent','3.1. substance','3.2. mixture','according to regulation','this mixture does not contain','pictogram(s)']):
                continue
            if ('chemical name' in line or 'ingredient' in line) and 'cas' in line: continue
    
            if line.strip()==date: continue
            line = line.split('not classified')[0].split('skin corr')[0].split('flam. sol.')[0].split('water-react')[0].split('acute tox')[0].split('eye dam')[0].split('stot se')[0].split('skin irrit')[0].split('eye irrit')[0].split('aquatic acute')[0].split('skin sens')[0].split('euh014')[0].split('press. gas')[0].strip()
            if line=='': continue
            if line.strip(' .') == 'not applicable': continue
            if all(x in '1234567890- x:.' for x in line): continue
            if 'contains no hazardous ingredients' in line: continue
            if line=='pigments:': 
                # use='pigments'
                continue
            casrns = findcas(line)
            ecs = findecs(line)
            reachs = findreachs(line)
            if len(ecs)==1: line=line.replace(ecs[0],'')
            if len(reachs)==1: line=line.replace(reachs[0],'')

            if len(casrns) == 1:
                chem.append(line.split(casrns[0])[0].strip())
                cas.append(casrns[0])
                centC.append(line.split(casrns[0])[-1].strip())
            elif len(chem)>0:
                chem[-1] = (chem[-1]+' '+line).strip()
            else:
                print('help',ID,line)
      
        
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Derwent Extracted Text.csv',index=False, header=True)

  