import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")

raw_data=pd.read_csv("unilever_1_-_msds_usa_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
raw_data=raw_data.loc[raw_data.unit_type__title=="weight fraction"]
clean_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]
clean_data=clean_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
clean_data=clean_data.fillna("")

clean_data.to_csv("unilever_1_msds_cleaned.csv", index=False)
