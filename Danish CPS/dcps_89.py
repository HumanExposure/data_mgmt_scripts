#lkoval
#6-20-19

from tabula import read_pdf
import pandas as pd
import string

#Table 6.1
p_23_24=read_pdf("document_1374304.pdf", pages="23,24", lattice=True, pandas_options={'header': None})
p_23_24["raw_chem_name"]=p_23_24.iloc[:,0]
p_23_24["raw_cas"]=p_23_24.iloc[:,1]
p_23_24=p_23_24[["raw_chem_name","raw_cas"]]
p_25=read_pdf("document_1374306.pdf", pages="25", lattice=True, multiple_tables=True, pandas_options={'header': None})
p_25=p_25[0]
p_25["raw_chem_name"]=p_25.iloc[:-2,1]
p_25["raw_cas"]=p_25.iloc[:-2,2]
p_25=p_25[["raw_chem_name","raw_cas"]]
table_6_1=pd.concat([p_23_24,p_25], ignore_index=True)
table_6_1=table_6_1.dropna(subset=["raw_chem_name"])
table_6_1=table_6_1.loc[table_6_1["raw_chem_name"]!="Balloon no."]
table_6_1=table_6_1.loc[table_6_1["raw_chem_name"]!="Chemical substance"]
table_6_1=table_6_1.reset_index()
table_6_1=table_6_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_1)):
    table_6_1["raw_chem_name"].iloc[j]=str(table_6_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_6_1["raw_chem_name"].iloc[j]=clean(str(table_6_1["raw_chem_name"].iloc[j]))
    if len(str(table_6_1["raw_cas"].iloc[j]).split())>1:
        table_6_1["raw_cas"].iloc[j]=" ".join(str(table_6_1["raw_cas"].iloc[j]).split())


table_6_1["data_document_id"]="1374304"
table_6_1["data_document_filename"]="DCPS_89_a.pdf"
table_6_1["doc_date"]="2007"
table_6_1["raw_category"]=""
table_6_1["cat_code"]=""
table_6_1["description_cpcat"]=""
table_6_1["cpcat_code"]=""
table_6_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_1["report_funcuse"]=""

table_6_1.to_csv("dcps_89_table_6_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.2
table_6_2=read_pdf("document_1374305.pdf", pages="25", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_2=table_6_2[1]
table_6_2["raw_chem_name"]=table_6_2.iloc[1:,0]
table_6_2["raw_cas"]=table_6_2.iloc[1:,1]
table_6_2=table_6_2.dropna(subset=["raw_chem_name"])
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_2)):
    table_6_2["raw_chem_name"].iloc[j]=str(table_6_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_6_2["raw_chem_name"].iloc[j]=clean(str(table_6_2["raw_chem_name"].iloc[j]))


table_6_2["data_document_id"]="1374305"
table_6_2["data_document_filename"]="DCPS_89_b.pdf"
table_6_2["doc_date"]="2007"
table_6_2["raw_category"]=""
table_6_2["cat_code"]=""
table_6_2["description_cpcat"]=""
table_6_2["cpcat_code"]=""
table_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_2["report_funcuse"]=""

table_6_2.to_csv("dcps_89_table_6_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
