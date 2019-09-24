#lkoval
#9-24-19

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("bell_labs_1_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
clean_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
clean_data=clean_data.drop(["unit_type__title"], axis=1)

clean_data.central_wf_analysis=(pd.to_numeric(clean_data.central_wf_analysis)/100).round(6)
clean_data=clean_data.fillna("")

clean_data.to_csv("bell_labs_1_cleaned.csv", index=False)
