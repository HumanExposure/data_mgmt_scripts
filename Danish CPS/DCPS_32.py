from tabula import read_pdf
import pandas as pd
import string

#Extract tables 2.10, 2.11, 3.2, 3.3, 3.5, 3.7, 3.8, 3.9, 3.10 as pandas dfs using tabula

#Table 2.10 Extraction
table_2_10=read_pdf("document_1372153.pdf", pages="31", lattice=True, pandas_options={'header': None})
table_2_10["raw_chem_name"]=table_2_10.iloc[:,0]
table_2_10["raw_cas"]=table_2_10.iloc[:,1]
table_2_10=table_2_10.loc[table_2_10["raw_chem_name"]!= "Substance"]
table_2_10=table_2_10.reset_index()
table_2_10=table_2_10[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_2_10)):
    table_2_10["raw_chem_name"].iloc[i]=clean(table_2_10["raw_chem_name"].iloc[i])
    table_2_10["raw_chem_name"].iloc[i]=table_2_10["raw_chem_name"].iloc[i].replace(",", "_")
    table_2_10["raw_chem_name"].iloc[i]=table_2_10["raw_chem_name"].iloc[i].strip().lower()

table_2_10["data_document_id"]="1372153"
table_2_10["data_document_filename"]="DCPS_32_a.pdf"
table_2_10["doc_date"]="2003"
table_2_10["raw_category"]="raw category"
table_2_10["cat_code"]="ACToR Assays"
table_2_10["description_cpcat"]="cpcat description"
table_2_10["cpcat_code"]="cpcat code"
table_2_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_10.to_csv("dcps_32_table_2_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 2.11 Extraction
table_2_11=read_pdf("document_1372154.pdf", pages="32", lattice=True, pandas_options={'header': None})

table_2_11["raw_chem_name"]=table_2_11.iloc[:,0]
table_2_11["raw_cas"]=table_2_11.iloc[:,1]
table_2_11=table_2_11.loc[table_2_11["raw_chem_name"]!= "Substance"]
table_2_11=table_2_11.reset_index()
table_2_11=table_2_11[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_2_11)):
    table_2_11["raw_chem_name"].iloc[i]=clean(table_2_11["raw_chem_name"].iloc[i])
    table_2_11["raw_chem_name"].iloc[i]=table_2_11["raw_chem_name"].iloc[i].replace(",", "_")
    table_2_11["raw_chem_name"].iloc[i]=table_2_11["raw_chem_name"].iloc[i].strip().lower()

table_2_11["data_document_id"]="1372154"
table_2_11["data_document_filename"]="DCPS_32_b.pdf"
table_2_11["doc_date"]="2003"
table_2_11["raw_category"]="raw category"
table_2_11["cat_code"]="ACToR Assays"
table_2_11["description_cpcat"]="cpcat description"
table_2_11["cpcat_code"]="cpcat code"
table_2_11["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_11.to_csv("dcps_32_table_2_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.2 Extraction
table_3_2=read_pdf("document_1372155.pdf", pages="43", lattice=True, pandas_options={'header': None})

table_3_2["raw_chem_name"]=table_3_2.iloc[:,0]
table_3_2["raw_cas"]=table_3_2.iloc[:,1]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!= "Substance"]
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[i]=clean(table_3_2["raw_chem_name"].iloc[i])
    table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i].strip().lower()
    if len(table_3_2["raw_chem_name"].iloc[i].split()) > 1:
        table_3_2["raw_chem_name"].iloc[i]=" ".join(table_3_2["raw_chem_name"].iloc[i].split())
    if len(table_3_2["raw_cas"].iloc[i].split()) > 1:
        table_3_2["raw_cas"].iloc[i]="".join(table_3_2["raw_cas"].iloc[i].split())

table_3_2["data_document_id"]="1372155"
table_3_2["data_document_filename"]="DCPS_32_c.pdf"
table_3_2["doc_date"]="2003"
table_3_2["raw_category"]="raw category"
table_3_2["cat_code"]="ACToR Assays"
table_3_2["description_cpcat"]="cpcat description"
table_3_2["cpcat_code"]="cpcat code"
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_32_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.3 Extraction
table_3_3=read_pdf("document_1372156.pdf", pages="44", lattice=True, pandas_options={'header': None})

