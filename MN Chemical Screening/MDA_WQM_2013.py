#lkoval
#11/12/19

import pandas as pd
from tabula import read_pdf
import os

os.chdir("//home//lkoval//MN")

#Extract chemicals detected in surface water MDA WQM 2014 Table 1
table_1_sw=read_pdf("MDA_2014_WQMReport.pdf", pages="22-25", lattice=True, pandas_options={"usecols":[0,1,2], "names":["raw_chem_name","report_funcuse","sw_detect"], "skiprows": lambda x: x<6 or x>220})
table_1_sw=table_1_sw.dropna(subset=["report_funcuse"])
table_1_sw=table_1_sw.loc[~table_1_sw.raw_chem_name.str.contains("Common Name", regex=False)]
table_1_sw=table_1_sw.loc[~pd.isnull(table_1_sw.sw_detect)]
table_1_sw=table_1_sw[["raw_chem_name","report_funcuse"]]

table_1_sw=table_1_sw.applymap(str.lower)

table_1_sw["data_document_id"]="1496300"
table_1_sw["data_document_filename"]="MDA_2014_WQMReport_a.pdf"
table_1_sw["doc_date"]="June 2015"
table_1_sw["raw_category"]=""
table_1_sw["raw_cas"]=""
table_1_sw["cat_code"]=""
table_1_sw["description_cpcat"]=""
table_1_sw["cpcat_code"]=""
table_1_sw["cpcat_sourcetype"]=""


table_1_sw=table_1_sw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]
table_1_sw.to_csv("MDA_2014_WQM_SW.csv", index=False)

#Extract chemicals detected in groundwater MDA WQM 2014 Table 1
table_1_gw=read_pdf("MDA_2014_WQMReport.pdf", pages="22-25", lattice=True, pandas_options={"usecols":[0,1,3], "names":["raw_chem_name","report_funcuse","gw_detect"], "skiprows": lambda x: x<6 or x>220})
table_1_gw=table_1_gw.dropna(subset=["report_funcuse"])
table_1_gw=table_1_gw.loc[~table_1_gw.raw_chem_name.str.contains("Common Name", regex=False)]
table_1_gw=table_1_gw.loc[~pd.isnull(table_1_gw.gw_detect)]
table_1_gw=table_1_gw[["raw_chem_name","report_funcuse"]]

table_1_gw=table_1_gw.applymap(str.lower)

table_1_gw["data_document_id"]="1496301"
table_1_gw["data_document_filename"]="MDA_2014_WQMReport_b.pdf"
table_1_gw["doc_date"]="June 2015"
table_1_gw["raw_category"]=""
table_1_gw["raw_cas"]=""
table_1_gw["cat_code"]=""
table_1_gw["description_cpcat"]=""
table_1_gw["cpcat_code"]=""
table_1_gw["cpcat_sourcetype"]=""

table_1_gw=table_1_gw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]
table_1_gw.to_csv("MDA_2014_WQM_GW.csv", index=False)

