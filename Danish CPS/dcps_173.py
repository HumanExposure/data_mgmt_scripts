#lkoval
#8-30-19

import pandas as pd
from tabula import read_pdf
import string


#Table 4
table_4=read_pdf("document_1374312.pdf", pages="41", lattice=False, pandas_options={'header': None})
table_4["raw_chem_name"]=table_4.iloc[:,0]

table_4=table_4[["raw_chem_name"]]
table_4=table_4.loc[table_4.raw_chem_name!="Unit: mg/kg"]
table_4=table_4.loc[table_4.raw_chem_name!="Metal"]
table_4=table_4.dropna()
table_4=table_4.reset_index()
table_4=table_4[["raw_chem_name"]]

table_4.raw_chem_name=table_4.raw_chem_name.str.lower().str.strip()
drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_4)):
    if len(table_4.raw_chem_name.iloc[i].split())==1 and "," not in table_4.raw_chem_name.iloc[i]:
        table_4.raw_chem_name.iloc[i]=table_4.raw_chem_name.iloc[i-1]+" "+table_4.raw_chem_name.iloc[i]
        drop_list.append(i-1)
    table_4.raw_chem_name.iloc[i]=clean(table_4.raw_chem_name.iloc[i])

table_4=table_4.drop(drop_list)

table_4["raw_category"]=""
table_4["data_document_id"]="1374312"
table_4["data_document_filename"]="table4.pdf"
table_4["doc_date"]="December 2018"
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]=""
table_4["report_funcuse"]=""

table_4.to_csv("dcps_173_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6
table_6=read_pdf("document_1374314.pdf", pages="45-46", lattice=False, pandas_options={'header': None})
table_6=table_6.iloc[:-3,:]
table_6["raw_chem_name"]=table_6.iloc[:,0]
table_6["raw_cas"]=table_6.iloc[:,1]

table_6=table_6[["raw_chem_name","raw_cas"]]
table_6=table_6.loc[table_6.raw_chem_name!="Substance"]
table_6=table_6.loc[table_6.raw_chem_name!="Unit: mg/kg"]
table_6=table_6.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]

table_6.raw_chem_name=table_6.raw_chem_name.str.lower().str.strip()
drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_6)):
    if pd.isnull(table_6.raw_cas.iloc[i]):
        table_6.raw_chem_name.iloc[i]=table_6.raw_chem_name.iloc[i-1]+" "+table_6.raw_chem_name.iloc[i]
        table_6.raw_cas.iloc[i]=table_6.raw_cas.iloc[i-1]
        drop_list.append(i-1)
    table_6.raw_chem_name.iloc[i]=clean(table_6.raw_chem_name.iloc[i])

table_6=table_6.drop(drop_list)

table_6["raw_category"]=""
table_6["data_document_id"]="1374314"
table_6["data_document_filename"]="table6.pdf"
table_6["doc_date"]="December 2018"
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]=""
table_6["report_funcuse"]=""

table_6.to_csv("dcps_173_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 7
table_7=read_pdf("document_1374315.pdf", pages="47", lattice=False, pandas_options={'header': None})
table_7=table_7.iloc[:30,:]
table_7["raw_chem_name"]=table_7.iloc[:,0]
table_7["raw_cas"]=table_7.iloc[:,1]

table_7=table_7[["raw_chem_name","raw_cas"]]
table_7=table_7.loc[table_7.raw_chem_name!="Substance CAS no."]
table_7=table_7.loc[table_7.raw_chem_name!="Unit: mg/kg"]
table_7=table_7.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_7=table_7[["raw_chem_name","raw_cas"]]

table_7.raw_chem_name=table_7.raw_chem_name.str.lower().str.strip().str.replace("α","alpha")
table_7.loc[table_7.raw_chem_name.str.contains("\d{0,7}-{1}\d{2}-\d{1}"), ["raw_cas"]]=table_7.raw_chem_name.str.extract("(\d{0,7}-{1}\d{2}-\d{1})", expand=False)
table_7.raw_chem_name=table_7.raw_chem_name.str.replace("(\d{0,7}-{1}\d{2}-\d{1})", "")

table_7=table_7.reset_index()
table_7=table_7[["raw_chem_name","raw_cas"]]

drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_7)):
    if pd.isnull(table_7.raw_cas.iloc[i]):
        table_7.raw_chem_name.iloc[i]=" ".join(table_7.raw_chem_name.iloc[i-1].split())+" "+table_7.raw_chem_name.iloc[i]
        table_7.raw_cas.iloc[i]=table_7.raw_cas.iloc[i-1]
        drop_list.append(i-1)
    elif table_7.raw_cas.iloc[i].isdigit():
        table_7.raw_chem_name.iloc[i]= " ".join(table_7.raw_chem_name.iloc[i].split("-"))
        table_7.raw_cas.iloc[i]="-"
    table_7.raw_chem_name.iloc[i]=clean(table_7.raw_chem_name.iloc[i])

