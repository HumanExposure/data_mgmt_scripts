#lkoval
#8-29-19

import pandas as pd
from tabula import read_pdf
import string

#Table 3.1
table_3_1=read_pdf("document_1395325.pdf", pages="18-21", lattice=True, pandas_options={'header': None})
table_3_1["raw_chem_name"]=table_3_1.iloc[4:,0]
table_3_1["raw_category"]=table_3_1.iloc[4:,4]
table_3_1=table_3_1[["raw_chem_name","raw_category",]]
table_3_1=table_3_1.loc[table_3_1.raw_chem_name!="Compound"]
table_3_1=table_3_1.dropna(subset=["raw_chem_name"], how="all")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_3_1.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace(".","")
    rows.raw_chem_name=clean(rows.raw_chem_name)
    rows.raw_category=rows.raw_category.strip().lower().replace(".","")
    rows.raw_category=clean(rows.raw_category)
    if len(rows.raw_chem_name.split())>1:
        rows.raw_chem_name=" ".join(rows.raw_chem_name.split())
    if len(rows.raw_category.split())>1:
        rows.raw_category=" ".join(rows.raw_category.split())


table_3_1["raw_cas"]=""
table_3_1["data_document_id"]="1395325"
table_3_1["data_document_filename"]="UK_Pharm_Use_orig_a.pdf"
table_3_1["doc_date"]="November 2007"
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_1["report_funcuse"]=""

