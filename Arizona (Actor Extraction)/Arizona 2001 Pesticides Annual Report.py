# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:02:59 2019

@author: ALarger

Pesticide Contamination Prevention Program Report A.R.S. 49-303.B (2001)
Extract chemicals and CAS from tables 2,4,5
"""

import camelot
import pandas as pd

chemName = []
casN = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\(2001) Pesticide Contamination Prevention Program Report A.R.S. 49-303.B/document_320430.pdf',pages='4-15', flavor='stream'))
i=0 
for table in tables:
    df = tables[i].df
    if i <= 4:
        chemName.extend(df.loc[:,1])
        casN.extend(df.loc[:,0])
    elif i >= 7:
        chemName.extend(df.loc[:,4])
        casN.extend(['']*len(df))
    i+=1

chemList = [] #list of chem names with cas numbers (so duplicates without cas can be deleted)
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if chemName[j] == '' or 'active ingredient' in chemName[j] or 'c_name' in chemName[j] or chemName[j] == '*':
        del chemName[j]
        del casN[j]
        continue
    elif chemName[j] == 'isopropanol' or chemName[j] == 'isopropylamine salt' or chemName[j] == 'salt' or chemName[j] == 'methanearsonate' or (chemName[j] == 'thidiazuron' and chemName[j-1] == 'diuron +') or chemName[j] == 'ammonium salt':
        chemName[j-1] = chemName[j-1] + ' ' + chemName[j]
        del chemName[j]
        del casN[j]
        continue
    if chemName[j] not in chemList and casN[j] != '':
        chemList.append(chemName[j])
        
k = len(chemName) - 1
while k >= 0:
    if chemName[k] in chemList and casN[k] == '':
        del chemName[k]
        del casN[k]
    k-=1
    
nIngredients = len(chemName)
prodID = [320430]*nIngredients
templateName = ['Arizona_***']*nIngredients
msdsDate = [2001]*nIngredients
recUse = ['***']*nIngredients
catCode = ['ACToR_Assays_***']*nIngredients
descrip = ['***']*nIngredients
code = ['Arizona_***']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\(2001) Pesticide Contamination Prevention Program Report A.R.S. 49-303.B\2001 Arizona Pest.csv',index=False, header=True, date_format=None)