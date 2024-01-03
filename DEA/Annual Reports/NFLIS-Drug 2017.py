# -*- coding: utf-8 -*-
"""
Created on Fri May 31 13:46:10 2019

@author: ALarger
"""

import camelot, csv
import pandas as pd

chemName = []
prodID = []
templateName = []

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\NFLIS-DRUG 2017 ANNUAL REPORT\document_1373608.pdf',pages='7-9,14-18', flavor='stream')
i=-1
for table in tables:
    i+=1
    df = tables[i].df
    inChems = False
    if i == 0: #Table 1.1
        chemName.extend(df.loc[5:29,0])
        prodID.extend([1373601]*25)
    elif i == 1: #Table 1.2
        chemName.extend(df.loc[8:40,2])
        prodID.extend([1373602]*33)
    elif i == 2: #Frequent Drugs Found by Fed Labs
        chemName.extend(df.loc[11:27,0])
        prodID.extend([1373608]*17)
    elif i == 5: #Table 2.1
        chemName.extend(df.loc[2:23,1])
        prodID.extend([1373603]*22)
    elif i == 6: #Table 2.2
        chemName.extend(df.loc[5:,4])
        prodID.extend([1373604]*18)
    elif i == 10: #Table 2.3
        chemName.extend(df.loc[5:,0])
        prodID.extend([1373605]*20)
    elif i == 13: #Table 2.4
        chemName.extend(df.loc[5:,0])
        prodID.extend([1373606]*25)
    elif i == 15: #Table 2.5
        chemName.extend(df.loc[12:39,0])
        prodID.extend([1373607]*28)
    
j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].split('  ')[0] 
    chemName[j] = chemName[j].strip()
    if chemName[j] == '':
        del chemName[j]
        del prodID[j]
    j-=1
    
    
for j in prodID: #Get template names from prod IDs
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\NFLIS-DRUG 2017 ANNUAL REPORT\nflis-drug-2017-annual-report_20190531.csv'))
    for row in template:
        if row[0] == str(j):
            templateName.append(row[3])
            break
    
nIngredients = len(chemName)
msdsDate = ['September 2018']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\NFLIS-DRUG 2017 ANNUAL REPORT\NFLIS-Drug 2017.csv',index=False, header=True)
