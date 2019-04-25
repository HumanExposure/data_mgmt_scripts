#Lauren Koval
#4/25/19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 5, 3.2.5, 17, & 18 as pandas dfs using tabula

#Table 5
tables=read_pdf("document_1372181.pdf", pages="21-23",  lattice=True, multiple_tables= True, pandas_options={'header': None})

table_5=pd.concat([tables[5],tables[6],tables[7],tables[8],tables[9],tables[10], tables[11], tables[12], tables[13], tables[14]], ignore_index=True)
table_5=table_5.iloc[:,:2]
table_5.columns=["raw_cas","raw_chem_name"]
table_5=table_5.loc[table_5["raw_cas"] != "CAS-no"]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5.reset_index()
table_5=table_5[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[i]=table_5["raw_chem_name"].iloc[i].strip().lower()
    table_5["raw_chem_name"].iloc[i]=clean(table_5["raw_chem_name"].iloc[i])
    table_5["raw_cas"].iloc[i]=clean(table_5["raw_cas"].iloc[i])
    if table_5["raw_chem_name"].iloc[i].endswith("1") or table_5["raw_chem_name"].iloc[i].endswith("2") or table_5["raw_chem_name"].iloc[i].endswith("3") or table_5["raw_chem_name"].iloc[i].endswith("4"):
        table_5["raw_chem_name"].iloc[i]=table_5["raw_chem_name"].iloc[i][:-1]

table_5["data_document_id"]="1372181"
table_5["data_document_filename"]="DCPS_52_a.pdf"
table_5["doc_date"]="2005"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5.to_csv("DCPS_52_table_5.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.2.5
tables=read_pdf("document_1372182.pdf", pages="25",  lattice=True,  pandas_options={'header': None})

table_3_2_5=tables
table_3_2_5=table_3_2_5.iloc[:,1:3]
table_3_2_5.columns=["raw_chem_name","raw_cas"]
table_3_2_5=table_3_2_5.loc[table_3_2_5["raw_cas"] != "CAS-no"]
table_3_2_5=table_3_2_5.reset_index()
table_3_2_5=table_3_2_5[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_3_2_5)):
    table_3_2_5["raw_chem_name"].iloc[i]=table_3_2_5["raw_chem_name"].iloc[i].strip().lower()
    table_3_2_5["raw_chem_name"].iloc[i]=clean(table_3_2_5["raw_chem_name"].iloc[i])
    table_3_2_5["raw_cas"].iloc[i]=clean(table_3_2_5["raw_cas"].iloc[i])
    if len(table_3_2_5["raw_chem_name"].iloc[i].split())>1:
        table_3_2_5["raw_chem_name"].iloc[i]=" ".join(table_3_2_5["raw_chem_name"].iloc[i].split())

table_3_2_5["data_document_id"]="1372182"
table_3_2_5["data_document_filename"]="DCPS_52_b.pdf"
table_3_2_5["doc_date"]="2005"
table_3_2_5["raw_category"]=""
table_3_2_5["cat_code"]=""
table_3_2_5["description_cpcat"]=""
table_3_2_5["cpcat_code"]=""
table_3_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2_5.to_csv("DCPS_52_table_3_2_5.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 17
tables=read_pdf("document_1372183.pdf", pages="42-43",  lattice=True, multiple_tables= True, pandas_options={'header': None})

table_17=pd.concat([tables[0],tables[1]], ignore_index=True)
table_17=table_17.iloc[:,:2]
table_17.columns=["raw_chem_name","raw_cas"]
table_17=table_17.loc[table_17["raw_cas"] != "CAS-no"]
table_17=table_17.dropna(how="all")
table_17=table_17.reset_index()
table_17=table_17[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_17)):
    table_17["raw_chem_name"].iloc[i]=table_17["raw_chem_name"].iloc[i].strip().lower().strip("*")
    table_17["raw_chem_name"].iloc[i]=clean(table_17["raw_chem_name"].iloc[i])
    table_17["raw_cas"].iloc[i]=clean(table_17["raw_cas"].iloc[i])
    if len(table_17["raw_chem_name"].iloc[i].split())>1:
        table_17["raw_chem_name"].iloc[i]=" ".join(table_17["raw_chem_name"].iloc[i].split())

table_17["data_document_id"]="1372183"
table_17["data_document_filename"]="DCPS_52_c.pdf"
table_17["doc_date"]="2005"
table_17["raw_category"]=""
table_17["cat_code"]=""
table_17["description_cpcat"]=""
table_17["cpcat_code"]=""
table_17["cpcat_sourcetype"]="ACToR Assays and Lists"

table_17.to_csv("DCPS_52_table_17.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 18
tables=read_pdf("document_1372184.pdf", pages="43,44",  lattice=True, multiple_tables= True, pandas_options={'header': None})

table_18=pd.concat([tables[1],tables[2]], ignore_index=True)
table_18=table_18.iloc[:,:2]
table_18.columns=["raw_chem_name","raw_cas"]
table_18=table_18.loc[table_18["raw_cas"] != "CAS-no"]
table_18=table_18.dropna(how="all")
table_18=table_18.reset_index()
table_18=table_18[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_18)):
    table_18["raw_chem_name"].iloc[i]=table_18["raw_chem_name"].iloc[i].strip().lower().strip("*")
    table_18["raw_chem_name"].iloc[i]=clean(table_18["raw_chem_name"].iloc[i])
    table_18["raw_cas"].iloc[i]=clean(table_18["raw_cas"].iloc[i])
    if len(table_18["raw_chem_name"].iloc[i].split())>1:
        table_18["raw_chem_name"].iloc[i]=" ".join(table_18["raw_chem_name"].iloc[i].split())
    if table_17["raw_chem_name"].iloc[i].endswith("2"):
        table_17["raw_chem_name"].iloc[i]=table_17["raw_chem_name"].iloc[i][:-1]


table_18["data_document_id"]="1372184"
table_18["data_document_filename"]="DCPS_52_d.pdf"
table_18["doc_date"]="2005"
table_18["raw_category"]=""
table_18["cat_code"]=""
table_18["description_cpcat"]=""
table_18["cpcat_code"]=""
table_18["cpcat_sourcetype"]="ACToR Assays and Lists"

table_18.to_csv("DCPS_52_table_18.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
