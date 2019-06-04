#lkoval
#6-4-19

from tabula import read_pdf
import pandas as pd
import string

#Table 1.1
table_1_1=read_pdf("document_1372589.pdf", pages="13", lattice=True, pandas_options={'header': None})
table_1_1["raw_chem_name"]=table_1_1.iloc[:-1,0]
table_1_1=table_1_1.dropna(subset=["raw_chem_name"])
table_1_1=table_1_1.reset_index()
table_1_1=table_1_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1_1)):
    table_1_1["raw_chem_name"].iloc[j]=str(table_1_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_1_1["raw_chem_name"].iloc[j]=clean(str(table_1_1["raw_chem_name"].iloc[j]))
    if len(table_1_1["raw_chem_name"].iloc[j].split())>1:
        table_1_1["raw_chem_name"].iloc[j]=" ".join(table_1_1["raw_chem_name"].iloc[j].split())

table_1_1["data_document_id"]="1372589"
table_1_1["data_document_filename"]="DCPS_54_d.pdf"
table_1_1["doc_date"]="2005"
table_1_1["raw_category"]=""
table_1_1["cat_code"]=""
table_1_1["description_cpcat"]=""
table_1_1["cpcat_code"]=""
table_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_1_1.to_csv("dcps_54_table_1_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1
table_3_1=read_pdf("document_1372590.pdf", pages="23", lattice=True, pandas_options={'header': None})
table_3_1["raw_chem_name"]=table_3_1.iloc[1:,0]
table_3_1=table_3_1.dropna(subset=["raw_chem_name"])
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[j]=str(table_3_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_3_1["raw_chem_name"].iloc[j]=clean(str(table_3_1["raw_chem_name"].iloc[j]))

table_3_1["data_document_id"]="1372590"
table_3_1["data_document_filename"]="DCPS_54_e.pdf"
table_3_1["doc_date"]="2005"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1.to_csv("dcps_54_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.3
tables=read_pdf("document_1372591.pdf", pages="26", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_3=tables[0]
table_3_3["raw_chem_name"]=table_3_3.iloc[1:,0]
table_3_3=table_3_3.dropna(subset=["raw_chem_name"])
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[j]=str(table_3_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_3_3["raw_chem_name"].iloc[j]=clean(str(table_3_3["raw_chem_name"].iloc[j]))
    if table_3_3["raw_chem_name"].iloc[j][-1]=="a":
        table_3_3["raw_chem_name"].iloc[j]=table_3_3["raw_chem_name"].iloc[j][:-1]

table_3_3["data_document_id"]="1372591"
table_3_3["data_document_filename"]="DCPS_54_f.pdf"
table_3_3["doc_date"]="2005"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("dcps_54_table_3_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 3.7
table_3_7=read_pdf("document_1372592.pdf", pages="30", lattice=True, pandas_options={'header': None})
table_3_7["raw_chem_name"]=table_3_7.iloc[1:,0]
table_3_7=table_3_7.dropna(subset=["raw_chem_name"])
table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_7)):
    table_3_7["raw_chem_name"].iloc[j]=str(table_3_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_3_7["raw_chem_name"].iloc[j]=clean(str(table_3_7["raw_chem_name"].iloc[j]))

table_3_7["data_document_id"]="1372592"
table_3_7["data_document_filename"]="DCPS_54_g.pdf"
table_3_7["doc_date"]="2005"
table_3_7["raw_category"]=""
table_3_7["cat_code"]=""
table_3_7["description_cpcat"]=""
table_3_7["cpcat_code"]=""
table_3_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_7.to_csv("dcps_54_table_3_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
