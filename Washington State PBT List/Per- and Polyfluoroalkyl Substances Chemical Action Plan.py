#%%
from tabula import read_pdf
import pandas as pd
import string
import os
import re
import math
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State of Washington\Chemical Action Plan\Documents')

#Function for combing rows
def combine_row(table):
    i = 0
    while i < len(table):
        if pd.isna(table.iloc[i,3]):
            if str(table.iloc[i-1,0]).endswith('-'):
                table.at[i-1,0] =  table.iloc[i-1,0] + table.iloc[i,0]
                table.drop(i,axis=0,inplace=True)
                table.reset_index(inplace=True,drop=True)
            else:
                table.at[i-1,0] =  table.iloc[i-1,0] + ' ' + table.iloc[i,0]
                table.drop(i,axis=0,inplace=True)
                table.reset_index(inplace=True,drop=True)
        else:
            i = i + 1
    return table

#Table10
table10_1=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 10.pdf", pages="126", lattice=False, pandas_options={'header': None})[0]
table10_1.drop([0,1,2],axis=0,inplace=True)
table10_1.drop([1],axis=1,inplace=True)
table10_1.reset_index(drop=True,inplace=True)
table10_1 = combine_row(table10_1)

table10_2=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 10.pdf", pages="127", lattice=False, pandas_options={'header': None})[0]
table10_2.drop([0,1,2],axis=0,inplace=True)
table10_2.drop([1],axis=1,inplace=True)
table10_2.reset_index(drop=True,inplace=True)
table10_2 = combine_row(table10_2)

array = [table10_1,table10_2]
table10 = pd.concat(array,ignore_index=True)
table10["data_document_id"]="1690548"
table10["data_document_filename"]="Per- and Polyfluoroalkyl Substances CAP Table 10.pdf"
table10["doc_date"]="September 2022"
table10["raw_chem_name"] = table10.iloc[:,0]
table10["raw_cas"] = table10.iloc[:,1]
table10["raw_category"]=""
table10["cat_code"]=""
table10["description_cpcat"]=""
table10["cpcat_code"]=""
table10["cpcat_sourcetype"]=""
table10["chem_detected_flag"]=""
table10.to_csv("Per- and Polyfluoroalkyl Substances CAP Table 10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

# %%
