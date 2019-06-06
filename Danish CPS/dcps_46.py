#lkoval
#6-5-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.1
tables=read_pdf("document_1373633.pdf", pages="21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1=tables[0]
table_3_1["raw_chem_name"]=table_3_1.iloc[:,0]
table_3_1["raw_cas"]=table_3_1.iloc[:,1]
table_3_1=table_3_1.dropna(subset=["raw_chem_name"])
table_3_1=table_3_1.loc[table_3_1["raw_chem_name"]!="Substance"]
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[j]=str(table_3_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3_1["raw_chem_name"].iloc[j]=clean(str(table_3_1["raw_chem_name"].iloc[j]))
    if len(table_3_1["raw_chem_name"].iloc[j].split())>1:
        table_3_1["raw_chem_name"].iloc[j]=" ".join(table_3_1["raw_chem_name"].iloc[j].split())


table_3_1["data_document_id"]="1373633"
table_3_1["data_document_filename"]="DCPS_46_a.pdf"
table_3_1["doc_date"]="2004"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1.to_csv("dcps_46_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.2
tables=read_pdf("document_1373634.pdf", pages="21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_2=tables[1]
table_3_2["raw_chem_name"]=table_3_2.iloc[:,0]
table_3_2["raw_cas"]=table_3_2.iloc[:,1]
table_3_2=table_3_2.dropna(subset=["raw_chem_name"])
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!="Substance"]
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(table_3_2["raw_chem_name"].iloc[j].split())>1:
        table_3_2["raw_chem_name"].iloc[j]=" ".join(table_3_2["raw_chem_name"].iloc[j].split())

table_3_2["data_document_id"]="1373634"
table_3_2["data_document_filename"]="DCPS_46_b.pdf"
table_3_2["doc_date"]="2004"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_46_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.3
tables=read_pdf("document_1373635.pdf", pages="21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_3=tables[2]
table_3_3["raw_chem_name"]=table_3_3.iloc[:,0]
table_3_3["raw_cas"]=table_3_3.iloc[:,1]
table_3_3=table_3_3.dropna(subset=["raw_chem_name"])
table_3_3=table_3_3.loc[table_3_3["raw_chem_name"]!="Substance"]
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[j]=str(table_3_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3_3["raw_chem_name"].iloc[j]=clean(str(table_3_3["raw_chem_name"].iloc[j]))
    if len(table_3_3["raw_chem_name"].iloc[j].split())>1:
        table_3_3["raw_chem_name"].iloc[j]=" ".join(table_3_3["raw_chem_name"].iloc[j].split())
    if len(str(table_3_3["raw_cas"].iloc[j]).split())>1:
        table_3_3["raw_cas"].iloc[j]=" ".join(str(table_3_3["raw_cas"].iloc[j]).split())

table_3_3["data_document_id"]="1373635"
table_3_3["data_document_filename"]="DCPS_46_c.pdf"
table_3_3["doc_date"]="2004"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("dcps_46_table_3_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.4
tables=read_pdf("document_1373636.pdf", pages="21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_4=tables[3]
table_3_4["raw_chem_name"]=table_3_4.iloc[:,0]
table_3_4["raw_cas"]=table_3_4.iloc[:,1]
table_3_4=table_3_4.dropna(subset=["raw_chem_name"])
table_3_4=table_3_4.loc[table_3_4["raw_chem_name"]!="Substance"]
table_3_4=table_3_4.reset_index()
table_3_4=table_3_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_4)):
    table_3_4["raw_chem_name"].iloc[j]=str(table_3_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3_4["raw_chem_name"].iloc[j]=clean(str(table_3_4["raw_chem_name"].iloc[j]))
    if len(table_3_4["raw_chem_name"].iloc[j].split())>1:
        table_3_4["raw_chem_name"].iloc[j]=" ".join(table_3_4["raw_chem_name"].iloc[j].split())

table_3_4["data_document_id"]="1373636"
table_3_4["data_document_filename"]="DCPS_46_d.pdf"
table_3_4["doc_date"]="2004"
table_3_4["raw_category"]=""
table_3_4["cat_code"]=""
table_3_4["description_cpcat"]=""
table_3_4["cpcat_code"]=""
table_3_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_4.to_csv("dcps_46_table_3_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.5
tables=read_pdf("document_1373637.pdf", pages="21,22", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_5=pd.concat([tables[4],tables[5]], ignore_index=True)
table_3_5["raw_chem_name"]=table_3_5.iloc[:,0]
table_3_5["raw_cas"]=table_3_5.iloc[:,1]
table_3_5=table_3_5.dropna(subset=["raw_chem_name"])
table_3_5=table_3_5.loc[table_3_5["raw_chem_name"]!="Substance"]
table_3_5=table_3_5.reset_index()
table_3_5=table_3_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_5)):
    table_3_5["raw_chem_name"].iloc[j]=str(table_3_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3_5["raw_chem_name"].iloc[j]=clean(str(table_3_5["raw_chem_name"].iloc[j]))
    if len(table_3_5["raw_chem_name"].iloc[j].split())>1:
        table_3_5["raw_chem_name"].iloc[j]=" ".join(table_3_5["raw_chem_name"].iloc[j].split())

table_3_5["data_document_id"]="1373637"
table_3_5["data_document_filename"]="DCPS_46_e.pdf"
table_3_5["doc_date"]="2004"
table_3_5["raw_category"]=""
table_3_5["cat_code"]=""
table_3_5["description_cpcat"]=""
table_3_5["cpcat_code"]=""
table_3_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_5.to_csv("dcps_46_table_3_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.6
tables=read_pdf("document_1373638.pdf", pages="22", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_6=tables[1]
table_3_6["raw_chem_name"]=table_3_6.iloc[:,0]
table_3_6["raw_cas"]=table_3_6.iloc[:,1]
table_3_6=table_3_6.dropna(subset=["raw_chem_name"])
table_3_6=table_3_6.loc[table_3_6["raw_chem_name"]!="Substance"]
table_3_6=table_3_6.reset_index()
table_3_6=table_3_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_6)):
    table_3_6["raw_chem_name"].iloc[j]=str(table_3_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_3_6["raw_chem_name"].iloc[j]=clean(str(table_3_6["raw_chem_name"].iloc[j]))
    if len(table_3_6["raw_chem_name"].iloc[j].split())>1:
        table_3_6["raw_chem_name"].iloc[j]=" ".join(table_3_6["raw_chem_name"].iloc[j].split())
    if len(str(table_3_6["raw_cas"].iloc[j]).split())>1:
        table_3_6["raw_cas"].iloc[j]="".join(str(table_3_6["raw_cas"].iloc[j]).split())

table_3_6["data_document_id"]="1373638"
table_3_6["data_document_filename"]="DCPS_46_f.pdf"
table_3_6["doc_date"]="2004"
table_3_6["raw_category"]=""
table_3_6["cat_code"]=""
table_3_6["description_cpcat"]=""
table_3_6["cpcat_code"]=""
table_3_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_6.to_csv("dcps_46_table_3_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.7
tables=read_pdf("document_1373639.pdf", pages="22", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_7=tables[2]
table_3_7["raw_chem_name"]=table_3_7.iloc[:,0]
table_3_7["raw_cas"]=table_3_7.iloc[:,1]
table_3_7=table_3_7.dropna(subset=["raw_chem_name"])
table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!="Substance"]
table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_7)):
    table_3_7["raw_chem_name"].iloc[j]=str(table_3_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_7["raw_chem_name"].iloc[j]=clean(str(table_3_7["raw_chem_name"].iloc[j]))
    if len(table_3_7["raw_chem_name"].iloc[j].split())>1:
        table_3_7["raw_chem_name"].iloc[j]=" ".join(table_3_7["raw_chem_name"].iloc[j].split())
    if len(str(table_3_7["raw_cas"].iloc[j]).split())>1:
        table_3_7["raw_cas"].iloc[j]="".join(str(table_3_7["raw_cas"].iloc[j]).split())

table_3_7["data_document_id"]="1373639"
table_3_7["data_document_filename"]="DCPS_46_g.pdf"
table_3_7["doc_date"]="2004"
table_3_7["raw_category"]=""
table_3_7["cat_code"]=""
table_3_7["description_cpcat"]=""
table_3_7["cpcat_code"]=""
table_3_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_7.to_csv("dcps_46_table_3_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.8
tables=read_pdf("document_1373640.pdf", pages="22,23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_8=pd.concat([tables[3],tables[4]], ignore_index=True)
table_3_8["raw_chem_name"]=table_3_8.iloc[:,0]
table_3_8["raw_cas"]=table_3_8.iloc[:,1]
table_3_8=table_3_8.dropna(subset=["raw_chem_name"])
table_3_8=table_3_8.loc[table_3_8["raw_chem_name"]!="Substance"]
table_3_8=table_3_8.reset_index()
table_3_8=table_3_8[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_8)):
    table_3_8["raw_chem_name"].iloc[j]=str(table_3_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_8["raw_chem_name"].iloc[j]=clean(str(table_3_8["raw_chem_name"].iloc[j]))
    if len(table_3_8["raw_chem_name"].iloc[j].split())>1:
        table_3_8["raw_chem_name"].iloc[j]=" ".join(table_3_8["raw_chem_name"].iloc[j].split())

table_3_8["data_document_id"]="1373640"
table_3_8["data_document_filename"]="DCPS_46_h.pdf"
table_3_8["doc_date"]="2004"
table_3_8["raw_category"]=""
table_3_8["cat_code"]=""
table_3_8["description_cpcat"]=""
table_3_8["cpcat_code"]=""
table_3_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_8.to_csv("dcps_46_table_3_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.9
tables=read_pdf("document_1373641.pdf", pages="23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_9=tables[1]
table_3_9["raw_chem_name"]=table_3_9.iloc[:,0]
table_3_9["raw_cas"]=table_3_9.iloc[:,1]
table_3_9=table_3_9.dropna(subset=["raw_chem_name"])
table_3_9=table_3_9.loc[table_3_9["raw_chem_name"]!="Substance"]
table_3_9=table_3_9.reset_index()
table_3_9=table_3_9[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_9)):
    table_3_9["raw_chem_name"].iloc[j]=str(table_3_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_9["raw_chem_name"].iloc[j]=clean(str(table_3_9["raw_chem_name"].iloc[j]))
    if len(table_3_9["raw_chem_name"].iloc[j].split())>1:
        table_3_9["raw_chem_name"].iloc[j]=" ".join(table_3_9["raw_chem_name"].iloc[j].split())

table_3_9["data_document_id"]="1373641"
table_3_9["data_document_filename"]="DCPS_46_i.pdf"
table_3_9["doc_date"]="2004"
table_3_9["raw_category"]=""
table_3_9["cat_code"]=""
table_3_9["description_cpcat"]=""
table_3_9["cpcat_code"]=""
table_3_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_9.to_csv("dcps_46_table_3_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.10
tables=read_pdf("document_1373642.pdf", pages="24", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_10=tables[0]
table_3_10["raw_chem_name"]=table_3_10.iloc[:,0]
table_3_10["raw_cas"]=table_3_10.iloc[:,1]
table_3_10=table_3_10.dropna(subset=["raw_chem_name"])
table_3_10=table_3_10.loc[table_3_10["raw_chem_name"]!="Substance"]
table_3_10=table_3_10.reset_index()
table_3_10=table_3_10[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_10)):
    table_3_10["raw_chem_name"].iloc[j]=str(table_3_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_10["raw_chem_name"].iloc[j]=clean(str(table_3_10["raw_chem_name"].iloc[j]))
    if len(table_3_10["raw_chem_name"].iloc[j].split())>1:
        table_3_10["raw_chem_name"].iloc[j]=" ".join(table_3_10["raw_chem_name"].iloc[j].split())

table_3_10["data_document_id"]="1373642"
table_3_10["data_document_filename"]="DCPS_46_j.pdf"
table_3_10["doc_date"]="2004"
table_3_10["raw_category"]=""
table_3_10["cat_code"]=""
table_3_10["description_cpcat"]=""
table_3_10["cpcat_code"]=""
table_3_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_10.to_csv("dcps_46_table_3_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.11
tables=read_pdf("document_1373643.pdf", pages="24", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_11=tables[1]
table_3_11["raw_chem_name"]=table_3_11.iloc[:,0]
table_3_11["raw_cas"]=table_3_11.iloc[:,1]
table_3_11=table_3_11.dropna(subset=["raw_chem_name"])
table_3_11=table_3_11.loc[table_3_11["raw_chem_name"]!="Substance"]
table_3_11=table_3_11.reset_index()
table_3_11=table_3_11[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_11)):
    table_3_11["raw_chem_name"].iloc[j]=str(table_3_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_11["raw_chem_name"].iloc[j]=clean(str(table_3_11["raw_chem_name"].iloc[j]))
    if len(table_3_11["raw_chem_name"].iloc[j].split())>1:
        table_3_11["raw_chem_name"].iloc[j]=" ".join(table_3_11["raw_chem_name"].iloc[j].split())

table_3_11["data_document_id"]="1373643"
table_3_11["data_document_filename"]="DCPS_46_k.pdf"
table_3_11["doc_date"]="2004"
table_3_11["raw_category"]=""
table_3_11["cat_code"]=""
table_3_11["description_cpcat"]=""
table_3_11["cpcat_code"]=""
table_3_11["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_11.to_csv("dcps_46_table_3_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.12
tables=read_pdf("document_1373644.pdf", pages="25", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_12=tables[0]
table_3_12["raw_chem_name"]=table_3_12.iloc[:,0]
table_3_12["raw_cas"]=table_3_12.iloc[:,1]
table_3_12=table_3_12.dropna(subset=["raw_chem_name"])
table_3_12=table_3_12.loc[table_3_12["raw_chem_name"]!="Substance"]
table_3_12=table_3_12.reset_index()
table_3_12=table_3_12[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_12)):
    table_3_12["raw_chem_name"].iloc[j]=str(table_3_12["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_3_12["raw_chem_name"].iloc[j]=clean(str(table_3_12["raw_chem_name"].iloc[j]))
    if len(table_3_12["raw_chem_name"].iloc[j].split())>1:
        table_3_12["raw_chem_name"].iloc[j]=" ".join(table_3_12["raw_chem_name"].iloc[j].split())

table_3_12["data_document_id"]="1373644"
table_3_12["data_document_filename"]="DCPS_46_l.pdf"
table_3_12["doc_date"]="2004"
table_3_12["raw_category"]=""
table_3_12["cat_code"]=""
table_3_12["description_cpcat"]=""
table_3_12["cpcat_code"]=""
table_3_12["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_12.to_csv("dcps_46_table_3_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.1
table_4_1=read_pdf("document_1373645.pdf", pages="28,29", lattice=True, pandas_options={'header': None})
table_4_1["raw_chem_name"]=table_4_1.iloc[:,1]
table_4_1["raw_cas"]=table_4_1.iloc[:,2]
table_4_1=table_4_1.dropna(subset=["raw_chem_name"])
table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!="Substance"]
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_1)):
    table_4_1["raw_chem_name"].iloc[j]=str(table_4_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_4_1["raw_chem_name"].iloc[j]=clean(str(table_4_1["raw_chem_name"].iloc[j]))
    if len(table_4_1["raw_chem_name"].iloc[j].split())>1:
        table_4_1["raw_chem_name"].iloc[j]=" ".join(table_4_1["raw_chem_name"].iloc[j].split())

table_4_1=table_4_1.drop_duplicates()
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

table_4_1["data_document_id"]="1373645"
table_4_1["data_document_filename"]="DCPS_46_m.pdf"
table_4_1["doc_date"]="2004"
table_4_1["raw_category"]=""
table_4_1["cat_code"]=""
table_4_1["description_cpcat"]=""
table_4_1["cpcat_code"]=""
table_4_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1.to_csv("dcps_46_table_4_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.2
table_4_2=read_pdf("document_1373646.pdf", pages="32", lattice=True, pandas_options={'header': None})
table_4_2["raw_chem_name"]=table_4_2.iloc[:,1]
table_4_2["raw_cas"]=table_4_2.iloc[:,2]
table_4_2=table_4_2.dropna(subset=["raw_chem_name"])
table_4_2=table_4_2.loc[table_4_2["raw_chem_name"]!="Name"]
table_4_2=table_4_2.reset_index()
table_4_2=table_4_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_2)):
    table_4_2["raw_chem_name"].iloc[j]=str(table_4_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_4_2["raw_chem_name"].iloc[j]=clean(str(table_4_2["raw_chem_name"].iloc[j]))

table_4_2["data_document_id"]="1373646"
table_4_2["data_document_filename"]="DCPS_46_n.pdf"
table_4_2["doc_date"]="2004"
table_4_2["raw_category"]=""
table_4_2["cat_code"]=""
table_4_2["description_cpcat"]=""
table_4_2["cpcat_code"]=""
table_4_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_2.to_csv("dcps_46_table_4_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.3
table_4_3=read_pdf("document_1373647.pdf", pages="33", lattice=True, pandas_options={'header': None})
table_4_3["raw_chem_name"]=table_4_3.iloc[:,0]
table_4_3["raw_cas"]=table_4_3.iloc[:,1]
table_4_3=table_4_3.dropna(subset=["raw_chem_name"])
table_4_3=table_4_3.loc[table_4_3["raw_chem_name"]!="Substance"]
table_4_3=table_4_3.reset_index()
table_4_3=table_4_3[["raw_chem_name","raw_cas"]]
table_4_3["raw_cas"].iloc[13]="nan"

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_3)):
    table_4_3["raw_chem_name"].iloc[j]=str(table_4_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_4_3["raw_chem_name"].iloc[j]=clean(str(table_4_3["raw_chem_name"].iloc[j]))
    if len(table_4_3["raw_chem_name"].iloc[j].split())>1:
        table_4_3["raw_chem_name"].iloc[j]=" ".join(table_4_3["raw_chem_name"].iloc[j].split())
    if len(str(table_4_3["raw_cas"].iloc[j]).split())>1:
        table_4_3["raw_cas"].iloc[j]="".join(str(table_4_3["raw_cas"].iloc[j]).split())
    if str(table_4_3["raw_cas"].iloc[j])=="nan" and table_4_3["raw_chem_name"].iloc[j]!="c10-c16":
        table_4_3["raw_chem_name"].iloc[j]=table_4_3["raw_chem_name"].iloc[j-1]+" "+table_4_3["raw_chem_name"].iloc[j]
        table_4_3["raw_cas"].iloc[j]=table_4_3["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_4_3=table_4_3.drop(j_drop)
table_4_3=table_4_3.reset_index()
table_4_3=table_4_3[["raw_chem_name","raw_cas"]]

table_4_3["data_document_id"]="1373647"
table_4_3["data_document_filename"]="DCPS_46_o.pdf"
table_4_3["doc_date"]="2004"
table_4_3["raw_category"]=""
table_4_3["cat_code"]=""
table_4_3["description_cpcat"]=""
table_4_3["cpcat_code"]=""
table_4_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_3.to_csv("dcps_46_table_4_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.4
table_4_4=read_pdf("document_1373648.pdf", pages="34", lattice=True, pandas_options={'header': None})
table_4_4["raw_chem_name"]=table_4_4.iloc[1:,0]
table_4_4["raw_cas"]=table_4_4.iloc[1:,1]
table_4_4=table_4_4.dropna(subset=["raw_chem_name"])
table_4_4=table_4_4.reset_index()
table_4_4=table_4_4[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_4)):
    table_4_4["raw_chem_name"].iloc[j]=str(table_4_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_4_4["raw_chem_name"].iloc[j]=clean(str(table_4_4["raw_chem_name"].iloc[j]))
    if len(table_4_4["raw_chem_name"].iloc[j].split())>1:
        table_4_4["raw_chem_name"].iloc[j]=" ".join(table_4_4["raw_chem_name"].iloc[j].split())
    if len(str(table_4_4["raw_cas"].iloc[j]).split())>1:
        table_4_4["raw_cas"].iloc[j]="".join(str(table_4_4["raw_cas"].iloc[j]).split())
    if str(table_4_4["raw_cas"].iloc[j])=="nan" and table_4_4["raw_chem_name"].iloc[j]!="c 10-16":
        table_4_4["raw_chem_name"].iloc[j]=table_4_4["raw_chem_name"].iloc[j-1]+" "+table_4_4["raw_chem_name"].iloc[j]
        table_4_4["raw_cas"].iloc[j]=table_4_4["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_4_4=table_4_4.drop(j_drop)
table_4_4=table_4_4.reset_index()
table_4_4=table_4_4[["raw_chem_name","raw_cas"]]

table_4_4["data_document_id"]="1373648"
table_4_4["data_document_filename"]="DCPS_46_p.pdf"
table_4_4["doc_date"]="2004"
table_4_4["raw_category"]=""
table_4_4["cat_code"]=""
table_4_4["description_cpcat"]=""
table_4_4["cpcat_code"]=""
table_4_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_4.to_csv("dcps_46_table_4_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.5
table_4_5=read_pdf("document_1373649.pdf", pages="36", lattice=True, pandas_options={'header': None})
table_4_5["raw_chem_name"]=table_4_5.iloc[1:,0]
table_4_5["raw_cas"]=table_4_5.iloc[1:,1]
table_4_5=table_4_5.dropna(subset=["raw_chem_name"])
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_5)):
    table_4_5["raw_chem_name"].iloc[j]=str(table_4_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta").replace("*","")
    table_4_5["raw_chem_name"].iloc[j]=clean(str(table_4_5["raw_chem_name"].iloc[j]))
    if len(table_4_5["raw_chem_name"].iloc[j].split())>1:
        table_4_5["raw_chem_name"].iloc[j]=" ".join(table_4_5["raw_chem_name"].iloc[j].split())
    if len(str(table_4_5["raw_cas"].iloc[j]).split())>1:
        table_4_5["raw_cas"].iloc[j]="".join(str(table_4_5["raw_cas"].iloc[j]).split())
    if str(table_4_5["raw_cas"].iloc[j])=="nan":
        table_4_5["raw_chem_name"].iloc[j]=table_4_5["raw_chem_name"].iloc[j-1]+" "+table_4_5["raw_chem_name"].iloc[j]
        table_4_5["raw_cas"].iloc[j]=table_4_5["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

table_4_5=table_4_5.drop(j_drop)
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name","raw_cas"]]

table_4_5["data_document_id"]="1373649"
table_4_5["data_document_filename"]="DCPS_46_q.pdf"
table_4_5["doc_date"]="2004"
table_4_5["raw_category"]=""
table_4_5["cat_code"]=""
table_4_5["description_cpcat"]=""
table_4_5["cpcat_code"]=""
table_4_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_5.to_csv("dcps_46_table_4_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
