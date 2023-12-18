# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:31:06 2023

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



# %%%
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

    os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Eastman/pdfs')
    remainder = glob('*.pdf')
    
    
    pdfToText(remainder)

# %%% has numbers def

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


# os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_Textile_face_masks')
# pdfDocument = pdf.Document("report.pdf")
# #Initialize TableAbsorber object
# tableAbsorber =  pdf.text.TableAbsorber()

#%% report location
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\report.pdf"
txt_file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\report.txt"

# %% table 2 (manual)
#manually extracted



# %% Table 6

table_6_raw = read_pdf(file, pages = "31-33", lattice = True)




table_6_ls = []
for i,j in enumerate(table_6_raw):
    new_j = j.iloc[:,[0,1]]
    table_6_ls.append(new_j)


table_6 = pd.concat(table_6_ls)

table_6 = table_6.dropna(how = "all", axis = 0)
table_6.columns = ['raw_chem_name', 'raw_cas']
table_6 = table_6.fillna('nan')


filter = table_6['raw_chem_name'].str.contains('H\d\d\d')
table_6 = table_6[~filter]

filter2 = table_6['raw_cas'].str.contains('\d+-\d\d-\d')
table_6 = table_6[filter2]
table_6 = table_6.replace('nan', np.NaN)


table_6.fillna(method='ffill', inplace=True)
table_6.reset_index(inplace = True, drop = True)


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i,j in enumerate(table_6['raw_chem_name']):
    print(str(type(j)))
    print(cleanLine(j))


for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower()
    table_6["raw_chem_name"].iloc[j]=cleanLine(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())
        
#cleaning data
        
        

