#%%
from tabula import read_pdf
import pandas as pd
import string
import os
import re
import math
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State of Washington\PFAS Concentrations in Effluent\Documents')

table2 = read_pdf("PFAS Concentrations in Effluent Table 2.pdf", pages="16", lattice=False, pandas_options={'header': None})[0]
table2.drop([0,1],axis=1,inplace=True)
table2["raw_chem_name"] = ""
table2.reset_index(drop=True,inplace=True)
for j in range(0,len(table2.columns)-1):
    table2.loc[j,"raw_chem_name"] = table2.iloc[0,j]
table2.drop([2,3,4,5,6,7,8,9,10,11,12],axis=1,inplace=True)
table2["data_document_id"]="1690573"
table2["data_document_filename"]="PFAS Concentrations in Effluent Table 2.pdf"
table2["doc_date"]="November 2022"
table2["raw_cas"] = ""
table2["raw_category"]=""
table2["cat_code"]=""
table2["description_cpcat"]=""
table2["cpcat_code"]=""
table2["cpcat_sourcetype"]=""
table2["chem_detected_flag"]=1
table2.to_csv("PFAS Concentrations in Effluent Table 2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)
# %%
