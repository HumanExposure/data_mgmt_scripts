#lkoval
#4-29-19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 1 & 3 as pandas dfs using tabula

#Table 1
table_1=read_pdf("document_1372200.pdf", pages="18-20", lattice=True, pandas_options={'header': None})
table_1=table_1.iloc[:,:2]
table_1.columns=["raw_chem_name","raw_cas"]
table_1=table_1.loc[table_1["raw_chem_name"]!="Name"]
table_1=table_1.loc[table_1["raw_chem_name"]!= "Sum of groups"]
table_1=table_1.dropna(how="all")
table_1=table_1.reset_index()
table_1=table_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_1)):
    table_1["raw_chem_name"].iloc[i]=table_1["raw_chem_name"].iloc[i].lower().strip().strip("#").strip("*")
    table_1["raw_chem_name"].iloc[i]=clean(table_1["raw_chem_name"].iloc[i])
    if len(table_1["raw_chem_name"].iloc[i].split())>1:
        table_1["raw_chem_name"].iloc[i]=" ".join(table_1["raw_chem_name"].iloc[i].split())
    if len(str(table_1["raw_cas"].iloc[i]).split())>1:
        table_1["raw_cas"].iloc[i]=" ".join(str(table_1["raw_cas"].iloc[i]).split())


table_1["data_document_id"]="1372200"
table_1["data_document_filename"]="DCPS_57_a.pdf"
table_1["doc_date"]="2005"
table_1["raw_category"]=""
table_1["cat_code"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_1.to_csv("DCPS_57_table_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3
table_3=read_pdf("document_1372201.pdf", pages="22-24", lattice=True, pandas_options={'header': None})
table_3=table_3.iloc[:,:2]
table_3.columns=["raw_chem_name","raw_cas"]
table_3=table_3.loc[table_3["raw_chem_name"]!="Name"]
table_3=table_3.loc[table_3["raw_chem_name"]!= "Metals"]
table_3=table_3.dropna(how="all")
table_3=table_3.reset_index()
table_3=table_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3)):
    table_3["raw_chem_name"].iloc[i]=table_3["raw_chem_name"].iloc[i].lower().strip().strip("#").strip("*")
    table_3["raw_chem_name"].iloc[i]=clean(table_3["raw_chem_name"].iloc[i])
    if len(table_3["raw_chem_name"].iloc[i].split())>1:
        table_3["raw_chem_name"].iloc[i]=" ".join(table_3["raw_chem_name"].iloc[i].split())
    if len(str(table_3["raw_cas"].iloc[i]).split())>1:
        table_3["raw_cas"].iloc[i]=" ".join(str(table_3["raw_cas"].iloc[i]).split())


table_3["data_document_id"]="1372201"
table_3["data_document_filename"]="DCPS_57_b.pdf"
table_3["doc_date"]="2005"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3.to_csv("DCPS_57_table_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
