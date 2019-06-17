#lkoval
#6-17-19

from tabula import read_pdf
import pandas as pd
import string

#Table 4.2
tables=read_pdf("document_1374275.pdf", pages="17,18", lattice=False, multiple_tables=True, pandas_options={'header': None})
table_4_2=pd.concat([tables[0],tables[1]], ignore_index=True)
table_4_2["raw_chem_name"]=table_4_2.iloc[:,0]
table_4_2=table_4_2.dropna(subset=["raw_chem_name"])
table_4_2=table_4_2.loc[table_4_2["raw_chem_name"]!="Sample name"]
table_4_2=table_4_2.reset_index()
table_4_2=table_4_2[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_2)):
    table_4_2["raw_chem_name"].iloc[j]=str(table_4_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_4_2["raw_chem_name"].iloc[j]=clean(str(table_4_2["raw_chem_name"].iloc[j]))

table_4_2["data_document_id"]="1374275"
table_4_2["data_document_filename"]="dcps_77_a.pdf"
table_4_2["doc_date"]="2006"
table_4_2["raw_category"]=""
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_2.to_csv("dcps_77_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.1
table_5_1=read_pdf("document_1374280.pdf", pages="31-33", lattice=True,pandas_options={'header': None})
table_5_1["raw_chem_name"]=table_5_1.iloc[:,0]
table_5_1["raw_cas"]=table_5_1.iloc[:,1]
table_5_1=table_5_1.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_5_1=table_5_1.loc[table_5_1["raw_chem_name"]!="Name"]
table_5_1=table_5_1.reset_index()
table_5_1=table_5_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_1)):
    table_5_1["raw_chem_name"].iloc[j]=str(table_5_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_5_1["raw_chem_name"].iloc[j]=clean(str(table_5_1["raw_chem_name"].iloc[j]))
    if len(table_5_1["raw_chem_name"].iloc[j].split())>1:
        table_5_1["raw_chem_name"].iloc[j]=" ".join(table_5_1["raw_chem_name"].iloc[j].split())
    if len(str(table_5_1["raw_cas"].iloc[j]).split())>1:
        table_5_1["raw_cas"].iloc[j]="".join(str(table_5_1["raw_cas"].iloc[j]).split())

table_5_1["raw_chem_name"].iloc[9]=table_5_1["raw_cas"].iloc[9]
table_5_1["raw_cas"].iloc[9]=""
table_5_1["raw_chem_name"].iloc[13]=table_5_1["raw_cas"].iloc[13]
table_5_1["raw_cas"].iloc[13]=""
table_5_1["raw_chem_name"].iloc[11]=table_5_1["raw_cas"].iloc[11]+table_5_1["raw_cas"].iloc[12]
table_5_1["raw_cas"].iloc[11]="80-55-7"

table_5_1=table_5_1.drop([12,30,31,32,33])
table_5_1=table_5_1.reset_index()
table_5_1=table_5_1[["raw_chem_name","raw_cas"]]

table_5_1["data_document_id"]="1374280"
table_5_1["data_document_filename"]="dcps_77_f.pdf"
table_5_1["doc_date"]="2006"
table_5_1["raw_category"]=""
table_5_1["cat_code"]=""
table_5_1["description_cpcat"]=""
table_5_1["cpcat_code"]=""
table_5_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_1.to_csv("dcps_77_table_5_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.3
tables=read_pdf("document_1374281.pdf", pages="34-36", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_3=pd.concat(tables[1:4], ignore_index=True)
table_5_3["raw_chem_name"]=table_5_3.iloc[:,0]
table_5_3["raw_cas"]=table_5_3.iloc[:,1]
table_5_3=table_5_3.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_5_3=table_5_3.loc[table_5_3["raw_chem_name"]!="Name"]
table_5_3=table_5_3.reset_index()
table_5_3=table_5_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_3)):
    table_5_3["raw_chem_name"].iloc[j]=str(table_5_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_5_3["raw_chem_name"].iloc[j]=clean(str(table_5_3["raw_chem_name"].iloc[j]))
    if len(table_5_3["raw_chem_name"].iloc[j].split())>1:
        table_5_3["raw_chem_name"].iloc[j]=" ".join(table_5_3["raw_chem_name"].iloc[j].split())
    if len(str(table_5_3["raw_cas"].iloc[j]).split())>1:
        table_5_3["raw_cas"].iloc[j]="".join(str(table_5_3["raw_cas"].iloc[j]).split())


table_5_3["data_document_id"]="1374281"
table_5_3["data_document_filename"]="dcps_77_g.pdf"
table_5_3["doc_date"]="2006"
table_5_3["raw_category"]=""
table_5_3["cat_code"]=""
table_5_3["description_cpcat"]=""
table_5_3["cpcat_code"]=""
table_5_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_3.to_csv("dcps_77_table_5_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
