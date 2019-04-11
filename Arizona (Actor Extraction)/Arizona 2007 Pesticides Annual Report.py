# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 09:33:01 2019

@author: ALarger

Actor Arizona 2007 Pesticides Annual Report Chemical Extraction
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

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2007 Pesticides Annual Report (A.R.S 49-303.B)\document_320436.pdf',pages='5-29', flavor='stream')
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    if i <= 1: #Table 2
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,1])
        casN.extend(df.loc[:,0])
        prodID.extend(['1372112']*len(df))
        templateName.extend(['Arizona 2007 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2007]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i >= 21:  #Table 5
        chemName.extend(df.loc[:,7])
        casN.extend(df.loc[:,6])
        prodID.extend(['1372115']*len(df))
        templateName.extend(['Arizona 2007 Pesticide Report Table 5.pdf']*len(df))
        msdsDate.extend([2007]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i >= 18: #Table 4
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,6])
        casN.extend(df.loc[:,5])
        prodID.extend(['1372114']*len(df))
        templateName.extend(['Arizona 2007 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2007]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i >= 5: #Table 3
        df = df.drop(df.index[0])
        chemName.extend(df.loc[:,5])
        casN.extend(df.loc[:,4])
        prodID.extend(['1372113']*len(df))
        templateName.extend(['Arizona 2007 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2007]*len(df))
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
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\2007 Pesticides Annual Report (A.R.S 49-303.B)\Arizona 2007 Pesticides Annual Report.csv',index=False, header=True, date_format=None)
