# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:17:34 2019

@author: ALarger
"""

import camelot
import pandas as pd

chemName = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USGS\Water Quality and Evaluation of Pesticides in Lakes in the Ridge Citrus Region of Central Florida\document_1371472.pdf',pages='59-60', flavor='stream')) 

for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if row[0] == '' or 'Lake' in row[0] or row[0] == 'Compound': continue
        chemName.append(row[0].replace('-NL','').replace('-KS',''))

nIngredients = len(chemName)
msdsDate = ['2009']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
prodID = [1371472]*nIngredients
templateName = ['sir2008-5178_choquette_a.pdf']*nIngredients
funcUse = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USGS\Water Quality and Evaluation of Pesticides in Lakes in the Ridge Citrus Region of Central Florida\Central Florida Lakes.csv',index=False, header=True)
