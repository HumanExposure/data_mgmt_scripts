#lkoval
#5/28/19

from tabula import read_pdf
import pandas as pd
import string

#Table 6
table_6=read_pdf("document_1372607.pdf", pages="26", lattice=False, pandas_options={'header': None})
table_6["raw_chem_name"]=table_6.iloc[:,0]
table_6["raw_cas"]=table_6.iloc[:,2]
table_6=table_6.loc[table_6["raw_cas"]!= "CAS no."]
table_6=table_6.dropna(subset=["raw_chem_name","raw_cas"],how="all")
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]

nameDrop=["Fillers","Retention agents","Dry strength agents","Wet strength agents","Dyes/coating","Biocides"]
nameDropList=[]
for i in range(0,len(table_6)):
    if table_6["raw_chem_name"].iloc[i] in nameDrop:
        nameDropList.append(i)

table_6=table_6.drop(nameDropList)
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower()
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if table_6["raw_chem_name"].iloc[j][0]=="-":
        table_6["raw_chem_name"].iloc[j]=table_6["raw_chem_name"].iloc[j][1:]

table_6["raw_chem_name"].iloc[6]=table_6["raw_chem_name"].iloc[6]+table_6["raw_chem_name"].iloc[7]
table_6["raw_chem_name"].iloc[19]=table_6["raw_chem_name"].iloc[19]+table_6["raw_chem_name"].iloc[20]
table_6=table_6.drop([7,20])
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]

