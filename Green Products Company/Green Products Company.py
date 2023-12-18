#Michael Metcalf
#12/14/2023
from tabula import read_pdf
import pandas as pd
import string
import os
import re
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Green Products Company\Green Products Company Documents')
tableCGB=read_pdf("Copper-Green Brown.pdf", pages="3", lattice=False, pandas_options={'header': None})[0]
tableCGB.drop([0,1],axis=0,inplace=True)
tableCGB.drop([1],axis=1,inplace=True)
tableCGB.reset_index(drop=True,inplace=True)
tableCGB["data_document_id"]="1687044"
tableCGB["data_document_filename"] = "Copper-Green Brown.pdf"
tableCGB["prod_name"] = "Copper-Green Wood Preservative"
tableCGB["doc_date"] = "19-Oct-2022"
tableCGB["rev_num"] = ""
tableCGB["raw_category"] = "wood perservative"
tableCGB["raw_cas"] = tableCGB.iloc[:,1]
tableCGB["raw_chem_name"] = tableCGB.iloc[:,0]
tableCGB=tableCGB.dropna(subset=["raw_chem_name"])
for j in range(0, len(tableCGB)):
    tableCGB["raw_chem_name"].iloc[j]=str(tableCGB["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
tableCGB["report_funcuse"] = ""
tableCGB["raw_min_comp"] = ""
tableCGB.loc[0,"raw_min_comp"] = 5
tableCGB.loc[1,"raw_min_comp"] = 25
tableCGB.loc[2,"raw_min_comp"] = 20
tableCGB["raw_max_comp"] = ""
tableCGB.loc[0,"raw_max_comp"] = 25
tableCGB.loc[1,"raw_max_comp"] = 75
tableCGB.loc[2,"raw_max_comp"] = 70
tableCGB["unit_type"] = "percent volume"
tableCGB["ingrediant_rank"] = ""
tableCGB.loc[0,"ingrediant_rank"] = 1
tableCGB.loc[1,"ingrediant_rank"] = 2
tableCGB.loc[2,"ingrediant_rank"] = 3
tableCGB["raw_central_comp"] = ""
tableCGB["component"] = ""
tableCGB.to_csv("Copper-Green Brown.csv", columns=["data_document_id","data_document_filename","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"], index=False)
