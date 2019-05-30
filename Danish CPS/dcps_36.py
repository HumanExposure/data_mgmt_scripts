#lkoval
#5/30/19

from tabula import read_pdf
import pandas as pd
import string

#Table 3.2
table_3_2=read_pdf("document_1373567.pdf", pages="26", lattice=True, pandas_options={'header': None})
table_3_2["raw_chem_name"]=table_3_2.iloc[2:,0]
table_3_2["raw_cas"]=table_3_2.iloc[2:,1]
table_3_2=table_3_2.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_3_2=table_3_2.drop([2,33])
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(str(table_3_2["raw_cas"].iloc[j]).split())>1:
        table_3_2["raw_cas"].iloc[j]=" ".join(str(table_3_2["raw_cas"].iloc[j]).split())


table_3_2["data_document_id"]="1373567"
table_3_2["data_document_filename"]="DCPS_36_a.pdf"
table_3_2["doc_date"]="2003"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_36_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.1
table_6_1=read_pdf("document_1373568.pdf", pages="69", lattice=True, pandas_options={'header': None})
table_6_1["raw_chem_name"]=table_6_1.iloc[3:-1,0]
table_6_1["raw_cas"]=table_6_1.iloc[3:-1,1]
table_6_1=table_6_1.dropna(subset=["raw_chem_name"])
table_6_1=table_6_1.reset_index()
table_6_1=table_6_1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_1)):
    table_6_1["raw_chem_name"].iloc[j]=str(table_6_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_1["raw_chem_name"].iloc[j]=clean(str(table_6_1["raw_chem_name"].iloc[j]))
    if len(table_6_1["raw_chem_name"].iloc[j].split())>1:
        table_6_1["raw_chem_name"].iloc[j]=" ".join(table_6_1["raw_chem_name"].iloc[j].split())


table_6_1["data_document_id"]="1373568"
table_6_1["data_document_filename"]="DCPS_36_b.pdf"
table_6_1["doc_date"]="2003"
table_6_1["raw_category"]=""
table_6_1["cat_code"]=""
table_6_1["description_cpcat"]=""
table_6_1["cpcat_code"]=""
table_6_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_1.to_csv("dcps_36_table_6_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.2
table_6_2=read_pdf("document_1373569.pdf", pages="70", lattice=True, pandas_options={'header': None})
table_6_2["raw_chem_name"]=table_6_2.iloc[3:-1,0]
table_6_2["raw_cas"]=table_6_2.iloc[3:-1,1]
table_6_2=table_6_2.dropna(subset=["raw_chem_name"])
table_6_2=table_6_2.reset_index()
table_6_2=table_6_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_2)):
    table_6_2["raw_chem_name"].iloc[j]=str(table_6_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_2["raw_chem_name"].iloc[j]=clean(str(table_6_2["raw_chem_name"].iloc[j]))
    if len(table_6_2["raw_chem_name"].iloc[j].split())>1:
        table_6_2["raw_chem_name"].iloc[j]=" ".join(table_6_2["raw_chem_name"].iloc[j].split())


table_6_2["data_document_id"]="1373569"
table_6_2["data_document_filename"]="DCPS_36_c.pdf"
table_6_2["doc_date"]="2003"
table_6_2["raw_category"]=""
table_6_2["cat_code"]=""
table_6_2["description_cpcat"]=""
table_6_2["cpcat_code"]=""
table_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_2.to_csv("dcps_36_table_6_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.3
table_6_3=read_pdf("document_1373570.pdf", pages="72", lattice=True, pandas_options={'header': None})
table_6_3["raw_chem_name"]=table_6_3.iloc[3:-1,0]
table_6_3["raw_cas"]=table_6_3.iloc[3:-1,1]
table_6_3=table_6_3.dropna(subset=["raw_chem_name"])
table_6_3=table_6_3.reset_index()
table_6_3=table_6_3[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_3)):
    table_6_3["raw_chem_name"].iloc[j]=str(table_6_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_3["raw_chem_name"].iloc[j]=clean(str(table_6_3["raw_chem_name"].iloc[j]))
    if len(table_6_3["raw_chem_name"].iloc[j].split())>1:
        table_6_3["raw_chem_name"].iloc[j]=" ".join(table_6_3["raw_chem_name"].iloc[j].split())


table_6_3["data_document_id"]="1373570"
table_6_3["data_document_filename"]="DCPS_36_d.pdf"
table_6_3["doc_date"]="2003"
table_6_3["raw_category"]=""
table_6_3["cat_code"]=""
table_6_3["description_cpcat"]=""
table_6_3["cpcat_code"]=""
table_6_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_3.to_csv("dcps_36_table_6_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.4
table_6_4=read_pdf("document_1373571.pdf", pages="73", lattice=True, pandas_options={'header': None})
table_6_4["raw_chem_name"]=table_6_4.iloc[3:-1,0]
table_6_4["raw_cas"]=table_6_4.iloc[3:-1,1]
table_6_4=table_6_4.dropna(subset=["raw_chem_name"])
table_6_4=table_6_4.reset_index()
table_6_4=table_6_4[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_4)):
    table_6_4["raw_chem_name"].iloc[j]=str(table_6_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_4["raw_chem_name"].iloc[j]=clean(str(table_6_4["raw_chem_name"].iloc[j]))
    if len(table_6_4["raw_chem_name"].iloc[j].split())>1:
        table_6_4["raw_chem_name"].iloc[j]=" ".join(table_6_4["raw_chem_name"].iloc[j].split())


table_6_4["data_document_id"]="1373571"
table_6_4["data_document_filename"]="DCPS_36_e.pdf"
table_6_4["doc_date"]="2003"
table_6_4["raw_category"]=""
table_6_4["cat_code"]=""
table_6_4["description_cpcat"]=""
table_6_4["cpcat_code"]=""
table_6_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_4.to_csv("dcps_36_table_6_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.5
table_6_5=read_pdf("document_1373572.pdf", pages="74", lattice=True, pandas_options={'header': None})
table_6_5["raw_chem_name"]=table_6_5.iloc[3:-1,0]
table_6_5["raw_cas"]=table_6_5.iloc[3:-1,1]
table_6_5=table_6_5.dropna(subset=["raw_chem_name"])
table_6_5=table_6_5.reset_index()
table_6_5=table_6_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_5)):
    table_6_5["raw_chem_name"].iloc[j]=str(table_6_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_5["raw_chem_name"].iloc[j]=clean(str(table_6_5["raw_chem_name"].iloc[j]))
    if len(table_6_5["raw_chem_name"].iloc[j].split())>1:
        table_6_5["raw_chem_name"].iloc[j]=" ".join(table_6_5["raw_chem_name"].iloc[j].split())


table_6_5["data_document_id"]="1373572"
table_6_5["data_document_filename"]="DCPS_36_f.pdf"
table_6_5["doc_date"]="2003"
table_6_5["raw_category"]=""
table_6_5["cat_code"]=""
table_6_5["description_cpcat"]=""
table_6_5["cpcat_code"]=""
table_6_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_5.to_csv("dcps_36_table_6_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.6
table_6_6=read_pdf("document_1373573.pdf", pages="75", lattice=True, pandas_options={'header': None})
table_6_6["raw_chem_name"]=table_6_6.iloc[3:-1,0]
table_6_6["raw_cas"]=table_6_6.iloc[3:-1,1]
table_6_6=table_6_6.dropna(subset=["raw_chem_name"])
table_6_6=table_6_6.reset_index()
table_6_6=table_6_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_6)):
    table_6_6["raw_chem_name"].iloc[j]=str(table_6_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_6["raw_chem_name"].iloc[j]=clean(str(table_6_6["raw_chem_name"].iloc[j]))
    if len(table_6_6["raw_chem_name"].iloc[j].split())>1:
        table_6_6["raw_chem_name"].iloc[j]=" ".join(table_6_6["raw_chem_name"].iloc[j].split())


table_6_6["data_document_id"]="1373573"
table_6_6["data_document_filename"]="DCPS_36_g.pdf"
table_6_6["doc_date"]="2003"
table_6_6["raw_category"]=""
table_6_6["cat_code"]=""
table_6_6["description_cpcat"]=""
table_6_6["cpcat_code"]=""
table_6_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_6.to_csv("dcps_36_table_6_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6.7
table_6_7=read_pdf("document_1373574.pdf", pages="76", lattice=True, pandas_options={'header': None})
table_6_7["raw_chem_name"]=table_6_7.iloc[3:-1,0]
table_6_7=table_6_7.dropna(subset=["raw_chem_name"])
table_6_7=table_6_7.reset_index()
table_6_7=table_6_7[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_7)):
    table_6_7["raw_chem_name"].iloc[j]=str(table_6_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    table_6_7["raw_chem_name"].iloc[j]=clean(str(table_6_7["raw_chem_name"].iloc[j]))

table_6_7["data_document_id"]="1373574"
table_6_7["data_document_filename"]="DCPS_36_h.pdf"
table_6_7["doc_date"]="2003"
table_6_7["raw_category"]=""
table_6_7["cat_code"]=""
table_6_7["description_cpcat"]=""
table_6_7["cpcat_code"]=""
table_6_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_7.to_csv("dcps_36_table_6_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Appendix 2
appen_2=read_pdf("document_1373575.pdf", pages="92-97", lattice=True, pandas_options={'header': None})
appen_2["raw_chem_name"]=appen_2.iloc[:,1]
appen_2["raw_cas"]=appen_2.iloc[:,2]
appen_2=appen_2.dropna(subset=["raw_chem_name"])
appen_2=appen_2.loc[appen_2["raw_chem_name"]!= "Component"]
appen_2=appen_2.loc[appen_2["raw_chem_name"]!= "Syrer"]
appen_2=appen_2.loc[appen_2["raw_chem_name"]!= "SUM"]
appen_2=appen_2.loc[appen_2["raw_chem_name"]!= "NUMBER"]
appen_2=appen_2.reset_index()
appen_2=appen_2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_2)):
    appen_2["raw_chem_name"].iloc[j]=str(appen_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_2["raw_chem_name"].iloc[j]=clean(str(appen_2["raw_chem_name"].iloc[j]))
    if len(appen_2["raw_chem_name"].iloc[j].split())>1:
        appen_2["raw_chem_name"].iloc[j]=" ".join(appen_2["raw_chem_name"].iloc[j].split())

#correct error caused by formatting mistake on pdf
appen_2["raw_chem_name"].iloc[134]="4-trimethyl-cyclohexanemethanol alpha alpha"
appen_2["raw_cas"].iloc[134]="498-81-7"
appen_2=appen_2.drop([57,135])
appen_2=appen_2.reset_index()
appen_2=appen_2[["raw_chem_name","raw_cas"]]

appen_2["data_document_id"]="1373575"
appen_2["data_document_filename"]="DCPS_36_i.pdf"
appen_2["doc_date"]="2003"
appen_2["raw_category"]=""
appen_2["cat_code"]=""
appen_2["description_cpcat"]=""
appen_2["cpcat_code"]=""
appen_2["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_2.to_csv("dcps_36_appen_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
