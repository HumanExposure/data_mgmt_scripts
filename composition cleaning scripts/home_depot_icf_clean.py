#lkoval
#9-19-19

import pandas as pd
import string
import os

os.chdir("//home//lkoval//comp_data_cleaning")


raw_data=pd.read_csv("home_depot_-_icf_msds_extract_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])

raw_data=raw_data.loc[raw_data.unit_type__title=="percent"]
raw_data=raw_data.loc[raw_data.raw_central_comp!="Balance"]
raw_data=raw_data.loc[raw_data.raw_central_comp!="Up to 100"]
raw_data=raw_data.loc[raw_data.raw_central_comp.astype(str).str.contains(",")==False]

raw_data=raw_data.reset_index()
raw_data=raw_data[["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"]]

cleaning_df=raw_data
chemID=[]
lower=[]
central=[]
upper=[]
double=[]
drop=[]

for index, row in cleaning_df.iterrows():

    if pd.isnull(row.raw_min_comp) and pd.isnull(row.raw_central_comp) and pd.isnull(row.raw_max_comp):
        continue

    elif pd.isnull(row.raw_min_comp)==False and pd.isnull(row.raw_central_comp):
        chemID.append(str(row.ExtractedChemical_id))
        lower.append(str(row.raw_min_comp))
        upper.append(str(row.raw_max_comp))
        central.append("")

    else:
        chemID.append(str(row.ExtractedChemical_id))
        flag=True
        if "-" in row.raw_central_comp:
            lower.append(row.raw_central_comp[:row.raw_central_comp.index("-")])
            upper.append(row.raw_central_comp[row.raw_central_comp.index("-")+1:])
            central.append("")
            flag=False

        if flag==True:
            if row.raw_central_comp[0]=="<":
                lower.append("0.0")
                upper.append(row.raw_central_comp)
                central.append("")
            elif row.raw_central_comp[0]==">":
                lower.append(row.raw_central_comp)
                upper.append("100.0")
                central.append("")
            else:
                lower.append("")
                upper.append("")
                central.append(row.raw_central_comp)

split_data=pd.DataFrame()
split_data["id"]=chemID
split_data["lower_wf_analysis"]=lower
split_data["central_wf_analysis"]=central
split_data["upper_wf_analysis"]=upper

split_data.lower_wf_analysis=pd.to_numeric(split_data.lower_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.lower_wf_analysis=split_data.lower_wf_analysis.round(6)
split_data.upper_wf_analysis=pd.to_numeric(split_data.upper_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.upper_wf_analysis=split_data.upper_wf_analysis.round(6)
split_data.central_wf_analysis=pd.to_numeric(split_data.central_wf_analysis.str.replace(">","").str.replace("<","").str.replace("=",""), errors='coerce')/100
split_data.central_wf_analysis=split_data.central_wf_analysis.round(6)
clean_data=split_data.fillna("")

clean_data.to_csv("home_depot_icf_msds_all_cleaned.csv", index=False)
