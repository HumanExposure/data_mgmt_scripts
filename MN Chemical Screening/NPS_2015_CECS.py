import os
import pandas as pd
from tabula import read_pdf


os.chdir("//home//lkoval//MN")

#read in data
data=read_pdf("VanderMeulen_2015_CECsSWinNPs.pdf", pages="51-62", lattice=False)
data=data.rename(columns={"Unnamed: 0": "site_id","Unnamed: 2": "raw_chem_name","Unnamed: 3": "raw_cas"})
data=data[["site_id","raw_chem_name","raw_cas"]]
data=data.loc[data.raw_chem_name!="Analyte"]
data=data.drop_duplicates()


#source surface water at site ID "coldwater spring" and IDs starting with "UM883"
source_sw=data.loc[((pd.isnull(data.site_id)) & (pd.isnull(data.raw_cas)==False)) | (data.site_id.str.contains("^UM883"))]
source_sw=source_sw[["raw_chem_name","raw_cas"]].drop_duplicates()

#no source surface water at all other sites starting with "UM"
ns_sw=data.loc[((pd.isnull(data.site_id)==False) & (data.site_id.str.contains("^UM883")==False)) | ((pd.isnull(data.site_id)) & (pd.isnull(data.raw_cas)))]
ns_sw=ns_sw.dropna(subset=["raw_chem_name","raw_cas"], how="all")
ns_sw.loc[pd.isnull(ns_sw.raw_chem_name),["raw_chem_name"]]="10,11-dihydro-10-hydroxycarbamazepine"
ns_sw=ns_sw.loc[pd.isnull(ns_sw.raw_cas)==False]
ns_sw=ns_sw[["raw_chem_name","raw_cas"]].drop_duplicates()

#make dfs
source_sw["data_document_id"]="1511886"
source_sw["data_document_filename"]="VanderMeulen_2015_CECsSWinNPs_a.pdf"
source_sw["doc_date"]="2013-2014"
source_sw["raw_category"]=""
source_sw["cat_code"]=""
source_sw["description_cpcat"]=""
source_sw["cpcat_sourcetype"]=""
source_sw["report_funcuse"]=""
source_sw["component"]=""

ns_sw["data_document_id"]="1511887"
ns_sw["data_document_filename"]="VanderMeulen_2015_CECsSWinNPs_b.pdf"
ns_sw["doc_date"]="2013-2014"
ns_sw["raw_category"]=""
ns_sw["cat_code"]=""
ns_sw["description_cpcat"]=""
ns_sw["cpcat_sourcetype"]=""
ns_sw["report_funcuse"]=""
ns_sw["component"]=""


source_sw=source_sw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]
ns_sw=ns_sw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]


source_sw.to_csv("nps_2015_cecs_source_sw.csv", index=False)
ns_sw.to_csv("nps_2015_cecs_ns_sw.csv", index=False)
