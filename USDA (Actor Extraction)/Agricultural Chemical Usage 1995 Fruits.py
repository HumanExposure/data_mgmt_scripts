# -*- coding: utf-8 -*-
"""
Created on Tue May 14 16:07:42 2019

@author: ALarger
"""

import string
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Agricultural Chemical Usage 1995 Fruits Summary\1995 Oranges.txt')

chemName = []
templateName = []
prodID = []
i = 1372713
inChems = False
inClasses = False
fruit = ''
dashes = 0

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
            prodID.append('1372739')
            templateName.append('1995 Herbicides.txt')
            chemName.append(cline[1])
        if 'I' in cline[0]:
            prodID.append('1372740')
            templateName.append('1995 Insecticides.txt')
            chemName.append(cline[1])
        if 'F' in cline[0]:
            prodID.append('1372741')
            templateName.append('1995 Fungicides.txt')
            chemName.append(cline[1])
        if 'O' in cline[0]:
            prodID.append('1372742')
            templateName.append('1995 Other Chemicals.txt')
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
        if cline.split(':')[0].strip() in ['','Agricultural','Chemical 2/','Fertilizers','Herbicides','Insecticides','Other Chemicals', 'Fungicides','Chemical','Primary','Nutrient','California','Florida','Major States','Georgia','Michigan','New Jersey','New York','Oregon','Pennsylvania','South Carolina','Washington','Total']: 
            continue
        elif 'Agricultural Chemical Applications,' in cline or 'Fertilizer Primary Nutrient Applications,' in cline: 
            fruit = cline.split(':')[0].strip()
            inChems = True
            continue
        elif inChems == True: 
            if len(templateName) > 0 and templateName[-1] != ('1995 ' + fruit + '.txt'):
                i += 1
            prodID.append(i)
            chemName.append(cline.split(':')[0].strip())
            templateName.append('1995 ' + fruit + '.txt')
            if chemName[-1][-1] == '/':
                chemName[-1] = chemName[-1][:-2].strip()

prodID.extend(['1372738']*3) #Add fertilizers (not in separate table)
templateName.extend(['1995 Fertilizers.txt']*3)
chemName.extend(['Nitrogen','Phosphate','Potash'])

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
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Agricultural Chemical Usage 1995 Fruits Summary\USDA Fruits 1995.csv',index=False, header=True)