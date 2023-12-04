#Michael Metcalf
#10-24-2023
#Imports
#%%
from tabula import read_pdf
import pandas as pd
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Arizona 2013')
#Table 2
#Reading table and removing empty rows/columns
table_2=read_pdf("Arizona 2013 Pesticide Report Table 2.pdf", pages="4", lattice=False, pandas_options={'header': None})[0]
table_2.drop([0,1,2,3],inplace=True)
#Assigning columns to labels for CSV
table_2["raw_chem_name"]=table_2.iloc[:,1]
#Cleaning the names by removing asteriks
table_2=table_2.dropna(subset=["raw_chem_name"])
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
#Asssigning required information for CSV format
table_2.reset_index(inplace=True)
table_2.drop_duplicates(inplace=True)
table_2["data_document_id"]="1400352"
table_2["data_document_filename"]="Arizona 2013 Pesticide Report Table 2.pdf"
table_2["raw_cas"]=""
table_2["doc_date"]="2013"
table_2["raw_category"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]=""
table_2.loc[0,"report_funcuse"]="Herbicide"
table_2.loc[1,"report_funcuse"]="Fungicide"
table_2.loc[2,"report_funcuse"]="Herbicide"
table_2.loc[3,"report_funcuse"]="Fungicide"
table_2.loc[4,"report_funcuse"]="Fungicide"
table_2.loc[5,"report_funcuse"]="Insecticide"
table_2.loc[6,"report_funcuse"]="Insecticide"
table_2.loc[7,"report_funcuse"]="Fungicide"
table_2.loc[8,"report_funcuse"]="Fungicide"
#Exporting to CSV
table_2.to_csv("Arizona 2013 Pesticides Annual Report Table 2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 3
#The table spans multiple pages. I appended the lists together.
table_3_1=read_pdf("Arizona 2013 Pesticide Report Table 2.pdf", pages="5", lattice=True, pandas_options={'header': None})[0]
table_3_2=read_pdf("Arizona 2013 Pesticide Report Table 2.pdf", pages="6", lattice=True, pandas_options={'header': None})[0]
table_3_3=read_pdf("Arizona 2013 Pesticide Report Table 2.pdf", pages="7", lattice=True, pandas_options={'header': None})[0]
table_3_4=read_pdf("Arizona 2013 Pesticide Report Table 2.pdf", pages="8", lattice=True, pandas_options={'header': None})[0]
#Function for cleaning table for each subtable
def table_debug(table_3):
    table_3.drop([0,1,3],axis=1,inplace=True)
    table_3.drop([0,1,2,3],axis=0,inplace=True)
    table_3.reset_index(drop=True,inplace=True)
    return table_3
#Concating all the tables
tables = [table_debug(table_3_1),table_debug(table_3_2),table_debug(table_3_3),table_debug(table_3_4)]
table_3 = pd.concat(tables, ignore_index=True)
#Assigning columns
table_3["raw_cas"]=table_3.iloc[:,0]
table_3["raw_chem_name"]=table_3.iloc[:,1]
table_3=table_3.dropna(subset=["raw_chem_name"])
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
table_3.drop_duplicates(inplace=True)
table_3["data_document_id"]="1400353"
table_3["data_document_filename"]="Arizona 2013 Pesticide Report Table 3.pdf"
table_3["doc_date"]="2013"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]=""
table_3["report_funcuse"]=""
#Exporting to CSV
table_3.to_csv("Arizona 2013 Pesticides Annual Report Table 3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 4
i = 9
table = []
while i < 30:
    table_4=read_pdf("Arizona 2013 Pesticide Report Table 4.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
    table_4.drop([0,1,2,3,6,7,8,9,10,11,12,13,14,15,16,17],axis=1,inplace=True)
    table_4.drop([0,1,2,3],axis=0,inplace=True)
    table_4.reset_index(drop=True,inplace=True)
    table.append(table_4)
    i = i + 1
table_4 = pd.concat(table,ignore_index=True)
table_4["raw_cas"]=table_4.iloc[:,0]
table_4["raw_chem_name"]=table_4.iloc[:,1]
table_4=table_4.dropna(subset=["raw_chem_name"])
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
table_4.drop_duplicates(inplace=True)
table_4["data_document_id"]="1400354"
table_4["data_document_filename"]="Arizona 2013 Pesticide Report Table 4.pdf"
table_4["doc_date"]="2013"
table_4["raw_category"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]=""
table_4["report_funcuse"]=""
table_4.to_csv("Arizona 2013 Pesticides Annual Report Table 4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
#Table 5
table_5=read_pdf("Arizona 2013 Pesticide Report Table 5.pdf", pages=30, lattice=True, pandas_options={'header': None})[0]
table_5.drop([0,1,2,3,4],axis=0,inplace=True)
table_5.drop([3,4,5,6,7,8],axis=1,inplace=True)
table_5.reset_index(drop=True,inplace=True)
table_5["raw_chem_name"]=table_5.iloc[:,0]
table_5["report_funcuse"]=table_5.iloc[:,1]
table_5["conc"]=table_5.iloc[:,2]
table_5['raw_cas']=''
table_5["raw_min_comp"]=''
table_5["raw_max_comp"]=''
for j in range(0, len(table_5)):
    table_5["conc"].iloc[j]=str(table_5["conc"].iloc[j]).replace("(","").replace(")","").replace("<","")
table_5=table_5.dropna(subset=["raw_chem_name"])
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
for j in range(0,len(table_5)):
    txt=str(table_5.loc[j,"conc"])
    txt2 = txt.split(' – ')[0]
    txt3 = txt.split(' – ')[1]
    table_5.loc[j,"raw_min_comp"] = txt2
    table_5.loc[j,"raw_max_comp"] = txt3
table_5.drop_duplicates(inplace=True)
table_5["data_document_id"]="1400355"
table_5["data_document_filename"]="Arizona 2013 Pesticide Report Table 5.pdf"
table_5["doc_date"]="2013"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]=""
table_5.to_csv("Arizona 2013 Pesticides Annual Report Table 5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","raw_min_comp","raw_max_comp","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)

#Table 6
i = 32
table = []
while i < 37:
    table_6=read_pdf("Arizona 2013 Pesticide Report Table 4.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
    table_6.drop([0,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],axis=1,inplace=True)
    table_6.drop([0,1,2,3,4],axis=0,inplace=True)
    table_6.reset_index(drop=True,inplace=True)
    table.append(table_6)
    i = i+1
table_6_37=read_pdf("Arizona 2013 Pesticide Report Table 4.pdf", pages=37, lattice=True, pandas_options={'header': None})[0]
table_6_37.drop([0,2,3,4,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],axis=1,inplace=True)
table_6_37.drop([0,1,2,3,4,13,14],axis=0,inplace=True)
table_6_37.reset_index(drop=True,inplace=True)
table.append(table_6_37)
table_6 = pd.concat(table,ignore_index=True)
table_6["raw_chem_name"]=table_6.iloc[:,1]
table_6.loc[17,"raw_chem_name"]=str(table_6.loc[17,"raw_chem_name"])+str(table_6.loc[18,"raw_chem_name"])
table_6.drop([18],axis=0,inplace=True)
table_6.reset_index(drop=True,inplace=True)
table_6["raw_chem_name"]=table_6["raw_chem_name"].replace(regex='\\r',value='')
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower()
table_6.drop_duplicates('raw_chem_name',inplace=True)
table_6["raw_cas"]=''
table_6["report_funcuse"]=table_6.iloc[:,0]
table_6["raw_central_comp"]=table_6.iloc[:,2]
table_6["raw_central_comp"]=table_6["raw_central_comp"].replace(regex=' ',value='')
table_6["data_document_id"]="1400356"
table_6["data_document_filename"]="Arizona 2013 Pesticide Report Table 6.pdf"
table_6["doc_date"]="2013"
table_6["raw_category"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]=""
table_6.to_csv("Arizona 2013 Pesticides Annual Report Table 6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","raw_central_comp","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
#Table 7
i = 38
table = []
while i < 48:
    table_7=read_pdf("Arizona 2013 Pesticide Report Table 4.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
    table_7.drop([0,1,2,3,4],axis=0,inplace=True)
    table_7.drop([0,1,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],axis=1,inplace=True)
    table_7.reset_index(drop=True,inplace=True)
    table.append(table_7)
    i = i+1
table_7_48=read_pdf("Arizona 2013 Pesticide Report Table 4.pdf", pages=48, lattice=True, pandas_options={'header': None})[0]
table_7_48.drop([0,1,2,3,4,5,24,25,26],axis=0,inplace=True)
table_7_48.drop([0,1,3,4,5,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],axis=1,inplace=True)
table_7_48.reset_index(drop=True,inplace=True)
table.append(table_7_48)
table_7 = pd.concat(table,ignore_index=True)
table_7["report_funcuse"]=table_7.iloc[:,0]
table_7["raw_chem_name"]=table_7.iloc[:,1]
#Need to combine rows that go over two pages
i = 0
while i < len(table_7):
    if(str(table_7.loc[i,"report_funcuse"])=="nan"):
        table_7.loc[i-1,"raw_chem_name"]=str(table_7.loc[i-1,"raw_chem_name"])+str(table_7.loc[i,"raw_chem_name"])
        table_7.drop([i],axis=0,inplace=True)
        table_7.reset_index(drop=True,inplace=True)
    else:
        i = i+1
table_7.loc[73,"raw_chem_name"]="Dimethylamine salt of dicamba"
table_7["raw_cas"]=''
table_7.reset_index(drop=True,inplace=True)
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).strip().lower()
table_7.drop_duplicates('raw_chem_name',inplace=True)
table_7["raw_central_comp"]=table_7.iloc[:,2]
table_7["raw_central_comp"]=table_7["raw_central_comp"].replace(regex=' ',value='')
table_7["data_document_id"]="1400357"
table_7["data_document_filename"]="Arizona 2013 Pesticide Report Table 7.pdf"
table_7["doc_date"]="2013"
table_7["raw_category"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]=""
table_7.to_csv("Arizona 2013 Pesticides Annual Report Table 7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","raw_central_comp","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"], index=False)
