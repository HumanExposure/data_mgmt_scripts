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
    line=line.replace('é','e').replace('É','e').replace('²','').replace('≤','<=').replace('≥','>=')
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
    if row[7].split('_')[0].lower() == 'sennelier':
        filename=row[6]
        ID = row[0]
    else: continue
    
    # if ID in []: continue
    
    # if filename not in sfiles: continue
    if filename == 'file name': continue
    #fix 1729632

    file=filename.replace('.pdf','.txt')    
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n')
    if cleaned == '':
        print('blank: ',file)
   
    if 'max sauer sas' not in cleaned: continue
  
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
    
    #Date and version
    if 'version' in cleaned:
        line = cleaned.split('version')[1].split('\n')[0].split('page')[0].strip(' -:')
        if '(' in line:
            rev = line.split('(')[0].strip(' -:')
            date = line.split('(')[-1].strip(' -:)')


    #Raw category
    if 'relevant identified uses of the substance or mixture and uses advised against' in cleaned: 
        cat = cleaned.split('relevant identified uses of the substance or mixture and uses advised against')[1]
    cat=cat.split('1.3')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    ec=0
    betweenPages=False
    inchem=False
    if 'section 3' in cleaned: 
        sec3=cleaned.split('section 3')[1].split('section 4')[0]
        nchems=sec3.count('cas:')
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            line = line.strip()
            if betweenPages == True:
                if 'cas:' in line or 'ec:' in line or 'x %' in line:
                    betweenPages=False
                else: 
                    continue
            if 'page:' in line or 'item numbers' in line:
                betweenPages=True
                continue
            if line.replace(' ','') in ['informationoningredients:','specificconcentrationlimits:']: break
            if any(x in line for x in ['composition/information','identification (ec)','information on ingredients','substance for which maximum workplace','composition:','no substances fulfil the criteria','3.2. mixtures','(full text of h-phrases','infodyne']): continue #these are unimportant lines
            
            
            if inchem == True:
                if 'ec:' in line:
                    ec+=1
                    if ec==2:
                        cas.append('')
                        chem.append('')
                        ec=0
                if 'cas:' in line: 
                    inchem=False
                elif 'ec:' not in line and 'reach:' not in line and 'index:' not in line:
                    line=line.split('skin ')[0].split('m acute')[0].split('aquatic')[0].split('m chronic')[0].split('eye ')[0].split('repr.')[0].split('acute')[0].split('dgr')[0].split('wng')[0].split('stot ')[0].split('ghs0')[0].split('asp.')[0].split('euh')[0].split('h304')[0].split('flam.')[0].split('resp.')[0].split('press.')[0]
                    chem[-1]=(chem[-1]+' '+line).strip()
                    pass
            
            if 'cas:' in line: 
                ec=0
                if len(centC)<len(cas):
                    centC.append('')
                    minC.append('')
                    maxC.append('')
                cas.append(line.split('cas:')[1].strip().split(' ')[0])
                inchem = True
                chem.append('')
            if 'x %' in line: 
                conc=re.findall('[0-9,.]{1,5}[ <=x%]{3,10}[0-9,.]{1,5}',line)
                if len(conc)==1:
                    minC.append(conc[0].split('<')[0].strip())
                    maxC.append(conc[0].split('<')[-1].strip())
                    centC.append('')
        
                
    if len(centC)>len(cas):
        print(ID,'help')
                
    if len(centC)<len(cas):
        centC.append('')
        minC.append('')
        maxC.append('')
    
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\sennelier Extracted Text.csv',index=False, header=True)

  