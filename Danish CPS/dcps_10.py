#lkoval
#5-20-19

from tabula import read_pdf
import pandas as pd
import string


table_p58=read_pdf("document_1372859.pdf", pages="58-65", lattice=True, pandas_options={'header': None})
table_p58["raw_cas"]=table_p58.iloc[:,3]
table_p58["raw_chem_name"]=table_p58.iloc[:,2]
table_p58=table_p58.loc[table_p58["raw_cas"]!= "CAS number"]
table_p58=table_p58.loc[table_p58["raw_cas"]!= "-"]
table_p58=table_p58.loc[table_p58["raw_chem_name"]!= ""]
table_p58=table_p58.reset_index()
table_p58=table_p58[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p58)):
    table_p58["raw_chem_name"].iloc[j]=str(table_p58["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_p58["raw_chem_name"].iloc[j]=clean(str(table_p58["raw_chem_name"].iloc[j]))
    if len(table_p58["raw_chem_name"].iloc[j].split())>1:
        table_p58["raw_chem_name"].iloc[j]=" ".join(table_p58["raw_chem_name"].iloc[j].split())
    if len(table_p58["raw_cas"].iloc[j].split())>1:
        table_p58["raw_cas"].iloc[j]=", ".join(table_p58["raw_cas"].iloc[j].split())
        table_p58["raw_cas"].iloc[j]=table_p58["raw_cas"].iloc[j].replace(" /,","")

table_p58["data_document_id"]="1372859"
table_p58["data_document_filename"]="document_1359396.pdf"
table_p58["doc_date"]="2002"
table_p58["raw_category"]=""
table_p58["cat_code"]=""
table_p58["description_cpcat"]=""
table_p58["cpcat_code"]=""
table_p58["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p58.to_csv("dcps_10_table_p58.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
