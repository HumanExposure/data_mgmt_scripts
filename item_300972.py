#%%
from tabula import read_pdf
import pandas as pd
import numpy as np
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\OneDrive - Environmental Protection Agency (EPA)\Profile\Desktop\walmart')
table=read_pdf("item_300972.pdf", pages=2, lattice=False, pandas_options={'header': None})[0]
table.drop([0],axis=0,inplace=True)
table.reset_index(drop=True,inplace=True)

#Code to fix rows
j = 0
while j < len(table)-1:
    if table.isnull().iloc[j+1,1]:
        table.at[j,0] = str(table.iloc[j,0]) + " " + str(table.iloc[j+1,0])
        table.drop([j+1],axis=0,inplace=True)
        table.reset_index(inplace=True,drop=True)
        j = j + 1
    else:
        j = j + 1

table["raw_chem_name"] = table.iloc[:,0]
table["raw_cas"] = table.iloc[:,1]
table["raw_central_comp"] = table.iloc[2,0]
for j in range(0, len(table)):
    table["raw_chem_name"].iloc[j]=str(table["raw_chem_name"].iloc[j]).strip().lower().replace("*","")

table["ingredient_rank"] = ""
j = 0
while j < len(table)-1:
    table.at[j,"ingredient_rank"] = j + 1
    j = j + 1

table.drop([0,1,2],axis=1,inplace=True)
table["data_document_id"]="1764292"
table["data_document_filename"]="item_300972.pdf"
table["prod_name"] = "JR Watkins Aloe & Green Tea Lotion"
table["doc_date"]="12-Jan-2007"
table["rev_num"] = "1"
table["raw_category"]="Skin-care"
table["unit_type"] = 3
table["component"]=""
# %%
