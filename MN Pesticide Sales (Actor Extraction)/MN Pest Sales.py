# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:30:41 2019

@author: ALarger

Minnesota Department of Agriculture-Pesticide Sales Database Search
"""

import lxml.html as lh
import pandas as pd

with open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\MN Pesticide Sales\Pesticide Sales Database Search - Results.html') as url:
    page = url.read()
    doc = lh.fromstring(page)
    tr_elements = doc.xpath('//tr')
chemName = []
prodID = []
templateName = []

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 3:
        break
    if 'CHEMICAL' in T[1].text_content() or 'TOTAL FOR YEAR' in T[1].text_content(): continue 
    chemName.append(T[1].text_content().lower())
    chemName[-1] = chemName[-1].replace('\n','')
    prodID.append(float(T[0].text_content()) + 1370253)
    templateName.append('MN Pest Sales ' + T[0].text_content().replace('\n','') + '.pdf')

nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\MN Pesticide Sales\MN Pest Sales.csv',index=False, header=True)