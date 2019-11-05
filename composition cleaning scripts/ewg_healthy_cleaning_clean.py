#lkoval
#11-5-19

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("guide_to_healthy_cleaning_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.dropna(subset=["raw_min_comp","raw_central_comp","raw_max_comp"], how="all")

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]


raw_data.loc[(raw_data.raw_central_comp.str.contains("\d{1}-{1}\d{1}")) & (raw_data.raw_central_comp.str.split("\-", expand=True)[0]==raw_data.raw_central_comp.str.split("\-", expand=True)[1]), ["raw_central_comp"]]=raw_data.raw_central_comp.str.get(0)
raw_data=raw_data.loc[~raw_data.raw_central_comp.str.contains("\d+ \d+")]
raw_data["raw_central_comp"]=raw_data["raw_central_comp"].str.replace(' ','')
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[0]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_max_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[1]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_central_comp"]]=""

split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis)/100
split_data.lower_wf_analysis=split_data.lower_wf_analysis.round(6)
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis)/100
split_data.upper_wf_analysis=split_data.upper_wf_analysis.round(6)
split_data=split_data.loc[~split_data.central_wf_analysis.str.contains("^\.+\d+\.*")]
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(6)
clean_data=split_data.fillna("")
clean_data=clean_data.loc[(clean_data.lower_wf_analysis=="") | ((clean_data.lower_wf_analysis!="") & (clean_data.lower_wf_analysis<clean_data.upper_wf_analysis))]


clean_data.to_csv("guide_to_healthy_cleaning_cleaned.csv", index=False)
