# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:28:47 2019

@author: ALarger

Air Water INC. Fine Chemicals List
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'http://www.awi.co.jp/english/business/chemical/technology/productlist/productlistunder.html#PlistT'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
casN = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 5: break
    if T[1].text_content() == 'Chemical name': continue
    chemName.append(clean(T[1].text_content().replace('α','alpha').replace('β','beta')))
    casN.append(clean(T[2].text_content()))
    chemName[-1] = chemName[-1].replace('\n','').strip().replace('  ',' ')
    
nIngredients = len(chemName)
prodID = [1373515]*nIngredients
templateName = ['Airwaterincfinechemicallist.pdf']*nIngredients
msdsDate = ['5/29/2019']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Air Water INC\Air Water INC Fine Chemicals List.csv',index=False, header=True)