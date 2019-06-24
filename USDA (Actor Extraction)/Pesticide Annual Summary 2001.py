# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 09:27:12 2019

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
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2001\document_1363478.pdf', pages='48-92', guess=False, lattice=False, multiple_tables=True)
for n in df:
    for index, row in n.iterrows():
        inChem = True
        if n.shape[1] == 1:
            for word in row[0].strip().replace('  ',' ').split(' '):
                if all(c.isalpha()==False for c in word): 
                    inChem = False
                    break
            if inChem == True:
                chem = row[0].split('(')[0].strip()
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
                if 'total' in commodity.lower() or 'total' in chem.lower() or detected == '0' or chem == '' or 'Appendix' in commodity: continue
                chemName.append(chem)
                templateName.append('2001 ' + commodity + '.pdf')
                funcUse.append(use)
        else:
            try:
                if pd.isnull(row[1]):
                    chem = row[0].split('(')[0].strip()
                    use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
                else:
                    commodity = row[0].split('(')[0].strip()
                    if commodity == 'Total': continue
                    if ' ' in row[1]:
                        detected = row[1].split(' ')[-1].strip()
                    else:
                        detected = row[2].strip()
                    if 'total' in commodity.lower() or 'total' in chem.lower() or detected == '0' or chem == '' or 'Appendix' in commodity or 'Pesticide' in commodity: continue
                    chemName.append(chem)
                    templateName.append('2001 ' + commodity + '.pdf')
                    funcUse.append(use)
            except: pass

#Rice    
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2001\document_1363478.pdf', pages='94-95', guess=False, lattice=False, multiple_tables=True)
for n in df:
    for index, row in n.iterrows():
        if len(row)>3: 
            try:
                if len(row[2].split(' ')) > 1 and '.' not in row[2].split(' ')[1] and any(c.isalpha() for c in row[2].split(' ')[1]) == False:
                    chem = row[1].split('(')[0].strip()
                    use = ', '.join(re.findall('\(.*?\)',row[1])).replace('(','').replace(')','')
                    commodity = 'Rice'
                    chemName.append(chem)
                    templateName.append('2001 ' + commodity + '.pdf')
                    funcUse.append(use)
            except: pass
        else:
            try:
                if len(row[1].split(' ')) > 1 and '.' not in row[1].split(' ')[1] and any(c.isalpha() for c in row[1].split(' ')[1]) == False:
                    chem = row[0].split('(')[0].strip()
                    use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
                    commodity = 'Rice'
                    chemName.append(chem)
                    templateName.append('2001 ' + commodity + '.pdf')
                    funcUse.append(use)
            except: pass
   
#Beef  
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2001\document_1363478.pdf', pages='106-114', guess=False, lattice=False, multiple_tables=True)
chem = ''
for n in df:
    for index, row in n.iterrows():
        if pd.isnull(row[0]) or '=' in row[0] or row[0] == 'Pesticide': continue
        if pd.isnull(row[1]):
            chem = row[0].split('(')[0].strip()
            use = ', '.join(re.findall('\(.*?\)',row[0])).replace('(','').replace(')','')
            continue
        else:
            if (len(row[1].split(' ')) > 1 and '.' in row[1].split(' ')[1]) or (len(row[1].split(' ')) == 1 and pd.isnull(row[2])) or (len(row[1].split(' ')) > 2 and row[1].split(' ')[2] == '^'):     
                continue
            commodity = row[0].split('(')[0].strip()
        chemName.append(chem)
        templateName.append('2001 ' + commodity + '.pdf')
        funcUse.append(use)
            
#Drinking Water
df = tabula.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2001\document_1363478.pdf', pages='116-120', guess=False, lattice=False, multiple_tables=True)
commodity = 'Drinking Water'
#Add water residues that couldn't be read (pg 116)
chemName.extend(['Alachlor ethanesulfonic acid (ESA)','Alachlor oxanilic acid (OA)','Atrazine','Bentazon'])
templateName.extend(['2001 ' + commodity + '.pdf']*4)
funcUse.extend(['']*4)
for n in df:
    for index, row in n.iterrows():
        try:
            if (len(row[1].split(' ')) > 1 and '.' not in row[1].split(' ')[1] and any(c.isalpha() for c in row[1].split(' ')[1]) == False) or (pd.isnull(row[2]) == False and any(c not in '1234567890 ' for c in row[2]) == False):
                chem = row[0]
                chemName.append(chem)
                templateName.append('2001 ' + commodity + '.pdf')
                funcUse.append('')
        except: pass
    
for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2001\usda_pesticide_annual_summary_2001_documents_20190624.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break
    
nIngredients = len(chemName)
msdsDate = ['2001']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Pesticide Annual Summary 2001\Pesticide 2001.csv',index=False, header=True)