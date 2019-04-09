# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:27:44 2019

@author: ALarger

Pesticides Sold in California years 1994-2010
Extract chemicals
"""

import camelot, os
import pandas as pd
from glob import glob

os.chdir(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Pesticides Sold in California')    
pdfs = glob("*.pdf")
prodID = []
templateName = []
msdsDate = []
recUse = []
catCode = []
descrip = []
code = []
sourceType = []
chemNames = []
casNs = []

k = 0
for file in pdfs:
    chemName = []
    casN = []
    lbs = []
    
    tables = (camelot.read_pdf(file,pages='all', flavor='stream'))
    i=0 
    for table in tables:
        df = tables[i].df
        if len(df.columns) < 3:
            print((k+1994),i,df)
            i+=1
            continue
        df = df.drop(df.index[0]) #Drop first 4 lines
        df = df.drop(df.index[0])
        df = df.drop(df.index[0])
        df = df.drop(df.index[0])
        chemName.extend(df.iloc[:,0])
        casN.extend(['']*len(df))
        lbs.extend(df.iloc[:,-1])
        i+=1
    
    j = len(chemName)
    while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
        j-=1
        if ',' in chemName[j] or '\n' in chemName[j]:
            chemName[j] = chemName[j].replace(',','_')
            chemName[j] = chemName[j].replace('\n',' ')
        chemName[j] = chemName[j].lower()
        chemName[j] = chemName[j].strip()
        if chemName[j] == '' or chemName[j] == 'active ingredients' or 'no. chemicals:' in chemName[j]:
            del chemName[j]
            del casN[j]
            del lbs[j]
            continue
        if lbs[j] == '':
            print(k+1994, chemName[j], lbs[j])
            chemName[j-1] = chemName[j-1] + ' ' + chemName[j]
            del chemName[j]
            del casN[j]
            del lbs[j]
            continue
            
    year = k + 1994
    nIngredients = len(chemName)
    prodID.extend([file.strip('.pdf').strip('document_')]*nIngredients)
    templateName.extend(['Cal_CDPR_PestSales_'+str(year)+'.pdf']*nIngredients)
    msdsDate.extend([year]*nIngredients)
    recUse.extend(['']*nIngredients)
    catCode.extend(['']*nIngredients)
    descrip.extend(['']*nIngredients)
    code.extend(['']*nIngredients)
    sourceType.extend(['ACToR Assays and Lists']*nIngredients)
    chemNames.extend(chemName)
    casNs.extend(casN)
    k+=1
    print(k/len(pdfs)*100, '%')
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casNs, 'raw_chem_name':chemNames, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r"L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Pesticides Sold in California\Pesticides Sold in California.csv",index=False, header=True, date_format=None)