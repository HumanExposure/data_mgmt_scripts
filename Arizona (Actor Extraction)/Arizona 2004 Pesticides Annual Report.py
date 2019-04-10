# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 08:36:41 2019

@author: ALarger

Pesticides Annual Report 2004 (A.R.S 49-303.C)
Extract chemicals and CAS from tables 2,4,5
"""

import camelot
import pandas as pd

chemName = []
casN = []
prodID = []
templateName = []
msdsDate = []
recUse = []
catCode = []
descrip = []
code = []
sourceType = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticides Annual Report 2004 (A.R.S 49-303.C)\document_320433.pdf',pages='4-15', flavor='lattice'))
i=0 
for table in tables:
    df = tables[i].df
    if i == 0: 
        df = df.drop(df.index[0])
        df = df.drop(df.index[0])
    if i <= 4: #Table 2
        chemName.extend(df.loc[:,1])
        casN.extend(df.loc[:,0])
        prodID.extend(['1372083']*len(df))
        templateName.extend(['Arizona 2004 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2004]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 6: #Table 4
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,4])
        casN.extend(['']*len(df))
        prodID.extend(['1372084']*len(df))
        templateName.extend(['Arizona 2004 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2004]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    else: #Table 5
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,4])
        casN.extend(['']*len(df))
        prodID.extend(['1372085']*len(df))
        templateName.extend(['Arizona 2004 Pesticide Report Table 5.pdf']*len(df))
        msdsDate.extend([2004]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    i+=1

j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n','')
    if '\n' in casN[j]:
        casN[j]=casN[j].replace('\n','')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    j-=1
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticides Annual Report 2004 (A.R.S 49-303.C)\Arizona 2004 Pesticides Annual Report.csv',index=False, header=True, date_format=None)
