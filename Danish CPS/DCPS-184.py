# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 16:19:14 2023

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


# %%% has numbers def

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)



# %% raw table ext with tabula
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_Yarn\survey and risk assesment of chemicals in knitting yarn.pdf"

# %% Table 1
table_1_raw = read_pdf(file, pages = '15-17', lattice = True, pandas_options={'header': None})


#extraction and clean up
table_1=pd.concat([table_1_raw[0], table_1_raw[1], table_1_raw[2]])
table_1 = table_1.iloc[:,[0]]
table_1 = table_1.dropna(subset=[0])
table_1 = table_1[~table_1[0].str.contains("Substance")]

table_1.reset_index(inplace = True, drop = True)


table_1['raw_cas'] = np.NaN
table_1.columns = ['raw_chem_name', 'raw_cas']


for i,j in enumerate(table_1['raw_chem_name']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        table_1['raw_cas'].iloc[i] = str(match)
        table_1['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-\d','',str(j))
    
for i,j in enumerate(table_1['raw_chem_name']):    
    if 'CAS' in str(j):
        table_1['raw_chem_name'].iloc[i] = str(j).replace('CAS', '')
        
for i,j in enumerate(table_1['raw_chem_name']):
    table_1['raw_chem_name'].iloc[i] = re.sub(r"\r",'',str(j)).strip()
    if '*' in str(j):
        table_1['raw_chem_name'].iloc[i] = table_1['raw_chem_name'].iloc[i].split('*')[0]






clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1)):
    table_1["raw_chem_name"].iloc[j]=str(table_1["raw_chem_name"].iloc[j]).strip().lower()
    table_1["raw_chem_name"].iloc[j]=clean(str(table_1["raw_chem_name"].iloc[j]))
    if len(table_1["raw_chem_name"].iloc[j].split())>1:
        table_1["raw_chem_name"].iloc[j]=" ".join(table_1["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_1["data_document_id"]="1675170"
table_1["data_document_filename"]="yarn_survey_a.pdf"
table_1["doc_date"]="March 2021"
table_1["component"]=""
table_1["raw_category"]=""
table_1["report_funcuse"]=""
table_1["cat_code"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"


table_1 = table_1.loc[:,["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"]]


# %% Table 3 (manual ext)
# %% Table 4 (manual ext)
# %% Table 5 (manual ext)

# %% Table 6
table_6_raw = read_pdf(file, pages = '38', lattice = True, pandas_options={'header': None})


#extraction and clean up

table_6=table_6_raw[0]
table_6 = table_6.iloc[:,[0]]

table_6['raw_cas'] = np.NaN
table_6.columns = ['raw_chem_name', 'raw_cas']
for i,j in enumerate(table_6['raw_chem_name']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.search(r'\d+-\d\d-\d', str(j))[0]
        table_6['raw_cas'].iloc[i] = str(match)
        table_6['raw_chem_name'].iloc[i] = str(j).replace(match, '')
    else:
        continue
    


table_6 = table_6.dropna(subset=['raw_cas'])
table_6.reset_index(inplace = True, drop = True)




clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower()
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())




#Repeating values declaration 
table_6["data_document_id"]="1675174"
table_6["data_document_filename"]="yarn_survey_e.pdf"
table_6["doc_date"]="March 2021"
table_6["component"]=""
table_6["raw_category"]=""
table_6["report_funcuse"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"


table_6 = table_6.loc[:,["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"]]

# %%
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_Yarn\csvs')
merged_tables = table_1.append(table_6, ignore_index=True)
merged_tables.to_csv("knitting_yarn_ext.csv", index = False)

