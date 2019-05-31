# -*- coding: utf-8 -*-
"""
Created on Fri May 31 16:58:45 2019

@author: ALarger
"""

import camelot, csv
import pandas as pd

chemName = []
prodID = []
templateName = []

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\2016 ANNUAL REPORT Revised April 2018\document_1373616.pdf',pages='7-9,14-18', flavor='stream')
i=-1
for table in tables:
    i+=1
    df = tables[i].df
    inChems = False
    if i == 0: #Table 1.1
        chemName.extend(df.loc[4:28,0])
        prodID.extend([1373609]*25)
    elif i == 1: #Table 1.2
        chemName.extend(df.loc[8:39,1])
        prodID.extend([1373610]*32)
    elif i == 3: #Frequent Drugs Found by Fed Labs
        chemName.extend(df.loc[46:62,0])
        prodID.extend([1373616]*17)
    elif i == 5: #Table 2.1
        chemName.extend(df.loc[2:,1])
        prodID.extend([1373611]*21)
    elif i == 6: #Table 2.2
        chemName.extend(df.loc[7:,4])
        prodID.extend([1373612]*21)
    elif i == 9: #Table 2.3
        chemName.extend(df.loc[11:29,0])
        prodID.extend([1373613]*19)
    elif i == 12: #Table 2.4
        chemName.extend(df.loc[7:,0])
        prodID.extend([1373614]*17)
    elif i == 14: #Table 2.5
        chemName.extend(df.loc[11:,0])
        prodID.extend([1373615]*27)
    
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
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\2016 ANNUAL REPORT Revised April 2018\2016-annual-report-revised-april-2018_20190531.csv'))
    for row in template:
        if row[0] == str(j):
            templateName.append(row[3])
            break
    
nIngredients = len(chemName)
msdsDate = ['April 2018']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\2016 ANNUAL REPORT Revised April 2018\NFLIS-Drug 2016.csv',index=False, header=True)