#Lauren Koval
#4/15/19

from tabula import read_pdf
import pandas as pd
import string

#Read in all pages of the table in EU Pesticides Database-Active Substances as pandas df with tabula-py
tables=read_pdf("document_1370048.pdf", pages="all", multiple_tables=True, lattice=True, pandas_options={'header': None})

#keeps elements of tables that have relevant information
good_tables=[]
for i in range(0, len(tables)):
    if len(tables[i])!=1:
        good_tables.append(tables[i])

#concatenate all the relevant elements and only keep chemical name column
df=pd.concat(good_tables, ignore_index=True)
df["raw_chem_name"]=df.iloc[:,1]

#drop column header found on each page and any null values
indices_to_drop=[]
for j in range(0, len(df)):
    if "Name" in str(df["raw_chem_name"].iloc[j]):
        indices_to_drop.append(j)

df=df.drop(indices_to_drop)
df=df.dropna(subset=["raw_chem_name"])
df=df.reset_index()
df=df[["raw_chem_name"]]

#clean df, replace commas with underscores, deal with spacing issues
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for k in range(0, len(df)):
    df["raw_chem_name"].iloc[k]=clean(df["raw_chem_name"].iloc[k])
    df["raw_chem_name"].iloc[k]=df["raw_chem_name"].iloc[k].replace(",", "_")
    df["raw_chem_name"].iloc[k]=df["raw_chem_name"].iloc[k].strip().lower()
    if len(df["raw_chem_name"].iloc[k].split()) > 1:
        df["raw_chem_name"].iloc[k]=" ".join(df["raw_chem_name"].iloc[k].split())

#reset df index and add additional information
df=df.drop_duplicates()
df=df.reset_index()
df=df[["raw_chem_name"]]

df["data_document_id"]="1370048"
df["data_document_filename"]="Europa_Actives.pdf"
df["doc_date"]="2/6/2019"
df["raw_category"]="raw category"
df["raw_cas"]=""
df["cat_code"]="ACToR Assays"
df["description_cpcat"]="cpcat description"
df["cpcat_code"]="cpcat code"
df["cpcat_sourcetype"]="ACToR Assays and Lists"


#write df to csv
df.to_csv("EU_pest_active_db.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
