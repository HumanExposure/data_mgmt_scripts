# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:14:13 2019

@author: ALarger
"""

import camelot, re, csv
import pandas as pd

chemName = []
templateName = []
funcUse = []
prodID = []
chem = ''

#Fruits and Veggies
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\document_1363480.pdf', pages='52-94', flavor='stream')
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if row[1] == '' and row[0] != '':
            chem = row[0].split('(')[0].strip()
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
        elif row[2] != '0' and row[2] != '' and any(c not in '1234567890 ' for c in row[2]) == False and 'TOTAL' not in row[0]:
            commodity = row[0].split('(')[0].strip().replace('/',' and ') #Can't have / in filename
            chemName.append(chem)
            templateName.append(('2002 ' + commodity + '.pdf').replace('Canned.pdf','Canned and Frozen.pdf'))
            funcUse.append(use)

#Rice    
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\document_1363480.pdf', pages='96', flavor='stream')
commodity = 'Rice'
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if row[2] != '' and any(c not in '1234567890 ' for c in row[2]) == False:
            chem = row[0].split('(')[0].strip()
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            chemName.append(chem)
            templateName.append('2002 ' + commodity + '.pdf')
            funcUse.append(use)

#Barley    
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\document_1363480.pdf', pages='98-99', flavor='stream')
commodity = 'Barley'
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if row[2] != '' and any(c not in '1234567890 .' for c in row[2].replace('\n','')) == False:
            chem = row[0].split('(')[0].strip()
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            chemName.append(chem)
            templateName.append('2002 ' + commodity + '.pdf')
            funcUse.append(use)

   
#Beef  
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\document_1363480.pdf', pages='101-109', flavor='stream')
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if row[1] == '' and row[0] != '':
            chem = row[0].split('(')[0].strip()
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
        elif row[2] != '' and any(c not in '1234567890 ' for c in row[2]) == False:
            commodity = row[0].split('(')[0].strip()
            chemName.append(chem)
            templateName.append('2002 ' + commodity + '.pdf')
            funcUse.append(use)          

#Drinking Water
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\document_1363480.pdf', pages='111-116', flavor='stream')
commodity = 'Drinking Water'
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False and row[1].strip() in ['F','H','I','FM','HM','IM']:
            chem = row[0].split('(')[0].strip()
            if row[1].strip() == 'F': 
                use = 'Fungicide'
            elif row[1].strip() == 'H': 
                use = 'Herbicide'
            elif row[1].strip() == 'I':
                use = 'Insecticide'
            elif row[1].strip() == 'FM':
                use = 'Fungicide Metabolite'
            elif row[1].strip() == 'HM':
                use = 'Herbicide Metabolite'
            elif row[1].strip() == 'IM':
                use = 'Insecticide Metabolite'
            chemName.append(chem)
            templateName.append('2002 ' + commodity + '.pdf')
            funcUse.append(use)
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\usda_pesticide_annual_summary_2002_documents_20190625.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break
    
nIngredients = len(chemName)
msdsDate = ['2002']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2002\Pesticide 2002.csv',index=False, header=True)