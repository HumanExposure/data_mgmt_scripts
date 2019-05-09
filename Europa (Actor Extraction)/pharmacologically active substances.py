# -*- coding: utf-8 -*-
"""
Created on Thu May  9 09:18:54 2019

@author: ALarger

COMMISSION REGULATION (EU) No  37/2010
of 22  December 2009
on pharmacologically active substances and their classification regarding maximum residue limits
in foodstuffs of animal origin
"""

import camelot, string
import pandas as pd

chemName = []
casN = []
prodID = []
templateName = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Europa\EU pharmacologically active substances and their classification regarding maximum residue limits in foodstuffs of animal origin\Pharmacologically active substances Table 1.pdf',pages='3-72', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    if i == 69: #Table 2
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1372289']*len(df))
        templateName.extend(['Pharmacologically active substances Table 2.pdf']*len(df))
    else: #Table 1
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1372288']*len(df))
        templateName.extend(['Pharmacologically active substances Table 1.pdf']*len(df))
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = clean(chemName[j]).replace('\n',' ').strip().replace('  ',' ')
    if chemName[j] == '' or 'Pharmacologically active' in chemName[j]:
        del chemName[j]
        del prodID[j]
        del templateName[j]
        continue

nIngredients = len(chemName)
msdsDate = ['20.1.2010']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Europa\EU pharmacologically active substances and their classification regarding maximum residue limits in foodstuffs of animal origin\Pharmacologically Active Substances.csv',index=False, header=True)