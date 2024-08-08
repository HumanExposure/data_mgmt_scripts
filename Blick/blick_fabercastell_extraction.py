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
    line=line.replace('é','e')
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
    if row[7].split('_')[0].lower() == 'faber-castell':
        filename=row[6]
        ID = row[0]
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
    
    
    if 'modern testing services' in cleaned: 
        continue #skip mts docs


    #Product name
    if 'product identifier' in cleaned: 
        prodname = cleaned.split('product identifier')[1]
    elif 'substance or preparation trade name' in cleaned: 
        prodname = cleaned.split('substance or preparation trade name')[1]
    
    else:
        continue
       
    prodname = prodname.split('recommended use')[0].split('company')[0].split('1.3')[0].split('further trade name')[0]
    prodname = prodname.replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'revision date' in cleaned:
        date = cleaned.split('revision date')[1]
    date=date.split('product')[0].split('page')[0].split('\n')[0].strip('# .:')

    
    
    #Raw category
    if 'use of the substance/mixture' in cleaned: 
        cat = cleaned.split('use of the substance/mixture')[1]
    cat=cat.split('details of the supplier')[0].split('.3')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    if 'cas no components quantity' in cleaned:
        sec3=cleaned.split('cas no components quantity')[1].split('4. first')[0].split('further')[0]
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            line = line.split(' ')
            if line[0]=='c.i.':
                cas.append('')
                chem.append(' '.join(line[:-2]))
                centC.append(line[-2])
            else:
                cas.append(line[0])
                chem.append(' '.join(line[1:-2]))
                centC.append(line[-2])
 
    elif 'the product is no dangerous substance' in cleaned: pass #no chemicals
    elif 'chemical characterization' in cleaned: 
        sec3=cleaned.split('chemical characterization')[1].split('further')[0].split('4. first')[0].split('item number')[0]
        sec3=sec3.replace('the lead consists of','').replace('the shaft is based on','').replace('and',',').replace('water-based ink with','')
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            # print(ID, line)
            line=line.split(',')
            for l in line:
                l=l.strip('. ')
                if l=='preparation': continue
                if l!='':
                    chem.append(l)
                    cas.append('')
                    centC.append('')
    else: 
        pass #no chemicals
        
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\faber castell Extracted Text.csv',index=False, header=True)

  