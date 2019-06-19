#lkoval
#6-19-19

from tabula import read_pdf
import pandas as pd
import string

#Table 0.1
table_0_1=read_pdf("document_1372356.pdf", pages="8", lattice=True, pandas_options={'header': None})
table_0_1["raw_chem_name"]=table_0_1.iloc[1:,0]
table_0_1=table_0_1.dropna(subset=["raw_chem_name"])
table_0_1=table_0_1.reset_index()
table_0_1=table_0_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_0_1)):
    table_0_1["raw_chem_name"].iloc[j]=str(table_0_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_0_1["raw_chem_name"].iloc[j]=clean(str(table_0_1["raw_chem_name"].iloc[j]))
    if len(table_0_1["raw_chem_name"].iloc[j].split())>1:
        table_0_1["raw_chem_name"].iloc[j]="".join(table_0_1["raw_chem_name"].iloc[j].split())

table_0_1["data_document_id"]="1372356"
table_0_1["data_document_filename"]="document_1359489_a.pdf"
table_0_1["doc_date"]="2006"
table_0_1["raw_category"]=""
table_0_1["cat_code"]=""
table_0_1["description_cpcat"]=""
table_0_1["cpcat_code"]=""
table_0_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_0_1["report_funcuse"]=""

table_0_1.to_csv("dcps_76_table_0_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 2.1
table_2_1=read_pdf("document_1372357.pdf", pages="28-30", lattice=False, pandas_options={'header': None})
table_2_1["raw_chem_name"]=table_2_1.iloc[:,0]
table_2_1["raw_cas"]=table_2_1.iloc[:,1]
table_2_1=table_2_1.dropna(subset=["raw_chem_name"])
table_2_1=table_2_1.loc[table_2_1["raw_chem_name"]!="Substance name"]
table_2_1=table_2_1.loc[table_2_1["raw_chem_name"]!="IstofnSubstance name"]
table_2_1=table_2_1.reset_index()
table_2_1=table_2_1[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if str(table_2_1["raw_cas"].iloc[j])=="nan":
        table_2_1["raw_chem_name"].iloc[j+1]=table_2_1["raw_chem_name"].iloc[j]+" "+table_2_1["raw_chem_name"].iloc[j+1]
        j_drop.append(j)

table_2_1=table_2_1.drop(j_drop)
table_2_1=table_2_1.drop_duplicates()
table_2_1=table_2_1.reset_index()
table_2_1=table_2_1[["raw_chem_name","raw_cas"]]

table_2_1["data_document_id"]="1372357"
table_2_1["data_document_filename"]="document_1359489_b.pdf"
table_2_1["doc_date"]="2006"
table_2_1["raw_category"]=""
table_2_1["cat_code"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_1["report_funcuse"]=""

table_2_1.to_csv("dcps_76_table_2_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 2.2
table_2_2=read_pdf("document_1372358.pdf", pages="31,32", lattice=True, pandas_options={'header': None})
table_2_2["raw_chem_name"]=table_2_2.iloc[:,0]
table_2_2["raw_cas"]=table_2_2.iloc[:,1]
table_2_2=table_2_2.dropna(subset=["raw_chem_name"])
table_2_2=table_2_2.loc[table_2_2["raw_chem_name"]!="Name"]
table_2_2=table_2_2.reset_index()
table_2_2=table_2_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_2)):
    table_2_2["raw_chem_name"].iloc[j]=str(table_2_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_2_2["raw_chem_name"].iloc[j]=clean(str(table_2_2["raw_chem_name"].iloc[j]))
    if len(table_2_2["raw_chem_name"].iloc[j].split())>1:
        table_2_2["raw_chem_name"].iloc[j]=" ".join(table_2_2["raw_chem_name"].iloc[j].split())


table_2_2["data_document_id"]="1372358"
table_2_2["data_document_filename"]="document_1359489_c.pdf"
table_2_2["doc_date"]="2006"
table_2_2["raw_category"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_2["report_funcuse"]=""

table_2_2.to_csv("dcps_76_table_2_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 2.3
table_2_3=read_pdf("document_1372359.pdf", pages="33", lattice=True, pandas_options={'header': None})
table_2_3["raw_chem_name"]=table_2_3.iloc[:,0]
table_2_3["raw_cas"]=table_2_3.iloc[:,1]
table_2_3=table_2_3.dropna(subset=["raw_chem_name"])
table_2_3=table_2_3.loc[table_2_3["raw_chem_name"]!="Name"]
table_2_3=table_2_3.reset_index()
table_2_3=table_2_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))
    if len(table_2_3["raw_chem_name"].iloc[j].split())>1:
        table_2_3["raw_chem_name"].iloc[j]=" ".join(table_2_3["raw_chem_name"].iloc[j].split())


table_2_3["data_document_id"]="1372359"
table_2_3["data_document_filename"]="document_1359489_d.pdf"
table_2_3["doc_date"]="2006"
table_2_3["raw_category"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_3["report_funcuse"]=""

table_2_3.to_csv("dcps_76_table_2_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 2.4
table_2_4=read_pdf("document_1372360.pdf", pages="34-37", lattice=True, pandas_options={'header': None})
table_2_4["raw_chem_name"]=table_2_4.iloc[:,0]
table_2_4["raw_cas"]=table_2_4.iloc[:,1]
table_2_4["report_funcuse"]=table_2_4.iloc[:,4]
table_2_4=table_2_4.dropna(subset=["raw_chem_name"])
table_2_4=table_2_4.loc[table_2_4["raw_chem_name"]!="Name"]
table_2_4=table_2_4.reset_index()
table_2_4=table_2_4[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    table_2_4["report_funcuse"].iloc[j]=str(table_2_4["report_funcuse"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_2_4["report_funcuse"].iloc[j]=clean(str(table_2_4["report_funcuse"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
    if len(table_2_4["report_funcuse"].iloc[j].split())>1:
        table_2_4["report_funcuse"].iloc[j]=" ".join(table_2_4["report_funcuse"].iloc[j].split())


table_2_4["data_document_id"]="1372360"
table_2_4["data_document_filename"]="document_1359489_e.pdf"
table_2_4["doc_date"]="2006"
table_2_4["raw_category"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_4.to_csv("dcps_76_table_2_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 3.1
table_3_1=read_pdf("document_1372361.pdf", pages="39,40", lattice=True, pandas_options={'header': None})
table_3_1["raw_chem_name"]=table_3_1.iloc[:,0]
table_3_1=table_3_1.dropna(subset=["raw_chem_name"])
table_3_1=table_3_1.loc[table_3_1["raw_chem_name"]!="Component"]
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[j]=str(table_3_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_1["raw_chem_name"].iloc[j]=clean(str(table_3_1["raw_chem_name"].iloc[j]))
    if len(table_3_1["raw_chem_name"].iloc[j].split())>1:
        table_3_1["raw_chem_name"].iloc[j]=" ".join(table_3_1["raw_chem_name"].iloc[j].split())

table_3_1=table_3_1.drop_duplicates()
table_3_1=table_3_1.drop([0,19,20,28,29,48])
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name"]]

table_3_1["data_document_id"]="1372361"
table_3_1["data_document_filename"]="document_1359489_f.pdf"
table_3_1["doc_date"]="2006"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_1["report_funcuse"]=""

table_3_1.to_csv("dcps_76_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.1
table_4_1=read_pdf("document_1372362.pdf", pages="41-44", lattice=True, pandas_options={'header': None})
table_4_1["raw_chem_name"]=table_4_1.iloc[:,0]
table_4_1=table_4_1.dropna(subset=["raw_chem_name"])
table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!="Substance"]
table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!="Product classification"]
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_1)):
    table_4_1["raw_chem_name"].iloc[j]=str(table_4_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_4_1["raw_chem_name"].iloc[j]=clean(str(table_4_1["raw_chem_name"].iloc[j]))

sampleNums=["1","2","4","6","7","8","11","12","13","23","24","27","29","30","32"]

for sample in sampleNums:
    table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!="sample number: %s"%sample]
    table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!="sample number:%s"%sample]

table_4_1=table_4_1.drop_duplicates()
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name"]]

table_4_1["data_document_id"]="1372362"
table_4_1["data_document_filename"]="document_1359489_v.pdf"
table_4_1["doc_date"]="2006"
table_4_1["raw_category"]=""
table_4_1["cat_code"]=""
table_4_1["description_cpcat"]=""
table_4_1["cpcat_code"]=""
table_4_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_1["report_funcuse"]=""

table_4_1.to_csv("dcps_76_table_4_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
