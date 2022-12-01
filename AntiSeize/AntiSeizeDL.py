# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:01:11 2022

@author: MHORTON
"""

#Import packages

import string, re, time, random, requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pdfkit
config = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
import pathlib
root = pathlib.PurePath(__file__).parent

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
    cline = re.sub(' &amp; ', ' ', cline)
    cline = cline.strip()
    return(cline)
    
# %% Site Scraping PDFs List

site= 'https://www.antiseize.com/alphabetically-msds'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="lxml")

paras = soup.find_all('p')

hrefs = []

for p in paras:
    if '.pdf"' in str(p):
        hrefs.append(str(p))

urls = []
names = []
pdfs = {}

for h in hrefs:
    if '.pdf' in h:
        url = 'https://www.antiseize.com' + h.split('<a href="')[1].split('" target="_blank">')[0]
        name = h.split('.pdf" target="_blank">')[1].split('</a></p>')[0].replace('<span style="color: #ff0000;">','').replace(' </span></p>','').replace('</a>','').replace('</span>','')
        url = cleanLine(url)
        name = cleanLine(name)
        pdfs[url] = name

# %%  Download PDFs

path = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AntiSeize/pdfs/'

for url, name in pdfs.items():
    random.seed()
    wait = 6 + 3 * random.random()
    time.sleep(wait)
    response = requests.get(url)
    file = path + url.split('/')[-1]
    with open(file, 'wb') as f:
        f.write(response.content)
