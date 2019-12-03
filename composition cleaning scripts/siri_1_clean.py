#lkoval
#11-13-19

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("siri_cpcat_data_1_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data.raw_central_comp=raw_data.raw_central_comp.str.replace(" ","")
raw_data.raw_min_comp=raw_data.raw_min_comp.str.replace(" ","")
raw_data.raw_max_comp=raw_data.raw_max_comp.str.replace(" ","")
raw_data=raw_data.fillna("")
raw_data=raw_data.loc[~((raw_data.raw_central_comp.str.isalpha()) | (raw_data.raw_max_comp.str.isalpha()))]
raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]


#dealing with situation where on orgignal document, comp data was presented as ‎x±y which was split up during extraction and thus the raw data being read in is incorret. Raw records are of the
#form raw_min_comp: x+ or x+/ raw_central_comp: empty raw_max_comp: y
raw_data.loc[raw_data.raw_min_comp.str.contains("+", regex=False), ["raw_central_comp"]]=pd.to_numeric(raw_data["raw_min_comp"].str.replace("+","").str.replace("/",""), errors="coerce")
raw_data.loc[raw_data.raw_min_comp.str.contains("+", regex=False), ["raw_max_comp"]]=pd.to_numeric(raw_data["raw_max_comp"], errors="coerce")
raw_data.loc[raw_data.raw_min_comp.str.contains("+", regex=False), ["raw_min_comp"]]=raw_data["raw_max_comp"]*-1
raw_data.loc[(raw_data.raw_min_comp!="") & (raw_data.raw_central_comp!=""), ["raw_max_comp"]]=raw_data["raw_central_comp"]+raw_data["raw_max_comp"]
raw_data.loc[(raw_data.raw_min_comp!="") & (raw_data.raw_central_comp!=""), ["raw_min_comp"]]=raw_data["raw_central_comp"]+raw_data["raw_min_comp"]
raw_data.loc[(raw_data.raw_min_comp!="") & (raw_data.raw_central_comp!=""), ["raw_central_comp"]]=""
raw_data=raw_data.applymap(str)

raw_data.loc[raw_data["raw_min_comp"].str.contains("wt", regex=False), ["raw_min_comp"]]=raw_data["raw_min_comp"].str.strip("wt")


#removes all rows that have uninterpretable comp data in the raw_min_comp field due to alphabetic characters
raw_data=raw_data.loc[~raw_data.raw_min_comp.str.contains("[a-zA-Z]")]

#corrects rows that have comp data on the original document in the form of <x-y or >x-y. These values were split up duting extraction and thus the raw data being read is in correct. The most
#conservative assumptions were made to correct the fields.
raw_data.loc[raw_data.raw_min_comp.str.contains("<", regex=False), ["raw_min_comp"]]="0"
raw_data.loc[raw_data.raw_min_comp.str.contains(">", regex=False), ["raw_max_comp"]]="100"

#splits data into min and max fields if it is in the central comp field but it is indicated that it should be a range
raw_data.loc[(raw_data["raw_central_comp"].str.contains(">", regex=False)) | (raw_data["raw_central_comp"].str.contains("min", regex=False)) | (raw_data["raw_central_comp"].str.endswith("+")), ["raw_min_comp"]]=raw_data["raw_central_comp"].str.strip("min").str.replace("w","")
raw_data.loc[(raw_data["raw_central_comp"].str.contains(">", regex=False)) | (raw_data["raw_central_comp"].str.contains("min", regex=False)) | (raw_data["raw_central_comp"].str.endswith("+")), ["raw_max_comp"]]="100"
raw_data.loc[(raw_data["raw_central_comp"].str.contains(">", regex=False)) | (raw_data["raw_central_comp"].str.contains("min", regex=False)) | (raw_data["raw_central_comp"].str.endswith("+")), ["raw_central_comp"]]=""

raw_data.loc[(raw_data["raw_central_comp"].str.contains("<", regex=False)) | (raw_data["raw_central_comp"].str.contains("max", regex=False)) , ["raw_max_comp"]]=raw_data["raw_central_comp"].str.strip("max").str.strip("/")
raw_data.loc[(raw_data["raw_central_comp"].str.contains("<", regex=False)) | (raw_data["raw_central_comp"].str.contains("max", regex=False)) , ["raw_min_comp"]]="0"
raw_data.loc[(raw_data["raw_central_comp"].str.contains("<", regex=False)) | (raw_data["raw_central_comp"].str.contains("max", regex=False)) , ["raw_central_comp"]]=""

#strips away "wt" if the raw central comp is a number that is of the form wt x or wt: x
raw_data.loc[raw_data["raw_central_comp"].str.contains("wt", regex=False), ["raw_central_comp"]]=raw_data["raw_central_comp"].str.split(":",expand=True)[1]

raw_data.loc[raw_data["raw_central_comp"].str.startswith("+"), ["raw_central_comp"]]=raw_data["raw_central_comp"].str.strip("+")

#removes rows with uninterpretable comp data in the raw_central_comp field
raw_data=raw_data.loc[~(raw_data["raw_central_comp"].str.contains("[a-zA-Z\*\_\+/]"))]

#cleans up raw_max_comp field then removes all rows with uninterpretable comp data in the raw_max_comp field
raw_data.loc[(raw_data.raw_max_comp.str.contains("w", regex=False)) | (raw_data["raw_max_comp"].str.contains("]", regex=False)), ["raw_max_comp"]]=raw_data["raw_max_comp"].str.strip("wt").str.strip("w").str.strip("]")
raw_data=raw_data.loc[~raw_data["raw_max_comp"].str.contains("[a-zA-Z]")]

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

#convert raw comp data to weight fractions
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis.str.replace(">","").str.replace("+","").str.replace("=","").str.replace("/","", regex=False))/100
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis, errors="coerce")/100
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis.str.replace("<","").str.replace("=","").str.replace("/","", regex=False))/100

split_data=split_data.dropna(subset=["lower_wf_analysis","central_wf_analysis","upper_wf_analysis"], how="all")

#Remove all rows where weight fractions are not appropriate such as being >1 or lower_wf>upper_wf
split_data=split_data.loc[~((pd.isnull(split_data.upper_wf_analysis)==False) & (split_data.upper_wf_analysis>1))]
split_data=split_data.loc[~((pd.isnull(split_data.central_wf_analysis)==False) & (split_data.central_wf_analysis>1))]
split_data=split_data.loc[~((pd.isnull(split_data.upper_wf_analysis)==False) & (split_data.upper_wf_analysis<split_data.lower_wf_analysis))]
split_data=split_data.loc[~((split_data.lower_wf_analysis==split_data.upper_wf_analysis) & (pd.isnull(split_data.lower_wf_analysis)==False))]
clean_data=split_data.fillna("")

clean_data.to_csv("siri_1_cleaned.csv", index=False)
