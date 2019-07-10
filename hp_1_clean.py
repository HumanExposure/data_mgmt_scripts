#lkoval
#7/10/19

import pandas as pd
import string

rawData=pd.read_csv("hewlett-packard_1_raw_extracted_records.csv", usecols=["ExtractedChemical_id","raw_min_comp","raw_central_comp","raw_max_comp","unit_type__title"])
chemID=[]
lower=[]
central=[]
upper=[]

for i in range(0,len(rawData)):
    chemID.append(str(rawData["ExtractedChemical_id"].iloc[i]))
    flag=True  #prevents double counting of chems that have - and <, >
    if "-" in rawData["raw_central_comp"].iloc[i]:
        lower.append(rawData["raw_central_comp"].iloc[i][:rawData["raw_central_comp"].iloc[i].index("-")])
        upper.append(rawData["raw_central_comp"].iloc[i][rawData["raw_central_comp"].iloc[i].index("-")+1:])
        central.append("")
        flag=False

    if flag==True:
        if rawData["raw_central_comp"].iloc[i][0]=="<":
            lower.append(0)
            upper.append(rawData["raw_central_comp"].iloc[i])
            central.append("")
        elif rawData["raw_central_comp"].iloc[i][0]==">":
            upper.append(100)
            lower.append(rawData["raw_central_comp"].iloc[i])
            central.append("")
        else:
            lower.append("")
            upper.append("")
            central.append(rawData["raw_central_comp"].iloc[i])

cleanData=pd.DataFrame()
cleanData["id"]=chemID
cleanData["lower_wf_analysis"]=lower
cleanData["central_wf_analysis"]=central
cleanData["upper_wf_analysis"]=upper

toDrop=[]
for j in range(0, len(cleanData)):
    if "<" in cleanData["central_wf_analysis"].iloc[j] or cleanData["central_wf_analysis"].iloc[j]=="(hazard":
        toDrop.append(j)

    if str(cleanData["lower_wf_analysis"].iloc[j]).replace(">","").replace("<","").replace(".","").replace(" ","").replace("%","").isnumeric():
        cleanData["lower_wf_analysis"].iloc[j]=float(str(cleanData["lower_wf_analysis"].iloc[j]).replace(">","").replace("<","").replace("%",""))/100
    if str(cleanData["central_wf_analysis"].iloc[j]).replace(">","").replace("<","").replace(".","").replace(" ","").replace("%","").isnumeric():
        cleanData["central_wf_analysis"].iloc[j]=float(str(cleanData["central_wf_analysis"].iloc[j]).replace(">","").replace("<","").replace("%",""))/100
    if str(cleanData["upper_wf_analysis"].iloc[j]).replace(">","").replace("<","").replace(".","").replace(" ","").replace("%","").isnumeric():
        cleanData["upper_wf_analysis"].iloc[j]=float(str(cleanData["upper_wf_analysis"].iloc[j]).replace(">","").replace("<","").replace("%",""))/100

cleanData=cleanData.drop(toDrop)

cleanData.to_csv("hp_1_cleaned.csv", columns=["id","lower_wf_analysis","central_wf_analysis","upper_wf_analysis"], index=False)
