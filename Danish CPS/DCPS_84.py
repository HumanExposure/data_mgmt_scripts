#lkoval
#4/25/19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 3.9A, 3.9B, and 4.1 as pandas dfs using tabula

#Table 3.9A
tables=read_pdf("document_1372170.pdf", pages="39,40", lattice=True, multiple_tables= True, pandas_options={'header': None})

tables[0]=tables[0].iloc[:,1:4]
tables[0].iloc[38,2]=tables[0].iloc[38,1]
tables[0].iloc[38,1]=tables[0].iloc[38,0]
tables[0].iloc[39,2]=tables[0].iloc[39,1]
tables[0].iloc[39,1]=tables[0].iloc[39,0]

tables[1]=tables[1].iloc[:,1:4]
tables[1].iloc[34,2]=tables[1].iloc[34,1]
tables[1].iloc[34,1]=tables[1].iloc[34,0]
tables[1].iloc[35,2]=tables[1].iloc[35,1]
tables[1].iloc[35,1]=tables[1].iloc[35,0]

table_3_9A=pd.concat([tables[0],tables[1]], ignore_index=True)
table_3_9A=table_3_9A.iloc[:,1:3]
table_3_9A.columns=["raw_chem_name", "raw_cas"]
table_3_9A=table_3_9A.loc[table_3_9A["raw_chem_name"]!= "Substance"]
table_3_9A=table_3_9A.dropna(subset=["raw_chem_name","raw_cas"],how="all")
table_3_9A=table_3_9A.reset_index()
table_3_9A=table_3_9A[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_9A)):
    table_3_9A["raw_chem_name"].iloc[i]=clean(str(table_3_9A["raw_chem_name"].iloc[i]))
    table_3_9A["raw_chem_name"].iloc[i]=str(table_3_9A["raw_chem_name"].iloc[i]).replace(",", "_")
    table_3_9A["raw_chem_name"].iloc[i]=str(table_3_9A["raw_chem_name"].iloc[i]).strip().lower()
    if len(str(table_3_9A["raw_chem_name"].iloc[i]).split()) > 1:
        table_3_9A["raw_chem_name"].iloc[i]=" ".join(table_3_9A["raw_chem_name"].iloc[i].split())

table_3_9A=table_3_9A.drop_duplicates()
table_3_9A.reset_index()
table_3_9A=table_3_9A[["raw_chem_name","raw_cas"]]

table_3_9A["data_document_id"]="1372170"
table_3_9A["data_document_filename"]="DCPS_84_a.pdf"
table_3_9A["doc_date"]="2007"
table_3_9A["raw_category"]=""
table_3_9A["cat_code"]=""
table_3_9A["description_cpcat"]=""
table_3_9A["cpcat_code"]=""
table_3_9A["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_9A.to_csv("DCPS_84_table_3_9A.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.9B Extraction
tables=read_pdf("document_1372171.pdf", pages="40,41,42", lattice=True, multiple_tables= True, pandas_options={'header': None})
table_3_9B=pd.concat([tables[1],tables[2],tables[3],tables[4]], ignore_index=True)
table_3_9B["raw_chem_name"]=table_3_9B.iloc[:,0]
table_3_9B["raw_cas"]=table_3_9B.iloc[:,1]
table_3_9B=table_3_9B.loc[table_3_9B["raw_cas"]!= "CAS"]
table_3_9B=table_3_9B.reset_index()
table_3_9B=table_3_9B[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_9B)):
    table_3_9B["raw_chem_name"].iloc[i]=clean(str(table_3_9B["raw_chem_name"].iloc[i]))
    table_3_9B["raw_chem_name"].iloc[i]=str(table_3_9B["raw_chem_name"].iloc[i]).replace(",", "_")
    table_3_9B["raw_chem_name"].iloc[i]=str(table_3_9B["raw_chem_name"].iloc[i]).strip().lower()
    if len(str(table_3_9B["raw_chem_name"].iloc[i]).split()) > 1:
        table_3_9B["raw_chem_name"].iloc[i]=" ".join(table_3_9B["raw_chem_name"].iloc[i].split())

table_3_9B=table_3_9B.drop_duplicates()
table_3_9B.reset_index()
table_3_9B=table_3_9B[["raw_chem_name","raw_cas"]]

table_3_9B["data_document_id"]="1372171"
table_3_9B["data_document_filename"]="DCPS_84_b.pdf"
table_3_9B["doc_date"]="2007"
table_3_9B["raw_category"]=""
table_3_9B["cat_code"]=""
table_3_9B["description_cpcat"]=""
table_3_9B["cpcat_code"]=""
table_3_9B["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_9B.to_csv("DCPS_84_table_3_9B.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.1 Extraction
table_4_1=read_pdf("document_1372172.pdf", pages="47-50", lattice=True, pandas_options={'header': None})
table_4_1["raw_chem_name"]=table_4_1.iloc[:,0]
table_4_1["raw_cas"]=table_4_1.iloc[:,1]
table_4_1=table_4_1.loc[table_4_1["raw_cas"]!= "CAS no."]
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

indices_to_drop=[]
for i in range(0,len(table_4_1)):
    if isinstance(table_4_1["raw_chem_name"].iloc[i], str):
        if "Content" in table_4_1["raw_chem_name"].iloc[i]:
            indices_to_drop.append(i)
        if "Substance" in table_4_1["raw_chem_name"].iloc[i]:
            indices_to_drop.append(i)

table_4_1=table_4_1.drop(indices_to_drop)
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1.drop(columns="index")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_4_1)):
    table_4_1["raw_chem_name"].iloc[i]=clean(str(table_4_1["raw_chem_name"].iloc[i]))
    table_4_1["raw_chem_name"].iloc[i]=str(table_4_1["raw_chem_name"].iloc[i]).replace(",", "_")
    table_4_1["raw_chem_name"].iloc[i]=str(table_4_1["raw_chem_name"].iloc[i]).strip().lower()
    if len(str(table_4_1["raw_chem_name"].iloc[i]).split()) > 1:
        table_4_1["raw_chem_name"].iloc[i]=" ".join(table_4_1["raw_chem_name"].iloc[i].split())
    if len(str(table_4_1["raw_cas"].iloc[i]).split()) > 1:
        table_4_1["raw_cas"].iloc[i]=" ".join(table_4_1["raw_cas"].iloc[i].split())

table_4_1=table_4_1.drop_duplicates()
table_4_1=table_4_1.dropna(how="all")
table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

table_4_1["data_document_id"]="1372172"
table_4_1["data_document_filename"]="DCPS_84_c.pdf"
table_4_1["doc_date"]="2007"
table_4_1["raw_category"]=""
table_4_1["cat_code"]=""
table_4_1["description_cpcat"]=""
table_4_1["cpcat_code"]=""
table_4_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1.to_csv("DCPS_84_table_4_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
