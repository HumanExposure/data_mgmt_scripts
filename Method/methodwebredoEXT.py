# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 2022

@author: MHORTON
"""

#Import packages

import string, re
import pdfkit
config = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
import pathlib
root = pathlib.PurePath(__file__).parent
import pandas as pd

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

# %% Retrieve reference lists from download
import pickle

htmls = pickle.load(open( "htmls.pkl","rb" ) )
names = pickle.load(open( "names.pkl","rb" ) )

# %% scraping the HTML files

dir = pathlib.Path.cwd() / '/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Method Web 2/htmls'
htmls = dir.glob('*.html')
files = []

for html in htmls:
    files.append(str(html))    

names = []
urls = []
pdfs = []
dates = []
images = []
ingredients = []
functions = []
shortdescs = []
longdescs = []
ranks = []

for file in files:
    with open(file, encoding = 'utf8') as f:
        rank = 1
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            # get date of last modification of document
            if 'dateModified' in line:
                date = line.split('"dateModified":')[1].split(',')[0].split('T')[0].replace('"', '')
            # get the product descriptions
            if '<div class="product_description">' in line:
                if '<strong>' not in lines[i+2]:
                    shortdesc = ''
                    longdesc = cleanLine(lines[i+2])
                else:
                    shortdesc = cleanLine(lines[i+3])
                    longdesc = cleanLine(lines[i+7])
            # get the ingredients and functional uses
            if 'column-1' in line:
                if "dated on" in lines[i+1] or "ingredient" in lines[i+1] or "contains fragrance" in lines[i+1]:
                    continue
                names.append(file.split('\\')[-1].rsplit('.html')[0])
                pdfs.append(file.split('\\')[-1].rsplit('.html')[0] + '.pdf')
                dates.append(date)
                images.append(file.split('\\')[-1].rsplit('.html')[0] + '.jpg')
                urls.append(('https://methodhome.com/products/' + file.split('\\')[-1].rsplit('.html')[0]) + '/')
                ingredients.append(cleanLine(lines[i+1]))
                functions.append(cleanLine(lines[i+4]))
                shortdescs.append(shortdesc)
                longdescs.append(longdesc)
                ranks.append(rank)
                rank += 1

# %% Getting product counts

counts = []

for name in names:
    if 'count' in name:
        counts.append(re.sub('\D', '', name) + ' count')
    elif 'wipes' in name:
        counts.append(re.sub('\D', '', name.split('wipes')[-2]) + ' wipes')
    elif 'laundry-detergent' in name:
        if 'packs' in name:
            counts.append(re.sub('\D', '', name) + ' packs')
        else:
            counts.append(re.sub('\D', '', name) + ' loads')
    elif 'fabric' in name:
        counts.append(re.sub('\D', '', name) + ' loads')
    else:
        counts.append('')


# %% Registered Record CSV

titles = []

for name in names:
    title = name.replace('-', ' ')
    titles.append(title)

org = ['method products, pbc.'] * len(titles)

doctype = ['ID'] * len(titles)

rrDF = pd.DataFrame({'filename':pdfs, 'title':titles, 'document_type':doctype, 'url':urls, 'organization':org})

rrDF = rrDF.drop_duplicates().reset_index(drop=True)

rrDF.to_csv(root / 'method-web-registered-records.csv', index=False, header=True)

# %% Product Data CSV

blanks = [''] * len(titles)
brand_names = ['method'] * len(titles)

productsDF = pd.DataFrame({'title':titles, 'upc':blanks, 'url':urls, 'brand_name':brand_names, 'size':counts, 
                         'color':blanks, 'item_id':blanks, 'parent_item_id':blanks, 'short_description':shortdescs, 
                         'long_description':longdescs, 'epa_reg_number':blanks, 'thumb_image':blanks, 'medium_image':blanks, 
                         'large_image':blanks, 'model_number':blanks, 'manufacturer':org, 'image_name':images})

productsDF.to_csv(root / 'method-web_products.csv',index=False, header=True)


# %% Extracted Text CSV

rridDF = pd.read_csv('method_web_registered_documents.csv')

file2id = dict(zip(rridDF['filename'], rridDF['DataDocument_id']))

extDF = pd.DataFrame({'data_document_id':pdfs, 'data_document_filename':pdfs, 'prod_name':titles,
                   'doc_date':dates, 'rev_num':'', 'raw_category':'', 'raw_cas':'',
                   'raw_chem_name':ingredients, 'report_funcuse':functions, 'raw_min_comp':'', 'raw_max_comp':'',
                   'unit_type':'', 'ingredient_rank':ranks, 'raw_central_comp':'', 'component':''})
    
extDF['data_document_id'] = extDF.data_document_id.replace(file2id)

extDF.to_csv(root / 'method-web_extracted-text.csv',index=False, header=True)
