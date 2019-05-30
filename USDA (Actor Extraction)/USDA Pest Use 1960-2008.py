# -*- coding: utf-8 -*-
"""
Created on Thu May 30 13:38:14 2019

@author: ALarger
"""


import camelot
import pandas as pd

chemName = []
prodID = []
templateName = []

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Use in U.S. Agriculture 1960-2008\Pesticideuse19602008_herbicides.pdf',pages='61-64', flavor='stream')
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    
    chemName.extend(df.loc[:,0])
    prodID.extend(['1373585']*len(df))
    templateName.extend(['Pesticideuse19602008_herbicides.pdf']*len(df))
    chemName.extend(df.loc[:,1])
    prodID.extend(['1373586']*len(df))
    templateName.extend(['Pesticideuse19602008_insecticides.pdf']*len(df))
    chemName.extend(df.loc[:,2])
    prodID.extend(['1373587']*len(df))
    templateName.extend(['Pesticideuse19602008_fungicides.pdf']*len(df))
    chemName.extend(df.loc[:,3])
    prodID.extend(['1373588']*len(df))
    templateName.extend(['Pesticideuse19602008_other.pdf']*len(df))

    i+=1

j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].strip()
    if chemName[j] == '' or 'Source:' in chemName[j]:
        del chemName[j]
        del prodID[j]
        del templateName[j]
    j-=1
    
nIngredients = len(chemName)
msdsDate = ['May 2014']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Use in U.S. Agriculture 1960-2008\USDA Pest Use 1960-2008.csv',index=False, header=True, date_format=None)