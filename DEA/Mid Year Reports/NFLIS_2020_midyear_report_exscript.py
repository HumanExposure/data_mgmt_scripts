# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 10:11:50 2024

@author: CLUTZ01
"""

# %% imports
import os, string, re
import pandas as pd
import numpy as np
from tabula import read_pdf
from glob import glob
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


    

# %% file

file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\pdfs\NFLIS-Drug-MYR2020_table1.1.pdf"
file_txt = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\NFLIS-Drug-MYR2020_table1.1.txt"

# """ files = [file]
# pdfToText(files) """

ifile = open(file_txt.replace('.pdf', '.txt'), encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)
lines = cleaned.split('\n')
clean_lines = [x for x in lines if len(x) > 0]


# %% Table 1.1
table_1_1_raw = read_pdf(file, pages = '8', pandas_options={'header': None})
table_1_1 = table_1_1_raw[0].iloc[10:35,:]
table_1_1.reset_index(drop = True, inplace = True)
table_1_1.columns = ['raw_chem_name']


for i,j in enumerate(table_1_1['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3},', str(j), maxsplit = 1)
    table_1_1['raw_chem_name'].iloc[i] = new_string[0]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_1)):
    table_1_1["raw_chem_name"].iloc[j]=str(table_1_1["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_1_1["raw_chem_name"].iloc[j]=clean(str(table_1_1["raw_chem_name"].iloc[j]))
    if len(table_1_1["raw_chem_name"].iloc[j].split())>1:
        table_1_1["raw_chem_name"].iloc[j]=" ".join(table_1_1["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_1_1["data_document_id"]="1690471"
table_1_1["data_document_filename"]="NFLIS-Drug-MYR2020_table1.1.pdf"
table_1_1["doc_date"]="April 2021"
table_1_1["raw_cas"]=""
table_1_1["raw_category"]=""
table_1_1["component"]=""
table_1_1["report_funcuse"]=""
table_1_1["cat_code"]=""
table_1_1["description_cpcat"]=""
table_1_1["cpcat_code"]=""
table_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_1_1.to_csv("NFLIS-Drug-MYR2020_table1.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 1.2


table_1_2_raw = read_pdf(file, pages = '9', stream=True, pandas_options={'header': None})
table_1_2 = table_1_2_raw[0].iloc[1:28,0:1]
table_1_2.reset_index(drop = True, inplace = True)
table_1_2 = table_1_2.dropna(how = 'all', axis = 0)

table_1_2.columns = ['raw_chem_name']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_2)):
    table_1_2["raw_chem_name"].iloc[j]=str(table_1_2["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_1_2["raw_chem_name"].iloc[j]=clean(str(table_1_2["raw_chem_name"].iloc[j]))
    if len(table_1_2["raw_chem_name"].iloc[j].split())>1:
        table_1_2["raw_chem_name"].iloc[j]=" ".join(table_1_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_1_2["data_document_id"]="1690472"
table_1_2["data_document_filename"]="NFLIS-Drug-MYR2020_table1.2.pdf"
table_1_2["doc_date"]="April 2021"
table_1_2["raw_cas"]=""
table_1_2["raw_category"]=""
table_1_2["component"]=""
table_1_2["report_funcuse"]=""
table_1_2["cat_code"]=""
table_1_2["description_cpcat"]=""
table_1_2["cpcat_code"]=""
table_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_1_2.to_csv("NFLIS-Drug-MYR2020_table1.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.1


for i,j in enumerate(clean_lines):
    if 'table 2.1 narcotic analgesics' in str(j):
        start = i
        continue
    elif 'analgesics 766 0.88%' in str(j):
        stop = i
        break
    
table_2_1 = clean_lines[start+1:stop]


table_2_1 = [x for x in table_2_1 if re.search(r'\d{0,2}\.\d{1,2}%', str(x))]
table_2_1 = pd.DataFrame(table_2_1, columns=['raw_chem_name'])

for i,t in enumerate(table_2_1['raw_chem_name']):
    if re.search(r'[a-z]', str(t)):
        split_txt = re.split(r'\s\d{1,2}', str(t), maxsplit=1)
        table_2_1['raw_chem_name'].iloc[i] = split_txt[0]
        
table_2_1 = table_2_1.dropna(how = 'all', axis = 0)
table_2_1.reset_index(drop = True, inplace = True)   

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if len(table_2_1["raw_chem_name"].iloc[j].split())>1:
        table_2_1["raw_chem_name"].iloc[j]=" ".join(table_2_1["raw_chem_name"].iloc[j].split())



#Repeating values declaration 
table_2_1["data_document_id"]="1690473"
table_2_1["data_document_filename"]="NFLIS-Drug-MYR2020_table2.1.pdf"
table_2_1["doc_date"]="April 2021"
table_2_1["raw_cas"]=""
table_2_1["raw_category"]=""
table_2_1["report_funcuse"]=""
table_2_1["cat_code"]=""
table_2_1["component"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_2_1.to_csv("NFLIS-Drug-MYR2020_table2.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.2


for i,j in enumerate(clean_lines):
    if 'table 2.2 tranquilizers and depressants' in str(j):
        start = i
        continue
    elif 'other tranquilizers and depressants 662 2.82% 240' in str(j):
        stop = i
        break
    
table_2_2 = clean_lines[start+1:stop]


table_2_2 = [x for x in table_2_2 if re.search(r'\d{0,2}\.\d{1,2}%', str(x))]
table_2_2 = pd.DataFrame(table_2_2, columns=['raw_chem_name'])

for i,t in enumerate(table_2_2['raw_chem_name']):
    if re.search(r'[a-z]', str(t)):
        split_txt = re.split(r'\s\d{1,2}', str(t), maxsplit=1)
        table_2_2['raw_chem_name'].iloc[i] = split_txt[0]
        
table_2_2 = table_2_2.dropna(how = 'all', axis = 0)
table_2_2.reset_index(drop = True, inplace = True)   


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_2)):
    table_2_2["raw_chem_name"].iloc[j]=str(table_2_2["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_2["raw_chem_name"].iloc[j]=clean(str(table_2_2["raw_chem_name"].iloc[j]))
    if len(table_2_2["raw_chem_name"].iloc[j].split())>1:
        table_2_2["raw_chem_name"].iloc[j]=" ".join(table_2_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_2["data_document_id"]="1690474"
table_2_2["data_document_filename"]="NFLIS-Drug-MYR2020_table2.2.pdf"
table_2_2["doc_date"]="April 2021"
table_2_2["raw_cas"]=""
table_2_2["raw_category"]=""
table_2_2["report_funcuse"]=""
table_2_2["component"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_2_2.to_csv("NFLIS-Drug-MYR2020_table2.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)
    
# %% Table 2.3

for i,j in enumerate(clean_lines):
    if 'anabolic steroid reports' in str(j):
        start = i
        continue
    elif 'other anabolic steroids 52 5.18%' in str(j):
        stop = i
        break
    
table_2_3 = clean_lines[start+1:stop]
table_2_3 = pd.DataFrame(table_2_3, columns=['raw_chem_name'])
for i,t in enumerate(table_2_3['raw_chem_name']):
    if re.search(r'[a-z]', str(t)):
        split_txt = re.split(r'\s\d{1,2}', str(t), maxsplit=1)
        table_2_3['raw_chem_name'].iloc[i] = split_txt[0]
        
table_2_3 = table_2_3.dropna(how = 'all', axis = 0)
table_2_3.reset_index(drop = True, inplace = True)        
        

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))
    if len(table_2_3["raw_chem_name"].iloc[j].split())>1:
        table_2_3["raw_chem_name"].iloc[j]=" ".join(table_2_3["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_3["data_document_id"]="1690475"
table_2_3["data_document_filename"]="NFLIS-Drug-MYR2020_table2.3.pdf"
table_2_3["doc_date"]="April 2021"
table_2_3["raw_cas"]=""
table_2_3["raw_category"]=""
table_2_3["component"]=""
table_2_3["report_funcuse"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_2_3.to_csv("NFLIS-Drug-MYR2020_table2.3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Table 2.4


for i,j in enumerate(clean_lines):
    if 'phenethylamine reports number' in str(j):
        start = i
        continue
    elif 'other phenethylamines' in str(j):
        stop = i
        break

table_2_4 = clean_lines[start:stop]
table_2_4 = pd.DataFrame(table_2_4, columns=['raw_chem_name'])
for i,t in enumerate(table_2_4['raw_chem_name']):
    if re.search(r'[a-z]', str(t)):
        split_txt = re.split(r'\s\d', str(t), maxsplit=1)
        table_2_4['raw_chem_name'].iloc[i] = split_txt[0]
    else:
        table_2_4['raw_chem_name'].iloc[i] = np.NaN
        
table_2_4 = table_2_4.iloc[1:, :]
table_2_4.reset_index(drop = True, inplace = True)    

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_4["data_document_id"]="1690476"
table_2_4["data_document_filename"]="NFLIS-Drug-MYR2020_table2.4.pdf"
table_2_4["doc_date"]="April 2021"
table_2_4["raw_cas"]=""
table_2_4["component"]=""
table_2_4["raw_category"]=""
table_2_4["report_funcuse"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_2_4.to_csv("NFLIS-Drug-MYR2020_table2.4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.5
for i,j in enumerate(clean_lines):
    if 'synthetic cannabinoid reports' in str(j):
        start = i
        continue
    elif 'other synthetic cannabinoids' in str(j):
        stop = i
        break
    
table_2_5 = clean_lines[start:stop]
table_2_5 = pd.DataFrame(table_2_5, columns=['raw_chem_name'])

for i,t in enumerate(table_2_5['raw_chem_name']):
    if re.search(r'\d%', str(t)):
        split_txt = re.split(r'\s\d\d+', str(t), maxsplit=1)
        table_2_5['raw_chem_name'].iloc[i] = split_txt[0]
    else:
        table_2_5['raw_chem_name'].iloc[i] = np.NaN
        
table_2_5 = table_2_5.dropna(how = 'all', axis = 0)
table_2_5.reset_index(drop = True, inplace = True)    

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[j]=str(table_2_5["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_5["raw_chem_name"].iloc[j]=clean(str(table_2_5["raw_chem_name"].iloc[j]))
    if len(table_2_5["raw_chem_name"].iloc[j].split())>1:
        table_2_5["raw_chem_name"].iloc[j]=" ".join(table_2_5["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_5["data_document_id"]="1690477"
table_2_5["data_document_filename"]="NFLIS-Drug-MYR2020_table2.5.pdf"
table_2_5["doc_date"]="April 2021"
table_2_5["raw_cas"]=""
table_2_5["raw_category"]=""
table_2_5["component"]=""
table_2_5["report_funcuse"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
table_2_5.to_csv("NFLIS-Drug-MYR2020_table2.5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %%

start_found = False
for i,j in enumerate(clean_lines):
    if 'frequently reported drugs' in str(j):
        start = i
        start_found = True
        print('start found')
        continue
    elif start_found == True and 'all other drugs 68,306' in str(j):
        stop = i
        print('stop found')
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



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(fed_labs)):
    fed_labs["raw_chem_name"].iloc[j]=str(fed_labs["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    fed_labs["raw_chem_name"].iloc[j]=clean(str(fed_labs["raw_chem_name"].iloc[j]))
    if len(fed_labs["raw_chem_name"].iloc[j].split())>1:
        fed_labs["raw_chem_name"].iloc[j]=" ".join(fed_labs["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
fed_labs["data_document_id"]="1690478"
fed_labs["data_document_filename"]="NFLIS-Drug-MYR2021_frequentdrugsfedlabs.pdf"
fed_labs["doc_date"]="April 2021"
fed_labs["raw_cas"]=""
fed_labs["raw_category"]=""
fed_labs["component"]=""
fed_labs["report_funcuse"]=""
fed_labs["cat_code"]=""
fed_labs["description_cpcat"]=""
fed_labs["cpcat_code"]=""
fed_labs["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
fed_labs.to_csv("NFLIS-Drug-MYR2020_fed_labs.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Joining files
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020\csvs")
path = os.getcwd()
files = os.path.join(path, "*.csv")

files = glob(files)


# joining files with concat and read_csv
extract_df = pd.concat(map(pd.read_csv, files), ignore_index=True)

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\midyear reports\2020")
extract_df.to_csv("nflis_midyear_report_2020_ext.csv", index=False)