table_6["data_document_id"]="1372607"
table_6["data_document_filename"]="DCPS_34_b.pdf"
table_6["doc_date"]="2003"
table_6["raw_category"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6.to_csv("dcps_34_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 9
table_9=read_pdf("document_1372608.pdf", pages="32,33", lattice=False, pandas_options={'header': None})
table_9["raw_chem_name"]=table_9.iloc[:,0]
table_9["flag"]=table_9.iloc[:,1]
table_9=table_9.loc[table_9["raw_chem_name"]!= "Component"]
table_9=table_9.dropna(subset=["raw_chem_name"])
table_9=table_9.reset_index()
table_9=table_9[["raw_chem_name","flag"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_9)):
    table_9["raw_chem_name"].iloc[j]=str(table_9["raw_chem_name"].iloc[j]).strip().lower().strip("*")
    table_9["raw_chem_name"].iloc[j]=clean(str(table_9["raw_chem_name"].iloc[j]))
    if str(table_9["flag"].iloc[j])=="nan":
        table_9["raw_chem_name"].iloc[j]=table_9["raw_chem_name"].iloc[j-1]+" "+table_9["raw_chem_name"].iloc[j]
        j_drop.append(j-1)

table_9=table_9[["raw_chem_name"]]
table_9=table_9.drop(j_drop)
table_9=table_9.drop_duplicates()
table_9=table_9.reset_index()
table_9=table_9[["raw_chem_name"]]

table_9["data_document_id"]="1372608"
table_9["data_document_filename"]="DCPS_34_c.pdf"
table_9["doc_date"]="2003"
table_9["raw_category"]=""
table_9["cat_code"]=""
table_9["description_cpcat"]=""
table_9["cpcat_code"]=""
table_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_9.to_csv("dcps_34_table_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.4.9
table_5_4_9=read_pdf("document_1372611.pdf", pages="37", lattice=False, pandas_options={'header': None})
table_5_4_9["raw_chem_name"]=table_5_4_9.iloc[4:,0]
table_5_4_9["flag"]=table_5_4_9.iloc[4:,1]
table_5_4_9=table_5_4_9.loc[table_5_4_9["raw_chem_name"]!= "Component"]
table_5_4_9=table_5_4_9.dropna(subset=["raw_chem_name"])
table_5_4_9=table_5_4_9.reset_index()
table_5_4_9=table_5_4_9[["raw_chem_name","flag"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_4_9)):
    table_5_4_9["raw_chem_name"].iloc[j]=str(table_5_4_9["raw_chem_name"].iloc[j]).strip().lower().strip("*")
    table_5_4_9["raw_chem_name"].iloc[j]=clean(str(table_5_4_9["raw_chem_name"].iloc[j]))
    if str(table_5_4_9["flag"].iloc[j])=="nan":
        table_5_4_9["raw_chem_name"].iloc[j]=table_5_4_9["raw_chem_name"].iloc[j-1]+" "+table_5_4_9["raw_chem_name"].iloc[j]
        j_drop.append(j-1)

table_5_4_9=table_5_4_9[["raw_chem_name"]]
table_5_4_9=table_5_4_9.drop(j_drop)
table_5_4_9=table_5_4_9.drop_duplicates()
table_5_4_9=table_5_4_9.reset_index()
table_5_4_9=table_5_4_9[["raw_chem_name"]]

table_5_4_9["data_document_id"]="1372611"
table_5_4_9["data_document_filename"]="DCPS_34_f.pdf"
table_5_4_9["doc_date"]="2003"
table_5_4_9["raw_category"]=""
table_5_4_9["cat_code"]=""
table_5_4_9["description_cpcat"]=""
table_5_4_9["cpcat_code"]=""
table_5_4_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_4_9.to_csv("dcps_34_table_5_4_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.4.10
table_5_4_10=read_pdf("document_1372612.pdf", pages="38", lattice=False, pandas_options={'header': None})
table_5_4_10["raw_chem_name"]=table_5_4_10.iloc[4:,0]
table_5_4_10["flag"]=table_5_4_10.iloc[4:,1]
table_5_4_10=table_5_4_10.loc[table_5_4_10["raw_chem_name"]!= "Component"]
table_5_4_10=table_5_4_10.dropna(subset=["raw_chem_name"])
table_5_4_10=table_5_4_10.reset_index()
table_5_4_10=table_5_4_10[["raw_chem_name","flag"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_4_10)):
    table_5_4_10["raw_chem_name"].iloc[j]=str(table_5_4_10["raw_chem_name"].iloc[j]).strip().lower().strip("*")
    table_5_4_10["raw_chem_name"].iloc[j]=clean(str(table_5_4_10["raw_chem_name"].iloc[j]))
    if str(table_5_4_10["flag"].iloc[j])=="nan":
        table_5_4_10["raw_chem_name"].iloc[j]=table_5_4_10["raw_chem_name"].iloc[j-1]+" "+table_5_4_10["raw_chem_name"].iloc[j]
        j_drop.append(j-1)

table_5_4_10=table_5_4_10[["raw_chem_name"]]
table_5_4_10=table_5_4_10.drop(j_drop)
table_5_4_10=table_5_4_10.drop_duplicates()
table_5_4_10=table_5_4_10.reset_index()
table_5_4_10=table_5_4_10[["raw_chem_name"]]

table_5_4_10["data_document_id"]="1372612"
table_5_4_10["data_document_filename"]="DCPS_34_g.pdf"
table_5_4_10["doc_date"]="2003"
table_5_4_10["raw_category"]=""
table_5_4_10["cat_code"]=""
table_5_4_10["description_cpcat"]=""
table_5_4_10["cpcat_code"]=""
table_5_4_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_4_10.to_csv("dcps_34_table_5_4_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 13
table_13=read_pdf("document_1372613.pdf", pages="42", lattice=True, pandas_options={'header': None})
table_13["raw_chem_name"]=table_13.iloc[1:,0]
table_13["raw_cas"]=table_13.iloc[1:,1]
table_13=table_13.dropna(subset=["raw_chem_name"])
table_13=table_13.reset_index()
table_13=table_13[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_13)):
    table_13["raw_chem_name"].iloc[j]=str(table_13["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("#","").replace("^","")
    table_13["raw_chem_name"].iloc[j]=clean(str(table_13["raw_chem_name"].iloc[j]))
    if len(table_13["raw_chem_name"].iloc[j].split())>1:
        table_13["raw_chem_name"].iloc[j]=" ".join(table_13["raw_chem_name"].iloc[j].split())
    if len(str(table_13["raw_cas"].iloc[j]).split())>1:
        table_13["raw_cas"].iloc[j]=" ".join(str(table_13["raw_cas"].iloc[j]).split())


table_13["data_document_id"]="1372613"
table_13["data_document_filename"]="DCPS_34_h.pdf"
table_13["doc_date"]="2003"
table_13["raw_category"]=""
table_13["cat_code"]=""
table_13["description_cpcat"]=""
table_13["cpcat_code"]=""
table_13["cpcat_sourcetype"]="ACToR Assays and Lists"

table_13.to_csv("dcps_34_table_13.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
