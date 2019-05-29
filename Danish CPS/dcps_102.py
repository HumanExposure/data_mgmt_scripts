#lkoval
#5-20-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.2
table_3_2=read_pdf("document_1372838.pdf", pages="35-37", lattice=True, pandas_options={'header': None})
table_3_2["raw_cas"]=table_3_2.iloc[:,1]
table_3_2["raw_chem_name"]=table_3_2.iloc[:,0]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!= "Substance name"]
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".",",")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(table_3_2["raw_chem_name"].iloc[j].split())>1:
        table_3_2["raw_chem_name"].iloc[j]=" ".join(table_3_2["raw_chem_name"].iloc[j].split())
    if len(str(table_3_2["raw_cas"].iloc[j]).split())>1:
        table_3_2["raw_cas"].iloc[j]=" ".join(str(table_3_2["raw_cas"].iloc[j]).split())

table_3_2["data_document_id"]="1372838"
table_3_2["data_document_filename"]="DCPS_102_a.pdf"
table_3_2["doc_date"]="2009"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_102_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.15
tables=read_pdf("document_1372842.pdf", pages="118,119", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_15=pd.concat([tables[0],tables[1]], ignore_index=True)
table_6_15["raw_cas"]=table_6_15.iloc[:,1]
table_6_15["raw_chem_name"]=table_6_15.iloc[:,0]
table_6_15=table_6_15.loc[table_6_15["raw_chem_name"]!= "Component"]
table_6_15=table_6_15.loc[table_6_15["raw_cas"]!= "Product no."]
table_6_15=table_6_15[["raw_chem_name","raw_cas"]]
table_6_15=table_6_15.dropna(how="all")
table_6_15=table_6_15.reset_index()
table_6_15=table_6_15[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_15)):
    table_6_15["raw_chem_name"].iloc[j]=str(table_6_15["raw_chem_name"].iloc[j]).strip().lower().replace(".",",")
    table_6_15["raw_chem_name"].iloc[j]=clean(str(table_6_15["raw_chem_name"].iloc[j]))
    if len(table_6_15["raw_chem_name"].iloc[j].split())>1:
        table_6_15["raw_chem_name"].iloc[j]=" ".join(table_6_15["raw_chem_name"].iloc[j].split())
    if len(str(table_6_15["raw_cas"].iloc[j]).split())>1:
        table_6_15["raw_cas"].iloc[j]=" ".join(str(table_6_15["raw_cas"].iloc[j]).split())

table_6_15["raw_chem_name"].iloc[29]=table_6_15["raw_chem_name"].iloc[29]+table_6_15["raw_chem_name"].iloc[30]
table_6_15["raw_cas"].iloc[32]="17418-58-5"
table_6_15["raw_cas"].iloc[33]="01-03-5256 or 6022-25-9"
table_6_15=table_6_15.drop(30)
table_6_15=table_6_15.reset_index()
table_6_15=table_6_15[["raw_chem_name","raw_cas"]]

