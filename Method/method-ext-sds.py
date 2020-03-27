# -*- coding: utf-8 -*-

import os, string, csv, re
import pandas as pd
from glob import glob
import pickle

#originalpath = r'L:\\Lab\\HEM\\hortonm\\Georgia Pacific\\'
originalpath = os.getcwd()

os.chdir(originalpath)

# %%
def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    Download xpdf here: https://www.xpdfreader.com/download.html
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\mhorton\\Documents\\xpdf-tools-win-4.02\\xpdf-tools-win-4.02\\bin64\\' #Path to execfile
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

# %%
def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    fileList: a list of the txt file names in the data group
    """

    dfs = pd.DataFrame(columns = ['data_document_filename', 'title', 'products_list', 'doc_date', 'rev_num',
                                  'raw_category', 'unit_type', 'component', 'chems'])
    
    for file in fileList:
        pdf = file.split('.')[0] + '.pdf'
        inChem = False
        
        ifile = open(file, encoding = 'utf8')
        
        chems = []
        prodname = ''
        prodlist = ''
        raw_category = ''
        rev_num = ''
        doc_date = ''

        for line in ifile:
            
            cline = cleanLine(line)
            if cline == '': continue
            
#            #GET PRODUCT ID HERE
            if 'product name' in cline:
#                print(cline)
                if ':' in cline:
                    prodname = cline.split(':')[1].lstrip(' ')
                else:
                    prodname = cline.split('name ')[1].lstrip(' ')
#                print(file, 'prodname: ', prodname)
            
            # Get raw category, aka general use of product
            if 'recommended use' in cline and ':' in cline:
                sline = splitLine(line)
                raw_category = sline[-1]
#                print(file, 'raw_category: ', raw_category)
            
            # Get document date and version number
            if 'version' in cline:
                sline = splitLine(line)
#                print(sline)
                for line in sline:
                    if 'date of issue' in line:
                        doc_date = line.split(': ')[1]
#                        print(file, 'doc_date: ', doc_date)
                    if 'revision' in line:
                        doc_date = line.split(': ')[1]
#                        print(file, 'revised doc_date: ', doc_date)
                    if 'version' in line:
                        rev_num = line.split(': ')[1]
#                        print(file, 'rev_num: ', rev_num)

            #GET INGREDIENT DATA HERE
            if inChem == True:
                if 'first-aid' in cline or 'composition comments' in cline: #Out of ingredient section
                    inChem = False
                    continue
                if 'hazard classes' in cline: #Header/footer/unneccessary lines
                    continue
                sline = splitLine(line)
#                print(len(sline),sline,file)                
                chems.append(sline)                
            if cline == 'name product identifier %': #In the ingredients section
                inChem = True
        
        
        component = ''
        unit_type = 3
        
        dfs = dfs.append( { 'data_document_filename' : pdf, 'title' : prodname, 'products_list' : prodlist,
                           'doc_date' : doc_date, 'rev_num' : rev_num, 'raw_category' : raw_category, 'unit_type' : unit_type,
                           'component' : component, 'chems' : chems }, ignore_index = True)

    f = open("sds-info.pkl","wb")
    pickle.dump(dfs,f)
    f.close()

    return()

# %% 
os.chdir(r'sds') #Folder sds pdfs are in
pdfs = glob('*.pdf')
nPdfs = len(pdfs)
nTxts = len(glob("*.txt"))
if (nTxts < nPdfs): pdfToText(pdfs)
nTxts = len(glob("*.txt"))
#print(nPdfs, nTxts)
if (nTxts == nPdfs):
    fileList = glob("*.txt")  
    extractData(fileList)

os.chdir(originalpath)

# %%
dfs = pickle.load(open( r"sds/sds-info.pkl","rb" ) )
dfdict = dict(zip(dfs['data_document_filename'], dfs['chems']))

info = pd.DataFrame(columns = ['file', 'rank', 'chem', 'cas', 'amount'])

for k, v in dfdict.items():
    for i in v:
        rank = v.index(i) + 1
        if len(i) == 3:
            chem = i[0]
            cas = i[1].split('no.) ')[1].strip(' ')
            amt = i[2]
            data = {'file':k, 'rank':rank, 'chem':chem, 'cas':cas, 'amount':amt}
            info = info.append(data, ignore_index = True)
        if len(i) == 1:
            info['chem'][len(info)-1] += ' ' + i[0]
            continue

# %% Fix ingredient ranking for multiline chemicals
lastrank = 1

for index, row in info.iterrows():
    file = row['file']
    rank = row['rank']
    if rank != 1:
        if rank != (lastrank + 1):
            row['rank'] = lastrank + 1
    lastfile = row['file']
    lastrank = row['rank']

# %%
amount = info['amount'].tolist()

centrals = []
minimums = []
maximums = []

for i in amount:
    if '-' not in i and '<' not in i:
        central = float(i)
        minimum = ''
        maximum = ''
    if '-' in i and '<' not in i:
        try:
            minimum = float(i.split('-')[0])
        except:
            minimum = float(0)
        try:
            maximum = float(i.split('-')[1])
        except:
            maximum = ''
        central = ''
    if '-' not in i and '<' in i:
        minimum = float(0)
        maximum = float(i.split('<')[1])
        central = ''
    if '-' in i and '<' in i:
        minimum = float(i.split('-')[0])
        maximum = float(i.split('<')[1])
        central = ''
#    if 'ph' in i:
#        minimum = ''
#        maximum = ''
#        central = ''
    else:
        pass
        
    centrals.append(central)
    minimums.append(minimum)
    maximums.append(maximum)


# %% Registered Record CSV
pdfs = dfs['data_document_filename'].tolist()

rrdf = pd.read_csv('registered_documents.csv')

urls = []

for pdf in pdfs:
    urls.append('https://methodhome.com/wp-content/uploads/' + pdf)

rrdf['filename'] = dfs['data_document_filename']
rrdf['title'] = dfs['title']
rrdf['document_type'] = 'SD'
rrdf['url'] = urls
rrdf['organization'] = 'method products, pbc'

rrdf = rrdf.drop_duplicates().reset_index(drop=True)

rrdf.to_csv("method-sds-registered-records.csv",index=False, header=True)