table_3_3["raw_chem_name"]=table_3_3.iloc[:,0]
table_3_3["raw_cas"]=table_3_3.iloc[:,1]
table_3_3=table_3_3.loc[table_3_3["raw_chem_name"]!= "Substance"]
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[i]=clean(table_3_3["raw_chem_name"].iloc[i])
    table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i].strip().lower()
    if len(table_3_3["raw_chem_name"].iloc[i].split()) > 1:
        table_3_3["raw_chem_name"].iloc[i]=" ".join(table_3_3["raw_chem_name"].iloc[i].split())
    if table_3_3["raw_chem_name"].iloc[i].endswith("1"):
        table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i][:-1]

table_3_3["data_document_id"]="1372156"
table_3_3["data_document_filename"]="DCPS_32_d.pdf"
table_3_3["doc_date"]="2003"
table_3_3["raw_category"]="raw category"
table_3_3["cat_code"]="ACToR Assays"
table_3_3["description_cpcat"]="cpcat description"
table_3_3["cpcat_code"]="cpcat code"
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("dcps_32_table_3_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.5 Extraction
table_3_5=read_pdf("document_1372157.pdf", pages="46", lattice=True, pandas_options={'header': None})

table_3_5["raw_chem_name"]=table_3_5.iloc[:,0]
table_3_5["raw_cas"]=table_3_5.iloc[:,1]
table_3_5=table_3_5.loc[table_3_5["raw_chem_name"]!= "Substance"]
table_3_5=table_3_5.reset_index()
table_3_5=table_3_5[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_5)):
    table_3_5["raw_chem_name"].iloc[i]=clean(table_3_5["raw_chem_name"].iloc[i])
    table_3_5["raw_chem_name"].iloc[i]=table_3_5["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_5["raw_chem_name"].iloc[i]=table_3_5["raw_chem_name"].iloc[i].strip().lower()
    if len(table_3_5["raw_cas"].iloc[i].split()) > 1:
        table_3_5["raw_cas"].iloc[i]="".join(table_3_5["raw_cas"].iloc[i].split())
    if table_3_5["raw_chem_name"].iloc[i].endswith("1"):
        table_3_5["raw_chem_name"].iloc[i]=table_3_5["raw_chem_name"].iloc[i][:-1]

table_3_5["data_document_id"]="1372157"
table_3_5["data_document_filename"]="DCPS_32_e.pdf"
table_3_5["doc_date"]="2003"
table_3_5["raw_category"]="raw category"
table_3_5["cat_code"]="ACToR Assays"
table_3_5["description_cpcat"]="cpcat description"
table_3_5["cpcat_code"]="cpcat code"
table_3_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_5.to_csv("dcps_32_table_3_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.7 Extraction
table_3_7=read_pdf("document_1372158.pdf", pages="49", lattice=True, pandas_options={'header': None})

table_3_7["raw_chem_name"]=table_3_7.iloc[:,0]
table_3_7["raw_cas"]=table_3_7.iloc[:,1]
table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!= "Substance"]
table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_7)):
    table_3_7["raw_chem_name"].iloc[i]=clean(table_3_7["raw_chem_name"].iloc[i])
    table_3_7["raw_chem_name"].iloc[i]=table_3_7["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_7["raw_chem_name"].iloc[i]=table_3_7["raw_chem_name"].iloc[i].strip().lower()
    if len(table_3_7["raw_cas"].iloc[i].split()) > 1:
        table_3_7["raw_cas"].iloc[i]="".join(table_3_7["raw_cas"].iloc[i].split())
    if len(table_3_7["raw_chem_name"].iloc[i].split())>1:
        table_3_7["raw_chem_name"].iloc[i]=" ".join(table_3_7["raw_chem_name"].iloc[i].split())

table_3_7["data_document_id"]="1372158"
table_3_7["data_document_filename"]="DCPS_32_f.pdf"
table_3_7["doc_date"]="2003"
table_3_7["raw_category"]="raw category"
table_3_7["cat_code"]="ACToR Assays"
table_3_7["description_cpcat"]="cpcat description"
table_3_7["cpcat_code"]="cpcat code"
table_3_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_7.to_csv("dcps_32_table_3_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.8 Extraction
table_3_8=read_pdf("document_1372159.pdf", pages="50", lattice=True, pandas_options={'header': None})

table_3_8["raw_chem_name"]=table_3_8.iloc[:,0]
table_3_8["raw_cas"]=table_3_8.iloc[:,1]
table_3_8=table_3_8.loc[table_3_8["raw_chem_name"]!= "Substance"]
table_3_8=table_3_8.reset_index()
table_3_8=table_3_8[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_8)):
    table_3_8["raw_chem_name"].iloc[i]=clean(table_3_8["raw_chem_name"].iloc[i])
    table_3_8["raw_chem_name"].iloc[i]=table_3_8["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_8["raw_chem_name"].iloc[i]=table_3_8["raw_chem_name"].iloc[i].strip().lower()

table_3_8["data_document_id"]="1372159"
table_3_8["data_document_filename"]="DCPS_32_g.pdf"
table_3_8["doc_date"]="2003"
table_3_8["raw_category"]="raw category"
table_3_8["cat_code"]="ACToR Assays"
table_3_8["description_cpcat"]="cpcat description"
table_3_8["cpcat_code"]="cpcat code"
table_3_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_8.to_csv("dcps_32_table_3_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 3.9 Extraction
table_3_9=read_pdf("document_1372160.pdf", pages="51", multiple_tables=True, lattice=True, pandas_options={'header': None})
table_3_9=table_3_9[0]
table_3_9["raw_chem_name"]=table_3_9.iloc[:,0]
table_3_9["raw_cas"]=table_3_9.iloc[:,1]
table_3_9=table_3_9.loc[table_3_9["raw_chem_name"]!= "Substance"]
table_3_9=table_3_9.reset_index()
table_3_9=table_3_9[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_9)):
    table_3_9["raw_chem_name"].iloc[i]=clean(table_3_9["raw_chem_name"].iloc[i])
    table_3_9["raw_chem_name"].iloc[i]=table_3_9["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_9["raw_chem_name"].iloc[i]=table_3_9["raw_chem_name"].iloc[i].strip().lower()

table_3_9["data_document_id"]="1372160"
table_3_9["data_document_filename"]="DCPS_32_h.pdf"
table_3_9["doc_date"]="2003"
table_3_9["raw_category"]="raw category"
table_3_9["cat_code"]="ACToR Assays"
table_3_9["description_cpcat"]="cpcat description"
table_3_9["cpcat_code"]="cpcat code"
table_3_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_9.to_csv("dcps_32_table_3_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3.10 Extraction
table_3_10=read_pdf("document_1372161.pdf", pages="51", multiple_tables=True, lattice=True, pandas_options={'header': None})
table_3_10=table_3_10[1]
table_3_10["raw_chem_name"]=table_3_10.iloc[:,0]
table_3_10["raw_cas"]=table_3_10.iloc[:,2]
table_3_10=table_3_10.loc[table_3_10["raw_chem_name"]!= "Substance"]
table_3_10=table_3_10.reset_index()
table_3_10=table_3_10[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_10)):
    table_3_10["raw_chem_name"].iloc[i]=clean(table_3_10["raw_chem_name"].iloc[i])
    table_3_10["raw_chem_name"].iloc[i]=table_3_10["raw_chem_name"].iloc[i].replace(",", "_")
    table_3_10["raw_chem_name"].iloc[i]=table_3_10["raw_chem_name"].iloc[i].strip().lower()
    if len(table_3_10["raw_cas"].iloc[i].split()) > 1:
        table_3_10["raw_cas"].iloc[i]="".join(table_3_10["raw_cas"].iloc[i].split())


table_3_10["data_document_id"]="1372161"
table_3_10["data_document_filename"]="DCPS_32_i.pdf"
table_3_10["doc_date"]="2003"
table_3_10["raw_category"]="raw category"
table_3_10["cat_code"]="ACToR Assays"
table_3_10["description_cpcat"]="cpcat description"
table_3_10["cpcat_code"]="cpcat code"
table_3_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_10.to_csv("dcps_32_table_3_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
