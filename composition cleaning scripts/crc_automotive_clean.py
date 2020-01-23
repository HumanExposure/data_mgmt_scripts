#lkoval
#1-23-2020

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")

raw_data=pd.read_csv("crc_automotive_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data.raw_min_comp=raw_data.raw_min_comp.str.replace(" ","")
raw_data.raw_central_comp=raw_data.raw_central_comp.str.replace(" ","")
raw_data.raw_max_comp=raw_data.raw_max_comp.str.replace(" ","")
raw_data=raw_data.fillna("")
raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

#split data in the form "<x" in the raw_central_comp field into "0" in raw_min_comp and "x" in raw_max_comp
raw_data.loc[raw_data.raw_central_comp.str.startswith("<"), ["raw_max_comp"]]=raw_data.raw_central_comp.str.replace("<","")
raw_data.loc[raw_data.raw_central_comp.str.startswith("<"), ["raw_min_comp"]]="0"
raw_data.loc[raw_data.raw_central_comp.str.startswith("<"), ["raw_central_comp"]]=""

#split data in the form ">=x"  or ">x" in the raw_central_comp field into "x" in raw_min_comp and "100" in raw_max_comp
raw_data.loc[raw_data.raw_central_comp.str.startswith(">"), ["raw_min_comp"]]=raw_data.raw_central_comp.str.replace(">","").str.replace("=","")
raw_data.loc[raw_data.raw_central_comp.str.startswith(">"), ["raw_max_comp"]]="100"
raw_data.loc[raw_data.raw_central_comp.str.startswith(">"), ["raw_central_comp"]]=""

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

clean_data.to_csv("crc_auto_cleaned.csv", index=False)
