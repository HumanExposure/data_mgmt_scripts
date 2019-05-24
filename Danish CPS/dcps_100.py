from tabula import read_pdf
import pandas as pd
import string

#Table 6.2
tables=read_pdf("document_1372852.pdf", pages="53", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_2=tables[0]
table_6_2["raw_cas"]=table_6_2.iloc[:,1]
table_6_2["raw_chem_name"]=table_6_2.iloc[:,0]
table_6_2=table_6_2.loc[table_6_2["raw_chem_name"]!= "Component"]
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_2)):
    table_6_2["raw_chem_name"].iloc[j]=str(table_6_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_6_2["raw_chem_name"].iloc[j]=clean(str(table_6_2["raw_chem_name"].iloc[j]))
    if len(table_6_2["raw_chem_name"].iloc[j].split())>1:
        table_6_2["raw_chem_name"].iloc[j]=" ".join(table_6_2["raw_chem_name"].iloc[j].split())
    if len(table_6_2["raw_cas"].iloc[j].split())>1:
        table_6_2["raw_cas"].iloc[j]="".join(table_6_2["raw_cas"].iloc[j].split())

table_6_2["data_document_id"]="1372852"
table_6_2["data_document_filename"]="DCPS_100_b.pdf"
table_6_2["doc_date"]="2008"
table_6_2["raw_category"]=""
table_6_2["cat_code"]=""
table_6_2["description_cpcat"]=""
table_6_2["cpcat_code"]=""
table_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_2.to_csv("dcps_100_table_6_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.4
table_6_4=read_pdf("document_1372854.pdf", pages="54", lattice=True, pandas_options={'header': None})
table_6_4["raw_cas"]=table_6_4.iloc[:,1]
table_6_4["raw_chem_name"]=table_6_4.iloc[:,0]
table_6_4=table_6_4.loc[table_6_4["raw_chem_name"]!= "Component"]
table_6_4=table_6_4.reset_index()
table_6_4=table_6_4[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_4)):
    table_6_4["raw_chem_name"].iloc[j]=str(table_6_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_6_4["raw_chem_name"].iloc[j]=clean(str(table_6_4["raw_chem_name"].iloc[j]))
    if len(table_6_4["raw_chem_name"].iloc[j].split())>1:
        table_6_4["raw_chem_name"].iloc[j]=" ".join(table_6_4["raw_chem_name"].iloc[j].split())
    if len(str(table_6_4["raw_cas"].iloc[j]).split())>1:
        table_6_4["raw_cas"].iloc[j]="".join(str(table_6_4["raw_cas"].iloc[j]).split())

table_6_4["data_document_id"]="1372854"
table_6_4["data_document_filename"]="DCPS_100_d.pdf"
table_6_4["doc_date"]="2008"
table_6_4["raw_category"]=""
table_6_4["cat_code"]=""
table_6_4["description_cpcat"]=""
table_6_4["cpcat_code"]=""
table_6_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_4.to_csv("dcps_100_table_6_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.6
tables=read_pdf("document_1372856.pdf", pages="55", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_6=tables[1]
table_6_6["raw_cas"]=table_6_6.iloc[:,1]
table_6_6["raw_chem_name"]=table_6_6.iloc[:,0]
table_6_6=table_6_6.loc[table_6_6["raw_chem_name"]!= "Component"]
table_6_6=table_6_6.reset_index()
table_6_6=table_6_6[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_6)):
    table_6_6["raw_chem_name"].iloc[j]=str(table_6_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_6_6["raw_chem_name"].iloc[j]=clean(str(table_6_6["raw_chem_name"].iloc[j]))
    if len(table_6_6["raw_chem_name"].iloc[j].split())>1:
        table_6_6["raw_chem_name"].iloc[j]=" ".join(table_6_6["raw_chem_name"].iloc[j].split())

table_6_6["data_document_id"]="1372856"
table_6_6["data_document_filename"]="DCPS_100_f.pdf"
table_6_6["doc_date"]="2008"
table_6_6["raw_category"]=""
table_6_6["cat_code"]=""
table_6_6["description_cpcat"]=""
table_6_6["cpcat_code"]=""
table_6_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_6.to_csv("dcps_100_table_6_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.8
table_6_8=read_pdf("document_1372857.pdf", pages="57,58", lattice=True, pandas_options={'header': None})
table_6_8["raw_cas"]=table_6_8.iloc[:,1]
table_6_8["raw_chem_name"]=table_6_8.iloc[:,0]
table_6_8=table_6_8[["raw_chem_name","raw_cas"]]
table_6_8=table_6_8.loc[table_6_8["raw_chem_name"]!= "Component"]
table_6_8=table_6_8.dropna(how="all")
table_6_8=table_6_8.reset_index()
table_6_8=table_6_8[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_8)):
    table_6_8["raw_chem_name"].iloc[j]=str(table_6_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_6_8["raw_chem_name"].iloc[j]=clean(str(table_6_8["raw_chem_name"].iloc[j]))
    if len(table_6_8["raw_chem_name"].iloc[j].split())>1:
        table_6_8["raw_chem_name"].iloc[j]=" ".join(table_6_8["raw_chem_name"].iloc[j].split())

table_6_8=table_6_8.drop_duplicates()
table_6_8=table_6_8.reset_index()
table_6_8=table_6_8[["raw_chem_name","raw_cas"]]

table_6_8["data_document_id"]="1372857"
table_6_8["data_document_filename"]="DCPS_100_g.pdf"
table_6_8["doc_date"]="2008"
table_6_8["raw_category"]=""
table_6_8["cat_code"]=""
table_6_8["description_cpcat"]=""
table_6_8["cpcat_code"]=""
table_6_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_8.to_csv("dcps_100_table_6_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
