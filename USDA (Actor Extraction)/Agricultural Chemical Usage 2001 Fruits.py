# -*- coding: utf-8 -*-
"""
Created on Thu May 16 14:30:13 2019

@author: ALarger
"""

import string, os
import pandas as pd
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

os.chdir(r'L:\\Lab\\HEM\\ALarger\\Actor Automated Extraction\\USDA\\Agricultural Chemical Usage 2001 Fruits Summary')    
execfile = "pdftotext.exe"
execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
cmd = os.path.join(execpath,execfile)
cmd = " ".join([cmd,"-nopgbrk","-layout",'"2001 Apples.pdf"'])
os.system(cmd) #Convert pdf to text
ifile = open(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Agricultural Chemical Usage 2001 Fruits Summary\2001 Apples.txt')

chemName = []
templateName = []
prodID = []
i = 1372890
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
                prodID.append('1372917')
                templateName.append('2001 Herbicides.txt')
            if 'I' in cline[0]:
                chemName.append(cline[1])
                prodID.append('1372918')
                templateName.append('2001 Insecticides.txt')
            if 'F' in cline[0]:
                chemName.append(cline[1])
                prodID.append('1372919')
                templateName.append('2001 Fungicides.txt')
            if 'O' in cline[0]:
                chemName.append(cline[1])
                prodID.append('1372920')
                templateName.append('2001 Other Chemicals.txt')
        except: pass
        continue
    cline = cline.strip()
    if cline == '': continue
    if cline.split('  ')[0].strip() == 'Class':
        inClasses = True

    if ':' in cline and 'Agricultural Chemical Applications,' in cline: 
        fruit = cline.split(':')[0].strip()
        inChems = True
        continue
    if inChems == True: 
        if 'See footnote' in cline or 'Area applied' in cline or 'Bearing acres' in cline or 'Agricultural Chemical Usage' in cline:
            inChems = False
            continue
        if '2001' in cline or 'Agricultural' in cline or 'Chemical' in cline or 'Herbicide' in cline or 'Insecticide' in cline or 'Fungicide' in cline or 'continued' in cline or any(c.isalpha() for c in cline.split('  ')[0]) == False:
            continue
        if len(templateName) > 0 and templateName[-1] != ('2001 ' + fruit + '.txt'):
            i += 1
        prodID.append(i)
        chemName.append(cline.split('  ')[0].strip())
        templateName.append('2001 ' + fruit + '.txt')
        chemName[-1] = chemName[-1].rstrip(' 1').rstrip(' 2').rstrip(' 3').rstrip(' 4')

nIngredients = len(chemName)
msdsDate = ['August 2002']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\USDA\Agricultural Chemical Usage 2001 Fruits Summary\USDA Fruits 2001.csv',index=False, header=True)