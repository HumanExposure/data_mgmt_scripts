# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 16:06:41 2019

@author: ALarger

Substances in cosmetics and personal care products regulated under the Food and Drugs Act (F&DA) 
that were in commerce between January 1, 1987 and September 13, 2001: CAS Registry Number Known
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://www.canada.ca/en/health-canada/services/environmental-workplace-health/environmental-contaminants/drugs-personal-care-products/environmental-impact-initiative/commerce-list-food-drugs-act-substances/substances-cosmetics-personal-care-products-regulated-under-food-drugs-act-that-were-commerce-between-january-1-1987-september-13-2001-cas-registry.html'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
casN = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if len(T) != 2:
        break
    chemName.append(clean(T[0].text_content()))
    casN.append(clean(T[1].text_content()))
    chemName[-1] = chemName[-1].replace(',','_').replace(';','_')
    casN[-1] = casN[-1].replace(',','_').replace(';','_')
    
nIngredients = len(chemName)
prodID = [1362866]*nIngredients
templateName = ['personal care products 1987-2001_a.pdf']*nIngredients
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Health Canada\Cosmetics and Personal Care Products\Health Canada Cosmetics and Personal Care Products.csv',index=False, header=True, date_format=None)
