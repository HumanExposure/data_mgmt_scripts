#lkoval
#5/23/19

from tabula import read_pdf
import pandas as pd
import string

#Table 5.5.1
table_5_5_1=read_pdf("document_1372756.pdf", pages="15,16", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_5_5_1["raw_chem_name"]=table_5_5_1.iloc[:,2]
table_5_5_1["raw_cas"]=table_5_5_1.iloc[:,1]
table_5_5_1=table_5_5_1.loc[table_5_5_1["raw_chem_name"]!= "Chemical name"]
table_5_5_1=table_5_5_1.reset_index()
table_5_5_1=table_5_5_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_5_1)):
    table_5_5_1["raw_chem_name"].iloc[j]=str(table_5_5_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("#","").replace("^","")
    table_5_5_1["raw_chem_name"].iloc[j]=clean(str(table_5_5_1["raw_chem_name"].iloc[j]))
    if len(table_5_5_1["raw_chem_name"].iloc[j].split())>1:
        table_5_5_1["raw_chem_name"].iloc[j]=" ".join(table_5_5_1["raw_chem_name"].iloc[j].split())

table_5_5_1=table_5_5_1.drop_duplicates()
table_5_5_1=table_5_5_1.reset_index()
table_5_5_1=table_5_5_1[["raw_chem_name","raw_cas"]]

table_5_5_1["data_document_id"]="1372756"
table_5_5_1["data_document_filename"]="document_1359424.pdf"
table_5_5_1["doc_date"]="2002"
table_5_5_1["raw_category"]=""
table_5_5_1["cat_code"]=""
table_5_5_1["description_cpcat"]=""
table_5_5_1["cpcat_code"]=""
table_5_5_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_5_1.to_csv("dcps_2_table_5_5_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
