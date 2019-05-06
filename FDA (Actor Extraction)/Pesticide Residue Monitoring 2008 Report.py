# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:05:38 2019

@author: ALarger

FDA Pesticide Monitoring Program - FY 2008
"""

import camelot, string
import pandas as pd

chemName = []
prodID = []
templateName = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Pesticide Monitoring Program - FY 2008\Pesticide Residue Monitoring 2008 Report Table 3.pdf',pages='21-31', flavor='lattice')
i=0 
for table in tables:
    df = tables[i].df
    if i <= 5: #Table 3
        chemName.extend(df.iloc[:,0])
        chemName.extend(df.iloc[:,1])
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1372239']*len(df)*3)
        templateName.extend(['Pesticide Residue Monitoring 2008 Report Table 3.pdf']*len(df)*3)
    elif i == 7: #Table 5
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1372240']*len(df))
        templateName.extend(['Pesticide Residue Monitoring 2008 Report Table 5.pdf']*len(df))
    elif i == 8: #Table 6
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1372241']*len(df))
        templateName.extend(['Pesticide Residue Monitoring 2008 Report Table 6.pdf']*len(df))
    elif i == 9: #Table 7
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1372242']*len(df))
        templateName.extend(['Pesticide Residue Monitoring 2008 Report Table 7.pdf']*len(df))
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').rstrip('+').strip().rstrip('*').strip().lower().replace('  ',' ')
    if prodID[j] != '1372239': chemName[j] = chemName[j].rstrip('2').rstrip('3').rstrip('4').rstrip('5')
    if chemName[j] == '' or 'pesticide' in chemName[j] or chemName[j] == 'all others':
        del chemName[j]
        del templateName[j]
        del prodID[j]
        
nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\FDA\Pesticide Monitoring Program - FY 2008\Pesticide Residue Monitoring 2008 Report.csv',index=False, header=True, date_format=None)