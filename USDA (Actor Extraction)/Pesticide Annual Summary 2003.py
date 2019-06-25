# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 10:51:07 2019

@author: ALarger
"""

import camelot, re, csv
import pandas as pd

chemName = []
templateName = []
funcUse = []
prodID = []

#Fruits and Veggies
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\document_1363482.pdf', pages='55-93', flavor='stream')
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
                templateName.append(('2003 ' + commodity + '.pdf').replace('/',' and ').replace('Conc.','Conc').replace('Concen.','Conc'))
                funcUse.append(use)
        except: pass
    
#Triazole Special Survey
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\document_1363482.pdf', pages='95-97', flavor='stream')
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
                templateName.append(('2003 ' + commodity + '.pdf').replace('/',' and ').replace('Conc.','Conc').replace('Concen.','Conc'))
                funcUse.append(use)
        except: pass
    
#Barley    
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\document_1363482.pdf', pages='99-100', flavor='stream')
commodity = 'Barley'
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
                elif row[1].strip() == 'R':
                    use = 'Insect Growth Regulator'
                templateName.append('2003 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
    
#Wheat Flour    
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\document_1363482.pdf', pages='102-103', flavor='stream')
commodity = 'Wheat Flour'
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
                elif row[1].strip() == 'R':
                    use = 'Insect Growth Regulator'
                templateName.append('2003 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
    
#Butter   
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\document_1363482.pdf', pages='105-108', flavor='stream')
commodity = 'Butter'
finishName = False #Flag for getting the end of names that are split between rows
for table in tables: 
    df = table.df
    for index, row in df.iterrows():
        try:
            if finishName == True:
                chemName[-1] = chemName[-1] + ' ' + row[0].split('(')[0].strip()
                finishName = False
                continue
            if row[3] != '' and any(c not in '1234567890 ' for c in row[3]) == False:
                chem = row[0].split('(')[0].strip()
                chemName.append(chem)
                if chemName[-1] == '': #Chem name split between two lines
                    chemName[-1] = lastRow[0].split('(')[0].strip()
                    finishName = True 
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
                templateName.append('2003 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
        lastRow = row
        
#Drinking Water   
tables = camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\document_1363482.pdf', pages='110-116', flavor='stream')
commodity = 'Drinking Water'
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
                elif row[1].strip() == 'O':
                    use = 'Molluscicide'
                elif row[1].strip() == 'P':
                    use = 'Plant Growth Regulator'
                elif row[1].strip() == 'W':
                    use = 'Wood Preservative'
                templateName.append('2003 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\usda_pesticide_annual_summary_2003_documents_20190625.csv'))
    prodID.append('')
    for row in template:
        if row[3] == t:
            prodID[-1] = row[0]
            break
    
nIngredients = len(chemName)
msdsDate = ['2003']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2003\Pesticide 2003.csv',index=False, header=True)