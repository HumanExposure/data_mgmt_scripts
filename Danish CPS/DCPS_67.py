from tabula import read_pdf
import pandas as pd
import string

#Read in tables 3.2, 3.3, 4.1 & 4.2 as pandas dfs using tabula

#Table 3.2
table_3_2=read_pdf("document_1372191.pdf", pages="31,32", lattice=True, pandas_options={'header': None})
table_3_2=table_3_2.iloc[:, :2]
table_3_2=table_3_2.dropna(how="all")
table_3_2.columns=["raw_chem_name", "raw_cas"]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!= "Component"]
table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i].lower().strip()
    table_3_2["raw_chem_name"].iloc[i]=clean(table_3_2["raw_chem_name"].iloc[i])
    if len(table_3_2["raw_chem_name"].iloc[i].split())>1:
        table_3_2["raw_chem_name"].iloc[i]=" ".join(table_3_2["raw_chem_name"].iloc[i].split())
    if len(str(table_3_2["raw_cas"].iloc[i]).split())>1:
        table_3_2["raw_cas"].iloc[i]="".join(str(table_3_2["raw_cas"].iloc[i]).split())

table_3_2["data_document_id"]="1372191"
table_3_2["data_document_filename"]="DCPS_67_a.pdf"
table_3_2["doc_date"]="2005"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("DCPS_67_table_3_2.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.3
table_3_3=read_pdf("document_1372192.pdf", pages="35,36", lattice=True, pandas_options={'header': None})
table_3_3=table_3_3.iloc[:, :2]
table_3_3=table_3_3.dropna(how="all")
table_3_3.columns=["raw_chem_name", "raw_cas"]
table_3_3=table_3_3.loc[table_3_3["raw_chem_name"]!= "Component"]
table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i].lower().strip()
    table_3_3["raw_chem_name"].iloc[i]=clean(table_3_3["raw_chem_name"].iloc[i])
    if len(table_3_3["raw_chem_name"].iloc[i].split())>1:
        table_3_3["raw_chem_name"].iloc[i]=" ".join(table_3_3["raw_chem_name"].iloc[i].split())
    if len(str(table_3_3["raw_cas"].iloc[i]).split())>1:
        table_3_3["raw_cas"].iloc[i]="".join(str(table_3_3["raw_cas"].iloc[i]).split())

table_3_3=table_3_3.drop_duplicates()
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]

table_3_3["data_document_id"]="1372192"
table_3_3["data_document_filename"]="DCPS_67_b.pdf"
table_3_3["doc_date"]="2005"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("DCPS_67_table_3_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



#Table 4.1
table_4_1=read_pdf("document_1372193.pdf", pages="40-43", lattice=True, pandas_options={'header': None})
table_4_1=table_4_1.iloc[:, :2]
table_4_1=table_4_1.dropna(how="all")
table_4_1.columns=["raw_chem_name", "raw_cas"]
table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!= "Component"]
table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1)):
    table_4_1["raw_chem_name"].iloc[i]=table_4_1["raw_chem_name"].iloc[i].lower().strip()
    table_4_1["raw_chem_name"].iloc[i]=clean(table_4_1["raw_chem_name"].iloc[i])
    if len(table_4_1["raw_chem_name"].iloc[i].split())>1:
        table_4_1["raw_chem_name"].iloc[i]=" ".join(table_4_1["raw_chem_name"].iloc[i].split())
    if len(str(table_4_1["raw_cas"].iloc[i]).split())>1:
        table_4_1["raw_cas"].iloc[i]="".join(str(table_4_1["raw_cas"].iloc[i]).split())

table_4_1["data_document_id"]="1372193"
table_4_1["data_document_filename"]="DCPS_67_c.pdf"
table_4_1["doc_date"]="2005"
table_4_1["raw_category"]=""
table_4_1["cat_code"]=""
table_4_1["description_cpcat"]=""
table_4_1["cpcat_code"]=""
table_4_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1.to_csv("DCPS_67_table_4_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.2
table_4_2=read_pdf("document_1372194.pdf", pages="51,52", lattice=True, pandas_options={'header': None})
table_4_2=table_4_2.iloc[:, :2]
table_4_2=table_4_2.dropna(how="all")
table_4_2.columns=["raw_chem_name", "raw_cas"]
table_4_2=table_4_2.loc[table_4_2["raw_chem_name"]!= "Component"]
table_4_2.reset_index()
table_4_2=table_4_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_2)):
    table_4_2["raw_chem_name"].iloc[i]=table_4_2["raw_chem_name"].iloc[i].lower().strip()
    table_4_2["raw_chem_name"].iloc[i]=clean(table_4_2["raw_chem_name"].iloc[i])
    if len(table_4_2["raw_chem_name"].iloc[i].split())>1:
        table_4_2["raw_chem_name"].iloc[i]=" ".join(table_4_2["raw_chem_name"].iloc[i].split())
    if len(str(table_4_2["raw_cas"].iloc[i]).split())>1:
        table_4_2["raw_cas"].iloc[i]="".join(str(table_4_2["raw_cas"].iloc[i]).split())

table_4_2["data_document_id"]="1372194"
table_4_2["data_document_filename"]="DCPS_67_d.pdf"
table_4_2["doc_date"]="2005"
table_4_2["raw_category"]=""
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_2.to_csv("DCPS_67_table_4_2.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
