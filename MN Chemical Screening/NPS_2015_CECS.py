import os
import pandas as pd
from tabula import read_pdf


os.chdir("//home//lkoval//MN")

data=read_pdf("VanderMeulen_2015_CECsSWinNPs.pdf", pages="51-62", lattice=False)
data=data.rename(columns={"Unnamed: 2": "raw_chem_name","Unnamed: 3": "raw_cas"})
data=data[["raw_chem_name","raw_cas"]]
data=data.dropna(how="all")
data=data.loc[data.raw_chem_name!="Analyte"]
data=data.drop_duplicates()


data["data_document_id"]="1509861"
data["data_document_filename"]="VanderMeulen_2015_CECsSWinNPs.pdf"
data["doc_date"]="2013-2014"
data["raw_category"]=""
data["cat_code"]=""
data["description_cpcat"]=""
data["cpcat_sourcetype"]=""
data["report_funcuse"]=""
data["component"]=""

data.loc[pd.isnull(data.raw_chem_name),["raw_chem_name"]]="10,11-dihydro-10-hydroxycarbamazepine"
data=data.loc[~(pd.isnull(data.raw_cas))]
data=data[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]
data.to_csv("nps_2015_cecs.csv", index=False)
