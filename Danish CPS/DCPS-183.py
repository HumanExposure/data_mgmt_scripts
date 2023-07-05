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
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\pdfs\survey_of_selected_endocrine_disruptors_table_8.pdf'

# %% Table 8
table_8_raw = read_pdf(file, pages = '24-25', lattice = True, pandas_options={'header': None})


#extraction and clean up
table_8=pd.concat([table_8_raw[0], table_8_raw[1]])
table_8 = table_8.iloc[:,[0,1]]
table_8 = table_8.dropna(subset=[0])
table_8.reset_index(inplace = True, drop = True)
table_8 = table_8.iloc[[2,3,4,5,6,7,23],[0,1]]

table_8.columns = ['raw_chem_name', 'raw_cas']


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8)):
    table_8["raw_chem_name"].iloc[j]=str(table_8["raw_chem_name"].iloc[j]).strip().lower()
    table_8["raw_chem_name"].iloc[j]=clean(str(table_8["raw_chem_name"].iloc[j]))
    if len(table_8["raw_chem_name"].iloc[j].split())>1:
        table_8["raw_chem_name"].iloc[j]=" ".join(table_8["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_8["data_document_id"]="1671699"
table_8["data_document_filename"]="endocrine_disruptors_table_8.pdf"
table_8["doc_date"]="December 2020"
table_8["raw_category"]=""
table_8["report_funcuse"]=""
table_8["cat_code"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
table_8.to_csv("endocrine_disruptors_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


# %% Table 9
table_9_raw = read_pdf(file, pages = '26', lattice = True, pandas_options={'header': None})


#extraction and clean up

table_9=table_9_raw[0]
table_9 = table_9.iloc[:,[0,1]]
table_9 = table_9.dropna(subset=[0])
table_9.reset_index(inplace = True, drop = True)
table_9 = table_9.iloc[1:6,:]


table_9.columns = ['raw_chem_name', 'raw_cas']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_9)):
    table_9["raw_chem_name"].iloc[j]=str(table_9["raw_chem_name"].iloc[j]).strip().lower()
    table_9["raw_chem_name"].iloc[j]=clean(str(table_9["raw_chem_name"].iloc[j]))
    if len(table_9["raw_chem_name"].iloc[j].split())>1:
        table_9["raw_chem_name"].iloc[j]=" ".join(table_9["raw_chem_name"].iloc[j].split())




#Repeating values declaration 
table_9["data_document_id"]="1671700"
table_9["data_document_filename"]="endocrine_disruptors_table_9.pdf"
table_9["doc_date"]="December 2020"
table_9["raw_category"]=""
table_9["report_funcuse"]=""
table_9["cat_code"]=""
table_9["description_cpcat"]=""
table_9["cpcat_code"]=""
table_9["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
table_9.to_csv("endocrine_disruptors_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


# %% Table 10
table_10_raw = read_pdf(file, pages = '28-29', lattice = True, pandas_options={'header': None})

table_10=pd.concat([table_10_raw[0], table_10_raw[1]])

#extraction and clean up

table_10 = table_10.iloc[:,[0,1]]
table_10 = table_10.dropna(subset=[0])
table_10.reset_index(inplace = True, drop = True)


table_10.columns = ['raw_chem_name', 'raw_cas']
table_10 = table_10.fillna('nan')

for j in range(0,len(table_10)):
    print('row ' + str(j))
    if re.search(r'(\d+)-(\d\d)-(\d)', table_10['raw_cas'].iloc[j]):
        continue
        
    else:
        table_10['raw_cas'].iloc[j] = 'nan'

column_list = table_10['raw_chem_name'].to_list()

for index, i in enumerate(column_list):
    if 'Herpes' in i:
        i_start = index
        break

for index, i in enumerate(column_list):
    if 'Prostate' in i:
        i_end = index
        break
    
table_10 = table_10.drop(table_10.index[i_start:i_end])
table_10.reset_index(inplace = True, drop = True)
table_10 = table_10.drop(table_10.index[16:]) 


searchfor = ['ubstance name', 'rostate']
table_10 = table_10[~table_10.raw_chem_name.str.contains('|'.join(searchfor))]

table_10 = table_10.replace('nan', np.nan)
table_10.fillna(method='ffill', inplace=True)
table_10 = table_10.groupby('raw_cas', as_index=False)['raw_chem_name'].apply(' '.join)
table_10 = table_10.iloc[:,[1,0]]





clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_10)):
    table_10["raw_chem_name"].iloc[j]=str(table_10["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_10["raw_chem_name"].iloc[j]=clean(str(table_10["raw_chem_name"].iloc[j]))
    if len(table_10["raw_chem_name"].iloc[j].split())>1:
        table_10["raw_chem_name"].iloc[j]=" ".join(table_10["raw_chem_name"].iloc[j].split())




#Repeating values declaration 
table_10["data_document_id"]="1671701"
table_10["data_document_filename"]="endocrine_disruptors_table_10.pdf"
table_10["doc_date"]="December 2020"
table_10["raw_category"]=""
table_10["report_funcuse"]=""
table_10["cat_code"]=""
table_10["description_cpcat"]=""
table_10["cpcat_code"]=""
table_10["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
table_10.to_csv("endocrine_disruptors_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


# %% Table 24
table_24_raw = read_pdf(file, pages = '59', lattice = True, pandas_options={'header': None})


#extraction and clean up

table_24=table_24_raw[0]
table_24 = table_24.iloc[0,2:]

table_24 = table_24.to_frame().reset_index(drop = True)
table_24.columns = ['raw_chem_name']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_24)):
    table_24["raw_chem_name"].iloc[j]=str(table_24["raw_chem_name"].iloc[j]).strip().lower()
    table_24["raw_chem_name"].iloc[j]=clean(str(table_24["raw_chem_name"].iloc[j]))
    if len(table_24["raw_chem_name"].iloc[j].split())>1:
        table_24["raw_chem_name"].iloc[j]=" ".join(table_24["raw_chem_name"].iloc[j].split())




#Repeating values declaration 
table_24["data_document_id"]="1671702"
table_24["data_document_filename"]="endocrine_disruptors_table_24.pdf"
table_24["doc_date"]="December 2020"
table_24["raw_cas"]=""
table_24["raw_category"]=""
table_24["report_funcuse"]=""
table_24["cat_code"]=""
table_24["description_cpcat"]=""
table_24["cpcat_code"]=""
table_24["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
table_24.to_csv("endocrine_disruptors_24.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

# %% Table 26
table_26_raw = read_pdf(file, pages = '61', lattice = True, pandas_options={'header': None})


#extraction and clean up

table_26=table_26_raw[1]
table_26 = table_26.iloc[0,2:]

table_26 = table_26.to_frame().reset_index(drop = True)
table_26.columns = ['raw_chem_name']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_26)):
    table_26["raw_chem_name"].iloc[j]=str(table_26["raw_chem_name"].iloc[j]).strip().lower()
    table_26["raw_chem_name"].iloc[j]=clean(str(table_26["raw_chem_name"].iloc[j]))
    if len(table_26["raw_chem_name"].iloc[j].split())>1:
        table_26["raw_chem_name"].iloc[j]=" ".join(table_26["raw_chem_name"].iloc[j].split())




#Repeating values declaration
table_26["data_document_id"]="1671703"
table_26["data_document_filename"]="endocrine_disruptors_table_26.pdf"
table_26["doc_date"]="December 2020"
table_26["raw_cas"]=""
table_26["raw_category"]=""
table_26["report_funcuse"]=""
table_26["cat_code"]=""
table_26["description_cpcat"]=""
table_26["cpcat_code"]=""
table_26["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
table_26.to_csv("endocrine_disruptors_26.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



# %% Table 27
table_27_raw = read_pdf(file, pages = '62', lattice = True, pandas_options={'header': None})


#extraction and clean up

table_27=table_27_raw[0]
table_27 = table_27.iloc[0,2:]

table_27 = table_27.to_frame().reset_index(drop = True)
table_27.columns = ['raw_chem_name']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_27)):
    table_27["raw_chem_name"].iloc[j]=str(table_27["raw_chem_name"].iloc[j]).strip().lower()
    table_27["raw_chem_name"].iloc[j]=clean(str(table_27["raw_chem_name"].iloc[j]))
    if len(table_27["raw_chem_name"].iloc[j].split())>1:
        table_27["raw_chem_name"].iloc[j]=" ".join(table_27["raw_chem_name"].iloc[j].split())




#Repeating values declaration 
table_27["data_document_id"]="1671704"
table_27["data_document_filename"]="endocrine_disruptors_table_27.pdf"
table_27["doc_date"]="December 2020"
table_27["raw_cas"]=""
table_27["raw_category"]=""
table_27["report_funcuse"]=""
table_27["cat_code"]=""
table_27["description_cpcat"]=""
table_27["cpcat_code"]=""
table_27["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
table_27.to_csv("endocrine_disruptors_27.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



# %% CONCAT ALL csv's TOGETHER
# %%% get files
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS - Endocrine Disruptors\csvs')
path = os.getcwd()
files = os.path.join(path, "endocrine_disruptors_*.csv")

files = glob.glob(files)


# %%% joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv("endocrine_disruptors_ext.csv", index = False)

