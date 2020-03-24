# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:09:12 2020

@author: MHORTON
"""

#Import packages

import os, string, re, time, random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import pickle
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
    
# %% Method Site Scraping

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

urls1 = []
produrls = []

for h in hrefs:
    if '.com/products' in h:
        urls1.append(h.split('href="')[1])

for u in urls1:
    t = u.split('"><img alt="" class=')[0]
    if 'class' not in t:
        produrls.append(t)
        
# Function for scraping each product page
def pagescrape(site):
    # pause between 4 and 7 seconds
    random.seed()
    wait = 4 + 3 * random.random()
    time.sleep(wait)
    # scrape the page and return the soup to it's can
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page)
    return soup

# %% Parsing the soup
def pageinfo(soup, file):
    
    # Get product name

    name = str(soup.title)
    name1 = name.split('<title>')[1]
    name = name1.split('</title>')[0]
    name = name.strip('\n')
    if '\n' in name:
        name = name.split('\n')[0]
    #     print(name)


    # Get the images of the product

    images = soup.find_all('img')

    pics = []

    for i in images:
        pics.append(str(i))

    pics1 = []

    for p in pics:
        if '<img src=' in p:
            pics1.append(p.split('<img src="')[1])

    pics = []

    for p in pics1:
        pics.append(p.split('"/>')[0])

    # Currently we can only put one picture into Factotum, so choose one
    for p in pics:
        if 'front' in p:
            pic = p
        else:
            pic = pics[0]


    # Get the product description

    desc = ''

    metas = soup.find_all('meta')

    meta = []

    for m in metas:
        meta.append(str(m))

    for m in meta:
        if 'description' in m:
            desc1 = m.split('content="')[1]
            if 'name' in desc1:
                desc = desc1.split('" name')[0]


    # Save ingredient disclosure PDF on each page

    links = soup.find_all('a')

    pdfs = []
    pdf_url = ''
    pdf_filename = ''

    for l in links:
        pdfs.append(str(l))

    for p in pdfs:
        if 'pdf' in p:
            pdf1 = p.split('href="')[1]
            pdf_url = pdf1.split('"', 1)[0]

    try:
        pdf_filename = pdf_url.split('uploads/')[1]
    except:
        pdf_filename = 'none'

    df = pd.DataFrame(columns = ['ingredient', 'function', 'source'])
    rows = list(soup.find_all('tr'))

    for row in rows:
        ingredient = str(row).split('</td>')[0].split('<td class')[1].split('>')[1].strip('\n').strip(' ')
        if '\n' in ingredient:
                ingredient = ingredient.rsplit('\n')[0]
        function = str(row).split('</td>')[1].split('>')[1].strip('\n').strip(' ')
        if '\n' in function:
                function = function.rsplit('\n')[0]
        try:
            source = str(row).split('</td>')[2].split('>')[1].strip('\n').strip(' ')
            if '\n' in source:
                source = source.rsplit('\n')[0]
        except:
            source = ''
        data = {'ingredient':ingredient, 'function':function, 'source':source}
        df = df.append(data, ignore_index = True)

    indexNames = df[ df['ingredient'] == 'ingredient' ].index
    df.drop(indexNames , inplace=True)
    for index, row in df.iterrows():
        if 'updated' in row[0]:
            df.drop(index , inplace=True)
    df = df.reset_index(drop=True)

    # name is product name
    # pic is product picture
    # desc is product description
    # pdf_filename is the filename of the pdf

    files = [file] * len(df)
    names = [name] * len(df)
    pics = [pic] * len(df)
    descs = [desc] * len(df)
    pdf_filenames = [pdf_filename] * len(df)

    labelDF = pd.DataFrame({'file':files, 'name':names, 'pic':pics, 'desc':descs, 'pdf_filename':pdf_filenames})
    labelDF = pd.concat([labelDF, df], axis=1)

    return labelDF

# %% A second parsing method for anomalous pages
def pageinfo2(soup, file):
    
    #### Define a function to get what you need off of each page
    # Get product name

    name = str(soup.title)
    name1 = name.split('<title>')[1]
    name = name1.split('</title>')[0]
    name = name.strip('\n')
    if '\n' in name:
        name = name.split('\n')[0]

        
    # Get the images of the product

    images = soup.find_all('img')

    pics = []

    for i in images:
        pics.append(str(i))

    pics1 = []

    for p in pics:
        if '<img src=' in p:
            pics1.append(p.split('<img src="')[1])

    pics = []

    for p in pics1:
        pics.append(p.split('"/>')[0])

    # Currently we can only put one picture into Factotum, so choose one
    for p in pics:
        if 'front' in p:
            pic = p
        else:
            pic = pics[0]
    

    # Get the product description

    desc = ''

    metas = soup.find_all('meta')

    meta = []

    for m in metas:
        meta.append(str(m))

    for m in meta:
        if 'description' in m:
            desc1 = m.split('content="')[1]
            if 'name' in desc1:
                desc = desc1.split('" name')[0]


    # Save ingredient disclosure PDF on each page

    links = soup.find_all('a')

    pdfs = []
    pdf_url = ''
    pdf_filename = ''

    for l in links:
        pdfs.append(str(l))

    for p in pdfs:
        if 'pdf' in p:
            pdf1 = p.split('href="')[1]
            pdf_url = pdf1.split('"', 1)[0]

    try:
        pdf_filename = pdf_url.split('uploads/')[1]
    except:
        pdf_filename = 'none'

    df = pd.DataFrame(columns = ['ingredient', 'function', 'source'])
    rows = list(soup.find_all('tr'))
    
    if len(rows) == 0:
        print('no ingredient table for:', file)
        data = {'ingredient':'', 'function':'', 'source':''}
        df = df.append(data, ignore_index = True)
    else:
        for row in rows:
            ingredient = str(row).split('</td>')[0].split('>')[-1].strip('\n').strip(' ')
            if '\n' in ingredient:
                    ingredient = ingredient.rsplit('\n')[0]
            function = str(row).split('"column-2">')[1].split('</td>')[0].strip('\n').strip(' ')
            if '\n' in function:
                    function = function.rsplit('\n')[0]
            try:
                source = str(row).split('</td>')[2].split('>')[1].strip('\n').strip(' ')
                if '\n' in source:
                    source = source.rsplit('\n')[0]
            except:
                source = ''
            data = {'ingredient':ingredient, 'function':function, 'source':source}
            df = df.append(data, ignore_index = True)

    indexNames = df[ df['ingredient'] == 'ingredient' ].index
    df.drop(indexNames , inplace=True)
    for index, row in df.iterrows():
        if 'updated' in row[0]:
            df.drop(index , inplace=True)
    df = df.reset_index(drop=True)

    # name is product name
    # pic is product picture
    # desc is product description
    # pdf_filename is the filename of the pdf

    files = [file] * len(df)
    names = [name] * len(df)
    pics = [pic] * len(df)
    descs = [desc] * len(df)
    pdf_filenames = [pdf_filename] * len(df)

    labelDF = pd.DataFrame({'file':files, 'name':names, 'pic':pics, 'desc':descs, 'pdf_filename':pdf_filenames})
    labelDF = pd.concat([labelDF, df], axis=1)

    return labelDF

# %% Scrape the individual product pages
# Drop any duplicates to avoid unnecessary site access
produrls = list(dict.fromkeys(produrls))

# Scrape the product pages and store the soup as txt

minTime = 4 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

directory = r'txts/'

finished = []

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        finished.append(file)

files = []
urls = []
problems = []

path = directory #Folder the txt files should go to 
os.chdir(path)

produrls2 = produrls[1:3]

for row in produrls:
    try:
        name = str(row.split('/')[-2] + '.txt')
#         print(name)
        if name in finished:
#            print(name, 'is already downloaded.')
            files.append(name)
            urls.append(row)
            continue
        soup = pagescrape(row)
        with open(name, 'w', encoding='utf-8') as f_out:
            f_out.write(soup.prettify())
        files.append(name)
        urls.append(row)
        print(name, 'downloaded')
    except:
        print('problem with:',name,row)
        problems.append(row)

os.chdir(originalpath)

# %% Parse the soup and create overall info DF
# Dictionaries to associate urls and filenames for later
urls2files = dict(zip(urls, files)) 
files2urls = dict((v,k) for k,v in urls2files.items())

# Get a list of the text files you're going to work with
txtFiles = []

directory = r'txts/'

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        txtFiles.append(file)

# Get the information from the extracted text files
info = pd.DataFrame()
goodfiles = []
errorfiles = []

for file in txtFiles:
    try:
        soup = BeautifulSoup(open(r'txts/' + file).read(), features="lxml")
        infodict = pageinfo(soup, file)
        info = info.append(infodict, ignore_index=True)
        goodfiles.append(file)
    except:
        errorfiles.append(file)

# Try alternate labeller
errorinfo = pd.DataFrame()
txtFiles = errorfiles
goodfiles = []
errorfiles = []

for file in txtFiles:
    try:
        soup = BeautifulSoup(open(r'txts/' + file).read(), features="lxml")
        infodict = pageinfo2(soup, file)
        errorinfo = errorinfo.append(infodict, ignore_index=True)
        goodfiles.append(file)
    except:
        errorfiles.append(file)

# Put it together and clean it up
info = info.append(errorinfo, sort=False)
info = info.reset_index(drop=True)

cleanColumns = ['name', 'desc', 'ingredient', 'function', 'source']

for column in cleanColumns:
    info[column] = info[column].apply(cleanLine)
    
# %% Finalize info DataFrame
info['url'] = info['file']
info = info.replace({'url': files2urls})

f = open("method-info.pkl","wb")
pickle.dump(info,f)
f.close()

# %% Download pictures from site

minTime = 4 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

finished = []

directory = r'pics/'

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        finished.append(file)

pics = info['pic']
pics = list(dict.fromkeys(pics))

data = pics

path = directory #Folder the pictures should go to 
os.chdir(path)

for row in data:
    try:
        name = row.split('/')[-1]
        if name in finished:
            print(name, 'is already downloaded.')
            continue      
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

# %% Create a list of URLs without PDFs that will need to be printed
pdfDict = pd.Series(info.pdf_filename.values,index=info.url).to_dict()

noPdf = []

for url, pdf in pdfDict.items():
    if pdf == 'none':
        noPdf.append(url)

f = open("method-noPdfs.pkl","wb")
pickle.dump(noPdf,f)
f.close()

## %% Script Allison used to print URLs to PDFs
#"""
#Created on Thu Feb 20 13:23:22 2020
#
#@author: ALarger
#"""
#
#import time, os, random, pickle, pdfkit
#
#
#path_wkhtmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#options = { 'quiet': '', 'encoding': "UTF-8",'disable-javascript': None}
#
#path = r'L:\Lab\HEM\ALarger\Method pages' #Folder doc is in
#os.chdir(path)   
#minTime = 5 #minimum wait time in between clicks
#maxTime = 10 #maximum wait time in between clicks
#
#pages = pickle.load(open( "MethodPDFsPrintyThingie.pkl","rb" ) )
#    
#for p in pages:
#    try:
#        name = p.split('/')[-2]+'.pdf'
#        pdfkit.from_url(p,name,options=options, configuration=config)
#        time.sleep(random.randint(minTime,maxTime))
#    except: 
#        print(p)
