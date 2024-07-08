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
table["raw_central_comp"] = table.iloc[:,2]
for j in range(0, len(table)):
    table["raw_chem_name"].iloc[j]=str(table["raw_chem_name"].iloc[j]).strip().lower().replace("*","")

#Code to add rank
table["ingredient_rank"] = ""
j = 0
while j < len(table):
    table.at[j,"ingredient_rank"] = j + 1
    j = j + 1

#Code to fix comp
table["raw_min_comp"] = ""
table["raw_max_comp"] = ""
j = 0
while j < len(table):
    if "-" in str(table.loc[j,"raw_central_comp"]):
        comp = str(table.loc[j,"raw_central_comp"]).split('-')
        table.at[j,"raw_min_comp"] = comp[0].strip()
        table.at[j,"raw_max_comp"] = comp[1].strip()
        table.at[j,"raw_central_comp"] = ""
        j = j + 1
    else:
        j = j + 1

table.drop([0,1,2],axis=1,inplace=True)
table["data_document_id"]="1764292"
table["data_document_filename"]="item_300972.pdf"
table["prod_name"] = "JR Watkins Aloe & Green Tea Lotion"
table["doc_date"]="12-Jan-2007"
table["rev_num"] = "1"
table["raw_category"]="Skin-care"
table["report_funcuse"] = ""
table["unit_type"] = 3
table["component"]=""

table.to_csv("item_300972.csv", columns=["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingredient_rank","raw_central_comp","component"], index=False)
