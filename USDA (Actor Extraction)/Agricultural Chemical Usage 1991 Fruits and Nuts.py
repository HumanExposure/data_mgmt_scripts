# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:00:57 2019

@author: ALarger
"""

import string, csv
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Fruits and Nuts Summary 1991\1991 Oranges.txt')

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
            templateName.append('1991 Herbicides.txt')
            chemName.append(cline[1])
        if 'I' in cline[0]:
            templateName.append('1991 Insecticides.txt')
            chemName.append(cline[1])
        if 'F' in cline[0]:
            templateName.append('1991 Fungicides.txt')
            chemName.append(cline[1])
        if 'O' in cline[0]:
            templateName.append('1991 Other Chemicals.txt')
            chemName.append(cline[1])
        continue
    cline = cline.strip()
    if cline == '': continue
    if cline.split(':')[0].strip() == 'Class':
        inClasses = True
    if inChems == True and '-------------' in cline:
        dashes += 1
        if dashes == 3:
            inChems = False
            dashes = 0
    if ':' in cline:
        if cline.split(':')[0].strip() in ['','Agricultural','Chemical 2/','Fertilizers','Herbicides','Insecticides','Other Chemicals', 'Fungicides', 'Chemical']: 
            continue
        elif 'Agricultural Chemical Applications,' in cline and 'Nonbearing' not in cline: 
            fruit = cline.split(':')[0].strip()
            inChems = True
            continue
        elif inChems == True: 
            chemName.append(cline.split(':')[0].strip())
            templateName.append('1991 ' + fruit + '.txt')
            if chemName[-1][-1] == '/':
                chemName[-1] = chemName[-1][:-2].strip()

templateName.extend(['1991 Fertilizers.txt']*3)
chemName.extend(['Nitrogen','Phosphate','Potash'])

for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Fruits and Nuts Summary 1991\usda-ag-chemical-use-1991-fruits-and-nuts_20190520.csv'))
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
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Fruits and Nuts Summary 1991\USDA Fruits and Nuts 1991.csv',index=False, header=True)