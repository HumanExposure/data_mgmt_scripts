# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 09:05:52 2019

@author: ALarger
"""

import camelot
import pandas as pd

chemName = []
prodID = []
templateName = []
funcUse = []

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\NPIC, NRC, NY, New Zealand, Opasnet\The Chemical Constituents in Cigarettes and Cigarette Smoke Priorities for Harm Reduction\NZ Cigarettes Table 1.pdf',pages='18-22', flavor='lattice')) 

for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        chemName.append(row[1])
        prodID.append(1374308)
        templateName.append('NZ Cigarettes Table 1.pdf')
        funcUse.append('')
    
tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\NPIC, NRC, NY, New Zealand, Opasnet\The Chemical Constituents in Cigarettes and Cigarette Smoke Priorities for Harm Reduction\NZ Cigarettes Table 1.pdf',pages='51-67', flavor='lattice')) 
func = ''
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[0][1] == '.':
                func = row[0].split('.')[-1].strip()
                continue
        except: pass
        chemName.append(row[0])
        prodID.append(1374309)
        templateName.append('NZ Cigarettes Appendix B.pdf')
        funcUse.append(func)
        
m = len(chemName) 
while m > 0: #Go backwards through chemical name list so that the indexing does not get messed up when one is deleted
    m-=1
    chemName[m] = chemName[m].replace('–','-').replace('\n','').replace('\r','').strip()
    if chemName[m] == '' or chemName[m] == 'Chemical' or chemName[m] == 'Additive or Ingredient':
        del chemName[m]
        del prodID[m]
        del templateName[m]
        del funcUse[m]

nIngredients = len(chemName)
msdsDate = ['March 2000']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\NPIC, NRC, NY, New Zealand, Opasnet\The Chemical Constituents in Cigarettes and Cigarette Smoke Priorities for Harm Reduction\NZ Cigarettes.csv',index=False, header=True)