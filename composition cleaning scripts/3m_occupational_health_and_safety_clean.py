#lkoval
#9-23-19

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("3m_occupational_health_and_safety_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.loc[raw_data.raw_central_comp.str.replace(" ","").str.contains("[A-Za-z]")==False]
raw_data=raw_data.loc[raw_data.raw_central_comp.str.replace(" ","")!="0<1"]

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"]]


raw_data["raw_central_comp"]=raw_data["raw_central_comp"].str.replace(' ','')
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[0]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_max_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[1]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_central_comp"]]=""
raw_data.loc[raw_data["raw_central_comp"].str.contains("<"), ["raw_max_comp"]]=raw_data["raw_central_comp"].str.strip("<")
raw_data.loc[raw_data["raw_central_comp"].str.contains("<"), ["raw_min_comp"]]="0"
raw_data.loc[raw_data["raw_central_comp"].str.contains("<"), ["raw_central_comp"]]=""
raw_data.loc[raw_data["raw_central_comp"].str.contains(">"), ["raw_max_comp"]]="100"
raw_data.loc[raw_data["raw_central_comp"].str.contains(">"), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.strip(">")
raw_data.loc[raw_data["raw_central_comp"].str.contains(">"), ["raw_central_comp"]]=""


split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.lower_wf_analysis=split_data.lower_wf_analysis.round(6)
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.upper_wf_analysis=split_data.upper_wf_analysis.round(6)
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(6)
clean_data=split_data.fillna("")

clean_data.to_csv("3m_occupational_health_and_safety_cleaned.csv", index=False)
