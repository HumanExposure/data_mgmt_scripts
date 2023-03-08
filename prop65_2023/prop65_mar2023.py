# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 14:52:54 2023

@author: ALarger

A csv copy of the prop 65 list was used for this extraction instead of pdf
Download the csv here: https://oehha.ca.gov/proposition-65/proposition-65-list/
"""

import string, os, csv
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

chemName = []
casN = []


path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Prop 65'
os.chdir(path)

i=0
chemicallist = csv.reader(open('p65chemicalslist.csv'))
for row in chemicallist:
    i+=1
    if i < 13 or i > 1032: continue
    elif "delisted" in row[0].lower(): continue
    elif row[0].strip() == '' and row[3].strip() == '': continue
    else:
        chemName.append(row[0])
        if any(x in '1234567890' for x in row[3]):
            casN.append(row[3])
        else: casN.append('')

nIngredients = len(chemName)
templateName = ['p65chemicalslistsinglelisttable2021p.pdf']*nIngredients
prodID=['1660309']*nIngredients
msdsDate = ['January 27, 2023']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'OEHHA Proposition 65_2023.csv',index=False, header=True)