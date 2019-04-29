#Lauren Koval
#4/29/19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 4.3, 4.4, 4.5 as pandas dfs using tabula

#Table 4.3
tables=read_pdf("document_1372187.pdf", pages="18,19", lattice=True, multiple_tables= True, pandas_options={'header': None})

table_4_3=pd.concat([tables[0],tables[1]], ignore_index=True)
table_4_3=table_4_3.iloc[:,:2]
table_4_3.columns=["raw_chem_name","raw_cas"]
table_4_3=table_4_3.loc[table_4_3["raw_chem_name"]!="INCI"]
table_4_3=table_4_3.reset_index()
table_4_3=table_4_3[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_3)):
    table_4_3["raw_chem_name"].iloc[i]=table_4_3["raw_chem_name"].iloc[i].lower().strip().strip("*")
    table_4_3["raw_chem_name"].iloc[i]=clean(table_4_3["raw_chem_name"].iloc[i])

table_4_3["data_document_id"]="1372187"
table_4_3["data_document_filename"]="DCPS_69_a.pdf"
table_4_3["doc_date"]="2006"
table_4_3["raw_category"]=""
table_4_3["cat_code"]=""
table_4_3["description_cpcat"]=""
table_4_3["cpcat_code"]=""
table_4_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_3.to_csv("DCPS_69_table_4_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.4
tables=read_pdf("document_1372188.pdf", pages="19", lattice=True, multiple_tables= True, pandas_options={'header': None})

table_4_4=tables[1]
table_4_4=table_4_4.iloc[:,:2]
table_4_4.columns=["raw_chem_name","raw_cas"]
table_4_4=table_4_4.loc[table_4_4["raw_chem_name"]!="INCI"]
table_4_4=table_4_4.reset_index()
table_4_4=table_4_4[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_4)):
    table_4_4["raw_chem_name"].iloc[i]=table_4_4["raw_chem_name"].iloc[i].lower().strip().strip("*")
    table_4_4["raw_chem_name"].iloc[i]=clean(table_4_4["raw_chem_name"].iloc[i])

table_4_4["data_document_id"]="1372188"
table_4_4["data_document_filename"]="DCPS_69_b.pdf"
table_4_4["doc_date"]="2006"
table_4_4["raw_category"]=""
table_4_4["cat_code"]=""
table_4_4["description_cpcat"]=""
table_4_4["cpcat_code"]=""
table_4_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_4.to_csv("DCPS_69_table_4_4.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.5
table_4_5=read_pdf("document_1372189.pdf", pages="20", lattice=True, pandas_options={'header': None})
table_4_5=table_4_5.iloc[:,:2]
table_4_5.columns=["raw_chem_name","raw_cas"]
table_4_5=table_4_5.loc[table_4_5["raw_chem_name"]!="INCI"]
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_5)):
    table_4_5["raw_chem_name"].iloc[i]=table_4_5["raw_chem_name"].iloc[i].lower().strip()
    table_4_5["raw_chem_name"].iloc[i]=clean(table_4_5["raw_chem_name"].iloc[i])
    if len(table_4_5["raw_chem_name"].iloc[i].split())>1:
        table_4_5["raw_chem_name"].iloc[i]=" ".join(table_4_5["raw_chem_name"].iloc[i].split())


table_4_5["data_document_id"]="1372189"
table_4_5["data_document_filename"]="DCPS_69_c.pdf"
table_4_5["doc_date"]="2006"
table_4_5["raw_category"]=""
table_4_5["cat_code"]=""
table_4_5["description_cpcat"]=""
table_4_5["cpcat_code"]=""
table_4_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_5.to_csv("DCPS_69_table_4_5.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
