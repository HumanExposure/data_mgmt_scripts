# -*- coding: utf-8 -*-
"""
Created on Wed May  1 13:24:32 2019

@author: ALarger

Inventory of Effective Food Contact Substance (FCS) Notifications
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://www.accessdata.fda.gov/scripts/fdcc/index.cfm?set=FCN&sort=FCN_No&order=ASC&showAll=true&type=basic&search='
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
casN = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    cas = ''
    T = tr_elements[j]
    if len(T) != 4: break
    if T[1].text_content().lower().strip() == 'food contact substance' or clean(T[1].text_content()) == '': continue
    chemName.append(clean(T[1].text_content()).strip()) #Get first column
    name = chemName[-1].split(' ')
    for n in name:
        n=n.split(')')[0].replace('No.','').strip(',').strip(';')
        if n.count('-') == 2 and any(c.isalpha() for c in n) == False and '(' not in n:
            cas = (cas + ', ' + n).lstrip(', ')
    casN.append(cas)
    
nIngredients = len(chemName)
prodID = [1372234]*nIngredients
templateName = ['Inventory of Effective Food Contact Substance (FCS) Notifications.html']*nIngredients
msdsDate = ['03/29/2019']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Inventory of Effective Food Contact Substance (FCS)\Food Contact Substance.csv',index=False, header=True)