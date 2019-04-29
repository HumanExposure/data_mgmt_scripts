# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 16:09:28 2019

@author: ALarger

List of 78 Chemicals Used in Hydraulic Fracturing Fluid in Pennsylvania
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://marcellusdrilling.com/2010/06/list-of-78-chemicals-used-in-hydraulic-fracturing-fluid-in-pennsylvania/'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 2: break
    if clean(T[0].text_content()) == 'Chemical' or clean(T[0].text_content()) == '': continue
    chemName.append(clean(T[0].text_content())) #Get first column
    chemName[-1] = chemName[-1].replace(',','_').replace(';','_').strip()
    
nIngredients = len(chemName)
prodID = [1371496]*nIngredients
templateName = ['PA_Fracking.pdf']*nIngredients
msdsDate = ['June 30, 2010']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\PA, USITC, WADA, WA, WHO\List of 78 Chemicals Used in Hydraulic Fracturing Fluid in Pennsylvania\PA Fracking Fluid.csv',index=False, header=True)