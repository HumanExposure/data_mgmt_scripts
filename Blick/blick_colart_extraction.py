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
    line=line.replace('é','e').replace('É','e').replace('À','a').replace('≤','<=').replace('≥','>=')
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
    if clean(row[7].split('_')[0].replace(' ','').lower()) in ['winsor&newton','liquitex','contparis','snazaroo','charbonnel','lefranc&bourgeois']:
        filename=row[6]
        ID = row[0]
        # i+=1
    else: continue
    
    if ID in ['1734200','1752121','1755917','1732034']: continue
    
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
    if 'trade name' in cleaned: 
        prodname = cleaned.split('trade name')[1]
    elif 'name' in cleaned: 
        prodname = cleaned.split('name')[1]
    prodname = prodname.split('1.2.')[0].split('recommended')[0].split('product group')[0].split('other means of')[0].split('type of product')[0].split('product n')[0].split('ufi :')[0]
    prodname = clean(prodname).replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
    #Date
    if 'revision date' in cleaned:
        date = cleaned.split('revision date')[1]
    elif 'issue date' in cleaned:
        date = cleaned.split('issue date')[1]
    elif 'date of issue' in cleaned:
        date = cleaned.split('date of issue')[1]
    else:
        dates = re.findall('\d{2}[/-]\d{2}[/-]\d{4}',cleaned)
        # if len(dates) > 0: 
        print('help',ID,dates)
            # date=dates[0]
    date=date.split('supercedes')[0].split('supersedes')[0].split('version')[0].split('revision')[0].split('sds')[0].split('\n')[0].strip('# .:')

    #Version
    if 'version:' in cleaned:
        rev= cleaned.split('version:')[1]
    elif 'revision:' in cleaned:
        rev= cleaned.split('revision:')[1]
    elif 'revision' in cleaned:
        rev= cleaned.split('revision')[-1]
    rev=rev.split('\n')[0].split('replaces')[0].split('page')[0].split('supersedes')[0].strip('# -.:')

    #Raw category
    if '\nidentified uses' in cleaned: 
        cat = cleaned.split('\nidentified uses')[1]
    elif 'recommended use and restrictions on use' in cleaned:
        cat = cleaned.split('recommended use and restrictions on use')[1]
    elif 'application' in cleaned: 
        cat = cleaned.split('application')[1]
    elif 'use of the substance/mixture' in cleaned: 
        cat = cleaned.split('use of the substance/mixture')[1]
    elif 'main use category' in cleaned: 
        cat = cleaned.split('main use category')[1]
    cat=clean(cat).split('uses advised against')[0].split('1.2')[0].split('1.3')[0].replace('\n',' ').strip(': .')
    cat = re.sub(' +', ' ', cat)
    
    
    #Ingredient section:
    sec3=''
    betweenPages=False
    if '3. composition/information on ingredients' in cleaned:
        sec3=cleaned.split('3. composition/information on ingredients')[1].split('4. first')[0]
    elif 'section 3' in cleaned: 
        sec3=cleaned.split('section 3')[1].split('section 4')[0]

    lines = sec3.split('\n')
    lines = list(filter(None,lines))

    for line in lines:
        if 'name chemical name' in line: 
            print(ID,line)
        if betweenPages == True:
            if 'safety data sheet' in line:
                betweenPages=False
            elif any(x in line for x in ['winsor & newton','liquitex','conte a paris','snazaroo','charbonnel','lefranc & bourgeois']):
                betweenPages=False
            continue
        if 'page' in line or 'item numbers' in line:
            betweenPages=True
            continue
        if any(x in line for x in ['composition/information','page','3.1 substances','3.2 mixtures','item numbers','safety data sheet','for full text of','3.1. substance','3.2. mixture','according to regulation','this mixture does','pictogram(s)','art materials are labelled according','appropriate labelling is listed','full text of hazard class','name :','according to federal register','see section 16','name product identifier','the full text for all','revision date','date de revision','according to the reach regulation','directive 67/548/eec','1272/2008 [clp]','the full text for all hazard statements','3.2. melanges','ce melange ne contient aucune','en (english)','safety information sheet','been created','issue date','according to the hazardous products']): #skip these lines
            continue
        if 'comment' in line or 'note b :' in line or 'note p :' in line or 'section 1:' in line: 
            break
       
        if 'classification' in line:
            continue
        if 'ec number' in line:
            line = line.split('ec number')[0]
        if 'ec index-no' in line:
            line = line.split('ec index-no')[0]
        if 'ec no.:' in line:
            line = line.split('ec no.:')[0]
        if 'ec-no' in line: 
            line = line.split('ec-no')[0]
            if len(line)>0 and line[-1] == '(':
                line=line.strip('( ')
        if 'reach-no:' in line: 
            line = line.split('reach-no:')[0]
        if 'reach registration' in line: 
            line = line.split('reach registration')[0]
        line = line.split('carc.')[0].split('stot se')[0].split('asp. tox')[0].split('flam. liq')[0].split('eye irrit')[0].split('skin irrit')[0].split('aquatic')[0].split('repr.')[0].split('stot re')[0].split('skin sens')[0].split('eye dam')[0].split('skin corr')[0].split('muta.')[0].split('acute tox')[0].split('m factor')[0].split('(note b)')[0]
        if line == prodname: continue
        if 'not classified' in line:
            line = line.split('not classified')[0]
            
        line = line.replace('cas number:','').replace('(cas-no.)','').replace('cas-no.:','')
        line=line.strip()
        if line == '': continue
        if line in ['not applicable','[clp]','regulation (ec) no. 1272/2008','not classified -','2119456809-23-xxxx','2119457558-25-xxxx','2119471991-29xxx','2119463259-31-xxxx','2119455851-35-xxxx','2119457290-43-xxxx','2119471310-51-xxxx','regulation (ec) no.','mixtures','regulations.','non applicable','identifier','2119457736-27-0001']: continue #skip these lines
        
        if 'specific concentration limits' in line:
            break
        
        
        casrns = findcas(line)
        if len(casrns) < 1: #if no cas, go through line backwards to split chem name and conc
            words = reversed(line.split(' '))
            comp = ''
            for x in words:
                if all(y in '0123456789-%<>.~=' for y in x) or (x.strip(' *.') == 'proprietary' and comp == ''):
                    comp = (x+' '+comp).strip()
                else:
                    break
            if comp == '' and len(chem)>0:
                chem[-1] = chem[-1] + ' ' + line
            elif comp == '':
                chem.append(line)
                cas.append('')
                centC.append('')
            else:
                chem.append(line.split(comp)[0])
                cas.append('')
                centC.append(comp)
                
        elif len(casrns) == 1:
            if line.replace(casrns[0],'').strip() == '' and len(cas)>0 and cas[-1] == '':
                cas[-1]=casrns[0]
            else:
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

df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\colart extracted text.csv',index=False, header=True)
