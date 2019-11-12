# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 15:21:20 2019

@author: ALarger

Extracts the detected chemicals from table 3 of MPCA 2013 Pharms and EACs in Lakes
Does not extract non-detects
Written in python 3.6
"""

import camelot, os
import pandas as pd

path = r'L:\Lab\HEM\Minnesota\MPCA 2013 Pharms and EACs in Lakes'
os.chdir(path)

chemName = []

tables = camelot.read_pdf('MPCA 2013 Pharms and EACs in Lakes.pdf',pages='12-15', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    for index, row in df.iterrows():
        if row[0] == 'Chemical' or row[1] == 'ND' or row[1] == '0' or row[1] == '':
            pass
        else: 
            chemName.append(row[0].replace('\n',' ').replace('  ',' ').strip())
    i+=1
        
n = len(chemName)
msdsDate = ['May 2013']*n
recUse = ['']*n
catCode = ['']*n
descrip = ['']*n
code = ['']*n
sourceType = ['']*n
casN = ['']*n
prodID = [1496306]*n
templateName = ['MPCA 2013 Pharms and EACs in Lakes.pdf']*n
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv('MPCA 2013 Pharms and EACs in Lakes.csv',index=False, header=True)