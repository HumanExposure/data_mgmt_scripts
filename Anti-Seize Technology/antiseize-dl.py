# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:09:12 2020

@author: MHORTON
"""

#Import packages

import os, string, re, time, random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from glob import glob

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
    
# %% Site Scraping

# Scrape main product listing
site= 'https://www.antiseize.com/alphabetically-msds'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="lxml")

links = soup.find_all('p')

# %%
hrefs = []

for l in links:
    l = str(l)
    if '.pdf"' in l and 'Discontinued' not in l:
        hrefs.append(l)

# %%
files = []
urls = []
for h in hrefs:
    url = h.split('href="')[1]
    url = 'https://www.antiseize.com' + url.split('"', 1)[0]
    file = h.split('blank">')[1]
    file = cleanLine(file.split('</a>')[0])
    file = file.replace(' ', '-')
    file = file.replace('/', '-')
    if 'span' in file:
        file = file.split('<span')[0]
    urls.append(url)
    files.append(file + '.pdf')

pdfdict = dict(zip(files, urls)) 
# %% Download PDFs
# get list of PDFs that have been downloaded

minTime = 4 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

finished = []
problems = []

os.chdir(r'pdfs')
finished = glob('*.pdf')

data = pdfdict

for k, v in data.items():
    try:
        name = k
        if name in finished:
#            print(name, 'is already downloaded.')
            continue
        site = v
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
        print('problem with:', k, v)
        problems.append(v)
        time.sleep(random.randint(minTime,maxTime))

os.chdir(originalpath)
