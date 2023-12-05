#CSV was extracted using Tabula's web application
import pandas as pd
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\UK & UN')
table = pd.read_csv('Annual Report on Surveillance for Veterinary Residues in Food in the UK 2007.csv')
table.drop_duplicates(inplace=True)
table["description_cpcat"]=""
table.to_csv("Annual Report on Surveillance for Veterinary Residues in Food in the UK 2007.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","cpcat_code","description_cpcat","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

table2 = pd.read_csv('Annual Report on Surveillance for Veterinary Residues in Food in the UK 2008.csv')
table2.drop_duplicates(inplace=True)
table2.to_csv("Annual Report on Surveillance for Veterinary Residues in Food in the UK 2008.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)
