#Michael Metcalf
#12/14/2023
from tabula import read_pdf
import pandas as pd
import string
import os
import re
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Green Products Company\Green Products Company Documents')

#Copper-Green Brown
tableCGB=read_pdf("Copper-Green Brown.pdf", pages="3", lattice=False, pandas_options={'header': None})[0]
tableCGB.drop([0,1],axis=0,inplace=True)
tableCGB.drop([1],axis=1,inplace=True)
tableCGB.reset_index(drop=True,inplace=True)
tableCGB["data_document_id"]="1687044"
tableCGB["data_document_filename"] = "Copper-Green Brown.pdf"
tableCGB["prod_name"] = "Copper-Green Brown Wood Preservative"
tableCGB["doc_date"] = "19-Oct-2022"
tableCGB["rev_num"] = ""
tableCGB["raw_category"] = "wood perservative"
tableCGB["raw_cas"] = tableCGB.iloc[:,1]
tableCGB["raw_chem_name"] = tableCGB.iloc[:,0]
tableCGB=tableCGB.dropna(subset=["raw_chem_name"])
for j in range(0, len(tableCGB)):
    tableCGB["raw_chem_name"].iloc[j]=str(tableCGB["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
tableCGB["report_funcuse"] = ""
tableCGB["raw_min_comp"] = ""
tableCGB.loc[0,"raw_min_comp"] = 5
tableCGB.loc[1,"raw_min_comp"] = 25
tableCGB.loc[2,"raw_min_comp"] = 20
tableCGB["raw_max_comp"] = ""
tableCGB.loc[0,"raw_max_comp"] = 25
tableCGB.loc[1,"raw_max_comp"] = 75
tableCGB.loc[2,"raw_max_comp"] = 70
tableCGB["unit_type"] = 14
tableCGB["ingrediant_rank"] = ""
tableCGB.loc[0,"ingrediant_rank"] = 1
tableCGB.loc[1,"ingrediant_rank"] = 2
tableCGB.loc[2,"ingrediant_rank"] = 3
tableCGB["raw_central_comp"] = ""
tableCGB["component"] = ""
tableCGB.to_csv("Copper-Green Brown.csv", columns=["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"], index=False)

#Copper-Green
tableCG = tableCGB
tableCG["data_document_id"] = "1687045"
tableCG["data_document_filename"] = "Copper-Green.pdf"
tableCG["prod_name"] = "Copper-Green Wood Perservative"
tableCG.to_csv("Copper-Green.csv", columns=["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"], index=False)

#Green's Water-Based
tableGWB=read_pdf("Green_s Water-Based.pdf", pages="3", lattice=False, pandas_options={'header': None})[0]
tableGWB.drop([0],axis=0,inplace=True)
tableGWB.drop([1],axis=1,inplace=True)
tableGWB.reset_index(drop=True,inplace=True)
tableGWB["data_document_id"]="1687046"
tableGWB["data_document_filename"] = "Green_s Water-Based.pdf"
tableGWB["prod_name"] = "Green's Water-Based Wood Preservative"
tableGWB["doc_date"] = "06-Dec-2022"
tableGWB["rev_num"] = ""
tableGWB["raw_category"] = "wood perservative"
tableGWB["raw_cas"] = tableGWB.iloc[:,1]
tableGWB["raw_chem_name"] = tableGWB.iloc[:,0]
tableGWB=tableGWB.dropna(subset=["raw_chem_name"])
for j in range(0, len(tableGWB)):
    tableGWB["raw_chem_name"].iloc[j]=str(tableGWB["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
tableGWB["report_funcuse"] = ""
tableGWB["raw_min_comp"] = ""
tableGWB.loc[0,"raw_min_comp"] = 2
tableGWB.loc[1,"raw_min_comp"] = 1
tableGWB["raw_max_comp"] = ""
tableGWB.loc[0,"raw_max_comp"] = 8
tableGWB.loc[1,"raw_max_comp"] = 5
tableGWB["unit_type"] = 14
tableGWB["ingrediant_rank"] = ""
tableGWB.loc[0,"ingrediant_rank"] = 1
tableGWB.loc[1,"ingrediant_rank"] = 2
tableGWB.loc[2,"ingrediant_rank"] = 3
tableGWB["raw_central_comp"] = ""
tableGWB.loc[2,"raw_central_comp"] = "< 1"
tableGWB["component"] = ""
tableGWB.to_csv("Green's Water-Based.csv", columns=["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"], index=False)

#Hydroperox
tableH = tableGWB
tableH.drop([0],axis=0,inplace=True)
tableH.reset_index(drop=True,inplace=True)
tableH["data_document_id"] = "1687047"
tableH["data_document_filename"] = "Hydroperox3percentS.pdf"
tableH["prod_name"] = "Hydrogen Peroxide 3%"
tableH["doc_date"] = "November 1, 2013"
tableH["raw_category"] = "disinfectant"
tableH.loc[0,"raw_chem_name"] = "Water"
tableH.loc[1,"raw_chem_name"] = "Hydrogen Peroxide"
tableH.loc[0,"raw_cas"] = "7732-18-5"
tableH.loc[1,"raw_cas"] = "7722-84-1"
tableH["raw_min_comp"] = ""
tableH["raw_max_comp"] = ""
tableH["unit_type"] = 3
tableH.loc[0,"raw_central_comp"] = 97
tableH.loc[1,"raw_central_comp"] = 3
tableH=tableH.dropna(subset=["raw_chem_name"])
for j in range(0, len(tableH)):
    tableH["raw_chem_name"].iloc[j]=str(tableH["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
tableH.loc[0,"ingrediant_rank"] = 1
tableH.loc[1,"ingrediant_rank"] = 2
tableH.to_csv("Hydroperox3percentS.csv", columns=["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"], index=False)

#Super Tardus
tableST = tableH
tableST.drop([1],axis=0,inplace=True)
tableST["data_document_id"] = "1687048"
tableST["data_document_filename"] = "SuperTardus.pdf"
tableST["prod_name"] = "Super-Tardus"
tableST["doc_date"] = "November 1, 2013"
tableST["raw_category"] = "concrete surface retarder"
tableST["raw_cas"] = ""
tableST["raw_chem_name"] = "Proprietary aqueous mixture"
tableST["unit_type"] = ""
tableST["raw_central_comp"] = ""
tableST.to_csv("SuperTardus.csv", columns=["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"], index=False)
