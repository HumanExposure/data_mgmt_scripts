#lkoval
#6-26-19

from tabula import read_pdf
import pandas as pd
import string

#Table 4.2
table_4_2=read_pdf("document_1374613.pdf", pages="57,58", lattice=True, pandas_options={'header': None})
table_4_2["raw_chem_name"]=table_4_2.iloc[:,0]
table_4_2=table_4_2.dropna(subset=["raw_chem_name"])
table_4_2=table_4_2.loc[table_4_2["raw_chem_name"]!="Element"]
table_4_2=table_4_2[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_2)):
    table_4_2["raw_chem_name"].iloc[j]=str(table_4_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_2["raw_chem_name"].iloc[j]=clean(str(table_4_2["raw_chem_name"].iloc[j]))

table_4_2["data_document_id"]="1374613"
table_4_2["data_document_filename"]="DCPS_116_b.pdf"
table_4_2["doc_date"]="2012"
table_4_2["raw_category"]=""
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_2["report_funcuse"]=""

table_4_2.to_csv("dcps_116_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.7
table_4_7=read_pdf("document_1374614.pdf", pages="62", lattice=True, pandas_options={'header': None})
table_4_7["raw_chem_name"]=table_4_7.iloc[2:,0]
table_4_7["raw_cas"]=table_4_7.iloc[2:,1]
table_4_7=table_4_7.dropna(subset=["raw_chem_name"])
table_4_7=table_4_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_7)):
    table_4_7["raw_chem_name"].iloc[j]=str(table_4_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_7["raw_chem_name"].iloc[j]=clean(str(table_4_7["raw_chem_name"].iloc[j]))
    if len(table_4_7["raw_chem_name"].iloc[j].split())>1:
        table_4_7["raw_chem_name"].iloc[j]="".join(table_4_7["raw_chem_name"].iloc[j].split())
    if len(str(table_4_7["raw_cas"].iloc[j]).split())>1:
        table_4_7["raw_cas"].iloc[j]="".join(str(table_4_7["raw_cas"].iloc[j]).split())

table_4_7["data_document_id"]="1374614"
table_4_7["data_document_filename"]="DCPS_116_c.pdf"
table_4_7["doc_date"]="2012"
table_4_7["raw_category"]=""
table_4_7["cat_code"]=""
table_4_7["description_cpcat"]=""
table_4_7["cpcat_code"]=""
table_4_7["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_7["report_funcuse"]=""

table_4_7.to_csv("dcps_116_table_4_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.18
table_4_18=read_pdf("document_1374624.pdf", pages="75", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_18=table_4_18[0]
table_4_18["raw_chem_name"]=table_4_18.iloc[1:,0]
table_4_18["raw_cas"]=table_4_18.iloc[1:,1]
table_4_18=table_4_18.dropna(subset=["raw_chem_name"])
table_4_18=table_4_18[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_18)):
    table_4_18["raw_chem_name"].iloc[j]=str(table_4_18["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_18["raw_chem_name"].iloc[j]=clean(str(table_4_18["raw_chem_name"].iloc[j]))
    if len(table_4_18["raw_chem_name"].iloc[j].split())>1:
        table_4_18["raw_chem_name"].iloc[j]=" ".join(table_4_18["raw_chem_name"].iloc[j].split())
    if len(str(table_4_18["raw_cas"].iloc[j]).split())>1:
        table_4_18["raw_cas"].iloc[j]="".join(str(table_4_18["raw_cas"].iloc[j]).split())

table_4_18["data_document_id"]="1374624"
table_4_18["data_document_filename"]="DCPS_116_m.pdf"
table_4_18["doc_date"]="2012"
table_4_18["raw_category"]=""
table_4_18["cat_code"]=""
table_4_18["description_cpcat"]=""
table_4_18["cpcat_code"]=""
table_4_18["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_18["report_funcuse"]=""

table_4_18.to_csv("dcps_116_table_4_18.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.19
table_4_19=read_pdf("document_1374625.pdf", pages="75-76", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_19=pd.concat(table_4_19[1:3], ignore_index=True)
table_4_19["raw_chem_name"]=table_4_19.iloc[:,0]
table_4_19=table_4_19.loc[table_4_19["raw_chem_name"]!="Name"]
table_4_19=table_4_19.dropna(subset=["raw_chem_name"])
table_4_19=table_4_19.reset_index()
table_4_19=table_4_19[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_19)):
    table_4_19["raw_chem_name"].iloc[j]=str(table_4_19["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_19["raw_chem_name"].iloc[j]=clean(str(table_4_19["raw_chem_name"].iloc[j]))
    if len(table_4_19["raw_chem_name"].iloc[j].split())>1:
        table_4_19["raw_chem_name"].iloc[j]=" ".join(table_4_19["raw_chem_name"].iloc[j].split())

table_4_19["data_document_id"]="1374625"
table_4_19["data_document_filename"]="DCPS_116_n.pdf"
table_4_19["doc_date"]="2012"
table_4_19["raw_category"]=""
table_4_19["cat_code"]=""
table_4_19["description_cpcat"]=""
table_4_19["cpcat_code"]=""
table_4_19["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_19["report_funcuse"]=""

table_4_19.to_csv("dcps_116_table_4_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 4.20
table_4_20=read_pdf("document_1374626.pdf", pages="76", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4_20=table_4_20[1]
table_4_20["raw_chem_name"]=table_4_20.iloc[:,0]
table_4_20["raw_cas"]=table_4_20.iloc[:,1]
table_4_20=table_4_20.loc[table_4_20["raw_chem_name"]!="Name"]
table_4_20=table_4_20.dropna(subset=["raw_chem_name"])
table_4_20=table_4_20.reset_index()
table_4_20=table_4_20[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_20)):
    table_4_20["raw_chem_name"].iloc[j]=str(table_4_20["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_4_20["raw_chem_name"].iloc[j]=clean(str(table_4_20["raw_chem_name"].iloc[j]))
    if len(table_4_20["raw_chem_name"].iloc[j].split())>1:
        table_4_20["raw_chem_name"].iloc[j]=" ".join(table_4_20["raw_chem_name"].iloc[j].split())

table_4_20["data_document_id"]="1374626"
table_4_20["data_document_filename"]="DCPS_116_o.pdf"
table_4_20["doc_date"]="2012"
table_4_20["raw_category"]=""
table_4_20["cat_code"]=""
table_4_20["description_cpcat"]=""
table_4_20["cpcat_code"]=""
table_4_20["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4_20["report_funcuse"]=""

table_4_20.to_csv("dcps_116_table_4_20.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#A1
A1=read_pdf("document_1374627.pdf", pages="124,125", lattice=True, pandas_options={'header': None})
A1["raw_chem_name"]=A1.iloc[:,0]
A1["raw_cas"]=A1.iloc[:,1]
A1=A1.loc[A1["raw_chem_name"]!="Name"]
A1=A1.dropna(subset=["raw_chem_name"])
A1=A1.reset_index()
A1=A1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(A1)):
    A1["raw_chem_name"].iloc[j]=str(A1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    A1["raw_chem_name"].iloc[j]=clean(str(A1["raw_chem_name"].iloc[j]))
    if len(A1["raw_chem_name"].iloc[j].split())>1:
        A1["raw_chem_name"].iloc[j]=" ".join(A1["raw_chem_name"].iloc[j].split())
    if len(str(A1["raw_cas"].iloc[j]).split())>1:
        A1["raw_cas"].iloc[j]="".join(str(A1["raw_cas"].iloc[j]).split())

A1=A1.drop_duplicates()
A1=A1.reset_index()
A1=A1[["raw_chem_name","raw_cas"]]

A1["data_document_id"]="1374627"
A1["data_document_filename"]="DCPS_116_p.pdf"
A1["doc_date"]="2012"
A1["raw_category"]=""
A1["cat_code"]=""
A1["description_cpcat"]=""
A1["cpcat_code"]=""
A1["cpcat_sourcetype"]="ACToR Assays and Lists"
A1["report_funcuse"]=""

A1.to_csv("dcps_116_A1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#A2
A2=read_pdf("document_1374628.pdf", pages="126", lattice=True, pandas_options={'header': None})
A2["raw_chem_name"]=A2.iloc[:,0]
A2["raw_cas"]=A2.iloc[:,1]
A2=A2.loc[A2["raw_chem_name"]!="Name"]
A2=A2.dropna(subset=["raw_chem_name"])
A2=A2.reset_index()
A2=A2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(A2)):
    A2["raw_chem_name"].iloc[j]=str(A2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    A2["raw_chem_name"].iloc[j]=clean(str(A2["raw_chem_name"].iloc[j]))
    if len(A2["raw_chem_name"].iloc[j].split())>1:
        A2["raw_chem_name"].iloc[j]=" ".join(A2["raw_chem_name"].iloc[j].split())
    if len(str(A2["raw_cas"].iloc[j]).split())>1:
        A2["raw_cas"].iloc[j]="".join(str(A2["raw_cas"].iloc[j]).split())


A2["data_document_id"]="1374628"
A2["data_document_filename"]="DCPS_116_q.pdf"
A2["doc_date"]="2012"
A2["raw_category"]=""
A2["cat_code"]=""
A2["description_cpcat"]=""
A2["cpcat_code"]=""
A2["cpcat_sourcetype"]="ACToR Assays and Lists"
A2["report_funcuse"]=""

A2.to_csv("dcps_116_A2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#B1
B1=read_pdf("document_1374629.pdf", pages="127,128", lattice=True, pandas_options={'header': None})
B1["raw_chem_name"]=B1.iloc[:,1]
B1["raw_cas"]=B1.iloc[:,0]
B1=B1.loc[B1["raw_chem_name"]!="Pigment"]
B1=B1.dropna(subset=["raw_chem_name"])
B1=B1.reset_index()
B1=B1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(B1)):
    B1["raw_chem_name"].iloc[j]=str(B1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    B1["raw_chem_name"].iloc[j]=clean(str(B1["raw_chem_name"].iloc[j]))
    if len(B1["raw_chem_name"].iloc[j].split())>1:
        B1["raw_chem_name"].iloc[j]=" ".join(B1["raw_chem_name"].iloc[j].split())
    if "CAS#" in str(B1["raw_cas"].iloc[j]).split():
        B1["raw_cas"].iloc[j]=str(B1["raw_cas"].iloc[j]).split()[-1]
    else:
        B1["raw_cas"].iloc[j]=""

B1=B1.drop_duplicates()
B1=B1.reset_index()
B1=B1[["raw_chem_name","raw_cas"]]

B1["data_document_id"]="1374629"
B1["data_document_filename"]="DCPS_116_r.pdf"
B1["doc_date"]="2012"
B1["raw_category"]=""
B1["cat_code"]=""
B1["description_cpcat"]=""
B1["cpcat_code"]=""
B1["cpcat_sourcetype"]="ACToR Assays and Lists"
B1["report_funcuse"]=""

B1.to_csv("dcps_116_B1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#B2
B2=read_pdf("document_1374630.pdf", pages="129,130", lattice=True, pandas_options={'header': None})
B2["raw_chem_name"]=B2.iloc[:,1]
B2["raw_cas"]=B2.iloc[:,0]
B2=B2.loc[B2["raw_chem_name"]!="Pigment name"]
B2=B2.dropna(subset=["raw_chem_name"])
B2=B2.reset_index()
B2=B2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(B2)):
    B2["raw_chem_name"].iloc[j]=str(B2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    B2["raw_chem_name"].iloc[j]=clean(str(B2["raw_chem_name"].iloc[j]))
    if len(B2["raw_chem_name"].iloc[j].split())>1:
        B2["raw_chem_name"].iloc[j]=" ".join(B2["raw_chem_name"].iloc[j].split())
    if "CAS#" in str(B2["raw_cas"].iloc[j]).split():
        B2["raw_cas"].iloc[j]=str(B2["raw_cas"].iloc[j]).split()[-1]
    else:
        B2["raw_cas"].iloc[j]=""

B2=B2.drop_duplicates()
B2=B2.reset_index()
B2=B2[["raw_chem_name","raw_cas"]]

B2["data_document_id"]="1374630"
B2["data_document_filename"]="DCPS_116_s.pdf"
B2["doc_date"]="2012"
B2["raw_category"]=""
B2["cat_code"]=""
B2["description_cpcat"]=""
B2["cpcat_code"]=""
B2["cpcat_sourcetype"]="ACToR Assays and Lists"
B2["report_funcuse"]=""

B2.to_csv("dcps_116_B2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#B6
B6=read_pdf("document_1374634.pdf", pages="132", lattice=True, pandas_options={'header': None})
B6["raw_chem_name"]=B6.iloc[:,1]
B6["raw_cas"]=B6.iloc[:,0]
B6=B6.loc[B6["raw_chem_name"]!="Pigment name"]
B6=B6.dropna(subset=["raw_chem_name"])
B6=B6.reset_index()
B6=B6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(B6)):
    B6["raw_chem_name"].iloc[j]=str(B6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    B6["raw_chem_name"].iloc[j]=clean(str(B6["raw_chem_name"].iloc[j]))
    if len(B6["raw_chem_name"].iloc[j].split())>1:
        B6["raw_chem_name"].iloc[j]=" ".join(B6["raw_chem_name"].iloc[j].split())
    if "CAS#" in str(B6["raw_cas"].iloc[j]).split():
        B6["raw_cas"].iloc[j]=str(B6["raw_cas"].iloc[j]).split()[-1]
    else:
        B6["raw_cas"].iloc[j]=""

B6=B6.drop_duplicates()
B6=B6.reset_index()
B6=B6[["raw_chem_name","raw_cas"]]

B6["data_document_id"]="1374634"
B6["data_document_filename"]="DCPS_116_w.pdf"
B6["doc_date"]="2012"
B6["raw_category"]=""
B6["cat_code"]=""
B6["description_cpcat"]=""
B6["cpcat_code"]=""
B6["cpcat_sourcetype"]="ACToR Assays and Lists"
B6["report_funcuse"]=""

B6.to_csv("dcps_116_B6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#B7
B7=read_pdf("document_1374635.pdf", pages="133,134", lattice=True, multiple_tables=True, pandas_options={'header': None})
B7=pd.concat(B7[:2])
B7["raw_chem_name"]=B7.iloc[:,1]
B7["raw_cas"]=B7.iloc[:,0]
B7=B7.loc[B7["raw_chem_name"]!="Pigment name"]
B7=B7.dropna(subset=["raw_chem_name"])
B7=B7.reset_index()
B7=B7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(B7)):
    B7["raw_chem_name"].iloc[j]=str(B7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    B7["raw_chem_name"].iloc[j]=clean(str(B7["raw_chem_name"].iloc[j]))
    if len(B7["raw_chem_name"].iloc[j].split())>1:
        B7["raw_chem_name"].iloc[j]=" ".join(B7["raw_chem_name"].iloc[j].split())
    if "CAS#" in str(B7["raw_cas"].iloc[j]).split():
        B7["raw_cas"].iloc[j]=str(B7["raw_cas"].iloc[j]).split()[-1]
    else:
        B7["raw_cas"].iloc[j]=""

B7=B7.drop_duplicates()
B7=B7.reset_index()
B7=B7[["raw_chem_name","raw_cas"]]

B7["data_document_id"]="1374635"
B7["data_document_filename"]="DCPS_116_x.pdf"
B7["doc_date"]="2012"
B7["raw_category"]=""
B7["cat_code"]=""
B7["description_cpcat"]=""
B7["cpcat_code"]=""
B7["cpcat_sourcetype"]="ACToR Assays and Lists"
B7["report_funcuse"]=""

B7.to_csv("dcps_116_B7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#B8
B8=read_pdf("document_1374636.pdf", pages="134", lattice=True, multiple_tables=True, pandas_options={'header': None})
B8=B8[1]
B8["raw_chem_name"]=B8.iloc[:,1]
B8["raw_cas"]=B8.iloc[:,0]
B8=B8.loc[B8["raw_chem_name"]!="Pigment name"]
B8=B8.dropna(subset=["raw_chem_name"])
B8=B8.reset_index()
B8=B8[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(B8)):
    B8["raw_chem_name"].iloc[j]=str(B8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    B8["raw_chem_name"].iloc[j]=clean(str(B8["raw_chem_name"].iloc[j]))
    if len(B8["raw_chem_name"].iloc[j].split())>1:
        B8["raw_chem_name"].iloc[j]=" ".join(B8["raw_chem_name"].iloc[j].split())
    if "CAS#" in str(B8["raw_cas"].iloc[j]).split():
        B8["raw_cas"].iloc[j]=str(B8["raw_cas"].iloc[j]).split()[-1]
    else:
        B8["raw_cas"].iloc[j]=""

B8=B8.drop_duplicates()
B8=B8.reset_index()
B8=B8[["raw_chem_name","raw_cas"]]

B8["data_document_id"]="1374636"
B8["data_document_filename"]="DCPS_116_y.pdf"
B8["doc_date"]="2012"
B8["raw_category"]=""
B8["cat_code"]=""
B8["description_cpcat"]=""
B8["cpcat_code"]=""
B8["cpcat_sourcetype"]="ACToR Assays and Lists"
B8["report_funcuse"]=""

B8.to_csv("dcps_116_B8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C1
C1=read_pdf("document_1374637.pdf", pages="135,136", lattice=True, pandas_options={'header': None})
C1["raw_chem_name"]=C1.iloc[:,0]
C1=C1.loc[C1["raw_chem_name"]!="Element"]
C1=C1.dropna(subset=["raw_chem_name"])
C1=C1.reset_index()
C1=C1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C1)):
    C1["raw_chem_name"].iloc[j]=str(C1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C1["raw_chem_name"].iloc[j]=clean(str(C1["raw_chem_name"].iloc[j]))

C1["data_document_id"]="1374637"
C1["data_document_filename"]="DCPS_116_z.pdf"
C1["doc_date"]="2012"
C1["raw_category"]=""
C1["cat_code"]=""
C1["description_cpcat"]=""
C1["cpcat_code"]=""
C1["cpcat_sourcetype"]="ACToR Assays and Lists"
C1["report_funcuse"]=""

C1.to_csv("dcps_116_C1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C2
C2=read_pdf("document_1374638.pdf", pages="137,138", lattice=True, pandas_options={'header': None})
C2["raw_chem_name"]=C2.iloc[:,0]
C2=C2.loc[C2["raw_chem_name"]!="Element"]
C2=C2.dropna(subset=["raw_chem_name"])
C2=C2.reset_index()
C2=C2[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C2)):
    C2["raw_chem_name"].iloc[j]=str(C2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C2["raw_chem_name"].iloc[j]=clean(str(C2["raw_chem_name"].iloc[j]))

C2["data_document_id"]="1374638"
C2["data_document_filename"]="DCPS_116_aa.pdf"
C2["doc_date"]="2012"
C2["raw_category"]=""
C2["cat_code"]=""
C2["description_cpcat"]=""
C2["cpcat_code"]=""
C2["cpcat_sourcetype"]="ACToR Assays and Lists"
C2["report_funcuse"]=""

C2.to_csv("dcps_116_C2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C3
C3=read_pdf("document_1374639.pdf", pages="139,140", lattice=True, pandas_options={'header': None})
C3["raw_chem_name"]=C3.iloc[:,0]
C3=C3.loc[C3["raw_chem_name"]!="Element"]
C3=C3.dropna(subset=["raw_chem_name"])
C3=C3.reset_index()
C3=C3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C3)):
    C3["raw_chem_name"].iloc[j]=str(C3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C3["raw_chem_name"].iloc[j]=clean(str(C3["raw_chem_name"].iloc[j]))

C3["data_document_id"]="1374639"
C3["data_document_filename"]="DCPS_116_ab.pdf"
C3["doc_date"]="2012"
C3["raw_category"]=""
C3["cat_code"]=""
C3["description_cpcat"]=""
C3["cpcat_code"]=""
C3["cpcat_sourcetype"]="ACToR Assays and Lists"
C3["report_funcuse"]=""

C3.to_csv("dcps_116_C3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C4
C4=read_pdf("document_1374640.pdf", pages="141,142", lattice=True, pandas_options={'header': None})
C4["raw_chem_name"]=C4.iloc[:,0]
C4=C4.loc[C4["raw_chem_name"]!="Element"]
C4=C4.dropna(subset=["raw_chem_name"])
C4=C4.reset_index()
C4=C4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C4)):
    C4["raw_chem_name"].iloc[j]=str(C4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C4["raw_chem_name"].iloc[j]=clean(str(C4["raw_chem_name"].iloc[j]))

C4["data_document_id"]="1374640"
C4["data_document_filename"]="DCPS_116_ac.pdf"
C4["doc_date"]="2012"
C4["raw_category"]=""
C4["cat_code"]=""
C4["description_cpcat"]=""
C4["cpcat_code"]=""
C4["cpcat_sourcetype"]="ACToR Assays and Lists"
C4["report_funcuse"]=""

C4.to_csv("dcps_116_C4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C5
C5=read_pdf("document_1374641.pdf", pages="143,144", lattice=True, pandas_options={'header': None})
C5["raw_chem_name"]=C5.iloc[:,0]
C5=C5.loc[C5["raw_chem_name"]!="Element"]
C5=C5.dropna(subset=["raw_chem_name"])
C5=C5.reset_index()
C5=C5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C5)):
    C5["raw_chem_name"].iloc[j]=str(C5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C5["raw_chem_name"].iloc[j]=clean(str(C5["raw_chem_name"].iloc[j]))

C5["data_document_id"]="1374641"
C5["data_document_filename"]="DCPS_116_ad.pdf"
C5["doc_date"]="2012"
C5["raw_category"]=""
C5["cat_code"]=""
C5["description_cpcat"]=""
C5["cpcat_code"]=""
C5["cpcat_sourcetype"]="ACToR Assays and Lists"
C5["report_funcuse"]=""

C5.to_csv("dcps_116_C5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C6
C6=read_pdf("document_1374642.pdf", pages="145,146", lattice=True, pandas_options={'header': None})
C6["raw_chem_name"]=C6.iloc[:,0]
C6=C6.loc[C6["raw_chem_name"]!="Element"]
C6=C6.dropna(subset=["raw_chem_name"])
C6=C6.reset_index()
C6=C6[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C6)):
    C6["raw_chem_name"].iloc[j]=str(C6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C6["raw_chem_name"].iloc[j]=clean(str(C6["raw_chem_name"].iloc[j]))

C6["data_document_id"]="1374642"
C6["data_document_filename"]="DCPS_116_ae.pdf"
C6["doc_date"]="2012"
C6["raw_category"]=""
C6["cat_code"]=""
C6["description_cpcat"]=""
C6["cpcat_code"]=""
C6["cpcat_sourcetype"]="ACToR Assays and Lists"
C6["report_funcuse"]=""

C6.to_csv("dcps_116_C6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C7
C7=read_pdf("document_1374643.pdf", pages="147,148", lattice=True, pandas_options={'header': None})
C7["raw_chem_name"]=C7.iloc[:,0]
C7=C7.loc[C7["raw_chem_name"]!="Element"]
C7=C7.dropna(subset=["raw_chem_name"])
C7=C7.reset_index()
C7=C7[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C7)):
    C7["raw_chem_name"].iloc[j]=str(C7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C7["raw_chem_name"].iloc[j]=clean(str(C7["raw_chem_name"].iloc[j]))

C7["data_document_id"]="1374643"
C7["data_document_filename"]="DCPS_116_af.pdf"
C7["doc_date"]="2012"
C7["raw_category"]=""
C7["cat_code"]=""
C7["description_cpcat"]=""
C7["cpcat_code"]=""
C7["cpcat_sourcetype"]="ACToR Assays and Lists"
C7["report_funcuse"]=""

C7.to_csv("dcps_116_C7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#C8
C8=read_pdf("document_1374643.pdf", pages="147,148", lattice=True, pandas_options={'header': None})
C8["raw_chem_name"]=C8.iloc[:,0]
C8=C8.loc[C8["raw_chem_name"]!="Element"]
C8=C8.dropna(subset=["raw_chem_name"])
C8=C8.reset_index()
C8=C8[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(C8)):
    C8["raw_chem_name"].iloc[j]=str(C8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    C8["raw_chem_name"].iloc[j]=clean(str(C8["raw_chem_name"].iloc[j]))

C8["data_document_id"]="1374643"
C8["data_document_filename"]="DCPS_116_af.pdf"
C8["doc_date"]="2012"
C8["raw_category"]=""
C8["cat_code"]=""
C8["description_cpcat"]=""
C8["cpcat_code"]=""
C8["cpcat_sourcetype"]="ACToR Assays and Lists"
C8["report_funcuse"]=""

C8.to_csv("dcps_116_C8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
