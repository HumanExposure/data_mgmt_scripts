# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 13:27:11 2019

@author: ALarger
"""

import camelot
import pandas as pd

chemName = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USGS\Water-Quality Assessment of Eastern Iowa Basins Selected Pesticides and Pesticide Degradates in Streams, 1996-98\document_1371481.pdf',pages='51-67', flavor='stream')) 

for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if any(c.isalpha() for c in row[2]) == False and row[2] != '' and row[0] != '' and row[2] != '0.0':
            chemName.append(row[0].strip('*').replace("’","'"))

nIngredients = len(chemName)
msdsDate = ['2003']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
prodID = [1371481]*nIngredients
templateName = ['USGS_WQA_Iowa_1996-1998.pdf']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USGS\Water-Quality Assessment of Eastern Iowa Basins Selected Pesticides and Pesticide Degradates in Streams, 1996-98\Iowa Basins Water Quality.csv',index=False, header=True)