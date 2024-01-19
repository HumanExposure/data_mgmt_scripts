# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:07:04 2024

@author: CLUTZ01
"""


# %% imports
import os, string, re
import pandas as pd
import numpy as np
from tabula import read_pdf
from glob import glob
# %% Definitions
# %%%DEFINITION cleaning text
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



# %%renaming files


os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2019")


file_names = pd.read_csv("filenames_2019.csv")
file_names = file_names["filename"].to_list()


data = os.path.abspath("pdfs/")

for i, f in enumerate(os.listdir(data)):
    
    file = file_names[i]
    src = os.path.join(data, f)
    dst = os.path.join(data, file)
    os.rename(src, dst)
    


# %%% DEFINITION pdftotext

def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64' #Path to execfile
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return

    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2019')
    remainder = glob('*.pdf')
    
    
    pdfToText(remainder)
    
    


    

# %% file

file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2019\pdfs\NFLIS-Drug-MYR2019_table1.1.pdf"
files = [file]
pdfToText(files)




ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)
lines = cleaned.split('\n')
clean_lines = [x for x in lines if len(x) > 0]
# %% Table 1.1
table_1_1_raw = read_pdf(file, pages = '8', pandas_options={'header': None})
table_1_1 = table_1_1_raw[0].iloc[1:26,0:1]
table_1_1.reset_index(drop = True, inplace = True)
table_1_1.columns = ['raw_chem_name']


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_1)):
    table_1_1["raw_chem_name"].iloc[j]=str(table_1_1["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_1_1["raw_chem_name"].iloc[j]=clean(str(table_1_1["raw_chem_name"].iloc[j]))
    if len(table_1_1["raw_chem_name"].iloc[j].split())>1:
        table_1_1["raw_chem_name"].iloc[j]=" ".join(table_1_1["raw_chem_name"].iloc[j].split())
        

#Repeating values declaration 
table_1_1["data_document_id"]="1690395"
table_1_1["data_document_filename"]="NFLIS-Drug-MYR2021_table1.1.pdf"
table_1_1["doc_date"]="April 2022"
table_1_1["raw_cas"]=""
table_1_1["raw_category"]=""
table_1_1["component"]=""
table_1_1["report_funcuse"]=""
table_1_1["cat_code"]=""
table_1_1["description_cpcat"]=""
table_1_1["cpcat_code"]=""
table_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_1_1.to_csv("NFLIS-Drug-MYR2021_table1.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 1.2


start_found = False
for i,j in enumerate(clean_lines):
    if 'national case estimates' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'top 25 total' in str(j):
        stop = i
        break
        

table_1_2 = pd.DataFrame(clean_lines[start:stop])
table_1_2 = table_1_2.iloc[5:,:]
table_1_2.reset_index(drop = True, inplace = True)

table_1_2.columns = ['raw_chem_name']



for i,j in enumerate(table_1_2['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3},', str(j), maxsplit = 1)
    table_1_2['raw_chem_name'].iloc[i] = new_string[0]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_2)):
    table_1_2["raw_chem_name"].iloc[j]=str(table_1_2["raw_chem_name"].iloc[j]).strip().lower()
    table_1_2["raw_chem_name"].iloc[j]=clean(str(table_1_2["raw_chem_name"].iloc[j]))
    if len(table_1_2["raw_chem_name"].iloc[j].split())>1:
        table_1_2["raw_chem_name"].iloc[j]=" ".join(table_1_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_1_2["data_document_id"]="1690396"
table_1_2["data_document_filename"]="NFLIS-Drug-MYR2021_table1.2.pdf"
table_1_2["doc_date"]="April 2022"
table_1_2["raw_cas"]=""
table_1_2["raw_category"]=""
table_1_2["component"]=""
table_1_2["report_funcuse"]=""
table_1_2["cat_code"]=""
table_1_2["description_cpcat"]=""
table_1_2["cpcat_code"]=""
table_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_1_2.to_csv("NFLIS-Drug-MYR2021_table1.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.1


start_found = False
for i,j in enumerate(clean_lines):
    if 'table 2.1 narcotic analgesics' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'other narcotic analgesics' in str(j):
        stop = i
        break
        

table_2_1 = pd.DataFrame(clean_lines[start:stop])
table_2_1 = table_2_1.iloc[6:,:]
table_2_1.reset_index(drop = True, inplace = True)

table_2_1.columns = ['raw_chem_name']

for i,j in enumerate(table_2_1['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3}', str(j), maxsplit = 1)
    table_2_1['raw_chem_name'].iloc[i] = new_string[0]





clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).replace('²', '').strip().lower()
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if len(table_2_1["raw_chem_name"].iloc[j].split())>1:
        table_2_1["raw_chem_name"].iloc[j]=" ".join(table_2_1["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_1["data_document_id"]="1690397"
table_2_1["data_document_filename"]="NFLIS-Drug-MYR2021_table2.1.pdf"
table_2_1["doc_date"]="April 2022"
table_2_1["raw_cas"]=""
table_2_1["raw_category"]=""
table_2_1["report_funcuse"]=""
table_2_1["cat_code"]=""
table_2_1["component"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_2_1.to_csv("NFLIS-Drug-MYR2021_table2.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.2

start_found = False
for i,j in enumerate(clean_lines):
    if 'table 2.2' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'other tranquilizers' in str(j):
        stop = i
        break

table_2_2 = pd.DataFrame(clean_lines[start:stop])
table_2_2 = table_2_2.iloc[5:,:]
table_2_2.reset_index(drop = True, inplace = True)

table_2_2.columns = ['raw_chem_name']

for i,j in enumerate(table_2_2['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3}', str(j), maxsplit = 1)
    table_2_2['raw_chem_name'].iloc[i] = new_string[0]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_2)):
    table_2_2["raw_chem_name"].iloc[j]=str(table_2_2["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_2["raw_chem_name"].iloc[j]=clean(str(table_2_2["raw_chem_name"].iloc[j]))
    if len(table_2_2["raw_chem_name"].iloc[j].split())>1:
        table_2_2["raw_chem_name"].iloc[j]=" ".join(table_2_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_2["data_document_id"]="1690398"
table_2_2["data_document_filename"]="NFLIS-Drug-MYR2021_table2.2.pdf"
table_2_2["doc_date"]="April 2022"
table_2_2["raw_cas"]=""
table_2_2["raw_category"]=""
table_2_2["report_funcuse"]=""
table_2_2["component"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_2_2.to_csv("NFLIS-Drug-MYR2021_table2.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)
    
# %% Table 2.3

start_found = False
for i,j in enumerate(clean_lines):
    if 'table 2.3' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'anabolic steroids' in str(j):
        stop = i
        break
    
    
table_2_3 = pd.DataFrame(clean_lines[start:stop])
table_2_3 = table_2_3.iloc[4:,:]
table_2_3.reset_index(drop = True, inplace = True)




table_2_3.columns = ['raw_chem_name']

for i,t in enumerate(table_2_3['raw_chem_name']):
    if re.search(r'[a-z]', str(t)):
        split_txt = re.split(r'\d', str(t), maxsplit=1)
        table_2_3['raw_chem_name'].iloc[i] = split_txt[0]
    else:
        table_2_3['raw_chem_name'].iloc[i] = np.NaN
        
table_2_3 = table_2_3.dropna(how = 'all', axis = 0)
table_2_3.reset_index(drop = True, inplace = True)        
        

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).strip().lower()
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))
    if len(table_2_3["raw_chem_name"].iloc[j].split())>1:
        table_2_3["raw_chem_name"].iloc[j]=" ".join(table_2_3["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_3["data_document_id"]="1690399"
table_2_3["data_document_filename"]="NFLIS-Drug-MYR2021_table2.3.pdf"
table_2_3["doc_date"]="April 2022"
table_2_3["raw_cas"]=""
table_2_3["raw_category"]=""
table_2_3["component"]=""
table_2_3["report_funcuse"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_2_3.to_csv("NFLIS-Drug-MYR2021_table2.3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Table 2.4



start_found = False
for i,j in enumerate(clean_lines):
    if 'table 2.4' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'other phenethylamines' in str(j):
        stop = i
        break
    
    
table_2_4 = pd.DataFrame(clean_lines[start:stop])
table_2_4 = table_2_4.iloc[4:,:]
table_2_4.reset_index(drop = True, inplace = True)




table_2_4.columns = ['raw_chem_name']


for i,j in enumerate(table_2_4['raw_chem_name']):
    new_string = str(j).strip()
    new_string = re.split(r'\s\d{1,3}', new_string, maxsplit = 1)
    table_2_4['raw_chem_name'].iloc[i] = new_string[0]

        
table_2_4 = table_2_4.dropna(how = 'all', axis = 0)
table_2_4.reset_index(drop = True, inplace = True)      


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower()
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_4["data_document_id"]="1690400"
table_2_4["data_document_filename"]="NFLIS-Drug-MYR2021_table2.4.pdf"
table_2_4["doc_date"]="April 2022"
table_2_4["raw_cas"]=""
table_2_4["component"]=""
table_2_4["raw_category"]=""
table_2_4["report_funcuse"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_2_4.to_csv("NFLIS-Drug-MYR2021_table2.4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.5



start_found = False
for i,j in enumerate(clean_lines):
    if 'table 2.5' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'other synthetic cannabinoids' in str(j):
        stop = i
        break
    
    
table_2_5 = pd.DataFrame(clean_lines[start:stop])
table_2_5 = table_2_5.iloc[6:,:]
table_2_5.reset_index(drop = True, inplace = True)




table_2_5.columns = ['raw_chem_name']


for i,j in enumerate(table_2_5['raw_chem_name']):
    new_string = str(j).strip()
    new_string = re.split(r'\s\d{1,3}', new_string, maxsplit = 1)
    table_2_5['raw_chem_name'].iloc[i] = new_string[0]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[j]=str(table_2_5["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_5["raw_chem_name"].iloc[j]=clean(str(table_2_5["raw_chem_name"].iloc[j]))
    if len(table_2_5["raw_chem_name"].iloc[j].split())>1:
        table_2_5["raw_chem_name"].iloc[j]=" ".join(table_2_5["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_5["data_document_id"]="1690401"
table_2_5["data_document_filename"]="NFLIS-Drug-MYR2021_table2.5.pdf"
table_2_5["doc_date"]="April 2022"
table_2_5["raw_cas"]=""
table_2_5["raw_category"]=""
table_2_5["component"]=""
table_2_5["report_funcuse"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
table_2_5.to_csv("NFLIS-Drug-MYR2021_table2.5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Joining files
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021\csvs")
path = os.getcwd()
files = os.path.join(path, "*.csv")

files = glob(files)


# joining files with concat and read_csv
extract_df = pd.concat(map(pd.read_csv, files), ignore_index=True)

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2021")
extract_df.to_csv("nflis_midyear_report_2021_ext.csv", index=False)


