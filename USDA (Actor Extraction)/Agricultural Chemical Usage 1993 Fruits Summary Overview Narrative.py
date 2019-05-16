# -*- coding: utf-8 -*-
"""
Created on Tue May 14 10:51:50 2019

@author: ALarger
"""

import string
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Agricultural Chemical Usage 1993 Fruits Summary Overview Narrative\1993 Oranges.txt')

chemName = []
templateName = []
prodID = []
i = 1372651
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
            prodID.append('1372679')
            templateName.append('1993 Herbicides.txt')
            chemName.append(cline[1])
        if 'I' in cline[0]:
            prodID.append('1372680')
            templateName.append('1993 Insecticides.txt')
            chemName.append(cline[1])
        if 'F' in cline[0]:
            prodID.append('1372681')
            templateName.append('1993 Fungicides.txt')
            chemName.append(cline[1])
        if 'O' in cline[0]:
            prodID.append('1372682')
            templateName.append('1993 Other Chemicals.txt')
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
        if cline.split(':')[0].strip() in ['','Agricultural','Chemical 2/','Fertilizers','Herbicides','Insecticides','Other Chemicals', 'Fungicides']: 
            continue
        elif 'Agricultural Chemical Applications,' in cline: 
            fruit = cline.split(':')[0].strip()
            inChems = True
            continue
        elif inChems == True: 
            if len(templateName) > 0 and templateName[-1] != ('1993 ' + fruit + '.txt'):
                i += 1
            prodID.append(i)
            chemName.append(cline.split(':')[0].strip())
            templateName.append('1993 ' + fruit + '.txt')
            if chemName[-1][-1] == '/':
                chemName[-1] = chemName[-1][:-2].strip()

prodID.extend(['1372678']*3) #Add fertilizers (not in separate table)
templateName.extend(['1993 Fertilizers.txt']*3)
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
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Agricultural Chemical Usage 1993 Fruits Summary Overview Narrative\USDA Fruits 1993.csv',index=False, header=True)
