# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 08:35:50 2019

@author: ALarger

FDA CDER New Molecular Entity Calendar Year Approvals
2008-2011
"""

import camelot, os
import pandas as pd
from glob import glob

os.chdir(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\CDER New Molecular Entity Drug Approvals')    
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
    year = k + 2008
    chemName = []
    casN = []
    tables = (camelot.read_pdf(file,pages='all', flavor='lattice'))
    i=0 
    for table in tables:
        df = tables[i].df
        if df.iloc[0,0] == '' or 'application' in df.iloc[0,0].lower():
            df = df.drop(df.index[0]) #Drop first 4 lines
        if 'BLA' in df.iloc[0,0]:
            break
        if year == 2008: chemName.extend(df.iloc[:,3])
        else: chemName.extend(df.iloc[:,2])
        casN.extend(['']*len(df))
        i+=1
    
    j = len(chemName)
    while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
        j-=1
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace(';','_')
        chemName[j] = chemName[j].replace('\n',' ')
        chemName[j] = chemName[j].lower()
        chemName[j] = chemName[j].strip()
        chemName[j] = chemName[j].replace('  ',' ')

            
    if year == 2008: tname = 'CY08_NME_Approvals_Orphan_Update.pdf'
    elif year == 2009: tname = 'CY09 NME Approvals (with Orphans).pdf'
    elif year == 2010: tname = 'NME CY Approvals (12 31 2010).pdf'
    else: tname = 'CY11 NME Approvals (12.31.2011).pdf'
    nIngredients = len(chemName)
    prodID.extend([file.strip('.pdf').strip('document_')]*nIngredients)
    templateName.extend([tname]*nIngredients)
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
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\CDER New Molecular Entity Drug Approvals\CDER NME Approvals.csv',index=False, header=True, date_format=None)