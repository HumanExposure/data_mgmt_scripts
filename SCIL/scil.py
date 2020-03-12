#lkoval
#3-12-20

import pandas as pd
import os
from tabula import read_pdf
import string

os.chdir("//home//lkoval//FUse")

#tabula reads in pages with slightly different format so read all pages individually instead of together
pages=read_pdf("Safer Chemical Ingredients List _ Safer Choice _ US EPA.pdf", pages="3-76", multiple_tables=True, lattice=True)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #clean function to remove non-printable characters

#concat tables from all pages together
data=pd.DataFrame()
for table in pages:
    data=pd.concat([data,table], ignore_index=True)

#keep columns with any relevant data
data=data[[1,2,3,4,5]]

#most cas numbers were in column 2 but some where in column 3 instead. Move all cas in 3 to 2. Same for functional use with columns 4 and 5.
data.loc[pd.isnull(data[3])==False, [2]]=data[3]
data.loc[pd.isnull(data[5])==False, [4]]=data[5]

#keep the raw_chem_name, raw_cas, and report_funcuse columns and assign the name to the number
data=data[[1,2,4]]
data=data.rename(columns={1:"raw_chem_name",2:"raw_cas",4:"report_funcuse"})
data=data.dropna(how="all")

#remove return carriages for when cas and functional use are on multiple lines on the original document
data.raw_cas=data.raw_cas.str.replace("\r","")
data.report_funcuse=data.report_funcuse.str.replace("\r"," ")

#remove additional comments on chemicals, remove return carriages from chemical names, remove headers from the top of each page, and remove non printable characters
data.loc[data.raw_chem_name.str.contains("*", regex=False), ["raw_chem_name"]]=data.raw_chem_name.str.split("*", expand=True)[0]
data.raw_chem_name=data.raw_chem_name.str.replace("\r","")
data=data.loc[data.raw_cas.str.contains("[a-zA-Z]")==False]
data.raw_chem_name=data.raw_chem_name.apply(clean)

data["data_document_id"]="1512353"
data["data_document_filename"]="Safer Chemical Ingredients List _ Safer Choice _ US EPA.pdf"
data["doc_date"]="3/4/2020"
data["raw_category"]=""
data["cat_code"]=""
data["description_cpcat"]=""
data["cpcat_sourcetype"]=""
data["component"]=""

data=data[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]

data.to_csv("scil.csv", index=False)
