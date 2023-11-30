import os, string, csv, re
import pandas as pd
from glob import glob
from pikepdf import Pdf



def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.03\\bin64\\' #Path to execfile
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
    # clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('–','-').replace('≤','<=').replace('≥','>=')
    cline = cline.lower()
    # cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)





os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/docs')
#Original pdfs give permission errors when reading. Make copies of the pdfs that can be extracted
pdfs = glob("*.pdf")    
uncopied = []
extractable = glob('*new.pdf')
for p in pdfs:
    if 'new' not in p and p.replace('.pdf','_new.pdf') not in extractable:
        uncopied.append(p)
        
for u in uncopied: #Make copies of the pdfs that can be extracted (original copies are secured)
    new_pdf = Pdf.new()
    with Pdf.open(u) as pdf:
        pdf.save(u.replace('.pdf','_new.pdf'))
            
pdfs = glob("*_new.pdf")
txts = glob("*.txt")
unconverted = []
for p in pdfs:  #Convert to txt
    if p.replace('.pdf','.txt') not in txts:
        unconverted.append(p)
pdfToText(unconverted)

fileList = glob("*new.txt") #extract text

#csv columns
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

for file in fileList:
    
    #fields for each document
    prodtitle = ''
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    ID = ''
    filename = ''
    use = []
    component = []
    chem = []
    cas = []
    minC = []
    maxC = []
    centC = []
    unit = []
    
    template = csv.reader(open(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/Factotum_Airgas_HardGoods_documents_20231016.csv')) #Get factotum document ids
    filename = file.replace('_new.txt','.pdf')
    for row in template:
        if row[6] == filename:
            ID = row[0]
            prodtitle = row[7].lower().replace(' ','')
            break
        
    if ID == '':
        continue
        
    if 'eutectic' not in prodtitle: continue #only extract lincoln electric documents    

        
    ifile = open(file, encoding='utf8',errors='ignore')
    text = ifile.read()
    
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    

    if cleaned == '': print(file)
    
    
    prodname = cleaned.split('name of product:')[-1].split('synonyms:')[0].replace('\n',' ').replace('tm','').strip() #get product name
    date = cleaned.split('\n')[2].strip()
    if 'date' in date: date = date.split('2013')[-1].strip()

    if 'product classification:' in cleaned:
        cat = cleaned.split('product classification:')[-1].split('section 2')[0].replace('\n',' ').strip(': ') #Get raw category
    else: 
        cat = cleaned.split('product use:')[-1].split('section 2')[0].replace('\n',' ').strip(': ') #Get raw category
    cat = re.sub(' +', ' ', cat) #get rid of extra spaces
    
    
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    section3 = cleaned.split('section 3: composition/information on ingredients')[1].split('section 4: first aid measures')[0].strip()
    
    lines = section3.split('\n')
    lines = list(filter(None,lines))
    inIngredients = False
    namestart = '' #beginning of a name that goes on to another line
    for line in lines: #Extract ingredient section
        if inIngredients == False: 
            if 'percent ingredients by weight' in line or 'percent ingredients (by weight)' in line or 'number osha pel acgih tlv (by weight )' in line or 'ingredients cas number osha pel acgih -tlv (by weight)' in line: 
                inIngredients = True
                continue
        if inIngredients == True:
            if 'hazard classification' in line: 
                inIngredients = False
                continue
            casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",line)
            if len(casrn) == 1: pass
            elif 'trade secret' in line and 'not hazardous' in line: casrn = ['not hazardous']
            elif 'organic binder' in line and 'n/a' in line: casrn = ['n/a']
            elif '$$$' in line and 'acrylic polymer' in line: casrn = ['$$$']
            elif line.strip() in ['hexafluoroaluminate','tetrahydrate','methacrylate basis)']: #line is end of previous chemical name
                chem[-1] = chem[-1] + ' ' + line.strip()
                continue
            elif line.strip() in ['dimethylamine','potassium pentaborate','potassium pentaborate-','potassium tetraborate','potassium tetraborate-']: #line is beginning of next chemical name
                namestart = (namestart + ' ' + line.strip()).strip()
                continue
            else: 
                print(ID,file,line)
                continue
            if namestart != '': 
                chem.append(namestart+' '+line.split(casrn[0])[0].strip('# '))
            else:
                chem.append(line.split(casrn[0])[0].strip('# '))
            cas.append(casrn[0])
            line=line.replace('-',' ').strip()
            line = re.sub(' +', ' ', line)
            line = line.split(' ')
            centC.append(line[-2]+'-'+line[-1])
            use.append('')

            
    if chem == []:
        chem = ['']
        cas = ['']
        centC = ['']
        use = ['']
  
    for c in range(0,len(chem)): #clean up concentrations and names
        chem[c] = re.sub(' +', ' ', chem[c])
        minC.append('')
        maxC.append('')
        # use.append('')
        component.append('')
        centC[c]=centC[c].replace('%','')
        if 'balance' in centC[c]: centC[c] = ''
        centC[c] = re.sub(' +', ' ', centC[c])
        if 'ppm' in centC[c]: 
            centC[c]=centC[c].replace('ppm','').strip()
            unit.append('4')
        elif centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip()
            maxC[c] = centC[c].split('-')[1].strip()
            centC[c] = ''
        if minC[c] == '<': minC[c] = '0'
        elif maxC[c] == 'minimum': maxC[c] = '100'
        elif maxC[c] == 'max':
            maxC[c] = minC[c]
            minC[c] = '0'
        


    n = len(chem)
    idList.extend([ID]*n)
    filenameList.extend([filename]*n)
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
    componentList.extend(component)
    
    if chem == ['']:
        rankList.extend([''])
    else:
        rankList.extend(list(range(1,n+1)))
   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
df.to_csv(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/airgas eutectic extracted text.csv',index=False, header=True)


