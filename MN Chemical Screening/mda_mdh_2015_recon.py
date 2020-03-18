#lkoval
#3-17-20

from tabula import read_pdf
import pandas as pd
import os

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//MN//MDA-MDH 2015 Recon Study Community Public Water Supply Wells")

tab_2=read_pdf("MDA-MDH 2015 Recon Study Community Public Water Supply Wells_a.pdf", pages="22", dtype=str, pandas_options={"usecols":[0,1,2]})
tab_2=tab_2.rename(columns={"Unnamed: 0":"raw_chem_name", "2010":"detfre10","2015":"detfre15"})
tab_2=tab_2.dropna()
tab_2=tab_2.loc[tab_2.detfre10!="Frequency"]
tab_2.detfre10=tab_2.detfre10.str.strip("%")
tab_2.detfre15=tab_2.detfre15.str.strip("%")

ten=tab_2[["raw_chem_name","detfre10"]]
ten=ten.loc[(ten.detfre10!="na")]
ten=ten.loc[pd.to_numeric(ten.detfre10)>0]

ten["ten_document_id"]="1512357"
ten["ten_document_filename"]="MDA-MDH 2015 Recon Study Community Public Water Supply Wells_a.pdf"
ten["doc_date"]="October 2016"
ten["raw_category"]=""
ten["raw_cas"]=""
ten["cat_code"]=""
ten["description_cpcat"]=""
ten["cpcat_code"]=""
ten["cpcat_sourcetype"]=""
ten["report_funcuse"]=""

ten=ten[["ten_document_id","ten_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]

ten.to_csv("MDA_MDH_2015_recon_table2_2010.csv", index=False)


fif=tab_2[["raw_chem_name","detfre15"]]
fif=fif.loc[(fif.detfre15!="na")]
fif=fif.loc[pd.to_numeric(fif.detfre15)>0]

fif["fif_document_id"]="1512358"
fif["fif_document_filename"]="MDA-MDH 2015 Recon Study Community Public Water Supply Wells_b.pdf"
fif["doc_date"]="October 2016"
fif["raw_category"]=""
fif["raw_cas"]=""
fif["cat_code"]=""
fif["description_cpcat"]=""
fif["cpcat_code"]=""
fif["cpcat_sourcetype"]=""
fif["report_funcuse"]=""

fif=fif[["fif_document_id","fif_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]

fif.to_csv("MDA_MDH_2015_recon_table2_2015.csv", index=False)
