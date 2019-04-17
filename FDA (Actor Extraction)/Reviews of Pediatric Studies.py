# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:06:42 2019

@author: ALarger

Reviews of Pediatric Studies Conducted under BPCA and PREA from 2012 – present
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://www.fda.gov/Drugs/DevelopmentApprovalProcess/DevelopmentResources/ucm316937.htm'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 6: break
    chemName.append(clean(T[0].text_content())) #Get first column
    chemName[-1] = chemName[-1].replace(',','_').replace(';','_').replace('NEW','').strip()
    
nIngredients = len(chemName)
prodID = [1370069]*nIngredients
templateName = ['Pediatric Rev.pdf']*nIngredients
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Reviews of Pediatric Studies\Reviews of Pediatric Studies.csv',index=False, header=True, date_format=None)