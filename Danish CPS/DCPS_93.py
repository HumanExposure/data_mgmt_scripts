#Lauren Koval
#4/17/19


from tabula import read_pdf
import pandas as pd
import string


#Extract tables 2.3, 2.5, 2.6, 2.7, & 2.8 as pandas dfs using tabula


#Table 2.3 Extraction
tables=read_pdf("document_1372134.pdf", pages="31,32", multiple_tables= True, lattice=True, pandas_options={'header': None})
table_2_3=pd.concat([tables[0],tables[1]], ignore_index=True)
table_2_3["raw_chem_name"]=table_2_3.iloc[:,0]
table_2_3["raw_cas"]=table_2_3.iloc[:,1]
table_2_3=table_2_3.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_2_3=table_2_3.loc[table_2_3["raw_chem_name"]!= "Identification"]
table_2_3=table_2_3.reset_index()
table_2_3=table_2_3[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_2_3)):
    if len(table_2_3["raw_chem_name"].iloc[i].split()) > 1:
        table_2_3["raw_chem_name"].iloc[i]=" ".join(table_2_3["raw_chem_name"].iloc[i].split())
    table_2_3["raw_chem_name"].iloc[i]=clean(table_2_3["raw_chem_name"].iloc[i])
    table_2_3["raw_chem_name"].iloc[i]=table_2_3["raw_chem_name"].iloc[i].replace(",", "_")
    table_2_3["raw_chem_name"].iloc[i]=table_2_3["raw_chem_name"].iloc[i].strip().lower()

table_2_3=table_2_3.drop_duplicates()
table_2_3=table_2_3.reset_index()
table_2_3=table_2_3[["raw_chem_name", "raw_cas"]]

table_2_3["data_document_id"]="1372134"
table_2_3["data_document_filename"]="DCPS_93_a.pdf"
table_2_3["doc_date"]="2008"
table_2_3["raw_category"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_3.to_csv("dcps_93_table_2_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 2.5 Extraction
tables=read_pdf("document_1372135.pdf", pages="33", multiple_tables= True, lattice=True, pandas_options={'header': None})
table_2_5=tables[1]
table_2_5["raw_chem_name"]=table_2_5.iloc[:,0]
table_2_5["raw_cas"]=table_2_5.iloc[:,1]
table_2_5=table_2_5.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_2_5=table_2_5.loc[table_2_5["raw_chem_name"]!= "Identification"]
table_2_5=table_2_5.reset_index()
table_2_5=table_2_5[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[i]=clean(table_2_5["raw_chem_name"].iloc[i])
    table_2_5["raw_chem_name"].iloc[i]=table_2_5["raw_chem_name"].iloc[i].replace(",", "_")
    table_2_5["raw_chem_name"].iloc[i]=table_2_5["raw_chem_name"].iloc[i].strip().lower()

table_2_5=table_2_5.drop_duplicates()
table_2_5=table_2_5.reset_index()
table_2_5=table_2_5[["raw_chem_name", "raw_cas"]]


table_2_5["data_document_id"]="1372135"
table_2_5["data_document_filename"]="DCPS_93_b.pdf"
table_2_5["doc_date"]="2008"
table_2_5["raw_category"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_5.to_csv("dcps_93_table_2_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 2.6 Extraction
tables=read_pdf("document_1372136.pdf", pages="33", multiple_tables= True, lattice=True, pandas_options={'header': None})
table_2_6=tables[2]
table_2_6["raw_chem_name"]=table_2_6.iloc[:,0]
table_2_6["raw_cas"]=table_2_6.iloc[:,1]
table_2_6=table_2_6.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_2_6=table_2_6.loc[table_2_6["raw_chem_name"]!= "Identification"]
table_2_6=table_2_6.reset_index()
table_2_6=table_2_6[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_2_6)):
    table_2_6["raw_chem_name"].iloc[i]=clean(table_2_6["raw_chem_name"].iloc[i])
    table_2_6["raw_chem_name"].iloc[i]=table_2_6["raw_chem_name"].iloc[i].replace(",", "_")
    table_2_6["raw_chem_name"].iloc[i]=table_2_6["raw_chem_name"].iloc[i].strip().lower()

table_2_6=table_2_6.drop_duplicates()
table_2_6=table_2_6.reset_index()
table_2_6=table_2_6[["raw_chem_name", "raw_cas"]]


table_2_6["data_document_id"]="1372136"
table_2_6["data_document_filename"]="DCPS_93_c.pdf"
table_2_6["doc_date"]="2008"
table_2_6["raw_category"]=""
table_2_6["cat_code"]=""
table_2_6["description_cpcat"]=""
table_2_6["cpcat_code"]=""
table_2_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_6.to_csv("dcps_93_table_2_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 2.7 Extraction
tables=read_pdf("document_1372137.pdf", pages="34", multiple_tables= True, lattice=True, pandas_options={'header': None})
table_2_7=pd.concat([tables[0],tables[1]], ignore_index=True)
table_2_7["raw_chem_name"]=table_2_7.iloc[:,0]
table_2_7["raw_cas"]=table_2_7.iloc[:,1]
table_2_7=table_2_7.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_2_7=table_2_7.loc[table_2_7["raw_chem_name"]!= "Identification"]
table_2_7=table_2_7.reset_index()
table_2_7=table_2_7[["raw_chem_name", "raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_2_7)):
    if len(table_2_7["raw_chem_name"].iloc[i].split()) > 1:
        table_2_7["raw_chem_name"].iloc[i]=" ".join(table_2_7["raw_chem_name"].iloc[i].split())
    table_2_7["raw_chem_name"].iloc[i]=clean(table_2_7["raw_chem_name"].iloc[i])
    table_2_7["raw_chem_name"].iloc[i]=table_2_7["raw_chem_name"].iloc[i].replace(",", "_")
    table_2_7["raw_chem_name"].iloc[i]=table_2_7["raw_chem_name"].iloc[i].strip().lower()

table_2_7=table_2_7.drop_duplicates()
table_2_7=table_2_7.reset_index()
table_2_7=table_2_7[["raw_chem_name", "raw_cas"]]

table_2_7["data_document_id"]="1372137"
table_2_7["data_document_filename"]="DCPS_93_d.pdf"
table_2_7["doc_date"]="2008"
table_2_7["raw_category"]=""
table_2_7["cat_code"]=""
table_2_7["description_cpcat"]=""
table_2_7["cpcat_code"]=""
table_2_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_7.to_csv("dcps_93_table_2_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 2.8 Extraction
tables=read_pdf("document_1372138.pdf", pages="34", multiple_tables= True, lattice=True, pandas_options={'header': None})
table_2_8=tables[2]
table_2_8["raw_chem_name"]=table_2_8.iloc[:,0]
table_2_8["raw_cas"]=table_2_8.iloc[:,1]
table_2_8=table_2_8.loc[table_2_8["raw_chem_name"]!= "Identification"]
table_2_8=table_2_8.dropna()
table_2_8=table_2_8.reset_index()
table_2_8=table_2_8[["raw_chem_name", "raw_cas"]]
table_2_8["raw_chem_name"].iloc[0]=table_2_8["raw_chem_name"].iloc[0].strip().lower()

table_2_8["data_document_id"]="1372138"
table_2_8["data_document_filename"]="DCPS_93_e.pdf"
table_2_8["doc_date"]="2008"
table_2_8["raw_category"]=""
table_2_8["cat_code"]=""
table_2_8["description_cpcat"]=""
table_2_8["cpcat_code"]=""
table_2_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_8.to_csv("dcps_93_table_2_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
