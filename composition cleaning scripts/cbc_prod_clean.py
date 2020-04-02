#lkoval
#4-2-20


import pandas as pd
import string
import os

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents")

#read in data and only keep those with units of percent (all in this case)
raw_data=pd.read_csv("cbc_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")


#convert percent to wf
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("cbc_prods_cleaned.csv", index=False)
