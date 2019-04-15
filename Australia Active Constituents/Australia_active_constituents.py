#Lauren Koval
#4/15/19

from tabula import read_pdf
import pandas as pd
import string

#Read in all pages of the table from Australia Record of Approved Active Constituents as pandas df with tabula-py
table=read_pdf("document_1370040.pdf", pages="all", lattice=True, pandas_options={'header': None})

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

#Remove column headers, duplicates, and other irrelevant info.Add rest of information
table=table.iloc[4:]
table=table.loc[table["raw_chem_name"]!= "common name"]
table=table.drop_duplicates()
table=table.reset_index()
table=table[["raw_chem_name"]]

table["data_document_id"]="1370040"
table["data_document_filename"]="AU_APVMA_Approved_Actives.pdf"
table["doc_date"]="19/02/2014"
table["raw_category"]="raw category"
table["raw_cas"]=""
table["cat_code"]="ACToR Assays"
table["description_cpcat"]="cpcat description"
table["cpcat_code"]="cpcat code"
table["cpcat_sourcetype"]="ACToR Assays and Lists"

#write to csv
table.to_csv("Aus_active_constituents.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
