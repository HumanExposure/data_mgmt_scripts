#lkoval
#6-19-19

from tabula import read_pdf
import pandas as pd
import string

#Table 5
table_5=read_pdf("document_1374295.pdf", pages="18", lattice=True, pandas_options={'header': None})
table_5["raw_chem_name"]=table_5.iloc[1:,0]
table_5["raw_cas"]=table_5.iloc[1:,2]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]=" ".join(table_5["raw_chem_name"].iloc[j].split())
    if len(str(table_5["raw_cas"].iloc[j]).split())>1:
        table_5["raw_cas"].iloc[j]=" ".join(str(table_5["raw_cas"].iloc[j]).split())

table_5["data_document_id"]="1374295"
table_5["data_document_filename"]="DCPS_83_a.pdf"
table_5["doc_date"]="2007"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5["report_funcuse"]=""

table_5.to_csv("dcps_83_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6
table_6=read_pdf("document_1374296.pdf", pages="19,20", lattice=True, pandas_options={'header': None})
table_6["raw_chem_name"]=table_6.iloc[:,0]
table_6["raw_cas"]=table_6.iloc[:,2]
table_6=table_6.dropna(subset=["raw_chem_name"])
table_6=table_6.loc[table_6["raw_chem_name"]!="Chemical substance"]
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())
    if len(str(table_6["raw_cas"].iloc[j]).split())>1:
        table_6["raw_cas"].iloc[j]="".join(str(table_6["raw_cas"].iloc[j]).split())

table_6["data_document_id"]="1374296"
table_6["data_document_filename"]="DCPS_83_b.pdf"
table_6["doc_date"]="2007"
table_6["raw_category"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6["report_funcuse"]=""

table_6.to_csv("dcps_83_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
