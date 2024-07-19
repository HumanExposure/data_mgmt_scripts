
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
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)


def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    sline = clean(line.replace('–','-'))
    sline = sline.lower()
    sline = sline.strip()
    sline = sline.split("  ")
    sline = [x.strip() for x in sline if x != ""]
    
    return(sline)


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\3M 2024') #Folder pdfs are in
pdfs = glob("*.pdf")
txts = glob("*.txt")

unconverted = []
for p in pdfs: 
    if p.replace('.pdf','.txt') not in txts:
        unconverted.append(p)
pdfToText(unconverted)

fileList = glob("*.txt")       


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
kit = [] #list of documents that are kits
primarynameList=[] #column for kits that will get deleted

i=0
for file in fileList:
    if file in ['b00012427_sds.txt','b00012435_sds.txt', 'b00015046_sds.txt','b40066200_sds.txt']: continue #these documents have different formats
    i+=1
    # print(i)
    ifile = open(file, encoding = 'utf8', errors='ignore')
    prodname = ''
    revDate = ''
    rev = ''
    cat = ''
    ID = ''
    use = ''
    component = ''
    chem = []
    cas = []
    minC = []
    maxC = []
    centC = []
    unit = []
    primaryname=''
    
            
    inUse = False
    inIngredients = False
    inName = False
    
    ID = ''
    template = csv.reader(open('Factotum_3M_SDS_2024_registered_documents_20240708.csv')) 
    for row in template:
        if row[1] == file.replace('.txt','.pdf'):
            ID = row[0]
            break
    if ID == '':
        continue
        
    for line in ifile:
        
        cline = cleanLine(line)
        if cline == '': continue
            
        if  'product identifier' in cline: 
            if prodname == '':
                prodname = cline.split('identifier')[-1].strip()
                inName = True
                continue
            else: #KIT
                kit.append(file.replace('.txt','.pdf'))
                
                #append lists for previous component
                if chem == []:
                    if primaryname=='': primaryname=prodname
                    prodname = cline.split('identifier')[-1].strip()
                    inName = True
                    continue
    
                    
                    
                for c in range(0,len(chem)): 
                    chem[c] = re.sub(' +', ' ', chem[c])
                    chem[c]=chem[c].strip('* ')
                    minC.append('')
                    maxC.append('')
                    centC[c]=centC[c].replace('%','').strip(' trade secret*')
                    if centC[c] != '':
                        unit.append('3')
                    else:
                        unit.append('')
                    if '-' in centC[c]:
                        minC[c] = centC[c].split('-')[0].strip()
                        maxC[c] = centC[c].split('-')[1].strip()
                        centC[c] = ''
                                  
                if primaryname == '': primaryname=prodname
                n = len(chem)
                idList.extend([ID]*n)
                filenameList.extend([file.replace('.txt','.pdf')]*n)
                prodnameList.extend([prodname]*n)
                dateList.extend([revDate]*n)
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
                primarynameList.extend([primaryname]*n)
                
                if chem == ['']:
                    rankList.extend([''])
                else:
                    rankList.extend(list(range(1,n+1)))
                    
                chem = []
                cas = []
                minC = []
                maxC = []
                centC = []
                unit = []
                
                
                prodname = cline.split('identifier')[-1].replace('(tm)','').replace('tm','').strip()
                inName = True
                continue            
            
        if inName == True:
            if 'other means of identification' in cline or 'recommended use' in cline or 'product identification' in cline or 'id number' in cline:
                inName = False
            else: prodname = (prodname + ' ' + cline.replace('(tm)','').replace('tm','')).strip()
        if 'issue date' in cline and revDate == '':
            revDate = cline.split('issue date')[-1].split('supercedes')[0].strip(': ')
      
        if 'version number' in cline and rev == '':
            rev = cline.split('version number')[-1].strip('#: ')
        if 'recommended use' in cline and 'restrictions' not in cline and cat == '':
            cat = cline.split('recommended use')[-1].strip(': ')
            inUse = True
            continue
        
        
        if inUse == True:
            if 'supplier' in cline or 'restrictions on use' in cline or 'this chemical' in cline:
                inUse = False
            else:
                cat = (cat + ' ' + cline).strip()
                
                
                
        if inIngredients == True: #extract ingredient table
            if cline.strip('_ ')=='': continue
            sline = splitLine(line)
            if 'composition comments' in cline or 'first-aid measures' in cline or 'the specific chemical identity' in cline or 'section 4' in cline or 'njts or njtsrn: new jersey trade secret registry number' in cline or 'any remaining components' in cline:
                inIngredients = False #out of ingredient table
                continue
            if 'page ' in cline or cline.strip().split(' ')[-1].count('/')==2 or '3mtm ' in cline or 'standard abrasivestm' in cline or '(tm)' in cline or 'avagardtm' in cline: 
                continue
            if 'ingredient' in cline and '%' in cline: continue #skip table header
            
  
            if len(sline) == 2:
                casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",cline)
                if len(casrn)==1:
                    sline=[cline.split(casrn[0])[0],casrn[0],cline.split(casrn[0])[-1]]
                elif 'trade secret' in sline[0]:
                    sline=[sline[0].split('trade secret')[0],'trade secret',sline[-1]]
                elif sline[-1]=='*':
                    sline=[sline[0]]
                elif sline[-1] in ['phosphates','complexes','and sodium']:
                    sline=[sline[0]+' '+sline[1]]
                else:
                     print(file,'help',sline)
    
            if len(sline) == 1:
                chem[-1] = chem[-1] + ' ' + sline[0]
                continue
            if len(sline) == 3:
                if sline[1].count('-')!=2 and sline[1].strip(' *') not in ['mixture','trade secret','none','unknown','non-material','mixed']:
                    casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",cline)
                    if len(casrn)==1:
                        chem.append(cline.split(casrn[0])[0])
                        centC.append(cline.split(casrn[0])[1])
                        cas.append(casrn[0])
                    elif len(casrn)==0 and 'mixture' in sline[0]:
                        chem.append(sline[0].split('mixture')[0])
                        centC.append(sline[1]+' '+sline[2])
                        cas.append('mixture')
                    else: print('halp',file, sline)
                else:
                    chem.append(sline[0])
                    centC.append(sline[2])
                    cas.append(sline[1])
            elif len(sline) > 3: 
                fixed=False
                for x in range(0,len(sline)):
                    element = sline[x]
                    if x>0:
                        if (all(y in '1234567890-' for y in element) and element.count('-')==2) or element=='mixture' or element.strip('* ')== 'trade secret' or element=='none' or element=='unknown' or element == 'non-material' or element == 'mixed': 
                            cas.append(element)
                            chem.append(' '.join(sline[:x]))
                            centC.append(' '.join(sline[x+1:]))
                            fixed=True
                            break
                if fixed == False: print('not fixed',ID,sline, file)

                    
            else:
                print(len(sline), file, sline)
            
            if len(cas)>0 and any(x not in '1234567890- *' for x in cas[-1]) and cas[-1].strip(' *') not in ['mixture','trade secret','none','unknown','non-material','mixed']:
                print(file,'bad cas',cas[-1])
                cas[-1] = ''
                
            
        if 'section 3: composition' in cline: 
            inIngredients = True
            
    if chem == []:
        if idList[-1]==ID:continue
        chem = ['']
        cas = ['']
        centC = ['']
        
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        chem[c]=chem[c].strip('* ')
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').strip(' trade secret*')
        if centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip()
            maxC[c] = centC[c].split('-')[1].strip()
            centC[c] = ''
      
    if primaryname == '': primaryname=prodname
    n = len(chem)
    idList.extend([ID]*n)
    filenameList.extend([file.replace('.txt','.pdf')]*n)
    prodnameList.extend([prodname]*n)
    dateList.extend([revDate]*n)
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
    primarynameList.extend([primaryname]*n)
    
    if chem == ['']:
        rankList.extend([''])
    else:
        rankList.extend(list(range(1,n+1)))
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList, 'primary name':primarynameList})
i=-1
for index, row in df.iterrows():
    i+=1
    if row['data_document_filename'] in kit:
        df.loc[i,'component'] = df.loc[i,'prod_name']
        df.loc[i,'prod_name'] = df.loc[i,'primary name']
df=df.drop('primary name',axis=1)
df.to_csv('3m 2024 Extracted Text 3.csv',index=False, header=True)

  