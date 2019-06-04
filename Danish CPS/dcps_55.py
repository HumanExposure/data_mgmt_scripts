#lkoval
#6-4-19

from tabula import read_pdf
import pandas as pd
import string

#Table 5.4
table_5_4=read_pdf("document_1372474.pdf", pages="30", lattice=True, pandas_options={'header': None})
table_5_4["raw_chem_name"]=table_5_4.iloc[:,0]
table_5_4["count"]=table_5_4.iloc[:,1]
table_5_4=table_5_4.dropna(subset=["raw_chem_name"])
table_5_4=table_5_4.loc[table_5_4["raw_chem_name"]!="Sum"]
table_5_4=table_5_4.loc[table_5_4["count"]!="0"]
table_5_4=table_5_4.reset_index()
table_5_4=table_5_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_4)):
    table_5_4["raw_chem_name"].iloc[j]=str(table_5_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('α',"alpha")
    table_5_4["raw_chem_name"].iloc[j]=clean(str(table_5_4["raw_chem_name"].iloc[j]))
    if len(table_5_4["raw_chem_name"].iloc[j].split())>1:
        table_5_4["raw_chem_name"].iloc[j]=" ".join(table_5_4["raw_chem_name"].iloc[j].split())


table_5_4["data_document_id"]="1372474"
table_5_4["data_document_filename"]="DCPS55_b.pdf"
table_5_4["doc_date"]="2005"
table_5_4["raw_category"]=""
table_5_4["cat_code"]=""
table_5_4["description_cpcat"]=""
table_5_4["cpcat_code"]=""
table_5_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_4.to_csv("dcps_55_table_5_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.2
tables=read_pdf("document_1372477.pdf", pages="34", lattice=False, multiple_tables=True, pandas_options={'header': None})
table_6_2=tables[0]
table_6_2["raw_chem_name"]=table_6_2.iloc[2:,0]
table_6_2["raw_cas"]=table_6_2.iloc[2:,3]
table_6_2=table_6_2.dropna(subset=["raw_chem_name"])
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_2)):
    table_6_2["raw_chem_name"].iloc[j]=str(table_6_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('α',"alpha")
    table_6_2["raw_chem_name"].iloc[j]=clean(str(table_6_2["raw_chem_name"].iloc[j]))
    if str(table_6_2["raw_cas"].iloc[j])=="nan":
        table_6_2["raw_chem_name"].iloc[j]=table_6_2["raw_chem_name"].iloc[j-1]+" "+table_6_2["raw_chem_name"].iloc[j]
        table_6_2["raw_cas"].iloc[j]=table_6_2["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_6_2=table_6_2.drop(j_drop)
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]


table_6_2["data_document_id"]="1372476"
table_6_2["data_document_filename"]="DCPS55_d.pdf"
table_6_2["doc_date"]="2005"
table_6_2["raw_category"]=""
table_6_2["cat_code"]=""
table_6_2["description_cpcat"]=""
table_6_2["cpcat_code"]=""
table_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_2.to_csv("dcps_55_table_6_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.3
tables=read_pdf("document_1372477.pdf", pages="34", lattice=False, multiple_tables=True, pandas_options={'header': None})
table_6_3=tables[1]
table_6_3["raw_chem_name"]=table_6_3.iloc[2:,0]
table_6_3["raw_cas"]=table_6_3.iloc[2:,3]
table_6_3=table_6_3.dropna(subset=["raw_chem_name"])
table_6_3=table_6_3.reset_index()
table_6_3=table_6_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_3)):
    table_6_3["raw_chem_name"].iloc[j]=str(table_6_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace('α',"alpha")
    table_6_3["raw_chem_name"].iloc[j]=clean(str(table_6_3["raw_chem_name"].iloc[j]))


table_6_3["data_document_id"]="1372477"
table_6_3["data_document_filename"]="DCPS55_e.pdf"
table_6_3["doc_date"]="2005"
table_6_3["raw_category"]=""
table_6_3["cat_code"]=""
table_6_3["description_cpcat"]=""
table_6_3["cpcat_code"]=""
table_6_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_3.to_csv("dcps_55_table_6_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
