



"""
@author: CLUTZ01
"""
# %% imports
import os, string, csv, re
import camelot
import pandas as pd
import glob
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from pikepdf import Pdf
from tqdm import tqdm
import unicodedata



# %%
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
        file_path = os.path.abspath(__file__)
        print(file_path)        
    return


# %%

import pyperclip

# pyperclip.copy('text to be copied')
text = pyperclip.paste()
# %%
text_prep = text.split('\n')
# %%
for i,t in enumerate(text_prep):
    if 'max' in str(t) and not re.search(r'^max', str(t)):
        new = t.split(' max', 1)[0]
        print(new)
    elif re.search(r'^max|^[\.]', str(t)):
        continue
    else:
        print(t)


# %%

for i,t in enumerate(text_prep):
    if re.search(r'^\s{0,1}[a-z]{1}\)', str(t)):
        print(t.split(')', 1)[-1])

# %%

for i,t in enumerate(text_prep):
    if re.search(r'^\s{0,1}[0-9]\.', str(t)):
        print(str(t.split('.', 1)[-1].strip()) + "*")

# %%
[print(x) for x in text_prep]
    

# %%
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Manual Extractions\BFR reccomendations\multi_doc_pdfs\XLIV-Artificial-Sausage-Casings')
files = glob.glob('*.xlsx')

# %%
data = pd.read_excel(files[0])
print(data)

# %%
print(list(data))
categories = data['divination'].loc[:].drop_duplicates().to_list()
print(categories)

# %% subset data

sausage_i = data[data['divination'].str.contains(str(categories[0]))].iloc[:,[0,1]]
sausage_ii = data[data['divination'].str.contains(str(categories[1]))].iloc[:,[0,1]]
sausage_iii = data[data['divination'].str.contains(str(categories[2]))].iloc[:,[0,1]]
sausage_iv = data[data['divination'].str.contains(str(categories[3]))].iloc[:,[0,1]]
sausage_v = data[data['divination'].str.contains(str(categories[4]))].iloc[:,[0,1]]
sausage_vi = data[data['divination'].str.contains(str(categories[5]))].iloc[:,[0,1]]



dfs = {'sausage_i': sausage_i, 'sausage_ii' : sausage_ii, 'sausage_iii': sausage_iii, 'sausage_iv' : sausage_iv, 'sausage_v': sausage_v, 'sausage_vi' : sausage_vi }
for k,v in dfs.items():
    print(k)

# %% get date

pdf = glob.glob('*.pdf')
print(pdf)
pdfToText(pdf)


ifile = open(pdf[0].replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()
date = re.findall(r'\d{1,2}\.\d{1,2}\.\d{1,4}', text)[0]
print(date)

# %%



dfs_final = []
for k,df in dfs.items():

    # print(k)
    # print(df)
    for j in range(0, len(df)):
        clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
        df["raw_chem_name"].iloc[j]=str(df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
        df["raw_chem_name"].iloc[j]=clean(str(df["raw_chem_name"].iloc[j]))
        if len(df["raw_chem_name"].iloc[j].split())>1:
            df["raw_chem_name"].iloc[j]=" ".join(df["raw_chem_name"].iloc[j].split())
    
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Manual Extractions\BFR reccomendations\multi_doc_pdfs\XLIV-Artificial-Sausage-Casings\doc_records.csv"))
    for row in template:
        print(str(k).replace('sausage', ''))
        print(row[7])
        if str(k).replace('sausage','') in row[6].lower():
            id = row[0]
            filename = row[6]
        # else:
        #     print('issue with filename')
        #     # print(id)

    
    df["data_document_id"]=id
    df["data_document_filename"]=filename
    df["doc_date"]=date
    df["raw_cas"]=""
    df["component"]=""
    df["raw_category"]=""
    df["cat_code"]=""
    df["description_cpcat"]=""
    df["cpcat_code"]=""
    df["cpcat_sourcetype"]="ACToR Assays and Lists"

    # print("df" + str(k))
    # print(df)
    dfs_final.append(df)
# %%
print(dfs_final)
[print() for x in dfs_final]

sausage_ext = pd.concat(dfs_final)
print(len(sausage_ext))
# first = dfs_final[0]
# %%
sausage_ext.to_csv('sausage_ext.csv', columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)