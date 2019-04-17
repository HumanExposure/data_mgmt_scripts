from tabula import read_pdf
import pandas as pd
import string


#Table 4.2 Extraction

table=read_pdf("document_1372162.pdf", pages="9",  lattice=True, pandas_options={'header': None})

table=table.iloc[:,0:2]
table.columns=["raw_chem_name", "raw_cas"]
table=table.loc[table["raw_cas"]!= "CAS no."]
table=table.dropna(how="all")
table=table.reset_index()
table=table.drop(columns="index")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table)):
    table["raw_chem_name"].iloc[i]=clean(table["raw_chem_name"].iloc[i])
    table["raw_chem_name"].iloc[i]=table["raw_chem_name"].iloc[i].replace(",", "_")
    table["raw_chem_name"].iloc[i]=table["raw_chem_name"].iloc[i].strip().lower()
    if len(table["raw_chem_name"].iloc[i].split()) > 1:
        table["raw_chem_name"].iloc[i]=" ".join(table["raw_chem_name"].iloc[i].split())
    if table["raw_chem_name"].iloc[i].endswith("*"):
        table["raw_chem_name"].iloc[i]=table["raw_chem_name"].iloc[i][:-1]

table["data_document_id"]="1372162"
table["data_document_filename"]="DCPS_30_a.pdf"
table["doc_date"]="2003"
table["raw_category"]="raw category"
table["cat_code"]="ACToR Assay"
table["description_cpcat"]="cpcat description"
table["cpcat_code"]="cpcat code"
table["cpcat_sourcetype"]="ACToR Assays and Lists"

table.to_csv("dcps_30_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
