# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:33:37 2019

@author: ALarger

Fragranced consumer products: Chemicals emitted, ingredients unlisted (Supplemental materials)
"""

import camelot, string
import pandas as pd

chemName = []
casN = []
prodID = []
templateName = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Fragranced Consumer Products\document_1359902.pdf',pages='all', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    i+=1
    if i in [1,2,3,4]: #Laundry Product
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        prodID.extend(['1359902']*len(df))
        templateName.extend(['Frangrance_Consumer_Product_supp_w.pdf']*len(df))
    elif i in [5,6,7,9,10,11,12,17,25]: #Personal Care Product
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        prodID.extend(['1359901']*len(df))
        templateName.extend(['Frangrance_Consumer_Product_supp_v.pdf']*len(df))
    elif i in [8,13,15,16]: #Cleaner
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        prodID.extend(['1359900']*len(df))
        templateName.extend(['Frangrance_Consumer_Product_supp_u.pdf']*len(df))
    else: #Air Freshener
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        prodID.extend(['1359899']*len(df))
        templateName.extend(['Frangrance_Consumer_Product_supp_t.pdf']*len(df))
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = clean(chemName[j]).replace('\n',' ').strip().replace('  ',' ')
    casN[j] = casN[j].replace('\n',' ').strip().replace('  ',' ')
    if chemName[j] == '' or 'cas' in casN[j].lower():
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        continue

nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Fragranced Consumer Products\Fragranced Consumer Products.csv',index=False, header=True)