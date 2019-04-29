from tabula import read_pdf
import pandas as pd
import string

#Read in table 4 as pandas dfs using tabula

#Table 4
table_4=read_pdf("document_1372190.pdf", pages="21-24", lattice=True, pandas_options={'header': None})
table_4=table_4.iloc[:, :2]
table_4.columns=["raw_chem_name","raw_cas"]
table_4=table_4.loc[table_4["raw_chem_name"]!= "Name"]
table_4.reset_index()
table_4=table_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4)):
    table_4["raw_chem_name"].iloc[i]=table_4["raw_chem_name"].iloc[i].lower().strip()
    table_4["raw_chem_name"].iloc[i]=clean(table_4["raw_chem_name"].iloc[i])
    if len(table_4["raw_chem_name"].iloc[i].split())>1:
        table_4["raw_chem_name"].iloc[i]=" ".join(table_4["raw_chem_name"].iloc[i].split())
    if len(str(table_4["raw_cas"].iloc[i]).split())>1:
        table_4["raw_cas"].iloc[i]="".join(str(table_4["raw_cas"].iloc[i]).split())

table_4["data_document_id"]="1372190"
table_4["data_document_filename"]="DCPS_60_a.pdf"
table_4["doc_date"]="2005"
table_4["raw_category"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4.to_csv("DCPS_60_table_4.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
