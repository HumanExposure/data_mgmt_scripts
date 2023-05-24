# -*- coding: utf-8 -*-
"""
Created on Mon May 22 16:14:42 2023

@author: CLUTZ01
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:53:51 2023

@author: CLUTZ01
"""

# %% imports
from tabula import read_pdf
import pandas as pd
import string
import os
import glob
import re






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

# %%% file set up

# file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\survey_risk_assessment_of_developers_in_thermal_paper.pdf'
# execfile = "pdftotext.exe"
# execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64'
    

# pdf = '"'+file+'"'
# cmd = os.path.join(execpath,execfile)
# cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
# os.system(cmd)





# %% raw table ext with tabula
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\pdfs\survey_risk_assessment_of_developers_in_thermal_paper.pdf'
raw_tables = read_pdf(file, pages = 'all', stream = True, pandas_options={'header': None})

table_12 = read_pdf(file, pages = '48', stream = True, pandas_options={'header': None})

# %% Table 2


# %%% extraction and clean up
table_2=raw_tables[3]
table_2 = table_2.iloc[:,0]
table_2 = pd.DataFrame({'raw_chem_name': table_2.values})
table_2.dropna(how = 'all', inplace = True)



# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))
    if len(table_2["raw_chem_name"].iloc[j].split())>1:
        table_2["raw_chem_name"].iloc[j]=" ".join(table_2["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration 
table_2["data_document_id"]="1669866"
table_2["data_document_filename"]="survey_risk_assessment_of_developers_in_thermal_paper_a.pdf"
table_2["doc_date"]="December 2019"
table_2["raw_cas"]=""
table_2["component"]=""
table_2["raw_category"]=""
table_2["report_funcuse"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
table_2.to_csv("thermal_papers_table_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)





# %% TABLE 4

file_txt = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\survey_risk_assessment_of_developers_in_thermal_paper.txt"
ifile = open(file_txt, encoding='utf-8')
text = ifile.read()


cleaned = text
cleaned = cleanLine(text)
cleaned = re.sub(' +', ' ', cleaned)

# %%% cleaning
#select needed elements and create df
split_string = 'Hazard assessment (classification, most critical NOAEL/LOAEL values and DNEL values)'
split_string = split_string.lower()
table_4_raw = cleaned.split(split_string)
table_4_raw = table_4_raw[1]
table_4_raw = table_4_raw.split('\n')
# table_4 = read_pdf(file, pages = '24,25,26',stream = True, pandas_options={'header': None}, area=[[100,50,1000,1000]])


table_4_v2 = []
for line in table_4_raw:
    if len(line) == 0:
        continue
    
    elif 'registered' in line or re.search(r'(\d+)-(\d\d)-(\d)', line):
        table_4_v2.append(line)
        
table_4_v3 = []
for line in table_4_v2:
    per_line = line.split(' ')
    for index, p in enumerate(per_line):
        if 'registered' in p:
            stop_index = index
            break
        elif re.search(r'(\d+)-(\d\d)-(\d)', p):
            stop_index = index + 1
            break
        else:
            stop_index = index 
            
            
    new_p = per_line[0:stop_index]
    new_p = ' '.join(str(v) for v in new_p)
    table_4_v3.append(new_p)
    
table_4 = table_4_v3[0:14]

chem_name = []
raw_cas = []
for g in table_4:
    if re.search(r'(\d+)-(\d\d)-(\d)', g):
        raw_cas.append(g)
    else:
        chem_name.append(g)
        
        
table_4_df = pd.DataFrame(
    {'raw_chem_name': chem_name,
     'raw_cas': raw_cas,
    })      
        
 

# clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_df)):
    table_4_df["raw_chem_name"].iloc[j]=str(table_4_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_4_df["raw_chem_name"].iloc[j]=clean(str(table_4_df["raw_chem_name"].iloc[j]))
    table_4_df["raw_cas"].iloc[j]=str(table_4_df["raw_cas"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_4_df["raw_cas"].iloc[j]=clean(str(table_4_df["raw_cas"].iloc[j]))
    
    if len(table_4_df["raw_chem_name"].iloc[j].split())>1:
        table_4_df["raw_chem_name"].iloc[j]=" ".join(table_4_df["raw_chem_name"].iloc[j].split())
# %%% Repeating values declaration and csv creation
table_4 = table_4_df
table_4["data_document_id"]="1669867"
table_4["data_document_filename"]="survey_risk_assessment_of_developers_in_thermal_paper_b.pdf"
table_4["doc_date"]="December 2019"
table_4["report_funcuse"]=""
table_4["raw_category"]=""
table_4["component"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
table_4.to_csv("thermal_papers_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 6
# %%% RAW EXTRACTION
table_6_raw = raw_tables[5]
# %%% cleaning
#select needed elements and create df
table_6_raw = table_6_raw.iloc[1,1:3]

table_6 = []
for t in table_6_raw:
    t_split = t.split(' ')
    for s in t_split:
        table_6.append(s)
        
table_6_df = pd.DataFrame(
    {'raw_chem_name': table_6,
    })      


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6_df["raw_chem_name"].iloc[j]=str(table_6_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '')
    table_6_df["raw_chem_name"].iloc[j]=clean(str(table_6_df["raw_chem_name"].iloc[j]))
    if len(table_6_df["raw_chem_name"].iloc[j].split())>1:
        table_6_df["raw_chem_name"].iloc[j]=" ".join(table_6_df["raw_chem_name"].iloc[j].split())
# %%% Repeating values declaration and csv creation

table_6 = table_6_df
table_6["data_document_id"]="1669868"
table_6["data_document_filename"]="survey_risk_assessment_of_developers_in_thermal_paper_c.pdf"
table_6["doc_date"]="December 2019"
table_6["raw_category"]=""
table_6["raw_cas"]=""
table_6["component"]=""
table_6["report_funcuse"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
table_6.to_csv("thermal_papers_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% TABLE 7
# %%% RAW EXTRACTION
table_7_raw=raw_tables[6]
# %%% Cleaning
#select needed elements and create df

table_7_raw = table_7_raw.iloc[4:,1]
table_7 = table_7_raw.dropna()
table_7.reset_index(inplace=True, drop=True)


table_7_df = pd.DataFrame(
    {'raw_chem_name': table_7,
    })      

table_7 = table_7_df

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("*","")
    table_7["raw_chem_name"].iloc[j]=clean(str(table_7["raw_chem_name"].iloc[j]))
    if len(table_7["raw_chem_name"].iloc[j].split())>1:
        table_7["raw_chem_name"].iloc[j]=" ".join(table_7["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration and csv creation
table_7["data_document_id"]="1669869"
table_7["data_document_filename"]="survey_risk_assessment_of_developers_in_thermal_paper_d.pdf"
table_7["doc_date"]="December 2019"
table_7["raw_category"]=""
table_7["raw_cas"]=""
table_7["component"]=""
table_7["report_funcuse"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
table_7.to_csv("thermal_papers_table_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% TABLE 8
# %%% RAW EXTRACTION
table_8_raw=raw_tables[7]
# %%% cleaning
#select needed elements and create df

table_8_raw = table_8_raw.iloc[5:,1]
table_8 = table_8_raw.dropna()
table_8.reset_index(inplace=True, drop=True)


table_8_df = pd.DataFrame(
    {'raw_chem_name': table_8,
    })      

table_8 = table_8_df

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8)):
    table_8["raw_chem_name"].iloc[j]=str(table_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace("*","")
    table_8["raw_chem_name"].iloc[j]=clean(str(table_8["raw_chem_name"].iloc[j]))
    if len(table_8["raw_chem_name"].iloc[j].split())>1:
        table_8["raw_chem_name"].iloc[j]=" ".join(table_8["raw_chem_name"].iloc[j].split())


        
# %%% Repeating values declaration and csv creation

table_8["data_document_id"]="1669870"
table_8["data_document_filename"]="survey_risk_assessment_of_developers_in_thermal_paper_e.pdf"
table_8["doc_date"]="December 2019"
table_8["raw_category"]=""
table_8["report_funcuse"]=""
table_8["raw_cas"]=""
table_8["cat_code"]=""
table_8["component"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]="ACToR Assays and Lists"


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
table_8.to_csv("thermal_papers_table_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 12
# %%% RAW EXTRACTION

split_string_one = 'table 12. risk assessment (rcr-calculation) of exposure scenarios for bps, d-8 and tgsa.'
split_string_two = 'when calculating rcr using conventionally calculated dnel values and calculations where dnel (decreased metabolism)'

table_12_raw = cleaned.split(split_string_one)[-1]
table_12_raw = table_12_raw.split(split_string_two)[0]
table_12_raw = table_12_raw.split('\n')



table_12_v2 = []
for line in table_12_raw:
    if len(line) == 0:
        continue
    elif ',' not in line:
        continue
    else:
        table_12_v2.append(line)
        
        
table_12 = list(filter(lambda x: len(x) > 22, table_12_v2))

raw_chem_name = []
for l in table_12:
    new_l = l.split(',')[0]
    raw_chem_name.append(new_l)


table_12_df = pd.DataFrame(
    {'raw_chem_name': raw_chem_name,
    })      
table_12 = table_12_df

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_12)):
    table_12["raw_chem_name"].iloc[j]=str(table_12["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace(";","")
    table_12["raw_chem_name"].iloc[j]=clean(str(table_12["raw_chem_name"].iloc[j]))
    if len(table_12["raw_chem_name"].iloc[j].split())>1:
        table_12["raw_chem_name"].iloc[j]=" ".join(table_12["raw_chem_name"].iloc[j].split())
# %%% Repeating values declaration and csv creation

table_12["data_document_id"]="1669871"
table_12["data_document_filename"]="survey_risk_assessment_of_developers_in_thermal_paper_f.pdf"
table_12["doc_date"]="December 2019"
table_12["raw_category"]=""
table_12["raw_cas"]=""
table_12["report_funcuse"]=""
table_12["cat_code"]=""
table_12["component"]=""
table_12["description_cpcat"]=""
table_12["cpcat_code"]=""
table_12["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
table_12.to_csv("thermal_papers_table_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% CONCAT ALL csv's TOGETHER
# %%% get files
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DPS_Thermal Paper\csvs')
path = os.getcwd()
files = os.path.join(path, "thermal_papers_table_*.csv")

files = glob.glob(files)


# %%% joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv("thermal_papers_ext.csv", index = False)

