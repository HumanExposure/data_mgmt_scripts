# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 08:49:48 2019

@author: ALarger
"""

import os, string, re
import pandas as pd
from glob import glob

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.strip('\n-')
    cline = cline.split('  ')
    cline = [cline[0]] + [x.strip() for x in cline[1:] if (x != "")] #Leave the first element of a line even if it is a blank space. This will help to differentiate chemical names from functional uses if they take up multiple lines
    return(cline)

os.chdir(r'L:\Lab\HEM\Health Product Declaration\Allison2')    
filenameList = [] #list of file names matching those in the extacted text template
prodList = [] #list of product names
dateList = [] #list of msdsDates
casList = [] #list of CAS numbers
chemList = [] #list of chemical names
funcList = [] #list of functional uses of each chemical
unitList = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...14=percent volume,...)
rankList = [] #list of ingredient ranks
centList = [] #list of central concentrations
nanoList = [] #nano? yes/no

file_list = glob('*.pdf')
numFiles=len(file_list)

#Go through file list
for file in file_list:
    name = ''
    date = ''
    ingredients = []
    inContent = False #Flag for if you are in the content section
    inChem = False #Flag for collecting chemical data that spills over multiple lines
    txt = file.replace('.pdf','.txt').replace('.PDF','.txt')
    ifile = open(txt)
    
    #Parse txt file
    for line in ifile:
        cline = cleanLine(line)
        if cline == [] or cline == ['']: continue
        #Get product name
        if len(cline) > 1 and cline[0] == 'name' and name == '':
            name = ' '.join(cline[1:])
        #Get date
        if 'release date' in cline[0] and date == '':
            if 'x' not in cline[1] and 'self' not in cline[1]:
                date = cline[1]
        #check if you enter content section
        if 'gs' in cline and 'rc' in cline:
            inContent = True
            continue
        #Check if you leave content section
        if 'certifications and' in cline[0] and inContent == True:
            inContent = False
            inChem = False
            
        #In the content section:
        if inContent == True:
            #In ingredient
            if (any(all(x in '1234567890 ._-%' for x in cline[y]) and cline[y] != '-' for y in list(range(1,len(cline)-1))) or ('unknown' in cline and ('n' in cline or 'y' in cline or 'u' in cline or 'no' in cline or 'yes' in cline or 'unk' in cline))) and cline[0] != '' and len(cline) > 3 and inChem == False:
                #Check if the name was split across multiple elements
                for x in list(range(1,len(cline)-1)):
                    if (any(c.isalpha() for c in cline[1]) or sum(c.isdigit() for c in cline[1]) == 1 or cline[1] == '-') and 'unknown' not in cline[1] and 'mixed' not in cline[1] and 'proprietary' not in cline[1] and 'undisclosed' not in cline[1] and 'not registered' not in cline[1] and '%' not in cline[1] and 'cas' not in cline[1] and 'n/a' not in cline[1] and len(cline) > 3:
                        cline = [cline[0] + ' ' + cline[1]] + cline[2:]
                    else: 
                        break
                #Check if the functional use was split across multiple elements
                for x in list(range(1,len(cline)-1)):
                    if (any(c.isalpha() for c in cline[-2]) or cline[-2] == '-') and 'unknown' not in cline[-2] and 'mixed' not in cline[-2] and 'proprietary' not in cline[-2] and 'undisclosed' not in cline[-2] and 'not registered' not in cline[-2] and '%' not in cline[-2] and 'cas' not in cline[-2] and 'n/a' not in cline[-2] and 'lt-' not in cline[-2] and 'bm' not in cline[-2] and len(cline) > 3 and cline[-2] not in ['n','y','u','p1','no','yes','r', 'unk']:
                        cline = cline[:-2] + [cline[-2] + ' ' + cline[-1]] 
                    else: 
                        break
                ingredients.append(cline[0].strip('-'))
                inChem = True
                #CAS
                if all(x in '1234567890- cas' for x in cline[1]):
                    casList.append(cline[1])
                else:
                    casList.append('')
                #Concentration
                if all(x in '1234567890-.%><= ' for x in cline[2]) and len(re.findall('-', cline[2])) <= 1:
                    centList.append(cline[2].strip('% '))
                elif all(x in '1234567890-.%><= ' for x in cline[1]) and '%' in cline[1] and len(re.findall('-', cline[1])) <= 1:
                    centList.append(cline[1].strip('% '))
                else: 
                    centList.append('')
                #Unit (for concentration)
                if centList[-1] == '':
                    unitList.append('')
                else: 
                    unitList.append('%')
                #Nano
                if cline[-2] == 'n' or cline[-2] == 'no':
                    nanoList.append('N')
                elif cline[-2] == 'y' or cline[-2] == 'yes':
                    nanoList.append('Y')
                elif cline[-2] == 'u' or cline[-2] == 'unk':
                    nanoList.append('U')
                else: 
                    nanoList.append('')
                #Functional use
                if len(cline[-1]) > 1 and any(x.isalpha() for x in cline[-1]):
                    funcList.append(cline[-1].strip('-'))
                else: 
                    funcList.append('')
            #Out of chemical name/cas/conc/use and into warnings/notes
            elif inChem == True and any(('warning' in c or 'hazard' in c or 'none found' in c or 'cancer' in c or 'irritat' in c or 'unknown' in c or 'not disclosed' in c or 'respiratory' in c or 'acute' in c or 'endocrine' in c or 'sensiti' in c or 'harmful' in c or 'health product declaration' in c or ' action' in c or 'effects' in c or 'concern' in c or 'human' in c or 'section' in c or 'page' in c or 'toxic' in c or 'epa ' in c or 'priority' in c or 'risk' in c or 'reproductive' in c or 'pbt' in c or 'developmental' in c or 'weight %' in c or 'this listing' in c or 'flammable' in c or 'global warming' in c or 'mammalian' in c or 'development' in c) for c in cline):
                inChem = False
            #chemical names, cas numbers and functional uses sometimes go onto multiple lines. Collect this data
            elif inChem == True:
                if cline[0] != '':
                    ingredients[-1] = ingredients[-1] + ' ' + cline[0]
                if len(cline) > 1:
                    if casList[-1] != '' and all(x in '1234567890- ' for x in cline[1]) and (len(re.findall('-', casList[-1])) < 2 or casList[-1][-1] == '-'):
                        casList[-1] = casList[-1] + cline[1]
                    if any(c.isalpha() for c in cline[-1]) and cline[-1] not in ['n','y','u','p1','no','yes','r', 'unk'] and 'lt-' not in cline[-1]:
                        funcList[-1] = funcList[-1] + ' ' + cline[-1]
                        
    if ingredients == []:
        ingredients = [''] #include doc even if no ingredients were found
    n = len(ingredients)
    chemList.extend(ingredients)
    filenameList.extend([file]*n)
    prodList.extend([name]*n)
    dateList.extend([date]*n)
    rankList.extend(list(range(1,n+1)))

#Make csv
df = pd.DataFrame({'data_document_filename':filenameList, 'prod_name':prodList, 'doc_date':dateList, 'raw_cas':casList, 'raw_chem_name':chemList, 'Nano':nanoList, 'report_funcuse':funcList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList})
df.to_csv('HPD Extracted Data.csv',index=False, header=True)