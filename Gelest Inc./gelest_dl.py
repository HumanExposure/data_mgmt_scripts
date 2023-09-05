# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 14:52:09 2023

@author: CLUTZ01
"""


import string, re, time, random, requests, os, csv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

from tqdm import tqdm


# %% Line Cleaning Function
def cleanLine(line ):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-').replace('<sup>', '').replace('</sup>', ''))
    # cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = re.sub(' &amp; ', ' ', cline)
    cline = cline.strip()
    return(cline)



# %% Dictionary filter def
def dictFilter(dictObj, filter_string, bool):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if bool == True:
            if filter_string in key:
                newDict[key] = value
        elif bool == False:
            if filter_string not in key:
                newDict[key] = value
    return newDict



#%%intial data grab


site = 'https://www.gelest.com/product-lines/silanes/?pl_page=1&perpage=400'


hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="html.parser")

soup_txt = print(soup)

paras = soup.findAll("li", {"class": "menu-item"})

paras_text = print(paras)

hrefs = []



for p in paras:
    if 'https://www.gelest.com/product-lines/' in str(p):
        hrefs.append(str(p))




url = []
names = []
prod_lines= {}


for h in hrefs:
    if 'https://www.gelest.com/product-lines/' in h:
        url = h.split('href="')[1].split('">')[0]+'?pl_page=1&perpage=400'
        name = h.split('/">')[1].split('</a>')[0]
        name = cleanLine(name)
        prod_lines[name] = url
        
        
prod_lines = dictFilter(prod_lines, 'featured products', False)
prod_lines = dictFilter(prod_lines, 'treated micro particles', False)
prod_lines = dictFilter(prod_lines, 'substrates', False)



# %% Site Scraping PDFs List


#sites =list(prod_lines.values())

#all_pdfs = {}


sites = list(prod_lines.values())
site_dfs = []

for site in sites:

    

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    
    soup_txt = print(soup)
    
    paras = soup.findAll("ul", {"class": "dropdown-menu"})
    
    
    hrefs = []
    
    
    
    for p in paras:
        if '.pdf"' in str(p):
            hrefs.append(str(p))
    
    url = []
    names = []
    pdfs = {}
    
    for h in hrefs:
        if '.pdf' in h:
            url = h.split('EU English SDS')[1].split('href="')[1].split('" target=')[0]
            name = h.split('EU English SDS')[1].split('sds/')[1].split('_GHS')[0]
            name = cleanLine(name)
            name = name.lower()
            pdfs[url] = name
    pdfs_df = pd.DataFrame(pdfs.items())   
        
    site_dfs.append(pdfs_df)


#gs_pdfs = pd.DataFrame(pdfs.items())
    
gs_pdfs = pd.concat(site_dfs, axis=0, ignore_index=True)


# %% Product Info



#sites =list(prod_lines.values())

#all_pdfs = {}


sites = list(prod_lines.values())
products_dfs = {}

for site in sites:

    
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    
    soup_txt = print(soup)
    
    paras = soup.findAll("a", {"class": "arrow-link btn btn-gray smalltext"})
    
    
    hrefs = []
    
    
    
    for p in paras:
        if '/product/' in str(p):
            hrefs.append(str(p))
    
    url = []
    names = []
    
    
    for h in hrefs:
        if 'Product Details' in h:
            url = h.split('href="')[1].split('"')[0]
            name = h.split('product/')[1].split('/"')[0]
            name = cleanLine(name).lower()
            products_dfs[name] = url



# %% save url and file data

import pickle
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc')
with open('products_dfs.pickle', 'wb') as handle:
    pickle.dump(products_dfs, handle, protocol=pickle.HIGHEST_PROTOCOL)



with open('products_dfs.pickle', 'rb') as handle:
    b = pickle.load(handle)
    

# %%Make Registered Records (move)

#reset index and name columns
gs_pdfs.columns = ['url', 'file_name']


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc')

#set up repeating variables
doctype = ['SD'] * len(gs_pdfs['file_name'])
blanks = [''] * len(gs_pdfs['file_name'])
organization = ['Gelest'] * len(gs_pdfs['file_name'])


#creating needed fields
gs_pdfs['doctype'] = ['SD'] * len(gs_pdfs['file_name'])
gs_pdfs['title'] = gs_pdfs['file_name']
gs_pdfs['file_name'] = gs_pdfs['file_name']+'.pdf'

#compile into dataframe
rrDF = pd.DataFrame({'filename':gs_pdfs['file_name'], 'title':gs_pdfs['title'], 
                      'document_type':gs_pdfs['doctype'], 'url':gs_pdfs['url'], 'organization':organization, 
                      'subtitle':blanks, 'epa_reg_number':blanks, 'pmid':blanks, 
                      'hero_id':blanks})

#cleanup and export as csv
rrDF['title'] = rrDF['title'].apply(cleanLine)
#rrDF = rrDF.drop_duplicates().reset_index(drop=True)
# rrDF.to_csv('gelest_inc-registered-records-v2.csv', index=False, header=True)






