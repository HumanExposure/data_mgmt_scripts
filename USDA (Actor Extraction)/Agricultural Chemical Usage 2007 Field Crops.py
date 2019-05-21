# -*- coding: utf-8 -*-
"""
Created on Tue May 21 17:31:13 2019

@author: ALarger
"""

import string, os, csv
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

os.chdir(r'L:\\Lab\\HEM\\ALarger\\Actor Automated Extraction\\USDA\\Annual Field Crops Summaries 2007')    
execfile = "pdftotext.exe"
execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
cmd = os.path.join(execpath,execfile)
cmd = " ".join([cmd,"-nopgbrk","-layout",'"2007 Fungicides.pdf"'])
os.system(cmd) #Convert pdf to text
ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 2007\2007 Fungicides.txt')

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
        if len(cline[0]) > 2 and len(cline[0].split(' ')[0]) == 1:
            cline = [cline[0][0],cline[0][2:]]
        if len(cline[0]) > 3:
            continue
        try:
            if 'H' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2007 Herbicides.pdf')
            if 'I' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2007 Insecticides.pdf')
            if 'F' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2007 Fungicides.pdf')
            if 'O' in cline[0]:
                chemName.append(cline[1])
                templateName.append('2007 Other Chemicals.pdf')
        except: pass
        continue
    cline = cline.strip()
    if cline == '': continue
    if cline.split('  ')[0].strip() == 'Class':
        inClasses = True

    if ':' in cline and ('Agricultural Chemical Applications,' in cline or 'Primary Nutrient Applications,' in cline) or cline == 'Oranges excluding Temples: Fertilizer': 
        fruit = cline.split(':')[0].strip()
        inChems = True
        continue
    if inChems == True: 
        if 'See footnote' in cline or 'Area applied' in cline or 'Bearing acres' in cline or 'Agricultural Chemical Usage' in cline or 'Total acres' in cline or 'Publication Status' in cline or 'Planted acre' in cline or 'Insufficient reports' in cline or 'acreage' in cline:
            inChems = False
            continue
        if ' 2006' in cline or 'Agricultural' in cline or 'Chemical' in cline or 'Herbicide' in cline or 'Insecticide' in cline or 'Fungicide' in cline or 'continued' in cline or 'States' in cline or 'California' in cline or 'Michigan' in cline or 'New York' in cline or 'Carolina' in cline or 'Oregon' in cline or 'Pennsylvania' in cline or 'Washington' in cline or 'Florida' in cline or 'Texas' in cline or 'New Jersey' in cline or 'Georgia' in cline or 'Indiana' in cline or 'Iowa' in cline or 'Minnesota' in cline or 'Nebraska' in cline or 'Ohio' in cline or 'Wisconsin' in cline or 'Montana' in cline or 'Dakota' in cline or 'Illinois' in cline or 'Kansas' in cline or 'Kentucky' in cline or 'Louisiana' in cline or 'Maryland' in cline or 'Missouri' in cline or 'Tennessee' in cline or 'Virginia' in cline or 'Oklahoma' in cline or 'Idaho' in cline or 'Utah' in cline or 'Maine' in cline or 'Arizona' in cline or 'Arkansas' in cline or 'Mississippi' in cline or 'Colorado' in cline or 'Alabama' in cline or 'Total' in cline or 'Nutrient' in cline or 'Ingredient' in cline or 'Percent' in cline or ' lbs' in cline or 'Crop Year' in cline or any(c.isalpha() for c in cline.split('  ')[0]) == False:
            continue

        chemName.append(cline.split('  ')[0].strip())
        templateName.append('2007 ' + fruit + '.pdf')
        chemName[-1] = chemName[-1].rstrip(' 1').rstrip(' 2').rstrip(' 3').rstrip(' 4')

templateName.extend(['2007 Fertilizers.pdf']*4)
chemName.extend(['Nitrogen','Phosphate','Potash','Sulfur'])

for t in templateName:
    template = csv.reader(open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 2007\usda-agricultural-chemical-usage-2007-field-crops_20190521.csv'))
    for row in template:
        if row[3] == t:
            prodID.append(row[0])
            break

nIngredients = len(chemName)
msdsDate = ['May 2008']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Annual Field Crops Summaries 2007\USDA Field Crops 2007.csv',index=False, header=True)