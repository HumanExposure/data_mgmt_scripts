
"""
Created on Wed Apr 24 8:05:35 2023
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
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Manual Extractions\BFR reccomendations\XXXVI-1-Cooking-Papers')
files = glob.glob('*.xlsx')


# %%
data = pd.read_excel(files[0])

# %%
print(list(data))
categories = data['divination'].loc[:].drop_duplicates().to_list()
print(categories)
# %% subset data


raw_materials = data[data['divination'].str.contains(str(categories[0]))].iloc[:,[0,1]]
production_aids = data[data['divination'].str.contains(str(categories[1]))].iloc[:,[0,1]]
special_raw = data[data['divination'].str.contains(str(categories[2]))].iloc[:,[0,1]]

dfs = {'raw_materials': raw_materials, 'production_aids' : production_aids, 'special_raw': special_raw}
for k,v in dfs.items():
    print(k)
    print(v)

# %% get date

pdf = glob.glob('*.pdf')
print(pdf)
pdfToText(pdf)


ifile = open(pdf[0].replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()
date = re.findall(r'\d{1,2}\.\d{1,2}\.\d{1,4}', text)[0]


# %%



dfs_final = []
for k,df in dfs.items():
    has_component = False
    for x in list(df):
        if 'component' in str(x):
            has_component = True
            break


    print(list(df))
    print(k)
    for j in range(0, len(df)):
        clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
        df["raw_chem_name"].iloc[j]=str(df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
        df["raw_chem_name"].iloc[j]=clean(str(df["raw_chem_name"].iloc[j]))
        if len(df["raw_chem_name"].iloc[j].split())>1:
            df["raw_chem_name"].iloc[j]=" ".join(df["raw_chem_name"].iloc[j].split())
    
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Manual Extractions\BFR reccomendations\XV. Silicones\doc_records.csv"))
    for row in template:
        print(str(k))
        if str(k) in row[7].lower():
            id = row[0]
            filename = row[6]
            print(id)

    if has_component == False:
        df["component"]=""



    df["data_document_id"]=id
    df["data_document_filename"]=filename
    df["doc_date"]=date
    df["raw_cas"]=""
    df["raw_category"]=""
    df["cat_code"]=""
    df["description_cpcat"]=""
    df["cpcat_code"]=""
    df["cpcat_sourcetype"]="ACToR Assays and Lists"

    
    print(df)
    dfs_final.append(df)
# %%
print(dfs_final)
[print() for x in dfs_final]

silicones_ext = pd.concat(dfs_final)
print(len(silicones_ext))
# first = dfs_final[0]
