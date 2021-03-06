# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:05:59 2019

@author: ALarger

Global Automotive Declarable Substance List (2014)
"""

import camelot, string
import pandas as pd

chemName = []
casN = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Flavornet, GADSL, IL, MN, NIOSH, Netherlands\Global Automotive Declarable Substance List (2014)\document_1371494.pdf',pages='7-42', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    chemName.extend(df.iloc[:,1])
    casN.extend(df.iloc[:,2])
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').strip().replace('  ',' ')
    if 'Note' in chemName[j]:
        chemName[j] = chemName[j].split('Note')[0]
    if chemName[j] == '' or chemName[j] == 'Substance':
        del chemName[j]
        del casN[j]
        
nIngredients = len(chemName)
prodID = ['1371494']*nIngredients
templateName = ['GADSL-Document_2014.pdf']*nIngredients
msdsDate = ['2014-04-01']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Flavornet, GADSL, IL, MN, NIOSH, Netherlands\Global Automotive Declarable Substance List (2014)\GADSL 2014.csv',index=False, header=True)