table_3_1.to_csv("pharms_in_drinking_water_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 4.2
table_4_2=read_pdf("document_1395326.pdf", pages="37", lattice=True, pandas_options={'header': None})
table_4_2["raw_chem_name"]=table_4_2.iloc[:,0]
table_4_2["raw_category"]=table_4_2.iloc[:,1]
table_4_2=table_4_2[["raw_chem_name","raw_category"]]
table_4_2=table_4_2.loc[table_4_2.raw_chem_name!="Compound"]
table_4_2=table_4_2.dropna(subset=["raw_chem_name"], how="all")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_4_2.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace(".","")
    rows.raw_chem_name=clean(rows.raw_chem_name)
    rows.raw_category=rows.raw_category.strip().lower().replace(".","")
    rows.raw_category=clean(rows.raw_category)
    if len(rows.raw_chem_name.split())>1:
        rows.raw_chem_name=" ".join(rows.raw_chem_name.split())
    if len(rows.raw_category.split())>1:
        rows.raw_category=" ".join(rows.raw_category.split())


table_4_2["raw_cas"]=""
table_4_2["data_document_id"]="1395326"
table_4_2["data_document_filename"]="UK_Pharm_Use_orig_b.pdf"
table_4_2["doc_date"]="November 2007"
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_2["report_funcuse"]=""

table_4_2.to_csv("pharms_in_drinking_water_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 4.4
table_4_4=read_pdf("document_1395327.pdf", pages="42", lattice=True, pandas_options={'header': None})
table_4_4["raw_chem_name"]=table_4_4.iloc[:,0]
table_4_4=table_4_4[["raw_chem_name"]]
table_4_4=table_4_4.loc[table_4_4.raw_chem_name!="Compound"]
table_4_4=table_4_4.dropna(subset=["raw_chem_name"], how="all")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_4_4.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace(".","")
    rows.raw_chem_name=clean(rows.raw_chem_name)
    if len(rows.raw_chem_name.split())>1:
        rows.raw_chem_name=" ".join(rows.raw_chem_name.split())

table_4_4["raw_cas"]=""
table_4_4["raw_category"]=""
table_4_4["data_document_id"]="1395327"
table_4_4["data_document_filename"]="UK_Pharm_Use_orig_c.pdf"
table_4_4["doc_date"]="November 2007"
table_4_4["cat_code"]=""
table_4_4["description_cpcat"]=""
table_4_4["cpcat_code"]=""
table_4_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_4["report_funcuse"]=""

table_4_4.to_csv("pharms_in_drinking_water_table_4_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.7
table_4_7=read_pdf("document_1395328.pdf", pages="47-48", lattice=True, pandas_options={'header': None})
table_4_7["raw_chem_name"]=table_4_7.iloc[:,0]
table_4_7["raw_category"]=table_4_7.iloc[:,1]
table_4_7=table_4_7[["raw_chem_name","raw_category"]]
table_4_7=table_4_7.loc[table_4_7.raw_chem_name!="Compound"]
table_4_7=table_4_7.loc[table_4_7.raw_chem_name.str.isdigit()==False]
table_4_7=table_4_7.dropna(subset=["raw_chem_name"], how="all")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_4_7.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace(".","")
    rows.raw_chem_name=clean(rows.raw_chem_name)
    rows.raw_category=rows.raw_category.strip().lower().replace(".","")
    rows.raw_category=clean(rows.raw_category)

    if len(rows.raw_chem_name.split())>1:
        rows.raw_chem_name=" ".join(rows.raw_chem_name.split())
    if len(rows.raw_category.split())>1:
        rows.raw_category=" ".join(rows.raw_category.split())

table_4_7["raw_cas"]=""
table_4_7["data_document_id"]="1395328"
table_4_7["data_document_filename"]="UK_Pharm_Use_orig_d.pdf"
table_4_7["doc_date"]="November 2007"
table_4_7["cat_code"]=""
table_4_7["description_cpcat"]=""
table_4_7["cpcat_code"]=""
table_4_7["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_7["report_funcuse"]=""

table_4_7.to_csv("pharms_in_drinking_water_table_4_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 5.1
table_5_1=read_pdf("document_1395329.pdf", pages="61-62", lattice=False, pandas_options={'header': None})
table_5_1["raw_chem_name"]=table_5_1.iloc[:,0]
table_5_1=table_5_1[["raw_chem_name"]]
table_5_1=table_5_1.loc[table_5_1.raw_chem_name!="Name"]
table_5_1=table_5_1.dropna(subset=["raw_chem_name"], how="all")
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_5_1.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace(".","")
    rows.raw_chem_name=clean(rows.raw_chem_name)

table_5_1=table_5_1.drop([15,37,38])

table_5_1["raw_category"]=""
table_5_1["raw_cas"]=""
table_5_1["data_document_id"]="1395329"
table_5_1["data_document_filename"]="UK_Pharm_Use_orig_e.pdf"
table_5_1["doc_date"]="November 2007"
table_5_1["cat_code"]=""
table_5_1["description_cpcat"]=""
table_5_1["cpcat_code"]=""
table_5_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5_1["report_funcuse"]=""

table_5_1.to_csv("pharms_in_drinking_water_table_5_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5.2
table_5_2=read_pdf("document_1395330.pdf", pages="63", lattice=True, pandas_options={'header': None})
table_5_2["raw_chem_name"]=table_5_2.iloc[:,0]
table_5_2=table_5_2[["raw_chem_name"]]
table_5_2=table_5_2.loc[table_5_2.raw_chem_name!="Compound"]
table_5_2=table_5_2.dropna(subset=["raw_chem_name"], how="all")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_5_2.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace("1","")
    rows.raw_chem_name=clean(rows.raw_chem_name)

table_5_2["raw_category"]=""
table_5_2["raw_cas"]=""
table_5_2["data_document_id"]="1395330"
table_5_2["data_document_filename"]="UK_Pharm_Use_orig_f.pdf"
table_5_2["doc_date"]="November 2007"
table_5_2["cat_code"]=""
table_5_2["description_cpcat"]=""
table_5_2["cpcat_code"]=""
table_5_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5_2["report_funcuse"]=""

table_5_2.to_csv("pharms_in_drinking_water_table_5_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 6.1
table_6_1=read_pdf("document_1395331.pdf", pages="64", lattice=True, pandas_options={'header': None})
table_6_1["raw_chem_name"]=table_6_1.iloc[:,0]
table_6_1=table_6_1[["raw_chem_name"]]
table_6_1=table_6_1.dropna(subset=["raw_chem_name"], how="all")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_6_1.iterrows():
    rows.raw_chem_name=rows.raw_chem_name.strip().lower().replace("1","")
    rows.raw_chem_name=clean(rows.raw_chem_name)

table_6_1["raw_category"]=""
table_6_1["raw_cas"]=""
table_6_1["data_document_id"]="1395331"
table_6_1["data_document_filename"]="UK_Pharm_Use_orig_g.pdf"
table_6_1["doc_date"]="November 2007"
table_6_1["cat_code"]=""
table_6_1["description_cpcat"]=""
table_6_1["cpcat_code"]=""
table_6_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_1["report_funcuse"]=""

table_6_1.to_csv("pharms_in_drinking_water_table_6_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 6.6
table_6_6=read_pdf("document_1395332.pdf", pages="68-69", lattice=True, pandas_options={'header': None})
table_6_6["raw_chem_name"]=table_6_6.iloc[:,0]
table_6_6["temp"]=table_6_6.iloc[:,1]
table_6_6["raw_category"]=""
table_6_6=table_6_6[["raw_chem_name","temp","raw_category"]]
table_6_6=table_6_6.dropna(subset=["raw_chem_name"], how="all")

cat_list=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for index, rows in table_6_6.iterrows():
    if pd.isna(rows.temp):
        cat=clean(rows.raw_chem_name.strip().lower())
        cat_list.append(cat)

    rows.raw_chem_name=rows.raw_chem_name.strip().lower()
    rows.raw_chem_name=clean(rows.raw_chem_name)
    rows.raw_category=cat
    if len(rows.raw_chem_name.split())>1:
        rows.raw_chem_name=" ".join(rows.raw_chem_name.split())

del cat_list[len(cat_list)-1]
table_6_6=table_6_6[["raw_chem_name","raw_category"]]
for category in cat_list:
    table_6_6=table_6_6.loc[table_6_6.raw_chem_name!=category]
table_6_6.raw_chem_name[23]=table_6_6.raw_chem_name[23]+table_6_6.raw_chem_name[27]
table_6_6=table_6_6.drop(27)

table_6_6["raw_cas"]=""
table_6_6["data_document_id"]="1395332"
table_6_6["data_document_filename"]="UK_Pharm_Use_orig_h.pdf"
table_6_6["doc_date"]="November 2007"
table_6_6["cat_code"]=""
table_6_6["description_cpcat"]=""
table_6_6["cpcat_code"]=""
table_6_6["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_6["report_funcuse"]=""

table_6_6.to_csv("pharms_in_drinking_water_table_6_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
