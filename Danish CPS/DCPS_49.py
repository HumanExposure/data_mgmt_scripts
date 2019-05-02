#lkoval
#5-2-19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables 18, as pandas dfs using tabula

#Table 18
tables=read_pdf("document_1359461.pdf", pages="38", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_18=tables[1]
table_18["raw_chem_name"]=table_18.iloc[:,0]
table_18["raw_cas"]=table_18.iloc[:,1]
table_18=table_18.loc[table_18["raw_chem_name"]!= "Component"]
table_18=table_18.reset_index()
table_18=table_18[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_18)):
    table_18["raw_chem_name"].iloc[i]=table_18["raw_chem_name"].iloc[i].lower().strip()
    table_18["raw_chem_name"].iloc[i]=clean(table_18["raw_chem_name"].iloc[i])

table_18["data_document_id"]="1359461"
table_18["data_document_filename"]="DCPS_49_a.pdf"
table_18["doc_date"]="2004"
table_18["raw_category"]=""
table_18["cat_code"]=""
table_18["description_cpcat"]=""
table_18["cpcat_code"]=""
table_18["cpcat_sourcetype"]="ACToR Assays and Lists"

table_18.to_csv("DCPS_49_table_18.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 20
tables=read_pdf("document_1359461.pdf", pages="39", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_20=tables[2]
table_20["raw_chem_name"]=table_20.iloc[:,0]
table_20["raw_cas"]=table_20.iloc[:,1]
table_20=table_20.loc[table_20["raw_chem_name"]!= "Compound"]
table_20=table_20.reset_index()
table_20=table_20[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_20)):
    table_20["raw_chem_name"].iloc[i]=table_20["raw_chem_name"].iloc[i].lower().strip()
    table_20["raw_chem_name"].iloc[i]=clean(table_20["raw_chem_name"].iloc[i])
    if len(table_20["raw_cas"].iloc[i].split())>1:
        table_20["raw_cas"].iloc[i]=" ".join(table_20["raw_cas"].iloc[i].split())

table_20["data_document_id"]="1359461"
table_20["data_document_filename"]="DCPS_49_b.pdf"
table_20["doc_date"]="2004"
table_20["raw_category"]=""
table_20["cat_code"]=""
table_20["description_cpcat"]=""
table_20["cpcat_code"]=""
table_20["cpcat_sourcetype"]="ACToR Assays and Lists"

table_20.to_csv("DCPS_49_table_20.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 21
tables=read_pdf("document_1359461.pdf", pages="39", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_21=tables[3]
table_21["raw_chem_name"]=table_21.iloc[:,0]
table_21["raw_cas"]=table_21.iloc[:,1]
table_21=table_21.loc[table_21["raw_chem_name"]!= "Compound"]
table_21=table_21.reset_index()
table_21=table_21[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_21)):
    table_21["raw_chem_name"].iloc[i]=table_21["raw_chem_name"].iloc[i].lower().strip()
    table_21["raw_chem_name"].iloc[i]=clean(table_21["raw_chem_name"].iloc[i])
    if len(table_21["raw_cas"].iloc[i].split())>1:
        table_21["raw_cas"].iloc[i]=" ".join(table_21["raw_cas"].iloc[i].split())

table_21["data_document_id"]="1359461"
table_21["data_document_filename"]="DCPS_49_c.pdf"
table_21["doc_date"]="2004"
table_21["raw_category"]=""
table_21["cat_code"]=""
table_21["description_cpcat"]=""
table_21["cpcat_code"]=""
table_21["cpcat_sourcetype"]="ACToR Assays and Lists"

table_21.to_csv("DCPS_49_table_21.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 22
tables=read_pdf("document_1359461.pdf", pages="44", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_22=tables[0]
table_22["raw_chem_name"]=table_22.iloc[:-1,1]
table_22["raw_cas"]=table_22.iloc[:-1,2]
table_22=table_22.loc[table_22["raw_cas"]!= "CAS no."]
table_22=table_22.loc[table_22["raw_chem_name"]!= "Comfort and health assessment"]
table_22=table_22[["raw_chem_name","raw_cas"]]
table_22=table_22.dropna(how="all")
table_22=table_22.reset_index()
table_22=table_22[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_22)):
    table_22["raw_chem_name"].iloc[i]=table_22["raw_chem_name"].iloc[i].lower().strip()
    table_22["raw_chem_name"].iloc[i]=clean(table_22["raw_chem_name"].iloc[i])
    if len(table_22["raw_chem_name"].iloc[i].split())>1:
        table_22["raw_chem_name"].iloc[i]=" ".join(table_22["raw_chem_name"].iloc[i].split())

table_22["data_document_id"]="1359461"
table_22["data_document_filename"]="DCPS_49_d.pdf"
table_22["doc_date"]="2004"
table_22["raw_category"]=""
table_22["cat_code"]=""
table_22["description_cpcat"]=""
table_22["cpcat_code"]=""
table_22["cpcat_sourcetype"]="ACToR Assays and Lists"

table_22.to_csv("DCPS_49_table_22.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 23
tables=read_pdf("document_1359461.pdf", pages="44,45", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_23=pd.concat([tables[1], tables[2]],ignore_index=True)
table_23["raw_chem_name"]=table_23.iloc[:-1,1]
table_23["raw_cas"]=table_23.iloc[:-1,2]
table_23=table_23.loc[table_23["raw_cas"]!= "CAS no."]
table_23=table_23.loc[table_23["raw_chem_name"]!= "Comfort and health assessment"]
table_23["raw_chem_name"].iloc[2]="Butane"
table_23["raw_cas"].iloc[2]="71-36-3"
table_23=table_23[["raw_chem_name","raw_cas"]]
table_23=table_23.dropna(how="all")
table_23=table_23.reset_index()
table_23=table_23[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_23)):
    table_23["raw_chem_name"].iloc[i]=table_23["raw_chem_name"].iloc[i].lower().strip()
    table_23["raw_chem_name"].iloc[i]=clean(table_23["raw_chem_name"].iloc[i])
    if len(table_23["raw_chem_name"].iloc[i].split())>1:
        table_23["raw_chem_name"].iloc[i]=" ".join(table_23["raw_chem_name"].iloc[i].split())

table_23["data_document_id"]="1359461"
table_23["data_document_filename"]="DCPS_49_e.pdf"
table_23["doc_date"]="2004"
table_23["raw_category"]=""
table_23["cat_code"]=""
table_23["description_cpcat"]=""
table_23["cpcat_code"]=""
table_23["cpcat_sourcetype"]="ACToR Assays and Lists"

table_23.to_csv("DCPS_49_table_23.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



#Table 24
tables=read_pdf("document_1359461.pdf", pages="44,45", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_24=tables[3]
table_24["raw_chem_name"]=table_24.iloc[:-1,1]
table_24["raw_cas"]=table_24.iloc[:-1,2]
table_24=table_24.loc[table_24["raw_cas"]!= "CAS no."]
table_24=table_24.loc[table_24["raw_chem_name"]!= "Comfort and health assessment"]
table_24=table_24[["raw_chem_name","raw_cas"]]
table_24=table_24.dropna(how="all")
table_24=table_24.reset_index()
table_24=table_24[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_24)):
    table_24["raw_chem_name"].iloc[i]=table_24["raw_chem_name"].iloc[i].lower().strip()
    table_24["raw_chem_name"].iloc[i]=clean(table_24["raw_chem_name"].iloc[i])
    if len(table_24["raw_chem_name"].iloc[i].split())>1:
        table_24["raw_chem_name"].iloc[i]=" ".join(table_24["raw_chem_name"].iloc[i].split())

table_24["data_document_id"]="1359461"
table_24["data_document_filename"]="DCPS_49_f.pdf"
table_24["doc_date"]="2004"
table_24["raw_category"]=""
table_24["cat_code"]=""
table_24["description_cpcat"]=""
table_24["cpcat_code"]=""
table_24["cpcat_sourcetype"]="ACToR Assays and Lists"

table_24.to_csv("DCPS_49_table_24.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 25
tables=read_pdf("document_1359461.pdf", pages="44,45", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_25=pd.concat([tables[1], tables[2]],ignore_index=True)
table_25["raw_chem_name"]=table_25.iloc[:-1,1]
table_25["raw_cas"]=table_25.iloc[:-1,2]
table_25=table_25.loc[table_25["raw_cas"]!= "CAS no."]
table_25=table_25.loc[table_25["raw_chem_name"]!= "Comfort and health assessment"]
table_25["raw_chem_name"].iloc[2]="Butane"
table_25["raw_cas"].iloc[2]="71-36-3"
table_25=table_25[["raw_chem_name","raw_cas"]]
table_25=table_25.dropna(how="all")
table_25=table_25.reset_index()
table_25=table_25[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_25)):
    table_25["raw_chem_name"].iloc[i]=table_25["raw_chem_name"].iloc[i].lower().strip()
    table_25["raw_chem_name"].iloc[i]=clean(table_25["raw_chem_name"].iloc[i])
    if len(table_25["raw_chem_name"].iloc[i].split())>1:
        table_25["raw_chem_name"].iloc[i]=" ".join(table_25["raw_chem_name"].iloc[i].split())

table_25["data_document_id"]="1359461"
table_25["data_document_filename"]="DCPS_49_g.pdf"
table_25["doc_date"]="2004"
table_25["raw_category"]=""
table_25["cat_code"]=""
table_25["description_cpcat"]=""
table_25["cpcat_code"]=""
table_25["cpcat_sourcetype"]="ACToR Assays and Lists"

table_25.to_csv("DCPS_49_table_25.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 26
tables=read_pdf("document_1359461.pdf", pages="45", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_26=tables[3]
table_26["raw_chem_name"]=table_26.iloc[:-1,1]
table_26["raw_cas"]=table_26.iloc[:-1,2]
table_26=table_26.loc[table_26["raw_cas"]!= "CAS no."]
table_26=table_26.loc[table_26["raw_chem_name"]!= "Comfort and health assessment"]
table_26=table_26[["raw_chem_name","raw_cas"]]
table_26=table_26.dropna(how="all")
table_26=table_26.reset_index()
table_26=table_26[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_26)):
    table_26["raw_chem_name"].iloc[i]=table_26["raw_chem_name"].iloc[i].lower().strip().replace("α","alpha")
    table_26["raw_chem_name"].iloc[i]=clean(table_26["raw_chem_name"].iloc[i])
    if len(table_26["raw_chem_name"].iloc[i].split())>1:
        table_26["raw_chem_name"].iloc[i]=" ".join(table_26["raw_chem_name"].iloc[i].split())

table_26["data_document_id"]="1359461"
table_26["data_document_filename"]="DCPS_49_h.pdf"
table_26["doc_date"]="2004"
table_26["raw_category"]=""
table_26["cat_code"]=""
table_26["description_cpcat"]=""
table_26["cpcat_code"]=""
table_26["cpcat_sourcetype"]="ACToR Assays and Lists"

table_26.to_csv("DCPS_49_table_26.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 28
tables=read_pdf("document_1359461.pdf", pages="47", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_28=tables[0]
table_28["raw_chem_name"]=table_28.iloc[:,0]
table_28["raw_cas"]=table_28.iloc[:,1]
table_28=table_28.loc[table_28["raw_cas"]!= "CAS no."]
table_28=table_28.reset_index()
table_28=table_28[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_28)):
    table_28["raw_chem_name"].iloc[i]=table_28["raw_chem_name"].iloc[i].lower().strip()
    table_28["raw_chem_name"].iloc[i]=clean(table_28["raw_chem_name"].iloc[i])
    if len(table_28["raw_chem_name"].iloc[i].split())>1:
        table_28["raw_chem_name"].iloc[i]=" ".join(table_28["raw_chem_name"].iloc[i].split())

table_28["data_document_id"]="1359461"
table_28["data_document_filename"]="DCPS_49_i.pdf"
table_28["doc_date"]="2004"
table_28["raw_category"]=""
table_28["cat_code"]=""
table_28["description_cpcat"]=""
table_28["cpcat_code"]=""
table_28["cpcat_sourcetype"]="ACToR Assays and Lists"

table_28.to_csv("DCPS_49_table_28.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 29
tables=read_pdf("document_1359461.pdf", pages="47,48", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_29=pd.concat([tables[1],tables[2]], ignore_index=True)
table_29["raw_chem_name"]=table_29.iloc[:,0]
table_29["raw_cas"]=table_29.iloc[:,1]
table_29=table_29.loc[table_29["raw_cas"]!= "CAS no."]
table_29=table_29.reset_index()
table_29=table_29[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_29)):
    table_29["raw_chem_name"].iloc[i]=table_29["raw_chem_name"].iloc[i].lower().strip()
    table_29["raw_chem_name"].iloc[i]=clean(table_29["raw_chem_name"].iloc[i])
    if len(table_29["raw_chem_name"].iloc[i].split())>1:
        table_29["raw_chem_name"].iloc[i]=" ".join(table_29["raw_chem_name"].iloc[i].split())

table_29["data_document_id"]="1359461"
table_29["data_document_filename"]="DCPS_49_j.pdf"
table_29["doc_date"]="2004"
table_29["raw_category"]=""
table_29["cat_code"]=""
table_29["description_cpcat"]=""
table_29["cpcat_code"]=""
table_29["cpcat_sourcetype"]="ACToR Assays and Lists"

table_29.to_csv("DCPS_49_table_29.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
