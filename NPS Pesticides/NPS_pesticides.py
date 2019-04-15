#Lauren Koval
#4/15/19

from tabula import read_pdf
import pandas as pd
import string

#Read in all pages of the table from NPS Conserve O Gram - Physical Properties and Health Effects of Pesticides Used on National Park Service Collections as pandas table with tabula-py
tables=read_pdf("document_1370043.pdf", pages="2-10", multiple_tables=True, lattice=True, pandas_options={'header': None})

#list of all the indices of elements of tables that are relevant
good_indices=[0,2,3,4,6,7,8,9,10,11,12]
good_tables=[]
for i in good_indices:
    good_tables.append(tables[i])

#Concatenate useful elements into single df
df=pd.concat(good_tables, ignore_index=True)
df["raw_chem_name"]=df.iloc[:,0]
df=df.dropna(subset=["raw_chem_name"])
df=df.reset_index()
df=df[["raw_chem_name"]]

#Clean table, replace commas with underscores, deal with spacing issues
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0,len(df)):
    if len(df["raw_chem_name"].iloc[j].split()) > 1:
        df["raw_chem_name"].iloc[j]=" ".join(df["raw_chem_name"].iloc[j].split())
    df["raw_chem_name"].iloc[j]=clean(df["raw_chem_name"].iloc[j])
    df["raw_chem_name"].iloc[j]=df["raw_chem_name"].iloc[j].replace(",", "_")
    df["raw_chem_name"].iloc[j]=df["raw_chem_name"].iloc[j].strip().lower()

#Remove column headers and add rest of information
df=df.loc[df["raw_chem_name"]!= "pesticide"]
df=df.drop_duplicates()
df=df.reset_index()
df=df[["raw_chem_name"]]

df["data_document_id"]="1370043"
df["data_document_filename"]="DOI_NPS_PestProperties.pdf"
df["doc_date"]="September 2001"
df["raw_category"]="raw category"
df["raw_cas"]=""
df["cat_code"]="ACToR Assays"
df["description_cpcat"]="cpcat description"
df["cpcat_code"]="cpcat code"
df["cpcat_sourcetype"]="ACToR Assays and Lists"

#write to csv
df.to_csv("NPS_pesticides.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
