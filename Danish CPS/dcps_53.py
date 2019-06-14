#lkoval
#6-11-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.1.1
tables=read_pdf("document_1372570.pdf", pages="17", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_1=tables[0]
table_3_1_1["raw_chem_name"]=table_3_1_1.iloc[1:,0]
table_3_1_1["raw_cas"]=table_3_1_1.iloc[1:,1]
table_3_1_1=table_3_1_1.dropna(subset=["raw_chem_name"])
table_3_1_1=table_3_1_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_1)):
    table_3_1_1["raw_chem_name"].iloc[j]=str(table_3_1_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3_1_1["raw_chem_name"].iloc[j]=clean(str(table_3_1_1["raw_chem_name"].iloc[j]))
    if len(table_3_1_1["raw_chem_name"].iloc[j].split())>1:
        table_3_1_1["raw_chem_name"].iloc[j]="".join(table_3_1_1["raw_chem_name"].iloc[j].split())

table_3_1_1["data_document_id"]="1372570"
table_3_1_1["data_document_filename"]="DCPS_53_a.pdf"
table_3_1_1["doc_date"]="2005"
table_3_1_1["raw_category"]=""
table_3_1_1["cat_code"]=""
table_3_1_1["description_cpcat"]=""
table_3_1_1["cpcat_code"]=""
table_3_1_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_1.to_csv("dcps_53_table_3_1_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.2
table_3_1_2=read_pdf("document_1372571.pdf", pages="18", lattice=True, pandas_options={'header': None})
table_3_1_2["raw_chem_name"]=table_3_1_2.iloc[:,0]
table_3_1_2["raw_cas"]=table_3_1_2.iloc[:,1]
table_3_1_2=table_3_1_2.loc[table_3_1_2["raw_cas"]!="CAS NO."]
table_3_1_2=table_3_1_2.dropna(subset=["raw_chem_name"])
table_3_1_2=table_3_1_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_2)):
    table_3_1_2["raw_chem_name"].iloc[j]=str(table_3_1_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_2["raw_chem_name"].iloc[j]=clean(str(table_3_1_2["raw_chem_name"].iloc[j]))
    if len(table_3_1_2["raw_chem_name"].iloc[j].split())>1:
        table_3_1_2["raw_chem_name"].iloc[j]=" ".join(table_3_1_2["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_2["raw_cas"].iloc[j]).split())>1:
        table_3_1_2["raw_cas"].iloc[j]="".join(str(table_3_1_2["raw_cas"].iloc[j]).split())

table_3_1_2=table_3_1_2.drop_duplicates()
table_3_1_2=table_3_1_2.reset_index()
table_3_1_2=table_3_1_2[["raw_chem_name","raw_cas"]]

table_3_1_2["data_document_id"]="1372571"
table_3_1_2["data_document_filename"]="DCPS_53_b.pdf"
table_3_1_2["doc_date"]="2005"
table_3_1_2["raw_category"]=""
table_3_1_2["cat_code"]=""
table_3_1_2["description_cpcat"]=""
table_3_1_2["cpcat_code"]=""
table_3_1_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_2.to_csv("dcps_53_table_3_1_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.3
tables=read_pdf("document_1372572.pdf", pages="19", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_3=pd.concat([tables[0],tables[1]], ignore_index=True)
table_3_1_3["raw_chem_name"]=table_3_1_3.iloc[:,0]
table_3_1_3["raw_cas"]=table_3_1_3.iloc[:,1]
table_3_1_3=table_3_1_3.loc[table_3_1_3["raw_cas"]!="CAS NO."]
table_3_1_3=table_3_1_3.dropna(subset=["raw_chem_name"])
table_3_1_3=table_3_1_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_3)):
    table_3_1_3["raw_chem_name"].iloc[j]=str(table_3_1_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_3["raw_chem_name"].iloc[j]=clean(str(table_3_1_3["raw_chem_name"].iloc[j]))
    if len(table_3_1_3["raw_chem_name"].iloc[j].split())>1:
        table_3_1_3["raw_chem_name"].iloc[j]=" ".join(table_3_1_3["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_3["raw_cas"].iloc[j]).split())>1:
        table_3_1_3["raw_cas"].iloc[j]="".join(str(table_3_1_3["raw_cas"].iloc[j]).split())

table_3_1_3=table_3_1_3.drop_duplicates()
table_3_1_3=table_3_1_3.reset_index()
table_3_1_3=table_3_1_3[["raw_chem_name","raw_cas"]]

table_3_1_3["data_document_id"]="1372572"
table_3_1_3["data_document_filename"]="DCPS_53_c.pdf"
table_3_1_3["doc_date"]="2005"
table_3_1_3["raw_category"]=""
table_3_1_3["cat_code"]=""
table_3_1_3["description_cpcat"]=""
table_3_1_3["cpcat_code"]=""
table_3_1_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_3.to_csv("dcps_53_table_3_1_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.4
tables=read_pdf("document_1372573.pdf", pages="19,20", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_4=pd.concat([tables[2],tables[3],tables[4]], ignore_index=True)
table_3_1_4["raw_chem_name"]=table_3_1_4.iloc[:,0]
table_3_1_4["raw_cas"]=table_3_1_4.iloc[:,1]
table_3_1_4=table_3_1_4.loc[table_3_1_4["raw_cas"]!="CAS NO."]
table_3_1_4=table_3_1_4.dropna(subset=["raw_chem_name"])
table_3_1_4=table_3_1_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_4)):
    table_3_1_4["raw_chem_name"].iloc[j]=str(table_3_1_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_4["raw_chem_name"].iloc[j]=clean(str(table_3_1_4["raw_chem_name"].iloc[j]))
    if len(table_3_1_4["raw_chem_name"].iloc[j].split())>1:
        table_3_1_4["raw_chem_name"].iloc[j]=" ".join(table_3_1_4["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_4["raw_cas"].iloc[j]).split())>1:
        table_3_1_4["raw_cas"].iloc[j]="".join(str(table_3_1_4["raw_cas"].iloc[j]).split())
    if table_3_1_4["raw_chem_name"].iloc[j][-1]=="4":
        table_3_1_4["raw_chem_name"].iloc[j]=table_3_1_4["raw_chem_name"].iloc[j][:-1]

table_3_1_4=table_3_1_4.drop_duplicates()
table_3_1_4=table_3_1_4.reset_index()
table_3_1_4=table_3_1_4[["raw_chem_name","raw_cas"]]

table_3_1_4["data_document_id"]="1372573"
table_3_1_4["data_document_filename"]="DCPS_53_d.pdf"
table_3_1_4["doc_date"]="2005"
table_3_1_4["raw_category"]=""
table_3_1_4["cat_code"]=""
table_3_1_4["description_cpcat"]=""
table_3_1_4["cpcat_code"]=""
table_3_1_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_4.to_csv("dcps_53_table_3_1_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.5
tables=read_pdf("document_1372574.pdf", pages="20", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_5=tables[2]
table_3_1_5["raw_chem_name"]=table_3_1_5.iloc[:,0]
table_3_1_5["raw_cas"]=table_3_1_5.iloc[:,1]
table_3_1_5=table_3_1_5.loc[table_3_1_5["raw_cas"]!="CAS NO."]
table_3_1_5=table_3_1_5.dropna(subset=["raw_chem_name"])
table_3_1_5=table_3_1_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_5)):
    table_3_1_5["raw_chem_name"].iloc[j]=str(table_3_1_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_5["raw_chem_name"].iloc[j]=clean(str(table_3_1_5["raw_chem_name"].iloc[j]))
    if len(table_3_1_5["raw_chem_name"].iloc[j].split())>1:
        table_3_1_5["raw_chem_name"].iloc[j]=" ".join(table_3_1_5["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_5["raw_cas"].iloc[j]).split())>1:
        table_3_1_5["raw_cas"].iloc[j]="".join(str(table_3_1_5["raw_cas"].iloc[j]).split())

table_3_1_5=table_3_1_5.drop_duplicates()
table_3_1_5=table_3_1_5.reset_index()
table_3_1_5=table_3_1_5[["raw_chem_name","raw_cas"]]

table_3_1_5["data_document_id"]="1372574"
table_3_1_5["data_document_filename"]="DCPS_53_e.pdf"
table_3_1_5["doc_date"]="2005"
table_3_1_5["raw_category"]=""
table_3_1_5["cat_code"]=""
table_3_1_5["description_cpcat"]=""
table_3_1_5["cpcat_code"]=""
table_3_1_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_5.to_csv("dcps_53_table_3_1_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.6
tables=read_pdf("document_1372575.pdf", pages="20,21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_6=pd.concat([tables[3],tables[4],tables[5]], ignore_index=True)
table_3_1_6["raw_chem_name"]=table_3_1_6.iloc[:,0]
table_3_1_6["raw_cas"]=table_3_1_6.iloc[:,1]
table_3_1_6=table_3_1_6.loc[table_3_1_6["raw_cas"]!="CAS NO."]
table_3_1_6=table_3_1_6.dropna(subset=["raw_chem_name"])
table_3_1_6=table_3_1_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_6)):
    table_3_1_6["raw_chem_name"].iloc[j]=str(table_3_1_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("(v)","").replace("(t)","").replace("(t and v)","")
    table_3_1_6["raw_chem_name"].iloc[j]=clean(str(table_3_1_6["raw_chem_name"].iloc[j]))
    if len(table_3_1_6["raw_chem_name"].iloc[j].split())>1:
        table_3_1_6["raw_chem_name"].iloc[j]=" ".join(table_3_1_6["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_6["raw_cas"].iloc[j]).split())>1:
        table_3_1_6["raw_cas"].iloc[j]="".join(str(table_3_1_6["raw_cas"].iloc[j]).split())

table_3_1_6=table_3_1_6.drop_duplicates()
table_3_1_6=table_3_1_6.reset_index()
table_3_1_6=table_3_1_6[["raw_chem_name","raw_cas"]]

table_3_1_6["data_document_id"]="1372575"
table_3_1_6["data_document_filename"]="DCPS_53_f.pdf"
table_3_1_6["doc_date"]="2005"
table_3_1_6["raw_category"]=""
table_3_1_6["cat_code"]=""
table_3_1_6["description_cpcat"]=""
table_3_1_6["cpcat_code"]=""
table_3_1_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_6.to_csv("dcps_53_table_3_1_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.7
tables=read_pdf("document_1372576.pdf", pages="21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_7=pd.concat([tables[1],tables[2]], ignore_index=True)
table_3_1_7["raw_chem_name"]=table_3_1_7.iloc[:,0]
table_3_1_7["raw_cas"]=table_3_1_7.iloc[:,1]
table_3_1_7=table_3_1_7.loc[table_3_1_7["raw_cas"]!="CAS NO."]
table_3_1_7=table_3_1_7.dropna(subset=["raw_chem_name"])
table_3_1_7=table_3_1_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_7)):
    table_3_1_7["raw_chem_name"].iloc[j]=str(table_3_1_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_7["raw_chem_name"].iloc[j]=clean(str(table_3_1_7["raw_chem_name"].iloc[j]))
    if len(table_3_1_7["raw_chem_name"].iloc[j].split())>1:
        table_3_1_7["raw_chem_name"].iloc[j]=" ".join(table_3_1_7["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_7["raw_cas"].iloc[j]).split())>1:
        table_3_1_7["raw_cas"].iloc[j]="".join(str(table_3_1_7["raw_cas"].iloc[j]).split())

table_3_1_7=table_3_1_7.drop_duplicates()
table_3_1_7=table_3_1_7.reset_index()
table_3_1_7=table_3_1_7[["raw_chem_name","raw_cas"]]

table_3_1_7["data_document_id"]="1372576"
table_3_1_7["data_document_filename"]="DCPS_53_g.pdf"
table_3_1_7["doc_date"]="2005"
table_3_1_7["raw_category"]=""
table_3_1_7["cat_code"]=""
table_3_1_7["description_cpcat"]=""
table_3_1_7["cpcat_code"]=""
table_3_1_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_7.to_csv("dcps_53_table_3_1_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.8
tables=read_pdf("document_1372577.pdf", pages="21,22", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_8=pd.concat([tables[3],tables[4],tables[5]], ignore_index=True)
table_3_1_8["raw_chem_name"]=table_3_1_8.iloc[:,0]
table_3_1_8["raw_cas"]=table_3_1_8.iloc[:,1]
table_3_1_8=table_3_1_8.loc[table_3_1_8["raw_cas"]!="CAS NO."]
table_3_1_8=table_3_1_8.dropna(subset=["raw_chem_name"])
table_3_1_8=table_3_1_8[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_8)):
    table_3_1_8["raw_chem_name"].iloc[j]=str(table_3_1_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("(am)","")
    table_3_1_8["raw_chem_name"].iloc[j]=clean(str(table_3_1_8["raw_chem_name"].iloc[j]))
    if len(table_3_1_8["raw_chem_name"].iloc[j].split())>1:
        table_3_1_8["raw_chem_name"].iloc[j]=" ".join(table_3_1_8["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_8["raw_cas"].iloc[j]).split())>1:
        table_3_1_8["raw_cas"].iloc[j]="".join(str(table_3_1_8["raw_cas"].iloc[j]).split())

table_3_1_8=table_3_1_8.drop_duplicates()
table_3_1_8=table_3_1_8.reset_index()
table_3_1_8=table_3_1_8[["raw_chem_name","raw_cas"]]

table_3_1_8["data_document_id"]="1372577"
table_3_1_8["data_document_filename"]="DCPS_53_h.pdf"
table_3_1_8["doc_date"]="2005"
table_3_1_8["raw_category"]=""
table_3_1_8["cat_code"]=""
table_3_1_8["description_cpcat"]=""
table_3_1_8["cpcat_code"]=""
table_3_1_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_8.to_csv("dcps_53_table_3_1_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.9
tables=read_pdf("document_1372578.pdf", pages="22", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_9=pd.concat([tables[2],tables[3]], ignore_index=True)
table_3_1_9["raw_chem_name"]=table_3_1_9.iloc[:,0]
table_3_1_9["raw_cas"]=table_3_1_9.iloc[:,1]
table_3_1_9=table_3_1_9.loc[table_3_1_9["raw_cas"]!="CAS NO."]
table_3_1_9=table_3_1_9.dropna(subset=["raw_chem_name"])
table_3_1_9=table_3_1_9[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_9)):
    table_3_1_9["raw_chem_name"].iloc[j]=str(table_3_1_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_9["raw_chem_name"].iloc[j]=clean(str(table_3_1_9["raw_chem_name"].iloc[j]))
    if len(table_3_1_9["raw_chem_name"].iloc[j].split())>1:
        table_3_1_9["raw_chem_name"].iloc[j]=" ".join(table_3_1_9["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_9["raw_cas"].iloc[j]).split())>1:
        table_3_1_9["raw_cas"].iloc[j]="".join(str(table_3_1_9["raw_cas"].iloc[j]).split())

table_3_1_9=table_3_1_9.drop_duplicates()
table_3_1_9=table_3_1_9.reset_index()
table_3_1_9=table_3_1_9[["raw_chem_name","raw_cas"]]

table_3_1_9["data_document_id"]="1372578"
table_3_1_9["data_document_filename"]="DCPS_53_i.pdf"
table_3_1_9["doc_date"]="2005"
table_3_1_9["raw_category"]=""
table_3_1_9["cat_code"]=""
table_3_1_9["description_cpcat"]=""
table_3_1_9["cpcat_code"]=""
table_3_1_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_9.to_csv("dcps_53_table_3_1_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.1.10
tables=read_pdf("document_1372579.pdf", pages="23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_10=tables[0]
table_3_1_10["raw_chem_name"]=table_3_1_10.iloc[:,0]
table_3_1_10["raw_cas"]=table_3_1_10.iloc[:,1]
table_3_1_10=table_3_1_10.loc[table_3_1_10["raw_cas"]!="CAS NO."]
table_3_1_10=table_3_1_10.dropna(subset=["raw_chem_name"])
table_3_1_10=table_3_1_10[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_10)):
    table_3_1_10["raw_chem_name"].iloc[j]=str(table_3_1_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("(sc)","").replace("(s)","").replace("(a)","")
    table_3_1_10["raw_chem_name"].iloc[j]=clean(str(table_3_1_10["raw_chem_name"].iloc[j]))
    if len(table_3_1_10["raw_chem_name"].iloc[j].split())>1:
        table_3_1_10["raw_chem_name"].iloc[j]=" ".join(table_3_1_10["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_10["raw_cas"].iloc[j]).split())>1:
        table_3_1_10["raw_cas"].iloc[j]="".join(str(table_3_1_10["raw_cas"].iloc[j]).split())

table_3_1_10=table_3_1_10.drop_duplicates()
table_3_1_10=table_3_1_10.reset_index()
table_3_1_10=table_3_1_10[["raw_chem_name","raw_cas"]]

table_3_1_10["data_document_id"]="1372579"
table_3_1_10["data_document_filename"]="DCPS_53_j.pdf"
table_3_1_10["doc_date"]="2005"
table_3_1_10["raw_category"]=""
table_3_1_10["cat_code"]=""
table_3_1_10["description_cpcat"]=""
table_3_1_10["cpcat_code"]=""
table_3_1_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_10.to_csv("dcps_53_table_3_1_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_1_11
tables=read_pdf("document_1372580.pdf", pages="23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_11=pd.concat([tables[1],tables[2]], ignore_index=True)
table_3_1_11["raw_chem_name"]=table_3_1_11.iloc[:,0]
table_3_1_11["raw_cas"]=table_3_1_11.iloc[:,1]
table_3_1_11=table_3_1_11.loc[table_3_1_11["raw_cas"]!="CAS NO."]
table_3_1_11=table_3_1_11.dropna(subset=["raw_chem_name"])
table_3_1_11=table_3_1_11[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_11)):
    table_3_1_11["raw_chem_name"].iloc[j]=str(table_3_1_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("(f)","").replace("(h)","")
    table_3_1_11["raw_chem_name"].iloc[j]=clean(str(table_3_1_11["raw_chem_name"].iloc[j]))
    if len(table_3_1_11["raw_chem_name"].iloc[j].split())>1:
        table_3_1_11["raw_chem_name"].iloc[j]=" ".join(table_3_1_11["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_11["raw_cas"].iloc[j]).split())>1:
        table_3_1_11["raw_cas"].iloc[j]="".join(str(table_3_1_11["raw_cas"].iloc[j]).split())

table_3_1_11=table_3_1_11.drop_duplicates()
table_3_1_11=table_3_1_11.reset_index()
table_3_1_11=table_3_1_11[["raw_chem_name","raw_cas"]]

table_3_1_11["data_document_id"]="1372580"
table_3_1_11["data_document_filename"]="DCPS_53_k.pdf"
table_3_1_11["doc_date"]="2005"
table_3_1_11["raw_category"]=""
table_3_1_11["cat_code"]=""
table_3_1_11["description_cpcat"]=""
table_3_1_11["cpcat_code"]=""
table_3_1_11["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_11.to_csv("dcps_53_table_3_1_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_1_12
tables=read_pdf("document_1372581.pdf", pages="24", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_12=pd.concat([tables[0],tables[1]], ignore_index=True)
table_3_1_12["raw_chem_name"]=table_3_1_12.iloc[:,0]
table_3_1_12["raw_cas"]=table_3_1_12.iloc[:,1]
table_3_1_12=table_3_1_12.loc[table_3_1_12["raw_cas"]!="CAS NO."]
table_3_1_12=table_3_1_12.dropna(subset=["raw_chem_name"])
table_3_1_12=table_3_1_12[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_12)):
    table_3_1_12["raw_chem_name"].iloc[j]=str(table_3_1_12["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_12["raw_chem_name"].iloc[j]=clean(str(table_3_1_12["raw_chem_name"].iloc[j]))
    if len(table_3_1_12["raw_chem_name"].iloc[j].split())>1:
        table_3_1_12["raw_chem_name"].iloc[j]=" ".join(table_3_1_12["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_12["raw_cas"].iloc[j]).split())>1:
        table_3_1_12["raw_cas"].iloc[j]=" ".join(str(table_3_1_12["raw_cas"].iloc[j]).split())

table_3_1_12=table_3_1_12.drop_duplicates()
table_3_1_12=table_3_1_12.reset_index()
table_3_1_12=table_3_1_12[["raw_chem_name","raw_cas"]]

table_3_1_12["data_document_id"]="1372581"
table_3_1_12["data_document_filename"]="DCPS_53_l.pdf"
table_3_1_12["doc_date"]="2005"
table_3_1_12["raw_category"]=""
table_3_1_12["cat_code"]=""
table_3_1_12["description_cpcat"]=""
table_3_1_12["cpcat_code"]=""
table_3_1_12["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_12.to_csv("dcps_53_table_3_1_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_1_13
tables=read_pdf("document_1372582.pdf", pages="24", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_13=pd.concat([tables[2],tables[3]], ignore_index=True)
table_3_1_13["raw_chem_name"]=table_3_1_13.iloc[:,0]
table_3_1_13["raw_cas"]=table_3_1_13.iloc[:,1]
table_3_1_13=table_3_1_13.loc[table_3_1_13["raw_cas"]!="CAS NO."]
table_3_1_13=table_3_1_13.dropna(subset=["raw_chem_name"])
table_3_1_13=table_3_1_13[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_13)):
    table_3_1_13["raw_chem_name"].iloc[j]=str(table_3_1_13["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_13["raw_chem_name"].iloc[j]=clean(str(table_3_1_13["raw_chem_name"].iloc[j]))
    if len(table_3_1_13["raw_chem_name"].iloc[j].split())>1:
        table_3_1_13["raw_chem_name"].iloc[j]=" ".join(table_3_1_13["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_13["raw_cas"].iloc[j]).split())>1:
        table_3_1_13["raw_cas"].iloc[j]=" ".join(str(table_3_1_13["raw_cas"].iloc[j]).split())

table_3_1_13=table_3_1_13.drop_duplicates()
table_3_1_13=table_3_1_13.reset_index()
table_3_1_13=table_3_1_13[["raw_chem_name","raw_cas"]]

table_3_1_13["data_document_id"]="1372582"
table_3_1_13["data_document_filename"]="DCPS_53_m.pdf"
table_3_1_13["doc_date"]="2005"
table_3_1_13["raw_category"]=""
table_3_1_13["cat_code"]=""
table_3_1_13["description_cpcat"]=""
table_3_1_13["cpcat_code"]=""
table_3_1_13["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_13.to_csv("dcps_53_table_3_1_13.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_1_14
tables=read_pdf("document_1372583.pdf", pages="25", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_14=pd.concat([tables[0],tables[1]], ignore_index=True)
table_3_1_14["raw_chem_name"]=table_3_1_14.iloc[:,0]
table_3_1_14["raw_cas"]=table_3_1_14.iloc[:,1]
table_3_1_14=table_3_1_14.loc[table_3_1_14["raw_cas"]!="CAS NO."]
table_3_1_14=table_3_1_14.dropna(subset=["raw_chem_name"])
table_3_1_14=table_3_1_14[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_14)):
    table_3_1_14["raw_chem_name"].iloc[j]=str(table_3_1_14["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_14["raw_chem_name"].iloc[j]=clean(str(table_3_1_14["raw_chem_name"].iloc[j]))
    if len(table_3_1_14["raw_chem_name"].iloc[j].split())>1:
        table_3_1_14["raw_chem_name"].iloc[j]=" ".join(table_3_1_14["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_14["raw_cas"].iloc[j]).split())>1:
        table_3_1_14["raw_cas"].iloc[j]=" ".join(str(table_3_1_14["raw_cas"].iloc[j]).split())

table_3_1_14=table_3_1_14.drop_duplicates()
table_3_1_14=table_3_1_14.reset_index()
table_3_1_14=table_3_1_14[["raw_chem_name","raw_cas"]]

table_3_1_14["data_document_id"]="1372583"
table_3_1_14["data_document_filename"]="DCPS_53_n.pdf"
table_3_1_14["doc_date"]="2005"
table_3_1_14["raw_category"]=""
table_3_1_14["cat_code"]=""
table_3_1_14["description_cpcat"]=""
table_3_1_14["cpcat_code"]=""
table_3_1_14["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_14.to_csv("dcps_53_table_3_1_14.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_1_15
tables=read_pdf("document_1372584.pdf", pages="25", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1_15=pd.concat([tables[2],tables[3]], ignore_index=True)
table_3_1_15["raw_chem_name"]=table_3_1_15.iloc[:,0]
table_3_1_15["raw_cas"]=table_3_1_15.iloc[:,1]
table_3_1_15=table_3_1_15.loc[table_3_1_15["raw_cas"]!="CAS NO."]
table_3_1_15=table_3_1_15.dropna(subset=["raw_chem_name"])
table_3_1_15=table_3_1_15[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1_15)):
    table_3_1_15["raw_chem_name"].iloc[j]=str(table_3_1_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_1_15["raw_chem_name"].iloc[j]=clean(str(table_3_1_15["raw_chem_name"].iloc[j]))
    if len(table_3_1_15["raw_chem_name"].iloc[j].split())>1:
        table_3_1_15["raw_chem_name"].iloc[j]=" ".join(table_3_1_15["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1_15["raw_cas"].iloc[j]).split())>1:
        table_3_1_15["raw_cas"].iloc[j]=" ".join(str(table_3_1_15["raw_cas"].iloc[j]).split())

table_3_1_15=table_3_1_15.drop_duplicates()
table_3_1_15=table_3_1_15.reset_index()
table_3_1_15=table_3_1_15[["raw_chem_name","raw_cas"]]

table_3_1_15["data_document_id"]="1372584"
table_3_1_15["data_document_filename"]="DCPS_53_o.pdf"
table_3_1_15["doc_date"]="2005"
table_3_1_15["raw_category"]=""
table_3_1_15["cat_code"]=""
table_3_1_15["description_cpcat"]=""
table_3_1_15["cpcat_code"]=""
table_3_1_15["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1_15.to_csv("dcps_53_table_3_1_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_2
table_3_2=read_pdf("document_1372585.pdf", pages="26", lattice=True, pandas_options={'header': None})
table_3_2["raw_chem_name"]=table_3_2.iloc[1:,0]
table_3_2=table_3_2.dropna(subset=["raw_chem_name"])
table_3_2=table_3_2[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(table_3_2["raw_chem_name"].iloc[j].split())>1:
        table_3_2["raw_chem_name"].iloc[j]=" ".join(table_3_2["raw_chem_name"].iloc[j].split())

table_3_2["data_document_id"]="1372585"
table_3_2["data_document_filename"]="DCPS_53_p.pdf"
table_3_2["doc_date"]="2005"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_53_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
