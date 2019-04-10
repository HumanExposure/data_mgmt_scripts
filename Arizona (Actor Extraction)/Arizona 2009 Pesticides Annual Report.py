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
prodID = []
templateName = []
msdsDate = []
recUse = []
catCode = []
descrip = []
code = []
sourceType = []

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2009 Pesticides Annual Report (A.R.S 49-303.C)\document_320438.pdf',pages='6-39', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    df=df.drop(df.index[0])
    if i <= 1: #Table 2
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,1])
        casN.extend(['']*len(df))
        prodID.extend(['1372090']*len(df))
        templateName.extend(['Arizona 2009 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 5: #Table 3
        chemName.extend(df.loc[:,2])
        casN.extend(df.loc[:,1])
        prodID.extend(['1372091']*len(df))
        templateName.extend(['Arizona 2009 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 18: #Table 4
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,4])
        prodID.extend(['1372092']*len(df))
        templateName.extend(['Arizona 2009 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 19: #Table 5
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,0])
        casN.extend(['']*len(df))
        prodID.extend(['1372093']*len(df))
        templateName.extend(['Arizona 2009 Pesticide Report Table 5.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 23: #Table 6
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,6])
        prodID.extend(['1372094']*len(df))
        templateName.extend(['Arizona 2009 Pesticide Report Table 6.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    else: #Table 7
        df=df.drop(df.index[0])
        chemName.extend(df.loc[:,6])
        casN.extend(df.loc[:,7])
        prodID.extend(['1372095']*len(df))
        templateName.extend(['Arizona 2009 Pesticide Report Table 7.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
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
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if '\n' in casN[j]:
        casN[j]=casN[j].replace('\n','')
    if chemName[j] == '':
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
    j-=1
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2009 Pesticides Annual Report (A.R.S 49-303.C)\Arizona 2009 Pesticides Annual Report.csv',index=False, header=True, date_format=None)
