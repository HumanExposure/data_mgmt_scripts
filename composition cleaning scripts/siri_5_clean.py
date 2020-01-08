#lkoval
#1-8-19

import pandas as pd
import string
import os
import math

#takes a dataframe and only keeps rows that have unit type of percent, replaces all spaces with empty strings, replaces all null values with empty strings, and removes rows that have comp data that
#is entirely alphabetic. Also removes rows with comp data of the form .x. The index is reset and the dataframe is returned with the columns ExtractedChemical_id, raw_min_comp, raw_central_comp, and raw_max_comp.
def initial_clean(df=pd.DataFrame()):
    df=df.loc[df.unit_type__title=="percent"]
    df.raw_central_comp=df.raw_central_comp.str.replace(" ","")
    df.raw_min_comp=df.raw_min_comp.str.replace(" ","")
    df.raw_max_comp=df.raw_max_comp.str.replace(" ","")
    df=df.fillna("")
    df=df.loc[~((df.raw_central_comp.str.isalpha()) | (df.raw_max_comp.str.isalpha()))]
    df=df.loc[~(df.raw_central_comp.str.contains("\.\d+\."))]
    df=df.reset_index()
    df=df[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]
    return df

#takes a dataframe and deals with situation where on orgignal document, comp data was presented as ‎x±y which was split up during extraction and thus the raw data being read in is incorret. Raw records
#are of the form raw_min_comp: x+ or x+/; raw_central_comp: empty; raw_max_comp: y. A dataframe of the corrected data is returned where raw_min_comp takes the value i where i=x-y, raw_central_comp remains empty, and
#raw_max_comp takes the value j where j=x+y.
def plus_minus(df=pd.DataFrame()):
    df.loc[df.raw_min_comp.str.contains("\d+\+"), ["raw_central_comp"]]=pd.to_numeric(df["raw_min_comp"].str.replace("+","").str.replace("/",""), errors="coerce")
    df.loc[df.raw_min_comp.str.contains("\d+\+"), ["raw_max_comp"]]=pd.to_numeric(df["raw_max_comp"], errors="coerce")
    df=df.dropna()
    df.loc[df.raw_min_comp.str.contains("\d+\+"), ["raw_min_comp"]]=df["raw_max_comp"]*-1
    df.loc[(df.raw_min_comp!="") & (df.raw_central_comp!=""), ["raw_max_comp"]]=df["raw_central_comp"]+df["raw_max_comp"]
    df.loc[(df.raw_min_comp!="") & (df.raw_central_comp!=""), ["raw_min_comp"]]=df["raw_central_comp"]+df["raw_min_comp"]
    df.loc[(df.raw_min_comp!="") & (df.raw_central_comp!=""), ["raw_central_comp"]]=""
    df=df.applymap(str)
    return df

#takes a dataframe and for all values in raw_central_comp that indicate that the number provided is the minimum possible value ("min x", ">x", etc.) and places numerical value in
#raw_min_comp, 100 in raw_max_comp, and an empty string in raw_central_comp. Extraneous characters are removed. Adjusted dataframe is returned.
def min_split(df=pd.DataFrame()):
    bad_comps=list(df.ExtractedChemical_id.loc[df.raw_central_comp.str.contains('^>(\d+).o')])
    df=df.loc[lambda df: df.ExtractedChemical_id.isin(bad_comps)==False]
    min_keys=["^>","min","high","<$","\+$"]
    df.loc[(df["raw_central_comp"].str.contains("|".join(min_keys))), ["raw_min_comp"]]=df["raw_central_comp"].str.replace("[minhgorw\+><()/=_]","")
    df.loc[(df["raw_central_comp"].str.contains("|".join(min_keys))), ["raw_max_comp"]]="100"
    df.loc[(df["raw_central_comp"].str.contains("|".join(min_keys))), ["raw_central_comp"]]=""
    return df

#takes a dataframe and for all values in raw_central_comp that indicate that the number provided is the maximum possible value ("max x", "<x", etc.) and places numerical value in
#raw_max_comp, 0 in raw_min_comp, and an empty string in raw_central_comp. Extraneous characters are removed. Adjusted dataframe is returned.
def max_split(df=pd.DataFrame()):
    bad_comps=list(df.ExtractedChemical_id.loc[df.raw_central_comp.str.contains('^<(\d+).(\d+)ea')])
    df=df.loc[lambda df: df.ExtractedChemical_id.isin(bad_comps)==False]
    max_keys=["^<","max","upto","low","under","upto",">$"]
    df.loc[df["raw_central_comp"].str.contains("|".join(max_keys)), ["raw_min_comp"]]="0"
    df.loc[df["raw_central_comp"].str.contains("|".join(max_keys)), ["raw_max_comp"]]=df["raw_central_comp"].str.replace("[maxunderlwby><_()/]","").str.replace("pto","")
    df.loc[df["raw_central_comp"].str.contains("|".join(max_keys)), ["raw_central_comp"]]=""
    return df

