# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 09:33:59 2019

@author: ALarger

Cal Pesticide Residues 2009
"""

import camelot
import pandas as pd

chemName = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\document_1359557.pdf',pages='655-981', flavor='lattice')) 

for table in tables: 
    df = table.df
    chemName.extend(df.iloc[:,1])

m = len(chemName) 
while m > 0: #Go backwards through chemical name list so that the indexing does not get messed up when one is deleted
    m-=1
    chemName[m] = chemName[m].strip()
    if chemName[m] == '' or chemName[m] == 'no residue detected' or chemName[m] == 'CHEMICAL DETECTED':
        del chemName[m]
    
nIngredients = len(chemName)
msdsDate = ['2009']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
prodID = [1359557]*nIngredients
templateName = ['Cal_Pesticide_Residues_2009_orig.pdf']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\Cal Pest Residues 2009.csv',index=False, header=True)