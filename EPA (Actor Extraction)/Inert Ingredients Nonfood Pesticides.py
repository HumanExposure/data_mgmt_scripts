# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 10:52:16 2019

@author: ALarger

EPA Inert Ingredients Permitted for Use in Nonfood Use Pesticide Products
"""

import camelot, string
import pandas as pd

chemName = []
casN = []
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Inert Ingredients Permitted for Use in Nonfood Use Pesticide Products\document_1365245.pdf',pages='all', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    for index, row in df.iterrows():
        chem = ''
        cas = ''
        line=row[0].replace('\n','  ')
        line = line.split('  ')
        for element in line:
            if element == '': continue
            elif any(c not in ['0','1','2','3','4','5','6','7','8','9','-','N','A','/',' '] for c in element):
                chem = chem + ' ' + element.strip()
            else:
                cas = cas + element
        if cas == '' and chem.strip()[0].isupper() == False:
            chemName[-1] = chemName[-1] + chem
        else:
            chemName.append(chem)
            casN.append(cas)
    i+=1

j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace(',','_')
    chemName[j] = chemName[j].replace(';','_')
    chemName[j] = chemName[j].replace('.','')
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].replace('  ',' ').strip()
    chemName[j] = chemName[j].replace('α','alpha')
    chemName[j] = chemName[j].replace('ω','omega')
    chemName[j] = clean(chemName[j])

nIngredients = len(chemName)
prodID = [1365244]*nIngredients
templateName = ['inert_nonfooduse_a.pdf']*nIngredients
msdsDate = ['January 7, 2008']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Inert Ingredients Permitted for Use in Nonfood Use Pesticide Products\Inert Ingredients Nonfood Pesticides.csv',index=False, header=True, date_format=None)