#takes a dataframe and converts all comp data from percents to weight fractions by converting the strings to numbers and then dividing by 100. All data that can't be converted to a number
#is turned in a null value. This is used to eliminate any missed odd cases such as data with bizzare unit types that we shouldn't be cleaing anyway. All rows where this is the case are removed and
#the dataframe of weight fractions is returned.
def convert_2_wf(df=pd.DataFrame()):
    df=df.rename(columns={"raw_min_comp":"lower_wf_analysis","raw_central_comp":"central_wf_analysis","raw_max_comp":"upper_wf_analysis"})
    df.lower_wf_analysis=pd.to_numeric(df.lower_wf_analysis.str.replace(">","").str.replace("<","").str.replace("+","").str.replace("=","").str.replace("/","", regex=False))/100
    df.lower_wf_analysis=df.lower_wf_analysis.round(10)
    df.central_wf_analysis=pd.to_numeric(df.central_wf_analysis, errors="coerce")/100
    df.central_wf_analysis=df.central_wf_analysis.round(10)
    df.upper_wf_analysis=pd.to_numeric(df.upper_wf_analysis.str.replace("<","").str.replace(">","").str.replace("=","").str.replace("/","", regex=False))/100
    df.upper_wf_analysis=df.upper_wf_analysis.round(10)
    df=df.dropna(subset=["lower_wf_analysis","central_wf_analysis","upper_wf_analysis"], how="all")
    return df

#takes a dataframe and removes rows where any comp data is larger than 1, the lower_wf_analysis is larger thena the upper_wf_analysis,the lower_wf_analysis=upper_wf_analysis, or the lower or upper wf_analysis is
#empty when the other is populated. The adjusted dataframe is returned.
def remove_bad_rows(df=pd.DataFrame()):
    df=df.loc[~((pd.isnull(df.upper_wf_analysis)==False) & (df.upper_wf_analysis>1))]
    df=df.loc[~((pd.isnull(df.central_wf_analysis)==False) & (df.central_wf_analysis>1))]
    df=df.loc[~((pd.isnull(df.upper_wf_analysis)==False) & (df.upper_wf_analysis<df.lower_wf_analysis))]
    df=df.loc[~((df.lower_wf_analysis==df.upper_wf_analysis) & (pd.isnull(df.lower_wf_analysis)==False))]
    df=df.loc[~(df.central_wf_analysis==0)]
    df=df.loc[~(((pd.isnull(df.lower_wf_analysis)) & (pd.isnull(df.upper_wf_analysis)==False)) | ((pd.isnull(df.lower_wf_analysis)==False) & (pd.isnull(df.upper_wf_analysis))))]
    df=df.reset_index()
    df=df[["ExtractedChemical_id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"]]
    return df


os.chdir("//home//lkoval//comp_data_cleaning")
raw_data=pd.read_csv("siri_cpcat_data_5_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"], dtype=str)

raw_data=initial_clean(raw_data)
raw_data=plus_minus(raw_data)
raw_data=min_split(raw_data)
raw_data=max_split(raw_data)

#removes "w" & "wt"from raw_central_comp point estimate values
raw_data.loc[raw_data["raw_central_comp"].str.contains("w"), ["raw_central_comp"]]=raw_data["raw_central_comp"].str.replace("[wt/()*]","")
raw_data=raw_data.loc[~(raw_data.raw_central_comp.str.contains("[a-zA-Z/_+*]"))]

#There are cases where on the original document the comp data has the format <x-y. y was kept in the raw_max_comp field and 0 was placed in the raw_min_comp field.
raw_data.loc[raw_data.raw_min_comp.str.startswith("<"), ["raw_max_comp"]]=raw_data["raw_max_comp"].str.strip("<")
raw_data.loc[raw_data.raw_min_comp.str.startswith("<"), ["raw_min_comp"]]="0"


#drops all rows in raw_min_comp that contain alphabetic characters and extraneous characters
raw_data=raw_data.loc[~(raw_data.raw_min_comp.str.contains("[a-zA-Z_+*/)(]"))]

#removes "wt" or related strings from raw_max_comp
raw_data.loc[raw_data.raw_max_comp.str.contains("/$|[wt]"),["raw_max_comp"]]=raw_data.raw_max_comp.str.replace("[wt/]","")

#drops all rows in raw_max_comp that contain alphabetic characters and extraneous characters
raw_data=raw_data.loc[~(raw_data.raw_max_comp.str.contains("[a-zA-Z*_+()/]"))]

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp"]]

split_data=convert_2_wf(raw_data)
split_data=remove_bad_rows(split_data)
clean_data=split_data.fillna("")

#split data in multiple files to upload due to size of clean_data
start=0
for i in range(1,math.ceil(len(clean_data)/7500)+1):
    stop=i*7500
    temp=clean_data.iloc[start:stop]
    temp.to_csv("siri_5_cleaned_%d.csv"%i, index=False)
    start=stop
