#Lauren Koval
#4/15/19

from tabula import read_pdf
import pandas as pd
import string

#Read in all pages of the table from Fighting Rare Diseases: 22 New Orphan Drugs in Five Years as pandas table with tabula-py
table=read_pdf("document_1370046.pdf", pages="3-7", lattice=True, pandas_options={'header': None})

#gets the chemical name column
table["raw_chem_name"]=table.iloc[:,0]
table=table.dropna(subset=["raw_chem_name"])
table=table.reset_index()
table=table[["raw_chem_name"]]

#Clean table, replace commas with underscores, deal with spacing issues
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table)):
    if len(table["raw_chem_name"].iloc[i].split()) > 1:
        table["raw_chem_name"].iloc[i]=" ".join(table["raw_chem_name"].iloc[i].split())
    table["raw_chem_name"].iloc[i]=clean(table["raw_chem_name"].iloc[i])
    table["raw_chem_name"].iloc[i]=table["raw_chem_name"].iloc[i].replace(",", "_")
    table["raw_chem_name"].iloc[i]=table["raw_chem_name"].iloc[i].strip().lower()

#Remove column headers and add rest of information
table=table.loc[table["raw_chem_name"]!= "medicinal product"]

table["data_document_id"]="1370046"
table["data_document_filename"]="EU_Orphan_Drugs_2005.pdf"
table["doc_date"]="26 June 2006"
table["raw_category"]="raw category"
table["raw_cas"]=""
table["cat_code"]="ACToR Assays"
table["description_cpcat"]="cpcat description"
table["cpcat_code"]="cpcat code"
table["cpcat_sourcetype"]="ACToR Assays and Lists"

#write to csv
table.to_csv("EU_orphan_drugs_2005.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
