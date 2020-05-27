#lkoval
#4-24-20


import pandas as pd
import string
import os

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//covid_19")



"""
APR 10 2020
"""

#read in data and only keep those with units of percent (all in this case)
raw_data=pd.read_csv("epa_list_n_-_april_10_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]

#fill in null cells of df with empty string
raw_data=raw_data.fillna("")

#convert percent to wf
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("list_n_apr10_2020_cleaned.csv", index=False)



"""
APR 17 2020
"""
raw_data=pd.read_csv("epa_list_n_-_april_17_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("list_n_apr17_2020_cleaned.csv", index=False)



"""
APR 24 2020
"""

raw_data=pd.read_csv("epa_list_n_-_april_24_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("list_n_apr24_2020_cleaned.csv", index=False)


"""
May 1 2020
"""

raw_data=pd.read_csv("epa_list_n_-_may_1_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("list_n_may1_2020_cleaned.csv", index=False)


"""
May 11 2020
"""

raw_data=pd.read_csv("epa_list_n_-_may_11_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("list_n_may11_2020_cleaned.csv", index=False)



"""
May 22 2020
"""

raw_data=pd.read_csv("epa_list_n_-_may_22_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.fillna("")
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]

split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.copy()
clean_data.to_csv("list_n_may22_2020_cleaned.csv", index=False)

