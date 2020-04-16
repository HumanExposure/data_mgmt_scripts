# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 16:40:52 2020

@author: ALarger
"""

import os, csv, string
import pandas as pd

os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Scraping\scj sds')
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
compList = [] #List of components

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
extracted = csv.reader(open('scj sds extracted text.csv','r',encoding = "utf-8"))
i = 0
for row in extracted:
    i += 1
    if i == 1: continue
    filenameList.append(row[0])
    template = csv.reader(open('sc_johnson_sds_documents_20200416.csv')) #"Document records" csv from factotum
    docID = ''
    for trow in template:
        if trow[4] == filenameList[-1]:
            idList.append(trow[0])
            break
    if len(idList) < len(filenameList):
        idList.append('')
    prodList.append(clean(row[1]))
    dateList.append(row[2])
    revList.append(row[3])
    useList.append(row[4])
    casList.append(clean(row[5]))
    chemList.append(clean(row[6]))
    funcList.append('')
    if row[8] == '':
        minList.append('')
        maxList.append('')
        unitList.append('')
    else: 
        minList.append(row[8].split('-')[0].strip())
        maxList.append(row[8].split('-')[1].strip())
        unitList.append(3)
    rankList.append(row[9])
    centList.append('')
    compList.append('')

#Create a csv after the script is finished running
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':useList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':compList})
df.to_csv('scj sds upload.csv',index=False, header=True)