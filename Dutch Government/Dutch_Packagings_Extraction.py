from tabula import read_pdf
import numpy as np
import pandas as pd
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Dutch Government\Docs')

# DUTCH I - PLASTICS
i = 18
tableI1 = []
while i < 25:
     table=read_pdf("Dutch Packagings and Consumer Articles Regulation from July 1st 2022.pdf", pages=str(i), lattice=False, pandas_options={'header': None})[0]
     table.drop([0,3,4],axis=1,inplace=True)
     table.drop([0,1],axis=0,inplace=True)
     table.reset_index(drop=True,inplace=True)
     tableI1.append(table)
     i = i + 1
tableI1 = pd.concat(tableI1,ignore_index=True)
tableI1["raw_chem_name"] = tableI1.iloc[:,1]
tableI1["raw_cas"] = tableI1.iloc[:,0]

i = 0
while i < (len(tableI1)-1):
    if str(tableI1.at[i, "raw_cas"]).endswith('/'):
        tableI1.at[i, "raw_cas"] = str(tableI1.loc[i, "raw_cas"]) + str(tableI1.loc[i+1, "raw_cas"])
        tableI1.drop([i+1],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    elif str(tableI1.at[i, "raw_cas"]).endswith(';'):
        tableI1.at[i, "raw_cas"] = str(tableI1.loc[i, "raw_cas"]) + ' ' + str(tableI1.loc[i+1, "raw_cas"])
        tableI1.drop([i+1],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    elif str(tableI1.at[i, "raw_cas"]).endswith('-') and str(tableI1.at[i, "raw_cas"]) != '-':
        tableI1.at[i, "raw_cas"] = str(tableI1.loc[i, "raw_cas"]) + str(tableI1.loc[i+1, "raw_cas"])
        tableI1.at[i, "raw_chem_name"] = str(tableI1.loc[i, "raw_chem_name"]) + str(tableI1.loc[i+1, "raw_chem_name"])
        tableI1.drop([i+1],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    elif str(tableI1.at[i, "raw_cas"]).endswith('or'):
        tableI1.at[i, "raw_cas"] = str(tableI1.loc[i, "raw_cas"]) + ' ' + str(tableI1.loc[i+1, "raw_cas"])
        tableI1.drop([i+1],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    elif str(tableI1.at[i, "raw_cas"]).startswith('or'):
        tableI1.at[i-1, "raw_cas"] = str(tableI1.loc[i-1, "raw_cas"]) + ' ' + str(tableI1.loc[i, "raw_cas"])
        tableI1.drop([i],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    else:
        i = i + 1

j = 0
while j < len(tableI1):
    if(str(tableI1.loc[j,"raw_cas"])=="nan"):
        tableI1.at[j-1,"raw_chem_name"] = str(tableI1.loc[j-1, "raw_chem_name"]) + " " + str(tableI1.loc[j,"raw_chem_name"])
        tableI1.drop([j],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    else:
        j = j + 1

j = 0
while j < len(tableI1):
    if(str(tableI1.loc[j,"raw_chem_name"])=="nan"):
        tableI1.drop([j],axis=0,inplace=True)
        tableI1.reset_index(drop=True,inplace=True)
    else:
        j = j + 1

tableI1.drop_duplicates("raw_chem_name",inplace=True)
for j in range(0, len(tableI1)):
    tableI1["raw_chem_name"].iloc[j]=str(tableI1["raw_chem_name"].iloc[j]).strip().lower()
tableI1["data_document_id"] = "1723592"
tableI1["data_document_filename"] = "Dutch Packagings and Consumer Articles Regulation from July 1st 2022.pdf"
tableI1["doc_date"] = '09/13/2022'
tableI1["raw_category"] = ''
tableI1["report_funcuse"] = ''
tableI1["cat_code"] = ''
tableI1['description_cpcat'] = ''
tableI1["cpcat_code"] = ''
tableI1["cpcat_sourcetype"] = ''
tableI1["component"] = ''
tableI1["chem_detected_flag"] = ''
tableI1["author"] = 'Dutch Ministry of Health, Welfare and Sport'
tableI1["doi"] = ''
tableI1.to_csv("Dutch Packagings and Consumer Articles Regulation I - Plastics.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

# DUTCH XII - EPOXY POLYMERS
i = 99
tableI1 = []
while i < 101:
     table=read_pdf("Dutch Packagings and Consumer Articles Regulation from July 1st 2022.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
     table.drop([0,1,4,5],axis=1,inplace=True)
     table.drop([0,1,2],axis=0,inplace=True)
     table.reset_index(drop=True,inplace=True)
     tableI1.append(table)
     i = i + 1
tableI1 = pd.concat(tableI1,ignore_index=True)
tableI1.drop([6,7,8,9,10,11,12,13],axis=1,inplace=True)
tableI1["raw_chem_name"] = tableI1.iloc[:,1]
tableI1["raw_cas"] = tableI1.iloc[:,0]

# i = 0
# while i < (len(tableI1)-1):
#     if str(tableI1.at[i, "raw_cas"]).endswith(('/',';')):
#         tableI1.at[i, "raw_cas"] = str(tableI1.loc[i, "raw_cas"]) + str(tableI1.loc[i+1, "raw_cas"])
#         tableI1.drop([i+1],axis=0,inplace=True)
#         tableI1.reset_index(drop=True,inplace=True)
#     elif str(tableI1.at[i, "raw_cas"]).endswith('-'):
#         tableI1.at[i, "raw_cas"] = str(tableI1.loc[i, "raw_cas"]) + str(tableI1.loc[i+1, "raw_cas"])
#         tableI1.at[i, "raw_chem_name"] = str(tableI1.loc[i, "raw_chem_name"]) + str(tableI1.loc[i+1, "raw_chem_name"])
#         tableI1.drop([i+1],axis=0,inplace=True)
#         tableI1.reset_index(drop=True,inplace=True)
#     else:
#         i = i + 1

# j = 0
# while j < len(tableI1):
#     if(str(tableI1.loc[j,"raw_cas"])=="nan"):
#         tableI1.at[j-1,"raw_chem_name"] = str(tableI1.loc[j-1, "raw_chem_name"]) + " " + str(tableI1.loc[j,"raw_chem_name"])
#         tableI1.drop([j],axis=0,inplace=True)
#         tableI1.reset_index(drop=True,inplace=True)
#     else:
#         j = j + 1

# j = 0
# while j < len(tableI1):
#     if(str(tableI1.loc[j,"raw_chem_name"])=="nan"):
#         tableI1.drop([j],axis=0,inplace=True)
#         tableI1.reset_index(drop=True,inplace=True)
#     else:
#         j = j + 1

tableI1.drop_duplicates("raw_chem_name",inplace=True)
for j in range(0, len(tableI1)):
    tableI1["raw_chem_name"].iloc[j]=str(tableI1["raw_chem_name"].iloc[j]).strip().lower()
tableI1["data_document_id"] = "1723608"
tableI1["data_document_filename"] = "Dutch Packagings and Consumer Articles Regulation from July 1st 2022 - Copy (16).pdf"
tableI1["doc_date"] = '09/13/2022'
tableI1["raw_category"] = ''
tableI1["report_funcuse"] = ''
tableI1["cat_code"] = ''
tableI1['description_cpcat'] = ''
tableI1["cpcat_code"] = ''
tableI1["cpcat_sourcetype"] = ''
tableI1["component"] = ''
tableI1["chem_detected_flag"] = ''
tableI1["author"] = 'Dutch Ministry of Health, Welfare and Sport'
tableI1["doi"] = ''
tableI1.to_csv("Dutch Packagings and Consumer Articles Regulation XII - Epoxy Polymers.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)
