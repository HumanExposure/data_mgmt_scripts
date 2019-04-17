from tabula import read_pdf
import pandas as pd
import string

#read in tables 4.1.1.1, 4.1.1.2, 4.1.1.3, 4.1.1.5, 4.1.2.1, 4.1.2.2, 4.1.3.1 as pandas df using tabula and only keep the relevant ones

#Table 4.1.1.1 Extraction
table_4_1_1_1=read_pdf("document_1372163.pdf", pages="20", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_1_1=table_4_1_1_1[0]
table_4_1_1_1["raw_chem_name"]=table_4_1_1_1.iloc[:,0]
table_4_1_1_1["raw_cas"]=table_4_1_1_1.iloc[:,1]
table_4_1_1_1=table_4_1_1_1.loc[table_4_1_1_1["raw_chem_name"]!= "Substance name"]
table_4_1_1_1=table_4_1_1_1.reset_index()
table_4_1_1_1=table_4_1_1_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1_1_1)):
    table_4_1_1_1["raw_chem_name"].iloc[i]=clean(table_4_1_1_1["raw_chem_name"].iloc[i])
    table_4_1_1_1["raw_chem_name"].iloc[i]=table_4_1_1_1["raw_chem_name"].iloc[i].replace(",", "_")
    table_4_1_1_1["raw_chem_name"].iloc[i]=table_4_1_1_1["raw_chem_name"].iloc[i].strip().lower()
    if len(table_4_1_1_1["raw_chem_name"].iloc[i].split()) > 1:
        table_4_1_1_1["raw_chem_name"].iloc[i]=" ".join(table_4_1_1_1["raw_chem_name"].iloc[i].split())
    if len(table_4_1_1_1["raw_cas"].iloc[i].split()) > 1:
        table_4_1_1_1["raw_cas"].iloc[i]="".join(table_4_1_1_1["raw_cas"].iloc[i].split())

table_4_1_1_1["data_document_id"]="1372163"
table_4_1_1_1["data_document_filename"]="DCPS_19_a.pdf"
table_4_1_1_1["doc_date"]="2002"
table_4_1_1_1["raw_category"]=""
table_4_1_1_1["cat_code"]=""
table_4_1_1_1["description_cpcat"]=""
table_4_1_1_1["cpcat_code"]=""
table_4_1_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1_1_1.to_csv("DCPS_19_table_4_1_1_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1.1.2 Extraction
tables=read_pdf("document_1372164.pdf", pages="20,21", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_1_2=pd.concat([tables[1],tables[2]])
table_4_1_1_2["raw_chem_name"]=table_4_1_1_2.iloc[:,0]
table_4_1_1_2["raw_cas"]=table_4_1_1_2.iloc[:,1]
table_4_1_1_2=table_4_1_1_2.loc[table_4_1_1_2["raw_chem_name"]!= "Substance name"]
table_4_1_1_2=table_4_1_1_2.reset_index()
table_4_1_1_2=table_4_1_1_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1_1_2)):
    table_4_1_1_2["raw_chem_name"].iloc[i]=clean(table_4_1_1_2["raw_chem_name"].iloc[i])
    table_4_1_1_2["raw_chem_name"].iloc[i]=table_4_1_1_2["raw_chem_name"].iloc[i].replace(",", "_")
    table_4_1_1_2["raw_chem_name"].iloc[i]=table_4_1_1_2["raw_chem_name"].iloc[i].strip().lower()
    if len(table_4_1_1_2["raw_chem_name"].iloc[i].split()) > 1:
        table_4_1_1_2["raw_chem_name"].iloc[i]=" ".join(table_4_1_1_2["raw_chem_name"].iloc[i].split())

