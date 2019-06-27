#lkoval
#6-27-19

from tabula import read_pdf
import pandas as pd
import string

#Table 2
table_2=read_pdf("document_1374766.pdf", pages="21", lattice=False, pandas_options={'header': None})
table_2["raw_chem_name"]=table_2.iloc[:,0]
table_2["raw_cas"]=table_2.iloc[:,1]
table_2=table_2.loc[table_2["raw_chem_name"]!="Substance name"]
table_2=table_2.loc[table_2["raw_chem_name"]!="Sum VOC"]
table_2=table_2.dropna(subset=["raw_chem_name"])
table_2=table_2.reset_index()
table_2=table_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))

table_2["data_document_id"]="1374766"
table_2["data_document_filename"]="DCPS_154_a.pdf"
table_2["doc_date"]="2012"
table_2["raw_category"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2["report_funcuse"]=""

table_2.to_csv("dcps_154_table_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 3
table_3=read_pdf("document_1374767.pdf", pages="23", lattice=False, pandas_options={'header': None})
table_3["raw_chem_name"]=table_3.iloc[:,0]
table_3["raw_cas"]=table_3.iloc[:,1]
table_3=table_3.loc[table_3["raw_chem_name"]!="Measured VOCs"]
table_3=table_3.loc[table_3["raw_chem_name"]!="Sum VOC"]
table_3=table_3.dropna(subset=["raw_chem_name"])
table_3=table_3.reset_index()
table_3=table_3[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3["raw_chem_name"].iloc[j]=clean(str(table_3["raw_chem_name"].iloc[j]))
    if str(table_3["raw_cas"].iloc[j])=="nan":
        table_3["raw_chem_name"].iloc[j]=table_3["raw_chem_name"].iloc[j-1]+table_3["raw_chem_name"].iloc[j]
        table_3["raw_cas"].iloc[j]=table_3["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_3=table_3.drop(j_drop)
table_3=table_3.reset_index()
table_3=table_3[["raw_chem_name","raw_cas"]]

table_3["data_document_id"]="1374767"
table_3["data_document_filename"]="DCPS_154_b.pdf"
table_3["doc_date"]="2012"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3["report_funcuse"]=""

table_3.to_csv("dcps_154_table_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4
table_4=read_pdf("document_1374768.pdf", pages="25", lattice=False, pandas_options={'header': None})
table_4["raw_chem_name"]=table_4.iloc[:,0]
table_4["raw_cas"]=table_4.iloc[:,1]
table_4=table_4.loc[table_4["raw_chem_name"]!="Volatile substances"]
table_4=table_4.loc[table_4["raw_chem_name"]!="Sum VOC"]
table_4=table_4.dropna(subset=["raw_chem_name"])
table_4=table_4.reset_index()
table_4=table_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))

table_4["data_document_id"]="1374768"
table_4["data_document_filename"]="DCPS_154_c.pdf"
table_4["doc_date"]="2012"
table_4["raw_category"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4["report_funcuse"]=""

table_4.to_csv("dcps_154_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5
table_5=read_pdf("document_1374769.pdf", pages="26", lattice=False, pandas_options={'header': None})
table_5["raw_chem_name"]=table_5.iloc[:,0]
table_5["raw_cas"]=table_5.iloc[:,1]
table_5=table_5.loc[table_5["raw_chem_name"]!="Substance"]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5.reset_index()
table_5=table_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))

table_5["data_document_id"]="1374769"
table_5["data_document_filename"]="DCPS_154_d.pdf"
table_5["doc_date"]="2012"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5["report_funcuse"]=""

table_5.to_csv("dcps_154_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6
table_6=read_pdf("document_1374770.pdf", pages="27", lattice=False, pandas_options={'header': None})
table_6["raw_chem_name"]=table_6.iloc[:,0]
table_6["raw_cas"]=table_6.iloc[:,3]
table_6=table_6.loc[table_6["raw_chem_name"]!="Substance"]
table_6=table_6.loc[table_6["raw_chem_name"]!="1"]
table_6=table_6.loc[table_6["raw_chem_name"]!="2"]
table_6=table_6.dropna(subset=["raw_chem_name"])
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if str(table_6["raw_cas"].iloc[j])=="nan":
        table_6["raw_chem_name"].iloc[j]=table_6["raw_chem_name"].iloc[j-1]+" "+table_6["raw_chem_name"].iloc[j]
        table_6["raw_cas"].iloc[j]=table_6["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_6=table_6.drop(j_drop)
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]
table_6["raw_chem_name"].iloc[4]=table_6["raw_chem_name"].iloc[4]+" (dehp)"

table_6["data_document_id"]="1374770"
table_6["data_document_filename"]="DCPS_154_e.pdf"
table_6["doc_date"]="2012"
table_6["raw_category"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6["report_funcuse"]=""

table_6.to_csv("dcps_154_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
