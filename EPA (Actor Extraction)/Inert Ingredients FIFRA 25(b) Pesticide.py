# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 09:59:29 2019

@author: ALarger

Inert Ingredients Eligible for FIFRA 25(b) Pesticide Products 
Food-Use and Non-Food Use
"""

import camelot, string
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
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Inert Ingredients Eligible for FIFRA 25(b) Pesticide Products\Inert Ingredients FIFRA 25(b) Pesticide Food-Use.pdf',pages='all', flavor='stream'))
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    if i < 3:
        chemName.extend(df.iloc[:,1])
        casN.extend(df.iloc[:,0])
        prodID.extend(['1372123']*len(df))
        templateName.extend(['Inert Ingredients FIFRA 25(b) Pesticide Food-Use.pdf']*len(df))
        msdsDate.extend(['April 10, 2008']*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    else:
        chemName.extend(df.iloc[:,1])
        casN.extend(df.iloc[:,0])
        prodID.extend(['1372124']*len(df))
        templateName.extend(['Inert Ingredients FIFRA 25(b) Pesticide Non-Food Use.pdf']*len(df))
        msdsDate.extend(['April 10, 2008']*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    i+=1

j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace(',','_')
    chemName[j] = chemName[j].replace(';','_')
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].strip()
    chemName[j] = clean(chemName[j])
    if chemName[j] == '' or casN[j] == '' or 'Chemical' in chemName[j] or 'pesticide' in chemName[j]:
        print(chemName[j],casN[j])
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
        continue
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Inert Ingredients Eligible for FIFRA 25(b) Pesticide Products\Inert Ingredients FIFRA.csv',index=False, header=True, date_format=None)