table_4_1_1_2["data_document_id"]="1372164"
table_4_1_1_2["data_document_filename"]="DCPS_19_b.pdf"
table_4_1_1_2["doc_date"]="2002"
table_4_1_1_2["raw_category"]=""
table_4_1_1_2["cat_code"]=""
table_4_1_1_2["description_cpcat"]=""
table_4_1_1_2["cpcat_code"]=""
table_4_1_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1_1_2.to_csv("DCPS_19_table_4_1_1_2.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1.1.3 Extraction
tables=read_pdf("document_1372165.pdf", pages="21", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_1_3=tables[1]
table_4_1_1_3["raw_chem_name"]=table_4_1_1_3.iloc[:,0]
table_4_1_1_3["raw_cas"]=table_4_1_1_3.iloc[:,1]
table_4_1_1_3=table_4_1_1_3.loc[table_4_1_1_3["raw_chem_name"]!= "Substance name"]
table_4_1_1_3=table_4_1_1_3.reset_index()
table_4_1_1_3=table_4_1_1_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1_1_3)):
    table_4_1_1_3["raw_chem_name"].iloc[i]=clean(table_4_1_1_3["raw_chem_name"].iloc[i])
    table_4_1_1_3["raw_chem_name"].iloc[i]=table_4_1_1_3["raw_chem_name"].iloc[i].replace(",", "_")
    table_4_1_1_3["raw_chem_name"].iloc[i]=table_4_1_1_3["raw_chem_name"].iloc[i].strip().lower()

