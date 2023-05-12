# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:53:51 2023

@author: CLUTZ01
"""

# %% imports and def set up
# %%%
from tabula import read_pdf
import pandas as pd
import string
import os
import glob
import re
import numpy as np



# %%%
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('–','-').replace('≤','<=').replace('®', '').replace('â', '').replace('€“', '-')
    # cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)


# %%%

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

# %%% file set up
execfile = "pdftotext.exe"
execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64'
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime')


file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\slime_toys_pdf.pdf'
pdf = '"'+file+'"'
cmd = os.path.join(execpath,execfile)
cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
os.system(cmd)

file_txt = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\slime_toys_pdf.txt"
ifile = open(file_txt.replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)


# %% Table 1


# %%% extraction and clean up
table_1_raw=read_pdf(file, pages='19')
table_1=table_1_raw[0]
table_1 = table_1.dropna(subset=['Substance name'])
table_1 = table_1.replace('als',np.nan, regex=True)
table_1 = table_1[['Substance name', 'CAS no.']]
table_1.reset_index(inplace=True, drop=True)

#fill, groupby, reorder, and rename
table_1.fillna(method='ffill', inplace=True)
table_1 = table_1.iloc[0:13]
table_1 = table_1.groupby(['CAS no.'], as_index=False)['Substance name'].apply(' '.join)
table_1 = table_1.iloc[:,[1,0]]
table_1 = table_1.rename(columns={'Substance name': 'raw_chem_name', 'CAS no.': 'raw_cas'})

# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1)):
    table_1["raw_chem_name"].iloc[j]=str(table_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    table_1["raw_chem_name"].iloc[j]=clean(str(table_1["raw_chem_name"].iloc[j]))
    if len(table_1["raw_chem_name"].iloc[j].split())>1:
        table_1["raw_chem_name"].iloc[j]=" ".join(table_1["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration
table_1["data_document_id"]="1668055"
table_1["data_document_filename"]="slime_toys_a.pdf"
table_1["doc_date"]="June 2020"
table_1["raw_category"]=""
table_1["report_funcuse"]=""
table_1["cat_code"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_1.to_csv("slime_toys_table_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



# %%Table 2
#%%% Raw extraction
table_2_raw=read_pdf(file, pages="20", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2=table_2_raw[0]
table_2 = table_2.iloc[1:len(table_2),[1,2]]

table_2.columns = ['raw_chem_name', 'raw_cas']
table_2 = table_2.dropna(subset=['raw_chem_name'])
table_2.reset_index(inplace=True, drop=True)


# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))
    if len(table_2["raw_chem_name"].iloc[j].split())>1:
        table_2["raw_chem_name"].iloc[j]=" ".join(table_2["raw_chem_name"].iloc[j].split())


# %%% repeated values declaration and csv creation
table_2["data_document_id"]="1668056"
table_2["data_document_filename"]="slime_toys_b.pdf"
table_2["doc_date"]="June 2020"
table_2["raw_category"]=""
table_2["cat_code"]=""
table_2["report_funcuse"] = ""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_2.to_csv("slime_toys_table_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



# %% TABLE 3 & 4
# %%% RAW EXTRACTION
table_3_raw=read_pdf(file, pages="25-27", lattice=True, multiple_tables=True, pandas_options={'header': None})
# %%% cleaning
#select needed elements and create df
table_3=pd.concat([table_3_raw[0], table_3_raw[1], table_3_raw[2]])
table_3.reset_index(inplace=True, drop=True)

# clean up
table_3 = table_3.iloc[:,[0,1]]
table_3.columns = ['raw_chem_name', 'raw_cas']
table_3 = table_3.dropna(subset=['raw_chem_name'])
table_3 = table_3.drop(table_3[table_3["raw_chem_name"].str.contains("ubstance|ame")].index)
table_3.reset_index(inplace=True, drop=True)
table_3['raw_cas'] = table_3['raw_cas'].replace('whose contents', np.NaN)



table_3 = table_3.iloc[0:17]
table_3.fillna(method='ffill', inplace=True)

for j in range(0,len(table_3)):
    if len(table_3['raw_cas'].iloc[j]) <= 1:
        table_3['raw_cas'].iloc[j] = table_3['raw_cas'].iloc[j].replace('-', table_3['raw_chem_name'].iloc[j])
        table_3['raw_cas'].iloc[j+1] = table_3['raw_cas'].iloc[j].replace('-', table_3['raw_chem_name'].iloc[j])

#fill, groupby, reorder, and rename
table_3 = table_3.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(' '.join)
table_3 = table_3.iloc[:,[1,0]]

for j in range(0,len(table_3)):
    if "P" in table_3['raw_cas'].iloc[j]:
        table_3['raw_cas'].iloc[j] = "-"
        
table_3['report_funcuse'] = 'Preservatives'


# clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_3["raw_chem_name"].iloc[j]=clean(str(table_3["raw_chem_name"].iloc[j]))
    if len(table_3["raw_chem_name"].iloc[j].split())>1:
        table_3["raw_chem_name"].iloc[j]=" ".join(table_3["raw_chem_name"].iloc[j].split())
# %%% Repeating values declaration and csv creation
table_3["data_document_id"]="1668057"
table_3["data_document_filename"]="slime_toys_c.pdf"
table_3["doc_date"]="June 2020"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_3.to_csv("slime_toys_table_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

# %% TABLE 5
# %%% RAW EXTRACTION
table_5_raw=read_pdf(file, pages="27-28", lattice=True, multiple_tables=True, pandas_options={'header': None})
# %%% cleaning
#select needed elements and create df
table_5=pd.concat([table_5_raw[1], table_5_raw[2]])
table_5.reset_index(inplace=True, drop=True)
table_5 = table_5.iloc[:,[0,1]]

table_5.columns = ['raw_chem_name', 'raw_cas']
table_5 = table_5.dropna(subset=['raw_chem_name'])

table_5 = table_5.drop(table_5[table_5["raw_chem_name"].str.contains("ubstance|ame")].index)
table_5.reset_index(inplace=True, drop=True)


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]=" ".join(table_5["raw_chem_name"].iloc[j].split())
# %%% Repeating values declaration and csv creation
table_5["data_document_id"]="1668058"
table_5["data_document_filename"]="slime_toys_d.pdf"
table_5["doc_date"]="June 2020"
table_5["raw_category"]=""
table_5["report_funcuse"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_5.to_csv("slime_toys_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


# %% TABLE 6
# %%% RAW EXTRACTION
table_6_raw=read_pdf(file, pages="28-29", lattice=True, multiple_tables=True, pandas_options={'header': None})
# %%% cleaning
#select needed elements and create df
table_6=pd.concat([table_6_raw[1], table_6_raw[2]])
table_6.reset_index(inplace=True, drop=True)
table_6 = table_6.iloc[:,[0,1]]

table_6.columns = ['raw_chem_name', 'raw_cas']
table_6 = table_6.dropna(subset=['raw_chem_name'])

table_6 = table_6.drop(table_6[table_6["raw_chem_name"].str.contains("ubstance|ame")].index)
table_6['raw_cas'] = table_6['raw_cas'].replace('ously', np.NaN)
table_6.reset_index(inplace=True, drop=True)

for j in range(0,len(table_6)):
    if ',' in str(table_6['raw_cas'].iloc[j]):
        x = table_6['raw_cas'].iloc[j]
        y = table_6['raw_cas'].iloc[j+1]
        table_6['raw_cas'].iloc[j] = (x+" "+y)
        table_6['raw_cas'].iloc[j+1] = np.nan
    else:
        continue

# table_6 = table_6.iloc[0:17]
table_6.fillna(method='ffill', inplace=True)

table_6_backup = table_6
#fill, groupby, reorder, and rename
table_6 = table_6.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
table_6 = table_6.iloc[:,[1,0]] 

# %%% editing chem names


for j in range(0,len(table_6)):
    if 'ben-' in str(table_6['raw_chem_name'].iloc[j]):
        table_6['raw_chem_name'].iloc[j] = str(table_6['raw_chem_name'].iloc[j]).replace('ben-', 'ben')
        continue
    elif has_numbers(str(table_6['raw_chem_name'].iloc[j])):
        print(j)
        continue    
    else:
        table_6['raw_chem_name'].iloc[j] = str(table_6['raw_chem_name'].iloc[j]).replace('N-', 'N--').replace('-', '')

# %%%
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("*","")
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())
        
# %%% Repeating values declaration and csv creation
table_6["data_document_id"]="1668059"
table_6["data_document_filename"]="slime_toys_e.pdf"
table_6["doc_date"]="June 2020"
table_6["raw_category"]=""
table_6["report_funcuse"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_6.to_csv("slime_toys_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



# %% TABLE 7
# %%% RAW EXTRACTION
table_7_raw=read_pdf(file, pages="29", stream=True, multiple_tables=True, pandas_options={'header': None})
# %%% cleaning
#select needed elements and create df
table_7 = table_7_raw[1]
table_7.reset_index(inplace=True, drop=True)


pd.DataFrame([])


# %%% clean up slime toy 1

slime_toy_1 = table_7.iloc[:,[0,1]]
slime_toy_1 = slime_toy_1.dropna(how='all')
slime_toy_1.fillna(method='ffill', inplace=True)
slime_toy_1.columns = ['report_funcuse', 'raw_chem_name']
slime_toy_1.iat[3, 1] = 'Glycerine*'


slime_toy_1 = slime_toy_1.groupby(['raw_chem_name'], as_index=False)['report_funcuse'].apply(' '.join)
slime_toy_1['report_funcuse'] = slime_toy_1['report_funcuse'].str.replace('- ', '')
slime_toy_1.reset_index(inplace = True, drop = True)
slime_toy_1.iat[4, 0] = 'Glycerine'

slime_toy_1 = slime_toy_1.drop(slime_toy_1[slime_toy_1["report_funcuse"].str.contains("ubstance|ame")].index)
slime_toy_1.reset_index(inplace = True, drop = True)
slime_toy_1['component'] = 'Slime Toy 1'

# %%% clean up slime toy 2

slime_toy_2 = table_7.iloc[:,[0,2]]
slime_toy_2 = slime_toy_2.dropna(how='all')
slime_toy_2.fillna(method='ffill', inplace=True)
slime_toy_2.columns = ['report_funcuse', 'raw_chem_name']
slime_toy_2 = slime_toy_2.groupby(['raw_chem_name'], as_index=False)['report_funcuse'].apply(' '.join)
slime_toy_2['report_funcuse'] = slime_toy_2['report_funcuse'].str.replace('- ', '')
slime_toy_2 = slime_toy_2.drop(slime_toy_2[slime_toy_2["report_funcuse"].str.contains("ubstance|ame")].index)
slime_toy_2.reset_index(inplace=True, drop=True)

slime_toy_2['component'] = 'Slime Toy 2'

# %%% clean up slime toy 3 
slime_toy_3 = table_7.iloc[:,[0,3]]
toy_3_clean_up = slime_toy_3.iloc[[10,11],:]
slime_toy_3 = slime_toy_3.drop(index=[10, 11])

toy_3_clean_up = toy_3_clean_up.apply(lambda x: x.str.split('^([\w]+\s[\w]+)', regex=True).explode())
toy_3_clean_up[toy_3_clean_up.columns] = toy_3_clean_up.apply(lambda x: x.str.strip())
toy_3_clean_up = toy_3_clean_up.iloc[:,1]
blanks = [''] * len(toy_3_clean_up)
df = pd.DataFrame(list(zip(blanks, toy_3_clean_up)),
               columns =['report_funcuse', 'raw_chem_name'])
df = df.replace(r'^\s*$', np.nan, regex=True)
df = df[df['raw_chem_name'].notna()]

slime_toy_3.columns = ['report_funcuse', 'raw_chem_name']
slime_toy_3.reset_index(inplace = True, drop = True)
slime_toy_3 = slime_toy_3.append(df)
slime_toy_3.iat[10, 0] = 'Colourant'

slime_toy_3 = slime_toy_3.dropna(how='all')
slime_toy_3.fillna(method='ffill', inplace=True)
slime_toy_3 = slime_toy_3.groupby(['raw_chem_name'], as_index=False)['report_funcuse'].apply(' '.join)
slime_toy_3 = slime_toy_3.drop(slime_toy_3[slime_toy_3["report_funcuse"].str.contains("ubstance|ame")].index)
slime_toy_3['report_funcuse'] = slime_toy_3['report_funcuse'].str.replace('- ', '')


slime_toy_3.reset_index(inplace=True, drop=True)
slime_toy_3['component'] = 'Slime Toy 3'

    # for name, value in slime
# %%%

table_7_1and2 = slime_toy_1.append(slime_toy_2)
table_7_final = table_7_1and2.append(slime_toy_3)
table_7 = table_7_final

# %%%
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("*","")
    table_7["raw_chem_name"].iloc[j]=clean(str(table_7["raw_chem_name"].iloc[j]))
    if len(table_7["raw_chem_name"].iloc[j].split())>1:
        table_7["raw_chem_name"].iloc[j]=" ".join(table_7["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration and csv creation
table_7["data_document_id"]="1668060"
table_7["data_document_filename"]="slime_toys_f.pdf"
table_7["doc_date"]="June 2020"
table_7["raw_category"]=""
table_7["raw_cas"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_7.to_csv("slime_toys_table_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component"], index=False)



# %% TABLE 8
# %%% RAW EXTRACTION
table_8_raw=read_pdf(file, pages="30", stream=True, multiple_tables=True, pandas_options={'header': None})
table_8 = table_8_raw[0]
table_8 = table_8.iloc[:,[0,1]]
table_8 = table_8.dropna(how='all')
table_8.columns = ['raw_chem_name', 'raw_cas']
table_8 = table_8.drop(table_8[table_8["raw_chem_name"].str.contains("ubstance|ame")].index)
table_8['report_funcuse'] = 'Preservatives'

# %%%
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8)):
    table_8["raw_chem_name"].iloc[j]=str(table_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("*","")
    table_8["raw_chem_name"].iloc[j]=clean(str(table_8["raw_chem_name"].iloc[j]))
    if len(table_8["raw_chem_name"].iloc[j].split())>1:
        table_8["raw_chem_name"].iloc[j]=" ".join(table_8["raw_chem_name"].iloc[j].split())
        
        
        
# %%%

table_8["data_document_id"]="1668061"
table_8["data_document_filename"]="slime_toys_g.pdf"
table_8["doc_date"]="June 2020"
table_8["raw_category"]=""
table_8["cat_code"]=""
table_8["component"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]="ACToR Assays and Lists"


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_8.to_csv("slime_toys_table_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component"], index=False)



# %% TABLE 10
# %%% RAW EXTRACTION
table_10_raw=read_pdf(file, pages="32-33", stream=True, multiple_tables=True, pandas_options={'header': None})
table_10=pd.concat([table_10_raw[1], table_10_raw[2]])
table_10 = table_10.iloc[:,[0,1]]
table_10.reset_index(inplace=True, drop=True)
table_10 = table_10.dropna(how='all')
table_10.columns = ['raw_chem_name', 'raw_cas']

# %%% cleaning
table_10 = table_10.fillna('')
table_10 = table_10.drop(table_10[table_10["raw_chem_name"].str.contains("ubstance|ame")].index)
table_10 = table_10.replace(r'^\s*$', np.nan, regex=True)

table_10.fillna(method='ffill', inplace=True)
table_10 = table_10.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(' '.join)
table_10 = table_10.sort_values('raw_cas', ascending=False)
table_10 = table_10.groupby(['raw_chem_name'], as_index=False)['raw_cas'].apply(''.join)
table_10.reset_index(inplace = True, drop = True)
table_10['report_funcuse'] = 'Fragrance'


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_10)):
    table_10["raw_chem_name"].iloc[j]=str(table_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("- ","")
    table_10["raw_chem_name"].iloc[j]=clean(str(table_10["raw_chem_name"].iloc[j]))
    if len(table_10["raw_chem_name"].iloc[j].split())>1:
        table_10["raw_chem_name"].iloc[j]=" ".join(table_10["raw_chem_name"].iloc[j].split())
# %%% repeated values declarations and csv creation

table_10["data_document_id"]="1668062"
table_10["data_document_filename"]="slime_toys_h.pdf"
table_10["doc_date"]="June 2020"
table_10["raw_category"]=""
table_10["cat_code"]=""
table_10["component"]=""
table_10["description_cpcat"]=""
table_10["cpcat_code"]=""
table_10["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_10.to_csv("slime_toys_table_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component"], index=False)


# %% Table 11
# %%% RAW EXTRACTION
table_11_raw=read_pdf(file, pages="34-35", stream=True, multiple_tables=True, pandas_options={'header': None})
table_11=pd.concat([table_11_raw[0], table_11_raw[1]])
table_11.reset_index(inplace=True, drop=True)
table_11 = table_11.iloc[:,[0,1]]
table_11 = table_11.dropna(how='all')
table_11.columns = ['raw_chem_name', 'raw_cas']


# %%% cleaning

table_11 = table_11.fillna('')
table_11 = table_11.drop(table_11[table_11["raw_chem_name"].str.contains("ubstance|ame")].index)
table_11 = table_11.replace(r'^\s*$', np.nan, regex=True)

table_11.fillna(method='ffill', inplace=True)


for j in range(0,len(table_11)):
    if len(table_11['raw_cas'].iloc[j]) <= 1:
        table_11['raw_cas'].iloc[j] = table_11['raw_cas'].iloc[j].replace('-', table_11['raw_chem_name'].iloc[j])
        table_11['raw_cas'].iloc[j+1] = table_11['raw_cas'].iloc[j].replace('-', table_11['raw_chem_name'].iloc[j])


table_11 = table_11.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(' '.join)
table_11 = table_11.iloc[:,[1,0]]

for j in range(0,len(table_11)):
    if "P" in table_11['raw_cas'].iloc[j]:
        table_11['raw_cas'].iloc[j] = "-"
        
        
table_11['report_funcuse'] = 'Preservatives'



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_11)):
    table_11["raw_chem_name"].iloc[j]=str(table_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("- ","-")
    table_11["raw_chem_name"].iloc[j]=clean(str(table_11["raw_chem_name"].iloc[j]))
    if len(table_11["raw_chem_name"].iloc[j].split())>1:
        table_11["raw_chem_name"].iloc[j]=" ".join(table_11["raw_chem_name"].iloc[j].split())


# %%%       

table_11["data_document_id"]="1668063"
table_11["data_document_filename"]="slime_toys_i.pdf"
table_11["doc_date"]="June 2020"
table_11["raw_category"]=""
table_11["cat_code"]=""
table_11["component"]=""
table_11["description_cpcat"]=""
table_11["cpcat_code"]=""
table_11["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_11.to_csv("slime_toys_table_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component"], index=False)




# %% Table 19
# %%% RAW EXTRACTION
table_19_raw=read_pdf(file, pages="58-61", stream=True, multiple_tables=True, pandas_options={'header': None})
table_19=pd.concat([table_19_raw[0], table_19_raw[1], table_19_raw[2], table_19_raw[3]])
table_19 = table_19.iloc[:,[0,1]]
table_19 = table_19.dropna(how='all')
table_19.reset_index(inplace=True, drop=True)
table_19.columns = ['raw_chem_name', 'raw_cas']


# %%% component declarations
binder = table_19.iloc[2:5,:]
other_substances = pd.DataFrame(table_19.iloc[6,:]).transpose()
preservatives = table_19.iloc[8:30,:]

# %%%binder component
binder.columns=['raw_chem_name','raw_cas']
binder['component'] = 'Binder'

# %%%other substances component
other_substances.columns=['raw_chem_name','raw_cas']
other_substances['component'] = 'Other substances'

# %%%preservatives component
preservatives.columns=['raw_chem_name','raw_cas']
preservatives = preservatives.fillna('')
preservatives = preservatives.drop(preservatives[preservatives["raw_chem_name"].str.contains("ubstance|ame")].index)
preservatives = preservatives.replace(r'^\s*$', np.nan, regex=True)
preservatives.fillna(method='ffill', inplace=True)

preservatives = preservatives.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(' '.join)
preservatives = preservatives.iloc[:,[1,0]]
preservatives['component'] = 'Preservatives'

# %%% combine 
table_19_binders_and_others = binder.append(other_substances)
table_19 = table_19_binders_and_others.append(preservatives)


# %%% cleaning


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_19)):
    table_19["raw_chem_name"].iloc[j]=str(table_19["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("- ","")
    table_19["raw_chem_name"].iloc[j]=clean(str(table_19["raw_chem_name"].iloc[j]))
    if len(table_19["raw_chem_name"].iloc[j].split())>1:
        table_19["raw_chem_name"].iloc[j]=" ".join(table_19["raw_chem_name"].iloc[j].split())


# %%%       

table_19["data_document_id"]="1668064"
table_19["data_document_filename"]="slime_toys_j.pdf"
table_19["doc_date"]="June 2020"
table_19["raw_category"]=""
table_19["report_funcuse"]=""
table_19["cat_code"]=""
table_19["description_cpcat"]=""
table_19["cpcat_code"]=""
table_19["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
table_19.to_csv("slime_toys_table_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component"], index=False)


# %% CONCAT ALL csv's TOGETHER
# %%% get files
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Slime\csvs')
path = os.getcwd()
files = os.path.join(path, "slime_toys_table_*.csv")

files = glob.glob(files)


# %%% joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv("slime_toys_ext.csv", index = False)

