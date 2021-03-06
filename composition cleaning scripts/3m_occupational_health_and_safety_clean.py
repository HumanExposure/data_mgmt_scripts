#lkoval
#3-3-20

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")

#read in data and only keep those with units of percent
raw_data=pd.read_csv("3m_occupational_health_and_safety_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")

#clean up df
raw_data=raw_data.loc[raw_data.raw_central_comp.str.replace(" ","")!="0<1"]
raw_data=raw_data.loc[raw_data.raw_central_comp!="trace"]
raw_data.raw_central_comp=raw_data.raw_central_comp.str.replace("[a-zA-Z]","") #for points that are "approximately X", just "X" is left in the raw_central_comp field
raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"]]
raw_data["raw_central_comp"]=raw_data["raw_central_comp"].str.replace(' ','')

#split ranges into min and max fields
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[0]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_max_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[1]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_central_comp"]]=""

#split inequalities to min and max fields
raw_data.loc[raw_data["raw_central_comp"].str.contains("<"), ["raw_max_comp"]]=raw_data["raw_central_comp"].str.strip("<")
raw_data.loc[raw_data["raw_central_comp"].str.contains("<"), ["raw_min_comp"]]="0"
raw_data.loc[raw_data["raw_central_comp"].str.contains("<"), ["raw_central_comp"]]=""

raw_data.loc[raw_data["raw_central_comp"].str.contains(">"), ["raw_max_comp"]]="100"
raw_data.loc[raw_data["raw_central_comp"].str.contains(">"), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.strip(">")
raw_data.loc[raw_data["raw_central_comp"].str.contains(">"), ["raw_central_comp"]]=""

#convert percent to wf
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.lower_wf_analysis=split_data.lower_wf_analysis.round(10)
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.upper_wf_analysis=split_data.upper_wf_analysis.round(10)
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)
clean_data=split_data.fillna("")

clean_data.to_csv("3m_occupational_health_and_safety_cleaned.csv", index=False)
