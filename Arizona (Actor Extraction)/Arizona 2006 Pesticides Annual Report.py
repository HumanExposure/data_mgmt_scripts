# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:12:08 2019

@author: ALarger

Arizona 2006 Pesticides Annual Report
Extract chemicals and CAS from tables 2,3,4
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

tables = (camelot.read_pdf(r'L:/Lab/HEM/ALarger/Actor Automated Extraction/Arizona/2006 Pesticides Annual Report/document_320435.pdf',pages='6-23', flavor='stream'))
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    if i <= 12: #Table 2
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,4])
        prodID.extend(['1372109']*len(df))
        templateName.extend(['Arizona 2006 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2006]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i == 16:  #Table 3
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,7])
        casN.extend(df.loc[:,6])
        prodID.extend(['1372110']*len(df))
        templateName.extend(['Arizona 2006 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2006]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i == 17: #Table 4
        chemName.extend(df.loc[:,8])
        casN.extend(df.loc[:,7])
        prodID.extend(['1372111']*len(df))
        templateName.extend(['Arizona 2006 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2006]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i == 18: #Table 4 continued (index is off)
        chemName.extend(df.loc[:,9])
        casN.extend(df.loc[:,8])
        prodID.extend(['1372111']*len(df))
        templateName.extend(['Arizona 2006 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2006]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    i+=1

j = len(chemName) 
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if chemName[j] == '' or 'active ingredient' in chemName[j]:
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
    elif casN[j] == '':
        chemName[j+1] = chemName[j] + ' ' + chemName[j+1]
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2006 Pesticides Annual Report\2006 Arizona Pest.csv',index=False, header=True, date_format=None)
