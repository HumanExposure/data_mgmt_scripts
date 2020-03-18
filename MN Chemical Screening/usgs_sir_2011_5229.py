#lkoval
#3-17-20

from tabula import read_pdf
import pandas as pd
import os

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//MN//USGS SIR2011-5229 WQ Asmt Aquifers Northern Midwest")

#Reads in and extracts chemicals from tables 12, 15, & 20 which range from 1995/1996-2007
early=read_pdf("WQ Asmt Aquifers Northern Midwest_a.pdf", pages="78,92,116", dtype=str, pandas_options={"usecols":[0,2]})
early=early.rename(columns={"Unnamed: 0":"raw_chem_name", "Unnamed: 2":"detects"})
early=early.dropna(subset=["raw_chem_name"])
early=early.loc[(early.detects!="Number") & (early.raw_chem_name!="Trace element")]
early=early.reset_index()
early=early[["raw_chem_name","detects"]]

#fixchem names that were split on multiple lines
for i in range(len(early)):
    if pd.isnull(early.detects.iloc[i]):
        early.raw_chem_name.iloc[i-1]=early.raw_chem_name.iloc[i-1]+" "+early.raw_chem_name[i]

#keep only detected chemicals
early=early.dropna()
early=early.loc[(early.detects.str.contains("[0-9]")) & (pd.to_numeric(early.detects, errors="coerce")>0)]
early=early[["raw_chem_name"]]

#fill in rest of template
early["data_document_id"]="1512363"
early["data_document_filename"]="WQ Asmt Aquifers Northern Midwest_a.pdf"
early["doc_date"]="2011"
early["raw_category"]=""
early["raw_cas"]=""
early["cat_code"]=""
early["description_cpcat"]=""
early["cpcat_code"]=""
early["cpcat_sourcetype"]=""
early["report_funcuse"]=""

early=early[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]

early.to_csv("USGS_SIR2011_5229_tables_12_15_20.csv", index=False)


#read and extract chemicals and reported functional use from tables 22 and 25. Tables had to be adjusted individually before being concatenated together
later_tabs=read_pdf("WQ Asmt Aquifers Northern Midwest_b.pdf", pages="123,128", dtype=str, multiple_tables=True)

tab_20=later_tabs[1].iloc[:,[0,3]].rename(columns={0:"raw_chem_name",3:"detects"})
tab_20["report_funcuse"]=""
tab_20.loc[pd.isnull(tab_20.raw_chem_name)==False, ["report_funcuse"]]=tab_20.raw_chem_name.str.split(" ", n=1,expand=True)[1]
tab_20.loc[pd.isnull(tab_20.raw_chem_name)==False, ["raw_chem_name"]]=tab_20.raw_chem_name.str.split(" ", expand=True)[0]

tab_25=later_tabs[2].iloc[:,[0,2,4]].rename(columns={0:"raw_chem_name",2:"report_funcuse",4:"detects"})

later=pd.concat([tab_20,tab_25], ignore_index=True)
later=later[["raw_chem_name","detects","report_funcuse"]]
later=later.dropna(subset=["raw_chem_name"])
later=later.loc[(later.raw_chem_name!="Total") & (later.raw_chem_name!="Pesticide")]
later=later.reset_index()
later=later[["raw_chem_name","detects","report_funcuse"]]

#fix chemical names that were on multiple lines
for i in range(len(later)):
    if pd.isnull(later.detects.iloc[i]):
        later.raw_chem_name.iloc[i-1]=later.raw_chem_name.iloc[i-1]+" "+later.raw_chem_name[i]

later=later.dropna(subset=["detects"])

#tabula read in the numer of detects and the detection percentage in the same column. keep on the number of detects
later.detects=later.detects.str.split(" ", expand=True)[0]

#only keep chemicals that were detected
later=later.loc[pd.to_numeric(later.detects)>0]
later=later[["raw_chem_name", "report_funcuse"]]

#fill in rest of template
later["data_document_id"]="1512364"
later["data_document_filename"]="WQ Asmt Aquifers Northern Midwest_b.pdf"
later["doc_date"]="2011"
later["raw_category"]=""
later["raw_cas"]=""
later["cat_code"]=""
later["description_cpcat"]=""
later["cpcat_code"]=""
later["cpcat_sourcetype"]=""

later=later[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]

later.to_csv("USGS_SIR2011_5229_tables_22_25.csv", index=False)
