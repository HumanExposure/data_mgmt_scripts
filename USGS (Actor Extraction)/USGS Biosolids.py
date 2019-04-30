# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 12:46:13 2019

@author: ALarger

The 25 Chemicals Found in All Nine of the Biosolids Studied
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://toxics.usgs.gov/highlights/compounds_biosolids_study.html'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 3: break
    if clean(T[0].text_content()) == 'Chemical Measured' or clean(T[0].text_content()) == '': continue
    chemName.append(clean(T[0].text_content()).strip()) #Get first column
    
nIngredients = len(chemName)
prodID = [1371471]*nIngredients
templateName = ['Biosolids Chemicals.pdf']*nIngredients
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USGS\The 25 Chemicals Found in All Nine of the Biosolids Studied\USGS Biosolids.csv',index=False, header=True)