# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:50:13 2019

@author: ALarger

Pesticide Contamination Prevention Program A.R.S. 49-1051.D
Extract chemicals and CAS from tables V.P1, V.5, V.7
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

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticide Contamination Prevention Program A.R.S. 49-1051.D\document_320429.pdf',pages='3-4', flavor='stream'))
i=0 
for table in tables: #Table V.P1
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    chemName.extend(df.loc[:,1])
    casN.extend(df.loc[:,0])
    chemName.extend(df.loc[:,3])
    casN.extend(df.loc[:,2])
    nIngredients = len(df)*2
    prodID.extend(['1372071']*nIngredients)
    templateName.extend(['Arizona 2000 Pesticide Report Table VP1.pdf']*nIngredients)
    msdsDate.extend([2000]*nIngredients)
    recUse.extend(['']*nIngredients)
    catCode.extend(['']*nIngredients)
    descrip.extend(['']*nIngredients)
    code.extend(['']*nIngredients)
    sourceType.extend(['ACToR Assays and Lists']*nIngredients)
    i+=1

m = len(chemName) - 1
while m >= 0:
    if casN[m] == '':
        chemName[m-1] = chemName[m-1] + ' ' + chemName[m]
        del chemName[m]
        del casN[m]
        del prodID[m]
        del templateName[m]
        del msdsDate[m]
        del recUse[m]
        del catCode[m]
        del descrip[m]
        del code[m]
        del sourceType[m]
    m-=1

i=0
tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticide Contamination Prevention Program A.R.S. 49-1051.D\document_320429.pdf',pages='6-20', flavor='lattice'))
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    chemName.extend(df.loc[:,4])
    casN.extend(['']*len(df))
    nIngredients = len(df)
    if i <= 8: #Table V.5
        prodID.extend(['1372072']*nIngredients)
        templateName.extend(['Arizona 2000 Pesticide Report Table V5.pdf']*nIngredients)
    else: #Table V.7
        prodID.extend(['1372073']*nIngredients)
        templateName.extend(['Arizona 2000 Pesticide Report Table V7.pdf']*nIngredients)
    msdsDate.extend([2000]*nIngredients)
    recUse.extend(['']*nIngredients)
    catCode.extend(['']*nIngredients)
    descrip.extend(['']*nIngredients)
    code.extend(['']*nIngredients)
    sourceType.extend(['ACToR Assays and Lists']*nIngredients)
    i+=1

j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    if chemName[j] == '' or 'appendix' in chemName[j] or chemName[j] == '*':
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
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona\Pesticide Contamination Prevention Program A.R.S. 49-1051.D\Pesticide Contamination Prevention Program A.R.S. 49-1051.D.csv',index=False, header=True, date_format=None)
