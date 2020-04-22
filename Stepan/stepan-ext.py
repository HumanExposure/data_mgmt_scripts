# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 11:25:58 2020

@author: MHORTON
"""

#Import packages

import os, string, re
import pandas as pd
import pickle
from glob import glob

originalpath = os.getcwd()

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

    dfs = pd.DataFrame(columns = ['data_document_filename', 'title', 'doc_date', 'rev_num',
                                  'raw_category', 'unit_type', 'component', 'chems'])
    problems = []
    for file in fileList:

        pdf = file.split('.')[0] + '.pdf'
        inChem = False
        inProdID = False
        count = 0
        
        ifile = open(file, encoding = 'utf8')
        
        chem = []
        prodname = ''
        rev_date = ''
        rev_num = ''
        
        for line in ifile:
            
            cline = cleanLine(line)
            if cline == '': continue
        
            #GET PRODUCT ID HERE
            if inProdID == True:
                sline = splitLine(line)
                if 'other means of identification' in cline: #Out of identifier section
                    inProdID = False
                    continue
                if count == 1 and inProdID == True:
                    prodname = prodname + ' ' + sline[-1]
                elif 'sku#' in sline[-1] and inProdID == True:
                    prodname = sline[-2]
                elif inProdID == True:
                    prodname = sline[-1]
                    count += 1
                    
            if '1. identification' in cline: #In the ingredients section
                inProdID = True

            # Get raw category, aka general use of product
            if 'recommended use' in cline:
                sline = splitLine(line)
                raw_category = sline[1]
            
            # Get document date and version number
            if 'issue date' in cline:
                sline = splitLine(line)
                doc_date = sline[1]
#                print(file, 'doc_date', doc_date)
            if rev_num == '':
                if 'revision date' in cline and 'version' in cline:
                    sline = splitLine(line)
                    rev_date = sline[-3].split(' ')[-1]
                    rev_num = sline[-4].split(' ')[-1]
#                    print(file, 'rev date and num', rev_date, rev_num) 
                
            #GET INGREDIENT DATA HERE
            if inChem == True:
                if 'first-aid' in cline or 'composition comments' in cline: #Out of ingredient section
                    inChem = False
                    continue
                if 'material id' in cline or 'material name' in cline or 'designates' in cline or 'chemical name' in cline: #Header/footer/unneccessary lines
                    continue
                sline = splitLine(line)
                sline = [str(x) for x in sline]

                try:
                    if len(sline) == 1:
                        if len(chem) == 0:
                            chem.append(sline)
                        else:
                            chem[len(chem)-1][0] = chem[len(chem)-1][0] + ' ' + sline[0]
                    elif len(sline) == 2:
                        if 'other' in sline[0] or len(chem) == 0:
                            chem.append(sline)
                        else:
                            chem[len(chem)-1][0] = chem[len(chem)-1][0] + ' ' + sline[0]
                            if 'not applicable' or 'alternate' in sline[1]:
                                chem[len(chem)-1][0] = chem[len(chem)-1][0] + ' ' + sline[0]
                            else: print(file, chem, sline)
                    elif len(sline) == 3:
                        chem.append(sline)
                    elif len(sline) == 4:
                        if 'light' in sline[1]:
                            sline[0] = sline[0] + ' ' + sline[1]
                            del sline[1]
                        else:
                            sline[2] = sline[2] + ' ' + sline[3]
                            del sline[3]
                        chem.append(sline)
                    elif len(sline) == 5:
                        if 'other components' in sline[0]:
                            sline[0] = sline[0] + ' ' + sline[1]
                            sline[2] = sline[2] + ' ' + sline[3] + ' ' + sline[4]
                            del sline[4]
                            del sline[3]
                            del sline[1]
                        else:
                            sline[2] = sline[2] + ' ' + sline[3] + ' ' + sline[4]
                            del sline[4]
                            del sline[3]
                        chem.append(sline)
                    else:
                        print('not caught:', file, len(sline), sline, '\n', chem, '\n\n')
                except: 
#                    print('problem with', file, chem, len(sline), sline, '\n\n')
                    problems.append(file)
                
            if 'chemical name common name and synonyms cas number' in cline: #In the ingredients section
                inChem = True
        
#        print(file, chem)
        component = ''
        unit_type = 3
        
        if rev_num != '':
            doc_date = rev_date

        dfs = dfs.append( { 'data_document_filename' : pdf, 'title' : prodname,
                           'doc_date' : doc_date, 'rev_num' : rev_num, 'raw_category' : raw_category, 'unit_type' : unit_type,
                           'component' : component, 'chems' : chem }, ignore_index = True)

    f = open("pdf-info.pkl","wb")
    pickle.dump(dfs,f)
    f.close()

    return(problems)

# %% 
os.chdir(r'sds') #Folder pdfs are in
pdfs = glob('*.pdf')
nPdfs = len(pdfs)
nTxts = len(glob("*.txt"))
if (nTxts < nPdfs): pdfToText(pdfs)
nTxts = len(glob("*.txt"))
print(nPdfs, nTxts)
if (nTxts == nPdfs):
    fileList = glob("*.txt")
    problems = extractData(fileList)
    dfs = pickle.load(open( "pdf-info.pkl","rb" ) )

problems = list(dict.fromkeys(problems))
os.chdir(originalpath)

# %%
dfs = pickle.load(open( r"sds/pdf-info.pkl","rb" ) )
dfdict = dict(zip(dfs['data_document_filename'], dfs['chems']))

info = pd.DataFrame(columns = ['file', 'rank', 'chem', 'cas', 'amount'])

for k, v in dfdict.items():
    for i in v:
        rank = v.index(i) + 1
        if len(i) == 3:
            chem = i[0]
            cas = i[1].rstrip('*').split(' (')[0]
            if 'levels' in cas:
                cas = ''
            amt = i[2]
            data = {'file':k, 'rank':rank, 'chem':chem, 'cas':cas, 'amount':amt}
            info = info.append(data, ignore_index = True)
        elif len(i) == 2:
            if 'other' in i[0]:
                chem = i[0]
                cas = ''
                amt = i[1]
            else:
                chem = i[0]
                cas = i[1]
                amt = ''
            data = {'file':k, 'rank':rank, 'chem':chem, 'cas':cas, 'amount':amt}
            info = info.append(data, ignore_index = True)
        
        else:
            print(k, len(i), i)
            continue
# %% Fix ingredient ranking for multiline chemicals
lastrank = 1

for index, row in info.iterrows():
    file = row['file']
    rank = row['rank']
    if rank != 1:
        if rank != (lastrank + 1):
            print(row)
            row['rank'] = lastrank + 1
    lastfile = row['file']
    lastrank = row['rank']

# %%
amount = info['amount'].tolist()

centrals = []
minimums = []
maximums = []

for i in amount:
    i = i.strip('%')
    if '-' not in i and '<' not in i and '>' not in i:
        central = i
        minimum = ''
        maximum = ''
    elif '-' in i and '<' not in i and '>' not in i:
        central = ''
        minimum = i.split('-')[0].strip(' ')
        maximum = i.split('-')[1].strip(' ')
    elif '-' in i and '<' in i and '>' not in i:
        central = ''
        minimum = i.split('- <')[0].strip(' ')
        maximum = i.split('- <')[1].strip(' ')
    elif '-' not in i and '<' in i:
        central = ''
        minimum = '0'
        maximum = i.split('<')[1].strip(' ')
    elif '>' in i:
        central = ''
        minimum = i.split('>')[1].strip(' ')
        maximum = '100'
    else:
        print(i)
        pass
        
    centrals.append(central)
    minimums.append(minimum)
    maximums.append(maximum)

# %% Make Registered Records CSV

#url = 'https://www.stepan.com/Products/Product-Finder.aspx'
#os.chdir(r'sds') #Folder pdfs are in
#pdfs = glob('*.pdf')
#os.chdir(originalpath)
#
#os.chdir(r'csv')
#rrdf = pd.read_csv('registered_documents.csv')
#
#rrdf['filename'] = pdfs
#rrdf['title'] = dfs['title']
#rrdf['document_type'] = 'SD'
#rrdf['url'] = yrl
#rrdf['organization'] = 'Stepan'
#
#rrdf.to_csv('stepan_registered-records.csv',index=False, header=True)

# %% Make product data CSV

#proddatadf = pd.read_csv('product_csv_template_691.csv')
#id2files = dict(zip(proddatadf['data_document_filename'], proddatadf['data_document_id']))
#
#docs = []
#titles = []
#
#for index, row in dfs.iterrows():
#    if len(row['products_list']) == 0:
#        docs.append(row['data_document_filename'])
#        titles.append(row['title'])
#    if len(row['products_list']) != 0:
#        for x in row['products_list']:
#            docs.append(row['data_document_filename'])
#            titles.append(x)
#
#data_document_filename = [x.split('.')[0] + '.pdf' for x in docs]
#
#proddatadf = pd.DataFrame({'data_document_id':data_document_filename, })
#
#proddatadf = pd.DataFrame({'data_document_id':data_document_filename, 'data_document_filename':data_document_filename, 
#                           'title':titles, 'upc':'', 'url':url, 'brand_name':'', 'size':'',
#                           'color':'', 'item_id':'', 'parent_item_id':'', 'short_description':'', 'long_description':'',
#                           'thumb_image':'', 'medium_image':'', 'large_image':'', 'model_number':'',
#                           'manufacturer':'Stepan' })
#
#proddatadf['data_document_id'] = proddatadf.data_document_filename.replace(id2files) #get doc IDs from template dictionary
#
#proddatadf.to_csv('stepan_product-data.csv',index=False, header=True)
        
# %% Extracted text CSV

#extdf = pd.read_csv('stepan_unextracted_documents.csv')
#file2prod = dict(zip(rrdf['filename'], rrdf['title']))
#file2date = dict(zip(dfs['data_document_filename'], dfs['doc_date']))
#file2rev = dict(zip(dfs['data_document_filename'], dfs['rev_num']))
#file2cat = dict(zip(dfs['data_document_filename'], dfs['raw_category']))
#
#data_document_filename = info['file'].tolist()
#chemicals = info['chem'].tolist()
#cas = info['cas'].tolist()
#
#prod_name = dfs['title']
#cas = [x.rstrip('*') for x in cas]
#chemicals = [x.rstrip('*') for x in chemicals]
#
#extdf = pd.DataFrame({'data_document_id':data_document_filename, 'data_document_filename':data_document_filename, 'prod_name':data_document_filename,
#                   'doc_date':data_document_filename, 'rev_num':data_document_filename, 'raw_category':data_document_filename, 'raw_cas':cas,
#                   'raw_chem_name':chemicals, 'report_funcuse':'', 'raw_min_comp':minimums, 'raw_max_comp':maximums, 'unit_type':int(3),
#                   'ingredient_rank':info['rank'], 'raw_central_comp':centrals, 'component':''})
#    
#extdf['data_document_id'] = extdf.data_document_filename.replace(id2files)
#extdf['prod_name'] = extdf.data_document_filename.replace(file2prod)
#extdf['doc_date'] = extdf.data_document_filename.replace(file2date)
#extdf['rev_num'] = extdf.data_document_filename.replace(file2rev)
#extdf['raw_category'] = extdf.data_document_filename.replace(file2cat)
#
#extdf.to_csv('stepan_extracted-text.csv',index=False, header=True)
