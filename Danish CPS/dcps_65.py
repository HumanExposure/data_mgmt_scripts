#lkoval
#6-4-19

from tabula import read_pdf
import pandas as pd
import string

#Table 1
table_1=read_pdf("document_1372429.pdf", pages="25-27", lattice=True, pandas_options={'header': None})
table_1["raw_chem_name"]=table_1.iloc[:,1]
table_1=table_1.dropna(subset=["raw_chem_name"])
table_1=table_1.loc[table_1["raw_chem_name"]!="Name"]
table_1=table_1.reset_index()
table_1=table_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1)):
    table_1["raw_chem_name"].iloc[j]=str(table_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('α',"alpha")
    table_1["raw_chem_name"].iloc[j]=clean(str(table_1["raw_chem_name"].iloc[j]))

table_1=table_1.drop_duplicates()
table_1=table_1.reset_index()
table_1=table_1[["raw_chem_name"]]
table_1=table_1.iloc[:65]

nd=["ruthenium","palladium","tellurium","osmium","iridium","platinum","gold","mercury","uranium"]
for chem in nd:
    table_1=table_1.loc[table_1["raw_chem_name"]!=chem]

table_1=table_1.reset_index()
table_1=table_1[["raw_chem_name"]]

table_1["data_document_id"]="1372429"
table_1["data_document_filename"]="document_1359476_a.pdf"
table_1["doc_date"]="2005"
table_1["raw_category"]=""
table_1["cat_code"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_1.to_csv("dcps_65_table_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4
table_4=read_pdf("document_1372429.pdf", pages="30,31", lattice=True, pandas_options={'header': None})
table_4["raw_chem_name"]=table_4.iloc[:,1]
table_4=table_4.dropna(subset=["raw_chem_name"])
table_4=table_4.loc[table_4["raw_chem_name"]!="Name"]
table_4=table_4.reset_index()
table_4=table_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('α',"alpha")
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))

table_4=table_4.drop_duplicates()
table_4=table_4.reset_index()
table_4=table_4[["raw_chem_name"]]
table_4=table_4.iloc[:65]

nd=["beryllium","ruthenium","palladium","indium","tellurium","thulium","lutetium","hafnium","osmium","iridium","platinum","gold","mercury","uranium"]
for chem in nd:
    table_4=table_4.loc[table_4["raw_chem_name"]!=chem]

table_4=table_4.reset_index()
table_4=table_4[["raw_chem_name"]]

table_4["data_document_id"]="1372430"
table_4["data_document_filename"]="document_1359476_b.pdf"
table_4["doc_date"]="2005"
table_4["raw_category"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4.to_csv("dcps_65_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
