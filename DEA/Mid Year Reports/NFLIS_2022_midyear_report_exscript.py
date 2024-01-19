# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:57:53 2024

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

# =============================================================================
# 
# os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022")
# 
# 
# file_names = pd.read_csv("filenames_2022.csv")
# file_names = file_names["filename"].to_list()
# 
# 
# data = os.path.abspath("pdfs/")
# 
# for i, f in enumerate(os.listdir(data)):
#     
#     file = file_names[i]
#     src = os.path.join(data, f)
#     dst = os.path.join(data, file)
#     os.rename(src, dst)
#     
# =============================================================================


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

    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022')
    remainder = glob('*.pdf')
    
    
    pdfToText(remainder)
    
    


    

# %% file

file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\pdfs\NFLIS-Drug-MYR2022_table1.1.pdf"
# %%% convert and use txt file
# files = [file]
# pdfToText(files)



os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022")

txt_file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\NFLIS-Drug-MYR2022_table1.1.txt'
ifile = open(txt_file, encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)
lines = cleaned.split('\n')
clean_lines = [x for x in lines if len(x) > 0]




# %% Table 1.1
table_1_1_raw = read_pdf(file, pages = '8', pandas_options={'header': None})

table_1_1 = table_1_1_raw[0]
table_1_1 = table_1_1.iloc[1:32, 0:2]
table_1_1.reset_index(drop = True, inplace = True)
table_1_1.columns = ['raw_chem_name','misc']




table_1_1['misc'].fillna(method='ffill', inplace=True)
table_1_1 = table_1_1.groupby(['misc'], sort = False, as_index=False)['raw_chem_name'].apply(' '.join)
table_1_1 = table_1_1.loc[:,['raw_chem_name']]


table_1_1['raw_chem_name'].iloc[5] = np.NaN
table_1_1 = table_1_1.dropna(how = "all", axis = 0)

for i,j in enumerate(table_1_1['raw_chem_name']):
    new_j = re.sub(r'\d{1}$', '',str(j))
    table_1_1['raw_chem_name'].iloc[i] = str(new_j)



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_1)):
    table_1_1["raw_chem_name"].iloc[j]=str(table_1_1["raw_chem_name"].iloc[j]).strip().lower()
    table_1_1["raw_chem_name"].iloc[j]=clean(str(table_1_1["raw_chem_name"].iloc[j]))
    if len(table_1_1["raw_chem_name"].iloc[j].split())>1:
        table_1_1["raw_chem_name"].iloc[j]=" ".join(table_1_1["raw_chem_name"].iloc[j].split())
        

