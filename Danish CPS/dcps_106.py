#lkoval
#5/22/2019

from tabula import read_pdf
import pandas as pd
import string

#Table 2.4
table_2_4=read_pdf("document_1372786.pdf", pages="19,20", lattice=True, pandas_options={'header': None})
table_2_4["raw_cas"]=table_2_4.iloc[:,2]
table_2_4["raw_chem_name"]=table_2_4.iloc[:,1]
table_2_4=table_2_4.loc[table_2_4["raw_cas"]!= "CAS No."]
table_2_4=table_2_4.reset_index()
table_2_4=table_2_4[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
    if len(table_2_4["raw_cas"].iloc[j].split())>1:
        table_2_4["raw_cas"].iloc[j]=" ".join(table_2_4["raw_cas"].iloc[j].split())

    if table_2_4["raw_chem_name"].iloc[j][-1]=="4":
        table_2_4["raw_chem_name"].iloc[j]=table_2_4["raw_chem_name"].iloc[j][:-1]

table_2_4["raw_chem_name"].iloc[32]="silicone"
table_2_4["raw_cas"].iloc[32]="no data"
table_2_4["raw_chem_name"].iloc[33]="silicone oil"
table_2_4["raw_cas"].iloc[33]="63148-62-9"
table_2_4["raw_chem_name"].iloc[39]="butane"
table_2_4["raw_cas"].iloc[39]="106-97-8"

table_2_4=table_2_4.drop_duplicates()
table_2_4=table_2_4.reset_index()
table_2_4=table_2_4[["raw_chem_name","raw_cas"]]

table_2_4["data_document_id"]="1372786"
table_2_4["data_document_filename"]="DCPS_106_a.pdf"
table_2_4["doc_date"]="2010"
table_2_4["raw_category"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_4.to_csv("dcps_106_table_2_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.2
tables=read_pdf("document_1372787.pdf", pages="30", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_2=tables[0]
table_4_2["raw_chem_name"]=table_4_2.iloc[:,0]
table_4_2=table_4_2.loc[table_4_2["raw_chem_name"]!= "Product No."]
table_4_2=table_4_2.reset_index()
table_4_2=table_4_2[["raw_chem_name"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_2)):
    table_4_2["raw_chem_name"].iloc[j]=str(table_4_2["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
    table_4_2["raw_chem_name"].iloc[j]=clean(str(table_4_2["raw_chem_name"].iloc[j]))
    if len(table_4_2["raw_chem_name"].iloc[j].split())>1:
        table_4_2["raw_chem_name"].iloc[j]=" ".join(table_4_2["raw_chem_name"].iloc[j].split())

table_4_2["data_document_id"]="1372787"
table_4_2["data_document_filename"]="DCPS_106_b.pdf"
table_4_2["doc_date"]="2010"
table_4_2["raw_category"]=""
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_2.to_csv("dcps_106_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.4
table_4_4=read_pdf("document_1372788.pdf", pages="31", lattice=True, pandas_options={'header': None})
table_4_4["raw_cas"]=table_4_4.iloc[:,1]
table_4_4["raw_chem_name"]=table_4_4.iloc[:,0]
table_4_4=table_4_4.loc[table_4_4["raw_cas"]!= "CAS No."]
table_4_4=table_4_4.reset_index()
table_4_4=table_4_4[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_4)):
    table_4_4["raw_chem_name"].iloc[j]=str(table_4_4["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
    table_4_4["raw_chem_name"].iloc[j]=clean(str(table_4_4["raw_chem_name"].iloc[j]))
    if len(table_4_4["raw_chem_name"].iloc[j].split())>1:
        table_4_4["raw_chem_name"].iloc[j]=" ".join(table_4_4["raw_chem_name"].iloc[j].split())
    if len(table_4_4["raw_cas"].iloc[j].split())>1:
        table_4_4["raw_cas"].iloc[j]=" ".join(table_4_4["raw_cas"].iloc[j].split())


table_4_4["data_document_id"]="1372788"
table_4_4["data_document_filename"]="DCPS_106_c.pdf"
table_4_4["doc_date"]="2010"
table_4_4["raw_category"]=""
table_4_4["cat_code"]=""
table_4_4["description_cpcat"]=""
table_4_4["cpcat_code"]=""
table_4_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_4.to_csv("dcps_106_table_4_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.6
table_4_6=read_pdf("document_1372789.pdf", pages="34", lattice=True, pandas_options={'header': None})
table_4_6["raw_cas"]=table_4_6.iloc[:,2]
table_4_6["raw_chem_name"]=table_4_6.iloc[:,1]
table_4_6=table_4_6.loc[table_4_6["raw_cas"]!= "CAS No."]
table_4_6=table_4_6.reset_index()
table_4_6=table_4_6[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_6)):
    table_4_6["raw_chem_name"].iloc[j]=str(table_4_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_4_6["raw_chem_name"].iloc[j]=clean(str(table_4_6["raw_chem_name"].iloc[j]))
    if len(table_4_6["raw_chem_name"].iloc[j].split())>1:
        table_4_6["raw_chem_name"].iloc[j]=" ".join(table_4_6["raw_chem_name"].iloc[j].split())
    if len(table_4_6["raw_cas"].iloc[j].split())>1:
        table_4_6["raw_cas"].iloc[j]=" ".join(table_4_6["raw_cas"].iloc[j].split())


table_4_6["data_document_id"]="1372789"
table_4_6["data_document_filename"]="DCPS_106_d.pdf"
table_4_6["doc_date"]="2010"
table_4_6["raw_category"]=""
table_4_6["cat_code"]=""
table_4_6["description_cpcat"]=""
table_4_6["cpcat_code"]=""
table_4_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_6.to_csv("dcps_106_table_4_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
