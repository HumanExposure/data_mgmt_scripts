# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:24:04 2019

@author: ALarger

Postmarketing Drug Safety Evaluation Summaries Completed 
from September 2007 through December 2009
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://wayback.archive-it.org/7993/20170111133829/http://www.fda.gov/Drugs/GuidanceComplianceRegulatoryInformation/Surveillance/ucm231026.htm'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 4: break
    chemName.append(clean(T[0].xpath('p')[0].text_content())) #Get first paragraph in first column
    chemName[-1] = chemName[-1].replace(',','_').replace(';','_')
    if 'NDA' in chemName[-1]: chemName[-1] = chemName[-1].split('NDA')[0]
    
nIngredients = len(chemName)
prodID = [1370070]*nIngredients
templateName = ['Postmarket Eval 2007-2008.pdf']*nIngredients
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Postmarket Drug Safety Evaluation\Postmarket Drug Safety Eval.csv',index=False, header=True, date_format=None)