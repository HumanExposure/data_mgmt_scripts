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
    cline = clean(line.replace('–','-').replace('－','-'))
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
    
casrns = lambda text: re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",text)
findcas = lambda text: re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",text) #finds cas number     
findecs = lambda text: re.findall("[0-9]{3}\-[0-9]{3}\-[0-9]",text) #finds ec number
    
    
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
unextractedids = []
unextracted = csv.reader(open(r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Factotum_Blick_(M)SDS_(2024)_unextracted_documents_20250218.csv'))
for row in unextracted:
    unextractedids.append(row[0])
    
template = csv.reader(open(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Blick/Factotum_Blick_(M)SDS_documents_20240705.csv')) 
for row in template:
    if row[7].split('_')[0].lower() =='jacquard' and row[0] in unextractedids:
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
    
    #Product name
    if 'product identity' in cleaned: 
        prodname = cleaned.split('product identity')[1]
    elif 'product name and/or code' in cleaned: 
        prodname = cleaned.split('product name')[1]
    elif 'product name' in cleaned: 
        prodname = cleaned.split('product name')[1]
    elif 'identification of the mixture' in cleaned: 
        prodname = cleaned.split('identification of the mixture')[1]
    elif 'product identifier' in cleaned: 
        prodname = cleaned.split('product identifier')[1]
    elif 'trade name' in cleaned: 
        prodname = cleaned.split('trade name')[1]
    elif 'product:' in cleaned: 
        prodname = cleaned.split('product:')[1]
    elif 'product :' in cleaned: 
        prodname = cleaned.split('product :')[1]
    elif 'common name' in cleaned: 
        prodname = cleaned.split('common name')[1]
    # else: print('help',ID)
    prodname = prodname.split('alternate names')[0].split('1.2')[0].split('product code')[0].split('other means')[0].split('c. i. name')[0].split('product number')[0].split('contact information')[0].split('utilization')[0].split('product use')[0].split('issue date')[0].split('effective date')[0].split('code')[0].split('product description')[0].split('product type')[0]
    prodname = prodname.replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'revised date' in cleaned:
        date = cleaned.split('revised date')[1]
    elif 'revision date' in cleaned: 
        date = cleaned.split('revision date')[1]
    elif 'issue date' in cleaned: 
        date = cleaned.split('issue date')[1]
    elif 'date revised' in cleaned: 
        date = cleaned.split('date revised')[1]
    elif 'date-revised' in cleaned: 
        date = cleaned.split('date-revised')[1]
    elif 'date of revision' in cleaned: 
        date = cleaned.split('date of revision')[1]
    elif 'date:' in cleaned: 
        date = cleaned.split('date:')[1]
    elif 'date :' in cleaned: 
        date = cleaned.split('date :')[1]
    elif 'revision:' in cleaned: 
        date = cleaned.split('revision:')[1]
    # else: print('help',ID)
    date=date.split('\n')[0].split('issue')[0].split('amendatory')[0].split('print')[0].split('page')[0].strip(' :.')
    if date=='-':
        date=cleaned.split('issue date')[1].split('page')[0].split('\n')[0].strip(' :.')
    
    #Revision number
    if 'revision number' in cleaned:
        rev = cleaned.split('revision number')[1]
    elif 'version' in cleaned:
        rev = cleaned.split('version')[1]
    # else: print('help',ID)
    rev=rev.split('date')[0].split('issue')[0].split('revision')[0].split('\n')[0].strip('# .:')
    
    #Raw category
    if 'identification of the product' in cleaned: 
        cat = cleaned.split('identification of the product')[1]
    elif 'recommended use' in cleaned:
        cat = cleaned.split('recommended use')[1]
    elif 'product use' in cleaned:
        cat = cleaned.split('product use')[1]
    # else: print('help',ID)
    cat = re.sub(' +', ' ', cat)
    cat=cat.split('restrictions on use')[0].split('description')[0].split('chemical family')[0].split('synonym')[0].split('manufacturer')[0].split('manufactured by')[0].split('supplier')[0].split('emergency telephone number')[0].split('restricted')[0].split('recommended restrictions')[0].split('2. hazards identification')[0].split('restricted product use')[0].split('dyes of this type can cause')[0].split('1. substance')[0].split('product class')[0].split('by....')[0].replace('\n',' ').strip(': .')
    
    
    
    
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    
    #No ingredients
    if any(x in cleaned.replace(' ','') for x in ['therearenoingredientspresentwhich','nohazardousingredientspresent','substancenamec.a.s.no.:na','criticalhazardstomanandtheenvironment:non-hazardous','nohazardousmaterialsarecontainedinthisproduct']): 
        #these documents don't have any chemicals
        pass
    elif 'section 3 - composition / information on ingredients' in cleaned:
        sec3 = cleaned.split('section 3 - composition / information on ingredients')[1]
    elif 'section 3. composition/information on ingredients' in cleaned:
        sec3 = cleaned.split('section 3. composition/information on ingredients')[1]
    elif 'section 3: composition/information on ingredients' in cleaned:
        sec3 = cleaned.split('section 3: composition/information on ingredients')[1]
    elif '3. composition/information on ingredients' in cleaned:
        sec3 = cleaned.split('3. composition/information on ingredients')[1]
    elif '3. composition and information on ingredients' in cleaned:
        sec3 = cleaned.split('3. composition and information on ingredients')[1]
    elif '3. composition/informations on ingredients' in cleaned:
        sec3 = cleaned.split('3. composition/informations on ingredients')[1]
    elif '2. composition and information on ingredients' in cleaned:
        sec3 = cleaned.split('2. composition and information on ingredients')[1]
    elif '3. hazardous ingredients' in cleaned:
        sec3 = cleaned.split('3. hazardous ingredients')[1]
    elif '3. composition / information on ingredients' in cleaned:
        sec3 = cleaned.split('3. composition / information on ingredients')[1]
    elif '3. ingredients:' in cleaned:
        sec3 = cleaned.split('3. ingredients:')[1]
    elif '3. ingredients' in cleaned:
        sec3 = cleaned.split('3. ingredients')[1]
    elif '2. composition/informations on ingredients' in cleaned:
        sec3 = cleaned.split('2. composition/informations on ingredients')[1]
    elif '3. compositions/informations on ingredients' in cleaned:
        sec3 = cleaned.split('3. compositions/informations on ingredients')[1]
    elif '3 ingredients' in cleaned:
        sec3 = cleaned.split('3 ingredients')[1]
    else:
        print('sec3',ID)
    sec3=sec3.split('4. first')[0].split('section 4')[0].split('4. emergency')[0].split('3. hazards')[0]
    
    
    lines = sec3.split('\n')
    lines = list(filter(None,lines))

    for line in lines:
        if betweenPages == True: #skip page headers and footers
            if 'msds for' in line:
                betweenPages=False
            continue
        
        if 'page' in line or 'item numbers' in line:
            betweenPages=True
            continue
        
        if line[0]=='*' or any(x in line for x in ['this product has not been tested on animals']): #end of ingredient table
            break
        if 'cas number :' in line: print(ID,line)
        if any(x in line for x in ['gras substance','the exact','resp fraction','osha twa','chemical identity content','composition % by weight cas','chemical identity cas','exact percentages withheld','toxicological data on ingredients','composition: % by weight','chemical name cas','impurities/additives: none','sds','www.jacquardproducts.com','chemical identity %','chemical component concentration','name cas','none known per osha hazard communication standard','rupert, gibbon','other components below reportable levels','concentration shown as a range','and in the concentrations applicable','hence require reporting','substance/mixture','cas number/other identifiers','other means of identification','cas number :','there are no additional ingredients present','occupational exposure limits','component wt','components cas','composition cas','product are hazardous','name product identifier','the specific identity']): 
            continue #skip these lines
        if line in ['percent (%)*','mixtures','as a trade secret.','composition:','(%)*','3.2. mixtures','section ','withheld as a trade secret.','hazardous components: none','chemical characterization: multifunctional polycarbodiimide water emulsion','this product is a mixture.','substance.','percent (%)* weight']: 
            continue #skip these lines
        
        #get rid of ec numbers
        line=line.replace('237-323-33','') #common incorrect ec number
        ecs=findecs(line)
        for e in ecs:
            line=line.replace(e,'')
            
        #skip ghs lines
        if line[:3]=='ghs': continue
            
        #find casrn   
        casrns=findcas(line)
        if len(casrns)>1:
            print('cas',ID,line)
        elif len(casrns)==1:
            line=line.replace(casrns[0],'')
            line=line.replace('( )','').replace('()','').replace('(  )','')
        elif len(casrns)==0 and 'trade secret' in line and line.replace('trade secret','').strip(' .') !='':
            casrns.append('trade secret')
            line=line.replace('trade secret','')
            
        #get rid of acgth-tlv and osha-pel
        if 'ppm' in line: 
            line=line.split('ppm')[0].strip()
            line=' '.join(line.split(' ')[:-1])
            
        line = line.replace(' na ','  ')
        
        if line =='': continue
        
        
        #clean up lines
        badwords = ['n/l','(respiratory system)','may cause long lasting effects to aquatic life','mild eye irritant','may be harmful if swallowed','causes sensitization with skin contact','product can be harmful to aquatic life','eye and respiratory irritant','mild irritant','may cause long-term adverse effects','may cause long-term adverse effects','non-hazardous material','slight eye and skin irritant','category 2b eye irritant','eye irritant','may be harmful if swallowed','causes eye irritation','10 mg/m3','n/a','in vitro mutagen in animal tests','---','aquatic toxicity','irritant',' nr','not available','not hazardous','causes skin irritation','causes serious eye irritation','harmful to aquatic life','non-hazardous','non- hazardous','h411 aquatic chronic 2','h304 asp.tox. 1','h226 flam. liq. 3','h317 skin sens. 1b','h315 skin irrit. 2','h410 aquatic chronic 1','h400 aquatic acute 1','harmful if swallowed','irritating to eyes','harmful to aquatic organisms','c6h8o7xfe3ynh3','skin corr. 1b','possible skin sensitizer','H632','may cause an allergic skin reaction','may cause skin sensitization','toxic to aquatic organisms','may be harmful if','may be','harmful to','may cause eye and','harmful','skin irritation','toxic to aquatic life','to aquatic life with long lasting effects','swallowed','effects in the aquatic environment','in the aquatic environment','eye and skin','animal sensitizer','eye dam. 1','stot se 3','may cause long -term adverse','may cause long-term adverse']
        for b in badwords: 
            line=line.replace(b,'')
        if 'only)' in line:
            line='('.join(line.split('only)')[0].split('(')[:-1])
        
        line=line.rstrip('.,:-= ')
        if len(casrns) == 0 and line in ['']: continue
        
        
        if len(casrns)==0: casrns.append('')
        if '  ' in line:
            chem.append(line.split('  ')[0])
            centC.append(line.split('  ')[-1])
            cas.append(casrns[0])
        elif line in ['nylacrylamide/ vinylamine-hcl(1/1)/ n-vinylformamide (abbreviation:pvfy)','aliph'] and len(chem)>0 and casrns[0]=='':
            chem[-1]=chem[-1]+' '+line
        elif 'd&c green no. 6' in line:
            chem.append('d&c green no. 6')
            centC.append(line.replace('d&c green no. 6',''))
            cas.append(casrns[0])
        elif 'basic blue 41' in line:
            chem.append('basic blue 41')
            centC.append(line.replace('basic blue 41',''))
            cas.append(casrns[0])
        elif 'pigment green 7' in line:
            chem.append('pigment green 7')
            centC.append(line.replace('pigment green 7',''))
            cas.append(casrns[0])
        elif line == 'dyestuff acetic':
            chem[-1] = chem[-1]+' '+line
        elif line == 'acid 1.5%':
            chem[-1] = chem[-1]+' '+'acid'
            centC[-1] = '1.5'
        else: 
            line=line.replace('-',' -')
            sline = reversed(line.split(' '))
            comp = ''
            breaknext=False
            prev=''
            for x in sline:
                if x == '': comp=comp+' '
                elif prev != '' and all(y in ['1234567890.'] for y in prev) and all(y in ['1234567890.'] for y in x):
                    break
                elif all(y in '0123456789-%<>.~=/' for y in x) or (x.strip(' *.') == 'proprietary' and comp == ''):
                    comp = (x+' '+comp).strip()
                    if breaknext==True and all(y in '1234567890' for y in x): 
                        break
                    if '-' in x:
                        breaknext=True
                else:
                    break
                prev=x
            line = re.sub(' +', ' ', line)
            comp = re.sub(' +', ' ', comp)
            chem.append(line.replace(comp,''))
            centC.append(comp)
            cas.append(casrns[0])
  
        
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        chem[c] = re.sub(' +', ' ', chem[c])
        chem[c]=chem[c].strip(' *')
        minC.append('')
        maxC.append('')
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').replace('>/=','>').replace('</=','<').strip()
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Jacquard Extracted Text.csv',index=False, header=True)

  
