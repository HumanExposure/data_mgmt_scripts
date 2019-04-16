# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 08:50:22 2019

@author: ALarger

EPA Aerosol Coating RF
TABLE 2A TO SUBPART E OF PART 59—REACTIVITY FACTORS
"""

import camelot, string
import pandas as pd

chemName = []
casN = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))


tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Aerosol Coating RF/document_1365238.pdf',pages='all', flavor='stream'))
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    if i > 0 and i < 4:
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
    i+=1

j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace(',','_')
    chemName[j] = chemName[j].replace(';','_')
    chemName[j] = chemName[j].replace('.','')
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].strip()
    chemName[j] = clean(chemName[j])
    casN[j] = casN[j].replace('–','-')
    if chemName[j] == '':
        del chemName[j]
        del casN[j]
        continue
    
nIngredients = len(chemName)
prodID = [1365238]*nIngredients
templateName = ['EPA_Aerosol_Coating_RF.pdf']*nIngredients
msdsDate = ['June 23, 2009']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Aerosol Coating RF\Aerosol Coating RF.csv',index=False, header=True, date_format=None)