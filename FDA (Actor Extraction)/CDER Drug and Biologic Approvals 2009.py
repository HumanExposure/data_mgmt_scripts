# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:12:44 2019

@author: ALarger

FDA CDER Drug and Biologic Approvals 2009
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
propName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\CDER Drug and Biologic Approvals 2009\CDER New Drug Approvals 2009.pdf',pages='all', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    if i == (len(tables)-1):
        chemName.extend(df.iloc[:,2])
        casN.extend(['']*len(df))
        propName.extend(df.iloc[:,1])
        prodID.extend(['1372140']*len(df))
        templateName.extend(['CDER Biologic License Approvals 2009.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    else: 
        chemName.extend(df.iloc[:,2])
        casN.extend(['']*len(df))
        propName.extend(df.iloc[:,1])
        prodID.extend(['1372139']*len(df))
        templateName.extend(['CDER New Drug Approvals 2009.pdf']*len(df))
        msdsDate.extend([2009]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    if chemName[j] == '':
        chemName[j] = propName[j]
    chemName[j] = chemName[j].replace(',','_')
    chemName[j] = chemName[j].replace(';','_')
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].strip()
    chemName[j] = chemName[j].lower()
    chemName[j] = clean(chemName[j])
    if 'name' in chemName[j]:
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
        del propName[j]
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\CDER Drug and Biologic Approvals 2009\CDER Drug and Biologic Approvals 2009.csv',index=False, header=True, date_format=None)