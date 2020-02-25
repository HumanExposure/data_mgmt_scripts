#lkoval
#2-24-2020

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("declare_living_future_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype="str")
raw_data=raw_data.fillna("")

clean_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
clean_data.lower_wf_analysis=pd.to_numeric(clean_data.lower_wf_analysis)/100
clean_data.lower_wf_analysis=clean_data.lower_wf_analysis.round(10)
clean_data.central_wf_analysis=pd.to_numeric(clean_data.central_wf_analysis)/100
clean_data.central_wf_analysis=clean_data.central_wf_analysis.round(10)
clean_data.upper_wf_analysis=pd.to_numeric(clean_data.upper_wf_analysis)/100
clean_data.upper_wf_analysis=clean_data.upper_wf_analysis.round(10)

clean_data=clean_data.fillna("")
clean_data=clean_data.applymap(str)
clean_data=clean_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]
clean_data=clean_data.loc[~(pd.to_numeric(clean_data.central_wf_analysis)==0)]
clean_data.loc[(clean_data.central_wf_analysis!="") | (pd.to_numeric(clean_data.central_wf_analysis)<=1)]
clean_data=clean_data.loc[~(pd.to_numeric(clean_data.central_wf_analysis)>1)]
clean_data=clean_data.loc[~(pd.to_numeric(clean_data.upper_wf_analysis)>1)]

clean_data.to_csv("declare_living_future_cleaned.csv", index=False)
