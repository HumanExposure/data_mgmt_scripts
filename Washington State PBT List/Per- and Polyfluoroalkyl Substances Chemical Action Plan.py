from tabula import read_pdf
import pandas as pd
import string
import os
import re
import math
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State of Washington\Chemical Action Plan\Documents')

#Function for combing rows
def combine_row(table):
    i = 0
    while i < len(table):
        #Check if cell in column is empty
        if pd.isna(table.iloc[i,3]):
            #Check if part of the CAS number is in the cell below it
            #If it doesn't, the the row doesn't take the CAS number and add it to the row above it
            if pd.isna(table.iloc[i,1]):
                if str(table.iloc[i-1,0]).endswith('-'):
                    table.at[i-1,0] =  table.iloc[i-1,0] + table.iloc[i,0]
                    table.drop(i,axis=0,inplace=True)
                    table.reset_index(inplace=True,drop=True)
                else:
                    table.at[i-1,0] = table.iloc[i-1,0] + ' ' + table.iloc[i,0]
                    table.drop(i,axis=0,inplace=True)
                    table.reset_index(inplace=True,drop=True)
            else:
                table.iloc[i-1,1] = (table.iloc[i-1,1] + table.iloc[i,1])
                if str(table.iloc[i-1,0]).endswith('-'):
                    table.at[i-1,0] = table.iloc[i-1,0] + table.iloc[i,0]
                    table.drop(i,axis=0,inplace=True)
                    table.reset_index(inplace=True,drop=True)
                else:
                    table.at[i-1,0] =  table.iloc[i-1,0] + ' ' + table.iloc[i,0]
                    table.drop(i,axis=0,inplace=True)
                    table.reset_index(inplace=True,drop=True)               
        else:
            i = i + 1
    return table

#Table10
table10_1=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 10.pdf", pages="126", lattice=False, pandas_options={'header': None})[0]
table10_1.drop([0,1,2],axis=0,inplace=True)
table10_1.drop([1],axis=1,inplace=True)
table10_1.reset_index(drop=True,inplace=True)
table10_1 = combine_row(table10_1)

table10_2=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 10.pdf", pages="127", lattice=False, pandas_options={'header': None})[0]
table10_2.drop([0,1,2],axis=0,inplace=True)
table10_2.drop([1],axis=1,inplace=True)
table10_2.reset_index(drop=True,inplace=True)
table10_2 = combine_row(table10_2)

array = [table10_1,table10_2]
table10 = pd.concat(array,ignore_index=True)
table10["data_document_id"]="1690552"
table10["data_document_filename"]="Per- and Polyfluoroalkyl Substances CAP Table 10.pdf"
table10["doc_date"]="September 2022"
table10["raw_chem_name"] = table10.iloc[:,0]
table10["raw_cas"] = table10.iloc[:,1]
table10["raw_category"]=""
table10["cat_code"]=""
table10["description_cpcat"]=""
table10["cpcat_code"]=""
table10["cpcat_sourcetype"]=""
table10["chem_detected_flag"]=1
table10.to_csv("Per- and Polyfluoroalkyl Substances CAP Table 10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","chem_detected_flag"], index=False)

#Table11
table11=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 10.pdf", pages="130", stream=True, pandas_options={'header': None})[0]
table11.drop([0],axis=0,inplace=True)
table11.reset_index(drop=True,inplace=True)
table11["data_document_id"]="1690549"
table11["data_document_filename"]="Per- and Polyfluoroalkyl Substances CAP Table 11.pdf"
table11["doc_date"]="September 2022"
table11["raw_chem_name"] = table11.iloc[:,0]
for j in range(0, len(table11)):
    table11["raw_chem_name"].iloc[j]=str(table11["raw_chem_name"].iloc[j]).replace("*","")
table11["raw_cas"] = table11.iloc[:,1]
table11["raw_category"]=""
table11["cat_code"]=""
table11["description_cpcat"]=""
table11["cpcat_code"]=""
table11["cpcat_sourcetype"]=""
table11.to_csv("Per- and Polyfluoroalkyl Substances CAP Table 11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table12
table12_1=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 12.pdf", pages="130", stream=True, pandas_options={'header': None})[1]
table12_1.drop([0],axis=0,inplace=True)
table12_1.reset_index(drop=True,inplace=True)
table12_2=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 12.pdf", pages="131", stream=True, pandas_options={'header': None})[0]
table12_2.drop([0],axis=0,inplace=True)
table12_2.reset_index(drop=True,inplace=True)
array = [table12_1,table12_2]
table12 = pd.concat(array,ignore_index=True)
table12["data_document_id"]="1690550"
table12["data_document_filename"]="Per- and Polyfluoroalkyl Substances CAP Table 12.pdf"
table12["doc_date"]="September 2022"
table12["raw_chem_name"] = table12.iloc[:,0]
for j in range(0, len(table12)):
    table12["raw_chem_name"].iloc[j]=str(table12["raw_chem_name"].iloc[j]).replace("*","")
table12["raw_cas"] = table12.iloc[:,1]
table12["raw_category"]=""
table12["cat_code"]=""
table12["description_cpcat"]=""
table12["cpcat_code"]=""
table12["cpcat_sourcetype"]=""
table12.to_csv("Per- and Polyfluoroalkyl Substances CAP Table 12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table13
table13=read_pdf("Per- and Polyfluoroalkyl Substances CAP Table 12.pdf", pages="131", stream=True, pandas_options={'header': None})[1]
table13.drop([0],axis=0,inplace=True)
table13.reset_index(drop=True,inplace=True)
table13["data_document_id"]="1690551"
table13["data_document_filename"]="Per- and Polyfluoroalkyl Substances CAP Table 13.pdf"
table13["doc_date"]="September 2022"
table13["raw_chem_name"] = table13.iloc[:,0]
for j in range(0, len(table13)):
    table13["raw_chem_name"].iloc[j]=str(table13["raw_chem_name"].iloc[j]).replace("*","")
table13["raw_cas"] = table13.iloc[:,1]
table13["raw_category"]=""
table13["cat_code"]=""
table13["description_cpcat"]=""
table13["cpcat_code"]=""
table13["cpcat_sourcetype"]=""
table13.to_csv("Per- and Polyfluoroalkyl Substances CAP Table 13.csv", columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name","raw_category","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
