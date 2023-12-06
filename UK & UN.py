#CSV was extracted using Tabula's web application
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
