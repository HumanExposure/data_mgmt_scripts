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

    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\annual reports\2019')
    remainder = glob('*.pdf')
    
    
    pdfToText(remainder)
    
    
# %%renaming files


os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\annual reports\2019")


file_names = pd.read_csv("filenames_2019_ar.csv")
file_names = file_names["filename"].to_list()


data = os.path.abspath("pdfs/")

for i, f in enumerate(os.listdir(data)):
    
    file = file_names[i]
    src = os.path.join(data, f)
    dst = os.path.join(data, file)
    os.rename(src, dst)
    

# %% file

file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\annual reports\2019\pdfs\NFLIS-Drug-AR2019_frequentdrugsfedlabs.pdf"
# %%%
files = [file]
pdfToText(files)

# %%
file_txt= r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\annual reports\2019\NFLIS-Drug-AR2019_frequentdrugsfedlabs.txt"

ifile = open(file_txt, encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)
lines = cleaned.split('\n')
clean_lines = [x for x in lines if len(x) > 0]

# %% Table 1.1
table_1_1_raw = read_pdf(file, pages = '7', pandas_options={'header': None})
table_1_1 = table_1_1_raw[0].iloc[5:30,:]
table_1_1.reset_index(drop = True, inplace = True)
table_1_1.columns = ['raw_chem_name', 'get rid of']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_1)):
    table_1_1["raw_chem_name"].iloc[j]=str(table_1_1["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_1_1["raw_chem_name"].iloc[j]=clean(str(table_1_1["raw_chem_name"].iloc[j]))
    if len(table_1_1["raw_chem_name"].iloc[j].split())>1:
        table_1_1["raw_chem_name"].iloc[j]=" ".join(table_1_1["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_1_1["data_document_id"]="1690417"
table_1_1["data_document_filename"]="NFLIS-Drug-AR2019_table1.1.pdf"
table_1_1["doc_date"]="September 2020"
table_1_1["raw_cas"]=""
table_1_1["raw_category"]=""
table_1_1["component"]=""
table_1_1["report_funcuse"]=""
table_1_1["cat_code"]=""
table_1_1["description_cpcat"]=""
table_1_1["cpcat_code"]=""
table_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_1_1.to_csv("NFLIS-Drug-AR2019_table1.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 1.2


table_1_2_raw = read_pdf(file, pages = '8',area=[[129,300,461,550]], pandas_options={'header': None})
table_1_2 = table_1_2_raw[0].iloc[:,[0,1]]
table_1_2.reset_index(drop = True, inplace = True)
table_1_2 = table_1_2.dropna(how = 'all', axis = 0)

table_1_2.columns = ['raw_chem_name','misc']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_2)):
    table_1_2["raw_chem_name"].iloc[j]=str(table_1_2["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_1_2["raw_chem_name"].iloc[j]=clean(str(table_1_2["raw_chem_name"].iloc[j]))
    if len(table_1_2["raw_chem_name"].iloc[j].split())>1:
        table_1_2["raw_chem_name"].iloc[j]=" ".join(table_1_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_1_2["data_document_id"]="1690418"
table_1_2["data_document_filename"]="NFLIS-Drug-AR2019_table1.2.pdf"
table_1_2["doc_date"]="September 2020"
table_1_2["raw_cas"]=""
table_1_2["raw_category"]=""
table_1_2["component"]=""
table_1_2["report_funcuse"]=""
table_1_2["cat_code"]=""
table_1_2["description_cpcat"]=""
table_1_2["cpcat_code"]=""
table_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_1_2.to_csv("NFLIS-Drug-AR2019_table1.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.1


table_2_1_raw = read_pdf(file, pages = '14', stream = True, pandas_options={'header': None})
table_2_1 = table_2_1_raw[0].iloc[5:22,[1,2]]
table_2_1 = table_2_1.dropna(how = 'all', axis = 0)
table_2_1.reset_index(drop = True, inplace = True)

table_2_1.columns = ['raw_chem_name', 'misc']



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if len(table_2_1["raw_chem_name"].iloc[j].split())>1:
        table_2_1["raw_chem_name"].iloc[j]=" ".join(table_2_1["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_1["data_document_id"]="1690419"
table_2_1["data_document_filename"]="NFLIS-Drug-AR2019_table2.1.pdf"
table_2_1["doc_date"]="September 2020"
table_2_1["raw_cas"]=""
table_2_1["raw_category"]=""
table_2_1["report_funcuse"]=""
table_2_1["cat_code"]=""
table_2_1["component"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_2_1.to_csv("NFLIS-Drug-AR2019_table2.1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 2.2

table_2_2_raw = read_pdf(file, pages = '15', stream = True,area=[[10,300,700,400]], pandas_options={'header': None})
table_2_2 = table_2_2_raw[0].iloc[5:20,[0]]
table_2_2.reset_index(drop = True, inplace = True)


table_2_2.columns = ['raw_chem_name']

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_2)):
    table_2_2["raw_chem_name"].iloc[j]=str(table_2_2["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_2["raw_chem_name"].iloc[j]=clean(str(table_2_2["raw_chem_name"].iloc[j]))
    if len(table_2_2["raw_chem_name"].iloc[j].split())>1:
        table_2_2["raw_chem_name"].iloc[j]=" ".join(table_2_2["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_2["data_document_id"]="1690420"
table_2_2["data_document_filename"]="NFLIS-Drug-AR2019_table2.2.pdf"
table_2_2["doc_date"]="September 2020"
table_2_2["raw_cas"]=""
table_2_2["raw_category"]=""
table_2_2["report_funcuse"]=""
table_2_2["component"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_2_2.to_csv("NFLIS-Drug-AR2019_table2.2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)
    
# %% Table 2.3





for i,j in enumerate(clean_lines):
    if 'anabolic steroid reports' in str(j):
        start = i
        continue
    elif 'other steroids' in str(j):
        stop = i
        break
    
table_2_3 = clean_lines[(start+1):stop]
table_2_3 = pd.DataFrame(table_2_3, columns=['raw_chem_name'])



for i,j in enumerate(table_2_3['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3}', str(j), maxsplit = 1)
    table_2_3['raw_chem_name'].iloc[i] = new_string[0]
        

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))
    if len(table_2_3["raw_chem_name"].iloc[j].split())>1:
        table_2_3["raw_chem_name"].iloc[j]=" ".join(table_2_3["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_3["data_document_id"]="1690421"
table_2_3["data_document_filename"]="NFLIS-Drug-AR2019_table2.3.pdf"
table_2_3["doc_date"]="September 2020"
table_2_3["raw_cas"]=""
table_2_3["raw_category"]=""
table_2_3["component"]=""
table_2_3["report_funcuse"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_2_3.to_csv("NFLIS-Drug-AR2019_table2.3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Table 2.4


for i,j in enumerate(clean_lines):
    if 'phenethylamine reports number' in str(j):
        start = i
        continue
    elif 'other phenethylamines' in str(j):
        stop = i
        break
    
table_2_4 = clean_lines[(start+2):stop]
table_2_4 = pd.DataFrame(table_2_4, columns=['raw_chem_name'])


for i,j in enumerate(table_2_4['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3}', str(j), maxsplit = 1)
    table_2_4['raw_chem_name'].iloc[i] = new_string[0]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_4["data_document_id"]="1690422"
table_2_4["data_document_filename"]="NFLIS-Drug-AR2019_table2.4.pdf"
table_2_4["doc_date"]="September 2020"
table_2_4["raw_cas"]=""
table_2_4["component"]=""
table_2_4["raw_category"]=""
table_2_4["report_funcuse"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_2_4.to_csv("NFLIS-Drug-AR2019_table2.4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


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
        split_txt = re.split(r'\s\d', str(t), maxsplit=1)
        table_2_5['raw_chem_name'].iloc[i] = split_txt[0]
    else:
        table_2_5['raw_chem_name'].iloc[i] = np.NaN
        
table_2_5 = table_2_5.dropna(how = 'all', axis = 0)
table_2_5.reset_index(drop = True, inplace = True)    

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[j]=str(table_2_5["raw_chem_name"].iloc[j]).strip().lower()
    table_2_5["raw_chem_name"].iloc[j]=clean(str(table_2_5["raw_chem_name"].iloc[j]))
    if len(table_2_5["raw_chem_name"].iloc[j].split())>1:
        table_2_5["raw_chem_name"].iloc[j]=" ".join(table_2_5["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
table_2_5["data_document_id"]="1690423"
table_2_5["data_document_filename"]="NFLIS-Drug-AR2019_table2.5.pdf"
table_2_5["doc_date"]="September 2020"
table_2_5["raw_cas"]=""
table_2_5["raw_category"]=""
table_2_5["component"]=""
table_2_5["report_funcuse"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
table_2_5.to_csv("NFLIS-Drug-AR2019_table2.5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Most Frequently Reported Drugs By Federal Laboratories


for i,j in enumerate(clean_lines):
    if 'methamphetamine 15,126' in str(j):
        start = i
        break

for i,j in enumerate(clean_lines):
    if i<start:
        continue
    elif 'all other drug reports' in str(j):
        stop = i
        break
    
most_freq_by_lab = clean_lines[start:stop]
most_freq_by_lab = pd.DataFrame(most_freq_by_lab, columns=['raw_chem_name'])



for i,j in enumerate(most_freq_by_lab['raw_chem_name']):
    new_string = re.split(r'\s\d{1,3}', str(j), maxsplit = 1)
    most_freq_by_lab['raw_chem_name'].iloc[i] = new_string[0]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(most_freq_by_lab)):
    most_freq_by_lab["raw_chem_name"].iloc[j]=str(most_freq_by_lab["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    most_freq_by_lab["raw_chem_name"].iloc[j]=clean(str(most_freq_by_lab["raw_chem_name"].iloc[j]))
    if len(most_freq_by_lab["raw_chem_name"].iloc[j].split())>1:
        most_freq_by_lab["raw_chem_name"].iloc[j]=" ".join(most_freq_by_lab["raw_chem_name"].iloc[j].split())
        
        
#Repeating values declaration 
most_freq_by_lab["data_document_id"]="1690326"
most_freq_by_lab["data_document_filename"]="NFLIS-Drug-AR2019_frequentdrugsfedlabs.pdf"
most_freq_by_lab["doc_date"]="September 2020"
most_freq_by_lab["raw_cas"]=""
most_freq_by_lab["raw_category"]=""
most_freq_by_lab["report_funcuse"]=""
most_freq_by_lab["cat_code"]=""
most_freq_by_lab["component"]=""
most_freq_by_lab["description_cpcat"]=""
most_freq_by_lab["cpcat_code"]=""
most_freq_by_lab["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs")
most_freq_by_lab.to_csv("NFLIS-Drug-AR2019_frequentdrugsfedlabs.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Joining files
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018\csvs\\")
path = os.getcwd()
files = os.path.join(path, "*.csv")

files = glob(files)


# joining files with concat and read_csv
extract_df = pd.concat(map(pd.read_csv, files), ignore_index=True)

os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\DEA\2018")
extract_df.to_csv("nflis_annual_report_2018_ext.csv", index=False)


