#lkoval
#5-21-19

from tabula import read_pdf
import pandas as pd
import string

#Table 5.3
tables=read_pdf("document_1372793.pdf", pages="39", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_3=tables[0]
table_5_3["raw_cas"]=table_5_3.iloc[:,1]
table_5_3["raw_chem_name"]=table_5_3.iloc[:,0]
table_5_3=table_5_3.loc[table_5_3["raw_chem_name"]!="Identification"]
table_5_3=table_5_3[["raw_chem_name","raw_cas"]]
table_5_3=table_5_3.dropna(how="all")
table_5_3=table_5_3.reset_index()
table_5_3=table_5_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_3)):
    table_5_3["raw_chem_name"].iloc[j]=str(table_5_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_5_3["raw_chem_name"].iloc[j]=clean(str(table_5_3["raw_chem_name"].iloc[j]))
    if len(table_5_3["raw_chem_name"].iloc[j].split())>1:
        table_5_3["raw_chem_name"].iloc[j]=" ".join(table_5_3["raw_chem_name"].iloc[j].split())
    if len(str(table_5_3["raw_cas"].iloc[j]).split())>1:
        table_5_3["raw_cas"].iloc[j]="".join(str(table_5_3["raw_cas"].iloc[j]).split())


table_5_3["data_document_id"]="1372793"
table_5_3["data_document_filename"]="DCPS_105_4.pdf"
table_5_3["doc_date"]="2010"
table_5_3["raw_category"]=""
table_5_3["cat_code"]=""
table_5_3["description_cpcat"]=""
table_5_3["cpcat_code"]=""
table_5_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_3.to_csv("dcps_105_table_5_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.4
tables=read_pdf("document_1372794.pdf", pages="39", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_4=tables[1]
table_5_4["raw_cas"]=table_5_4.iloc[:,1]
table_5_4["raw_chem_name"]=table_5_4.iloc[:,0]
table_5_4=table_5_4.loc[table_5_4["raw_chem_name"]!="Identification"]
table_5_4=table_5_4[["raw_chem_name","raw_cas"]]
table_5_4=table_5_4.dropna(how="all")
table_5_4=table_5_4.reset_index()
table_5_4=table_5_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_4)):
    table_5_4["raw_chem_name"].iloc[j]=str(table_5_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_5_4["raw_chem_name"].iloc[j]=clean(str(table_5_4["raw_chem_name"].iloc[j]))
    if len(table_5_4["raw_chem_name"].iloc[j].split())>1:
        table_5_4["raw_chem_name"].iloc[j]=" ".join(table_5_4["raw_chem_name"].iloc[j].split())
    if len(str(table_5_4["raw_cas"].iloc[j]).split())>1:
        table_5_4["raw_cas"].iloc[j]="".join(str(table_5_4["raw_cas"].iloc[j]).split())


table_5_4["data_document_id"]="1372794"
table_5_4["data_document_filename"]="DCPS_105_5.pdf"
table_5_4["doc_date"]="2010"
table_5_4["raw_category"]=""
table_5_4["cat_code"]=""
table_5_4["description_cpcat"]=""
table_5_4["cpcat_code"]=""
table_5_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_4.to_csv("dcps_105_table_5_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.5
tables=read_pdf("document_1372795.pdf", pages="40", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_5=tables[0]
table_5_5["raw_cas"]=table_5_5.iloc[:,1]
table_5_5["raw_chem_name"]=table_5_5.iloc[:,0]
table_5_5=table_5_5.loc[table_5_5["raw_chem_name"]!="Identification"]
table_5_5=table_5_5[["raw_chem_name","raw_cas"]]
table_5_5=table_5_5.dropna(how="all")
table_5_5=table_5_5.reset_index()
table_5_5=table_5_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_5)):
    table_5_5["raw_chem_name"].iloc[j]=str(table_5_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_5["raw_chem_name"].iloc[j]=clean(str(table_5_5["raw_chem_name"].iloc[j]))
    if len(table_5_5["raw_chem_name"].iloc[j].split())>1:
        table_5_5["raw_chem_name"].iloc[j]=" ".join(table_5_5["raw_chem_name"].iloc[j].split())
    if len(str(table_5_5["raw_cas"].iloc[j]).split())>1:
        table_5_5["raw_cas"].iloc[j]="".join(str(table_5_5["raw_cas"].iloc[j]).split())

table_5_5["data_document_id"]="1372795"
table_5_5["data_document_filename"]="DCPS_105_6.pdf"
table_5_5["doc_date"]="2010"
table_5_5["raw_category"]=""
table_5_5["cat_code"]=""
table_5_5["description_cpcat"]=""
table_5_5["cpcat_code"]=""
table_5_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_5.to_csv("dcps_105_table_5_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.6
tables=read_pdf("document_1372796.pdf", pages="40", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_6=tables[1]
table_5_6["raw_cas"]=table_5_6.iloc[:,1]
table_5_6["raw_chem_name"]=table_5_6.iloc[:,0]
table_5_6=table_5_6.loc[table_5_6["raw_chem_name"]!="Identification"]
table_5_6=table_5_6[["raw_chem_name","raw_cas"]]
table_5_6=table_5_6.dropna(how="all")
table_5_6=table_5_6.reset_index()
table_5_6=table_5_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_6)):
    table_5_6["raw_chem_name"].iloc[j]=str(table_5_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_6["raw_chem_name"].iloc[j]=clean(str(table_5_6["raw_chem_name"].iloc[j]))
    if len(table_5_6["raw_chem_name"].iloc[j].split())>1:
        table_5_6["raw_chem_name"].iloc[j]=" ".join(table_5_6["raw_chem_name"].iloc[j].split())
    if len(str(table_5_6["raw_cas"].iloc[j]).split())>1:
        table_5_6["raw_cas"].iloc[j]="".join(str(table_5_6["raw_cas"].iloc[j]).split())

table_5_6["data_document_id"]="1372796"
table_5_6["data_document_filename"]="DCPS_105_7.pdf"
table_5_6["doc_date"]="2010"
table_5_6["raw_category"]=""
table_5_6["cat_code"]=""
table_5_6["description_cpcat"]=""
table_5_6["cpcat_code"]=""
table_5_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_6.to_csv("dcps_105_table_5_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.7
tables=read_pdf("document_1372797.pdf", pages="40", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_7=tables[2]
table_5_7["raw_cas"]=table_5_7.iloc[:,1]
table_5_7["raw_chem_name"]=table_5_7.iloc[:,0]
table_5_7=table_5_7.loc[table_5_7["raw_chem_name"]!="Identification"]
table_5_7=table_5_7[["raw_chem_name","raw_cas"]]
table_5_7=table_5_7.dropna(how="all")
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_7)):
    table_5_7["raw_chem_name"].iloc[j]=str(table_5_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_7["raw_chem_name"].iloc[j]=clean(str(table_5_7["raw_chem_name"].iloc[j]))
    if len(table_5_7["raw_chem_name"].iloc[j].split())>1:
        table_5_7["raw_chem_name"].iloc[j]=" ".join(table_5_7["raw_chem_name"].iloc[j].split())
    if len(str(table_5_7["raw_cas"].iloc[j]).split())>1:
        table_5_7["raw_cas"].iloc[j]="".join(str(table_5_7["raw_cas"].iloc[j]).split())

table_5_7["data_document_id"]="1372797"
table_5_7["data_document_filename"]="DCPS_105_8.pdf"
table_5_7["doc_date"]="2010"
table_5_7["raw_category"]=""
table_5_7["cat_code"]=""
table_5_7["description_cpcat"]=""
table_5_7["cpcat_code"]=""
table_5_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_7.to_csv("dcps_105_table_5_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.8
tables=read_pdf("document_1372798.pdf", pages="41", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_8=tables[0]
table_5_8["raw_cas"]=table_5_8.iloc[:,1]
table_5_8["raw_chem_name"]=table_5_8.iloc[:,0]
table_5_8=table_5_8.loc[table_5_8["raw_chem_name"]!="Identification"]
table_5_8=table_5_8[["raw_chem_name","raw_cas"]]
table_5_8=table_5_8.dropna(how="all")
table_5_8=table_5_8.reset_index()
table_5_8=table_5_8[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_8)):
    table_5_8["raw_chem_name"].iloc[j]=str(table_5_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_8["raw_chem_name"].iloc[j]=clean(str(table_5_8["raw_chem_name"].iloc[j]))
    if len(table_5_8["raw_chem_name"].iloc[j].split())>1:
        table_5_8["raw_chem_name"].iloc[j]=" ".join(table_5_8["raw_chem_name"].iloc[j].split())
    if len(str(table_5_8["raw_cas"].iloc[j]).split())>1:
        table_5_8["raw_cas"].iloc[j]="".join(str(table_5_8["raw_cas"].iloc[j]).split())

table_5_8["data_document_id"]="1372798"
table_5_8["data_document_filename"]="DCPS_105_9.pdf"
table_5_8["doc_date"]="2010"
table_5_8["raw_category"]=""
table_5_8["cat_code"]=""
table_5_8["description_cpcat"]=""
table_5_8["cpcat_code"]=""
table_5_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_8.to_csv("dcps_105_table_5_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.9
tables=read_pdf("document_1372799.pdf", pages="41", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_9=tables[1]
table_5_9["raw_cas"]=table_5_9.iloc[:,1]
table_5_9["raw_chem_name"]=table_5_9.iloc[:,0]
table_5_9=table_5_9.loc[table_5_9["raw_chem_name"]!="Identification"]
table_5_9=table_5_9[["raw_chem_name","raw_cas"]]
table_5_9=table_5_9.dropna(how="all")
table_5_9=table_5_9.reset_index()
table_5_9=table_5_9[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_9)):
    table_5_9["raw_chem_name"].iloc[j]=str(table_5_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_9["raw_chem_name"].iloc[j]=clean(str(table_5_9["raw_chem_name"].iloc[j]))
    if len(table_5_9["raw_chem_name"].iloc[j].split())>1:
        table_5_9["raw_chem_name"].iloc[j]=" ".join(table_5_9["raw_chem_name"].iloc[j].split())
    if len(str(table_5_9["raw_cas"].iloc[j]).split())>1:
        table_5_9["raw_cas"].iloc[j]="".join(str(table_5_9["raw_cas"].iloc[j]).split())

table_5_9["data_document_id"]="1372799"
table_5_9["data_document_filename"]="DCPS_105_10.pdf"
table_5_9["doc_date"]="2010"
table_5_9["raw_category"]=""
table_5_9["cat_code"]=""
table_5_9["description_cpcat"]=""
table_5_9["cpcat_code"]=""
table_5_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_9.to_csv("dcps_105_table_5_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.10
tables=read_pdf("document_1372800.pdf", pages="41", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_10=tables[2]
table_5_10["raw_cas"]=table_5_10.iloc[:,1]
table_5_10["raw_chem_name"]=table_5_10.iloc[:,0]
table_5_10=table_5_10.loc[table_5_10["raw_chem_name"]!="Identification"]
table_5_10=table_5_10[["raw_chem_name","raw_cas"]]
table_5_10=table_5_10.dropna(how="all")
table_5_10=table_5_10.reset_index()
table_5_10=table_5_10[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_10)):
    table_5_10["raw_chem_name"].iloc[j]=str(table_5_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_10["raw_chem_name"].iloc[j]=clean(str(table_5_10["raw_chem_name"].iloc[j]))
    if len(table_5_10["raw_chem_name"].iloc[j].split())>1:
        table_5_10["raw_chem_name"].iloc[j]=" ".join(table_5_10["raw_chem_name"].iloc[j].split())
    if len(str(table_5_10["raw_cas"].iloc[j]).split())>1:
        table_5_10["raw_cas"].iloc[j]="".join(str(table_5_10["raw_cas"].iloc[j]).split())

table_5_10["data_document_id"]="1372800"
table_5_10["data_document_filename"]="DCPS_105_11.pdf"
table_5_10["doc_date"]="2010"
table_5_10["raw_category"]=""
table_5_10["cat_code"]=""
table_5_10["description_cpcat"]=""
table_5_10["cpcat_code"]=""
table_5_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_10.to_csv("dcps_105_table_5_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.11
tables=read_pdf("document_1372801.pdf", pages="41", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_11=tables[3]
table_5_11["raw_cas"]=table_5_11.iloc[:,1]
table_5_11["raw_chem_name"]=table_5_11.iloc[:,0]
table_5_11=table_5_11.loc[table_5_11["raw_chem_name"]!="Identification"]
table_5_11=table_5_11[["raw_chem_name","raw_cas"]]
table_5_11=table_5_11.dropna(how="all")
table_5_11=table_5_11.reset_index()
table_5_11=table_5_11[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_11)):
    table_5_11["raw_chem_name"].iloc[j]=str(table_5_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_11["raw_chem_name"].iloc[j]=clean(str(table_5_11["raw_chem_name"].iloc[j]))
    if len(table_5_11["raw_chem_name"].iloc[j].split())>1:
        table_5_11["raw_chem_name"].iloc[j]=" ".join(table_5_11["raw_chem_name"].iloc[j].split())
    if len(str(table_5_11["raw_cas"].iloc[j]).split())>1:
        table_5_11["raw_cas"].iloc[j]="".join(str(table_5_11["raw_cas"].iloc[j]).split())

table_5_11["data_document_id"]="1372801"
table_5_11["data_document_filename"]="DCPS_105_12.pdf"
table_5_11["doc_date"]="2010"
table_5_11["raw_category"]=""
table_5_11["cat_code"]=""
table_5_11["description_cpcat"]=""
table_5_11["cpcat_code"]=""
table_5_11["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_11.to_csv("dcps_105_table_5_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.14
tables=read_pdf("document_1372803.pdf", pages="42", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_14=tables[2]
table_5_14["raw_cas"]=table_5_14.iloc[:,1]
table_5_14["raw_chem_name"]=table_5_14.iloc[:,0]
table_5_14=table_5_14.loc[table_5_14["raw_chem_name"]!="Identification"]
table_5_14=table_5_14[["raw_chem_name","raw_cas"]]
table_5_14=table_5_14.dropna(how="all")
table_5_14=table_5_14.reset_index()
table_5_14=table_5_14[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_14)):
    table_5_14["raw_chem_name"].iloc[j]=str(table_5_14["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_14["raw_chem_name"].iloc[j]=clean(str(table_5_14["raw_chem_name"].iloc[j]))
    if len(table_5_14["raw_chem_name"].iloc[j].split())>1:
        table_5_14["raw_chem_name"].iloc[j]=" ".join(table_5_14["raw_chem_name"].iloc[j].split())
    if len(str(table_5_14["raw_cas"].iloc[j]).split())>1:
        table_5_14["raw_cas"].iloc[j]="".join(str(table_5_14["raw_cas"].iloc[j]).split())

table_5_14["data_document_id"]="1372803"
table_5_14["data_document_filename"]="DCPS_105_14.pdf"
table_5_14["doc_date"]="2010"
table_5_14["raw_category"]=""
table_5_14["cat_code"]=""
table_5_14["description_cpcat"]=""
table_5_14["cpcat_code"]=""
table_5_14["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_14.to_csv("dcps_105_table_5_14.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.15
tables=read_pdf("document_1372804.pdf", pages="43", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_15=tables[0]
table_5_15["raw_cas"]=table_5_15.iloc[:,1]
table_5_15["raw_chem_name"]=table_5_15.iloc[:,0]
table_5_15=table_5_15.loc[table_5_15["raw_chem_name"]!="Identification"]
table_5_15=table_5_15[["raw_chem_name","raw_cas"]]
table_5_15=table_5_15.dropna(how="all")
table_5_15=table_5_15.reset_index()
table_5_15=table_5_15[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_15)):
    table_5_15["raw_chem_name"].iloc[j]=str(table_5_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_15["raw_chem_name"].iloc[j]=clean(str(table_5_15["raw_chem_name"].iloc[j]))
    if len(table_5_15["raw_chem_name"].iloc[j].split())>1:
        table_5_15["raw_chem_name"].iloc[j]=" ".join(table_5_15["raw_chem_name"].iloc[j].split())
    if len(str(table_5_15["raw_cas"].iloc[j]).split())>1:
        table_5_15["raw_cas"].iloc[j]="".join(str(table_5_15["raw_cas"].iloc[j]).split())

table_5_15["data_document_id"]="1372804"
table_5_15["data_document_filename"]="DCPS_105_15.pdf"
table_5_15["doc_date"]="2010"
table_5_15["raw_category"]=""
table_5_15["cat_code"]=""
table_5_15["description_cpcat"]=""
table_5_15["cpcat_code"]=""
table_5_15["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_15.to_csv("dcps_105_table_5_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.16
tables=read_pdf("document_1372805.pdf", pages="43", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_16=tables[1]
table_5_16["raw_cas"]=table_5_16.iloc[:,1]
table_5_16["raw_chem_name"]=table_5_16.iloc[:,0]
table_5_16=table_5_16.loc[table_5_16["raw_chem_name"]!="Identification"]
table_5_16=table_5_16[["raw_chem_name","raw_cas"]]
table_5_16=table_5_16.dropna(how="all")
table_5_16=table_5_16.reset_index()
table_5_16=table_5_16[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_16)):
    table_5_16["raw_chem_name"].iloc[j]=str(table_5_16["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_16["raw_chem_name"].iloc[j]=clean(str(table_5_16["raw_chem_name"].iloc[j]))
    if len(table_5_16["raw_chem_name"].iloc[j].split())>1:
        table_5_16["raw_chem_name"].iloc[j]=" ".join(table_5_16["raw_chem_name"].iloc[j].split())
    if len(str(table_5_16["raw_cas"].iloc[j]).split())>1:
        table_5_16["raw_cas"].iloc[j]="".join(str(table_5_16["raw_cas"].iloc[j]).split())

table_5_16["data_document_id"]="1372805"
table_5_16["data_document_filename"]="DCPS_105_16.pdf"
table_5_16["doc_date"]="2010"
table_5_16["raw_category"]=""
table_5_16["cat_code"]=""
table_5_16["description_cpcat"]=""
table_5_16["cpcat_code"]=""
table_5_16["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_16.to_csv("dcps_105_table_5_16.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.17
tables=read_pdf("document_1372806.pdf", pages="44", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_17=tables[0]
table_5_17["raw_cas"]=table_5_17.iloc[:,1]
table_5_17["raw_chem_name"]=table_5_17.iloc[:,0]
table_5_17=table_5_17.loc[table_5_17["raw_chem_name"]!="Identification"]
table_5_17=table_5_17[["raw_chem_name","raw_cas"]]
table_5_17=table_5_17.dropna(how="all")
table_5_17=table_5_17.reset_index()
table_5_17=table_5_17[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_17)):
    table_5_17["raw_chem_name"].iloc[j]=str(table_5_17["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_17["raw_chem_name"].iloc[j]=clean(str(table_5_17["raw_chem_name"].iloc[j]))
    if len(table_5_17["raw_chem_name"].iloc[j].split())>1:
        table_5_17["raw_chem_name"].iloc[j]=" ".join(table_5_17["raw_chem_name"].iloc[j].split())
    if len(str(table_5_17["raw_cas"].iloc[j]).split())>1:
        table_5_17["raw_cas"].iloc[j]="".join(str(table_5_17["raw_cas"].iloc[j]).split())

table_5_17["data_document_id"]="1372806"
table_5_17["data_document_filename"]="DCPS_105_17.pdf"
table_5_17["doc_date"]="2010"
table_5_17["raw_category"]=""
table_5_17["cat_code"]=""
table_5_17["description_cpcat"]=""
table_5_17["cpcat_code"]=""
table_5_17["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_17.to_csv("dcps_105_table_5_17.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.18
tables=read_pdf("document_1372807.pdf", pages="44", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_18=tables[1]
table_5_18["raw_cas"]=table_5_18.iloc[:,2]
table_5_18["raw_chem_name"]=table_5_18.iloc[:,0]
table_5_18=table_5_18.loc[table_5_18["raw_chem_name"]!="Identification"]
table_5_18=table_5_18[["raw_chem_name","raw_cas"]]
table_5_18=table_5_18.dropna(how="all")
table_5_18=table_5_18.reset_index()
table_5_18=table_5_18[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_18)):
    table_5_18["raw_chem_name"].iloc[j]=str(table_5_18["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_18["raw_chem_name"].iloc[j]=clean(str(table_5_18["raw_chem_name"].iloc[j]))
    if len(table_5_18["raw_chem_name"].iloc[j].split())>1:
        table_5_18["raw_chem_name"].iloc[j]=" ".join(table_5_18["raw_chem_name"].iloc[j].split())
    if len(str(table_5_18["raw_cas"].iloc[j]).split())>1:
        table_5_18["raw_cas"].iloc[j]="".join(str(table_5_18["raw_cas"].iloc[j]).split())

table_5_18["data_document_id"]="1372807"
table_5_18["data_document_filename"]="DCPS_105_18.pdf"
table_5_18["doc_date"]="2010"
table_5_18["raw_category"]=""
table_5_18["cat_code"]=""
table_5_18["description_cpcat"]=""
table_5_18["cpcat_code"]=""
table_5_18["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_18.to_csv("dcps_105_table_5_18.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.19
tables=read_pdf("document_1372808.pdf", pages="44,45", lattice=True, multiple_tables=True, pandas_options={'header': None})
t44=tables[2]
t45=tables[3]
t44["raw_cas"]=t44.iloc[:,1]
t44["raw_chem_name"]=t44.iloc[:,0]
t44=t44.loc[t44["raw_chem_name"]!="Identification"]
t44=t44[["raw_chem_name","raw_cas"]]
t44=t44.dropna(how="all")
t44=t44.reset_index()
t44=t44[["raw_chem_name","raw_cas"]]
t45["raw_cas"]=t45.iloc[:,2]
t45["raw_chem_name"]=t45.iloc[:,0]
t45=t45.loc[t45["raw_chem_name"]!="Identification"]
t45=t45[["raw_chem_name","raw_cas"]]
t45=t45.dropna(how="all")
t45=t45.reset_index()
t45=t45[["raw_chem_name","raw_cas"]]
table_5_19=pd.concat([t44,t45],ignore_index=True)
table_5_19=table_5_19.dropna(subset=["raw_chem_name"])

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_19)):
    table_5_19["raw_chem_name"].iloc[j]=str(table_5_19["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_19["raw_chem_name"].iloc[j]=clean(str(table_5_19["raw_chem_name"].iloc[j]))
    if len(table_5_19["raw_chem_name"].iloc[j].split())>1:
        table_5_19["raw_chem_name"].iloc[j]=" ".join(table_5_19["raw_chem_name"].iloc[j].split())
    if len(str(table_5_19["raw_cas"].iloc[j]).split())>1:
        table_5_19["raw_cas"].iloc[j]="".join(str(table_5_19["raw_cas"].iloc[j]).split())

table_5_19["data_document_id"]="1372808"
table_5_19["data_document_filename"]="DCPS_105_19.pdf"
table_5_19["doc_date"]="2010"
table_5_19["raw_category"]=""
table_5_19["cat_code"]=""
table_5_19["description_cpcat"]=""
table_5_19["cpcat_code"]=""
table_5_19["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_19.to_csv("dcps_105_table_5_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.20
tables=read_pdf("document_1372809.pdf", pages="45", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_20=tables[1]
table_5_20["raw_cas"]=table_5_20.iloc[:,1]
table_5_20["raw_chem_name"]=table_5_20.iloc[:,0]
table_5_20=table_5_20.loc[table_5_20["raw_chem_name"]!="Identification"]
table_5_20=table_5_20[["raw_chem_name","raw_cas"]]
table_5_20=table_5_20.dropna(how="all")
table_5_20=table_5_20.reset_index()
table_5_20=table_5_20[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_20)):
    table_5_20["raw_chem_name"].iloc[j]=str(table_5_20["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_20["raw_chem_name"].iloc[j]=clean(str(table_5_20["raw_chem_name"].iloc[j]))
    if len(table_5_20["raw_chem_name"].iloc[j].split())>1:
        table_5_20["raw_chem_name"].iloc[j]=" ".join(table_5_20["raw_chem_name"].iloc[j].split())
    if len(str(table_5_20["raw_cas"].iloc[j]).split())>1:
        table_5_20["raw_cas"].iloc[j]="".join(str(table_5_20["raw_cas"].iloc[j]).split())

table_5_20["data_document_id"]="1372809"
table_5_20["data_document_filename"]="DCPS_105_20.pdf"
table_5_20["doc_date"]="2010"
table_5_20["raw_category"]=""
table_5_20["cat_code"]=""
table_5_20["description_cpcat"]=""
table_5_20["cpcat_code"]=""
table_5_20["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_20.to_csv("dcps_105_table_5_20.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.23
tables=read_pdf("document_1372812.pdf", pages="45", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_23=tables[4]
table_5_23["raw_cas"]=table_5_23.iloc[:,1]
table_5_23["raw_chem_name"]=table_5_23.iloc[:,0]
table_5_23=table_5_23.loc[table_5_23["raw_chem_name"]!="Identification"]
table_5_23=table_5_23[["raw_chem_name","raw_cas"]]
table_5_23=table_5_23.dropna(how="all")
table_5_23=table_5_23.reset_index()
table_5_23=table_5_23[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_23)):
    table_5_23["raw_chem_name"].iloc[j]=str(table_5_23["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_23["raw_chem_name"].iloc[j]=clean(str(table_5_23["raw_chem_name"].iloc[j]))
    if len(table_5_23["raw_chem_name"].iloc[j].split())>1:
        table_5_23["raw_chem_name"].iloc[j]=" ".join(table_5_23["raw_chem_name"].iloc[j].split())
    if len(str(table_5_23["raw_cas"].iloc[j]).split())>1:
        table_5_23["raw_cas"].iloc[j]="".join(str(table_5_23["raw_cas"].iloc[j]).split())

table_5_23["data_document_id"]="1372812"
table_5_23["data_document_filename"]="DCPS_105_23.pdf"
table_5_23["doc_date"]="2010"
table_5_23["raw_category"]=""
table_5_23["cat_code"]=""
table_5_23["description_cpcat"]=""
table_5_23["cpcat_code"]=""
table_5_23["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_23.to_csv("dcps_105_table_5_23.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.24
tables=read_pdf("document_1372813.pdf", pages="45,46", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_24=pd.concat([tables[5],tables[6]], ignore_index=True)
table_5_24["raw_cas"]=table_5_24.iloc[:,1]
table_5_24["raw_chem_name"]=table_5_24.iloc[:,0]
table_5_24=table_5_24.loc[table_5_24["raw_chem_name"]!="Identification"]
table_5_24=table_5_24[["raw_chem_name","raw_cas"]]
table_5_24=table_5_24.dropna(how="all")
table_5_24=table_5_24.reset_index()
table_5_24=table_5_24[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_24)):
    table_5_24["raw_chem_name"].iloc[j]=str(table_5_24["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_24["raw_chem_name"].iloc[j]=clean(str(table_5_24["raw_chem_name"].iloc[j]))
    if len(table_5_24["raw_chem_name"].iloc[j].split())>1:
        table_5_24["raw_chem_name"].iloc[j]=" ".join(table_5_24["raw_chem_name"].iloc[j].split())
    if len(str(table_5_24["raw_cas"].iloc[j]).split())>1:
        table_5_24["raw_cas"].iloc[j]="".join(str(table_5_24["raw_cas"].iloc[j]).split())

table_5_24["data_document_id"]="1372813"
table_5_24["data_document_filename"]="DCPS_105_24.pdf"
table_5_24["doc_date"]="2010"
table_5_24["raw_category"]=""
table_5_24["cat_code"]=""
table_5_24["description_cpcat"]=""
table_5_24["cpcat_code"]=""
table_5_24["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_24.to_csv("dcps_105_table_5_24.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.4
tables=read_pdf("document_1372815.pdf", pages="55", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_4=tables[1]
table_6_4["raw_cas"]=table_6_4.iloc[:,1]
table_6_4["raw_chem_name"]=table_6_4.iloc[:,0]
table_6_4=table_6_4.loc[table_6_4["raw_chem_name"]!="Identification"]
table_6_4=table_6_4[["raw_chem_name","raw_cas"]]
table_6_4=table_6_4.dropna(how="all")
table_6_4=table_6_4.reset_index()
table_6_4=table_6_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_4)):
    table_6_4["raw_chem_name"].iloc[j]=str(table_6_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_4["raw_chem_name"].iloc[j]=clean(str(table_6_4["raw_chem_name"].iloc[j]))
    if len(table_6_4["raw_chem_name"].iloc[j].split())>1:
        table_6_4["raw_chem_name"].iloc[j]=" ".join(table_6_4["raw_chem_name"].iloc[j].split())
    if len(str(table_6_4["raw_cas"].iloc[j]).split())>1:
        table_6_4["raw_cas"].iloc[j]="".join(str(table_6_4["raw_cas"].iloc[j]).split())

table_6_4["data_document_id"]="1372815"
table_6_4["data_document_filename"]="DCPS_105_26.pdf"
table_6_4["doc_date"]="2010"
table_6_4["raw_category"]=""
table_6_4["cat_code"]=""
table_6_4["description_cpcat"]=""
table_6_4["cpcat_code"]=""
table_6_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_4.to_csv("dcps_105_table_6_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.5
tables=read_pdf("document_1372816.pdf", pages="56", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_5=tables[0]
table_6_5["raw_cas"]=table_6_5.iloc[:,1]
table_6_5["raw_chem_name"]=table_6_5.iloc[:,0]
table_6_5=table_6_5.loc[table_6_5["raw_chem_name"]!="Identification"]
table_6_5=table_6_5[["raw_chem_name","raw_cas"]]
table_6_5=table_6_5.dropna(how="all")
table_6_5=table_6_5.reset_index()
table_6_5=table_6_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_5)):
    table_6_5["raw_chem_name"].iloc[j]=str(table_6_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_5["raw_chem_name"].iloc[j]=clean(str(table_6_5["raw_chem_name"].iloc[j]))
    if len(table_6_5["raw_chem_name"].iloc[j].split())>1:
        table_6_5["raw_chem_name"].iloc[j]=" ".join(table_6_5["raw_chem_name"].iloc[j].split())
    if len(str(table_6_5["raw_cas"].iloc[j]).split())>1:
        table_6_5["raw_cas"].iloc[j]="".join(str(table_6_5["raw_cas"].iloc[j]).split())

table_6_5["data_document_id"]="1372816"
table_6_5["data_document_filename"]="DCPS_105_27.pdf"
table_6_5["doc_date"]="2010"
table_6_5["raw_category"]=""
table_6_5["cat_code"]=""
table_6_5["description_cpcat"]=""
table_6_5["cpcat_code"]=""
table_6_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_5.to_csv("dcps_105_table_6_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.6
tables=read_pdf("document_1372817.pdf", pages="56", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_6=tables[1]
table_6_6["raw_cas"]=table_6_6.iloc[:,1]
table_6_6["raw_chem_name"]=table_6_6.iloc[:,0]
table_6_6=table_6_6.loc[table_6_6["raw_chem_name"]!="Identification"]
table_6_6=table_6_6[["raw_chem_name","raw_cas"]]
table_6_6=table_6_6.dropna(how="all")
table_6_6=table_6_6.reset_index()
table_6_6=table_6_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_6)):
    table_6_6["raw_chem_name"].iloc[j]=str(table_6_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_6["raw_chem_name"].iloc[j]=clean(str(table_6_6["raw_chem_name"].iloc[j]))
    if len(table_6_6["raw_chem_name"].iloc[j].split())>1:
        table_6_6["raw_chem_name"].iloc[j]=" ".join(table_6_6["raw_chem_name"].iloc[j].split())
    if len(str(table_6_6["raw_cas"].iloc[j]).split())>1:
        table_6_6["raw_cas"].iloc[j]="".join(str(table_6_6["raw_cas"].iloc[j]).split())

table_6_6["data_document_id"]="1372817"
table_6_6["data_document_filename"]="DCPS_105_28.pdf"
table_6_6["doc_date"]="2010"
table_6_6["raw_category"]=""
table_6_6["cat_code"]=""
table_6_6["description_cpcat"]=""
table_6_6["cpcat_code"]=""
table_6_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_6.to_csv("dcps_105_table_6_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.8
tables=read_pdf("document_1372819.pdf", pages="56,57", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_8=pd.concat([tables[3],tables[4]], ignore_index=True)
table_6_8["raw_cas"]=table_6_8.iloc[:,1]
table_6_8["raw_chem_name"]=table_6_8.iloc[:,0]
table_6_8=table_6_8.loc[table_6_8["raw_chem_name"]!="Identification"]
table_6_8=table_6_8[["raw_chem_name","raw_cas"]]
table_6_8=table_6_8.dropna(how="all")
table_6_8=table_6_8.reset_index()
table_6_8=table_6_8[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_8)):
    table_6_8["raw_chem_name"].iloc[j]=str(table_6_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_8["raw_chem_name"].iloc[j]=clean(str(table_6_8["raw_chem_name"].iloc[j]))
    if len(table_6_8["raw_chem_name"].iloc[j].split())>1:
        table_6_8["raw_chem_name"].iloc[j]=" ".join(table_6_8["raw_chem_name"].iloc[j].split())
    if len(str(table_6_8["raw_cas"].iloc[j]).split())>1:
        table_6_8["raw_cas"].iloc[j]="".join(str(table_6_8["raw_cas"].iloc[j]).split())

table_6_8["data_document_id"]="1372819"
table_6_8["data_document_filename"]="DCPS_105_30.pdf"
table_6_8["doc_date"]="2010"
table_6_8["raw_category"]=""
table_6_8["cat_code"]=""
table_6_8["description_cpcat"]=""
table_6_8["cpcat_code"]=""
table_6_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_8.to_csv("dcps_105_table_6_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.9
tables=read_pdf("document_1372820.pdf", pages="57", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_9=tables[1]
table_6_9["raw_cas"]=table_6_9.iloc[:,1]
table_6_9["raw_chem_name"]=table_6_9.iloc[:,0]
table_6_9=table_6_9.loc[table_6_9["raw_chem_name"]!="Identification"]
table_6_9=table_6_9[["raw_chem_name","raw_cas"]]
table_6_9=table_6_9.dropna(how="all")
table_6_9=table_6_9.reset_index()
table_6_9=table_6_9[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_9)):
    table_6_9["raw_chem_name"].iloc[j]=str(table_6_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_9["raw_chem_name"].iloc[j]=clean(str(table_6_9["raw_chem_name"].iloc[j]))
    if len(table_6_9["raw_chem_name"].iloc[j].split())>1:
        table_6_9["raw_chem_name"].iloc[j]=" ".join(table_6_9["raw_chem_name"].iloc[j].split())
    if len(str(table_6_9["raw_cas"].iloc[j]).split())>1:
        table_6_9["raw_cas"].iloc[j]="".join(str(table_6_9["raw_cas"].iloc[j]).split())

table_6_9["data_document_id"]="1372820"
table_6_9["data_document_filename"]="DCPS_105_31.pdf"
table_6_9["doc_date"]="2010"
table_6_9["raw_category"]=""
table_6_9["cat_code"]=""
table_6_9["description_cpcat"]=""
table_6_9["cpcat_code"]=""
table_6_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_9.to_csv("dcps_105_table_6_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.15
table_6_15=read_pdf("document_1372826.pdf", pages="58", lattice=True, pandas_options={'header': None})
table_6_15["raw_cas"]=table_6_15.iloc[:,1]
table_6_15["raw_chem_name"]=table_6_15.iloc[:,0]
table_6_15=table_6_15.iloc[4:]
table_6_15=table_6_15[["raw_chem_name","raw_cas"]]
table_6_15=table_6_15.dropna(how="all")
table_6_15=table_6_15.reset_index()
table_6_15=table_6_15[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_15)):
    table_6_15["raw_chem_name"].iloc[j]=str(table_6_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_15["raw_chem_name"].iloc[j]=clean(str(table_6_15["raw_chem_name"].iloc[j]))
    if len(table_6_15["raw_chem_name"].iloc[j].split())>1:
        table_6_15["raw_chem_name"].iloc[j]=" ".join(table_6_15["raw_chem_name"].iloc[j].split())
    if len(str(table_6_15["raw_cas"].iloc[j]).split())>1:
        table_6_15["raw_cas"].iloc[j]="".join(str(table_6_15["raw_cas"].iloc[j]).split())

table_6_15["data_document_id"]="1372826"
table_6_15["data_document_filename"]="DCPS_105_37.pdf"
table_6_15["doc_date"]="2010"
table_6_15["raw_category"]=""
table_6_15["cat_code"]=""
table_6_15["description_cpcat"]=""
table_6_15["cpcat_code"]=""
table_6_15["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_15.to_csv("dcps_105_table_6_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.17
tables=read_pdf("document_1372828.pdf", pages="59", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_17=tables[1]
table_6_17["raw_cas"]=table_6_17.iloc[:,1]
table_6_17["raw_chem_name"]=table_6_17.iloc[:,0]
table_6_17=table_6_17.iloc[4:]
table_6_17=table_6_17[["raw_chem_name","raw_cas"]]
table_6_17=table_6_17.dropna(how="all")
table_6_17=table_6_17.reset_index()
table_6_17=table_6_17[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_17)):
    table_6_17["raw_chem_name"].iloc[j]=str(table_6_17["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_17["raw_chem_name"].iloc[j]=clean(str(table_6_17["raw_chem_name"].iloc[j]))
    if len(table_6_17["raw_chem_name"].iloc[j].split())>1:
        table_6_17["raw_chem_name"].iloc[j]=" ".join(table_6_17["raw_chem_name"].iloc[j].split())
    if len(str(table_6_17["raw_cas"].iloc[j]).split())>1:
        table_6_17["raw_cas"].iloc[j]="".join(str(table_6_17["raw_cas"].iloc[j]).split())

table_6_17["data_document_id"]="1372828"
table_6_17["data_document_filename"]="DCPS_105_39.pdf"
table_6_17["doc_date"]="2010"
table_6_17["raw_category"]=""
table_6_17["cat_code"]=""
table_6_17["description_cpcat"]=""
table_6_17["cpcat_code"]=""
table_6_17["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_17.to_csv("dcps_105_table_6_17.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.19
tables=read_pdf("document_1372830.pdf", pages="60", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_19=tables[0]
table_6_19["raw_cas"]=table_6_19.iloc[:,1]
table_6_19["raw_chem_name"]=table_6_19.iloc[:,0]
table_6_19=table_6_19.iloc[4:]
table_6_19=table_6_19[["raw_chem_name","raw_cas"]]
table_6_19=table_6_19.dropna(how="all")
table_6_19=table_6_19.reset_index()
table_6_19=table_6_19[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_19)):
    table_6_19["raw_chem_name"].iloc[j]=str(table_6_19["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_19["raw_chem_name"].iloc[j]=clean(str(table_6_19["raw_chem_name"].iloc[j]))
    if len(table_6_19["raw_chem_name"].iloc[j].split())>1:
        table_6_19["raw_chem_name"].iloc[j]=" ".join(table_6_19["raw_chem_name"].iloc[j].split())
    if len(str(table_6_19["raw_cas"].iloc[j]).split())>1:
        table_6_19["raw_cas"].iloc[j]="".join(str(table_6_19["raw_cas"].iloc[j]).split())

table_6_19["data_document_id"]="1372830"
table_6_19["data_document_filename"]="DCPS_105_41.pdf"
table_6_19["doc_date"]="2010"
table_6_19["raw_category"]=""
table_6_19["cat_code"]=""
table_6_19["description_cpcat"]=""
table_6_19["cpcat_code"]=""
table_6_19["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_19.to_csv("dcps_105_table_6_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.21
tables=read_pdf("document_1372832.pdf", pages="60", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6_21=tables[2]
table_6_21["raw_cas"]=table_6_21.iloc[:,1]
table_6_21["raw_chem_name"]=table_6_21.iloc[:,0]
table_6_21=table_6_21.iloc[4:]
table_6_21=table_6_21[["raw_chem_name","raw_cas"]]
table_6_21=table_6_21.dropna(how="all")
table_6_21=table_6_21.reset_index()
table_6_21=table_6_21[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_21)):
    table_6_21["raw_chem_name"].iloc[j]=str(table_6_21["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_6_21["raw_chem_name"].iloc[j]=clean(str(table_6_21["raw_chem_name"].iloc[j]))
    if len(table_6_21["raw_chem_name"].iloc[j].split())>1:
        table_6_21["raw_chem_name"].iloc[j]=" ".join(table_6_21["raw_chem_name"].iloc[j].split())
    if len(str(table_6_21["raw_cas"].iloc[j]).split())>1:
        table_6_21["raw_cas"].iloc[j]="".join(str(table_6_21["raw_cas"].iloc[j]).split())

table_6_21["data_document_id"]="1372832"
table_6_21["data_document_filename"]="DCPS_105_43.pdf"
table_6_21["doc_date"]="2010"
table_6_21["raw_category"]=""
table_6_21["cat_code"]=""
table_6_21["description_cpcat"]=""
table_6_21["cpcat_code"]=""
table_6_21["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_21.to_csv("dcps_105_table_6_21.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 8.4
table_8_4=read_pdf("document_1372836.pdf", pages="81,82", lattice=True, pandas_options={'header': None})
table_8_4["raw_cas"]=table_8_4.iloc[:,1]
table_8_4["raw_chem_name"]=table_8_4.iloc[:,2]
table_8_4=table_8_4.loc[table_8_4["raw_chem_name"]!="Name"]
table_8_4=table_8_4[["raw_chem_name","raw_cas"]]
table_8_4=table_8_4.dropna(how="all")
table_8_4=table_8_4.reset_index()
table_8_4=table_8_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8_4)):
    table_8_4["raw_chem_name"].iloc[j]=str(table_8_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_8_4["raw_chem_name"].iloc[j]=clean(str(table_8_4["raw_chem_name"].iloc[j]))
    if len(table_8_4["raw_chem_name"].iloc[j].split())>1:
        table_8_4["raw_chem_name"].iloc[j]=" ".join(table_8_4["raw_chem_name"].iloc[j].split())
    if len(str(table_8_4["raw_cas"].iloc[j]).split())>1:
        table_8_4["raw_cas"].iloc[j]="".join(str(table_8_4["raw_cas"].iloc[j]).split())

table_8_4["raw_chem_name"].iloc[2]=table_8_4["raw_chem_name"].iloc[2]+" "+table_8_4["raw_chem_name"].iloc[3]
table_8_4=table_8_4.drop(3)
table_8_4=table_8_4.drop_duplicates()
table_8_4=table_8_4.reset_index()
table_8_4=table_8_4[["raw_chem_name","raw_cas"]]

table_8_4["data_document_id"]="1372836"
table_8_4["data_document_filename"]="DCPS_105_47.pdf"
table_8_4["doc_date"]="2010"
table_8_4["raw_category"]=""
table_8_4["cat_code"]=""
table_8_4["description_cpcat"]=""
table_8_4["cpcat_code"]=""
table_8_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_8_4.to_csv("dcps_105_table_8_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.25
table_5_25=read_pdf("document_1372814.pdf", pages="47,48,49,50", lattice=False,pandas_options={'header': None})
table_5_25["raw_cas"]=table_5_25.iloc[:,1]
table_5_25["raw_chem_name"]=table_5_25.iloc[:,0]
table_5_25=table_5_25.loc[table_5_25["raw_chem_name"]!="Substance name"]
table_5_25=table_5_25[["raw_chem_name","raw_cas"]]
table_5_25=table_5_25.dropna(how="all")
table_5_25=table_5_25.reset_index()
table_5_25=table_5_25[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(1, len(table_5_25)):
    table_5_25["raw_chem_name"].iloc[j]=str(table_5_25["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_25["raw_chem_name"].iloc[j]=clean(str(table_5_25["raw_chem_name"].iloc[j]))
    if str(table_5_25["raw_chem_name"].iloc[j])!="nan" and str(table_5_25["raw_cas"].iloc[j])=="nan":
        table_5_25["raw_chem_name"].iloc[j]=table_5_25["raw_chem_name"].iloc[j-1]+" "+table_5_25["raw_chem_name"].iloc[j]
        table_5_25["raw_cas"].iloc[j]=table_5_25["raw_cas"].iloc[j-1]
        j_drop.append(j-1)

    if str(table_5_25["raw_chem_name"].iloc[j])=="nan" and str(table_5_25["raw_cas"].iloc[j])!="nan":
        table_5_25["raw_chem_name"].iloc[j]=table_5_25["raw_chem_name"].iloc[j-1]
        table_5_25["raw_cas"].iloc[j]=table_5_25["raw_cas"].iloc[j-1]+table_5_25["raw_cas"].iloc[j]
        j_drop.append(j-1)

    if str(table_5_25["raw_cas"].iloc[j-1])[-1]=="," or str(table_5_25["raw_cas"].iloc[j-1])[-1]=="-":
        table_5_25["raw_chem_name"].iloc[j]=table_5_25["raw_chem_name"].iloc[j-1]+" "+table_5_25["raw_chem_name"].iloc[j]
        table_5_25["raw_cas"].iloc[j]=table_5_25["raw_cas"].iloc[j-1]+table_5_25["raw_cas"].iloc[j]
        j_drop.append(j-1)

table_5_25["raw_chem_name"].iloc[20]="xylene"
table_5_25["raw_cas"].iloc[20]="95-47-6, 108-38-3, 106-42-3"
table_5_25["raw_chem_name"].iloc[23]="alkyl benzenes"
table_5_25["raw_cas"].iloc[23]="95-47-6, 108-38-3, 106-42-3"
table_5_25["raw_chem_name"].iloc[52]="alkyl benzenes eg (1-methylethyl)-benzene, 1-ethyl-2-methyl-benzene"
table_5_25["raw_cas"].iloc[52]="98-82-8, 611-14-3"
table_5_25["raw_chem_name"].iloc[82]=table_5_25["raw_chem_name"].iloc[82]+table_5_25["raw_chem_name"].iloc[83]
table_5_25["raw_cas"].iloc[82]=table_5_25["raw_cas"].iloc[82]+table_5_25["raw_cas"].iloc[83]

table_5_25=table_5_25.drop(j_drop)
table_5_25=table_5_25.reset_index()
table_5_25=table_5_25[["raw_chem_name","raw_cas"]]

table_5_25["raw_chem_name"].iloc[82]=table_5_25["raw_chem_name"].iloc[82]+table_5_25["raw_chem_name"].iloc[83]
table_5_25["raw_cas"].iloc[82]=table_5_25["raw_cas"].iloc[82]+table_5_25["raw_cas"].iloc[83]

table_5_25=table_5_25.drop(83)
table_5_25=table_5_25.reset_index()
table_5_25=table_5_25[["raw_chem_name","raw_cas"]]


table_5_25["data_document_id"]="1372814"
table_5_25["data_document_filename"]="DCPS_105_25.pdf"
table_5_25["doc_date"]="2010"
table_5_25["raw_category"]=""
table_5_25["cat_code"]=""
table_5_25["description_cpcat"]=""
table_5_25["cpcat_code"]=""
table_5_25["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_25.to_csv("dcps_105_table_5_25.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 2.1
#name and cas split between 2 columns each so the respective columns for each page are combined and cleaned before all pages are concat'd

tableList=[]
notName=["substance name",
         "solvent",
         "no",
         "vinyl make-up",
         "propellant",
         "1","2","3","4","5","6","7","8","9","10",
         "11","12","13","14","15","16","17","18","19","20",
         "21","22","23","24","25","26","27","28","29","30",
         "31","32","33","34","35","36","37","38","39","40",
         "41",
         "soap/ tensides/ detergent",
         "glass cleaners",
         "acid/basic regulation",
         "compound name",
         "fabric waterproofin g/ surface treatment",
         "fabric waterproofing",
         "fabric cleaner",
         "soap/ tensides/",
         "odour remover",
         "vinyl cleaner",
         "no safety data sheet",
         "leather cleaner",
         "cleaning tissues",
         "anti-mist products",
         "detergent",
         "synthetic materials sealant"
         ]
tables=read_pdf("document_1372792.pdf", pages="19-25", lattice=True, multiple_tables=True, pandas_options={'header': None})
for t in tables:
    t["raw_chem_name_1"]=t.iloc[:,2]
    t["raw_chem_name_2"]=t.iloc[:,0]
    t["raw_cas_1"]=t.iloc[:,3]
    t["raw_cas_2"]=t.iloc[:,1]
    t=t[["raw_chem_name_1","raw_cas_1","raw_chem_name_2","raw_cas_2"]]

    tableTemp=pd.DataFrame()
    tableTemp["raw_chem_name"]=pd.concat([t["raw_chem_name_1"],t["raw_chem_name_2"]],ignore_index=True)
    tableTemp["raw_cas"]=pd.concat([t["raw_cas_1"],t["raw_cas_2"]],ignore_index=True)
    tableTemp=tableTemp[["raw_chem_name","raw_cas"]]
    tableTemp=tableTemp.dropna(how="all")
    tableTemp=tableTemp.reset_index()
    tableTemp=tableTemp[["raw_chem_name","raw_cas"]]

    j_drop=[]
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    for j in range(0, len(tableTemp)):
        tableTemp["raw_chem_name"].iloc[j]=str(tableTemp["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
        tableTemp["raw_chem_name"].iloc[j]=clean(str(tableTemp["raw_chem_name"].iloc[j]))
        if len(tableTemp["raw_chem_name"].iloc[j].split())>1:
            tableTemp["raw_chem_name"].iloc[j]=" ".join(tableTemp["raw_chem_name"].iloc[j].split())
        if len(str(tableTemp["raw_cas"].iloc[j]).split())>1:
            tableTemp["raw_cas"].iloc[j]="".join(str(tableTemp["raw_cas"].iloc[j]).split())

        if tableTemp["raw_chem_name"].iloc[j] in notName:
            j_drop.append(j)

    tableTemp=tableTemp.drop(j_drop)
    tableTemp=tableTemp.reset_index()
    tableTemp=tableTemp[["raw_chem_name","raw_cas"]]
    tableList.append(tableTemp)

table_2_1=pd.concat(tableList,ignore_index=True)
table_2_1["raw_chem_name"].iloc[11]=table_2_1["raw_chem_name"].iloc[11]+" "+table_2_1["raw_chem_name"].iloc[12]
table_2_1=table_2_1.drop([12,20])
table_2_1=table_2_1.drop_duplicates()
table_2_1=table_2_1.reset_index()
table_2_1=table_2_1[["raw_chem_name","raw_cas"]]


table_2_1["data_document_id"]="1372792"
table_2_1["data_document_filename"]="DCPS_105_3.pdf"
table_2_1["doc_date"]="2010"
table_2_1["raw_category"]=""
table_2_1["cat_code"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_1.to_csv("dcps_105_table_2_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
