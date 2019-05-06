# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:11:42 2019

@author: ALarger

Pesticide Residue Monitoring 2007 Report
"""

import requests
import lxml.html as lh
import pandas as pd

url = 'https://wayback.archive-it.org/7993/20170723033521/https://www.fda.gov/Food/FoodborneIllnessContaminants/Pesticides/ucm169577.htm'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
chemName = []
prodID = []
templateName = []
inTable5 = False
inTable6 = False
inTable7 = False

for j in range (1, len(tr_elements)):
    T = tr_elements[j]        
    if len(T) == 5 and inTable5 == False: 
        inTable5 = True
        continue
    if inTable5 == True:
        if T[0].text_content().strip() == 'Pesticide2':
            inTable5 = False
            inTable6 = True
            continue
        if T[0].text_content().strip() == 'all others4': continue
        chemName.append(T[0].text_content().strip().rstrip('3').rstrip('4'))
        prodID.append(1372236)
        templateName.append('Pesticide Residue Monitoring 2007 Report Table 5.html')
    if inTable6 == True:
        if T[0].text_content().strip() == 'Pesticide2':
            inTable6 = False
            inTable7 = True
            continue
        chemName.append(T[0].text_content().strip().rstrip('3').rstrip('4').rstrip('5'))
        prodID.append(1372237)
        templateName.append('Pesticide Residue Monitoring 2007 Report Table 6.html')
    if inTable7 == True:
        if len(T) != 4:
            inTable7 = False
            continue
        chemName.append(T[0].text_content().strip().rstrip('3').rstrip('4'))
        prodID.append(1372238)
        templateName.append('Pesticide Residue Monitoring 2007 Report Table 7.html')
        
ul_elements = doc.xpath('//ul')
for j in range (1, len(ul_elements)):
    li = ul_elements[j]
    if len(li) > 100:
        for l in li:
            chemName.append(l.text_content().rstrip('+').rstrip('*').strip())
            prodID.append(1372235)
            templateName.append('Pesticide Residue Monitoring 2007 Report Table 3.html')
    
nIngredients = len(chemName)
msdsDate = ['06/05/2017']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Pesticide Residue Monitoring 2007 Report\Pesticide Residue Monitoring 2007 Report.csv',index=False, header=True)