#Repeating values declaration 
table_6["data_document_id"]="1687054"
table_6["data_document_filename"]="textile_face_masks_table_6.pdf"
table_6["doc_date"]="November 2021"
table_6["component"]=""
table_6["raw_category"]=""
table_6["report_funcuse"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
table_6.to_csv("textile_face_masks_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Table 9 (manual)
#only one chemical to extract, done manually


# %% Table 10 (manual)
#extracted manually

# %% Table 11

raw_table_11 = read_pdf(file, pages = '47-49', lattice = True, pandas_options={'header': None})


table_11_ls = []
for i,j in enumerate(raw_table_11):
    if 'ubstance' in j.iat[0,0]:
        continue
    
    else:
        new_j = j.iloc[:,[0,1,2]]
        table_11_ls.append(new_j)

table_11 = pd.concat(table_11_ls)
table_11 = table_11.dropna(how = 'all', axis = 0)


for i,j in enumerate(table_11[0]):
    if re.search(r'\d+-\d\d-\d', str(j)):
        continue
    else:
        table_11[0].iloc[i] = np.NaN
        

#shift over nan rows
table_11 = table_11.dropna(how = 'all', axis = 0)        
table_11[[1,2]] = table_11[[1,2]].fillna('nan')
table_11 = pd.DataFrame(table_11.apply(lambda x : [x[x.notna().cumsum()>0].tolist()],1).str[0].tolist(),
                   index=table_11.index,
                   columns=table_11.columns)

table_11 = table_11.replace('nan', np.NaN)
table_11 = table_11.iloc[:,[0,1]]
table_11.columns = ['raw_cas','raw_chem_name']
table_11 = table_11[~table_11['raw_chem_name'].str.contains("ubstance|possibly")]

for i,j in enumerate(table_11['raw_cas']):
    if ')' in str(j):
        edit = str(j).split(")", 1)[-1].strip()
        table_11['raw_cas'].iloc[i] = edit
    

table_11['number'] = np.NaN
count = 1
for i,j in enumerate(table_11['raw_cas']):
    if 'nan' in str(j):
        continue
    else:
        table_11['number'].iloc[i] = count
        count += 1
        
      
        
table_11.fillna(method='ffill', inplace=True)
table_11 = table_11.groupby(['raw_cas', 'number'], as_index=False)['raw_chem_name'].apply(' '.join)
table_11 = table_11.sort_values(by=['number'])
table_11 = table_11.loc[:,['raw_chem_name', 'raw_cas']]
table_11.reset_index(inplace = True, drop = True)


for i,j in enumerate(table_11['raw_chem_name']):
    new_j = re.sub(r"[abcd]\)", "", str(j))
    new_j = new_j.replace('likely','')
    table_11['raw_chem_name'].iloc[i] = new_j.strip()
    




for j in range(0, len(table_11)):
    table_11["raw_chem_name"].iloc[j]=str(table_11["raw_chem_name"].iloc[j]).strip().lower()
    table_11["raw_chem_name"].iloc[j]=cleanLine(str(table_11["raw_chem_name"].iloc[j]))
    if len(table_11["raw_chem_name"].iloc[j].split())>1:
        table_11["raw_chem_name"].iloc[j]=" ".join(table_11["raw_chem_name"].iloc[j].split())
        


#Repeating values declaration 

table_11["data_document_id"]="1687057"
table_11["data_document_filename"]="textile_face_masks_table_11.pdf"
table_11["doc_date"]="November 2021"
table_11["component"]=""
table_11["raw_category"]=""
table_11["report_funcuse"]=""
table_11["cat_code"]=""
table_11["description_cpcat"]=""
table_11["cpcat_code"]=""
table_11["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
table_11.to_csv("textile_face_masks_table_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 13 (manual)
# ewxtracting manually

#the only chemicla is formaldehyde

# %% Table 14 (manual)
# ewxtracting manually

#the only chemicla is BPA


# %% Table 15



raw_table_15 = read_pdf(file, pages = '56-57', lattice = True, pandas_options={'header': None})


table_15_ls = []
for i,j in enumerate(raw_table_15):
    if 'abric' in j.iat[0,0]:
        continue
    
    else:
        new_j = j.iloc[:,[0,1,2]]
        table_15_ls.append(new_j)

table_15 = pd.concat(table_15_ls)
table_15 = table_15.dropna(how = 'any', axis = 0)
table_15 = table_15.iloc[:,0:2]

table_15.columns = ['raw_chem_name','extra']

table_15 = table_15[~table_15['raw_chem_name'].str.contains("PFAS")]





for j in range(0, len(table_15)):
    table_15["raw_chem_name"].iloc[j]=str(table_15["raw_chem_name"].iloc[j]).strip().lower()
    table_15["raw_chem_name"].iloc[j]=cleanLine(str(table_15["raw_chem_name"].iloc[j]))
    if len(table_15["raw_chem_name"].iloc[j].split())>1:
        table_15["raw_chem_name"].iloc[j]=" ".join(table_15["raw_chem_name"].iloc[j].split())
        

table_15["data_document_id"]="1687060"
table_15["data_document_filename"]="textile_face_masks_table_15.pdf"
table_15["doc_date"]="November 2021"
table_15["component"]=""
table_15["raw_category"]=""
table_15["raw_cas"]=""
table_15["report_funcuse"]=""
table_15["cat_code"]=""
table_15["description_cpcat"]=""
table_15["cpcat_code"]=""
table_15["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
table_15.to_csv("textile_face_masks_table_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% Table 16 (manual)
# extracting only 6:2 FTOH

# %% Table 17 

raw_table_17 = read_pdf(file, pages = '59', lattice = True, pandas_options={'header': None})

table_17 = raw_table_17[0]
table_17 = table_17.iloc[0,1:5]

#repeat for table 18
table_18 = pd.DataFrame({'raw_chem_name':table_17})

table_17 = pd.DataFrame({'raw_chem_name':table_17})
table_17.reset_index(inplace = True, drop = True)


for j in range(0, len(table_17)):
    table_17["raw_chem_name"].iloc[j]=str(table_17["raw_chem_name"].iloc[j]).strip().lower()
    table_17["raw_chem_name"].iloc[j]=cleanLine(table_17["raw_chem_name"].iloc[j])
    if len(table_17["raw_chem_name"].iloc[j].split())>1:
        table_17["raw_chem_name"].iloc[j]=" ".join(table_17["raw_chem_name"].iloc[j].split())
table_17["raw_chem_name"].iloc[2]

table_17["data_document_id"]="1687050"
table_17["data_document_filename"]="textile_face_masks_table_17.pdf"
table_17["doc_date"]="November 2021"
table_17["component"]=""
table_17["raw_category"]=""
table_17["raw_cas"]=""
table_17["report_funcuse"]=""
table_17["cat_code"]=""
table_17["description_cpcat"]=""
table_17["cpcat_code"]=""
table_17["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
table_17.to_csv("textile_face_masks_table_17.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% Table 18



for j in range(0, len(table_18)):
    table_18["raw_chem_name"].iloc[j]=str(table_18["raw_chem_name"].iloc[j]).strip().lower()
    table_18["raw_chem_name"].iloc[j]=cleanLine(str(table_18["raw_chem_name"].iloc[j]))
    if len(table_18["raw_chem_name"].iloc[j].split())>1:
        table_18["raw_chem_name"].iloc[j]=" ".join(table_18["raw_chem_name"].iloc[j].split())
        

table_18["data_document_id"]="1687051"
table_18["data_document_filename"]="textile_face_masks_table_18.pdf"
table_18["doc_date"]="November 2021"
table_18["component"]=""
table_18["raw_category"]=""
table_18["raw_cas"]=""
table_18["report_funcuse"]=""
table_18["cat_code"]=""
table_18["description_cpcat"]=""
table_18["cpcat_code"]=""
table_18["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
table_18.to_csv("textile_face_masks_table_18.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% Table 19

ifile = open(txt_file.replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)
lines = cleaned.split('\n')

clean_lines = [e for i,e in enumerate(lines) if len(e) != 0]


for i,line in enumerate(clean_lines):
    if '7.2.5.1 method of analysis - isocyanates' in str(line):
        start = i
    elif '7.2.5.2 analysis results - isocyanates' in str(line):
        stop = i
        break

table_19_raw = clean_lines[start:stop]

table_19_ls = []
for i,j in enumerate(table_19_raw):
    if '•' in str(j):
        clean_j = re.sub(r'•', '',str(j)).strip()
        table_19_ls.append(str(clean_j))

table_19 = pd.DataFrame(table_19_ls, columns=['raw_chem_name'])


table_19['raw_cas'] = np.NaN
for i,j in enumerate(table_19['raw_chem_name']):
    split = str(j).split(' - ', 1)
    print(split)
    raw_chem = split[0].strip()
    raw_cas = split[1].replace('cas no.', '').strip()
    table_19['raw_chem_name'].iloc[i] = raw_chem
    table_19['raw_cas'].iloc[i] = raw_cas

for j in range(0, len(table_19)):
    table_19["raw_chem_name"].iloc[j]=str(table_19["raw_chem_name"].iloc[j]).strip().lower()
    table_19["raw_chem_name"].iloc[j]=cleanLine(str(table_19["raw_chem_name"].iloc[j]))
    if len(table_19["raw_chem_name"].iloc[j].split())>1:
        table_19["raw_chem_name"].iloc[j]=" ".join(table_19["raw_chem_name"].iloc[j].split())
        
table_19["data_document_id"]="1687052"
table_19["data_document_filename"]="textile_face_masks_table_19.pdf"
table_19["doc_date"]="November 2021"
table_19["component"]=""
table_19["raw_category"]=""
table_19["report_funcuse"]=""
table_19["cat_code"]=""
table_19["description_cpcat"]=""
table_19["cpcat_code"]=""
table_19["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
table_19.to_csv("textile_face_masks_table_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% Table 20(manual)

#BPA is only chemical 


# %%


# Joining files

path = os.getcwd()
files = os.path.join(path, "textile_face_masks_table_*.csv")

files = glob.glob(files)


# joining files with concat and read_csv
face_masks_df = pd.concat(map(pd.read_csv, files), ignore_index=True)

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DCPS_Textile_face_masks\csvs')
face_masks_df.to_csv("face_mask_ext.csv", index=False)

