# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:06:17 2019

@author: ALarger

Cal Pesticide Residues 2006
"""

import camelot
import pandas as pd

chemName = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\document_1359554.pdf',pages='1291-1505', flavor='stream')) 

for table in tables: 
    df = table.df
    i=0
    while i < df.shape[1]:
        if 'NO RESIDUE FOUND' in list(df.iloc[:,i]):
            chemName.extend(df.iloc[:,i])
        i+=1

m = len(chemName) 
while m > 0: #Go backwards through chemical name list so that the indexing does not get messed up when one is deleted
    m-=1
    chemName[m] = chemName[m].strip()
    if any(c.isalpha() for c in chemName[m].split(' ')[0]) == False:
        chemName[m] = ' '.join(chemName[m].split(' ')[1:])
    if chemName[m] == '' or chemName[m] == 'NO RESIDUE FOUND' or chemName[m] == 'CHEMNAME':
        del chemName[m]
    
nIngredients = len(chemName)
msdsDate = ['2006']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
prodID = [1359554]*nIngredients
templateName = ['Cal_Pesticide_Residues_2006_orig.pdf']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\Cal Pest Residues 2006.csv',index=False, header=True)