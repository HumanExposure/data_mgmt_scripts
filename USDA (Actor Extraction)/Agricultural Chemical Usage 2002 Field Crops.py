# -*- coding: utf-8 -*-
"""
Created on Tue May 21 13:33:20 2019

@author: ALarger
"""

import string, os, csv
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

os.chdir(r'L:\\Lab\\HEM\\ALarger\\Actor Automated Extraction\\USDA\\Annual Field Crops Summaries 2002')    
execfile = "pdftotext.exe"
execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
cmd = os.path.join(execpath,execfile)
cmd = " ".join([cmd,"-nopgbrk","-layout",'"2002 Corn.pdf"'])
os.system(cmd) #Convert pdf to text
ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 2002\2002 Corn.txt')

chemName = []
templateName = []
prodID = []
inChems = False
inClasses = False
fruit = ''

for line in ifile:
    cline = clean(line)
    if inClasses == True:
        if 'Agricultural Chemical Usage' in cline:
            inClasses = False
            continue
        cline = cline.split('  ')
        cline = [x.strip() for x in cline if x != ""]
        try:
            if 'H' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2002 Herbicides.pdf')
            if 'I' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2002 Insecticides.pdf')
            if 'F' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2002 Fungicides.pdf')
            if 'O' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2002 Other Chemicals.pdf')
        except: pass
        continue
    cline = cline.strip()
    if cline == '': continue
    if cline.split('  ')[0].strip() == 'Class':
        inClasses = True
        print('here')
    if ':' in cline and ('Agricultural Chemical Applications,' in cline or 'Primary Nutrient Applications,' in cline) or cline == 'Oranges excluding Temples: Fertilizer': 
        fruit = cline.split(':')[0].strip()
        inChems = True
        continue
    if inChems == True: 
        if 'See footnote' in cline or 'Area applied' in cline or 'Bearing acres' in cline or 'Agricultural Chemical Usage' in cline or 'Total acres' in cline:
            inChems = False
            continue
        if ' 2002' in cline or 'Agricultural' in cline or 'Chemical' in cline or 'Herbicide' in cline or 'Insecticide' in cline or 'Fungicide' in cline or 'continued' in cline or 'States' in cline or 'California' in cline or 'Michigan' in cline or 'New York' in cline or 'Carolina' in cline or 'Oregon' in cline or 'Pennsylvania' in cline or 'Washington' in cline or 'Florida' in cline or 'Texas' in cline or 'New Jersey' in cline or 'Georgia' in cline or 'Indiana' in cline or 'Iowa' in cline or 'Minnesota' in cline or 'Nebraska' in cline or 'Ohio' in cline or 'Wisconsin' in cline or 'Montana' in cline or 'Dakota' in cline or 'Illinois' in cline or 'Kansas' in cline or 'Kentucky' in cline or 'Louisiana' in cline or 'Maryland' in cline or 'Missouri' in cline or 'Tennessee' in cline or 'Virginia' in cline or 'Oklahoma' in cline or 'Total' in cline or 'Nutrient' in cline or 'Ingredient' in cline or 'Percent' in cline or any(c.isalpha() for c in cline.split('  ')[0]) == False:
            continue

        chemName.append(cline.split('  ')[0].strip())
        templateName.append('2002 ' + fruit + '.pdf')
        chemName[-1] = chemName[-1].rstrip(' 1').rstrip(' 2').rstrip(' 3').rstrip(' 4')

templateName.extend(['2002 Fertilizers.pdf']*3)
chemName.extend(['Nitrogen','Phosphate','Potash'])

for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 2002\usda-agricultural-chemical-usage-2002-field-crops_20190521.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break

nIngredients = len(chemName)
msdsDate = ['May 2003']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 2002\USDA Field Crops 2002.csv',index=False, header=True)