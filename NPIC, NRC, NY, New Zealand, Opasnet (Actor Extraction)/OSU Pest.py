# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 17:24:46 2019

@author: ALarger

OSU Extension Pesticide Properties Database
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'http://npic.orst.edu/ingred/ppdmove.htm'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 5: break
    if clean(T[0].text_content()) == 'Common Name' or clean(T[0].text_content()) == '': continue
    chemName.append(clean(T[0].text_content())) #Get first column
    chemName[-1] = chemName[-1].strip()
    
nIngredients = len(chemName)
prodID = [1646367]*nIngredients
templateName = ['NPIC.pdf']*nIngredients
msdsDate = ['7/24/94']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 
component = ['']*nIngredients
chemDetected = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType, 'component':component, 'chem_detected_flag':chemDetected})
df.to_csv(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/OSU pest new\OSU Pest.csv',index=False, header=True)