#Repeating values declaration 
table_1_1["data_document_id"]="1690455"
table_1_1["data_document_filename"]="NFLIS-Drug-MYR2022_table1.1.pdf"
table_1_1["doc_date"]="April 2023"
table_1_1["raw_cas"]=""
table_1_1["raw_category"]=""
table_1_1["component"]=""
table_1_1["report_funcuse"]=""
table_1_1["cat_code"]=""
table_1_1["description_cpcat"]=""
table_1_1["cpcat_code"]=""
table_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_1_1.to_csv("NFLIS-Drug-MYR2022_table1.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 1.2

table_1_2_raw = read_pdf(file, pages = '9', pandas_options={'header': None})
table_1_2 = table_1_2_raw[0]

table_1_2 = table_1_2[table_1_2[0].notna()]

table_1_2 = table_1_2.iloc[:,0:2]

table_1_2.columns = ['raw_chem_name', 'misc']
for i,j in enumerate(table_1_2['raw_chem_name']):
    new_j = re.sub(r'\d{1}$', '',str(j))
    table_1_2['raw_chem_name'].iloc[i] = str(new_j)

table_1_2 = table_1_2.iloc[1:,:]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_2)):
    table_1_2["raw_chem_name"].iloc[j]=str(table_1_2["raw_chem_name"].iloc[j]).strip().lower()
    table_1_2["raw_chem_name"].iloc[j]=clean(str(table_1_2["raw_chem_name"].iloc[j]))
    if len(table_1_2["raw_chem_name"].iloc[j].split())>1:
        table_1_2["raw_chem_name"].iloc[j]=" ".join(table_1_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_1_2["data_document_id"]="1690456"
table_1_2["data_document_filename"]="NFLIS-Drug-MYR2022_table1.2.pdf"
table_1_2["doc_date"]="April 2023"
table_1_2["raw_cas"]=""
table_1_2["raw_category"]=""
table_1_2["component"]=""
table_1_2["report_funcuse"]=""
table_1_2["cat_code"]=""
table_1_2["description_cpcat"]=""
table_1_2["cpcat_code"]=""
table_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_1_2.to_csv("NFLIS-Drug-MYR2022_table1.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.1


table_2_1_raw = read_pdf(file, pages = '20', pandas_options={'header': None})
table_2_1 = table_2_1_raw[0]

table_2_1 = table_2_1.iloc[7:,:2]

table_2_1.reset_index(drop = True, inplace=True)

table_2_1.iloc[1,0] = np.NaN
table_2_1 = table_2_1[table_2_1[0].notna()]
table_2_1.reset_index(drop = True, inplace=True)

table_2_1.columns = ['raw_chem_name', 'misc']


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).replace('²', '').strip().lower()
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if len(table_2_1["raw_chem_name"].iloc[j].split())>1:
        table_2_1["raw_chem_name"].iloc[j]=" ".join(table_2_1["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_1["data_document_id"]="1690457"
table_2_1["data_document_filename"]="NFLIS-Drug-MYR2022_table2.1.pdf"
table_2_1["doc_date"]="April 2023"
table_2_1["raw_cas"]=""
table_2_1["raw_category"]=""
table_2_1["report_funcuse"]=""
table_2_1["cat_code"]=""
table_2_1["component"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_2_1.to_csv("NFLIS-Drug-MYR2022_table2.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.2



table_2_2_raw = read_pdf(file, pages = '21', pandas_options={'header': None})
table_2_2 = table_2_2_raw[0]

table_2_2 = table_2_2.iloc[6:22, :2]

table_2_2 = table_2_2[table_2_2[0].notna()]

table_2_2.columns = ['raw_chem_name', 'misc']

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
table_2_2["data_document_id"]="1690458"
table_2_2["data_document_filename"]="NFLIS-Drug-MYR2022_table2.2.pdf"
table_2_2["doc_date"]="April 2023"
table_2_2["raw_cas"]=""
table_2_2["raw_category"]=""
table_2_2["report_funcuse"]=""
table_2_2["component"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_2_2.to_csv("NFLIS-Drug-MYR2022_table2.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)
    
# %% Table 2.3


table_2_3_raw = read_pdf(file, pages = '21', pandas_options={'header': None})
table_2_3 = table_2_3_raw[0]

table_2_3 = table_2_3.iloc[36:,:2]

table_2_3 = table_2_3[table_2_3[0].notna()]

start_found = False
for i,j in enumerate(clean_lines):
    if 'table 2.3' in str(j):
        start = i
        start_found = True
    elif start_found == True and 'anabolic steroids' in str(j):
        stop = i
        break
    



table_2_3.columns = ['raw_chem_name','misc']

for i,j in enumerate(table_2_3['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3}', str(j), maxsplit = 1)
    table_2_3['raw_chem_name'].iloc[i] = new_string[0]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).strip().lower()
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))
    if len(table_2_3["raw_chem_name"].iloc[j].split())>1:
        table_2_3["raw_chem_name"].iloc[j]=" ".join(table_2_3["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_3["data_document_id"]="1690459"
table_2_3["data_document_filename"]="NFLIS-Drug-MYR2022_table2.3.pdf"
table_2_3["doc_date"]="April 2023"
table_2_3["raw_cas"]=""
table_2_3["raw_category"]=""
table_2_3["component"]=""
table_2_3["report_funcuse"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_2_3.to_csv("NFLIS-Drug-MYR2022_table2.3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Table 2.4



table_2_4_raw = read_pdf(file, pages = '22', pandas_options={'header': None})
table_2_4 = table_2_4_raw[0]

table_2_4 = table_2_4.iloc[4:19,:2]

table_2_4.reset_index(drop = True, inplace = True)




table_2_4.columns = ['raw_chem_name', 'misc']   


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower()
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_4["data_document_id"]="1690460"
table_2_4["data_document_filename"]="NFLIS-Drug-MYR2022_table2.4.pdf"
table_2_4["doc_date"]="April 2023"
table_2_4["raw_cas"]=""
table_2_4["component"]=""
table_2_4["raw_category"]=""
table_2_4["report_funcuse"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_2_4.to_csv("NFLIS-Drug-MYR2022_table2.4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.5



table_2_5_raw = read_pdf(file, pages = '23', pandas_options={'header': None})
table_2_5 = table_2_5_raw[0]
table_2_5 = table_2_5.iloc[6:29,:2]

table_2_5.columns = ['raw_chem_name', 'misc']   

table_2_5['uniso'] = np.NaN
for i,j in enumerate(table_2_5['raw_chem_name']):
    if 'unspecified isomer' in str(j):
        table_2_5['uniso'].iloc[i] = 'true'
        table_2_5['raw_chem_name'].iloc[i] = str(j).split('(')[0].strip()
    else:
        continue

table_2_5 = table_2_5.sort_values(by=['raw_chem_name', 'uniso'])
table_2_5 = table_2_5.loc[:, ['raw_chem_name', 'uniso']]



table_2_5['uniso'].fillna(method='ffill', inplace=True)
table_2_5 = table_2_5.drop_duplicates()

for i,j in enumerate(table_2_5['uniso']):
    if 'true' in str(j):
        table_2_5['raw_chem_name'].iloc[i] = str(table_2_5['raw_chem_name'].iloc[i]) + ' (unspecified isomer)'
      

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[j]=str(table_2_5["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_5["raw_chem_name"].iloc[j]=clean(str(table_2_5["raw_chem_name"].iloc[j]))
    if len(table_2_5["raw_chem_name"].iloc[j].split())>1:
        table_2_5["raw_chem_name"].iloc[j]=" ".join(table_2_5["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_5["data_document_id"]="1690461"
table_2_5["data_document_filename"]="NFLIS-Drug-MYR2022_table2.5.pdf"
table_2_5["doc_date"]="April 2023"
table_2_5["raw_cas"]=""
table_2_5["raw_category"]=""
table_2_5["component"]=""
table_2_5["report_funcuse"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
table_2_5.to_csv("NFLIS-Drug-MYR2022_table2.5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Drugs Reported by Federal Laboratories


for i,j in enumerate(clean_lines):
    if 'frequently reported drugs' in str(j):
        print('###############')
        print(i)
        print(str(j))

start_found = False
for i,j in enumerate(clean_lines):
    if 'frequently reported drugs' in str(j):
        start = i
        start_found = True
        continue
    elif start_found == True and 'all other drug reports 9,540' in str(j):
        stop = i
        break


fed_labs = pd.DataFrame(clean_lines[start:stop])
fed_labs = fed_labs.iloc[6:,:]
fed_labs.columns = ['raw_chem_name']


for i,j in enumerate(fed_labs['raw_chem_name']):
    split_chem = re.split(r'\d%', str(j), maxsplit=1)[-1]
    split_chem_2 = re.split(r'\s\d{1,3},\d{1,4}\s', split_chem, maxsplit=1)[0]
    split_chem_3 = re.split(r'\s\d{1,3}\s\d{1,3}|\s\d{1,3},\d{1,3}', split_chem, maxsplit=1)[0]
    if len(split_chem_3) == 0:
        fed_labs['raw_chem_name'].iloc[i] = np.NaN    
    else:
        fed_labs['raw_chem_name'].iloc[i] = split_chem_3.strip()



for i,j in enumerate(fed_labs['raw_chem_name']):
    if 'nan' in str(j):
        continue
    else:
        new_j = re.sub(r'\d{1}$', '',str(j))
        fed_labs['raw_chem_name'].iloc[i] = str(new_j)


fed_labs = fed_labs.dropna(how = 'any', axis = 0)
fed_labs.reset_index(drop = True, inplace=True)

fed_labs = fed_labs_raw[0]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(fed_labs)):
    fed_labs["raw_chem_name"].iloc[j]=str(fed_labs["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    fed_labs["raw_chem_name"].iloc[j]=clean(str(fed_labs["raw_chem_name"].iloc[j]))
    if len(fed_labs["raw_chem_name"].iloc[j].split())>1:
        fed_labs["raw_chem_name"].iloc[j]=" ".join(fed_labs["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
fed_labs["data_document_id"]="1690462"
fed_labs["data_document_filename"]="NFLIS-Drug-MYR2022_table2.5.pdf"
fed_labs["doc_date"]="April 2023"
fed_labs["raw_cas"]=""
fed_labs["raw_category"]=""
fed_labs["component"]=""
fed_labs["report_funcuse"]=""
fed_labs["cat_code"]=""
fed_labs["description_cpcat"]=""
fed_labs["cpcat_code"]=""
fed_labs["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
fed_labs.to_csv("NFLIS-Drug-MYR2022_table2.5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)





# %% Joining files
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022\csvs")
path = os.getcwd()
files = os.path.join(path, "*.csv")

files = glob(files)


# joining files with concat and read_csv
extract_df = pd.concat(map(pd.read_csv, files), ignore_index=True)

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2022")
extract_df.to_csv("nflis_midyear_report_2022_ext.csv", index=False)


