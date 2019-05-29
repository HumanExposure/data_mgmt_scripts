#lkoval
#5/23/19

from tabula import read_pdf
import pandas as pd
import string

#Table 3
table_3=read_pdf("document_1372762.pdf", pages="11,12,13", lattice=False, multiple_tables=False, pandas_options={'header': None})
table_3["raw_chem_name"]=table_3.iloc[4:,0]
table_3["flag"]=table_3.iloc[4:,1]
table_3=table_3.dropna(subset=["raw_chem_name"])
table_3=table_3.reset_index()
table_3=table_3[["raw_chem_name","flag"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_3["raw_chem_name"].iloc[j]=clean(str(table_3["raw_chem_name"].iloc[j]))
    if str(table_3["flag"].iloc[j])=="nan":
        table_3["raw_chem_name"].iloc[j]=table_3["raw_chem_name"].iloc[j-1]+" "+table_3["raw_chem_name"].iloc[j]
        table_3["flag"].iloc[j]=table_3["flag"].iloc[j-1]
        j_drop.append(j-1)

table_3=table_3.drop(j_drop)
table_3=table_3.reset_index()
table_3=table_3[["raw_chem_name"]]

table_3["data_document_id"]="1372762"
table_3["data_document_filename"]="DCPS_14_c.pdf"
table_3["doc_date"]="2002"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3.to_csv("dcps_14_table_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5
table_5=read_pdf("document_1372764.pdf", pages="16", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_5["raw_chem_name"]=table_5.iloc[:,0]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5.reset_index()
table_5=table_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("#","").replace("^","")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]=" ".join(table_5["raw_chem_name"].iloc[j].split())

#drop chems below limit of detection and irrelevant entries
table_5=table_5.drop([0,26,27])
table_5=table_5.reset_index()
table_5=table_5[["raw_chem_name"]]

table_5["data_document_id"]="1372764"
table_5["data_document_filename"]="DCPS_14_e.pdf"
table_5["doc_date"]="2002"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5.to_csv("dcps_14_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 6
table_6=read_pdf("document_1372765.pdf", pages="17-19", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_6["raw_chem_name"]=table_6.iloc[:,0]
table_6=table_6.dropna(subset=["raw_chem_name"])
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("#","").replace("^","").replace(" ^","")
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())

    if table_6["raw_chem_name"].iloc[j][0]=="(" and table_6["raw_chem_name"].iloc[j][-1]==")":
        table_6["raw_chem_name"].iloc[j]=table_6["raw_chem_name"].iloc[j][1:-1]

#drop chems below limit of detection and irrelevant entries
table_6=table_6.drop([0,94])
table_6=table_6.reset_index()
table_6=table_6[["raw_chem_name"]]

table_6["data_document_id"]="1372765"
table_6["data_document_filename"]="DCPS_14_f.pdf"
table_6["doc_date"]="2002"
table_6["raw_category"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6.to_csv("dcps_14_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
