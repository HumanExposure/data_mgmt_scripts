# -*- coding: utf-8 -*-
"""
Created on Wed May 29 13:05:31 2019

@author: ALarger
"""

import string, camelot
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\OEHHA Proposition 65 List\document_1373514.pdf',pages='all', flavor='stream')

chemName = []
casN = []
inChems = False

i=0 
for table in tables:
    df = tables[i].df
    if i > 0:
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,2])
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').replace('α','alpha').replace("′","'").replace("’","'").replace('m','micrometers')
    if j <= 2:
        del chemName[j]
        del casN[j]
    if chemName[j].split(' ')[0] == 'Delisted':
        del chemName[j]
        del casN[j] 
        del chemName[j-1]
        del casN[j-1]
        continue
    if (chemName[j] == '' and casN[j] == '') or 'Delisted' in chemName[j]:
        del chemName[j]
        del casN[j]
        continue
    if len(casN[j]) < 2:
        if chemName[j] == 'salt of':
            chemName[j+1] = chemName[j] + ' ' + chemName[j+1]
            del chemName[j]
            del casN[j]
        else: 
            chemName[j-1] = chemName[j-1] + ' ' + chemName[j]
            del chemName[j]
            del casN[j]
    if '(' in chemName[j] and ')' not in chemName[j]:
        if 'Ciclosporin' in chemName[j]:
            chemName[j] = chemName[j] + chemName[j] + ' ' + chemName[j+1]
            casN[j] = casN[j] + ', ' + casN[j+1]
            del chemName[j+1]
            del casN[j+1]
        else: 
            del chemName[j]
            del casN[j]
    if '(NOTE' in chemName[j]:
        chemName[j] = chemName[j].split('(NOTE')[0]
    if ('/' in casN[j] or ';' in casN[j]) and '/' not in casN[j+1]:
        chemName[j] = chemName[j] + chemName[j+1]
        casN[j] = casN[j] + casN[j+1]
        del chemName[j+1]
        del casN[j+1]
    if j < len(chemName) - 1 and chemName[j+1] == '':
        if casN[j+1] != casN[j]:
            casN[j] = casN[j] + ', ' + casN[j+1]
        del chemName[j+1]
        del casN[j+1]
    chemName[j] = clean(chemName[j].strip())

nIngredients = len(chemName)
templateName = ['p65list030819.pdf']*nIngredients
prodID=[1373514]*nIngredients
msdsDate = ['March 8, 2019']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\OEHHA Proposition 65 List\OEHHA Proposition 65.csv',index=False, header=True)