# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 13:34:20 2020

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

# %%
os.chdir(r'pdfs')
pdfs = glob('*.pdf')
os.chdir(originalpath)

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

sdss = []

for key in dfkeys:
    df = dfs[key]
    df = df[df[0].notna()].reset_index(drop=True)
    for index, row in df.iterrows():
        if 'Link to Safety Data Sheet' in row[0] and type(row[1]) == str:
            sdss.append(row[1])
sdss = list(dict.fromkeys(sdss))

f = open("sds-urls.pkl","wb")
pickle.dump(sdss,f)
f.close()

# %% Download PDFs from site

minTime = 4 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

finished = []

directory = r'sds/'

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        finished.append(file)

data = sdss

path = directory #Folder the PDFs should go to 
os.chdir(path)

for row in data:
    try:
        name = row.split('/')[-1]
#         print(name)
        if name in finished:
            print(name, 'is already downloaded.')
            continue
        print(row)
        site = row
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        time.sleep(random.randint(minTime,maxTime))
        output = open(name,'wb')
        output.write(page.read())
        output.close()
        finished.append(name)
        print(name, 'downloaded')
    except:
        print('problem with:',name,row)

os.chdir(originalpath)
