# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 11:34:48 2019

@author: ALarger
"""

import tabula, re, csv
import pandas as pd

df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 1999\document_1363474.pdf', pages='47-81', guess=False, lattice=False, multiple_tables=True)

chemName = []
templateName = []
funcUse = []
prodID = []

for n in df:
    for index, row in n.iterrows():
        try:
            if any(c.isalpha() for c in row[0].split(' ')[0]) == False and row[0].split(' ')[0] != '^' and row[0].split(' ')[0] != '+':
                chem = (' '.join(row[0].split(' ')[1:])).split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            if any(c not in '1234567890 ' for c in row[1]) == False:
                commodity = row[0].split('(')[0].strip()
                if commodity == 'Total': continue
                if ' ' in row[1]:
                    detected = row[1].split(' ')[-1].strip()
                else:
                    detected = row[2].strip()
                if detected != '0':
                    chemName.append(chem)
                    templateName.append('1999 ' + commodity + '.pdf')
                    funcUse.append(use)
        except: pass
    
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 1999\document_1363474.pdf', pages='91-92', guess=False, lattice=False, multiple_tables=True)

for n in df:
    for index, row in n.iterrows():
        try:
            if len(row[1].split(' ')) > 1 and '.' not in row[1].split(' ')[1] and any(c.isalpha() for c in row[1].split(' ')[1]) == False:
                chem = row[0].split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
                commodity = 'Oats'
                chemName.append(chem)
                templateName.append('1999 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 1999\usda_pesticide_annual_summary_1999_documents_20190621.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break
    
nIngredients = len(chemName)
msdsDate = ['1999']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 1999\Pesticide 1999.csv',index=False, header=True)
