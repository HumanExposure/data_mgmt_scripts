# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:43:37 2019

@author: ALarger
"""

import tabula, re, csv
import pandas as pd

chemName = []
templateName = []
funcUse = []
prodID = []
chem = ''

#Fruits and Veggies
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2000\document_1363475.pdf', pages='46-91', guess=False, lattice=False, multiple_tables=True)
for n in df:
    for index, row in n.iterrows():
        if n.shape[1] == 1:
            if any(c.isalpha() for c in row[0].split(' ')[0]) == False and row[0].split(' ')[0] != '^' and row[0].split(' ')[0] != '+':
                chem = (' '.join(row[0].split(' ')[1:])).split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            else: 
                rowList = row[0].split(' ')
                commodity = ''
                gotName = False
                for m in rowList:
                    if gotName == False:
                        if any(c.isalpha() for c in m) == True:
                            commodity = (commodity + ' ' + m).split('(')[0].strip()
                        else:
                            gotName = True
                    else: 
                        detected = m
                        break
                if commodity == 'Total' or detected == '0' or chem == '' or 'Appendix' in commodity: continue
                chemName.append(chem)
                templateName.append('2000 ' + commodity + '.pdf')
                funcUse.append(use)
        else:
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
                        templateName.append('2000 ' + commodity + '.pdf')
                        funcUse.append(use)
            except: pass
    
#Peanut Butter
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2000\document_1363475.pdf', pages='97-98', guess=False, lattice=False, multiple_tables=True)
commodity = 'Peanut Butter'
for n in df:
    for index, row in n.iterrows():
        chem = ''
        if n.shape[1] == 1:
            rowList = row[0].split(' ')
            rowList = [x.strip() for x in rowList if x != ""]
            gotName = False
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            for m in rowList:
                if gotName == False:
                    if any(c.isalpha() for c in m) == True:
                        chem = (chem + ' ' + m).split('(')[0].strip()
                    else:
                        gotName = True
                else: 
                    detected = m
                    break
            if '.' in detected or chem == '' or 'appendix' in chem.lower() or 'Samples' in chem or 'Detections' in chem: continue
            chemName.append(chem)
            templateName.append('2000 ' + commodity + '.pdf')
            funcUse.append(use)
        else:
            try:
                if len(row[1].split(' ')) > 1 and '.' not in row[1].split(' ')[1] and any(c.isalpha() for c in row[1].split(' ')[1]) == False:
                    chem = row[0].split('(')[0].strip()
                    use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
                    chemName.append(chem)
                    templateName.append('2000 ' + commodity + '.pdf')
                    funcUse.append(use)
            except: pass

#Rice    
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2000\document_1363475.pdf', pages='100-101', guess=False, lattice=False, multiple_tables=True)
for n in df:
    for index, row in n.iterrows():
        try:
            if len(row[1].split(' ')) > 1 and '.' not in row[1].split(' ')[1] and any(c.isalpha() for c in row[1].split(' ')[1]) == False:
                chem = row[0].split('(')[0].strip()
                use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
                commodity = 'Rice'
                chemName.append(chem)
                templateName.append('2000 ' + commodity + '.pdf')
                funcUse.append(use)
        except: pass
   
#POULTRY    
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2000\document_1363475.pdf', pages='103-110', guess=False, lattice=False, multiple_tables=True)
chem = ''
for n in df:
    for index, row in n.iterrows():
        if pd.isnull(row[0]) or '=' in row[0] or row[0] == 'Pesticide': continue
        if pd.isnull(row[1]):
            chem = row[0].split('(')[0].strip()
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            continue
        else:
            if (len(row[1].split(' ')) > 1 and '.' in row[1].split(' ')[1]) or (len(row[1].split(' ')) == 1 and pd.isnull(row[2])):     
                continue
            commodity = 'Poultry ' + row[0].split('(')[0].strip()
        chemName.append(chem)
        templateName.append('2000 ' + commodity + '.pdf')
        funcUse.append(use)
            
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2000\usda_pesticide_annual_summary_2000_documents_20190624.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break
    
nIngredients = len(chemName)
msdsDate = ['2000']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2000\Pesticide 2000.csv',index=False, header=True)