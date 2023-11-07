# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 10:49:34 2023

@author: CLUTZ01
"""

# %% imports
from tabula import read_pdf
import pandas as pd
import string
import os
import glob
import re


import numpy as np
# %%% CleanLine Def
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('–','-').replace('≤','<=').replace('®', '').replace('â', '').replace('€“', '-')
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)


# %% file set up
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides')
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides\pesticides_in_flowers_outside_eu_report.pdf'


# %% Table 2


ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)
# re.sub(' +', ' ', cleaned)

if cleaned == '': print(file)


lines = cleaned.split('\n')
lines = [x for x in lines if len(x) > 1]


for i,j in enumerate(lines):
    if 'table 2' in str(j) :
        start = i
        continue
    elif 'table 3' in str(j) and not '(' in str(j):
        stop = i
        break

table_2_lines = lines[start:stop]
months = ['april', 'october', 'january', 'jun', 'april', 'september', 'sept', 'may', 'period']
table_2_edit = []
is_month = False
for i,j in enumerate(table_2_lines):
    if 'survey of pesticides in flowers' in str(j) or 'active substance status eu comment' in str(j) or ' approved in database' in str(j) or 'malaysia' in str(j):
        continue
    
    else:    
        if 'approved' in str(j):
            j_cl = str(j).split('approved')[0].strip()

        elif " - " in str(j):
            j_cl = str(j).split(' - ')[0].strip()
        else:
            j_cl = str(j)
    
    table_2_edit.append(j_cl)


table_2_edit2 = []
for i,j in enumerate(table_2_edit):
    for month in months:
        if str(month) in str(j):
            is_month = True
            break
        else:
            continue

    if is_month == True:
        is_month = False
        continue
    else:
        table_2_edit2.append(j)

        
        
       
table_2_df = pd.DataFrame(table_2_edit2, columns=['raw_chem_name'])

table_2_df['number'] = np.NaN
for i,j in enumerate(table_2_df['raw_chem_name']):
    if re.search('^\d{1,2}', str(j)):
        match = re.match('^\d{1,2}', str(j))[0]
        table_2_df['number'].iloc[i] = int(match)
   
        
        
        
table_2_df.fillna(method='ffill', inplace=True)
table_2_df = table_2_df.groupby(['number'], as_index=False)['raw_chem_name'].apply(''.join)
table_2_df = table_2_df.loc[:,['raw_chem_name', 'number']]

table_2_df = table_2_df.sort_values('number')
table_2_df = table_2_df.loc[:,['raw_chem_name']]

for i,j in enumerate(table_2_df['raw_chem_name']):
    new = re.sub(r'\d{1,2}\s',"", str(j)).strip()
    new = new.replace('not', '').strip()
    table_2_df['raw_chem_name'].iloc[i] = new
        
table_2 = table_2_df
        




# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))
    if len(table_2["raw_chem_name"].iloc[j].split())>1:
        table_2["raw_chem_name"].iloc[j]=" ".join(table_2["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration 
table_2["data_document_id"]="1687019"
table_2["data_document_filename"]="flower_pesticides_table_2.pdf"
table_2["doc_date"]="February 2022"
table_2["raw_cas"]=""
table_2["component"]=""
table_2["raw_category"]=""
table_2["report_funcuse"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides\csvs')
table_2.to_csv("flower_pesticides_table_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)





# %% Appendix 1.2

append_1_2_raw = read_pdf(file, pages = '39', lattice = True, pandas_options={'header': None})



# %%% extraction and clean up
append_1_2 = append_1_2_raw[0]
append_1_2 = append_1_2.iloc[2:,[0,1]]

append_1_2.columns = ['raw_chem_name', 'report_funcuse']
append_1_2.reset_index(drop = True, inplace = True)



# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_1_2)):
    append_1_2["raw_chem_name"].iloc[j]=str(append_1_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    append_1_2["raw_chem_name"].iloc[j]=clean(str(append_1_2["raw_chem_name"].iloc[j]))
    append_1_2["report_funcuse"].iloc[j]=str(append_1_2["report_funcuse"].iloc[j]).strip().lower()
    append_1_2["report_funcuse"].iloc[j]=clean(str(append_1_2["report_funcuse"].iloc[j]))
    if len(append_1_2["raw_chem_name"].iloc[j].split())>1:
        append_1_2["raw_chem_name"].iloc[j]=" ".join(append_1_2["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration 
append_1_2["data_document_id"]="1687020"
append_1_2["data_document_filename"]="flower_pesticides_append_1_2.pdf"
append_1_2["doc_date"]="February 2022"
append_1_2["raw_cas"]=""
append_1_2["component"]=""
append_1_2["raw_category"]=""
append_1_2["cat_code"]=""
append_1_2["description_cpcat"]=""
append_1_2["cpcat_code"]=""
append_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides\csvs')
append_1_2.to_csv("flower_pesticides_append_1_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)




# %% Appendix 1.3

append_1_3_file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides\append_1_3_data.csv'
append_1_3 = pd.read_csv(append_1_3_file)
append_1_3 = append_1_3.iloc[3:,:]


append_1_3.columns = ['raw_chem_name']
append_1_3['raw_cas'] = np.NaN
for i,j in enumerate(append_1_3['raw_chem_name']):
    
    if 'also known' in str(j):
        split = append_1_3['raw_chem_name'].iloc[i].split('also known')[0].strip()
        append_1_3['raw_chem_name'].iloc[i] = split
    try:
        match = re.match(r'\d+-\d\d-\d', str(j))
        append_1_3['raw_cas'].iloc[i] = str(match[0])
        append_1_3['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-\d','',str(j))
    except:
        continue
    
    
    
    
# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_1_3)):
    append_1_3["raw_chem_name"].iloc[j]=str(append_1_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    append_1_3["raw_chem_name"].iloc[j]=clean(str(append_1_3["raw_chem_name"].iloc[j]))
    if len(append_1_3["raw_chem_name"].iloc[j].split())>1:
        append_1_3["raw_chem_name"].iloc[j]=" ".join(append_1_3["raw_chem_name"].iloc[j].split())
        
        
        
for i,j in enumerate(append_1_3['raw_chem_name']):
    
    if 'also known' in str(j):
        split = append_1_3['raw_chem_name'].iloc[i].split('also known')[0].strip()
        append_1_3['raw_chem_name'].iloc[i] = split


append_1_3.reset_index(inplace = True, drop = True)        
        
append_1_3 = append_1_3.iloc[:51,:] 

# %%% Repeating values declaration 
append_1_3["data_document_id"]="1687021"
append_1_3["data_document_filename"]="flower_pesticides_append_1_3.pdf"
append_1_3["doc_date"]="February 2022"
append_1_3["component"]=""
append_1_3["raw_category"]=""
append_1_3["report_funcuse"]=""
append_1_3["cat_code"]=""
append_1_3["description_cpcat"]=""
append_1_3["cpcat_code"]=""
append_1_3["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides\csvs')
append_1_3.to_csv("flower_pesticides_append_1_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% CONCAT ALL csv's TOGETHER
# %%% get files
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Flower Pesticides\csvs')
path = os.getcwd()
files = os.path.join(path, "flower_pesticides_*.csv")

files = glob.glob(files)


# %%% joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv("flower_pesticides_ext.csv", index = False)



