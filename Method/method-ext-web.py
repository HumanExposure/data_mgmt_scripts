# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:38:09 2020

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

info = pickle.load(open( "method-info.pkl","rb" ) )

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
    

# %% Drop chemical rows with "contains fragrance allergens" as a name
info = info[~info.ingredient.str.contains("contains fragrance allergens")]

# %%
#os.chdir(r'alarger-method-webprint') #Folder web print pdfs are in
#pdfs = glob('*.pdf')
#os.chdir(originalpath)

pdfsdict = {}
picsdict = {}

txtfiles = list(dict.fromkeys(info['file'].tolist()))
for file in txtfiles:
    pdfsdict[file] = file.split('.txt')[0] + '.pdf'
txtsdict = dict((v,k) for k,v in pdfsdict.items())
picfiles = list(dict.fromkeys(info['pic'].tolist()))
for file in picfiles:
    picsdict[file] = file.split('/')[-1]
#    picsdict[file] = file

prods = []
for name in info['name'].tolist():
    if 'method |' in name:
        prods.append(name.split('method | ', 1)[1].replace('|','-'))
        continue
    elif '| method' in name:
        prods.append(name.split(' | method', 1)[0].replace('|','-'))
    else:
        prods.append(name.replace('|','-'))

info['file'] = info.file.replace(pdfsdict)
prods = dict(zip(info['file'].tolist(), prods))
info['name'] = info.file.replace(prods)

#fix functions
funcs = []
functions = info['function'].tolist()
for function in functions:
    func = function.replace(';', ',')
    funcs.append(func)

info['function'] = funcs

# %%Get download date of files scraped, fix function
import datetime
datesdict = {}
os.chdir(r'txts')
for file in txtfiles:
    date = str(datetime.datetime.fromtimestamp(os.path.getmtime(file)))
    date = date.split(' ')[0]
#    print(date)
    datesdict[file] = date
os.chdir(originalpath)

# %%Get ingredient ranks
ranks = []
lastfile = 0
rank = ''

for index, row in info.iterrows():
    file = row[0]
    if row[0] == lastfile:
        rank = rank + 1
        ranks.append(rank)
        lastfile = row[0]
    else:
        rank = 1
        ranks.append(rank)
        lastfile = row[0]

info['rank'] = ranks
        
# %% Registered Record CSV
    
rrdf = pd.DataFrame({'filename':info['file'], 'title':info['file'], 'document_type':'ID', 'url':info['url'], 'organization':'method products, pbc.'})
rrdf = rrdf.drop_duplicates().reset_index(drop=True)

rrdf['title'] = rrdf.title.replace(prods)

rrdf.to_csv("method-web-registered-records.csv",index=False, header=True)

# %% Make product data CSV - Not functional yet, hold off

proddatadf = pd.read_csv('method_web_registered_documents.csv')

file2id = dict(zip(proddatadf['filename'], proddatadf['DataDocument_id']))

#data_document_filename = info['file'].tolist()
#
#proddatadf = pd.DataFrame({'data_document_id':data_document_filename, 'data_document_filename':data_document_filename, 
#                           'title':info['name'], 'upc':'', 'url':info['url'], 'brand_name': 'method', 'size':'', 'color':'',
#                           'item_id':'', 'parent_item_id':'', 'short_description':'', 'long_description':info['desc'], 'thumb_image':'',
#                           'medium_image':'', 'large_image':info['pic'], 'model_number':'', 'manufacturer':'method products, pbc.' })
#
#proddatadf['data_document_id'] = proddatadf.data_document_filename.replace(file2id) #get doc IDs from template dictionary
#proddatadf['title'] = proddatadf.data_document_filename.replace(prods)
##proddatadf['large_image'] = proddatadf.large_image.replace(picsdict)
#
#proddatadf = proddatadf.drop_duplicates()
#
#proddatadf.to_csv('method-web_product-data.csv',index=False, header=True)

# %% Extracted text CSV

extdf = pd.read_csv('extracted_text_template.csv')

extdf = pd.DataFrame({'data_document_id':info['file'], 'data_document_filename':info['file'], 'prod_name':info['name'],
                   'doc_date':info['file'], 'rev_num':'', 'raw_category':'', 'raw_cas':'',
                   'raw_chem_name':info['ingredient'], 'report_funcuse':info['function'], 'raw_min_comp':'', 'raw_max_comp':'',
                   'unit_type':'', 'ingredient_rank':info['rank'], 'raw_central_comp':'', 'component':''})
    
extdf['data_document_id'] = extdf.data_document_id.replace(file2id)
extdf['doc_date'] = extdf.doc_date.replace(txtsdict)
extdf['doc_date'] = extdf.doc_date.replace(datesdict)

extdf.to_csv('method-web_extracted-text.csv',index=False, header=True)
