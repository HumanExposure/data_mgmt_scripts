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
    if (clean(row[7].split('_')[0].replace(' ','').lower()) in ["carand'ache"]):
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
    chem = []
    cas = []
    minC = []
    maxC = []
    centC = []
    unit = []
    
    
    

    #Product name
    if 'trade name:' in cleaned: 
        prodname = cleaned.split('trade name:')[1]
    elif 'product trade name (as labeled):' in cleaned:
        prodname=cleaned.split('product trade name (as labeled):')[1]
    else:
        # print('prodname',ID)
        continue #these are not machine readable
    prodname = prodname.split('article number')[0].split('1.2')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'validation date' in cleaned:
        date = cleaned.split('validation date')[1]
    elif 'revision:' in cleaned:
        date = cleaned.split('revision:')[1]
    else: print('date',ID,file)
    date=date.split('version')[0].split('\n')[0].strip('# .:')

    
    #Revision number
    if 'version:' in cleaned:
        rev = cleaned.split('version:')[1]
    elif 'version number' in cleaned:
        rev = cleaned.split('version number')[1]
    else: print('version',ID,file)
    rev=rev.split('replaces')[0].split('\n')[0].strip('# .:')
 
    #Raw category
    if 'application of the substance / the mixture' in cleaned: 
        cat = cleaned.split('application of the substance / the mixture')[1]
    elif 'uses:' in cleaned: 
        cat = cleaned.split('uses:')[1]
    else: print('raw cat',ID,file)
    cat=clean(cat).split('uses advised against')[0].split('1.3')[0]
    cat=cat.replace('\n',' ').strip(':*_ .,')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if 'section 3:' in cleaned:
        sec3=cleaned.split('section 3:')[1].split('4. section 4')[0].split('section 4')[0]
  
    else: print('sec3',ID,file)

    lines = sec3.split('\n')
    lines = list(filter(None,lines))

    for line in lines:
        if betweenPages == True:
            if 'safety data sheet' in line or 'validation date' in line:
                betweenPages=False
            continue
        if 'page' in line or 'item numbers' in line:
            betweenPages=True
            continue
    
    
        if any(x in line for x in ['for the full text of the','hazardous components:','substance/mixture','subtance /mixture','composition/information on ingredients','numbers regulation (ce)','classification','additional information:','ingredients number regulation (ce) directives','these mixtures do not contain dangerous substances','revision','name of identification','printing date','einecs:','1967/548/cee','index number:','description','chemical characterisation','components:','version','trade name','subtance/mixture']): 
            continue #skip these lines
        if line.replace('not applicable','').strip() == '': continue

        line=line.replace('acute tox. 4, h302','').replace('ce: 215-410-7 h318, h400, h410','').replace('aquatic chronic 2, h411','').replace('effects in the aquatic environment','').replace('may cause long-term adverse','').replace('very toxic to aquatic organisms,','').replace('risk of serious damage to eyes','').replace('statement r: 41, 50/53','').replace('hazard pictogram(s): xi, n','').replace('cas:','')
        line = line.strip()
        if line == '': continue
        if line in ['23/05/2018']: 
            continue #skip these lines
        
        casrns = findcas(line)
        if len(casrns) == 1:
            cas.append(casrns[0]) 
            line=line.replace(casrns[0],'').strip()
        print(ID,line)
        if line[-1] == '%':
            sline = reversed(line.split(' '))
            comp = ''
            for x in sline:
                if all(y in '0123456789-%<>.~=' for y in x) and len(comp.split(' '))<4:
                    comp = (x+' '+comp).strip()
                else:
                    break
            name=line.split(comp)[0]
            centC.append(comp)
            if len(centC)>len(chem):
                chem.append(name)
            else: chem[-1]=chem[-1]+' '+name
        elif len(chem)== len(centC):
            chem.append(line)
        else:
            chem[-1]=chem[-1]+' '+line
            
        
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\caran d ache extracted text.csv',index=False, header=True)
