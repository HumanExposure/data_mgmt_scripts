#lkoval
#6-19-19

from tabula import read_pdf
import pandas as pd
import string

#Table 1.5
temp=read_pdf("document_1374286.pdf", pages="22,23", lattice=True, pandas_options={'header': None})
temp["raw_chem_name"]=temp.iloc[:,1]
temp=temp.drop([0,15])
temp=temp.dropna(subset=["raw_chem_name"])
temp=temp.reset_index()
temp=temp[["raw_chem_name"]]

chemList=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(temp)):
    temp["raw_chem_name"].iloc[j]=str(temp["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    temp["raw_chem_name"].iloc[j]=clean(str(temp["raw_chem_name"].iloc[j]))
    for k in range(0,len(temp["raw_chem_name"].iloc[j].split(","))):
        chemList.append(temp["raw_chem_name"].iloc[j].split(",")[k])

table_1_5=pd.DataFrame()
table_1_5["raw_chem_name"]=""
table_1_5["raw_chem_name"]=chemList

l_drop=[]
for l in range (0,len(table_1_5)):
    if len(table_1_5["raw_chem_name"].iloc[l].split())>1:
        table_1_5["raw_chem_name"].iloc[l]=" ".join(table_1_5["raw_chem_name"].iloc[l].split())
    if table_1_5["raw_chem_name"].iloc[l]=="" or table_1_5["raw_chem_name"].iloc[l]==" ":
        l_drop.append(l)
    table_1_5["raw_chem_name"].iloc[l]=table_1_5["raw_chem_name"].iloc[l].strip()

table_1_5=table_1_5.drop(l_drop)
table_1_5=table_1_5.drop_duplicates()
table_1_5=table_1_5.reset_index()
table_1_5=table_1_5[["raw_chem_name"]]

table_1_5["data_document_id"]="1374286"
table_1_5["data_document_filename"]="DCPS_79_b.pdf"
table_1_5["doc_date"]="2006"
table_1_5["raw_category"]=""
table_1_5["cat_code"]=""
table_1_5["description_cpcat"]=""
table_1_5["cpcat_code"]=""
table_1_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_1_5["report_funcuse"]=""

table_1_5.to_csv("dcps_79_table_1_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 2.2
table_2_2=read_pdf("document_1374287.pdf", pages="26", lattice=True, pandas_options={'header': None})
table_2_2["raw_chem_name"]=table_2_2.iloc[1:,0]
table_2_2["raw_cas"]=table_2_2.iloc[1:,1]
table_2_2=table_2_2.dropna(subset=["raw_chem_name"])
table_2_2=table_2_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_2)):
    table_2_2["raw_chem_name"].iloc[j]=str(table_2_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_2_2["raw_chem_name"].iloc[j]=clean(str(table_2_2["raw_chem_name"].iloc[j]))

table_2_2["data_document_id"]="1374287"
table_2_2["data_document_filename"]="DCPS_79_c.pdf"
table_2_2["doc_date"]="2006"
table_2_2["raw_category"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_2["report_funcuse"]=""

table_2_2.to_csv("dcps_79_table_2_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 2.4
table_2_4=read_pdf("document_1374288.pdf", pages="28,29", lattice=True, pandas_options={'header': None})
table_2_4["raw_chem_name"]=table_2_4.iloc[:,1]
table_2_4["raw_cas"]=table_2_4.iloc[:,2]
table_2_4["report_funcuse"]=table_2_4.iloc[1:,5]
table_2_4=table_2_4.dropna(subset=["raw_chem_name"])
table_2_4=table_2_4.loc[table_2_4["raw_chem_name"]!="Name"]
table_2_4=table_2_4[["raw_chem_name","raw_cas","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("β","beta")
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]=" ".join(table_2_4["raw_chem_name"].iloc[j].split())
    if len(str(table_2_4["report_funcuse"].iloc[j]).split())>1:
        table_2_4["report_funcuse"].iloc[j]=" ".join(str(table_2_4["report_funcuse"].iloc[j]).split())

table_2_4["data_document_id"]="1374288"
table_2_4["data_document_filename"]="DCPS_79_d.pdf"
table_2_4["doc_date"]="2006"
table_2_4["raw_category"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_4.to_csv("dcps_79_table_2_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 3.2
tables=read_pdf("document_1374289.pdf", pages="31,32", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_2=pd.concat(tables[1:3], ignore_index=True)
table_3_2["raw_chem_name"]=table_3_2.iloc[1:,0]
table_3_2["raw_cas"]=table_3_2.iloc[1:,1]
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

table_3_2["data_document_id"]="1374289"
table_3_2["data_document_filename"]="DCPS_79_e.pdf"
table_3_2["doc_date"]="2006"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_2["report_funcuse"]=""

table_3_2.to_csv("dcps_79_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 3.4
table_3_4=read_pdf("document_1374290.pdf", pages="33", lattice=True, pandas_options={'header': None})
table_3_4["raw_chem_name"]=table_3_4.iloc[1:,0]
table_3_4["raw_cas"]=table_3_4.iloc[1:,1]
table_3_4=table_3_4.dropna(subset=["raw_chem_name"])
table_3_4=table_3_4.loc[table_3_4["raw_chem_name"]!="Substance"]
table_3_4=table_3_4.reset_index()
table_3_4=table_3_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_4)):
    table_3_4["raw_chem_name"].iloc[j]=str(table_3_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_3_4["raw_chem_name"].iloc[j]=clean(str(table_3_4["raw_chem_name"].iloc[j]))

table_3_4["data_document_id"]="1374290"
table_3_4["data_document_filename"]="DCPS_79_f.pdf"
table_3_4["doc_date"]="2006"
table_3_4["raw_category"]=""
table_3_4["cat_code"]=""
table_3_4["description_cpcat"]=""
table_3_4["cpcat_code"]=""
table_3_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_4["report_funcuse"]=""

table_3_4.to_csv("dcps_79_table_3_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Section 4 classifications
sec_4=read_pdf("document_1374291.pdf", pages="35-37", lattice=True, pandas_options={'header': None})
sec_4["raw_chem_name"]=sec_4.iloc[1:,0]
sec_4=sec_4.dropna(subset=["raw_chem_name"])
sec_4=sec_4.reset_index()
sec_4=sec_4[["raw_chem_name"]]

j_drop=[]
notChems=["sample","product","substance", "to"]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(sec_4)):
    sec_4["raw_chem_name"].iloc[j]=str(sec_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    sec_4["raw_chem_name"].iloc[j]=clean(str(sec_4["raw_chem_name"].iloc[j]))
    if sec_4["raw_chem_name"].iloc[j].split()[0] in notChems:
        j_drop.append(j)

sec_4=sec_4.drop(j_drop)
sec_4=sec_4.drop_duplicates()
sec_4=sec_4.reset_index()
sec_4=sec_4[["raw_chem_name"]]


sec_4["data_document_id"]="1374291"
sec_4["data_document_filename"]="DCPS_79_g.pdf"
sec_4["doc_date"]="2006"
sec_4["raw_category"]=""
sec_4["cat_code"]=""
sec_4["description_cpcat"]=""
sec_4["cpcat_code"]=""
sec_4["cpcat_sourcetype"]="ACToR Assays and Lists"
sec_4["report_funcuse"]=""

sec_4.to_csv("dcps_79_sec_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