table_6_15["data_document_id"]="1372842"
table_6_15["data_document_filename"]="DCPS_102_e.pdf"
table_6_15["doc_date"]="2009"
table_6_15["raw_category"]=""
table_6_15["cat_code"]=""
table_6_15["description_cpcat"]=""
table_6_15["cpcat_code"]=""
table_6_15["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_15.to_csv("dcps_102_table_6_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



#Table 6.16
tables=read_pdf("document_1372842.pdf", pages="118,119", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_16=tables[2]
table_6_16["raw_cas"]=table_6_16.iloc[:,1]
table_6_16["raw_chem_name"]=table_6_16.iloc[:,0]
table_6_16=table_6_16.loc[table_6_16["raw_chem_name"]!= "Component"]
table_6_16=table_6_16.loc[table_6_16["raw_cas"]!= "Product no."]
table_6_16=table_6_16[["raw_chem_name","raw_cas"]]
table_6_16=table_6_16.dropna(how="all")
table_6_16=table_6_16.reset_index()
table_6_16=table_6_16[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_16)):
    table_6_16["raw_chem_name"].iloc[j]=str(table_6_16["raw_chem_name"].iloc[j]).strip().lower().replace(".",",")
    table_6_16["raw_chem_name"].iloc[j]=clean(str(table_6_16["raw_chem_name"].iloc[j]))
    if len(table_6_16["raw_chem_name"].iloc[j].split())>1:
        table_6_16["raw_chem_name"].iloc[j]=" ".join(table_6_16["raw_chem_name"].iloc[j].split())
    if len(str(table_6_16["raw_cas"].iloc[j]).split())>1:
        table_6_16["raw_cas"].iloc[j]=" ".join(str(table_6_16["raw_cas"].iloc[j]).split())

table_6_16["data_document_id"]="1372843"
table_6_16["data_document_filename"]="DCPS_102_f.pdf"
table_6_16["doc_date"]="2009"
table_6_16["raw_category"]=""
table_6_16["cat_code"]=""
table_6_16["description_cpcat"]=""
table_6_16["cpcat_code"]=""
table_6_16["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_16.to_csv("dcps_102_table_6_16.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 6.17
table_6_17=read_pdf("document_1372844.pdf", pages="120", lattice=True, pandas_options={'header': None})
table_6_17["raw_cas"]=table_6_17.iloc[:,1]
table_6_17["raw_chem_name"]=table_6_17.iloc[:,0]
table_6_17=table_6_17.loc[table_6_17["raw_chem_name"]!= "Component"]
table_6_17=table_6_17.loc[table_6_17["raw_cas"]!= "Product no."]
table_6_17=table_6_17[["raw_chem_name","raw_cas"]]
table_6_17=table_6_17.dropna(how="all")
table_6_17=table_6_17.reset_index()
table_6_17=table_6_17[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_17)):
    table_6_17["raw_chem_name"].iloc[j]=str(table_6_17["raw_chem_name"].iloc[j]).strip().lower().replace(".",",")
    table_6_17["raw_chem_name"].iloc[j]=clean(str(table_6_17["raw_chem_name"].iloc[j]))
    if len(table_6_17["raw_chem_name"].iloc[j].split())>1:
        table_6_17["raw_chem_name"].iloc[j]=" ".join(table_6_17["raw_chem_name"].iloc[j].split())
    if len(str(table_6_17["raw_cas"].iloc[j]).split())>1:
        table_6_17["raw_cas"].iloc[j]=" ".join(str(table_6_17["raw_cas"].iloc[j]).split())

#chem not detected
table_6_17=table_6_17.drop(39)
table_6_17=table_6_17.reset_index()
table_6_17=table_6_17[["raw_chem_name","raw_cas"]]

table_6_17["data_document_id"]="1372844"
table_6_17["data_document_filename"]="DCPS_102_g.pdf"
table_6_17["doc_date"]="2009"
table_6_17["raw_category"]=""
table_6_17["cat_code"]=""
table_6_17["description_cpcat"]=""
table_6_17["cpcat_code"]=""
table_6_17["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_17.to_csv("dcps_102_table_6_17.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 6.19
tables=read_pdf("document_1372845.pdf", pages="121,122", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_19=pd.concat([tables[1],tables[2]],ignore_index=True)
table_6_19["raw_cas"]=table_6_19.iloc[:,1]
table_6_19["raw_chem_name"]=table_6_19.iloc[:,0]
table_6_19=table_6_19.loc[table_6_19["raw_chem_name"]!= "Component"]
table_6_19=table_6_19.loc[table_6_19["raw_cas"]!= "Product no."]
table_6_19=table_6_19[["raw_chem_name","raw_cas"]]
table_6_19=table_6_19.dropna(how="all")
table_6_19=table_6_19.reset_index()
table_6_19=table_6_19[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_19)):
    table_6_19["raw_chem_name"].iloc[j]=str(table_6_19["raw_chem_name"].iloc[j]).strip().lower().replace(".",",")
    table_6_19["raw_chem_name"].iloc[j]=clean(str(table_6_19["raw_chem_name"].iloc[j]))
    if len(table_6_19["raw_chem_name"].iloc[j].split())>1:
        table_6_19["raw_chem_name"].iloc[j]=" ".join(table_6_19["raw_chem_name"].iloc[j].split())
    if len(str(table_6_19["raw_cas"].iloc[j]).split())>1:
        table_6_19["raw_cas"].iloc[j]=" ".join(str(table_6_19["raw_cas"].iloc[j]).split())

table_6_19["data_document_id"]="1372845"
table_6_19["data_document_filename"]="DCPS_102_h.pdf"
table_6_19["doc_date"]="2009"
table_6_19["raw_category"]=""
table_6_19["cat_code"]=""
table_6_19["description_cpcat"]=""
table_6_19["cpcat_code"]=""
table_6_19["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_19.to_csv("dcps_102_table_6_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 6.20
tables=read_pdf("document_1372846.pdf", pages="122,123", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_20=pd.concat([tables[1],tables[2]],ignore_index=True)
table_6_20["raw_cas"]=table_6_20.iloc[:,1]
table_6_20["raw_chem_name"]=table_6_20.iloc[:,0]
table_6_20=table_6_20.loc[table_6_20["raw_chem_name"]!= "Component"]
table_6_20=table_6_20.loc[table_6_20["raw_cas"]!= "Product no."]
table_6_20=table_6_20[["raw_chem_name","raw_cas"]]
table_6_20=table_6_20.dropna(how="all")
table_6_20=table_6_20.reset_index()
table_6_20=table_6_20[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_20)):
    table_6_20["raw_chem_name"].iloc[j]=str(table_6_20["raw_chem_name"].iloc[j]).strip().lower().replace(".",",")
    table_6_20["raw_chem_name"].iloc[j]=clean(str(table_6_20["raw_chem_name"].iloc[j]))
    if len(table_6_20["raw_chem_name"].iloc[j].split())>1:
        table_6_20["raw_chem_name"].iloc[j]=" ".join(table_6_20["raw_chem_name"].iloc[j].split())
    if len(str(table_6_20["raw_cas"].iloc[j]).split())>1:
        table_6_20["raw_cas"].iloc[j]=" ".join(str(table_6_20["raw_cas"].iloc[j]).split())

table_6_20["data_document_id"]="1372846"
table_6_20["data_document_filename"]="DCPS_102_i.pdf"
table_6_20["doc_date"]="2009"
table_6_20["raw_category"]=""
table_6_20["cat_code"]=""
table_6_20["description_cpcat"]=""
table_6_20["cpcat_code"]=""
table_6_20["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_20.to_csv("dcps_102_table_6_20.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
