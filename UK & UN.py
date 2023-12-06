#CSV was extracted using Tabula's web application
from tabula import read_pdf
import pandas as pd
import string
import os
import re
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\UK & UN')
table = pd.read_csv('Annual Report on Surveillance for Veterinary Residues in Food in the UK 2007.csv')
table.drop_duplicates(inplace=True)
table["description_cpcat"]=""
table.to_csv("Annual Report on Surveillance for Veterinary Residues in Food in the UK 2007.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","cpcat_code","description_cpcat","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

table2 = pd.read_csv('Annual Report on Surveillance for Veterinary Residues in Food in the UK 2008.csv')
table2.drop_duplicates(inplace=True)
table2.to_csv("Annual Report on Surveillance for Veterinary Residues in Food in the UK 2008.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

table3 = pd.read_csv('Annual Report on Surveillance for Veterinary Residues in Food in the UK 2009.csv')
table3.drop_duplicates("raw_chem_name",inplace=True)
table3.to_csv("Annual Report on Surveillance for Veterinary Residues in Food in the UK 2009.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

table4 = pd.read_csv("tabula-DWI70-2-232_c.csv")
table4.drop_duplicates("raw_chem_name",inplace=True)
for j in range(0, len(table4)):
    table4["raw_chem_name"].iloc[j]=str(table4["raw_chem_name"].iloc[j]).strip().lower()
j = 0
while j < len(table4):
    if(str(table4.loc[j,"raw_chem_name"])=="nan"):
        table4.drop([j],axis=0,inplace=True)
        table4.reset_index(drop=True,inplace=True)
    else:
        j = j + 1
table4.to_csv("DWI70-2-232_c.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

table5 = []
i = 100
while i < 107:
    table5sub = read_pdf("UK_Pharm_Use_orig_b.pdf", pages=i,lattice=True, pandas_options={'header': None})[1]
    table5sub.drop([0,1,2],axis=0,inplace=True)
    table5.append(table5sub)
    i = i + 1
table5107 = read_pdf("UK_Pharm_Use_orig_b.pdf", pages=107,lattice=True, pandas_options={'header': None})[0]
table5.append(table5107)
table5 = pd.concat(table5,ignore_index=True)
table5.drop([0,1,11,328,329,330],axis=0,inplace=True)
table5.drop([1,2,3,4],axis=1,inplace=True)
table5.reset_index(drop=True,inplace=True)
table5["raw_chem_name"] = table5.iloc[:,0]
for j in range(0, len(table5)):
     table5["raw_chem_name"].iloc[j]=str(table5["raw_chem_name"].iloc[j]).strip().lower()
table5.drop([0],axis=1,inplace=True)
table5.drop_duplicates('raw_chem_name',inplace=True)
table5["data_document_id"]="1363538"
table5["data_document_filename"]="UK_Pharm_Use_orig_b.pdf"
table5["doc_date"]="2007"
table5["raw_category"]=""
table5["raw_cas"] = ""
table5["report_funcuse"] = ""
table5["cat_code"]=""
table5["description_cpcat"]=""
table5["cpcat_code"]=""
table5["cpcat_sourcetype"]=""
table5["component"]=""
table5["chem_detected_flag"]=""
table5["author"]=""
table5["doi"]=""
table5.to_csv("UK_Pharm_Use_orig_b.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)
