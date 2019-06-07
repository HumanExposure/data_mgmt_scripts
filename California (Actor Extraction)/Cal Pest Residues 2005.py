# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 12:51:21 2019

@author: ALarger

Cal Pesticide Residues 2005
"""

import camelot
import pandas as pd

chemName = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\document_1359553.pdf',pages='1165-1358', flavor='stream')) 

for table in tables: 
    df = table.df
    for index, row in df.iterrows(): #Get first item in each row with a letter in it
        for i in row:
            if any(c.isalpha() for c in i) == True:
                chemName.append(i)
                break

m = len(chemName) 
while m > 0: #Go backwards through chemical name list so that the indexing does not get messed up when one is deleted
    m-=1
    chemName[m] = chemName[m].strip()
    if any(c.isalpha() for c in chemName[m].split(' ')[0]) == False:
        chemName[m] = ' '.join(chemName[m].split(' ')[1:])
    if chemName[m] == '' or chemName[m] == 'NO RESIDUE FOUND' or chemName[m] == 'CHEMNAME' or chemName[m] == 'SCHLOR':
        del chemName[m]
    
nIngredients = len(chemName)
msdsDate = ['2005']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
prodID = [1359553]*nIngredients
templateName = ['Cal_Pesticide_Residues_2005_orig.pdf']*nIngredients
    
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\California\Cal Pesticide Residues\Cal Pest Residues 2005.csv',index=False, header=True)
