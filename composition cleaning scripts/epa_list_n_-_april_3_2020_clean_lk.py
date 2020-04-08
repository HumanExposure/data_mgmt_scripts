import pandas as pd
import os
import string

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//covid_19")

#read in raw comp records as strings and only keep necessary columns
raw_data=pd.read_csv("epa_list_n_-_april_3_2020_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)

#Only keep records with a unit type of percent. In this case all the units are percent but it is a good safety check because this isn't always the case
raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]

#some quick checks to make sure all the composition data is in the raw_central_comp column (just in this particular case)
# raw_data.loc[pd.isnull(raw_data.raw_min_comp)==False]
# raw_data.loc[pd.isnull(raw_data.raw_max_comp)==False]
# raw_data.loc[pd.isnull(raw_data.raw_central_comp)]

#fill in null cells of df with empty string
raw_data=raw_data.fillna("")

#convert percentages to weight fractions and rename the columns to match the necessary headers to upload to Factotum. My standard practice involves creating a new df at this point after I have appropriately split the data into the correct raw columns. Again
#this is a super simple example so not really necessary here but just for consistency...I also round off the decimals at 10 places. This almost is never an issue but sometimes there will be a bajillion trailing zeros or something of the sort which Factotum doesn't like.
split_data=raw_data.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
split_data=split_data[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis)/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(10)

#Again I usually create a new df at this point where I double check to make sure everything looks good. Breaking things up into multiple dfs helps me debug. Usually I will perform some checks here (make sure there are no null values, negatives, values greater than 1, etc.).
#There is nothing of concern here so I can just copy the split df and make a csv.
clean_data=split_data.copy()
clean_data.to_csv("epa_list_n_april_3_2020_cleaned.csv", index=False)
