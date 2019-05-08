#lkoval
#5-8-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.1
table_3_1=read_pdf("document_1372275.pdf", pages="35,36,37", lattice=False, pandas_options={'header': None})
table_3_1=table_3_1.dropna(how="all")
table_3_1["raw_cas"]=table_3_1.iloc[4:,4]
table_3_1["raw_chem_name"]=table_3_1.iloc[4:,3]
table_3_1=table_3_1.loc[table_3_1["raw_cas"]!= "CAS no."]
table_3_1=table_3_1.dropna(subset=["raw_chem_name"])
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[i]=clean(str(table_3_1["raw_chem_name"].iloc[i]))
    table_3_1["raw_chem_name"].iloc[i]=str(table_3_1["raw_chem_name"].iloc[i]).strip().lower()
    if str(table_3_1["raw_chem_name"].iloc[i]).split()[0]=="no" or str(table_3_1["raw_chem_name"].iloc[i]).split()[0]=="been":
        i_drop.append(i)

table_3_1=table_3_1.drop(i_drop)
table_3_1=table_3_1.reset_index()

names_to_ignore=["fluor polymer", "silicone","paraffines","wax","contains petroleum distillates","methanol","mixture of heptane-isomers","non-aromatic gas"]
j_drop=[]
for j in range(0, len(table_3_1)):
    if str(table_3_1["raw_cas"].iloc[j])=="nan" and str(table_3_1["raw_chem_name"].iloc[j]) not in names_to_ignore:
        table_3_1["raw_chem_name"].iloc[j]=table_3_1["raw_chem_name"].iloc[j-1]+" "+table_3_1["raw_chem_name"].iloc[j]
        table_3_1["raw_cas"].iloc[j]=table_3_1["raw_cas"].iloc[j-1]
        j_drop.append(j-1)


table_3_1=table_3_1.drop(j_drop)
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]
table_3_1=table_3_1.drop_duplicates()
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]

table_3_1["data_document_id"]="1372275"
table_3_1["data_document_filename"]="DCPS_98_a.pdf"
table_3_1["doc_date"]="2008"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1.to_csv("dcps_98_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.2
tables=read_pdf("document_1372276.pdf", pages="50,51", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_2=pd.concat([tables[0],tables[1],tables[2]],ignore_index=True)
table_5_2["raw_cas"]=table_5_2.iloc[1:,1]
table_5_2["raw_chem_name"]=table_5_2.iloc[1:,0]
table_5_2=table_5_2.loc[table_5_2["raw_cas"]!= "CAS no."]
table_5_2=table_5_2.reset_index()
table_5_2=table_5_2[["raw_chem_name","raw_cas"]]
table_5_2=table_5_2.dropna(how="all")
table_5_2=table_5_2.reset_index()
table_5_2=table_5_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_5_2)):
    table_5_2["raw_chem_name"].iloc[i]=clean(str(table_5_2["raw_chem_name"].iloc[i]))
    table_5_2["raw_chem_name"].iloc[i]=str(table_5_2["raw_chem_name"].iloc[i]).strip().lower().strip("*")
    if len(table_5_2["raw_chem_name"].iloc[i].split())>1:
        table_5_2["raw_chem_name"].iloc[i]=" ".join(table_5_2["raw_chem_name"].iloc[i].split())
    if len(table_5_2["raw_cas"].iloc[i].split())>1:
        table_5_2["raw_cas"].iloc[i]=" ".join(table_5_2["raw_cas"].iloc[i].split())

table_5_2=table_5_2.drop_duplicates()
table_5_2=table_5_2.reset_index()
table_5_2=table_5_2[["raw_chem_name","raw_cas"]]

table_5_2["data_document_id"]="1372276"
table_5_2["data_document_filename"]="DCPS_98_b.pdf"
table_5_2["doc_date"]="2008"
table_5_2["raw_category"]=""
table_5_2["cat_code"]=""
table_5_2["description_cpcat"]=""
table_5_2["cpcat_code"]=""
table_5_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_2.to_csv("dcps_98_table_5_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.3
tables=read_pdf("document_1372277.pdf", pages="51,52", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_3=pd.concat([tables[1],tables[2]],ignore_index=True)
table_5_3["raw_cas"]=table_5_3.iloc[:,1]
table_5_3["raw_chem_name"]=table_5_3.iloc[:,0]
table_5_3=table_5_3.loc[table_5_3["raw_cas"]!= "CAS no."]
table_5_3=table_5_3.reset_index()
table_5_3=table_5_3[["raw_chem_name","raw_cas"]]
table_5_3=table_5_3.dropna(how="all")
table_5_3=table_5_3.reset_index()
table_5_3=table_5_3[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_5_3)):
    table_5_3["raw_chem_name"].iloc[i]=clean(str(table_5_3["raw_chem_name"].iloc[i]))
    table_5_3["raw_chem_name"].iloc[i]=str(table_5_3["raw_chem_name"].iloc[i]).strip().lower().strip("*")
    if len(table_5_3["raw_chem_name"].iloc[i].split())>1:
        table_5_3["raw_chem_name"].iloc[i]=" ".join(table_5_3["raw_chem_name"].iloc[i].split())
    if len(str(table_5_3["raw_cas"].iloc[i]).split())>1:
        table_5_3["raw_cas"].iloc[i]=" ".join(table_5_3["raw_cas"].iloc[i].split())

table_5_3["data_document_id"]="1372277"
table_5_3["data_document_filename"]="DCPS_98_c.pdf"
table_5_3["doc_date"]="2008"
table_5_3["raw_category"]=""
table_5_3["cat_code"]=""
table_5_3["description_cpcat"]=""
table_5_3["cpcat_code"]=""
table_5_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_3.to_csv("dcps_98_table_5_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 6.2
tables=read_pdf("document_1372278.pdf", pages="53,54", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_2=pd.concat([tables[1],tables[2],tables[3]],ignore_index=True)
table_6_2["raw_cas"]=table_6_2.iloc[:,1]
table_6_2["raw_chem_name"]=table_6_2.iloc[:,0]
table_6_2=table_6_2.loc[table_6_2["raw_cas"]!= "CAS no."]
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]
table_6_2=table_6_2.dropna(how="all")
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_6_2)):
    table_6_2["raw_chem_name"].iloc[i]=clean(str(table_6_2["raw_chem_name"].iloc[i]))
    table_6_2["raw_chem_name"].iloc[i]=str(table_6_2["raw_chem_name"].iloc[i]).strip().lower().strip("*")
    if len(table_6_2["raw_chem_name"].iloc[i].split())>1:
        table_6_2["raw_chem_name"].iloc[i]=" ".join(table_6_2["raw_chem_name"].iloc[i].split())
    if len(str(table_6_2["raw_cas"].iloc[i]).split())>1:
        table_6_2["raw_cas"].iloc[i]=" ".join(table_6_2["raw_cas"].iloc[i].split())

table_6_2=table_6_2.drop_duplicates()
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]

table_6_2["data_document_id"]="1372278"
table_6_2["data_document_filename"]="DCPS_98_d.pdf"
table_6_2["doc_date"]="2008"
table_6_2["raw_category"]=""
table_6_2["cat_code"]=""
table_6_2["description_cpcat"]=""
table_6_2["cpcat_code"]=""
table_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_2.to_csv("dcps_98_table_6_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
