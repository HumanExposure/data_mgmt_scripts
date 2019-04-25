# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:43:53 2019

@author: ALarger

Summary of Color Additives for Use in the United States in Foods, Drugs, Cosmetics, and Medical Devices
"""

import requests, string
import lxml.html as lh
import pandas as pd

url = 'https://www.fda.gov/ForIndustry/ColorAdditives/ColorAdditiveInventories/ucm115641.htm#table1B'
page = requests.get(url)
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
nIngredients = []
prodID = []
templateName = []
msdsDate = []
recUse = []
catCode = []
descrip = []
code = []
sourceType = []
casN = []
chemName = []
tables = ['Color Additives Approved for Use in Human Food Exempt from Batch Certification.html','Color Additives Approved for Use in Human Food Subject to Batch Certification.html','Color Additives Approved for Use in Drugs Exempt from Batch Certification.html','Color Additives Approved for Use in Drugs Subject to Batch Certification.html','Color Additives Approved for Use in Cosmetics Exempt from Batch Certification.html','Color Additives Approved for Use in Cosmetics Subject to Batch Certification.html','Color Additives Approved for Use in Medical Devices Exempt from Batch Certification.html','Color Additives Approved for Use in Medical Devices Subject to Batch Certification.html']
lastLen = 0
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

i = -1
for j in range (1, len(tr_elements)):
    T = tr_elements[j]
    if T[0].text_content() == 'Part':
        break
    if T[0].text_content() == '21 CFR Section':
        i += 1
        continue
    try: chem = clean(T[1].text_content())
    except: pass
    if len(T) < lastLen and (i + 1372173) == prodID[-1]: #handle rows with fewer columns
        if T[0].text_content()[0] == '(':
            chem = chemName[-1].split(':')[0].strip() + ': ' + clean(T[0].text_content())
        elif T[0].text_content()[0:2] in ['19','20'] or 'Color Additives' in T[0].text_content():
            continue
        else:
            chem = clean(T[0].text_content())
    else:lastLen = len(T)
    chemName.append(chem) #Get second column
    chemName[-1] = chemName[-1].replace(',','_').replace(';',':').replace('NEW','').replace('one or more of','').replace(': :',':').replace('(1)','').replace('(2)','').replace('(3)','').replace('(4)','').replace('(5)','').replace('(6)','').replace('(7)','').replace('(8)','').replace('(9)','').replace('(10)','').strip().replace('  ',' ')
    if chemName[-1][0] == '-': 
        chemName[-1] = 'Beta' + chemName[-1] 
    
    prodID.append(i + 1372173)
    templateName.append(tables[i])
    msdsDate.append('')
    recUse.append('')
    catCode.append('')
    descrip.append('')
    code.append('')
    sourceType.append('ACToR Assays and Lists')
    casN.append('') 

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Summary of Color Additives\Summary of Color Additives.csv',index=False, header=True, date_format=None)