# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 09:33:01 2019

@author: ALarger

Actor Arizona 2007 Pesticides Annual Report Chemical Extraction
"""

import camelot
import pandas as pd

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\document_320436.pdf',pages='22,23,24', flavor='lattice')
frames = [tables[0].df,tables[1].df,tables[2].df]
df = pd.concat(frames, ignore_index=True)
for index,row in df.iterrows(): #get rid of commas
    row[6]=row[6].replace(',','_')
    
nIngredients = len(df)
prodID = [320436]*nIngredients
templateName = ['Arizona_PestUse_2006.pdf']*nIngredients
msdsDate = [2007]*nIngredients
recUse = ['Pesticides: Active Ingredients']*nIngredients
casN = df.loc[:,5]
chemName = df.loc[:,6]
catCode = ['ACToR_Assays_557']*nIngredients
descrip = ['pesticide active_ingredient']*nIngredients
code = ['Arizona_PestUse_2006_AID_1']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df=df.drop(df.index[0])
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Arizona 2007 Pesticides Annual Report.csv',index=False, header=True, date_format=None)
