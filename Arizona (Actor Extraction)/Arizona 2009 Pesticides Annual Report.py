# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 12:03:56 2019

@author: ALarger

2009 Pesticides Annual Report (A.R.S 49-303.C)
Extract chemicals and CAS from tables 2-7
"""

import camelot
import pandas as pd

chemName = []
casN = []

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2009 Pesticides Annual Report (A.R.S 49-303.C)\document_320438.pdf',pages='6-39', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    df=df.drop(df.index[0])
    if i <= 1:
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,1])
        casN.extend(['']*len(df))
    elif i <= 5:
        chemName.extend(df.loc[:,2])
        casN.extend(df.loc[:,1])
    elif i <= 18:
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,4])
    elif i <= 19:
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,0])
        casN.extend(['']*len(df))
    elif i <= 23:
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,6])
    else:
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,6])
        casN.extend(df.loc[:,7])
    i+=1

chemList = [] #list of chem names with cas numbers (so duplicates without cas can be deleted)
j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n','')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if '\n' in casN[j]:
        casN[j]=casN[j].replace('\n','')
    if chemName[j] == '':
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
prodID = [320438]*nIngredients
templateName = ['Arizona_PestUse_2008.pdf']*nIngredients
msdsDate = [2009]*nIngredients
recUse = ['Pesticides: Active Ingredients']*nIngredients
catCode = ['ACToR_Assays_***']*nIngredients
descrip = ['pesticide active_ingredient']*nIngredients
code = ['Arizona_PestUse_2008_AID_1']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2009 Pesticides Annual Report (A.R.S 49-303.C)\Arizona 2009 Pesticides Annual Report.csv',index=False, header=True, date_format=None)