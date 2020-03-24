#lkoval
#3-24-20

import pandas as pd
import os

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//MN//EPA-USGS DWTP study 2017")

phase1=pd.read_excel("Phase I and II final data for Sci Hub and other distribution_b.xlsx", sheet_name="Phase I", dtype=str)
phase2=pd.read_excel("Phase I and II final data for Sci Hub and other distribution_b.xlsx", sheet_name="Phase II", dtype=str)

#numbers of Surface Water DWTPs according to MDH
sw_plants=[1,2,3,4,10,11,13,14,15,16,17,18,19,20,21,22,23,25,26,27,28,29]
sw_plants=[str(x) for x in sw_plants]


#indicators that a chemical was detected according to "abbreviations" sheet in excel file being read in
detect_keys=["^<LCMRL","^<RL", "^> 150% recovery","^[0-9]"]

#renaming and selecting data labeled as "Treated" from Surface Water DWTPs from Phase 1. Doesn't consider LFMs or Field Blanks.
p1_cols_fsw=[col.replace("\n"," ") for col in phase1.columns]
new_col_names=dict(zip(phase1.columns,p1_cols_fsw))
p1=phase1.rename(columns=new_col_names)
p1_cols_fsw=[col for col in p1.columns if ((("Treated" in col) or ("Analyte" in col)) and (("LFM" not in col) and ("Field" not in col)))]
p1=p1[p1_cols_fsw]
p1_cols_fsw=[col for col in p1.columns if (((len(col.split(" "))>1) and (col.split(" ")[1] in sw_plants)) or ("Analyte" in col))]
p1=p1[p1_cols_fsw]

#renaming and selecting data labeled as "Treated" from Surface Water DWTPs from Phase 2. Doesn't consider LFMs or Field Blanks.
p2_cols_fsw=[col.replace("\n"," ") for col in phase2.columns]
new_col_names=dict(zip(phase2.columns,p2_cols_fsw))
p2=phase2.rename(columns=new_col_names)
p2_cols_fsw=[col for col in p2.columns if ((("Treated" in col) or ("Analyte" in col)) and (("LFM" not in col) and ("Field" not in col)))]
p2=p2[p2_cols_fsw]
p2_cols_fsw=[col for col in p2.columns if (((len(col.split(" "))>1) and (col.split(" ")[1] in sw_plants)) or ("Analyte" in col))]
p2=p2[p2_cols_fsw]

#isolating chemicals that were detected at least once in Phase 1 at SW DWTPs
p1_detects=[]
for index, row in p1.drop("Analyte", axis=1).iterrows():
    if row.str.contains("|".join(detect_keys)).any():
        p1_detects.append(index)
p1=p1.iloc[p1_detects]
p1=p1[["Analyte"]]

#isolating chemicals that were detected at least once in Phase 2 at SW DWTPs
p2_detects=[]
for index, row in p2.drop("Analyte", axis=1).iterrows():
    if row.str.contains("|".join(detect_keys)).any():
        p2_detects.append(index)
p2=p2.iloc[p2_detects]
p2=p2[["Analyte"]]

#merge chem lists from phase 1 and phase 2
fsw=pd.concat([p1,p2], ignore_index=True)
fsw=fsw.rename(columns={"Analyte":"raw_chem_name"})

fsw["data_document_id"]="1512379"
fsw["data_document_filename"]="Phase I and II final data for Sci Hub and other distribution_b.xlsx"
fsw["doc_date"]="2017"
fsw["raw_category"]=""
fsw["raw_cas"]=""
fsw["cat_code"]=""
fsw["description_cpcat"]=""
fsw["cpcat_code"]=""
fsw["cpcat_sourcetype"]=""
fsw["report_funcuse"]=""

fsw=fsw[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]

fsw.to_csv("epa_usgs_2017_fsw.csv", index=False)
