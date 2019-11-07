#lkoval
#11-7-19

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("skin_deep_babies__moms_products_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.dropna(subset=["raw_min_comp","raw_central_comp","raw_max_comp"], how="all")

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data.central_wf_analysis=split_data.central_wf_analysis/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

clean_data=split_data.fillna("")
clean_data.to_csv("ewg_skin_deep_babies_moms_cleaned.csv", index=False)
