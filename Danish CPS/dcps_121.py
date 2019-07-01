#lkoval
#7-1-19

from tabula import read_pdf
import pandas as pd
import string

#Table 4.7
table_4_7=read_pdf("document_1374837.pdf", pages="39-42", lattice=True, pandas_options={'header': None})
table_4_7["raw_chem_name"]=table_4_7.iloc[:,0]
table_4_7["raw_cas"]=table_4_7.iloc[:,1]
table_4_7=table_4_7.loc[table_4_7["raw_chem_name"]!="INCI Name"]
table_4_7=table_4_7.dropna(subset=["raw_chem_name"])
table_4_7=table_4_7.reset_index()
table_4_7=table_4_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_7)):
    table_4_7["raw_chem_name"].iloc[j]=str(table_4_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_7["raw_chem_name"].iloc[j]=clean(str(table_4_7["raw_chem_name"].iloc[j]))
    if len(table_4_7["raw_chem_name"].iloc[j].split())>1:
        table_4_7["raw_chem_name"].iloc[j]=" ".join(table_4_7["raw_chem_name"].iloc[j].split())
    if len(str(table_4_7["raw_cas"].iloc[j]).split())>1:
        table_4_7["raw_cas"].iloc[j]="".join(str(table_4_7["raw_cas"].iloc[j]).split())

table_4_7["data_document_id"]="1374837"
table_4_7["data_document_filename"]=""
table_4_7["doc_date"]="2013"
table_4_7["raw_category"]=""
table_4_7["cat_code"]=""
table_4_7["description_cpcat"]=""
table_4_7["cpcat_code"]=""
table_4_7["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_7["report_funcuse"]=""

table_4_7.to_csv("dcps_121_table_4_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.8
table_4_8=read_pdf("document_1374838.pdf", pages="44", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_8=table_4_8[0]
table_4_8["raw_chem_name"]=table_4_8.iloc[1:-1,0]
table_4_8["raw_cas"]=table_4_8.iloc[1:-1,1]
table_4_8=table_4_8.dropna(subset=["raw_chem_name"])
table_4_8=table_4_8.reset_index()
table_4_8=table_4_8[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_8)):
    table_4_8["raw_chem_name"].iloc[j]=str(table_4_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_8["raw_chem_name"].iloc[j]=clean(str(table_4_8["raw_chem_name"].iloc[j]))
    if len(table_4_8["raw_chem_name"].iloc[j].split())>1:
        table_4_8["raw_chem_name"].iloc[j]=" ".join(table_4_8["raw_chem_name"].iloc[j].split())
    if len(str(table_4_8["raw_cas"].iloc[j]).split())>1:
        table_4_8["raw_cas"].iloc[j]="".join(str(table_4_8["raw_cas"].iloc[j]).split())

table_4_8["data_document_id"]="1374838"
table_4_8["data_document_filename"]="DCPS_121_b.pdf"
table_4_8["doc_date"]="2013"
table_4_8["raw_category"]=""
table_4_8["cat_code"]=""
table_4_8["description_cpcat"]=""
table_4_8["cpcat_code"]=""
table_4_8["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_8["report_funcuse"]=""

table_4_8.to_csv("dcps_121_table_4_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.9
table_4_9=read_pdf("document_1374839.pdf", pages="44", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_9=table_4_9[1]
table_4_9["raw_chem_name"]=table_4_9.iloc[1:-1,0]
table_4_9["raw_cas"]=table_4_9.iloc[1:-1,1]
table_4_9=table_4_9.dropna(subset=["raw_chem_name"])
table_4_9=table_4_9.reset_index()
table_4_9=table_4_9[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_9)):
    table_4_9["raw_chem_name"].iloc[j]=str(table_4_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_9["raw_chem_name"].iloc[j]=clean(str(table_4_9["raw_chem_name"].iloc[j]))
    if len(table_4_9["raw_chem_name"].iloc[j].split())>1:
        table_4_9["raw_chem_name"].iloc[j]=" ".join(table_4_9["raw_chem_name"].iloc[j].split())
    if len(str(table_4_9["raw_cas"].iloc[j]).split())>1:
        table_4_9["raw_cas"].iloc[j]="".join(str(table_4_9["raw_cas"].iloc[j]).split())

table_4_9["data_document_id"]="1374839"
table_4_9["data_document_filename"]="DCPS_121_c.pdf"
table_4_9["doc_date"]="2013"
table_4_9["raw_category"]=""
table_4_9["cat_code"]=""
table_4_9["description_cpcat"]=""
table_4_9["cpcat_code"]=""
table_4_9["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_9["report_funcuse"]=""

table_4_9.to_csv("dcps_121_table_4_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.15
table_4_15=read_pdf("document_1374840.pdf", pages="50-52", lattice=True, pandas_options={'header': None})
table_4_15["raw_chem_name"]=table_4_15.iloc[:,0]
table_4_15["raw_cas"]=table_4_15.iloc[:,1]
table_4_15=table_4_15.dropna(subset=["raw_chem_name"])
table_4_15=table_4_15.loc[table_4_15["raw_chem_name"]!="INCI Name"]
table_4_15=table_4_15.reset_index()
table_4_15=table_4_15[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_15)):
    table_4_15["raw_chem_name"].iloc[j]=str(table_4_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_15["raw_chem_name"].iloc[j]=clean(str(table_4_15["raw_chem_name"].iloc[j]))
    if len(table_4_15["raw_chem_name"].iloc[j].split())>1:
        table_4_15["raw_chem_name"].iloc[j]=" ".join(table_4_15["raw_chem_name"].iloc[j].split())
    if len(str(table_4_15["raw_cas"].iloc[j]).split())>1:
        table_4_15["raw_cas"].iloc[j]="".join(str(table_4_15["raw_cas"].iloc[j]).split())

table_4_15["data_document_id"]="1374840"
table_4_15["data_document_filename"]="DCPS_121_d.pdf"
table_4_15["doc_date"]="2013"
table_4_15["raw_category"]=""
table_4_15["cat_code"]=""
table_4_15["description_cpcat"]=""
table_4_15["cpcat_code"]=""
table_4_15["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_15["report_funcuse"]=""

table_4_15.to_csv("dcps_121_table_4_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.16
table_4_16=read_pdf("document_1374841.pdf", pages="53,54", lattice=True, pandas_options={'header': None})
table_4_16["raw_chem_name"]=table_4_16.iloc[1:,0]
table_4_16["raw_cas"]=table_4_16.iloc[1:,1]
table_4_16=table_4_16.dropna(subset=["raw_chem_name"])
table_4_16=table_4_16.reset_index()
table_4_16=table_4_16[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_16)):
    table_4_16["raw_chem_name"].iloc[j]=str(table_4_16["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_16["raw_chem_name"].iloc[j]=clean(str(table_4_16["raw_chem_name"].iloc[j]))
    if len(table_4_16["raw_chem_name"].iloc[j].split())>1:
        table_4_16["raw_chem_name"].iloc[j]=" ".join(table_4_16["raw_chem_name"].iloc[j].split())
    if len(str(table_4_16["raw_cas"].iloc[j]).split())>1:
        table_4_16["raw_cas"].iloc[j]="".join(str(table_4_16["raw_cas"].iloc[j]).split())

table_4_16["data_document_id"]="1374841"
table_4_16["data_document_filename"]="DCPS_121_e.pdf"
table_4_16["doc_date"]="2013"
table_4_16["raw_category"]=""
table_4_16["cat_code"]=""
table_4_16["description_cpcat"]=""
table_4_16["cpcat_code"]=""
table_4_16["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_16["report_funcuse"]=""

table_4_16.to_csv("dcps_121_table_4_16.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5.1
table_5_1=read_pdf("document_1374842.pdf", pages="60", lattice=True, pandas_options={'header': None})
table_5_1["raw_chem_name"]=table_5_1.iloc[3:,2]
table_5_1["raw_cas"]=table_5_1.iloc[3:,0]
table_5_1=table_5_1.dropna(subset=["raw_chem_name"])
table_5_1=table_5_1.reset_index()
table_5_1=table_5_1[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_1)):
    table_5_1["raw_chem_name"].iloc[j]=str(table_5_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_5_1["raw_chem_name"].iloc[j]=clean(str(table_5_1["raw_chem_name"].iloc[j]))
    if str(table_5_1["raw_cas"].iloc[j])=="nan":
        table_5_1["raw_chem_name"].iloc[j]=table_5_1["raw_chem_name"].iloc[j-1]+" "+table_5_1["raw_chem_name"].iloc[j]
        table_5_1["raw_cas"].iloc[j]=table_5_1["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_5_1=table_5_1.drop(j_drop)
table_5_1=table_5_1.reset_index()
table_5_1=table_5_1[["raw_chem_name","raw_cas"]]

table_5_1["data_document_id"]="1374842"
table_5_1["data_document_filename"]="DCPS_121_f.pdf"
table_5_1["doc_date"]="2013"
table_5_1["raw_category"]=""
table_5_1["cat_code"]=""
table_5_1["description_cpcat"]=""
table_5_1["cpcat_code"]=""
table_5_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5_1["report_funcuse"]=""

table_5_1.to_csv("dcps_121_table_5_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.2
table_6_2=read_pdf("document_1374843.pdf", pages="64", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_2=table_6_2[0]
table_6_2["raw_chem_name"]=table_6_2.iloc[4:,0]
table_6_2=table_6_2.dropna(subset=["raw_chem_name"])
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_2)):
    table_6_2["raw_chem_name"].iloc[j]=str(table_6_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_2["raw_chem_name"].iloc[j]=clean(str(table_6_2["raw_chem_name"].iloc[j]))
    if len(table_6_2["raw_chem_name"].iloc[j].split())>1:
        table_6_2["raw_chem_name"].iloc[j]=" ".join(table_6_2["raw_chem_name"].iloc[j].split())

table_6_2["data_document_id"]="1374843"
table_6_2["data_document_filename"]="DCPS_121_g.pdf"
table_6_2["doc_date"]="2013"
table_6_2["raw_category"]=""
table_6_2["cat_code"]=""
table_6_2["description_cpcat"]=""
table_6_2["cpcat_code"]=""
table_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_2["report_funcuse"]=""

table_6_2.to_csv("dcps_121_table_6_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.3
table_6_3=read_pdf("document_1374844.pdf", pages="64", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_3=table_6_3[1]
table_6_3["raw_chem_name"]=table_6_3.iloc[4:,0]
table_6_3=table_6_3.dropna(subset=["raw_chem_name"])
table_6_3=table_6_3.reset_index()
table_6_3=table_6_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_3)):
    table_6_3["raw_chem_name"].iloc[j]=str(table_6_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_3["raw_chem_name"].iloc[j]=clean(str(table_6_3["raw_chem_name"].iloc[j]))
    if len(table_6_3["raw_chem_name"].iloc[j].split())>1:
        table_6_3["raw_chem_name"].iloc[j]=" ".join(table_6_3["raw_chem_name"].iloc[j].split())

table_6_3["data_document_id"]="1374844"
table_6_3["data_document_filename"]="DCPS_121_h.pdf"
table_6_3["doc_date"]="2013"
table_6_3["raw_category"]=""
table_6_3["cat_code"]=""
table_6_3["description_cpcat"]=""
table_6_3["cpcat_code"]=""
table_6_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_3["report_funcuse"]=""

table_6_3.to_csv("dcps_121_table_6_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.4
table_6_4=read_pdf("document_1374845.pdf", pages="65", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_4=table_6_4[0]
table_6_4["raw_chem_name"]=table_6_4.iloc[4:,0]
table_6_4=table_6_4.dropna(subset=["raw_chem_name"])
table_6_4=table_6_4.reset_index()
table_6_4=table_6_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_4)):
    table_6_4["raw_chem_name"].iloc[j]=str(table_6_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_4["raw_chem_name"].iloc[j]=clean(str(table_6_4["raw_chem_name"].iloc[j]))
    if len(table_6_4["raw_chem_name"].iloc[j].split())>1:
        table_6_4["raw_chem_name"].iloc[j]=" ".join(table_6_4["raw_chem_name"].iloc[j].split())

table_6_4["data_document_id"]="1374845"
table_6_4["data_document_filename"]="DCPS_121_i.pdf"
table_6_4["doc_date"]="2013"
table_6_4["raw_category"]=""
table_6_4["cat_code"]=""
table_6_4["description_cpcat"]=""
table_6_4["cpcat_code"]=""
table_6_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_4["report_funcuse"]=""

table_6_4.to_csv("dcps_121_table_6_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.5
table_6_5=read_pdf("document_1374846.pdf", pages="65", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_5=table_6_5[1]
table_6_5["raw_chem_name"]=table_6_5.iloc[4:,0]
table_6_5=table_6_5.dropna(subset=["raw_chem_name"])
table_6_5=table_6_5.reset_index()
table_6_5=table_6_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_5)):
    table_6_5["raw_chem_name"].iloc[j]=str(table_6_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_5["raw_chem_name"].iloc[j]=clean(str(table_6_5["raw_chem_name"].iloc[j]))
    if len(table_6_5["raw_chem_name"].iloc[j].split())>1:
        table_6_5["raw_chem_name"].iloc[j]=" ".join(table_6_5["raw_chem_name"].iloc[j].split())

table_6_5["data_document_id"]="1374846"
table_6_5["data_document_filename"]="DCPS_121_j.pdf"
table_6_5["doc_date"]="2013"
table_6_5["raw_category"]=""
table_6_5["cat_code"]=""
table_6_5["description_cpcat"]=""
table_6_5["cpcat_code"]=""
table_6_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_5["report_funcuse"]=""

table_6_5.to_csv("dcps_121_table_6_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.6
table_6_6=read_pdf("document_1374847.pdf", pages="66", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6_6["raw_chem_name"]=table_6_6.iloc[4:,0]
table_6_6=table_6_6.dropna(subset=["raw_chem_name"])
table_6_6=table_6_6.reset_index()
table_6_6=table_6_6[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_6)):
    table_6_6["raw_chem_name"].iloc[j]=str(table_6_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_6["raw_chem_name"].iloc[j]=clean(str(table_6_6["raw_chem_name"].iloc[j]))
    if len(table_6_6["raw_chem_name"].iloc[j].split())>1:
        table_6_6["raw_chem_name"].iloc[j]=" ".join(table_6_6["raw_chem_name"].iloc[j].split())

table_6_6=table_6_6.drop([3,7])
table_6_6=table_6_6.reset_index()
table_6_6=table_6_6[["raw_chem_name"]]

table_6_6["data_document_id"]="1374847"
table_6_6["data_document_filename"]="DCPS_121_k.pdf"
table_6_6["doc_date"]="2013"
table_6_6["raw_category"]=""
table_6_6["cat_code"]=""
table_6_6["description_cpcat"]=""
table_6_6["cpcat_code"]=""
table_6_6["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_6["report_funcuse"]=""

table_6_6.to_csv("dcps_121_table_6_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.7
table_6_7=read_pdf("document_1374848.pdf", pages="67", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_7=table_6_7[0]
table_6_7["raw_chem_name"]=table_6_7.iloc[4:,0]
table_6_7=table_6_7.dropna(subset=["raw_chem_name"])
table_6_7=table_6_7.reset_index()
table_6_7=table_6_7[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_7)):
    table_6_7["raw_chem_name"].iloc[j]=str(table_6_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_7["raw_chem_name"].iloc[j]=clean(str(table_6_7["raw_chem_name"].iloc[j]))
    if len(table_6_7["raw_chem_name"].iloc[j].split())>1:
        table_6_7["raw_chem_name"].iloc[j]=" ".join(table_6_7["raw_chem_name"].iloc[j].split())

table_6_7=table_6_7.drop([4,10])
table_6_7=table_6_7.reset_index()
table_6_7=table_6_7[["raw_chem_name"]]

table_6_7["data_document_id"]="1374848"
table_6_7["data_document_filename"]="DCPS_121_l.pdf"
table_6_7["doc_date"]="2013"
table_6_7["raw_category"]=""
table_6_7["cat_code"]=""
table_6_7["description_cpcat"]=""
table_6_7["cpcat_code"]=""
table_6_7["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_7["report_funcuse"]=""

table_6_7.to_csv("dcps_121_table_6_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.8
table_6_8=read_pdf("document_1374849.pdf", pages="67,68", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_8=pd.concat(table_6_8[1:3], ignore_index=True)
table_6_8["raw_chem_name"]=table_6_8.iloc[:,0]
table_6_8=table_6_8.dropna(subset=["raw_chem_name"])
table_6_8=table_6_8.loc[table_6_8["raw_chem_name"]!="Product no."]
table_6_8=table_6_8.loc[table_6_8["raw_chem_name"]!="Hair colour"]
table_6_8=table_6_8.loc[table_6_8["raw_chem_name"]!="Substance"]

table_6_8=table_6_8.reset_index()
table_6_8=table_6_8[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_8)):
    table_6_8["raw_chem_name"].iloc[j]=str(table_6_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_8["raw_chem_name"].iloc[j]=clean(str(table_6_8["raw_chem_name"].iloc[j]))
    if len(table_6_8["raw_chem_name"].iloc[j].split())>1:
        table_6_8["raw_chem_name"].iloc[j]=" ".join(table_6_8["raw_chem_name"].iloc[j].split())

table_6_8=table_6_8.drop([3,7])
table_6_8=table_6_8.reset_index()
table_6_8=table_6_8[["raw_chem_name"]]

table_6_8["data_document_id"]="1374849"
table_6_8["data_document_filename"]="DCPS_121_m.pdf"
table_6_8["doc_date"]="2013"
table_6_8["raw_category"]=""
table_6_8["cat_code"]=""
table_6_8["description_cpcat"]=""
table_6_8["cpcat_code"]=""
table_6_8["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_8["report_funcuse"]=""

table_6_8.to_csv("dcps_121_table_6_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6.9
table_6_9=read_pdf("document_1374850.pdf", pages="68", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_9=table_6_9[1]
table_6_9["raw_chem_name"]=table_6_9.iloc[:,0]
table_6_9=table_6_9.dropna(subset=["raw_chem_name"])
table_6_9=table_6_9.loc[table_6_9["raw_chem_name"]!="Product no."]
table_6_9=table_6_9.loc[table_6_9["raw_chem_name"]!="Hair colour"]
table_6_9=table_6_9.loc[table_6_9["raw_chem_name"]!="Substance"]

table_6_9=table_6_9.reset_index()
table_6_9=table_6_9[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_9)):
    table_6_9["raw_chem_name"].iloc[j]=str(table_6_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_9["raw_chem_name"].iloc[j]=clean(str(table_6_9["raw_chem_name"].iloc[j]))
    if len(table_6_9["raw_chem_name"].iloc[j].split())>1:
        table_6_9["raw_chem_name"].iloc[j]=" ".join(table_6_9["raw_chem_name"].iloc[j].split())

table_6_9=table_6_9.drop([3,10])
table_6_9=table_6_9.reset_index()
table_6_9=table_6_9[["raw_chem_name"]]

table_6_9["data_document_id"]="1374850"
table_6_9["data_document_filename"]="DCPS_121_n.pdf"
table_6_9["doc_date"]="2013"
table_6_9["raw_category"]=""
table_6_9["cat_code"]=""
table_6_9["description_cpcat"]=""
table_6_9["cpcat_code"]=""
table_6_9["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_9["report_funcuse"]=""

table_6_9.to_csv("dcps_121_table_6_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6_10
table_6_10=read_pdf("document_1374851.pdf", pages="69", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6_10["raw_chem_name"]=table_6_10.iloc[:,0]
table_6_10=table_6_10.dropna(subset=["raw_chem_name"])
table_6_10=table_6_10.loc[table_6_10["raw_chem_name"]!="Product no."]
table_6_10=table_6_10.loc[table_6_10["raw_chem_name"]!="Hair colour"]
table_6_10=table_6_10.loc[table_6_10["raw_chem_name"]!="Substance"]

table_6_10=table_6_10.reset_index()
table_6_10=table_6_10[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_10)):
    table_6_10["raw_chem_name"].iloc[j]=str(table_6_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_10["raw_chem_name"].iloc[j]=clean(str(table_6_10["raw_chem_name"].iloc[j]))
    if len(table_6_10["raw_chem_name"].iloc[j].split())>1:
        table_6_10["raw_chem_name"].iloc[j]=" ".join(table_6_10["raw_chem_name"].iloc[j].split())

table_6_10["data_document_id"]="1374851"
table_6_10["data_document_filename"]="DCPS_121_o.pdf"
table_6_10["doc_date"]="2013"
table_6_10["raw_category"]=""
table_6_10["cat_code"]=""
table_6_10["description_cpcat"]=""
table_6_10["cpcat_code"]=""
table_6_10["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_10["report_funcuse"]=""

table_6_10.to_csv("dcps_121_table_6_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6_11
table_6_11=read_pdf("document_1374852.pdf", pages="70", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6_11["raw_chem_name"]=table_6_11.iloc[:,0]
table_6_11=table_6_11.dropna(subset=["raw_chem_name"])
table_6_11=table_6_11.loc[table_6_11["raw_chem_name"]!="Product no."]
table_6_11=table_6_11.loc[table_6_11["raw_chem_name"]!="Hair colour"]
table_6_11=table_6_11.loc[table_6_11["raw_chem_name"]!="Substance"]

table_6_11=table_6_11.reset_index()
table_6_11=table_6_11[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_11)):
    table_6_11["raw_chem_name"].iloc[j]=str(table_6_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_11["raw_chem_name"].iloc[j]=clean(str(table_6_11["raw_chem_name"].iloc[j]))
    if len(table_6_11["raw_chem_name"].iloc[j].split())>1:
        table_6_11["raw_chem_name"].iloc[j]=" ".join(table_6_11["raw_chem_name"].iloc[j].split())

table_6_11=table_6_11.drop([7,8,10,11])
table_6_11=table_6_11.reset_index()
table_6_11=table_6_11[["raw_chem_name"]]

table_6_11["data_document_id"]="1374852"
table_6_11["data_document_filename"]="DCPS_121_p.pdf"
table_6_11["doc_date"]="2013"
table_6_11["raw_category"]=""
table_6_11["cat_code"]=""
table_6_11["description_cpcat"]=""
table_6_11["cpcat_code"]=""
table_6_11["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_11["report_funcuse"]=""

table_6_11.to_csv("dcps_121_table_6_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6_12
table_6_12=read_pdf("document_1374853.pdf", pages="71", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_12=table_6_12[0]
table_6_12["raw_chem_name"]=table_6_12.iloc[:,0]
table_6_12=table_6_12.dropna(subset=["raw_chem_name"])
table_6_12=table_6_12.loc[table_6_12["raw_chem_name"]!="Product no."]
table_6_12=table_6_12.loc[table_6_12["raw_chem_name"]!="Hair colour"]
table_6_12=table_6_12.loc[table_6_12["raw_chem_name"]!="Substance"]

table_6_12=table_6_12.reset_index()
table_6_12=table_6_12[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_12)):
    table_6_12["raw_chem_name"].iloc[j]=str(table_6_12["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_12["raw_chem_name"].iloc[j]=clean(str(table_6_12["raw_chem_name"].iloc[j]))
    if len(table_6_12["raw_chem_name"].iloc[j].split())>1:
        table_6_12["raw_chem_name"].iloc[j]=" ".join(table_6_12["raw_chem_name"].iloc[j].split())

table_6_12=table_6_12.drop(3)
table_6_12=table_6_12.reset_index()
table_6_12=table_6_12[["raw_chem_name"]]

table_6_12["data_document_id"]="1374853"
table_6_12["data_document_filename"]="DCPS_121_q.pdf"
table_6_12["doc_date"]="2013"
table_6_12["raw_category"]=""
table_6_12["cat_code"]=""
table_6_12["description_cpcat"]=""
table_6_12["cpcat_code"]=""
table_6_12["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_12["report_funcuse"]=""

table_6_12.to_csv("dcps_121_table_6_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6_14
table_6_14=read_pdf("document_1374854.pdf", pages="72", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6_14["raw_chem_name"]=table_6_14.iloc[:,0]
table_6_14=table_6_14.dropna(subset=["raw_chem_name"])
table_6_14=table_6_14.loc[table_6_14["raw_chem_name"]!="Number of analyzed hair dye products"]

table_6_14=table_6_14.reset_index()
table_6_14=table_6_14[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_14)):
    table_6_14["raw_chem_name"].iloc[j]=str(table_6_14["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_14["raw_chem_name"].iloc[j]=clean(str(table_6_14["raw_chem_name"].iloc[j]))
    if len(table_6_14["raw_chem_name"].iloc[j].split())>1:
        table_6_14["raw_chem_name"].iloc[j]=" ".join(table_6_14["raw_chem_name"].iloc[j].split())

table_6_14["data_document_id"]="1374854"
table_6_14["data_document_filename"]="DCPS_121_r.pdf"
table_6_14["doc_date"]="2013"
table_6_14["raw_category"]=""
table_6_14["cat_code"]=""
table_6_14["description_cpcat"]=""
table_6_14["cpcat_code"]=""
table_6_14["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_14["report_funcuse"]=""

table_6_14.to_csv("dcps_121_table_6_14.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6_15
table_6_15=read_pdf("document_1374855.pdf", pages="73", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6_15["raw_chem_name"]=table_6_15.iloc[1:,0]
table_6_15=table_6_15.dropna(subset=["raw_chem_name"])

table_6_15=table_6_15.reset_index()
table_6_15=table_6_15[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_15)):
    table_6_15["raw_chem_name"].iloc[j]=str(table_6_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_15["raw_chem_name"].iloc[j]=clean(str(table_6_15["raw_chem_name"].iloc[j]))
    if len(table_6_15["raw_chem_name"].iloc[j].split())>1:
        table_6_15["raw_chem_name"].iloc[j]=" ".join(table_6_15["raw_chem_name"].iloc[j].split())

table_6_15["data_document_id"]="1374855"
table_6_15["data_document_filename"]="DCPS_121_s.pdf"
table_6_15["doc_date"]="2013"
table_6_15["raw_category"]=""
table_6_15["cat_code"]=""
table_6_15["description_cpcat"]=""
table_6_15["cpcat_code"]=""
table_6_15["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_15["report_funcuse"]=""

table_6_15.to_csv("dcps_121_table_6_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 6_16
table_6_16=read_pdf("document_1374856.pdf", pages="74", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6_16["raw_chem_name"]=table_6_16.iloc[:,0]
table_6_16=table_6_16.dropna(subset=["raw_chem_name"])
table_6_16=table_6_16.loc[table_6_16["raw_chem_name"]!="Concentration of hair dye substances"]
table_6_16=table_6_16.loc[table_6_16["raw_chem_name"]!="Number of analyzed hair dye products"]

table_6_16=table_6_16.reset_index()
table_6_16=table_6_16[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_16)):
    table_6_16["raw_chem_name"].iloc[j]=str(table_6_16["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_6_16["raw_chem_name"].iloc[j]=clean(str(table_6_16["raw_chem_name"].iloc[j]))
    if len(table_6_16["raw_chem_name"].iloc[j].split())>1:
        table_6_16["raw_chem_name"].iloc[j]=" ".join(table_6_16["raw_chem_name"].iloc[j].split())

table_6_16=table_6_16.drop(3)
table_6_16=table_6_16.reset_index()
table_6_16=table_6_16[["raw_chem_name"]]

table_6_16["data_document_id"]="1374856"
table_6_16["data_document_filename"]="DCPS_121_t.pdf"
table_6_16["doc_date"]="2013"
table_6_16["raw_category"]=""
table_6_16["cat_code"]=""
table_6_16["description_cpcat"]=""
table_6_16["cpcat_code"]=""
table_6_16["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6_16["report_funcuse"]=""

table_6_16.to_csv("dcps_121_table_6_16.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 7_1
table_7_1=read_pdf("document_1374857.pdf", pages="76", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_7_1["raw_chem_name"]=table_7_1.iloc[:,0]
table_7_1["raw_cas"]=table_7_1.iloc[:,2]
table_7_1=table_7_1.dropna(subset=["raw_chem_name"])
table_7_1=table_7_1.loc[table_7_1["raw_chem_name"]!="INCI Name"]

table_7_1=table_7_1.reset_index()
table_7_1=table_7_1[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7_1)):
    table_7_1["raw_chem_name"].iloc[j]=str(table_7_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_7_1["raw_chem_name"].iloc[j]=clean(str(table_7_1["raw_chem_name"].iloc[j]))
    if str(table_7_1["raw_cas"].iloc[j])=="nan":
        table_7_1["raw_chem_name"].iloc[j]=table_7_1["raw_chem_name"].iloc[j-1]+table_7_1["raw_chem_name"].iloc[j]
        table_7_1["raw_cas"].iloc[j]=table_7_1["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_7_1=table_7_1.drop(j_drop)
table_7_1=table_7_1.reset_index()
table_7_1=table_7_1[["raw_chem_name","raw_cas"]]

table_7_1["data_document_id"]="1374857"
table_7_1["data_document_filename"]="DCPS_121_u.pdf"
table_7_1["doc_date"]="2013"
table_7_1["raw_category"]=""
table_7_1["cat_code"]=""
table_7_1["description_cpcat"]=""
table_7_1["cpcat_code"]=""
table_7_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_7_1["report_funcuse"]=""

table_7_1.to_csv("dcps_121_table_7_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
