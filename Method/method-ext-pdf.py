# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:09:12 2020

@author: MHORTON
"""

#Import packages

import os, string, re, csv, time, random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import requests
import pickle
from glob import glob
from tabula import read_pdf

originalpath = os.getcwd()

# %%
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
    
# %% Extract PDFs
# get list of PDFs that have been downloaded

try:
    dfs = pickle.load(open( "pdfscrapeDFs.pkl","rb" ) )
except: #Dictionary of PDF scrapes is missing
    os.chdir(r'pdfs')
    pdfs = glob('*.pdf')

    dfs = {}

    for pdf in pdfs:
        try:
            #scrape the PDF
            read = read_pdf(pdf, lattice=True, multiple_tables=True)
            if type(read) is list:
                read = pd.concat(read)
            dfs.update( {pdf : read})
        except:
            #can't scrape the PDF
            print('problem with:', pdf)

    # return to original directory
    os.chdir(originalpath) 

    # Pickle the dictionary
    f = open("pdfscrapeDFs.pkl","wb")
    pickle.dump(dfs,f)
    f.close()

dfkeys = []

for k, v in dfs.items():
    dfkeys.append(k)

# Check if there are new PDFs to extract
os.chdir(r'pdfs')
pdfs = glob('*.pdf')

for pdf in pdfs:
    try:
        if pdf in dfkeys: # Already extracted
            continue
        else:
            #scrape the PDF
            read = read_pdf(pdf, lattice=True, multiple_tables=True)
            if type(read) is list:
                read = pd.concat(read)
            dfs.update( {pdf : read} )
            print(pdf, " extracted.")
    except:
        print('problem with:',pdf)

# return to original directory
os.chdir(originalpath) 

# %%
prods = {}
upcs = {}
names = {}
sdss = {}
dates = {}
lists = {}
manufacturers = {}

for key in dfkeys:
    df = dfs[key]
    df = df[df[0].notna()].reset_index(drop=True)
    for index, row in df.iterrows():
        if 'Product Name' in row[0]:
            prods[key] = row[1]
        if 'UPC' in row[0] and 'allergen' not in row[0]:
            upc = cleanLine(row[1])
            if ('\r') in row[1]:
                upc = ', '.join(upc.splitlines())
            upcs[key] = upc
        if 'Name of Company' in row[0] and type(row[1]) == str:
            names[key] = cleanLine(row[1])
        if 'Link to Safety Data Sheet' in row[0] and type(row[1]) == str:
            sdss[key] = row[1]
        if 'Date of Disclosure' in row[0] and type(row[1]) != float:
            dates[key] = row[1]
        if row[2] == "CAS #":
            inList = True
            start = (index+1)
            end = len(df)
    lists[key] = df[start:end].reset_index(drop=True)

pdfextract = pd.DataFrame(columns = ['file','chem','func','cas', 'rank'])

files = []
chems = []
funcs = []
cass = []
ranks = []

for key in dfkeys:
    file = key
    for index, row in lists[key].iterrows():
        if type(row[1]) is str and type(row[2]) is str:
            files.append(file)
            chem = cleanLine(row[0])
            chems.append(chem)
            func = cleanLine(row[1])
            func = func.replace(';', ',')
            funcs.append(func)
            cas = cleanLine(row[2])
            cass.append(cas)
            rank = index + 1
            ranks.append(rank)

pdfextract['file'] = files
pdfextract['chem'] = chems
pdfextract['func'] = funcs
pdfextract['cas'] = cass
pdfextract['rank'] = ranks

pdfurls = {}
for file in pdfextract['file']:
    pdfurls[file] = 'https://methodhome.com/wp-content/uploads/' + file

# %% Registered Record CSV

rrdf = pd.DataFrame({'filename':files, 'title':files, 'document_type':'ID', 'url':files, 'organization':'method products, pbc.'})
rrdf['title'] = rrdf.title.replace(prods)
rrdf['url'] = rrdf.url.replace(pdfurls)

rrdf = rrdf.drop_duplicates().reset_index(drop=True)

rrdf.to_csv("method-pdf-registered-records.csv",index=False, header=True)

# %% Make product data CSV

proddatadf = pd.read_csv('method_pdf_registered_documents.csv')

file2id = dict(zip(proddatadf['filename'], proddatadf['DataDocument_id']))

data_document_filename = pdfextract['file'].tolist()

proddatadf = pd.DataFrame({'data_document_id':data_document_filename, 'data_document_filename':data_document_filename, 
                           'title':data_document_filename, 'upc':data_document_filename, 'url':data_document_filename,
                           'brand_name': 'method', 'size':'', 'color':'', 'item_id':'', 'parent_item_id':'',
                           'short_description':'', 'long_description':'', 'thumb_image':'', 'medium_image':'',
                           'large_image':'', 'model_number':'', 'manufacturer':data_document_filename })

proddatadf['data_document_id'] = proddatadf.data_document_filename.replace(file2id) #get doc IDs from template dictionary
proddatadf['title'] = proddatadf.data_document_filename.replace(prods)
proddatadf['upc'] = proddatadf.data_document_filename.replace(upcs)
proddatadf['url'] = proddatadf.data_document_filename.replace(pdfurls)
proddatadf['manufacturer'] = proddatadf.data_document_filename.replace(names)

proddatadf = proddatadf.drop_duplicates()

proddatadf.to_csv('method-pdf_product-data.csv',index=False, header=True)

# %% Extracted text CSV

extdf = pd.DataFrame({'data_document_id':data_document_filename, 'data_document_filename':data_document_filename, 'prod_name':data_document_filename,
                   'doc_date':data_document_filename, 'rev_num':'', 'raw_category':'', 'raw_cas':pdfextract['cas'].tolist(),
                   'raw_chem_name':pdfextract['chem'].tolist(), 'report_funcuse':pdfextract['func'].tolist(), 'raw_min_comp':'', 'raw_max_comp':'',
                   'unit_type':'', 'ingredient_rank':pdfextract['rank'].tolist(), 'raw_central_comp':'', 'component':''})

extdf['data_document_id'] = extdf.data_document_filename.replace(file2id)
extdf['prod_name'] = extdf.data_document_filename.replace(prods)
extdf['doc_date'] = extdf.data_document_filename.replace(dates)

extdf.to_csv('method-pdf_extracted-text.csv',index=False, header=True)
