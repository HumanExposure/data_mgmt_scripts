#lkoval
#11-5-19

import pandas as pd
import string
import os

#Read in raw records and only keep records that are of the "percent" unit type
os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("guide_to_healthy_cleaning_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.dropna(subset=["raw_min_comp","raw_central_comp","raw_max_comp"], how="all")

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

#deal with cases where the same value is on both ends of a range, ie 1-1, in which case the value (1) is placed in the central field
raw_data.loc[(raw_data.raw_central_comp.str.contains("\d{1}-{1}\d{1}")) & (raw_data.raw_central_comp.str.split("\-", expand=True)[0]==raw_data.raw_central_comp.str.split("\-", expand=True)[1]), ["raw_central_comp"]]=raw_data.raw_central_comp.str.get(0)

#removes records that have spacing issues
raw_data=raw_data.loc[~raw_data.raw_central_comp.str.contains("\d+ \d+")]
raw_data["raw_central_comp"]=raw_data["raw_central_comp"].str.replace(' ','')

#splits range values into min and max fields then makes central field empty
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[0]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_max_comp"]]=raw_data["raw_central_comp"].str.split('\-', expand=True)[1]
raw_data.loc[raw_data["raw_central_comp"].str.contains("-"), ["raw_central_comp"]]=""

#convert percents to weight fractions
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis)/100
split_data.lower_wf_analysis=split_data.lower_wf_analysis.round(6)
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis)/100
split_data.upper_wf_analysis=split_data.upper_wf_analysis.round(6)
split_data=split_data.loc[~split_data.central_wf_analysis.str.contains("^\.+\d+\.*")] #removes records where some combination of decimals & ellipsis were present before any numbers which made it difficult to interpret
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(6)

#fill in all null cells with an empty string and only keep range records where lower_wf < upper_wf
clean_data=split_data.fillna("")
clean_data=clean_data.loc[(clean_data.lower_wf_analysis=="") | ((clean_data.lower_wf_analysis!="") & (clean_data.lower_wf_analysis<clean_data.upper_wf_analysis))]


clean_data.to_csv("guide_to_healthy_cleaning_cleaned.csv", index=False)
