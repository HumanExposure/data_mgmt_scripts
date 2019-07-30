# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 11:20:55 2019

@author: ALarger

Reads in csv of extracted Skin Deep data, separates and cleans ingredient list, and formats data in a template that can be uploaded to factotum
"""

import os, csv, re, string
import pandas as pd

os.chdir(r'L:\Lab\HEM\ALarger\Skin Deep\Sun')    
idList = [] #list of product IDs
filenameList = [] #list of file names matching those in the extacted text template
prodList = [] #list of product names
dateList = [] #list of msdsDates
revList = [] #list of revision numbers
useList = [] #list of recommended uses of products
casList = [] #list of CAS numbers
chemList = [] #list of chemical names
funcList = [] #list of functional uses of each chemical
minList = [] #list of minimum concentrations
maxList = [] #list of maximum concentrations
unitList = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...14=percent volume,...)
rankList = [] #list of ingredient ranks
centList = [] #list of central concentrations

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))    
extracted = csv.reader(open(r'Skin Deep Sun Products All.csv','r'))
i = 0
k = 0
for row in extracted:
    if i%1000 == 0:
        print(i)
    i += 1
    if i == 1: continue
    ingredients = clean(row[6]).lower().replace(';',',').replace('ingredienst','ingredients').replace('ingredient:','ingredients:').replace('inactive ingredients',',').replace('active ingredients',',').replace('other ingredients',',').replace('(and)',',').replace('additional ingredients',',').replace('natural ingredients',',').strip().split(',')
    centComps = ['']*len(ingredients)
    units = ['']*len(ingredients)
    j = len(ingredients)
    while j > 0:
        j -= 1
        ingredients[j] = ingredients[j].split('=')[0].strip(':.- ')
        if ingredients[j].strip() == '' or ingredients[j].startswith('(1)') or ingredients[j].startswith('(2)') or ingredients[j].startswith('(3)') or ingredients[j].startswith('(4)') or ingredients[j].startswith('**'):
            del ingredients[j]
            del centComps[j]
            del units[j]
        else:
            try:
                if any(c not in '1234567890 ' for c in ingredients[j]) == False:
                    ingredients[j+1] = ingredients[j] + ',' + ingredients[j+1]
                    del ingredients[j]
                    del centComps[j]
                    del units[j]
            except:
                ingredients[j-1] = ingredients[j-1] + ',' + ingredients[j]
                del ingredients[j]
                del centComps[j]
                del units[j]
            try:
                if ')' in ingredients[j] and '(' not in ingredients[j]:
                    ingredients[j-1] = ingredients[j-1] + ', ' + ingredients[j]
                    del ingredients[j]
                    del centComps[j]
                    del units[j]
            except: 
                pass
        try:
            if '%' in ingredients[j]:
                percent = re.findall(r'[0-9. -]+%', ingredients[j])
                if len(percent) == 1:
                    ingredients[j] = ingredients[j].replace(percent[0],'')
                    centComps[j] = percent[0].strip('-% ')
                    if 'v/v' in ingredients[j]: 
                        units[j] = 14 
                    else:
                        units[j] = 3
                else:
                    pass
        except:
            pass
        try:
            ingredients[j] = ingredients[j].replace('(1)','').replace('(2)','').replace('(3)','').replace('(4)','').replace('v/v','').replace('w/w','').replace('()','').replace('[]','').replace('( )','').replace('[ ]','').replace('*','').replace('^','').replace('(, ','(').strip()
            if ingredients[j].startswith('and '):
                ingredients[j] = ingredients[j][4:]
            if ingredients[j].startswith('ingredients'):
                ingredients[j] = ingredients[j][11:].strip(': ')
        except:
            pass

        try:
            if ingredients[j] == '':
                if centComps[j] != '' and centComps[j-1] == '':
                    del ingredients[j]
                    del centComps[j-1]
                    del units[j-1]
                elif centComps[j] == '':
                    del ingredients[j]
                    del centComps[j]
                    del units[j]
        except: 
            pass
           
    n = len(ingredients)
    chemList.extend(ingredients)
    unitList.extend(units)
    centList.extend(centComps)
    filenameList.extend([row[0]+'.pdf']*n)
    prodList.extend([row[1]]*n)
    dateList.extend([row[4]]*n)
    revList.extend(['']*n)
    useList.extend([row[5]]*n)
    casList.extend(['']*n)
    funcList.extend(['']*n)
    minList.extend(['']*n)
    maxList.extend(['']*n)
    rankList.extend(list(range(1,n+1)))
    template = csv.reader(open(r'skin_deep_sun_products_documents_20190729.csv'))
    docID = ''
    for row in template:
        if row[3] == filenameList[-1]:
            docID = row[0]
            break
    idList.extend([docID]*n)
    
    if i%1000 == 0: #create a new csv every 1000 products so that it can be loaded into factotum
        k += 1
        df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':useList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList})
        df.to_csv('Skin Deep Sun Upload' + str(k) + '.csv',index=False, header=True)
        idList = [] 
        filenameList = [] 
        prodList = [] 
        dateList = [] 
        revList = []
        useList = [] 
        casList = []
        chemList = [] 
        funcList = [] 
        minList = [] 
        maxList = [] 
        unitList = [] 
        rankList = [] 
        centList = [] 

#Create a csv after the script is finished running
k += 1
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':useList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList})
df.to_csv('Skin Deep Sun Upload' + str(k) + '.csv',index=False, header=True)
