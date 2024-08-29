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
    # cline = cline.lower()
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
    if row[7].split('_')[0].lower() == 'staedtler':
        filename=row[6]
        ID = row[0]
    else: continue
    
    
    if filename == 'file name': continue

    file=filename.replace('.pdf','.txt')    
    ifile = open(file, encoding = 'utf8')
    text = ifile.read()
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    cleaned=cleaned.replace('\n ','\n').replace(' \n','\n').replace('\n\n','\n')

   
  
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
    components=[]
    uses = []
    
    
    

    #Product name
    if 'Article description' in cleaned: 
        prodname = cleaned.split('Article description')[1]
    prodname = prodname.split('Constituents')[0]
    prodname = clean(prodname).replace('Made in Germany','').replace('Made in Italy','').replace('\n',' ').strip(':. ')
    prodname = re.sub(' +', ' ', prodname)
    
  
    
    #Ingredient section:
    sec3=''
    if 'Constituents' in cleaned: 
        sec3=cleaned.split('Constituents')[1].split('Conformity')[0].split('1) Certification for sustainable')[0]
        lines = sec3.split('\n')
        lines = list(filter(None,lines))
        for line in lines:
            line = line.strip()
           
         
            if any(x in line for x in ['PE: polyethylene','PP: polypropylene','PE= polyethylene','PET: polyethylene terephthalate','Not classified as hazardous in accordance','CSTEE','European Scientific Committee','POM: polyoxymethylene','PE = polyethylene','PET = Polyester']):
                continue
            print(ID,line)
            if ':' in line: 
                if line.split(':')[0].strip() not in ['Pen case','Triangular packaging','Refill station 487 17']:
                    component = line.split(':')[0].strip()
                    print(component)
            if line[:5]=='Inks ': 
                component = 'Inks'
                line=line.split('Inks')[-1].strip()
            elif line[:5]=='Clip ': 
                component = 'Clip'
                line=line.split('Clip')[-1].strip()
            elif line[:9]=='Plastics ': 
                component = 'Plastics'
                line=line.split('Plastics')[-1].strip()
            elif line[:7]=='Holder ': 
                component = 'Holder'
                line=line.split('Holder')[-1].strip()
            elif line[:10]=='Packaging ': 
                component = 'Packaging'
                line=line.split('Packaging')[-1].strip()
            elif line[:15]=='Metal-clad tip ': 
                component = 'Metal-clad tip'
                line=line.split('Metal-clad tip')[-1].strip()
            line=line.replace(', e.g.',' e.g.').replace(' / ',',')
            line=line.replace('PEFC','pefc').replace('PP','polypropylene').replace('PS','polystyrene').replace('PET','polyethylene terephthalate').replace('PE','polyethylene').replace('Barrel ','').replace('Cap ','').replace('Tip ','').replace('Sealing ','').replace('PA','nylon').replace('POM','polyoxymethylene').replace('Ink Carrier ','')
            line = line.split(':')[-1].strip()
            if line=='': continue
            line=line.split(',')
            for l in line:
                chem.append(l.strip())
                components.append(component)
                
           
    
    #clean up concentrations and names    
    for c in range(0,len(chem)): 
        minC.append('')
        maxC.append('')
        centC.append('')
        cas.append('')
        chem[c]=chem[c].replace('1)','').replace('2)','')
        chem[c] = re.sub(' +', ' ', chem[c])
        centC[c]=centC[c].replace('%','').replace('/','').replace('*','').strip()
        if centC[c] != '' or maxC[c]!='' or minC[c]!='':
            unit.append('3')
        else:
            unit.append('')
        if '-' in centC[c]:
            minC[c] = centC[c].split('-')[0].strip('> ')
            maxC[c] = centC[c].split('-')[1].strip(' <')
            centC[c] = ''
        if components[c] in ['Filler','Binding agent','Colouring agent']:
            uses.append(components[c])
        else:
            uses.append('')
 
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
    useList.extend(uses)
    minList.extend(minC)
    maxList.extend(maxC)
    unitList.extend(unit)
    centList.extend(centC)
    componentList.extend(components)
    rankList.extend(['']*n)
    

   
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
df=df.drop_duplicates()
df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\blick uploads\Staedtler Extracted Text.csv',index=False, header=True)

  