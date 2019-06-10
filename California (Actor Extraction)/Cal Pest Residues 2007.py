# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 14:34:50 2019

@author: ALarger

Cal Pesticide Residues 2007
"""

import camelot
import pandas as pd

chemName = []

#tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\document_1359555.pdf',pages='all', flavor='lattice')) 

i=0
for table in tables: 
    i+=1
    if (i+1) % 3 == 0:
        df = tables[i].df
        chemName.extend(df.iloc[:,0])

m = len(chemName) 
while m > 0: #Go backwards through chemical name list so that the indexing does not get messed up when one is deleted
    m-=1
    chemName[m] = chemName[m].strip()
    if chemName[m] == '' or chemName[m] == 'NO RESIDUE FOUND':
        del chemName[m]
    
nIngredients = len(chemName)
msdsDate = ['2007']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
prodID = [1359555]*nIngredients
templateName = ['Cal_Pesticide_Residues_2007_orig.pdf']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\Cal Pest Residues 2007.csv',index=False, header=True)