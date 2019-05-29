#lkoval
#5/23/19

from tabula import read_pdf
import pandas as pd
import string

#Table 4.2
table_4_2=read_pdf("document_1372750.pdf", pages="20", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_4_2["raw_chem_name"]=table_4_2.iloc[:,1]
table_4_2["raw_cas"]=table_4_2.iloc[:,0]
table_4_2=table_4_2.loc[table_4_2["raw_chem_name"]!= "Name of chemical"]
table_4_2=table_4_2.reset_index()
table_4_2=table_4_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_2)):
    table_4_2["raw_chem_name"].iloc[j]=str(table_4_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("#","").replace("^","")
    table_4_2["raw_chem_name"].iloc[j]=clean(str(table_4_2["raw_chem_name"].iloc[j]))
    if len(table_4_2["raw_chem_name"].iloc[j].split())>1:
        table_4_2["raw_chem_name"].iloc[j]=" ".join(table_4_2["raw_chem_name"].iloc[j].split())
    if len(str(table_4_2["raw_cas"].iloc[j]).split())>1:
        table_4_2["raw_cas"].iloc[j]=" ".join(str(table_4_2["raw_cas"].iloc[j]).split())

table_4_2["data_document_id"]="1372750"
table_4_2["data_document_filename"]="DCPS_21_a.pdf"
table_4_2["doc_date"]="2003"
table_4_2["raw_category"]=""
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_2.to_csv("dcps_21_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.3
table_4_3=read_pdf("document_1372751.pdf", pages="21", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_4_3["raw_chem_name"]=table_4_3.iloc[:,1]
table_4_3["raw_cas"]=table_4_3.iloc[:,0]
table_4_3=table_4_3.loc[table_4_3["raw_chem_name"]!= "Name of chemical"]
table_4_3=table_4_3.dropna(subset=["raw_chem_name"])
table_4_3=table_4_3.reset_index()
table_4_3=table_4_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_3)):
    table_4_3["raw_chem_name"].iloc[j]=str(table_4_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("#","").replace("^","")
    table_4_3["raw_chem_name"].iloc[j]=clean(str(table_4_3["raw_chem_name"].iloc[j]))
    if len(table_4_3["raw_chem_name"].iloc[j].split())>1:
        table_4_3["raw_chem_name"].iloc[j]=" ".join(table_4_3["raw_chem_name"].iloc[j].split())
    if len(str(table_4_3["raw_cas"].iloc[j]).split())>1:
        table_4_3["raw_cas"].iloc[j]=" ".join(str(table_4_3["raw_cas"].iloc[j]).split())


table_4_3["raw_chem_name"].iloc[19]="3295 hydrocarbons, liquid nos"
table_4_3["raw_cas"].iloc[19]="-"

table_4_3["data_document_id"]="1372751"
table_4_3["data_document_filename"]="DCPS_21_b.pdf"
table_4_3["doc_date"]="2003"
table_4_3["raw_category"]=""
table_4_3["cat_code"]=""
table_4_3["description_cpcat"]=""
table_4_3["cpcat_code"]=""
table_4_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_3.to_csv("dcps_21_table_4_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
