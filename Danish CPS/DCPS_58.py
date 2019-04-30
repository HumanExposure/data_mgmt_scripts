#lkoval
#4-30-19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 3 & 5 as pandas dfs using tabula

#Table 3
table_3=read_pdf("document_1372202.pdf", pages="19,20", lattice=True, pandas_options={'header': None})
table_3["raw_chem_name"]=table_3.iloc[:,0]
table_3=table_3.dropna(subset=["raw_chem_name"])
table_3=table_3.reset_index()
table_3=table_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3)):
    table_3["raw_chem_name"].iloc[i]=table_3["raw_chem_name"].iloc[i].lower().strip()
    table_3["raw_chem_name"].iloc[i]=clean(table_3["raw_chem_name"].iloc[i])
    if len(table_3["raw_chem_name"].iloc[i].split())>1:
        table_3["raw_chem_name"].iloc[i]=" ".join(table_3["raw_chem_name"].iloc[i].split())

table_3=table_3.drop_duplicates()
table_3=table_3[["raw_chem_name"]]

table_3["data_document_id"]="1372202"
table_3["data_document_filename"]="DCPS_58_a.pdf"
table_3["doc_date"]="2005"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3.to_csv("DCPS_58_table_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5
table_5=read_pdf("document_1372203.pdf", pages="24,25", lattice=True, pandas_options={'header': None})
table_5["raw_chem_name"]=table_5.iloc[:,0]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5.loc[table_5["raw_chem_name"] != "Sum of other grouped compounds:"]
table_5=table_5.reset_index()
table_5=table_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_5)):
    table_5["raw_chem_name"].iloc[i]=clean(table_5["raw_chem_name"].iloc[i])
    table_5["raw_chem_name"].iloc[i]=table_5["raw_chem_name"].iloc[i].lower().strip().strip("*").replace("#","")
    if len(table_5["raw_chem_name"].iloc[i].split())>1:
        table_5["raw_chem_name"].iloc[i]=" ".join(table_5["raw_chem_name"].iloc[i].split())


table_5["data_document_id"]="1372203"
table_5["data_document_filename"]="DCPS_58_b.pdf"
table_5["doc_date"]="2005"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5.to_csv("DCPS_58_table_5.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
