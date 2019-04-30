#lkoval
#4-30-19

from tabula import read_pdf
import pandas as pd
import string

#Read in table 4.1 as pandas dfs using tabula

#Table 4.1
table_4_1=read_pdf("document_1372204.pdf", pages="19-21", lattice=True, pandas_options={'header': None})
table_4_1["raw_chem_name"]=table_4_1.iloc[:,1]
table_4_1["raw_cas"]=table_4_1.iloc[:,4]
table_4_1=table_4_1[["raw_chem_name", "raw_cas"]]
table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!= "Systematic name"]
table_4_1=table_4_1.dropna(how="all")
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1)):
    table_4_1["raw_chem_name"].iloc[i]=table_4_1["raw_chem_name"].iloc[i].lower().strip()
    table_4_1["raw_chem_name"].iloc[i]=clean(table_4_1["raw_chem_name"].iloc[i])
    if len(table_4_1["raw_chem_name"].iloc[i].split())>1:
        table_4_1["raw_chem_name"].iloc[i]=" ".join(table_4_1["raw_chem_name"].iloc[i].split())

table_4_1["data_document_id"]="1372204"
table_4_1["data_document_filename"]="DCPS_68_a.pdf"
table_4_1["doc_date"]="2006"
table_4_1["raw_category"]=""
table_4_1["cat_code"]=""
table_4_1["description_cpcat"]=""
table_4_1["cpcat_code"]=""
table_4_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1.to_csv("DCPS_68_table_4_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
