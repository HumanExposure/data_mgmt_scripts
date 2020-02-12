import os
import pandas as pd
from tabula import read_pdf

os.chdir("//home//lkoval//MN")

#read in tables 3 & 4 (same chems, different sampling dates) separatley due to differneces in the number of columns
table_3=read_pdf("MPCA 2012 EAC Monitoring MN Lakes 2009_2011_a.pdf", pages="18-19", lattice=False)
table_3=table_3.rename(columns={"Unnamed: 0": "raw_chem_name"})
table_3=table_3.loc[~((table_3.raw_chem_name=="Compound") | (pd.isnull(table_3.raw_chem_name)))]

#drop columns that are matrix spike recovery percentages and not concentrations
table_3=table_3.drop(columns=["Site.2","Site.5","Site.8","Site.11"], axis=1)

table_3=table_3.iloc[:-6]
table_3["raw_chem_name"]=table_3["raw_chem_name"].str.strip().str.lower()

table_4=read_pdf("MPCA 2012 EAC Monitoring MN Lakes 2009_2011_a.pdf", pages="20-21", lattice=False)
table_4=table_4.rename(columns={"Unnamed: 0": "raw_chem_name"})
table_4=table_4.loc[~((table_4.raw_chem_name=="Compound") | (pd.isnull(table_4.raw_chem_name)))]
table_4=table_4.iloc[:-6]
table_4["raw_chem_name"]=table_4["raw_chem_name"].str.strip().str.lower()

#merge tables 3 & 4 on chemial name to get all concentrations from both sampling dates
all_data=table_3.merge(table_4, on="raw_chem_name", how="left")
all_data["detects"]=""

# set detects to False if concentrations for a chemicals are all "<.01" or all "<.05", else set detects to True
for i in range(0, len(all_data)):
    vals=all_data.iloc[i].values[1:-1]
    if all(elem==vals[0] for elem in vals):
        all_data.detects.iloc[i]=False
    else:
        all_data.detects.iloc[i]=True

#Only keep chemicals that were detected at least once
all_data=all_data.loc[all_data.detects==True]
all_data=all_data[["raw_chem_name"]]

#finish template
all_data["data_document_id"]="1511898"
all_data["data_document_filename"]="MPCA 2012 EAC Monitoring MN Lakes 2009_2011_b.pdf"
all_data["doc_date"]="February 2013"
all_data["raw_category"]=""
all_data["raw_cas"]=""
all_data["cat_code"]=""
all_data["description_cpcat"]=""
all_data["cpcat_sourcetype"]=""
all_data["report_funcuse"]=""
all_data["component"]=""

all_data=all_data[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]


all_data.to_csv("MPCA_2012_EAC_Mon_MN_lakes.csv", index=False)
