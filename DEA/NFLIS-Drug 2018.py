# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:01:12 2019

@author: ALarger
"""

import camelot, csv
import pandas as pd

chemName = []
prodID = []
templateName = []

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\NFLIS-Drug 2018 Midyear Report\document_1373593.pdf',pages='6-7,17-20', flavor='stream')
i=-1
for table in tables:
    i+=1
    df = tables[i].df
    inChems = False
    for row in df.loc[:,0]:
        if inChems == True:
            if 'Total' in row:
                inChems = False
                print('break')
                break
            print(i)
            if row == '': continue
            chemName.append(row)
            prodID.append(1373593+i)
        if row == 'Drug' or 'Reports' in row:
            inChems = True
            continue

for j in prodID:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\NFLIS-Drug 2018 Midyear Report\nflis-drug-2018-midyear-report_20190531.csv'))
    for row in template:
        if row[0] == str(j):
            templateName.append(row[3])
            break
    
nIngredients = len(chemName)
msdsDate = ['April 2019']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\NFLIS-Drug 2018 Midyear Report\NFLIS-Drug 2018.csv',index=False, header=True)