#Lauren Koval
#4/25/19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 3.2 & 3.3 as pandas dfs using tabula

#Table 3.2
tables=read_pdf("document_1372185.pdf", pages="16", multiple_tables= True, pandas_options={'header': None})

table_3_2=tables[0]
table_3_2["raw_chem_name"]=table_3_2.iloc[:,0]
table_3_2["raw_cas"]=table_3_2.iloc[:,2]
table_3_2=table_3_2.loc[table_3_2["raw_cas"] != "CAS no"]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"] != "products"]
table_3_2=table_3_2[["raw_chem_name", "raw_cas"]]
table_3_2=table_3_2.dropna(how="all")
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i].strip().lower()
    table_3_2["raw_chem_name"].iloc[i]=clean(table_3_2["raw_chem_name"].iloc[i])
    table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i].split()
    table_3_2["raw_chem_name"].iloc[i]=" ".join(table_3_2["raw_chem_name"].iloc[i][:-1])
    table_3_2["raw_cas"].iloc[i]=clean(str(table_3_2["raw_cas"].iloc[i]))

#required manual correction
table_3_2["raw_chem_name"].iloc[12]="cocoabutter /extraxt from bark and seed"
table_3_2["raw_cas"].iloc[12]="84649-99-0/ 8002-31-1"

table_3_2["data_document_id"]="1372185"
table_3_2["data_document_filename"]="DCPS_78_a.pdf"
table_3_2["doc_date"]="2006"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("DCPS_78_table_3_2.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.3
tables=read_pdf("document_1372186.pdf", pages="16,17", multiple_tables= True, pandas_options={'header': None})

table_3_3_pt1=tables[1]
table_3_3_pt1["raw_chem_name"]=table_3_3_pt1.iloc[:,0]
table_3_3_pt1["raw_cas"]=table_3_3_pt1.iloc[:,3]
table_3_3_pt1=table_3_3_pt1.loc[table_3_3_pt1["raw_cas"] != "CAS no."]
table_3_3_pt1=table_3_3_pt1.loc[table_3_3_pt1["raw_chem_name"]!= "products"]
table_3_3_pt1=table_3_3_pt1[["raw_chem_name", "raw_cas"]]
table_3_3_pt1=table_3_3_pt1.dropna(how="all")
table_3_3_pt1=table_3_3_pt1.reset_index()
table_3_3_pt1=table_3_3_pt1[["raw_chem_name", "raw_cas"]]

table_3_3_pt2=tables[2]
table_3_3_pt2["raw_chem_name"]=table_3_3_pt2.iloc[:,0]
table_3_3_pt2["raw_cas"]=table_3_3_pt2.iloc[:,2]
table_3_3_pt2=table_3_3_pt2.loc[table_3_3_pt2["raw_cas"] != "CAS no."]
table_3_3_pt2=table_3_3_pt2.loc[table_3_3_pt2["raw_chem_name"] != "products"]
table_3_3_pt2=table_3_3_pt2[["raw_chem_name", "raw_cas"]]
table_3_3_pt2=table_3_3_pt2.dropna(how="all")
table_3_3_pt2=table_3_3_pt2.reset_index()
table_3_3_pt2=table_3_3_pt2[["raw_chem_name", "raw_cas"]]


table_3_3=pd.concat([table_3_3_pt1,table_3_3_pt2], ignore_index=True)


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_3_3)):
    if table_3_3["raw_chem_name"].iloc[i]=="rose)":
        table_3_3["raw_chem_name"].iloc[i-1]=table_3_3["raw_chem_name"].iloc[i-1]+" "+table_3_3["raw_chem_name"].iloc[i]
        i_drop=i
    table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i].strip().lower()
    table_3_3["raw_chem_name"].iloc[i]=clean(table_3_3["raw_chem_name"].iloc[i])
    table_3_3["raw_cas"].iloc[i]=clean(str(table_3_3["raw_cas"].iloc[i]))
    digit_test=table_3_3["raw_chem_name"].iloc[i].split()
    if digit_test[-1].isdigit():
        table_3_3["raw_chem_name"].iloc[i]=" ".join(digit_test[:-1])

#required manual correction
table_3_3["raw_chem_name"].iloc[40]="citronella oil, orange grass"
table_3_3["raw_cas"].iloc[40]="8000-29-1"

table_3_3=table_3_3.drop(i_drop)
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]

table_3_3["data_document_id"]="1372186"
table_3_3["data_document_filename"]="DCPS_78_b.pdf"
table_3_3["doc_date"]="2006"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("DCPS_78_table_3_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
