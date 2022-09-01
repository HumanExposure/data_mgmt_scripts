# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 2022

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
    cline = cline.strip()
    return(cline)
    
# %% Method Site Scraping Products List

# Scrape main product listing
site= 'https://methodhome.com/products/'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = Request(site,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page, features="lxml")

links = soup.find_all('a')

hrefs = []

for l in links:
    hrefs.append(str(l))

produrls = []

for h in hrefs:
    if '/products' in h:
        url = h.split('href="')[1]
        url = url.split('">')[0]
        if url not in produrls:
            produrls.append(url)

# %%  Function for scraping each product page

def pagescrape(site):
    # pause between 6 and 9 seconds
    random.seed()
    wait = 6 + 3 * random.random()
    time.sleep(wait)
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="lxml")
    return soup

# %% Scrape the individual product pages and save as html

htmls = []
names = []
problems = []

for url in produrls:
    names.append(url.split('/')[-2])
    htmls.append(url.split('/')[-2] + '.html')

i=0
for url in produrls:
    try:
        # save each page as a PDF
        fname = names[i] + '.pdf'
        fdir = root / 'pdfs' / fname
        pdfkit.from_url(produrls[i], fdir, configuration=config)
        soup = pagescrape(produrls[i])
        # save an image of each product
        fname = names[i] + '.jpg'
        fdir = root / 'imgs' / fname
        images = soup.select('div img')
        image_url = images[0]['src']
        image = requests.get(image_url).content 
        with open(fdir, 'wb') as handler: 
           handler.write(image)
        # save each page as an HTML
        fname = names[i] + '.html'
        fdir = root / 'htmls' / fname
        with open(fdir, "w", encoding = 'utf-8') as file:
            file.write(str(soup.prettify()))
        del fname, fdir, soup, images, image_url, image
    except:
        # check if there are problems
        print('problem with:',url)
        problems.append(url)
    i+=1