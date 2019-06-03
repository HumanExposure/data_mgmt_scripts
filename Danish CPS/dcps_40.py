#lkoval
#6-3-19

from tabula import read_pdf
import pandas as pd
import string

#Table 5.2 #1
tables=read_pdf("document_1372483.pdf", pages="23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_2=tables[0]
table_5_2["raw_chem_name"]=table_5_2.iloc[:,2]
table_5_2["raw_cas"]=table_5_2.iloc[:,3]
table_5_2=table_5_2.loc[table_5_2["raw_chem_name"]!="Organic component"]
table_5_2=table_5_2.loc[table_5_2["raw_chem_name"]!="-"]
table_5_2=table_5_2.reset_index()

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_2)):
    table_5_2["raw_chem_name"].iloc[j]=str(table_5_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_5_2["raw_chem_name"].iloc[j]=clean(str(table_5_2["raw_chem_name"].iloc[j]))
    if str(table_5_2["raw_chem_name"].iloc[j])=="nan":
        table_5_2["raw_chem_name"].iloc[j]=table_5_2.iloc[j,1]
        table_5_2["raw_cas"].iloc[j]=table_5_2.iloc[j,2]

table_5_2=table_5_2[["raw_chem_name","raw_cas"]]
table_5_2=table_5_2.drop_duplicates()
table_5_2=table_5_2.reset_index()
table_5_2=table_5_2[["raw_chem_name","raw_cas"]]

table_5_2["data_document_id"]="1372483"
table_5_2["data_document_filename"]="dcps_40_a.pdf"
table_5_2["doc_date"]="2003"
table_5_2["raw_category"]=""
table_5_2["cat_code"]=""
table_5_2["description_cpcat"]=""
table_5_2["cpcat_code"]=""
table_5_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_2.to_csv("dcps_40_table_5_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.2 #2
tables=read_pdf("document_1372484.pdf", pages="23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_2_scd=tables[1]
table_5_2_scd["raw_chem_name"]=table_5_2_scd.iloc[:,0]
table_5_2_scd["raw_cas"]=table_5_2_scd.iloc[:,1]
table_5_2_scd=table_5_2_scd.loc[table_5_2_scd["raw_chem_name"]!="Organic component"]
table_5_2_scd=table_5_2_scd.reset_index()

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_2_scd)):
    table_5_2_scd["raw_chem_name"].iloc[j]=str(table_5_2_scd["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_5_2_scd["raw_chem_name"].iloc[j]=clean(str(table_5_2_scd["raw_chem_name"].iloc[j]))

table_5_2_scd=table_5_2_scd[["raw_chem_name","raw_cas"]]

table_5_2_scd["data_document_id"]="1372484"
table_5_2_scd["data_document_filename"]="dcps_40_b.pdf"
table_5_2_scd["doc_date"]="2003"
table_5_2_scd["raw_category"]=""
table_5_2_scd["cat_code"]=""
table_5_2_scd["description_cpcat"]=""
table_5_2_scd["cpcat_code"]=""
table_5_2_scd["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_2_scd.to_csv("dcps_40_table_5_2_scd.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.3
table_5_3=read_pdf("document_1372485.pdf", pages="24", lattice=True, pandas_options={'header': None})
table_5_3["raw_chem_name"]=table_5_3.iloc[:,2]
table_5_3["raw_cas"]=table_5_3.iloc[:,3]
table_5_3=table_5_3.loc[table_5_3["raw_chem_name"]!="Chemical name"]
table_5_3=table_5_3.reset_index()
table_5_3=table_5_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_3)):
    table_5_3["raw_chem_name"].iloc[j]=str(table_5_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_5_3["raw_chem_name"].iloc[j]=clean(str(table_5_3["raw_chem_name"].iloc[j]))
    if len(table_5_3["raw_chem_name"].iloc[j].split())>1:
        table_5_3["raw_chem_name"].iloc[j]=" ".join(table_5_3["raw_chem_name"].iloc[j].split())

table_5_3["data_document_id"]="1372485"
table_5_3["data_document_filename"]="dcps_40_c.pdf"
table_5_3["doc_date"]="2003"
table_5_3["raw_category"]=""
table_5_3["cat_code"]=""
table_5_3["description_cpcat"]=""
table_5_3["cpcat_code"]=""
table_5_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_3.to_csv("dcps_40_table_5_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
