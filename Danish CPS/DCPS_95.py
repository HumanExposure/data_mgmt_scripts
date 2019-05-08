#lkoval
#5-8-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.6
table_3_6=read_pdf("document_1372279.pdf", pages="20", lattice=True, pandas_options={'header': None})
table_3_6["raw_cas"]=table_3_6.iloc[:,1]
table_3_6["raw_chem_name"]=table_3_6.iloc[:,0]
table_3_6=table_3_6.loc[table_3_6["raw_chem_name"]!= "Ingredients"]
table_3_6=table_3_6.reset_index()
table_3_6=table_3_6[["raw_chem_name","raw_cas"]]
table_3_6=table_3_6.dropna(how="all")
table_3_6=table_3_6.reset_index()
table_3_6=table_3_6[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_3_6)):
    table_3_6["raw_chem_name"].iloc[i]=clean(str(table_3_6["raw_chem_name"].iloc[i]))
    table_3_6["raw_chem_name"].iloc[i]=str(table_3_6["raw_chem_name"].iloc[i]).strip().lower()
    if len(table_3_6["raw_chem_name"].iloc[i].split())>1:
        table_3_6["raw_chem_name"].iloc[i]=" ".join(table_3_6["raw_chem_name"].iloc[i].split())

table_3_6["data_document_id"]="1372279"
table_3_6["data_document_filename"]="DCPS_95_a.pdf"
table_3_6["doc_date"]="2008"
table_3_6["raw_category"]=""
table_3_6["cat_code"]=""
table_3_6["description_cpcat"]=""
table_3_6["cpcat_code"]=""
table_3_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_6.to_csv("dcps_95_table_3_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.7
table_3_7=read_pdf("document_1372280.pdf", pages="21", lattice=True, pandas_options={'header': None})
table_3_7["raw_cas"]=table_3_7.iloc[:,1]
table_3_7["raw_chem_name"]=table_3_7.iloc[:,0]
table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!= "Ingredients"]
table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name","raw_cas"]]
table_3_7=table_3_7.dropna(how="all")
table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_3_7)):
    table_3_7["raw_chem_name"].iloc[i]=clean(str(table_3_7["raw_chem_name"].iloc[i]))
    table_3_7["raw_chem_name"].iloc[i]=str(table_3_7["raw_chem_name"].iloc[i]).strip().lower()
    if len(table_3_7["raw_chem_name"].iloc[i].split())>1:
        table_3_7["raw_chem_name"].iloc[i]=" ".join(table_3_7["raw_chem_name"].iloc[i].split())

table_3_7["data_document_id"]="1372280"
table_3_7["data_document_filename"]="DCPS_95_b.pdf"
table_3_7["doc_date"]="2008"
table_3_7["raw_category"]=""
table_3_7["cat_code"]=""
table_3_7["description_cpcat"]=""
table_3_7["cpcat_code"]=""
table_3_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_7.to_csv("dcps_95_table_3_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.4
table_4_4=read_pdf("document_1372281.pdf", pages="27", lattice=True, pandas_options={'header': None})
table_4_4["raw_cas"]=table_4_4.iloc[:12,1]
table_4_4["raw_chem_name"]=table_4_4.iloc[:12,0]
table_4_4=table_4_4.loc[table_4_4["raw_chem_name"]!= "Ingredients"]
table_4_4=table_4_4.reset_index()
table_4_4=table_4_4[["raw_chem_name","raw_cas"]]
table_4_4=table_4_4.dropna(how="all")
table_4_4=table_4_4.reset_index()
table_4_4=table_4_4[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_4)):
    table_4_4["raw_chem_name"].iloc[i]=clean(str(table_4_4["raw_chem_name"].iloc[i]))
    table_4_4["raw_chem_name"].iloc[i]=str(table_4_4["raw_chem_name"].iloc[i]).strip().lower()
    if len(table_4_4["raw_chem_name"].iloc[i].split())>1:
        table_4_4["raw_chem_name"].iloc[i]=" ".join(table_4_4["raw_chem_name"].iloc[i].split())
    if len(str(table_4_4["raw_cas"].iloc[i]).split())>1:
        table_4_4["raw_cas"].iloc[i]=" ".join(table_4_4["raw_cas"].iloc[i].split())

