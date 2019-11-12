# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 11:54:15 2019

@author: ALarger

Extracts the detected chemicals from table 3 of MPCA 2017 Pharms and Chems of Concern in Rivers
Does not extract non-detects
Written in python 3.6
"""

import camelot, os
import pandas as pd

path = r'L:\Lab\HEM\Minnesota\MPCA 2017 Pharms and Chems of Concern in Rivers'
os.chdir(path)

chemName = []

tables = camelot.read_pdf('MPCA 2017 Pharms and Chems of Concern in Rivers.pdf',pages='12-13', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    for index, row in df.iterrows():
        if row[0] == '' or row[1] == '' or row[1] == 'ND':
            pass
        else: 
            chemName.append(row[0].replace('\n',' ').replace('  ',' ').strip())
    i+=1
        
n = len(chemName)
msdsDate = ['January 2017']*n
recUse = ['']*n
catCode = ['']*n
descrip = ['']*n
code = ['']*n
sourceType = ['']*n
casN = ['']*n
prodID = [1496302]*n
templateName = ['MPCA 2017 Pharms and Chems of Concern in Rivers.pdf']*n
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv('MPCA 2017 Pharms and Chems of Concern in Rivers Table 3.csv',index=False, header=True, date_format=None)