table_7=table_7.drop(drop_list)
table_7=table_7.reset_index()
table_7=table_7[["raw_chem_name","raw_cas"]]

table_7["raw_category"]=""
table_7["data_document_id"]="1374315"
table_7["data_document_filename"]="table7.pdf"
table_7["doc_date"]="December 2018"
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]=""
table_7["report_funcuse"]=""

table_7.to_csv("dcps_173_table_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 8
table_8=read_pdf("document_1374316.pdf", pages="47-48", lattice=False, pandas_options={'header': None})
table_8=table_8.iloc[36:68,:]
table_8["raw_chem_name"]=table_8.iloc[:,0]
table_8["raw_cas"]=table_8.iloc[:,1]

table_8=table_8[["raw_chem_name","raw_cas"]]
table_8=table_8.loc[table_8.raw_chem_name!="Substance CAS no."]
table_8=table_8.loc[table_8.raw_chem_name!="Unit: mg/kg"]
table_8=table_8.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_8=table_8[["raw_chem_name","raw_cas"]]

table_8.raw_chem_name=table_8.raw_chem_name.str.lower().str.strip().str.replace("α","alpha")
table_8.loc[table_8["raw_chem_name"].str.contains("\d{0,7}-{1}\d{2}-\d{1}"), ["raw_cas"]]=table_8.raw_chem_name.str.extract("(\d{0,7}-{1}\d{2}-\d{1})", expand=False)
table_8.raw_chem_name=table_8.raw_chem_name.str.replace("(\d{0,7}-{1}\d{2}-\d{1})", "")

table_8=table_8.reset_index()
table_8=table_8[["raw_chem_name","raw_cas"]]

drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_8)):
    if pd.isnull(table_8.raw_cas.iloc[i]):
        table_8.raw_chem_name.iloc[i]=" ".join(table_8.raw_chem_name.iloc[i-1].split())+" "+table_8.raw_chem_name.iloc[i]
        table_8.raw_cas.iloc[i]=table_8.raw_cas.iloc[i-1]
        drop_list.append(i-1)
    elif table_8.raw_cas.iloc[i].isdigit():
        table_8.raw_chem_name.iloc[i]= " ".join(table_8.raw_chem_name.iloc[i].split("-"))
        table_8.raw_cas.iloc[i]="-"
    table_8.raw_chem_name.iloc[i]=clean(table_8.raw_chem_name.iloc[i])

table_8=table_8.drop(drop_list)
table_8=table_8.reset_index()
table_8=table_8[["raw_chem_name","raw_cas"]]

table_8["raw_category"]=""
table_8["data_document_id"]="1374316"
table_8["data_document_filename"]="table8.pdf"
table_8["doc_date"]="December 2018"
table_8["cat_code"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]=""
table_8["report_funcuse"]=""

table_8.to_csv("dcps_173_table_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 9
table_9=read_pdf("document_1374317.pdf", pages="47-48", lattice=False, pandas_options={'header': None})
table_9=table_9.iloc[74:,:]
table_9["raw_chem_name"]=table_9.iloc[:,0]
table_9["raw_cas"]=table_9.iloc[:,1]

table_9=table_9[["raw_chem_name","raw_cas"]]
table_9=table_9.loc[table_9.raw_chem_name!="Substance CAS no."]
table_9=table_9.loc[table_9.raw_chem_name!="Unit: mg/kg"]
table_9=table_9.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_9=table_9[["raw_chem_name","raw_cas"]]

table_9.raw_chem_name=table_9.raw_chem_name.str.lower().str.strip().str.replace("α","alpha")
table_9.loc[table_9["raw_chem_name"].str.contains("\d{0,7}-{1}\d{2}-\d{1}"), ["raw_cas"]]=table_9.raw_chem_name.str.extract("(\d{0,7}-{1}\d{2}-\d{1})", expand=False)
table_9.raw_chem_name=table_9.raw_chem_name.str.replace("(\d{0,7}-{1}\d{2}-\d{1})", "")

table_9=table_9.reset_index()
table_9=table_9[["raw_chem_name","raw_cas"]]

drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_9)):
    if pd.isnull(table_9.raw_cas.iloc[i]):
        table_9.raw_chem_name.iloc[i]=" ".join(table_9.raw_chem_name.iloc[i-1].split())+" "+table_9.raw_chem_name.iloc[i]
        table_9.raw_cas.iloc[i]=table_9.raw_cas.iloc[i-1]
        drop_list.append(i-1)
    elif table_9.raw_cas.iloc[i].isdigit():
        table_9.raw_chem_name.iloc[i]= " ".join(table_9.raw_chem_name.iloc[i].split("-"))
        table_9.raw_cas.iloc[i]="-"
    table_9.raw_chem_name.iloc[i]=clean(table_9.raw_chem_name.iloc[i])

table_9=table_9.drop(drop_list)
table_9=table_9.reset_index()
table_9=table_9[["raw_chem_name","raw_cas"]]

