#lkoval
#11/12/19

import pandas as pd
from tabula import read_pdf
import os

os.chdir("//home//lkoval//MN")

#Extract chemicals detected in surface water MDA WQM 2012 Tables 1 & 2. Both contain the same information but used different detection methods which is irrelevant for our purposes, so tables were combined.

#read in pdfs and skip rows and columns without data then remove rows that aren't relevant. Only keep chemicals that were detected according the sw_detect column
tables=read_pdf("MDA_2012_WQMReport.pdf", pages="20-23", lattice=True, multiple_tables=True)
table_1_sw=pd.concat(tables[0:6], ignore_index=True).iloc[10:,]
table_1_sw=table_1_sw[[0,1,2,4,7]]
table_1_sw.columns=["raw_chem_name","report_funcuse","sw_detect","report_funcuse_2","sw_detect_2"]
table_1_sw.loc[(pd.isnull(table_1_sw.report_funcuse)==False) & (table_1_sw.report_funcuse.str.contains("[a-zA-Z]+\*")), ["raw_chem_name"]]=table_1_sw.report_funcuse
table_1_sw.loc[(pd.isnull(table_1_sw.report_funcuse)==False) & (table_1_sw.report_funcuse.str.contains("[a-zA-Z]+\*")), ["report_funcuse"]]=table_1_sw.report_funcuse_2
table_1_sw.loc[((pd.isnull(table_1_sw.report_funcuse)==False) & (table_1_sw.raw_chem_name.str.contains("[a-zA-Z]+\*"))) & (table_1_sw.sw_detect_2=="x"), ["sw_detect"]]=table_1_sw.sw_detect_2
table_1_sw.raw_chem_name=table_1_sw.raw_chem_name.str.strip("*")
table_1_sw=table_1_sw[["raw_chem_name","report_funcuse","sw_detect"]]
table_1_sw=table_1_sw.dropna(subset=["report_funcuse","raw_chem_name"])

table_1_sw_dif_format=tables[6].iloc[6:,]
table_1_sw_dif_format=table_1_sw_dif_format[[0,2,3]]
table_1_sw_dif_format.columns=["raw_chem_name","report_funcuse","sw_detect"]
table_1_sw_dif_format=table_1_sw_dif_format.dropna(subset=["report_funcuse"])

table_2_sw=tables[7].iloc[4:,]
table_2_sw=table_2_sw[[0,2,3]]
table_2_sw.columns=["raw_chem_name","report_funcuse","sw_detect"]

#combine tables 1 and 2
table_sw=pd.concat([table_1_sw,table_1_sw_dif_format,table_2_sw], ignore_index=True)
table_sw=table_sw[["raw_chem_name","report_funcuse"]].loc[~pd.isnull(table_sw.sw_detect)]

table_sw=table_sw.applymap(str.lower)


#fill in rest of factotum upload template
table_sw["data_document_id"]="1496307"
table_sw["data_document_filename"]="MDA_2012_WQMReport_a"
table_sw["doc_date"]="June 2013"
table_sw["raw_category"]=""
table_sw["raw_cas"]=""
table_sw["cat_code"]=""
table_sw["description_cpcat"]=""
table_sw["cpcat_code"]=""
table_sw["cpcat_sourcetype"]=""

table_sw=table_sw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]
table_sw.to_csv("MDA_2012_WQM_SW.csv", index=False)




#Extract chemicals detected in Groundwater MDA WQM 2012 Tables 1 & 2

tables=read_pdf("MDA_2012_WQMReport.pdf", pages="20-23", lattice=True, multiple_tables=True)
table_1_gw=pd.concat(tables[0:6], ignore_index=True).iloc[10:,]
table_1_gw=table_1_gw[[0,1,3,4,8]]
table_1_gw.columns=["raw_chem_name","report_funcuse","gw_detect","report_funcuse_2","gw_detect_2"]
table_1_gw.loc[(pd.isnull(table_1_gw.report_funcuse)==False) & (table_1_gw.report_funcuse.str.contains("[a-zA-Z]+\*")), ["raw_chem_name"]]=table_1_gw.report_funcuse
table_1_gw.loc[(pd.isnull(table_1_gw.report_funcuse)==False) & (table_1_gw.report_funcuse.str.contains("[a-zA-Z]+\*")), ["report_funcuse"]]=table_1_gw.report_funcuse_2
table_1_gw.loc[((pd.isnull(table_1_gw.report_funcuse)==False) & (table_1_gw.raw_chem_name.str.contains("[a-zA-Z]+\*"))) & (table_1_gw.gw_detect_2=="x"), ["gw_detect"]]=table_1_gw.gw_detect_2
table_1_gw.raw_chem_name=table_1_gw.raw_chem_name.str.strip("*")
table_1_gw=table_1_gw[["raw_chem_name","report_funcuse","gw_detect"]]
table_1_gw=table_1_gw.dropna(subset=["report_funcuse","raw_chem_name"])

table_1_gw_dif_format=tables[6].iloc[6:,]
table_1_gw_dif_format=table_1_gw_dif_format[[0,2,4]]
table_1_gw_dif_format.columns=["raw_chem_name","report_funcuse","gw_detect"]
table_1_gw_dif_format=table_1_gw_dif_format.dropna(subset=["report_funcuse"])

table_2_gw=tables[7].iloc[4:,]
table_2_gw=table_2_gw[[0,2,4]]
table_2_gw.columns=["raw_chem_name","report_funcuse","gw_detect"]

#combine tables 1 and 2
table_gw=pd.concat([table_1_gw,table_1_gw_dif_format,table_2_gw], ignore_index=True)
table_gw=table_gw.loc[~pd.isnull(table_gw.gw_detect)]
table_gw=table_gw[["raw_chem_name","report_funcuse"]].loc[table_gw.gw_detect!="na"]

table_gw=table_gw.applymap(str.lower)


#fill in rest of factotum upload template
table_gw["data_document_id"]="1496308"
table_gw["data_document_filename"]="MDA_2012_WQMReport_b"
table_gw["doc_date"]="June 2013"
table_gw["raw_category"]=""
table_gw["raw_cas"]=""
table_gw["cat_code"]=""
table_gw["description_cpcat"]=""
table_gw["cpcat_code"]=""
table_gw["cpcat_sourcetype"]=""

table_gw=table_gw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]
table_gw.to_csv("MDA_2012_WQM_GW.csv", index=False)
