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
i=0

for file in fileList:
    
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
        
    if 'radnor' not in prodtitle: continue #only extract lincoln electric documents    
        
    ifile = open(file, encoding='utf8',errors='ignore')
    text = ifile.read()
    
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    

    if cleaned == '': print(file)
    if 'revision date:' not in cleaned or 'recommended use:' not in cleaned or '3. composition / information on ingredients' not in cleaned: continue #different format
    
    
    prodname = cleaned.split('product name:')[-1].split('product size:')[0].replace('\n',' ').replace('tm','').strip() #get product name
    prodname = re.sub(' +', ' ', prodname) #get rid of extra spaces
    date = cleaned.split('revision date:')[1].strip(': ').split(' ')[0].strip() #get date

    cat = cleaned.split('recommended use:')[1].split('restrictions')[0].replace('\n',' ').strip(': ') #Get raw category
    cat = re.sub(' +', ' ', cat) #get rid of extra spaces
    
    
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    section3 = cleaned.split('3. composition / information on ingredients')[1].split('4. first aid measures')[0].split('composition comments')[0].split('* all concentrations')[0].strip()
    
    lines = section3.split('\n')
    lines = list(filter(None,lines))
    # inIngredients = False
    # betweenPages = False
    for line in lines: #Extract ingredient section
        
        if 'reportable hazardous ingredients' in line or 'sds_north america -' in line or 'revision date:' in line or 'chemical identity' in line: continue
        if line == 'mixtures': continue
        casrn = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",line)
        if len(casrn) == 1:
            chem.append(line.split(casrn[0])[0].strip())
            cas.append(casrn[0])
            centC.append(line.split(casrn[0])[1].strip())
            use.append('')
        else:
            # print(ID,line)
            chem[-1]=chem[-1]+' '+line
       
            
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
        centC[c] = re.sub(' +', ' ', centC[c])
        if centC[c] != '':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip()
            maxC[c] = centC[c].split('-')[1].strip()
            centC[c] = ''


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
df.to_csv(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/airgas radnor extracted text.csv',index=False, header=True)


