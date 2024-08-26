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
    cline = clean(line.replace('–','-').replace('－','-'))
    cline = cline.replace('–','-').replace('－','-')
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
    
findcas = lambda text: re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",text)
    
    
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
    if row[7].split('_')[0].lower() == 'createx colors':
        filename=row[6]
        ID = row[0]
        if ID in ['1736309','1736310','1749795','1729881']: continue
    else: continue
    

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
    if 'product name and/or code:' in cleaned: 
        prodname = cleaned.split('product name and/or code:')[1]
    elif 'product name:' in cleaned:
        prodname = cleaned.split('product name:')[1]
    elif 'product name' in cleaned:
        prodname = cleaned.split('product name')[1]
    
    prodname = prodname.split('effective date')[0].split('1.2')[0].split('product number')[0].split('other means of identification')[0]
    prodname = prodname.replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if '(updated' in cleaned:
        date = cleaned.split('(updated')[1]
    elif 'revision date:' in cleaned:
        date = cleaned.split('revision date:')[1]
    elif 'effective date:' in cleaned:
        date = cleaned.split('effective date:')[1]
    date=date.split('\n')[0].split('version')[0].replace(prodname,'').replace('manufacturer','').strip('# .):')
    if date == '' and 'original date:' in cleaned: 
        date = cleaned.split('original date:')[1].split('\n')[0].strip('# .):')

        
    #Revision number
    if 'version' in cleaned:
        rev = cleaned.split('version')[1]
    rev=rev.split('issue')[0].split('\n')[0].strip('# .:')
    
    #Raw category
    if 'recommended use' in cleaned: 
        cat = cleaned.split('recommended use')[1]
    elif 'product class:' in cleaned: 
        cat = cleaned.split('product class:')[1]
    elif 'product use:' in cleaned: 
        cat = cleaned.split('product use:')[1]
    cat=cat.split('details of the supplier')[0].split('section ii')[0].split('2. hazards identification')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    if 'of the chemical and restrictions on use' in cat: 
        cat = cleaned.split('recommended use')[2]
    cat=cat.replace('contact your local poison control center.','')
    cat=cat.split('details of the supplier')[0].split('section ii')[0].split('2. hazards identification')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    if '3. composition/information on ingredients' in cleaned: 
        sec3=cleaned.split('3. composition/information on ingredients')[1]
    elif '3.composition/information on ingredients' in cleaned: 
        sec3=cleaned.split('3.composition/information on ingredients')[1]
    elif 'section iii - composition / information on ingredients' in cleaned: 
        sec3=cleaned.split('section iii - composition / information on ingredients')[1]

        
    sec3=sec3.split('4. first')[0].split('4.first')[0].split('section iv')[0].split('the remainder of the formulation is')[0].split('ingredients are marked according to clp regulation')[0].split('if chemical name/cas no is "proprietary"')[0].replace('mixture of the following chemicals:','')
    lines = sec3.split('\n')
    lines = list(filter(None,lines))
    for line in lines:
        if 'this mixture is proprietary' in line or 'this mixture is a proprietary' in line: break #these docs don't have chemicals
        if any(x in line for x in ['substances:','3.1 substances','ntp:','iarc:','pel/tlv (mg/m#):','chemical name cas']): continue #skip these lines
        line=line.strip(' :*').replace('less than','<')
        if line=='': continue
        if line=='ingredient: none': break
        casnums = findcas(line)
        if len(casnums) == 1:
            line=line.replace(casnums[0],'')
            line=line.replace('(cas no. )','').replace('(cas no.: )','').replace('(cas )','').strip()
        else: casnums.append('')
        if 'ingredient:' in line: 
            chem.append(line.split('ingredient:')[-1].strip())
            cas.append('')
            centC.append('')
        elif 'cas#:' in line:
            if cas[-1]=='':
                cas[-1]=line.split('cas#:')[-1].strip()
        elif 'max % weight:' in line:
            if centC[-1] == '':
                centC[-1]='0-'+line.split('max % weight:')[-1].strip()
        else:
            sline = reversed(line.split(' '))
            comp = ''
            for x in sline:
                if all(y in '0123456789-%<>.~=/' for y in x) or (x.strip(' *.') == 'proprietary' and comp == ''):
                    comp = (x+' '+comp).strip()
                else:
                    break
            if line.replace(comp,'').strip()=='' and len(centC)>0:
                centC[-1]=centC[-1]+comp
            else:
                chem.append(line.replace(comp,'').strip())
                cas.append(casnums[0])
                centC.append(comp)
            
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip('- ')
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\createx colors Extracted Text.csv',index=False, header=True)

  