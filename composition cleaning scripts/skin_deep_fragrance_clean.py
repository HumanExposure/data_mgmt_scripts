#lkoval
#3-2-20

import pandas as pd
import os

os.chdir("//home//lkoval//comp_data_cleaning")

raw_data=pd.read_csv("skin_deep_fragrance_products_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

clean_data=raw_data.copy().rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
clean_data.central_wf_analysis=(pd.to_numeric(clean_data.central_wf_analysis,errors="coerce"))/100
clean_data=clean_data.dropna(subset=["lower_wf_analysis","central_wf_analysis","upper_wf_analysis"],how="all")
clean_data.central_wf_analysis=clean_data.central_wf_analysis.round(10)
clean_data=clean_data.fillna("")
clean_data.central_wf_analysis=clean_data.central_wf_analysis.astype(str)

clean_data.to_csv("skin_deep_fragrance_products_cleaned.csv", index=False)
