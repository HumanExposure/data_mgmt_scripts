# -*- coding: utf-8 -*-
"""
Created on Mon May 20 14:24:58 2019

@author: ALarger
"""

import string, csv
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 1995\1995 Corn.txt')

chemName = []
templateName = []
prodID = []
dashes = 0

inChems = False
inClasses = False
fruit = ''
for line in ifile:
    cline = clean(line)
    if inClasses == True:
        if '----------' in cline:
            dashes += 1
            continue
        if dashes == 2:
            dashes = 0
            inClasses = False
            continue
        cline = cline.split('  ')
        cline = [x.strip() for x in cline if x != ""]
        if 'H' in cline[0]:
            templateName.append('1995 Herbicides.txt')
            chemName.append(cline[1])
        if 'I' in cline[0]:
            templateName.append('1995 Insecticides.txt')
            chemName.append(cline[1])
        if 'F' in cline[0]:
            templateName.append('1995 Fungicides.txt')
            chemName.append(cline[1])
        if 'O' in cline[0]:
            templateName.append('1995 Other Chemicals.txt')
            chemName.append(cline[1])
        continue
    cline = cline.strip()
    if cline == '': continue
    if cline.split(':')[0].strip() == 'Class':
        inClasses = True
    if 'Publication Status' in cline:
        inChems = False
    if inChems == True and '-------------' in cline:
        dashes += 1
        if dashes == 3:
            inChems = False
            dashes = 0
    if ':' in cline:
        if cline.split(':')[0].strip() in ['','Agricultural','Chemical 2/','Fertilizers','Herbicides','Insecticides','Other Chemicals', 'Fungicides', 'Chemical']: 
            continue
        elif 'Agricultural Chemical Applications,' in cline and 'Percentage of Time' not in cline: 
            fruit = cline.split(':')[0].strip()
            inChems = True
            continue
        elif inChems == True: 
            if ('1995 ' + fruit + '.txt') not in templateName:
                chemName.extend(['Nitrogen','Phosphate','Potash'])
                templateName.extend(['1995 ' + fruit + '.txt']*3)
            chemName.append(cline.split(':')[0].strip())
            templateName.append('1995 ' + fruit + '.txt')
            if chemName[-1][-1] == '/':
                chemName[-1] = chemName[-1][:-2].strip()

templateName.extend(['1995 Fertilizers.txt']*3)
chemName.extend(['Nitrogen','Phosphate','Potash'])

for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 1995\usda-agricultural-chemical-usage-1995-field-crops_20190520.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break

nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 1995\USDA Field Crops 1995.csv',index=False, header=True)