table_4_1_1_3["data_document_id"]="1372165"
table_4_1_1_3["data_document_filename"]="DCPS_19_c.pdf"
table_4_1_1_3["doc_date"]="2002"
table_4_1_1_3["raw_category"]=""
table_4_1_1_3["cat_code"]=""
table_4_1_1_3["description_cpcat"]=""
table_4_1_1_3["cpcat_code"]=""
table_4_1_1_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1_1_3.to_csv("DCPS_19_table_4_1_1_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1.1.5 Extraction
tables=read_pdf("document_1372166.pdf", pages="22", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_1_5=tables[0]
table_4_1_1_5["raw_chem_name"]=table_4_1_1_5.iloc[:,0]
table_4_1_1_5["raw_cas"]=table_4_1_1_5.iloc[:,1]
table_4_1_1_5=table_4_1_1_5.loc[table_4_1_1_5["raw_chem_name"]!= "Substance name"]
table_4_1_1_5=table_4_1_1_5.reset_index()
table_4_1_1_5=table_4_1_1_5[["raw_chem_name","raw_cas"]]

for i in range(0,len(table_4_1_1_5)):
    table_4_1_1_5["raw_chem_name"].iloc[i]=table_4_1_1_5["raw_chem_name"].iloc[i].strip().lower()

table_4_1_1_5["data_document_id"]="1372166"
table_4_1_1_5["data_document_filename"]="DCPS_19_d.pdf"
table_4_1_1_5["doc_date"]="2002"
table_4_1_1_5["raw_category"]=""
table_4_1_1_5["cat_code"]=""
table_4_1_1_5["description_cpcat"]=""
table_4_1_1_5["cpcat_code"]=""
table_4_1_1_5["cpcat_sourcetype"]=""

table_4_1_1_5.to_csv("DCPS_19_table_4_1_1_5.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1.2.1 Extraction
tables=read_pdf("document_1372167.pdf", pages="22", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_2_1=tables[1]
table_4_1_2_1["raw_chem_name"]=table_4_1_2_1.iloc[:,0]
table_4_1_2_1["raw_cas"]=table_4_1_2_1.iloc[:,1]
table_4_1_2_1=table_4_1_2_1.loc[table_4_1_2_1["raw_chem_name"]!= "Substance name"]
table_4_1_2_1=table_4_1_2_1.reset_index()
table_4_1_2_1=table_4_1_2_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1_2_1)):
    table_4_1_2_1["raw_chem_name"].iloc[i]=clean(table_4_1_2_1["raw_chem_name"].iloc[i])
    table_4_1_2_1["raw_chem_name"].iloc[i]=table_4_1_2_1["raw_chem_name"].iloc[i].replace(",", "_")
    table_4_1_2_1["raw_chem_name"].iloc[i]=table_4_1_2_1["raw_chem_name"].iloc[i].strip().lower()
    if len(table_4_1_2_1["raw_cas"].iloc[i].split()) > 1:
        table_4_1_2_1["raw_cas"].iloc[i]="".join(table_4_1_2_1["raw_cas"].iloc[i].split())

table_4_1_2_1["data_document_id"]="1372167"
table_4_1_2_1["data_document_filename"]="DCPS_19_e.pdf"
table_4_1_2_1["doc_date"]="2002"
table_4_1_2_1["raw_category"]=""
table_4_1_2_1["cat_code"]=""
table_4_1_2_1["description_cpcat"]=""
table_4_1_2_1["cpcat_code"]=""
table_4_1_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1_2_1.to_csv("DCPS_19_table_4_1_2_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1.2.2 Extraction
tables=read_pdf("document_1372168.pdf", pages="22,23", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_2_2=pd.concat([tables[2],tables[3]], ignore_index=True)
table_4_1_2_2["raw_chem_name"]=table_4_1_2_2.iloc[:,0]
table_4_1_2_2["raw_cas"]=table_4_1_2_2.iloc[:,1]
table_4_1_2_2=table_4_1_2_2.loc[table_4_1_2_2["raw_chem_name"]!= "Substance name"]
table_4_1_2_2=table_4_1_2_2.reset_index()
table_4_1_2_2=table_4_1_2_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1_2_2)):
    table_4_1_2_2["raw_chem_name"].iloc[i]=clean(table_4_1_2_2["raw_chem_name"].iloc[i])
    table_4_1_2_2["raw_chem_name"].iloc[i]=table_4_1_2_2["raw_chem_name"].iloc[i].replace(",", "_")
    table_4_1_2_2["raw_chem_name"].iloc[i]=table_4_1_2_2["raw_chem_name"].iloc[i].strip().lower()
    if len(table_4_1_2_2["raw_chem_name"].iloc[i].split()) > 1:
        table_4_1_2_2["raw_chem_name"].iloc[i]=" ".join(table_4_1_2_2["raw_chem_name"].iloc[i].split())

table_4_1_2_2["data_document_id"]="1372168"
table_4_1_2_2["data_document_filename"]="DCPS_19_f.pdf"
table_4_1_2_2["doc_date"]="2002"
table_4_1_2_2["raw_category"]=""
table_4_1_2_2["cat_code"]=""
table_4_1_2_2["description_cpcat"]=""
table_4_1_2_2["cpcat_code"]=""
table_4_1_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1_2_2.to_csv("DCPS_19_table_4_1_2_2.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1.3.1 Extraction
tables=read_pdf("document_1372169.pdf", pages="24", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_4_1_3_1=tables[0]
table_4_1_3_1["raw_chem_name"]=table_4_1_3_1.iloc[:,0]
table_4_1_3_1["raw_cas"]=table_4_1_3_1.iloc[:,1]
table_4_1_3_1=table_4_1_3_1.loc[table_4_1_3_1["raw_chem_name"]!= "Substance name"]
table_4_1_3_1=table_4_1_3_1.reset_index()
table_4_1_3_1=table_4_1_3_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1_3_1)):
    table_4_1_3_1["raw_chem_name"].iloc[i]=clean(table_4_1_3_1["raw_chem_name"].iloc[i])
    table_4_1_3_1["raw_chem_name"].iloc[i]=table_4_1_3_1["raw_chem_name"].iloc[i].replace(",", "_")
    table_4_1_3_1["raw_chem_name"].iloc[i]=table_4_1_3_1["raw_chem_name"].iloc[i].strip().lower()

table_4_1_3_1["data_document_id"]="1372169"
table_4_1_3_1["data_document_filename"]="DCPS_19_g.pdf"
table_4_1_3_1["doc_date"]="2002"
table_4_1_3_1["raw_category"]=""
table_4_1_3_1["cat_code"]=""
table_4_1_3_1["description_cpcat"]=""
table_4_1_3_1["cpcat_code"]=""
table_4_1_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1_3_1.to_csv("DCPS_19_table_4_1_3_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
