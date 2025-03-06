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
    if (clean(row[7].split('_')[0].replace(' ','').lower()) in ['kwikstix', 'kwikkitz']):
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
   
  
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    use = ''
    component = ''
    rank = 0
    chem = []
    cas = []
    minC = []
    maxC = []
    centC = []
    unit = []
    uses = []
    components = []
    ranks = []
    
    
    

    #Product name
    if 'trade name:' in cleaned: 
        prodname = cleaned.split('trade name:')[1]
    else:
        print('prodname',ID)
        continue #different format
    prodname = prodname.split('1.2')[0].split('1. 2')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'actual revision:' in cleaned:
        date = cleaned.split('actual revision:')[1]
    else: print('date',ID,file)
    date=date.split('actual')[0].split('\n')[0].strip('# .:')

    
    #Revision number
    if 'actual version:' in cleaned:
        rev = cleaned.split('actual version:')[1]
    else: print('version',ID,file)
    rev=rev.split('next')[0].split('\n')[0].strip('# .:')
 
    #Raw category
    if 'identified uses:' in cleaned: 
        cat = cleaned.split('identified uses:')[1]
    else: print('raw cat',ID,file)
    cat=clean(cat).split('uses advised against')[0].split('1.3')[0]
    cat=cat.replace('\n',' ').strip(':*_ .,')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    inColors=False
    if '3. composition' in cleaned:
        sec3=cleaned.split('3. composition')[1].split('4. first')[0]
  
    else: print('sec3',ID,file)

    lines = sec3.split('\n')
    lines = list(filter(None,lines))

    for line in lines:
        if betweenPages == True:
            
            if 'next revision' in line:
                betweenPages=False
            continue
        if 'page' in line or 'item numbers' in line:
            betweenPages=True
            continue
    
    
        if any(x in line for x in ['information on ingredients','substances:','mixtures:','product description:','ingredients cas','sds kwik','r-phrases and h-statements','echa reference no']): 
            
            continue #skip these lines
        if line in ['sl-6 series','31521 solid tempera poster paint -']:
            continue
        
        if line == 'pigment list':
            use='pigment'
            inColors=True
            continue
        
        casrns = findcas(line)
        if len(casrns)!=1: print(ID,line)
        if inColors == True:
            if line.split(' ')[0] == casrns[0]:
                chem.append('')
                cas.append(casrns[0])
                centC.append(line.split('hazardous')[-1].strip())
                uses.append(use)
                components.append(component)
                rank+=1
                ranks.append(rank)
            else:
                rank = 1
                component = line.split(casrns[0])[0].strip()
                chem.append('')
                cas.append(casrns[0])
                centC.append(line.split('hazardous')[-1].strip())
                uses.append(use)
                components.append(component)
                ranks.append(rank)
                
        else:
            chem.append(line.split(casrns[0])[0].strip())
            cas.append(casrns[0])
            centC.append(line.split('hazardous')[-1].strip())
            uses.append(use)
            components.append(component)
            rank+=1
            ranks.append(rank)
                
            
        
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
            maxC[c] = centC[c].split('-')[-1].strip(' <')
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
    useList.extend(uses)
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\kwik extracted text.csv',index=False, header=True)
