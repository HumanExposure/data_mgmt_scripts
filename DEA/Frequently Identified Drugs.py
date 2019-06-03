# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 09:26:11 2019

@author: ALarger
"""

import camelot, os, csv
import pandas as pd
from glob import glob

os.chdir(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\National Estimates for Frequently Identified Drugs')    
pdfs = glob("*.pdf")
prodID = []
templateName = []
msdsDate = []
recUse = []
catCode = []
descrip = []
code = []
sourceType = []
chemName = []
casNs = []

for file in pdfs:
    tables = (camelot.read_pdf(file,pages='all', flavor='stream'))
    i=-1
    for table in tables:
        i+=1
        df = tables[i].df
        chemName.extend(df.iloc[:,0])
        prodID.extend([file.strip('.pdf').strip('document_')]*len(df))
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').replace('—','-').strip()
    if chemName[j] == '' or chemName[j] == 'Drug' or 'Table ' in chemName[j] or 'Counts of ' in chemName[j] or 'Methodology' in chemName[j] or 'http' in chemName[j] or 'Data ' in chemName[j] or '=' in chemName[j] or 'publication' in chemName[j] or 'percentage' in chemName[j] or 'reported' in chemName[j] or 'analyzed' in chemName[j] or 'Total' in chemName[j] or 'Reports' in chemName[j]:
        print(chemName[j])
        del chemName[j]
        del prodID [j]
        
            
nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

for j in prodID: #Get template names from prod IDs
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\National Estimates for Frequently Identified Drugs\national-estimates-for-frequently-identified-drugs_20190603.csv'))
    for row in template:
        if row[0] == j:
            templateName.append(row[3])
            break
          
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\DEA\National Estimates for Frequently Identified Drugs\Frequently Identified Drugs.csv',index=False, header=True)