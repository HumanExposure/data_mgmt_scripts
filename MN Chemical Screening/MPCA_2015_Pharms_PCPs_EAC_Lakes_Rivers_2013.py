# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 13:24:47 2019

@author: ALarger
"""

import camelot, os
import pandas as pd

path = r'L:\Lab\HEM\Minnesota\MPCA 2015 Pharms PCPs and EAC Monitoring Lakes and Rivers 2013'
os.chdir(path)

chemName = []

tables = camelot.read_pdf('MPCA 2015 Pharms PCPs and EAC Monitoring Lakes and Rivers 2013.pdf',pages='13-15', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    for index, row in df.iterrows():
        if i==0 or i==4 or row[0] == 'Chemical':
            pass
        else: 
            chemName.append(row[0].replace('\n',' ').replace('  ',' ').strip())
    i+=1
        
n = len(chemName)
msdsDate = ['May 2015']*n
recUse = ['']*n
catCode = ['']*n
descrip = ['']*n
code = ['']*n
sourceType = ['']*n
casN = ['']*n
prodID = [1496305]*n
templateName = ['MPCA 2015 Pharms PCPs and EAC Monitoring Lakes and Rivers 2013.pdf']*n
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv('MPCA 2015 Pharms PCPs and EAC Monitoring Lakes and Rivers 2013.csv',index=False, header=True, date_format=None)