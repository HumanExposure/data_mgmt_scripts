# -*- coding: utf-8 -*-
"""
@author: CLUTZ01
"""


import string, re, time, random, requests, os, csv
import glob as gb
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import html5lib
from tqdm import tqdm


# %% Line Cleaning Function
def cleanLine(line ):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-').replace('<sup>', '').replace('</sup>', ''))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = re.sub(' &amp; ', ' ', cline)
    cline = cline.strip()
    return(cline)



#%%intial data grab

site = 'https://www.whatsinsidescjohnson.com/us/en/fragrances-you-can-trust/our-palette'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="html.parser")


paras = soup.findAll("li")


chemicals = []

for p in paras:
    # print(type(p))
    # p_new = str(p).split('data-uw-original-href="',1)[-1].split('" data')[0]
    if 'col-md' in str(p):
        p_new = str(p).split('<span>',1)[-1].split('</span>', 1)[0]
        chemicals.append(str(p_new))

fragrances = pd.DataFrame({'raw_chem_name':chemicals})

fragrances = fragrances[~fragrances['raw_chem_name'].str.contains('fragrances', case=False)]

# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(fragrances)):
    fragrances["raw_chem_name"].iloc[j]=str(fragrances["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    fragrances["raw_chem_name"].iloc[j]=clean(str(fragrances["raw_chem_name"].iloc[j]))
    if len(fragrances["raw_chem_name"].iloc[j].split())>1:
        fragrances["raw_chem_name"].iloc[j]=" ".join(fragrances["raw_chem_name"].iloc[j].split())


filename = "SC Johnson Fragrance Ingredients"
filename = filename.replace(" ", "").strip().lower()+ ".pdf"





fragrances["data_document_id"]="1784802"
fragrances["data_document_filename"]=filename
fragrances["doc_date"]="7/29/2024"
fragrances["raw_cas"]=""
fragrances["component"]=""
fragrances["raw_category"]=""
fragrances["report_funcuse"]="fragrance"
fragrances["cat_code"]=""
fragrances["description_cpcat"]=""
fragrances["cpcat_code"]=""
fragrances["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\SC Johnson Fragrance Ingredients')
fragrances.to_csv("fragrances.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)