table_4_4["data_document_id"]="1372281"
table_4_4["data_document_filename"]="DCPS_95_c.pdf"
table_4_4["doc_date"]="2008"
table_4_4["raw_category"]=""
table_4_4["cat_code"]=""
table_4_4["description_cpcat"]=""
table_4_4["cpcat_code"]=""
table_4_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_4.to_csv("dcps_95_table_4_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.5
tables=read_pdf("document_1372282.pdf", pages="28", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_5=tables[0]
table_4_5["raw_cas"]=table_4_5.iloc[:,1]
table_4_5["raw_chem_name"]=table_4_5.iloc[:,0]
table_4_5=table_4_5.loc[table_4_5["raw_chem_name"]!= "Ingredients"]
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name","raw_cas"]]
table_4_5=table_4_5.dropna(how="all")
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_5)):
    table_4_5["raw_chem_name"].iloc[i]=clean(str(table_4_5["raw_chem_name"].iloc[i]))
    table_4_5["raw_chem_name"].iloc[i]=str(table_4_5["raw_chem_name"].iloc[i]).strip().lower()
    if len(table_4_5["raw_chem_name"].iloc[i].split())>1:
        table_4_5["raw_chem_name"].iloc[i]=" ".join(table_4_5["raw_chem_name"].iloc[i].split())
    if len(str(table_4_5["raw_cas"].iloc[i]).split())>1:
        table_4_5["raw_cas"].iloc[i]=" ".join(table_4_5["raw_cas"].iloc[i].split())

table_4_5["data_document_id"]="1372282"
table_4_5["data_document_filename"]="DCPS_95_d.pdf"
table_4_5["doc_date"]="2008"
table_4_5["raw_category"]=""
table_4_5["cat_code"]=""
table_4_5["description_cpcat"]=""
table_4_5["cpcat_code"]=""
table_4_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_5.to_csv("dcps_95_table_4_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.6
tables=read_pdf("document_1372283.pdf", pages="28", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_6=tables[8]
table_4_6["raw_cas"]=table_4_6.iloc[:,1]
table_4_6["raw_chem_name"]=table_4_6.iloc[:,0]
table_4_6=table_4_6.loc[table_4_6["raw_chem_name"]!= "Ingredients"]
table_4_6=table_4_6.reset_index()
table_4_6=table_4_6[["raw_chem_name","raw_cas"]]
table_4_6=table_4_6.dropna(how="all")
table_4_6=table_4_6.reset_index()
table_4_6=table_4_6[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_6)):
    table_4_6["raw_chem_name"].iloc[i]=clean(str(table_4_6["raw_chem_name"].iloc[i]))
    table_4_6["raw_chem_name"].iloc[i]=str(table_4_6["raw_chem_name"].iloc[i]).strip().lower()
    if len(table_4_6["raw_chem_name"].iloc[i].split())>1:
        table_4_6["raw_chem_name"].iloc[i]=" ".join(table_4_6["raw_chem_name"].iloc[i].split())
    if len(str(table_4_6["raw_cas"].iloc[i]).split())>1:
        table_4_6["raw_cas"].iloc[i]=" ".join(table_4_6["raw_cas"].iloc[i].split())

table_4_6["data_document_id"]="1372283"
table_4_6["data_document_filename"]="DCPS_95_e.pdf"
table_4_6["doc_date"]="2008"
table_4_6["raw_category"]=""
table_4_6["cat_code"]=""
table_4_6["description_cpcat"]=""
table_4_6["cpcat_code"]=""
table_4_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_6.to_csv("dcps_95_table_4_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