table_9["raw_category"]=""
table_9["data_document_id"]="1374317"
table_9["data_document_filename"]="table9.pdf"
table_9["doc_date"]="December 2018"
table_9["cat_code"]=""
table_9["description_cpcat"]=""
table_9["cpcat_code"]=""
table_9["cpcat_sourcetype"]=""
table_9["report_funcuse"]=""

table_9.to_csv("dcps_173_table_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 10
table_10=read_pdf("document_1374318.pdf", pages="49", lattice=False, pandas_options={'header': None})
table_10=table_10.iloc[:15,:]
table_10["raw_chem_name"]=table_10.iloc[:,0]
table_10["raw_cas"]=table_10.iloc[:,1]

table_10=table_10[["raw_chem_name","raw_cas"]]
table_10=table_10.loc[table_10.raw_chem_name!="Substance"]
table_10=table_10.loc[table_10.raw_chem_name!="Unit: mg/kg"]
table_10=table_10.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_10=table_10.reset_index()
table_10=table_10[["raw_chem_name","raw_cas"]]
table_10.raw_chem_name=table_10.raw_chem_name.str.lower().str.strip().str.replace("α","alpha")

drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_10)):
    if pd.isnull(table_10.raw_cas.iloc[i]):
        table_10.raw_chem_name.iloc[i]=" ".join(table_10.raw_chem_name.iloc[i-1].split())+" "+table_10.raw_chem_name.iloc[i]
        table_10.raw_cas.iloc[i]=table_10.raw_cas.iloc[i-1]
        drop_list.append(i-1)
    table_10.raw_chem_name.iloc[i]=clean(table_10.raw_chem_name.iloc[i])

table_10=table_10.drop(drop_list)
table_10=table_10.reset_index()
table_10=table_10[["raw_chem_name","raw_cas"]]

table_10["raw_category"]=""
table_10["data_document_id"]="1374318"
table_10["data_document_filename"]="table10.pdf"
table_10["doc_date"]="December 2018"
table_10["cat_code"]=""
table_10["description_cpcat"]=""
table_10["cpcat_code"]=""
table_10["cpcat_sourcetype"]=""
table_10["report_funcuse"]=""

table_10.to_csv("dcps_173_table_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 13
table_13=read_pdf("document_1374320.pdf", pages="56", lattice=False, pandas_options={'header': None})
table_13=table_13.iloc[:10,:]
table_13["raw_chem_name"]=table_13.iloc[:,0]
table_13["raw_cas"]=table_13.iloc[:,1]

table_13=table_13[["raw_chem_name","raw_cas"]]
table_13=table_13.loc[table_13.raw_chem_name!="Substance CAS no."]
table_13=table_13.loc[table_13.raw_chem_name!="Unit: mg/kg"]
table_13=table_13.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_13=table_13[["raw_chem_name","raw_cas"]]

table_13.raw_chem_name=table_13.raw_chem_name.str.lower().str.strip().str.replace("α","alpha")
table_13.loc[table_13["raw_chem_name"].str.contains("\d{0,7}-{1}\d{2}-\d{1}"), ["raw_cas"]]=table_13.raw_chem_name.str.extract("(\d{0,7}-{1}\d{2}-\d{1})", expand=False)
table_13.raw_chem_name=table_13.raw_chem_name.str.replace("(\d{0,7}-{1}\d{2}-\d{1})", "")

table_13=table_13.reset_index()
table_13=table_13[["raw_chem_name","raw_cas"]]

drop_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(len(table_13)):
    if pd.isnull(table_13.raw_cas.iloc[i]):
        table_13.raw_chem_name.iloc[i]=" ".join(table_13.raw_chem_name.iloc[i-1].split())+" "+table_13.raw_chem_name.iloc[i]
        table_13.raw_cas.iloc[i]=table_13.raw_cas.iloc[i-1]
        drop_list.append(i-1)
    elif table_13.raw_cas.iloc[i].isdigit():
        table_13.raw_chem_name.iloc[i]= " ".join(table_13.raw_chem_name.iloc[i].split("-"))
        table_13.raw_cas.iloc[i]="-"
    table_13.raw_chem_name.iloc[i]=clean(table_13.raw_chem_name.iloc[i])


table_13.raw_chem_name.iloc[5]=table_13.raw_chem_name.iloc[5]+table_13.raw_chem_name.iloc[7]
table_13.raw_cas.iloc[5]=table_13.raw_cas.iloc[7]
drop_list.append(6)
drop_list.append(7)
table_13=table_13.drop(drop_list)
table_13=table_13.reset_index()
table_13=table_13[["raw_chem_name","raw_cas"]]

table_13["raw_category"]=""
table_13["data_document_id"]="1374320"
table_13["data_document_filename"]="table10.pdf"
table_13["doc_date"]="December 2018"
table_13["cat_code"]=""
table_13["description_cpcat"]=""
table_13["cpcat_code"]=""
table_13["cpcat_sourcetype"]=""
table_13["report_funcuse"]=""

table_13.to_csv("dcps_173_table_13.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
