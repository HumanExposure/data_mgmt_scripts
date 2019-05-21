# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:32:28 2019

@author: ALarger
"""

import string, os, csv
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

os.chdir(r'L:\\Lab\\HEM\\ALarger\\Actor Automated Extraction\\USDA\\Annual Field Crops Summaries 1999')    
execfile = "pdftotext.exe"
execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
cmd = os.path.join(execpath,execfile)
cmd = " ".join([cmd,"-nopgbrk","-layout",'"1999 Corn.pdf"'])
os.system(cmd) #Convert pdf to text
ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 1999\1999 Corn.txt')

chemName = []
templateName = []
prodID = []
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
        if len(cline[0]) > 2 and len(cline[0].split(' ')[0]) < 4:
            cline = [cline[0].split(' ')[0],' '.join(cline[0].split(' ')[1:])]
        if len(cline[0]) > 3:
            continue
        if 'H' in cline[0]:
            templateName.append('1999 Herbicides.pdf')
            chemName.append(cline[1])
        if 'I' in cline[0]:
            templateName.append('1999 Insecticides.pdf')
            chemName.append(cline[1])
        if 'F' in cline[0]:
            templateName.append('1999 Fungicides.pdf')
            chemName.append(cline[1])
        if 'O' in cline[0]:
            templateName.append('1999 Other Chemicals.pdf')
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
        if cline.split(':')[0].strip() in ['','Agricultural','Chemical 2/','Fertilizers','Herbicides','Insecticides','Other Chemicals', 'Fungicides','Chemical','Primary','Nutrient','California','Florida','Major States','Georgia','Michigan','New Jersey','New York','Oregon','Pennsylvania','South Carolina','Washington','Colorado','Illinois','Indiana','Iowa','Kansas','Kentucky','Minnesota','Missouri','Nebraska','North Carolina','Ohio','South Dakota','Texas','Wisconsin','Alabama','Arizona','Arkansas','Louisiana','Mississippi','Tennessee','Idaho','Montana','Oklahoma','North Dakota','Maine','Total']: 
            continue
        elif 'Agricultural Chemical Applications,' in cline or 'Fertilizer Primary Nutrient Applications,' in cline: 
            fruit = cline.split(':')[0].strip()
            inChems = True
            continue
        elif inChems == True: 
            chemName.append(cline.split(':')[0].strip())
            templateName.append('1999 ' + fruit + '.pdf')
            if chemName[-1][-1] == '/':
                chemName[-1] = chemName[-1][:-2].strip()

templateName.extend(['1999 Fertilizers.pdf']*3)
chemName.extend(['Nitrogen','Phosphate','Potash'])

for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 1999\usda-agricultural-chemical-usage-1999-field-crops_20190521.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break

nIngredients = len(chemName)
msdsDate = ['May 2000']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 1999\USDA Field Crops 1999.csv',index=False, header=True)