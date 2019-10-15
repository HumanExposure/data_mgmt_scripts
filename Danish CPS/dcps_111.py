#lkoval
#6/25/19

from tabula import read_pdf
import pandas as pd
import string

#Table 5.6
tables=read_pdf("document_1374421.pdf", pages="36,37", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_6=pd.concat([tables[0],tables[1]], ignore_index=True)
table_5_6["raw_cas"]=table_5_6.iloc[:,2]
table_5_6["raw_chem_name"]=table_5_6.iloc[:,0]
table_5_6["report_funcuse"]=table_5_6.iloc[:,6]
table_5_6=table_5_6.loc[table_5_6["raw_cas"]!= "CAS No"]
table_5_6=table_5_6[["raw_chem_name","raw_cas","report_funcuse"]]
table_5_6=table_5_6.dropna(how="all")
table_5_6=table_5_6.reset_index()
table_5_6=table_5_6[["raw_chem_name","raw_cas","report_funcuse"]]

noCas=["parfum","coco-glucoside","aroma"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_6)):
    table_5_6["raw_chem_name"].iloc[j]=str(table_5_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_6["raw_chem_name"].iloc[j]=clean(str(table_5_6["raw_chem_name"].iloc[j]))

    if str(table_5_6["raw_chem_name"].iloc[j])=="nan" and str(table_5_6["raw_cas"].iloc[j])=="nan":
        table_5_6["raw_chem_name"].iloc[j]=table_5_6["raw_chem_name"].iloc[j-1]
        table_5_6["raw_cas"].iloc[j]=table_5_6["raw_cas"].iloc[j-1]
        table_5_6["report_funcuse"].iloc[j]=table_5_6["report_funcuse"].iloc[j-1]+" "+table_5_6["report_funcuse"].iloc[j]
        j_drop.append(j-1)


table_5_6=table_5_6.drop(j_drop)
table_5_6=table_5_6.reset_index()
table_5_6=table_5_6[["raw_chem_name","raw_cas","report_funcuse"]]

k_drop=[]
for k in range(0,len(table_5_6)):
    if table_5_6["raw_chem_name"].iloc[k] not in noCas:
        if str(table_5_6["raw_cas"].iloc[k])=="nan":
            table_5_6["raw_chem_name"].iloc[k]=table_5_6["raw_chem_name"].iloc[k-1]+" "+table_5_6["raw_chem_name"].iloc[k]
            table_5_6["raw_cas"].iloc[k]=table_5_6["raw_cas"].iloc[k-1]
            table_5_6["report_funcuse"].iloc[k]=table_5_6["report_funcuse"].iloc[k-1]+" "+table_5_6["report_funcuse"].iloc[k]
            k_drop.append(k-1)

table_5_6=table_5_6.drop(k_drop)
table_5_6=table_5_6.reset_index()
table_5_6=table_5_6[["raw_chem_name","raw_cas","report_funcuse"]]


table_5_6["data_document_id"]="1374421"
table_5_6["data_document_filename"]="DCPS_111_a.pdf"
table_5_6["doc_date"]="2011"
table_5_6["raw_category"]=""
table_5_6["cat_code"]=""
table_5_6["description_cpcat"]=""
table_5_6["cpcat_code"]=""
table_5_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_6.to_csv("dcps_111_table_5_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5.7
tables=read_pdf("document_1374422.pdf", pages="37,38", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_7=pd.concat([tables[1],tables[2]], ignore_index=True)
table_5_7["raw_cas"]=table_5_7.iloc[:,2]
table_5_7["raw_chem_name"]=table_5_7.iloc[:,0]
table_5_7["report_funcuse"]=table_5_7.iloc[:,6]
table_5_7=table_5_7.loc[table_5_7["raw_cas"]!= "CAS No"]
table_5_7=table_5_7[["raw_chem_name","raw_cas","report_funcuse"]]
table_5_7=table_5_7.dropna(how="all")
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name","raw_cas","report_funcuse"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_7)):
    table_5_7["raw_chem_name"].iloc[j]=str(table_5_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_7["raw_chem_name"].iloc[j]=clean(str(table_5_7["raw_chem_name"].iloc[j]))
    if str(table_5_7["raw_chem_name"].iloc[j-1])=="nan" and str(table_5_7["raw_cas"].iloc[j-1])=="nan":
        table_5_7["report_funcuse"].iloc[j]=str(table_5_7["report_funcuse"].iloc[j-1])+" "+str(table_5_7["report_funcuse"].iloc[j])
        j_drop.append(j-1)


table_5_7=table_5_7.drop(j_drop)
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name","raw_cas","report_funcuse"]]

k_drop=[]
for k in range(0,len(table_5_7)):
    if str(table_5_7["raw_cas"].iloc[k-1])=="nan" and table_5_7["raw_chem_name"].iloc[k-1]!= "aroma":
        table_5_7["raw_chem_name"].iloc[k]=table_5_7["raw_chem_name"].iloc[k-1]+" "+table_5_7["raw_chem_name"].iloc[k]
        k_drop.append(k-1)

table_5_7=table_5_7.drop(k_drop)
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name","raw_cas","report_funcuse"]]

table_5_7["report_funcuse"].iloc[9]="skin conditioning /emollient "
table_5_7["report_funcuse"].iloc[11]="skin conditioning /emollient "
table_5_7["report_funcuse"].iloc[22]="emollient / emulsifying/ skin conditioning"
table_5_7["report_funcuse"].iloc[17]=table_5_7["report_funcuse"].iloc[17].strip("of products")

table_5_7["data_document_id"]="1374422"
table_5_7["data_document_filename"]="DCPS_111_b.pdf"
table_5_7["doc_date"]="2011"
table_5_7["raw_category"]=""
table_5_7["cat_code"]=""
table_5_7["description_cpcat"]=""
table_5_7["cpcat_code"]=""
table_5_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_7.to_csv("dcps_111_table_5_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5.8
tables=read_pdf("document_1374423.pdf", pages="38,39", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_8=pd.concat([tables[1],tables[2]], ignore_index=True)
table_5_8["raw_cas"]=table_5_8.iloc[:,2]
table_5_8["raw_chem_name"]=table_5_8.iloc[:,0]
table_5_8["report_funcuse"]=table_5_8.iloc[:,6]
table_5_8=table_5_8.loc[table_5_8["raw_cas"]!= "CAS No"]
table_5_8=table_5_8[["raw_chem_name","raw_cas","report_funcuse"]]
table_5_8=table_5_8.dropna(how="all")
table_5_8=table_5_8.reset_index()
table_5_8=table_5_8[["raw_chem_name","raw_cas","report_funcuse"]]

noCas=["parfum","coco-glucoside"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_8)):
    table_5_8["raw_chem_name"].iloc[j]=str(table_5_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_8["raw_chem_name"].iloc[j]=clean(str(table_5_8["raw_chem_name"].iloc[j]))
    if str(table_5_8["raw_chem_name"].iloc[j-1])=="nan" and str(table_5_8["raw_cas"].iloc[j-1])=="nan":
        table_5_8["report_funcuse"].iloc[j]=str(table_5_8["report_funcuse"].iloc[j-1])+" "+str(table_5_8["report_funcuse"].iloc[j])
        j_drop.append(j-1)

table_5_8=table_5_8.drop(j_drop)
table_5_8=table_5_8.reset_index()
table_5_8=table_5_8[["raw_chem_name","raw_cas","report_funcuse"]]

k_drop=[]
for k in range(0,len(table_5_8)):
    if str(table_5_8["raw_cas"].iloc[k-1])=="nan" and table_5_8["raw_chem_name"].iloc[k-1] not in noCas:
        table_5_8["raw_chem_name"].iloc[k]=table_5_8["raw_chem_name"].iloc[k-1]+" "+table_5_8["raw_chem_name"].iloc[k]
        table_5_8["report_funcuse"].iloc[k]=str(table_5_8["report_funcuse"].iloc[k-1])+" "+str(table_5_8["report_funcuse"].iloc[k])
        k_drop.append(k-1)

    table_5_8["report_funcuse"].iloc[k]=str(table_5_8["report_funcuse"].iloc[k]).replace("nan","").replace("of products","")

table_5_8=table_5_8.drop(k_drop)
table_5_8=table_5_8.reset_index()
table_5_8=table_5_8[["raw_chem_name","raw_cas","report_funcuse"]]

table_5_8["report_funcuse"].iloc[15]="skin conditioning/ "+table_5_8["report_funcuse"].iloc[15]
table_5_8["report_funcuse"].iloc[23]="emollient/ skin "+table_5_8["report_funcuse"].iloc[23]

table_5_8["data_document_id"]="1374423"
table_5_8["data_document_filename"]="DCPS_111_c.pdf"
table_5_8["doc_date"]="2011"
table_5_8["raw_category"]=""
table_5_8["cat_code"]=""
table_5_8["description_cpcat"]=""
table_5_8["cpcat_code"]=""
table_5_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_8.to_csv("dcps_111_table_5_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 5.11
table_5_11=read_pdf("document_1374426.pdf", pages="43-45", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_5_11["raw_chem_name"]=table_5_11.iloc[:,0]
table_5_11["report_funcuse"]=table_5_11.iloc[:,1]
table_5_11=table_5_11.loc[table_5_11["raw_chem_name"]!= "INCI name"]
table_5_11=table_5_11[["raw_chem_name","report_funcuse"]]
table_5_11=table_5_11.dropna(subset=["raw_chem_name","report_funcuse"], how="all")
table_5_11=table_5_11.reset_index()
table_5_11=table_5_11[["raw_chem_name","report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_11)):
    table_5_11["raw_chem_name"].iloc[j]=str(table_5_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_11["raw_chem_name"].iloc[j]=clean(str(table_5_11["raw_chem_name"].iloc[j]))
    if len(table_5_11["raw_chem_name"].iloc[j].split())>1:
        table_5_11["raw_chem_name"].iloc[j]=" ".join(table_5_11["raw_chem_name"].iloc[j].split())
    if len(str(table_5_11["report_funcuse"].iloc[j]).split())>1:
        table_5_11["report_funcuse"].iloc[j]=" ".join(str(table_5_11["report_funcuse"].iloc[j]).split())

table_5_11["raw_chem_name"].iloc[58]=table_5_11["raw_chem_name"].iloc[58]+" "+table_5_11["raw_chem_name"].iloc[59]
table_5_11=table_5_11.drop(59)
table_5_11=table_5_11.reset_index()
table_5_11=table_5_11[["raw_chem_name","report_funcuse"]]

table_5_11["data_document_id"]="1374426"
table_5_11["data_document_filename"]="DCPS_111_f.pdf"
table_5_11["doc_date"]="2011"
table_5_11["raw_category"]=""
table_5_11["cat_code"]=""
table_5_11["description_cpcat"]=""
table_5_11["cpcat_code"]=""
table_5_11["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_11.to_csv("dcps_111_table_5_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 7.1
table_7_1=read_pdf("document_1374434.pdf", pages="59,60", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_7_1["raw_chem_name"]=table_7_1.iloc[:,0]
table_7_1=table_7_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7_1)):
    table_7_1["raw_chem_name"].iloc[j]=str(table_7_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_7_1["raw_chem_name"].iloc[j]=clean(str(table_7_1["raw_chem_name"].iloc[j]))
    if len(table_7_1["raw_chem_name"].iloc[j].split())>1:
        table_7_1["raw_chem_name"].iloc[j]=" ".join(table_7_1["raw_chem_name"].iloc[j].split())

table_7_1=table_7_1.drop_duplicates()
table_7_1=table_7_1.loc[table_7_1["raw_chem_name"]!= "essential oil or essential oil component"]
table_7_1=table_7_1.reset_index()
table_7_1=table_7_1[["raw_chem_name"]]

table_7_1["data_document_id"]="1374434"
table_7_1["data_document_filename"]="DCPS_111_n.pdf"
table_7_1["doc_date"]="2011"
table_7_1["raw_category"]=""
table_7_1["cat_code"]=""
table_7_1["description_cpcat"]=""
table_7_1["cpcat_code"]=""
table_7_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_7_1["report_funcuse"]=""

table_7_1.to_csv("dcps_111_table_7_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 2.1
table_2_1=read_pdf("document_1374435.pdf", pages="95-120", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_2_1["raw_chem_name"]=table_2_1.iloc[:,0]
table_2_1["raw_cas"]=table_2_1.iloc[:,1]
table_2_1["report_funcuse"]=table_2_1.iloc[:,3]
table_2_1=table_2_1[["raw_chem_name","raw_cas","report_funcuse"]]

notChems=["Table","INCIName","CAS","Function","Chemical","hemical","unction"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    if str(table_2_1["raw_chem_name"].iloc[j]).split()[0] in notChems:
        j_drop.append(j)

    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if len(table_2_1["raw_chem_name"].iloc[j].split())>1:
        table_2_1["raw_chem_name"].iloc[j]=" ".join(table_2_1["raw_chem_name"].iloc[j].split())
    if len(str(table_2_1["raw_cas"].iloc[j]).split())>1:
        table_2_1["raw_cas"].iloc[j]=" ".join(str(table_2_1["raw_cas"].iloc[j]).split())
    if len(str(table_2_1["report_funcuse"].iloc[j]).split())>1:
        table_2_1["report_funcuse"].iloc[j]=" ".join(str(table_2_1["report_funcuse"].iloc[j]).split())

table_2_1=table_2_1.drop(j_drop)
table_2_1=table_2_1.reset_index()
table_2_1=table_2_1[["raw_chem_name","raw_cas","report_funcuse"]]


table_2_1["data_document_id"]="1374435"
table_2_1["data_document_filename"]="DCPS_111_o.pdf"
table_2_1["doc_date"]="2011"
table_2_1["raw_category"]=""
table_2_1["cat_code"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_1.to_csv("dcps_111_table_2_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)


#Table 3.1
table_3_1=read_pdf("document_1374435.pdf", pages="147-161", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1=pd.concat(table_3_1[:-4], ignore_index=True)
table_3_1["raw_chem_name"]=table_3_1.iloc[:,0]
table_3_1["raw_cas"]=table_3_1.iloc[:,1]
table_3_1["report_funcuse"]=table_3_1.iloc[:,3]
table_3_1=table_3_1[["raw_chem_name","raw_cas","report_funcuse"]]

notChems=["Tabel","INCI","CAS","Function","Chemical","hemical","unction", "AS"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1)):
    if str(table_3_1["raw_chem_name"].iloc[j]).split()[0] in notChems:
        j_drop.append(j)

    table_3_1["raw_chem_name"].iloc[j]=str(table_3_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_3_1["raw_chem_name"].iloc[j]=clean(str(table_3_1["raw_chem_name"].iloc[j]))
    if len(table_3_1["raw_chem_name"].iloc[j].split())>1:
        table_3_1["raw_chem_name"].iloc[j]=" ".join(table_3_1["raw_chem_name"].iloc[j].split())
    if len(str(table_3_1["raw_cas"].iloc[j]).split())>1:
        table_3_1["raw_cas"].iloc[j]=" ".join(str(table_3_1["raw_cas"].iloc[j]).split())
    if len(str(table_3_1["report_funcuse"].iloc[j]).split())>1:
        table_3_1["report_funcuse"].iloc[j]=" ".join(str(table_3_1["report_funcuse"].iloc[j]).split())

table_3_1=table_3_1.drop(j_drop)
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas","report_funcuse"]]


table_3_1["data_document_id"]="1374435"
table_3_1["data_document_filename"]="DCPS_111_p.pdf"
table_3_1["doc_date"]="2011"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1.to_csv("dcps_111_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 3.2
table_3_2=read_pdf("document_1374436.pdf", pages="161-180", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_2=pd.concat(table_3_2[2:], ignore_index=True)
table_3_2["raw_chem_name"]=table_3_2.iloc[:,0]
table_3_2["raw_cas"]=table_3_2.iloc[:,1]
table_3_2["report_funcuse"]=table_3_2.iloc[:,3]
table_3_2=table_3_2[["raw_chem_name","raw_cas","report_funcuse"]]

notChems=["Tabel","INCI","CAS","Function","Chemical","hemical","unction", "AS"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    if str(table_3_2["raw_chem_name"].iloc[j]).split()[0] in notChems:
        j_drop.append(j)

    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(table_3_2["raw_chem_name"].iloc[j].split())>1:
        table_3_2["raw_chem_name"].iloc[j]=" ".join(table_3_2["raw_chem_name"].iloc[j].split())
    if len(str(table_3_2["raw_cas"].iloc[j]).split())>1:
        table_3_2["raw_cas"].iloc[j]=" ".join(str(table_3_2["raw_cas"].iloc[j]).split())
    if len(str(table_3_2["report_funcuse"].iloc[j]).split())>1:
        table_3_2["report_funcuse"].iloc[j]=" ".join(str(table_3_2["report_funcuse"].iloc[j]).split())

table_3_2=table_3_2.drop(j_drop)
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas","report_funcuse"]]


table_3_2["data_document_id"]="1374436"
table_3_2["data_document_filename"]="DCPS_111_q.pdf"
table_3_2["doc_date"]="2011"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_111_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
