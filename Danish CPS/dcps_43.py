#lkoval
#6-6-19

from tabula import read_pdf
import pandas as pd
import string

#Table 17
tables=read_pdf("document_1373716.pdf", pages="41-43", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_17=pd.concat([tables[0],tables[1],tables[2]], ignore_index=True)
table_17["raw_chem_name"]=table_17.iloc[:,0]
table_17["raw_cas"]=table_17.iloc[:,1]
table_17=table_17.dropna(subset=["raw_chem_name"])
table_17=table_17.loc[table_17["raw_chem_name"]!="Substance name"]
table_17=table_17.reset_index()
table_17=table_17[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_17)):
    table_17["raw_chem_name"].iloc[j]=str(table_17["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_17["raw_chem_name"].iloc[j]=clean(str(table_17["raw_chem_name"].iloc[j]))
    if len(table_17["raw_chem_name"].iloc[j].split())>1:
        table_17["raw_chem_name"].iloc[j]=" ".join(table_17["raw_chem_name"].iloc[j].split())


table_17["data_document_id"]="1373716"
table_17["data_document_filename"]="DCPS_43_m.pdf"
table_17["doc_date"]="2003"
table_17["raw_category"]=""
table_17["cat_code"]=""
table_17["description_cpcat"]=""
table_17["cpcat_code"]=""
table_17["cpcat_sourcetype"]="ACToR Assays and Lists"

table_17.to_csv("dcps_43_table_17.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 18
tables=read_pdf("document_1373717.pdf", pages="43,44", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_18=pd.concat([tables[1],tables[2]], ignore_index=True)
table_18["raw_chem_name"]=table_18.iloc[:-1,0]
table_18["raw_cas"]=table_18.iloc[:-1,1]
table_18=table_18.dropna(subset=["raw_chem_name"])
table_18=table_18.loc[table_18["raw_chem_name"]!="Substance name"]
table_18=table_18.reset_index()
table_18=table_18[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_18)):
    table_18["raw_chem_name"].iloc[j]=str(table_18["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_18["raw_chem_name"].iloc[j]=clean(str(table_18["raw_chem_name"].iloc[j]))
    if len(table_18["raw_chem_name"].iloc[j].split())>1:
        table_18["raw_chem_name"].iloc[j]=" ".join(table_18["raw_chem_name"].iloc[j].split())


table_18["data_document_id"]="1373717"
table_18["data_document_filename"]="DCPS_43_n.pdf"
table_18["doc_date"]="2003"
table_18["raw_category"]=""
table_18["cat_code"]=""
table_18["description_cpcat"]=""
table_18["cpcat_code"]=""
table_18["cpcat_sourcetype"]="ACToR Assays and Lists"

table_18.to_csv("dcps_43_table_18.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#p. 46 declared
tables=read_pdf("document_1373719.pdf", pages="46", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p46_d=tables[0]
table_p46_d["raw_chem_name"]=table_p46_d.iloc[:,2]
table_p46_d["raw_cas"]=table_p46_d.iloc[:,1]
table_p46_d["report_funcuse"]=table_p46_d.iloc[:,0]
table_p46_d=table_p46_d.dropna(subset=["raw_chem_name"])
table_p46_d=table_p46_d.loc[table_p46_d["raw_chem_name"]!="Substance name"]
table_p46_d=table_p46_d.loc[table_p46_d["raw_chem_name"]!="-"]
table_p46_d=table_p46_d.reset_index()
table_p46_d=table_p46_d[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p46_d)):
    table_p46_d["raw_chem_name"].iloc[j]=str(table_p46_d["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p46_d["raw_chem_name"].iloc[j]=clean(str(table_p46_d["raw_chem_name"].iloc[j]))
    table_p46_d["report_funcuse"].iloc[j]=str(table_p46_d["report_funcuse"].iloc[j]).strip().lower()
    table_p46_d["report_funcuse"].iloc[j]=clean(str(table_p46_d["report_funcuse"].iloc[j]))
    if len(table_p46_d["raw_chem_name"].iloc[j].split())>1:
        table_p46_d["raw_chem_name"].iloc[j]=" ".join(table_p46_d["raw_chem_name"].iloc[j].split())


table_p46_d["data_document_id"]="1373719"
table_p46_d["data_document_filename"]="DCPS_43_p.pdf"
table_p46_d["doc_date"]="2003"
table_p46_d["raw_category"]=""
table_p46_d["cat_code"]=""
table_p46_d["description_cpcat"]=""
table_p46_d["cpcat_code"]=""
table_p46_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p46_d.to_csv("dcps_43_table_p46_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 46 analyzed
tables=read_pdf("document_1373720.pdf", pages="46", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p46_a=tables[1]
table_p46_a["raw_chem_name"]=table_p46_a.iloc[:,2]
table_p46_a["raw_cas"]=table_p46_a.iloc[:,1]
table_p46_a["report_funcuse"]=table_p46_a.iloc[:,0]
table_p46_a=table_p46_a.dropna(subset=["raw_chem_name"])
table_p46_a=table_p46_a.loc[table_p46_a["raw_chem_name"]!="Substance name"]
table_p46_a=table_p46_a.loc[table_p46_a["raw_chem_name"]!="-"]
table_p46_a=table_p46_a.reset_index()
table_p46_a=table_p46_a[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p46_a)):
    table_p46_a["raw_chem_name"].iloc[j]=str(table_p46_a["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p46_a["raw_chem_name"].iloc[j]=clean(str(table_p46_a["raw_chem_name"].iloc[j]))
    table_p46_a["report_funcuse"].iloc[j]=str(table_p46_a["report_funcuse"].iloc[j]).strip().lower()
    table_p46_a["report_funcuse"].iloc[j]=clean(str(table_p46_a["report_funcuse"].iloc[j]))
    if len(table_p46_a["raw_chem_name"].iloc[j].split())>1:
        table_p46_a["raw_chem_name"].iloc[j]=" ".join(table_p46_a["raw_chem_name"].iloc[j].split())


table_p46_a["data_document_id"]="1373720"
table_p46_a["data_document_filename"]="DCPS_43_q.pdf"
table_p46_a["doc_date"]="2003"
table_p46_a["raw_category"]=""
table_p46_a["cat_code"]=""
table_p46_a["description_cpcat"]=""
table_p46_a["cpcat_code"]=""
table_p46_a["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p46_a.to_csv("dcps_43_table_p46_a.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 47 declared
tables=read_pdf("document_1373721.pdf", pages="47", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p47_d=tables[0]
table_p47_d["raw_chem_name"]=table_p47_d.iloc[:,2]
table_p47_d["raw_cas"]=table_p47_d.iloc[:,1]
table_p47_d["report_funcuse"]=table_p47_d.iloc[:,0]
table_p47_d=table_p47_d.dropna(subset=["raw_chem_name"])
table_p47_d=table_p47_d.loc[table_p47_d["raw_chem_name"]!="Substance name"]
table_p47_d=table_p47_d.loc[table_p47_d["raw_chem_name"]!="-"]
table_p47_d=table_p47_d.reset_index()
table_p47_d=table_p47_d[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p47_d)):
    table_p47_d["raw_chem_name"].iloc[j]=str(table_p47_d["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p47_d["raw_chem_name"].iloc[j]=clean(str(table_p47_d["raw_chem_name"].iloc[j]))
    table_p47_d["report_funcuse"].iloc[j]=str(table_p47_d["report_funcuse"].iloc[j]).strip().lower()
    table_p47_d["report_funcuse"].iloc[j]=clean(str(table_p47_d["report_funcuse"].iloc[j]))
    if len(table_p47_d["raw_chem_name"].iloc[j].split())>1:
        table_p47_d["raw_chem_name"].iloc[j]=" ".join(table_p47_d["raw_chem_name"].iloc[j].split())
    if len(table_p47_d["report_funcuse"].iloc[j].split())>1:
        table_p47_d["report_funcuse"].iloc[j]=" ".join(table_p47_d["report_funcuse"].iloc[j].split())


table_p47_d["data_document_id"]="1373721"
table_p47_d["data_document_filename"]="DCPS_43_r.pdf"
table_p47_d["doc_date"]="2003"
table_p47_d["raw_category"]=""
table_p47_d["cat_code"]=""
table_p47_d["description_cpcat"]=""
table_p47_d["cpcat_code"]=""
table_p47_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p47_d.to_csv("dcps_43_table_p47_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 47 analyzed
tables=read_pdf("document_1373722.pdf", pages="47,48", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p47_a=pd.concat([tables[1],tables[2]], ignore_index=True)
table_p47_a["raw_chem_name"]=table_p47_a.iloc[:,2]
table_p47_a["raw_cas"]=table_p47_a.iloc[:,1]
table_p47_a["report_funcuse"]=table_p47_a.iloc[:,0]
table_p47_a=table_p47_a.dropna(subset=["raw_chem_name"])
table_p47_a=table_p47_a.loc[table_p47_a["raw_chem_name"]!="Substance name"]
table_p47_a=table_p47_a.loc[table_p47_a["raw_chem_name"]!="-"]
table_p47_a=table_p47_a.reset_index()
table_p47_a=table_p47_a[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p47_a)):
    table_p47_a["raw_chem_name"].iloc[j]=str(table_p47_a["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p47_a["raw_chem_name"].iloc[j]=clean(str(table_p47_a["raw_chem_name"].iloc[j]))
    table_p47_a["report_funcuse"].iloc[j]=str(table_p47_a["report_funcuse"].iloc[j]).strip().lower()
    table_p47_a["report_funcuse"].iloc[j]=clean(str(table_p47_a["report_funcuse"].iloc[j]))
    if len(table_p47_a["raw_chem_name"].iloc[j].split())>1:
        table_p47_a["raw_chem_name"].iloc[j]=" ".join(table_p47_a["raw_chem_name"].iloc[j].split())
    if len(table_p47_a["report_funcuse"].iloc[j].split())>1:
        table_p47_a["report_funcuse"].iloc[j]=" ".join(table_p47_a["report_funcuse"].iloc[j].split())
    if table_p47_a["report_funcuse"].iloc[j]!="nan":
        funcTemp=table_p47_a["report_funcuse"].iloc[j]
    elif table_p47_a["report_funcuse"].iloc[j]=="nan" and table_p47_a["raw_chem_name"].iloc[j]!="fatty acids":
        table_p47_a["report_funcuse"].iloc[j]=funcTemp

table_p47_a["data_document_id"]="1373722"
table_p47_a["data_document_filename"]="DCPS_43_s.pdf"
table_p47_a["doc_date"]="2003"
table_p47_a["raw_category"]=""
table_p47_a["cat_code"]=""
table_p47_a["description_cpcat"]=""
table_p47_a["cpcat_code"]=""
table_p47_a["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p47_a.to_csv("dcps_43_table_p47_a.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 49 declared
tables=read_pdf("document_1373723.pdf", pages="49", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p49_d=tables[0]
table_p49_d["raw_chem_name"]=table_p49_d.iloc[:,2]
table_p49_d["raw_cas"]=table_p49_d.iloc[:,1]
table_p49_d["report_funcuse"]=table_p49_d.iloc[:,0]
table_p49_d=table_p49_d.dropna(subset=["raw_chem_name"])
table_p49_d=table_p49_d.loc[table_p49_d["raw_chem_name"]!="Substance name"]
table_p49_d=table_p49_d.loc[table_p49_d["raw_chem_name"]!="-"]
table_p49_d=table_p49_d.reset_index()
table_p49_d=table_p49_d[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p49_d)):
    table_p49_d["raw_chem_name"].iloc[j]=str(table_p49_d["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p49_d["raw_chem_name"].iloc[j]=clean(str(table_p49_d["raw_chem_name"].iloc[j]))
    table_p49_d["report_funcuse"].iloc[j]=str(table_p49_d["report_funcuse"].iloc[j]).strip().lower()
    table_p49_d["report_funcuse"].iloc[j]=clean(str(table_p49_d["report_funcuse"].iloc[j]))
    if len(table_p49_d["raw_chem_name"].iloc[j].split())>1:
        table_p49_d["raw_chem_name"].iloc[j]=" ".join(table_p49_d["raw_chem_name"].iloc[j].split())


table_p49_d["data_document_id"]="1373723"
table_p49_d["data_document_filename"]="DCPS_43_t.pdf"
table_p49_d["doc_date"]="2003"
table_p49_d["raw_category"]=""
table_p49_d["cat_code"]=""
table_p49_d["description_cpcat"]=""
table_p49_d["cpcat_code"]=""
table_p49_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p49_d.to_csv("dcps_43_table_p49_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table p. 49 analyzed
tables=read_pdf("document_1373724.pdf", pages="49", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p49_a=tables[1]
table_p49_a["raw_chem_name"]=table_p49_a.iloc[:,2]
table_p49_a["raw_cas"]=table_p49_a.iloc[:,1]
table_p49_a["report_funcuse"]=table_p49_a.iloc[:,0]
table_p49_a=table_p49_a.dropna(subset=["raw_chem_name"])
table_p49_a=table_p49_a.loc[table_p49_a["raw_chem_name"]!="Substance name"]
table_p49_a=table_p49_a.loc[table_p49_a["raw_chem_name"]!="-"]
table_p49_a=table_p49_a.reset_index()
table_p49_a=table_p49_a[["raw_chem_name","raw_cas","report_funcuse"]]
table_p49_a["report_funcuse"].iloc[0]="perfume substances"

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p49_a)):
    table_p49_a["raw_chem_name"].iloc[j]=str(table_p49_a["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p49_a["raw_chem_name"].iloc[j]=clean(str(table_p49_a["raw_chem_name"].iloc[j]))
    table_p49_a["report_funcuse"].iloc[j]=str(table_p49_a["report_funcuse"].iloc[j]).strip().lower()
    table_p49_a["report_funcuse"].iloc[j]=clean(str(table_p49_a["report_funcuse"].iloc[j]))
    if len(table_p49_a["raw_chem_name"].iloc[j].split())>1:
        table_p49_a["raw_chem_name"].iloc[j]=" ".join(table_p49_a["raw_chem_name"].iloc[j].split())
    if len(table_p49_a["report_funcuse"].iloc[j].split())>1:
        table_p49_a["report_funcuse"].iloc[j]=" ".join(table_p49_a["report_funcuse"].iloc[j].split())
    if table_p49_a["report_funcuse"].iloc[j]!="nan":
        funcTemp=table_p49_a["report_funcuse"].iloc[j]
    elif table_p49_a["report_funcuse"].iloc[j]=="nan" and table_p49_a["raw_chem_name"].iloc[j]!="fatty acids":
        table_p49_a["report_funcuse"].iloc[j]=funcTemp


table_p49_a["data_document_id"]="1373724"
table_p49_a["data_document_filename"]="DCPS_43_u.pdf"
table_p49_a["doc_date"]="2003"
table_p49_a["raw_category"]=""
table_p49_a["cat_code"]=""
table_p49_a["description_cpcat"]=""
table_p49_a["cpcat_code"]=""
table_p49_a["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p49_a.to_csv("dcps_43_table_p49_a.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 50 declared
tables=read_pdf("document_1373725.pdf", pages="50", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p50_d=tables[0]
table_p50_d["raw_chem_name"]=table_p50_d.iloc[:,2]
table_p50_d["raw_cas"]=table_p50_d.iloc[:,1]
table_p50_d["report_funcuse"]=table_p50_d.iloc[:,0]
table_p50_d=table_p50_d.dropna(subset=["raw_chem_name"])
table_p50_d=table_p50_d.loc[table_p50_d["raw_chem_name"]!="Substance name"]
table_p50_d=table_p50_d.loc[table_p50_d["raw_chem_name"]!="-"]
table_p50_d=table_p50_d.reset_index()
table_p50_d=table_p50_d[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p50_d)):
    table_p50_d["raw_chem_name"].iloc[j]=str(table_p50_d["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p50_d["raw_chem_name"].iloc[j]=clean(str(table_p50_d["raw_chem_name"].iloc[j]))
    table_p50_d["report_funcuse"].iloc[j]=str(table_p50_d["report_funcuse"].iloc[j]).strip().lower()
    table_p50_d["report_funcuse"].iloc[j]=clean(str(table_p50_d["report_funcuse"].iloc[j]))
    if len(table_p50_d["raw_chem_name"].iloc[j].split())>1:
        table_p50_d["raw_chem_name"].iloc[j]=" ".join(table_p50_d["raw_chem_name"].iloc[j].split())
    if len(str(table_p50_d["raw_cas"].iloc[j]).split())>1:
        table_p50_d["raw_cas"].iloc[j]="".join(str(table_p50_d["raw_cas"].iloc[j]).split())


table_p50_d["data_document_id"]="1373725"
table_p50_d["data_document_filename"]="DCPS_43_v.pdf"
table_p50_d["doc_date"]="2003"
table_p50_d["raw_category"]=""
table_p50_d["cat_code"]=""
table_p50_d["description_cpcat"]=""
table_p50_d["cpcat_code"]=""
table_p50_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p50_d.to_csv("dcps_43_table_p50_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 51 analyzed
tables=read_pdf("document_1373726.pdf", pages="51", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p51_a=tables[0]
table_p51_a["raw_chem_name"]=table_p51_a.iloc[:,2]
table_p51_a["raw_cas"]=table_p51_a.iloc[:,1]
table_p51_a["report_funcuse"]=table_p51_a.iloc[:,0]
table_p51_a=table_p51_a.dropna(subset=["raw_chem_name"])
table_p51_a=table_p51_a.loc[table_p51_a["raw_chem_name"]!="Substance name"]
table_p51_a=table_p51_a.loc[table_p51_a["raw_chem_name"]!="-"]
table_p51_a=table_p51_a.reset_index()
table_p51_a=table_p51_a[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p51_a)):
    table_p51_a["raw_chem_name"].iloc[j]=str(table_p51_a["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p51_a["raw_chem_name"].iloc[j]=clean(str(table_p51_a["raw_chem_name"].iloc[j]))
    table_p51_a["report_funcuse"].iloc[j]=str(table_p51_a["report_funcuse"].iloc[j]).strip().lower()
    table_p51_a["report_funcuse"].iloc[j]=clean(str(table_p51_a["report_funcuse"].iloc[j]))
    if len(table_p51_a["raw_chem_name"].iloc[j].split())>1:
        table_p51_a["raw_chem_name"].iloc[j]=" ".join(table_p51_a["raw_chem_name"].iloc[j].split())


table_p51_a["data_document_id"]="1373726"
table_p51_a["data_document_filename"]="DCPS_43_w.pdf"
table_p51_a["doc_date"]="2003"
table_p51_a["raw_category"]=""
table_p51_a["cat_code"]=""
table_p51_a["description_cpcat"]=""
table_p51_a["cpcat_code"]=""
table_p51_a["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p51_a.to_csv("dcps_43_table_p51_a.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#p. 51 declared
tables=read_pdf("document_1373727.pdf", pages="51", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p51_d=tables[1]
table_p51_d["raw_chem_name"]=table_p51_d.iloc[2:,2]
table_p51_d["raw_cas"]=table_p51_d.iloc[2:,1]
table_p51_d["report_funcuse"]=table_p51_d.iloc[2:,0]
table_p51_d=table_p51_d.dropna(subset=["raw_chem_name"])
table_p51_d=table_p51_d.loc[table_p51_d["raw_chem_name"]!="Substance name"]
table_p51_d=table_p51_d.loc[table_p51_d["raw_chem_name"]!="-"]
table_p51_d=table_p51_d.reset_index()
table_p51_d=table_p51_d[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p51_d)):
    table_p51_d["raw_chem_name"].iloc[j]=str(table_p51_d["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p51_d["raw_chem_name"].iloc[j]=clean(str(table_p51_d["raw_chem_name"].iloc[j]))
    table_p51_d["report_funcuse"].iloc[j]=str(table_p51_d["report_funcuse"].iloc[j]).strip().lower()
    table_p51_d["report_funcuse"].iloc[j]=clean(str(table_p51_d["report_funcuse"].iloc[j]))
    if len(table_p51_d["raw_chem_name"].iloc[j].split())>1:
        table_p51_d["raw_chem_name"].iloc[j]=" ".join(table_p51_d["raw_chem_name"].iloc[j].split())

table_p51_d["data_document_id"]="1373727"
table_p51_d["data_document_filename"]="DCPS_43_x.pdf"
table_p51_d["doc_date"]="2003"
table_p51_d["raw_category"]=""
table_p51_d["cat_code"]=""
table_p51_d["description_cpcat"]=""
table_p51_d["cpcat_code"]=""
table_p51_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p51_d.to_csv("dcps_43_table_p51_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table p.52 analyzed
tables=read_pdf("document_1373728.pdf", pages="52", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p52_a=tables[0]
table_p52_a["raw_chem_name"]=table_p52_a.iloc[2:,2]
table_p52_a["raw_cas"]=table_p52_a.iloc[2:,1]
table_p52_a["report_funcuse"]=table_p52_a.iloc[2:,0]
table_p52_a=table_p52_a.dropna(subset=["raw_chem_name"])
table_p52_a=table_p52_a.loc[table_p52_a["raw_chem_name"]!="Substance name"]
table_p52_a=table_p52_a.loc[table_p52_a["raw_chem_name"]!="-"]
table_p52_a=table_p52_a.reset_index()
table_p52_a=table_p52_a[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p52_a)):
    table_p52_a["raw_chem_name"].iloc[j]=str(table_p52_a["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p52_a["raw_chem_name"].iloc[j]=clean(str(table_p52_a["raw_chem_name"].iloc[j]))
    table_p52_a["report_funcuse"].iloc[j]=str(table_p52_a["report_funcuse"].iloc[j]).strip().lower()
    table_p52_a["report_funcuse"].iloc[j]=clean(str(table_p52_a["report_funcuse"].iloc[j]))
    if len(table_p52_a["raw_chem_name"].iloc[j].split())>1:
        table_p52_a["raw_chem_name"].iloc[j]=" ".join(table_p52_a["raw_chem_name"].iloc[j].split())
    if table_p52_a["report_funcuse"].iloc[j]!="nan":
        funcTemp=table_p52_a["report_funcuse"].iloc[j]
    elif table_p52_a["report_funcuse"].iloc[j]=="nan" and table_p52_a["raw_chem_name"].iloc[j]!="fatty acids":
        table_p52_a["report_funcuse"].iloc[j]=funcTemp
    table_p52_a["report_funcuse"].iloc[j]=table_p52_a["report_funcuse"].iloc[j].strip(":")

table_p52_a["data_document_id"]="1373728"
table_p52_a["data_document_filename"]="DCPS_43_y.pdf"
table_p52_a["doc_date"]="2003"
table_p52_a["raw_category"]=""
table_p52_a["cat_code"]=""
table_p52_a["description_cpcat"]=""
table_p52_a["cpcat_code"]=""
table_p52_a["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p52_a.to_csv("dcps_43_table_p52_a.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table p.52 declared
tables=read_pdf("document_1373729.pdf", pages="52", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_p52_d=tables[1]
table_p52_d["raw_chem_name"]=table_p52_d.iloc[:,3]
table_p52_d["raw_cas"]=table_p52_d.iloc[:,1]
table_p52_d["report_funcuse"]=table_p52_d.iloc[:,0]
table_p52_d=table_p52_d.dropna(subset=["raw_chem_name"])
table_p52_d=table_p52_d.loc[table_p52_d["raw_chem_name"]!="Substance name"]
table_p52_d=table_p52_d.loc[table_p52_d["raw_chem_name"]!="-"]
table_p52_d=table_p52_d.reset_index()
table_p52_d=table_p52_d[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_p52_d)):
    table_p52_d["raw_chem_name"].iloc[j]=str(table_p52_d["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("^","")
    table_p52_d["raw_chem_name"].iloc[j]=clean(str(table_p52_d["raw_chem_name"].iloc[j]))
    table_p52_d["report_funcuse"].iloc[j]=str(table_p52_d["report_funcuse"].iloc[j]).strip().lower()
    table_p52_d["report_funcuse"].iloc[j]=clean(str(table_p52_d["report_funcuse"].iloc[j]))
    if len(table_p52_d["raw_chem_name"].iloc[j].split())>1:
        table_p52_d["raw_chem_name"].iloc[j]=" ".join(table_p52_d["raw_chem_name"].iloc[j].split())

table_p52_d["data_document_id"]="1373729"
table_p52_d["data_document_filename"]="DCPS_43_z.pdf"
table_p52_d["doc_date"]="2003"
table_p52_d["raw_category"]=""
table_p52_d["cat_code"]=""
table_p52_d["description_cpcat"]=""
table_p52_d["cpcat_code"]=""
table_p52_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_p52_d.to_csv("dcps_43_table_p52_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
