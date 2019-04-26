# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 17:44:30 2019

@author: ALarger

Quantities of Radioactive Materials Requiring Consideration of the Need for and Emergency Plan for Responding to a Release
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://www.nrc.gov/reading-rm/doc-collections/cfr/part030/part030-0072.html'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 3: break
    if clean(T[0].text_content()) == 'Radioactive material1' or clean(T[0].text_content()) == '': continue
    chemName.append(clean(T[0].text_content())) #Get first column
    chemName[-1] = chemName[-1].replace(',','_').replace(';','_').strip()
    
nIngredients = len(chemName)
prodID = [1371508]*nIngredients
templateName = ['NRC_Schedule_C.pdf']*nIngredients
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\NPIC, NRC, NY, New Zealand, Opasnet\Quantities of Radioactive Materials Requiring Consideration of the Need for and Emergency Plan for Responding to a Release\Quantities of Radioactive Materials.csv',index=False, header=True)