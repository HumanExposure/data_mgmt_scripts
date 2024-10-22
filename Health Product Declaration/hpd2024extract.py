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
    line=line.replace('™','').replace('ó','o').replace('²','2').replace('ō','o').replace('’',"'").replace('®','').replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=')
    cline = (line.replace('–','-').replace('－','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.replace('\nspace\n','\n')
    cline = cline.strip()
    
    return(cline)


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\hpd download\hpd docs') #Folder pdfs are in
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

template = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\hpd download\Factotum_Health_Product_Declaration_2024_registered_documents_20241017.csv')) 
for row in template:
    file=row[1].replace('.pdf','.txt')
    ID = row[0]
    if file == 'filename': continue
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n')
    if cleaned == '':
        print('blank: ',file)
        continue
   
  
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    use = []
    component = ''
    components = []
    chem = []
    cas = []
    minC = []
    maxC = []
    centC = []
    unit = []
    rank = []
    
    
    

    #Product name
    prodname = cleaned .split('health product')[0].split('by ')[0].replace('\n',' ').strip()
    cat = re.sub(' +', ' ', cat)
    
    #Date
    if 'published date' in cleaned:
        date = cleaned.split('published date')[1]
    elif 'release date' in cleaned:
        date = cleaned.split('release date')[1]
    date=date.split('\n')[0].split('*')[0].strip('# .:')



    #Raw category
    if 'classification:' in cleaned: 
        cat = cleaned.split('classification:')[1]
    cat=cat.split('product description')[0].split('created via')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec2=''
    if '\nsection 2:' in cleaned: 
        sec2=cleaned.split('\nsection 2:')[1].split('section 3')[0]
  
        lines = sec2.split('\n')
        lines = list(filter(None,lines))
      
        inComponent = False
        inChem = False
        componentpercents = False #bool for if components have a percent next to them
        r=0 #rank
        prevline='' #previous line
        if '-standard' in sec2:
            firstcomp = sec2.split('product threshold:')[0].split('material threshold:')[0].split('inventory threshold:')[0].split('-standard')[-1].split('%:')[0]
            firstcomp = firstcomp.replace('\n',' ').strip()
        else: firstcomp = ''
        for line in lines:
            if len(chem)==0 and firstcomp!='':
                component = firstcomp
            line=line.strip()
            if line == '': continue
            if 'collaborative.org' in line and 'id:' not in line and 'standard version' not in line: continue
            if 'created via hpd' in line: continue
            if line == 'undisclosed':
                if len(components)>0 and components[-1]!=component:
                    r=1
                    rank.append(r)
                else:
                    r+=1
                    rank.append(r)
                chem.append('undisclosed')
                cas.append('')
                components.append(component)
            if '%:' in line and line[0]!= '%':
                component = line.split('%:')[0].strip()
                inComponent = True
                componentpercents = True
                continue
            if 'standard version' in line and 'available on the hpd' in line:
                inComponent = True
                continue
            if inComponent == True:
                if 'product threshold' in line or 'material threshold' in line or 'inventory threshold' in line or 'residuals and impurities' in line or 'prosduubcstatnhcreesnhootelds' in line: 
                    inComponent = False
                else: 
                    component = (component + ' ' + line).strip()
                continue
            if ('product threshold:' in line or 'material threshold:' in line or 'inventory threshold:' in line) and componentpercents==False:
                component = prevline
            
            if ' id:' in line:
                if len(use)<len(chem):
                    use.append('')
                if len(centC)<len(chem):
                    centC.append('')
                if len(components)>0 and components[-1]!=component:
                    r=1
                    rank.append(r)
                else:
                    r+=1
                    rank.append(r)
                chem.append(line.split('id:')[0].strip())
                cas.append(line.split('id:')[1].strip())
                components.append(component)
                inChem = True
                continue
            if 'id :' in line:
                if len(use)<len(chem):
                    use.append('')
                if len(centC)<len(chem):
                    centC.append('')
                if len(components)>0 and components[-1]!=component:
                    r=1
                    rank.append(r)
                else:
                    r+=1
                    rank.append(r)
                chem.append(line.split('id :')[0].strip())
                cas.append(line.split('id :')[1].strip())
                components.append(component)
                inChem = True
                continue
            if 'i d:' in line:
                if len(use)<len(chem):
                    use.append('')
                if len(centC)<len(chem):
                    centC.append('')
                if len(components)>0 and components[-1]!=component:
                    r=1
                    rank.append(r)
                else:
                    r+=1
                    rank.append(r)
                chem.append(line.split('i d:')[0].strip())
                cas.append(line.split('i d:')[1].strip())
                components.append(component)
                inChem = True
                continue
            if inChem == True:
                if 'hazard screening' in line or '%:' in line or 'hazard data' in line or 'screening date' in line:
                    inChem = False
                    continue
                else:
                    chem[-1] = (chem[-1] + ' ' + line).strip()
            if '%:' in line and line[0]=='%':
                centC.append(line.split('%:')[1].split('gs')[0].split('greenscreen')[0].strip())
                if len(centC)>len(chem): 
                    if len(components)>0 and components[-1]!=component:
                        r=1
                        rank.append(r)
                    else:
                        r+=1
                        rank.append(r)
                    chem.append('')
                    cas.append('')
                    components.append(component)
            if 'role:' in line and 'product threshold' not in line:
                use.append(line.split('role:')[1].strip())
                if len(use)>len(chem): 
                    if len(components)>0 and components[-1]!=component:
                        r=1
                        rank.append(r)
                    else:
                        r+=1
                        rank.append(r)
                    chem.append('')
                    cas.append('')
                    components.append(component)
            prevline=line
    else:
        print('no sec 2: ',file)
    
    if len(centC)<len(chem): #some files don't list conc for last ingredient
        centC.append('')
           
    if len(use)<len(chem): #some files don't list use for last ingredient
        use.append('') 
    
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        components[c] = re.sub(' +', ' ', components[c])
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
        use = ['']
        rank = ['']
        components = ['']
        
    n = len(chem)
    idList.extend([ID]*n)
    filenameList.extend([file.replace('.txt','.pdf')]*n)
    prodnameList.extend([prodname]*n)
    dateList.extend([date]*n)
    revList.extend([rev]*n)
    catList.extend([cat]*n)
    casList.extend(cas)
    chemList.extend(chem)
    useList.extend(use)
    minList.extend(minC)
    maxList.extend(maxC)
    unitList.extend(unit)
    centList.extend(centC)
    componentList.extend(components)
    rankList.extend(rank)
    
 
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\hpd download\hpd 2024 extracted text.csv',index=False, header=True)


