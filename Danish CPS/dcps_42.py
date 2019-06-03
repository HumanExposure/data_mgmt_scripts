#lkoval
#6-3-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.2
table_3_2=read_pdf("document_1372511.pdf", pages="27,28", lattice=True, pandas_options={'header': None})
table_3_2["raw_chem_name"]=table_3_2.iloc[:,1]
table_3_2["raw_cas"]=table_3_2.iloc[:,2]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!="Toothbrush ID"]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!="Anal. ID (30642-)"]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!="Compound"]
table_3_2=table_3_2.dropna(subset=["raw_chem_name"])
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(table_3_2["raw_chem_name"].iloc[j].split())>1:
        table_3_2["raw_chem_name"].iloc[j]=" ".join(table_3_2["raw_chem_name"].iloc[j].split())
    if len(str(table_3_2["raw_cas"].iloc[j]).split())>1:
        table_3_2["raw_cas"].iloc[j]="".join(str(table_3_2["raw_cas"].iloc[j]).split())

table_3_2["data_document_id"]="1372511"
table_3_2["data_document_filename"]="DCPS_42_a.pdf"
table_3_2["doc_date"]="2004"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_42_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.3
table_3_3=read_pdf("document_1372512.pdf", pages="30", lattice=True, pandas_options={'header': None})
table_3_3["raw_chem_name"]=table_3_3.iloc[2:16,0]
table_3_3=table_3_3.dropna(subset=["raw_chem_name"])
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[j]=str(table_3_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_3_3["raw_chem_name"].iloc[j]=clean(str(table_3_3["raw_chem_name"].iloc[j]))

table_3_3["data_document_id"]="1372512"
table_3_3["data_document_filename"]="DCPS_42_b.pdf"
table_3_3["doc_date"]="2004"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("dcps_42_table_3_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.1
table_5_1=read_pdf("document_1372513.pdf", pages="37", lattice=True, pandas_options={'header': None})
table_5_1["raw_chem_name"]=table_5_1.iloc[2:,0]
table_5_1=table_5_1.dropna(subset=["raw_chem_name"])
table_5_1=table_5_1.reset_index()
table_5_1=table_5_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_1)):
    table_5_1["raw_chem_name"].iloc[j]=str(table_5_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('\"',"")
    table_5_1["raw_chem_name"].iloc[j]=clean(str(table_5_1["raw_chem_name"].iloc[j]))

table_5_1["data_document_id"]="1372513"
table_5_1["data_document_filename"]="DCPS_42_c.pdf"
table_5_1["doc_date"]="2004"
table_5_1["raw_category"]=""
table_5_1["cat_code"]=""
table_5_1["description_cpcat"]=""
table_5_1["cpcat_code"]=""
table_5_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_1.to_csv("dcps_42_table_5_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
