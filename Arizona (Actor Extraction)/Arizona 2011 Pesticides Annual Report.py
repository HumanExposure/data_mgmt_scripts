# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:19:02 2019

@author: ALarger

2011 Pesticides Annual Report (A.R.S 49-303.C)
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

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2011 Pesticides Annual Report (A.R.S 49-303.C)\document_320440.pdf',pages='6-29', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    if i == 0: #Table 2
        chemName.extend(df.loc[:,1])
        casN.extend(['']*len(df))
        prodID.extend(['1372102']*len(df))
        templateName.extend(['Arizona 2011 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2011]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 4: #Table 3
        chemName.extend(df.loc[:,2])
        casN.extend(df.loc[:,1])
        prodID.extend(['1372103']*len(df))
        templateName.extend(['Arizona 2011 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2011]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 17: #Table 4
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,4])
        prodID.extend(['1372104']*len(df))
        templateName.extend(['Arizona 2011 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2011]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i <= 18: #Table 5
        chemName.extend(df.loc[:,0])
        casN.extend(['']*len(df))
        prodID.extend(['1372105']*len(df))
        templateName.extend(['Arizona 2011 Pesticide Report Table 5.pdf']*len(df))
        msdsDate.extend([2011]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    else: #Table 6
        chemName.extend(df.loc[:,5])
        casN.extend(['']*len(df))
        prodID.extend(['1372106']*len(df))
        templateName.extend(['Arizona 2011 Pesticide Report Table 6.pdf']*len(df))
        msdsDate.extend([2011]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    i+=1

tables2 = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2011 Pesticides Annual Report (A.R.S 49-303.C)\document_320440.pdf',pages='30-37', flavor='stream'))
k=0
for table in tables2: #Table 7
    df = tables2[k].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    chemName.extend(df.loc[:,6])
    casN.extend(['']*len(df))
    prodID.extend(['1372107']*len(df))
    templateName.extend(['Arizona 2011 Pesticide Report Table 7.pdf']*len(df))
    msdsDate.extend([2011]*len(df))
    recUse.extend(['']*len(df))
    catCode.extend(['']*len(df))
    descrip.extend(['']*len(df))
    code.extend(['']*len(df))
    sourceType.extend(['ACToR Assays and Lists']*len(df))
    k+=1

j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
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
    if '*' in chemName[j]:
        chemName[j] = chemName[j].split('*')[0]
    if chemName[j] == 'salt':
        chemName[j-1] = chemName[j-1] + ' salt'
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
    if chemName[j] == '1_2_3-':
        chemName[j+1] = '1_2_3-' + chemName[j+1] 
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
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    j-=1
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2011 Pesticides Annual Report (A.R.S 49-303.C)\Arizona 2011 Pesticides Annual Report.csv',index=False, header=True, date_format=None)
