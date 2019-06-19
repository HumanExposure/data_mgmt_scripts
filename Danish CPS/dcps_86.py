#lkoval
#6-19-19

from tabula import read_pdf
import pandas as pd
import string

#Table 2
table_2=read_pdf("document_1374297.pdf", pages="17", lattice=True, pandas_options={'header': None})
table_2["raw_chem_name"]=table_2.iloc[1:,0]
table_2=table_2.dropna(subset=["raw_chem_name"])
table_2=table_2[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))
    if len(table_2["raw_chem_name"].iloc[j].split())>1:
        table_2["raw_chem_name"].iloc[j]=" ".join(table_2["raw_chem_name"].iloc[j].split())

#drop chem that is not present in any products
table_2=table_2.drop(2)
table_2=table_2.reset_index()
table_2=table_2[["raw_chem_name"]]

table_2["data_document_id"]="1374297"
table_2["data_document_filename"]="DCPS_86_a.pdf"
table_2["doc_date"]="2007"
table_2["raw_category"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2["report_funcuse"]=""

table_2.to_csv("dcps_86_table_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 3
table_3=read_pdf("document_1374298.pdf", pages="18", lattice=True, pandas_options={'header': None})
table_3["raw_chem_name"]=table_3.iloc[1:,0]
table_3=table_3.dropna(subset=["raw_chem_name"])
table_3=table_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3["raw_chem_name"].iloc[j]=clean(str(table_3["raw_chem_name"].iloc[j]))
    if len(table_3["raw_chem_name"].iloc[j].split())>1:
        table_3["raw_chem_name"].iloc[j]=" ".join(table_3["raw_chem_name"].iloc[j].split())


table_3["data_document_id"]="1374298"
table_3["data_document_filename"]="DCPS_86_b.pdf"
table_3["doc_date"]="2007"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3["report_funcuse"]=""

table_3.to_csv("dcps_86_table_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4
table_4=read_pdf("document_1374299.pdf", pages="22", lattice=True, pandas_options={'header': None})
table_4["raw_chem_name"]=table_4.iloc[1:,0]
table_4=table_4.dropna(subset=["raw_chem_name"])
table_4=table_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))
    if len(table_4["raw_chem_name"].iloc[j].split())>1:
        table_4["raw_chem_name"].iloc[j]=" ".join(table_4["raw_chem_name"].iloc[j].split())

#drop chems that is not present in any products
table_4=table_4.drop([3,25])
table_4=table_4.reset_index()
table_4=table_4[["raw_chem_name"]]


table_4["data_document_id"]="1374299"
table_4["data_document_filename"]="DCPS_86_c.pdf"
table_4["doc_date"]="2007"
table_4["raw_category"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4["report_funcuse"]=""

table_4.to_csv("dcps_86_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5
tables=read_pdf("document_1374300.pdf", pages="25", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5=tables[0]
table_5["raw_chem_name"]=table_5.iloc[1:,0]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]=" ".join(table_5["raw_chem_name"].iloc[j].split())

#drop chems that is not present in any products
table_5=table_5.drop([2,24])
table_5=table_5.reset_index()
table_5=table_5[["raw_chem_name"]]


table_5["data_document_id"]="1374300"
table_5["data_document_filename"]="DCPS_86_d.pdf"
table_5["doc_date"]="2007"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5["report_funcuse"]=""

table_5.to_csv("dcps_86_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
