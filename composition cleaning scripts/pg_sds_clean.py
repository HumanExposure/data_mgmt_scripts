#lkoval
#1-24-2020

import pandas as pd
import os

os.chdir("//home//lkoval//comp_data_cleaning")

raw_data=pd.read_csv("pg_sds_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data.raw_min_comp=raw_data.raw_min_comp.str.replace(" ","")
raw_data.raw_central_comp=raw_data.raw_central_comp.str.replace(" ","")
raw_data.raw_max_comp=raw_data.raw_max_comp.str.replace(" ","")
raw_data=raw_data.fillna("")
raw_data=raw_data.loc[~((raw_data.raw_central_comp.str.contains("[a-zA-Z]")) & (raw_data.raw_central_comp.str.contains("-")))]
raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

#split data in the form "x-y" to x in the raw_min_comp field and y in the raw_max_comp field
raw_data.loc[raw_data.raw_central_comp.str.contains("-"), ["raw_max_comp"]]=raw_data.raw_central_comp.str.split("-", expand=True)[1]
raw_data.loc[raw_data.raw_central_comp.str.contains("-"), ["raw_min_comp"]]=raw_data.raw_central_comp.str.split("-", expand=True)[0]
raw_data.loc[raw_data.raw_central_comp.str.contains("-"), ["raw_central_comp"]]=""


#convert percentages to weight fractions
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis)/100
split_data.lower_wf_analysis=split_data.lower_wf_analysis.round(10)
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis)/100
split_data.upper_wf_analysis=split_data.upper_wf_analysis.round(10)

clean_data=split_data.fillna("")
clean_data=clean_data.applymap(str)

clean_data.to_csv("pg_sds_cleaned.csv", index=False)
