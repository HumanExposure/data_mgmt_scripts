#lkoval
#2-24-2020

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("schaeffer_manufacturing_co_safety_data_sheets_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype="str")
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")

split_data=raw_data.copy()
split_data.loc[split_data.raw_central_comp.str.contains("<"), ["raw_max_comp"]]=split_data.raw_central_comp.str.replace("<","")
split_data.loc[split_data.raw_central_comp.str.contains("<"), ["raw_min_comp"]]="0"
split_data.loc[split_data.raw_central_comp.str.contains("<"), ["raw_central_comp"]]=""

split_data.loc[split_data.raw_max_comp.str.contains("<"), ["raw_min_comp"]]="0"
split_data.loc[split_data.raw_max_comp.str.contains("<"), ["raw_max_comp"]]=split_data.raw_max_comp.str.replace("<","")


clean_data=split_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
clean_data.lower_wf_analysis=pd.to_numeric(clean_data.lower_wf_analysis)/100
clean_data.lower_wf_analysis=clean_data.lower_wf_analysis.round(10)
clean_data.central_wf_analysis=pd.to_numeric(clean_data.central_wf_analysis)/100
clean_data.central_wf_analysis=clean_data.central_wf_analysis.round(10)
clean_data.upper_wf_analysis=pd.to_numeric(clean_data.upper_wf_analysis)/100
clean_data.upper_wf_analysis=clean_data.upper_wf_analysis.round(10)

clean_data=clean_data.fillna("")
clean_data=clean_data.applymap(str)
clean_data=clean_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

clean_data.to_csv("schaeffer_man_sds_cleaned.csv", index=False)
