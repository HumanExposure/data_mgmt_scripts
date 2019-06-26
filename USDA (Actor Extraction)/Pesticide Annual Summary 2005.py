# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:58:07 2019

@author: ALarger
"""

import camelot, re, csv
import pandas as pd

chemName = []
templateName = []
funcUse = []
prodID = []

#Fruits and Veggies 
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='52-97', flavor='stream')
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[1] == '' and row[0] != '':
                chem = row[0].split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            elif row[0] == '' and row[1] != '' and row[2] == '':
                chem = row[1].split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[1])).replace('(','').replace(')','')
            elif row[2] != '0' and row[2] != '' and any(c not in '1234567890 ' for c in row[2]) == False and 'TOTAL' not in row[0]:
                commodity = row[0].split('(')[0].strip()
                chemName.append(chem)
                templateName.append(('2005 ' + commodity + '.pdf').replace('Froz.','Frozen'))
                funcUse.append(use)
        except: pass

#Soybeans (Appendices C and D)   
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='99-101,103', flavor='stream')
commodity = 'Soybeans'
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(')[0].strip()
                chemName.append(chem)
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
                elif row[1].strip() == 'P':
                    use = 'Plant Growth Regulator'
                elif row[1].strip() == 'R':
                    use = 'Insect Growth Regulator'
                elif row[1].strip() == 'S':
                    use = 'Herbicide Safener'
                else: 
                    use = ''
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
    
#Wheat    
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='105-107', flavor='stream')
commodity = 'Wheat'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].strip().split('(V')[0]).strip()
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
                elif row[1].strip() == 'R':
                    use = 'Insect Growth Regulator'
                else: 
                    use = ''
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row

#Milk
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='109-111', flavor='stream')
commodity = 'Milk'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].strip()).strip()
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
                else: 
                    use = ''
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Heavy Cream
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='113-115', flavor='stream')
commodity = 'Heavy Cream'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].strip()).strip()
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
                else: 
                    use = ''
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Pork
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='117-126', flavor='stream')
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[1] in ['F','FM','H','HM','I','IM','P','R','S','N','A'] and row[0] != '':
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
                elif row[1].strip() == 'P':
                    use = 'Plant Growth Regulator'
                elif row[1].strip() == 'R':
                    use = 'Insect Growth Regulator'
                elif row[1].strip() == 'S':
                    use = 'Herbicide Safener'
                elif row[1].strip() == 'N':
                    use = 'Nitrification Inhibitor'
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                chem = row[0].strip()
            elif (row[1] != '' and row[2] != '' and any(c not in '1234567890 ' for c in row[1])  == False and any(c not in '1234567890 ' for c in row[2])  == False) or (row[2] != '' and row[3] != '' and any(c not in '1234567890 ' for c in row[2])  == False and any(c not in '1234567890 ' for c in row[3])  == False):
                commodity = row[0].split('(')[0].strip()
                chemName.append(chem)
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass

#Bottled Water
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='128-130', flavor='stream')
commodity = 'Bottled Water'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].strip()).strip()
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
                else: 
                    use = ''
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
    
#Drinking Water
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\document_1363489.pdf', pages='132-147', flavor='stream')
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[1] in ['F','FM','H','HM','I','IM','P'] and row[0] != '':
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
                elif row[1].strip() == 'P':
                    use = 'Plant Growth Regulator'
                else: 
                    use = ''
                chem = row[0].strip()
            elif (row[1] != '' and row[2] != '' and any(c not in '1234567890 ' for c in row[1])  == False and any(c not in '1234567890 ' for c in row[2])  == False) or (row[2] != '' and row[3] != '' and any(c not in '1234567890 ' for c in row[2])  == False and any(c not in '1234567890 ' for c in row[3])  == False):
                commodity = row[0].split('(')[0].strip()
                chemName.append(chem)
                templateName.append('2005 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\usda_pesticide_annual_summary_2005_documents_20190626.csv'))
    prodID.append('')
    for row in template:
        if row[3] == t:
            prodID[-1] = row[0]
            break
    
nIngredients = len(chemName)
msdsDate = ['2005']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2005\Pesticide 2005.csv',index=False, header=True)