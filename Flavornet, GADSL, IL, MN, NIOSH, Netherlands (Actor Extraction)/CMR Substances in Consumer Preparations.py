# -*- coding: utf-8 -*-
"""
Created on Wed May  8 09:05:42 2019

@author: ALarger

The occurrence of Carcinogenic, Mutagenic and Reprotoxic (CMR) substances in consumer preparations
"""

import camelot, string
import pandas as pd

chemName = []
casN = []
prodID = []
templateName = []
col3 = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

#tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Flavornet, GADSL, IL, MN, NIOSH, Netherlands\The occurrence of Carcinogenic, Mutagenic and Reprotoxic (CMR) substances in consumer preparations\document_1371492.pdf',pages='19-35,50-57', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    if i < 17:
        chemName.extend(df.iloc[:,1])
        casN.extend(df.iloc[:,0])
        prodID.extend(['1371492']*len(df))
        templateName.extend(['The occurrence of Carcinogenic, Mutagenic and Reprotoxic (CMR) substances in consumer preparations Appendix 1']*len(df))
        col3.extend(['-']*len(df))
    elif i < 24: 
        chemName.extend(df.iloc[:,1])
        casN.extend(df.iloc[:,0])
        prodID.extend(['1371491']*len(df))
        templateName.extend(['The occurrence of Carcinogenic, Mutagenic and Reprotoxic (CMR) substances in consumer preparations Appendix 4']*len(df))
        col3.extend(df.iloc[:,2])
    else: 
        chemName.extend(df.iloc[:,1])
        casN.extend(df.iloc[:,0])
        prodID.extend(['1371490']*len(df))
        templateName.extend(['The occurrence of Carcinogenic, Mutagenic and Reprotoxic (CMR) substances in consumer preparations Appendix 5']*len(df))
        col3.extend(['-']*len(df))
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = clean(chemName[j]).replace('\n',' ').strip().replace('  ',' ')
    if chemName[j] == '' or 'cas' in casN[j].lower():
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del col3[j]
        continue
    if 'Carc. Cat.' in chemName[j]:
        chemName[j] = chemName[j].split('Carc. Cat.')[0]
    if casN[j] == '':
        chemName[j-2] = chemName[j-2] + ' ' + chemName[j]
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del col3[j]
        continue

    if chemName[j].lower().count(chemName[j].split(' ')[0].strip(',').lower())>1 and (col3[j] == '' or col3[j][0].islower()):
        #Sometimes the text in the 3rd column ends up in the chem name
        word = chemName[j].split(' ')[0]
        chemName[j] = (word + chemName[j].lower().split(word.lower().strip(','))[1]).replace(',,',',')

nIngredients = len(chemName)
msdsDate = ['2004']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\Flavornet, GADSL, IL, MN, NIOSH, Netherlands\The occurrence of Carcinogenic, Mutagenic and Reprotoxic (CMR) substances in consumer preparations\CMR Substances in Consumer Preparations.csv',index=False, header=True)