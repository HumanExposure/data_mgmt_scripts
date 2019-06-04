#lkoval
#6-4-19

from tabula import read_pdf
import pandas as pd
import string

#Table 2.3
table_2_3=read_pdf("document_1372409.pdf", pages="25", lattice=True, pandas_options={'header': None})
table_2_3["raw_chem_name"]=table_2_3.iloc[1:7,0]
table_2_3["raw_cas"]=table_2_3.iloc[1:7,1]
table_2_3=table_2_3.dropna(subset=["raw_chem_name"])
table_2_3=table_2_3.reset_index()
table_2_3=table_2_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))

table_2_3["data_document_id"]="1372409"
table_2_3["data_document_filename"]="document_1359485_a.pdf"
table_2_3["doc_date"]="2006"
table_2_3["raw_category"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_3.to_csv("dcps_70_table_2_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 2.4
tables=read_pdf("document_1372410.pdf", pages="26", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_4=tables[0]
table_2_4["raw_chem_name"]=table_2_4.iloc[1:11,0]
table_2_4["raw_cas"]=table_2_4.iloc[1:11,1]
table_2_4=table_2_4.dropna(subset=["raw_chem_name"])
table_2_4=table_2_4.reset_index()
table_2_4=table_2_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(str(table_2_4["raw_chem_name"].iloc[j]).split())>1:
        table_2_4["raw_chem_name"].iloc[j]="".join(str(table_2_4["raw_chem_name"].iloc[j]).split())


table_2_4["data_document_id"]="1372410"
table_2_4["data_document_filename"]="document_1359485_b.pdf"
table_2_4["doc_date"]="2006"
table_2_4["raw_category"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_4.to_csv("dcps_70_table_2_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 2.5
tables=read_pdf("document_1372411.pdf", pages="26", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_5=tables[1]
table_2_5["raw_chem_name"]=table_2_5.iloc[1:3,0]
table_2_5["raw_cas"]=table_2_5.iloc[1:3,1]
table_2_5=table_2_5.dropna(subset=["raw_chem_name"])
table_2_5=table_2_5.reset_index()
table_2_5=table_2_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[j]=str(table_2_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_2_5["raw_chem_name"].iloc[j]=clean(str(table_2_5["raw_chem_name"].iloc[j]))
    if len(str(table_2_5["raw_cas"].iloc[j]).split())>1:
        table_2_5["raw_cas"].iloc[j]="".join(str(table_2_5["raw_cas"].iloc[j]).split())


table_2_5["data_document_id"]="1372411"
table_2_5["data_document_filename"]="document_1359485_c.pdf"
table_2_5["doc_date"]="2006"
table_2_5["raw_category"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_5.to_csv("dcps_70_table_2_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 2.7
tables=read_pdf("document_1372412.pdf", pages="27", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_7=tables[1]
table_2_7["raw_chem_name"]=table_2_7.iloc[1:,0]
table_2_7["raw_cas"]=table_2_7.iloc[1:,1]
table_2_7=table_2_7.dropna(subset=["raw_chem_name"])
table_2_7=table_2_7.reset_index()
table_2_7=table_2_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_7)):
    table_2_7["raw_chem_name"].iloc[j]=str(table_2_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_2_7["raw_chem_name"].iloc[j]=clean(str(table_2_7["raw_chem_name"].iloc[j]))
    if len(str(table_2_7["raw_cas"].iloc[j]).split())>1:
        table_2_7["raw_cas"].iloc[j]="".join(str(table_2_7["raw_cas"].iloc[j]).split())


table_2_7["data_document_id"]="1372412"
table_2_7["data_document_filename"]="document_1359485_d.pdf"
table_2_7["doc_date"]="2006"
table_2_7["raw_category"]=""
table_2_7["cat_code"]=""
table_2_7["description_cpcat"]=""
table_2_7["cpcat_code"]=""
table_2_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_7.to_csv("dcps_70_table_2_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
