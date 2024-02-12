from tabula import read_pdf
import pandas as pd
import string
import os
import re
import math
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State of Washington\PFAS Concentrations in Effluent\Documents')

table2 = read_pdf("PFAS Concentrations in Effluent Table 2.pdf", pages="16", lattice=False, pandas_options={'header': None})[0]
table2.drop([0,1],axis=1,inplace=True)
table2["raw_chem_name"] = ""
table2.reset_index(drop=True,inplace=True)
for j in range(0,len(table2.columns)-1):
    table2.loc[j,"raw_chem_name"] = table2.iloc[0,j]
table2.drop([2,3,4,5,6,7,8,9,10,11,12],axis=1,inplace=True)
table2["data_document_id"]="1690580"
table2["data_document_filename"]="PFAS Concentrations in Effluent Table 2.pdf"
table2["doc_date"]="November 2022"
table2["raw_cas"] = ""
table2["raw_category"]=""
table2["cat_code"]=""
table2["description_cpcat"]=""
table2["cpcat_code"]=""
table2["cpcat_sourcetype"]=""
table2["chem_detected_flag"]=1
table2.loc[7,"chem_detected_flag"] = 0
table2.loc[8,"chem_detected_flag"] = 0
table2.loc[9,"chem_detected_flag"] = 0
table2.loc[10,"chem_detected_flag"] = 0
table2.to_csv("PFAS Concentrations in Effluent Table 2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

table3 = read_pdf("PFAS Concentrations in Effluent Table 3.pdf", pages="17", lattice=False, pandas_options={'header': None})[0]
table3.drop([0,1],axis=1,inplace=True)
table3["raw_chem_name"] = ""
table3.reset_index(drop=True,inplace=True)
for j in range(0,len(table3.columns)-1):
    table3.loc[j,"raw_chem_name"] = table3.iloc[0,j]
table3.drop([2,3,4,5,6,7,8,9,10,11,12],axis=1,inplace=True)
table3["data_document_id"]="1690574"
table3["data_document_filename"]="PFAS Concentrations in Effluent Table 3.pdf"
table3["doc_date"]="November 2022"
table3["raw_cas"] = ""
table3["raw_category"]=""
table3["cat_code"]=""
table3["description_cpcat"]=""
table3["cpcat_code"]=""
table3["cpcat_sourcetype"]=""
table3["chem_detected_flag"]=1
table3.loc[0,"chem_detected_flag"] = 0
table3.loc[3,"chem_detected_flag"] = 0
table3.to_csv("PFAS Concentrations in Effluent Table 3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

table4 = read_pdf("PFAS Concentrations in Effluent Table 4.pdf", pages="17", lattice=False, pandas_options={'header': None})[1]
table4.drop([0,1],axis=1,inplace=True)
table4["raw_chem_name"] = ""
table4.reset_index(drop=True,inplace=True)
for j in range(0,len(table4.columns)-1):
    table4.loc[j,"raw_chem_name"] = table4.iloc[0,j]
table4.drop([2,3,4,5,6,7,8,9],axis=1,inplace=True)
table4["data_document_id"]="1690575"
table4["data_document_filename"]="PFAS Concentrations in Effluent Table 4.pdf"
table4["doc_date"]="November 2022"
table4["raw_cas"] = ""
table4["raw_category"]=""
table4["cat_code"]=""
table4["description_cpcat"]=""
table4["cpcat_code"]=""
table4["cpcat_sourcetype"]=""
table4["chem_detected_flag"]=1
table4.loc[5,"chem_detected_flag"] = 0
table4.loc[3,"chem_detected_flag"] = 0
table4.loc[7,"chem_detected_flag"] = 0
table4.to_csv("PFAS Concentrations in Effluent Table 4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

table5 = read_pdf("PFAS Concentrations in Effluent Table 5.pdf", pages="18", lattice=False, pandas_options={'header': None})[0]
table5.drop([0,1],axis=1,inplace=True)
table5["raw_chem_name"] = ""
table5.reset_index(drop=True,inplace=True)
for j in range(0,len(table5.columns)-1):
    table5.loc[j,"raw_chem_name"] = table5.iloc[0,j]
table5.drop([2,3,4,5,6,7,8,9],axis=1,inplace=True)
table5["data_document_id"]="1690576"
table5["data_document_filename"]="PFAS Concentrations in Effluent Table 5.pdf"
table5["doc_date"]="November 2022"
table5["raw_cas"] = ""
table5["raw_category"]=""
table5["cat_code"]=""
table5["description_cpcat"]=""
table5["cpcat_code"]=""
table5["cpcat_sourcetype"]=""
table5["chem_detected_flag"]=1
table5.loc[1,"chem_detected_flag"] = 0
table5.loc[3,"chem_detected_flag"] = 0
table5.to_csv("PFAS Concentrations in Effluent Table 5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

table6 = read_pdf("PFAS Concentrations in Effluent Table 6.pdf", pages="18", lattice=False, pandas_options={'header': None})[1]
table6.iloc[0,5] = "N-MeFOSE"
table6.iloc[0,6] = "N-EtFOSE"
table6.iloc[0,7] = "5:3 FTCA"
table6.iloc[0,8] = "7:3 FTCA"
table6.drop([0],axis=1,inplace=True)
table6["raw_chem_name"] = ""
table6.reset_index(drop=True,inplace=True)
for j in range(0,len(table6.columns)-1):
    table6.loc[j,"raw_chem_name"] = table6.iloc[0,j]
table6.drop([2,3,4,5,6,7,8],axis=1,inplace=True)
table6.drop([1],axis=1,inplace=True)
table6.reset_index(drop=True,inplace=True)
table6["data_document_id"]="1690577"
table6["data_document_filename"]="PFAS Concentrations in Effluent Table 6.pdf"
table6["doc_date"]="November 2022"
table6["raw_cas"] = ""
table6["raw_category"]=""
table6["cat_code"]=""
table6["description_cpcat"]=""
table6["cpcat_code"]=""
table6["cpcat_sourcetype"]=""
table6["chem_detected_flag"]=1
table6.loc[1,"chem_detected_flag"] = 0
table6.loc[4,"chem_detected_flag"] = 0
table6.loc[7,"chem_detected_flag"] = 0
table6.to_csv("PFAS Concentrations in Effluent Table 6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

table7 = table6
table7["data_document_id"]="1690578"
table7["data_document_filename"]="PFAS Concentrations in Effluent Table 7.pdf"
table7["chem_detected_flag"]=1
table7.loc[0,"chem_detected_flag"] = 0
table7.to_csv("PFAS Concentrations in Effluent Table 7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

table8 = read_pdf("PFAS Concentrations in Effluent Table 8.pdf", pages="21", lattice=False, pandas_options={'header': None})[0]
table8.drop([0,11],axis=0,inplace=True)
table8.drop([1,2,3,4,5,6,7],axis=1,inplace=True)
table8["raw_chem_name"] = table8.iloc[:,0]
table8["raw_chem_name"] = table8["raw_chem_name"].apply(lambda x: re.sub(r'[^A-Za-z\s]|ND', '', str(x)))
table8['raw_chem_name'] = table8['raw_chem_name'].apply(lambda x: x.rstrip() if isinstance(x, str) else x)
table8.drop([0],axis=1,inplace=True)
table8.reset_index(drop=True,inplace=True)
table8["data_document_id"]="1690579"
table8["data_document_filename"]="PFAS Concentrations in Effluent Table 8.pdf"
table8["doc_date"]="November 2022"
table8["raw_cas"] = ""
table8["raw_category"]=""
table8["cat_code"]=""
table8["description_cpcat"]=""
table8["cpcat_code"]=""
table8["cpcat_sourcetype"]=""
table8["chem_detected_flag"]=1
table8.to_csv("PFAS Concentrations in Effluent Table 8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)
