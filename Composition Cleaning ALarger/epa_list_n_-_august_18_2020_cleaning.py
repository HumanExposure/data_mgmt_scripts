# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 10:48:53 2021

@author: ALarger
"""

import csv
import pandas as pd

idList = [] #Product ids
lowerList = [] #Document title
centList = [] #Document type
upperList = [] #Product page urls

file = 'epa_list_n_-_august_18_2020_raw_extracted_records.csv' #Name of raw extracted records file
newName = file.replace('_raw_extracted_records','_cleaned')

template = csv.reader(open(file))
for row in template:
    if row[7] == 'percent' and all(n in '1234567890.' for n in row[5]): 
        idList.append(row[1])
        lowerList.append('')
        centList.append((pd.to_numeric(row[5])/100).round(10))
        upperList.append('')
        # print(row[5],centList[-1])
        if any(pd.to_numeric(n) > 1 or pd.to_numeric(n) < 0 for n in [lowerList[-1],centList[-1],upperList[-1]]): #Check if wf makes sense
            print('concentration out of range:',row) 
    else: print(row) #Print rows not being cleaned

df = pd.DataFrame({'ExtractedChemical_id':idList, 'lower_wf_analysis':lowerList, 'central_wf_analysis':centList, 'upper_wf_analysis':upperList})
df.to_csv(newName,index=False, header=True)