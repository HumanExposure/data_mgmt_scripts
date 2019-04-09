# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 12:54:53 2019

@author: ALarger

Actively Registered AI's
"""

import camelot
import pandas as pd

chemName = []
casN = []

tables = (camelot.read_pdf(r"L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Actively Registered AI's by Common Name/document_1359540.pdf",pages='1-13', flavor='stream'))
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    chemName.extend(df.loc[:,2])
    casN.extend(['']*len(df))
    i+=1

j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if chemName[j] == '' or chemName[j] == 'common' or chemName[j] == 'name' or '/13' in chemName[j]:
        del chemName[j]
        del casN[j]
        continue
    
nIngredients = len(chemName)
prodID = [1359540]*nIngredients
templateName = ['Cal_Pest_Registered_2011.pdf']*nIngredients
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r"L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Actively Registered AI's by Common Name\Actively Registered AIs.csv",index=False, header=True, date_format=None)