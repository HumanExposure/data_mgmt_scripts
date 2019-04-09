# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:27:46 2019

@author: ALarger

Pesticides Annual Report 2005 (A.R.S 49-303.B)
Extract chemicals and CAS from tables 2-5
"""

import camelot
import pandas as pd

chemName = []
casN = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticides Annual Report 2005 (A.R.S 49-303.B)\document_320434.pdf',pages='5-54', flavor='lattice'))
i=0 
for table in tables:
    df = tables[i].df
    if i <= 41:
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,4])
    elif i <= 43:
        chemName.extend(df.loc[:,7])
        casN.extend(df.loc[:,8])
    elif i <= 47:
        chemName.extend(df.loc[:,8])
        casN.extend(df.loc[:,9])
    i+=1

chemList = [] #list of chem names with cas numbers (so duplicates without cas can be deleted)
j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if chemName[j] == '' or 'active ingredient' in chemName[j]:
        del chemName[j]
        del casN[j]
    if 'CAS' in casN[j]:
        del chemName[j]
        del casN[j]
    if chemName[j] not in chemList and casN[j] != '':
        chemList.append(chemName[j])
    j-=1
        
k = len(chemName) - 1
while k >= 0:
    if chemName[k] in chemList and casN[k] == '':
        del chemName[k]
        del casN[k]
    k-=1
    
nIngredients = len(chemName)
prodID = [320434]*nIngredients
templateName = ['Arizona_PestUse_2004.pdf']*nIngredients
msdsDate = [2005]*nIngredients
recUse = ['Pesticides: Active Ingredients']*nIngredients
catCode = ['ACToR_Assays_***']*nIngredients
descrip = ['pesticide active_ingredient']*nIngredients
code = ['Arizona_PestUse_2004_AID_1']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticides Annual Report 2005 (A.R.S 49-303.B)\Arizona 2005 Pesticides Annual Report.csv',index=False, header=True, date_format=None)