# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:50:59 2019

@author: ALarger
"""

import csv, string
import pandas as pd

chemName = []
casN = []
code = []
recUse = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

file = csv.reader(open(r'L:\Lab\HEM\ALarger\CDR\2016_cdr_database\Consumer and Commercial Use1.csv','r'))
i = 0
for row in file:
    i+=1
    if i == 1: continue
    chemName.append(clean(row[4]))
    casN.append(row[2])
    code.append(row[1])
    recUse.append(clean(row[43]+'/' + row[44].replace('Both','Consumer and Commercial').replace('NKRA','') + '/' + row[45].replace('Yes','Child').replace('No','Not child').replace('NKRA','')).replace('//','/').rstrip('/').strip())

nIngredients = len(chemName)
msdsDate = ['2016']*nIngredients
descrip = ['']*nIngredients
catCode = ['']*nIngredients
sourceType = ['']*nIngredients
templateName = ['Consumer and Commercial Use1.csv']*nIngredients
prodID = [1374251]*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\CDR\2016_cdr_database\CDR 2016 Consumer.csv',index=False, header=True)