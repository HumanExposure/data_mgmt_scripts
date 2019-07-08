# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 13:10:18 2019

@author: ALarger
"""

import camelot, re, csv
import pandas as pd

chemName = []
templateName = []
funcUse = []
prodID = []

#Fruits and Veggies 
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='51-130', flavor='stream')
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if (row[1] == '' or row[1][0] == '(') and row[0] != '':
                chem = row[0].split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',(row[0]+row[1]+row[2]))).replace('(','').replace(')','')
            elif row[0] == '' and row[1] != '' and row[2] == '':
                chem = row[1].split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[1])).replace('(','').replace(')','')
            elif row[2] != '0' and row[2] != '' and any(c not in '1234567890 ' for c in row[2]) == False and 'TOTAL' not in row[0]:
                commodity = row[0].split('(X')[0].split('(V')[0].strip()
                chemName.append(chem)
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass

#Almonds
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='132-134', flavor='stream')
commodity = 'Almonds'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].strip()
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
                elif row[1].strip() == 'P':
                    use = 'Plant Growth Regulator'
                elif row[1].strip() == 'R':
                    use = 'Insect Growth Regulator'
                elif row[1].strip() == 'S':
                    use = 'Herbicide Safener'
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Honey
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='136-140', flavor='stream')
commodity = 'Honey'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].split('(X')[0].replace('\n',' ').strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].split('(V')[0].split('(X')[0].strip()).strip()
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
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
    
#Catfish
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='142-147', flavor='stream')
commodity = 'Catfish'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].split('(X')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].split('(V')[0].split('(X')[0].strip()).strip()
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
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row

#Corn Grain
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='149-152', flavor='stream')
commodity = 'Corn Grain'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].split('(X')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].split('(V')[0].split('(X')[0].strip()).strip()
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
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Rice
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='154-156', flavor='stream')
commodity = 'Rice'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].split('(X')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].split('(V')[0].split('(X')[0].strip()).strip()
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
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Groundwater
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='158-160', flavor='stream')
commodity = 'Groundwater'
lastRow = ['','']
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(V')[0].split('(X')[0].strip()
                chemName.append(chem)
                if lastRow[1] == '': #Chem name split between two lines
                    chemName[-1] = (lastRow[0].strip() + ' ' + row[0].split('(V')[0].split('(X')[0].strip()).strip()
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
                elif row[1].strip() == 'A':
                    use = 'Acaricide'
                else: 
                    use = ''
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Drinking Water
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\document_1363498.pdf', pages='162-176', flavor='stream')
lastRow = ['','','']
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
                if lastRow[1] == '' and lastRow[2] == '': #Chem name split between two lines
                    chem = (lastRow[0].strip() + ' ' + row[0].strip()).strip()
            elif (row[1] != '' and row[2] != '' and any(c not in '1234567890 ' for c in row[1])  == False and any(c not in '1234567890 ' for c in row[2])  == False) or (row[2] != '' and row[3] != '' and any(c not in '1234567890 ' for c in row[2])  == False and any(c not in '1234567890 ' for c in row[3])  == False):
                commodity = row[0].split('(')[0].strip()
                chemName.append(chem)
                templateName.append('2008 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\usda_pesticide_annual_summary_2008_documents_20190708.csv'))
    prodID.append('')
    for row in template:
        if row[3] == t:
            prodID[-1] = row[0]
            break
    
nIngredients = len(chemName)
msdsDate = ['December 2009']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2008\Pesticide 2008.csv',index=False, header=True)