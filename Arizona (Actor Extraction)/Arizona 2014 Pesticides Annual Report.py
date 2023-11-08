#Michael Metcalf
#Arizona 2014
#11-01-2023
#Imports
from tabula import read_pdf
import pandas as pd
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Arizona 2014')
table = []
table_2=read_pdf("Arizona 2014 Pesticide Report Table 2.pdf", pages=5, lattice=False, pandas_options={'header': None})[0]
table_2.drop([0,1,2,3],axis=0,inplace=True)
table_2.drop([0,3,4],axis=1,inplace=True)
table_2.reset_index(drop=True,inplace=True)
table.append(table_2)
table_2_2=read_pdf("Arizona 2014 Pesticide Report Table 2.pdf", pages=6, lattice=True, pandas_options={'header': None})[0]
table_2_2.drop([0,1,2,3,4],axis=0,inplace=True)
table_2_2.drop([0,3,4],axis=1,inplace=True)
table_2_2.reset_index(drop=True,inplace=True)
table.append(table_2_2)
table_2_3=read_pdf("Arizona 2014 Pesticide Report Table 2.pdf", pages=7, lattice=True, pandas_options={'header': None})[0]
table_2_3.drop([0,1,2,3,4],axis=0,inplace=True)
table_2_3.drop([0,3,4],axis=1,inplace=True)
table_2_3.reset_index(drop=True,inplace=True)
table.append(table_2_3)
table_2 = pd.concat(table,ignore_index=True)
table_2["raw_chem_name"]=table_2.iloc[:,0]
table_2["raw_chem_name"]=table_2["raw_chem_name"].replace(regex='\\r',value=' ')
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
table_2["report_funcuse"]=table_2.iloc[:,1]
for j in range(0,len(table_2)):
    txt=str(table_2.loc[j,"report_funcuse"])
    txt2 = txt.split(' ')[0]
    table_2.loc[j,"report_funcuse"]=txt2
table_2.loc[8,"report_funcuse"]="Herbicide"
table_2.loc[10,"report_funcuse"]="Biocontrol agent"
table_2.loc[12,"report_funcuse"]="germicidal cleaner"
table_2.loc[13,"report_funcuse"]="germicidal cleaner"
table_2.loc[14,"report_funcuse"]="germicidal cleaner"
table_2.loc[15,"report_funcuse"]="Biological insecticide"
table_2.loc[16,"report_funcuse"]="Systemic fungicide"
table_2.loc[17,"report_funcuse"]="plant growth regulator"
table_2.loc[19,"report_funcuse"]="Bird repellent"
table_2.loc[20,"report_funcuse"]="herbicide"
table_2.loc[22,"report_funcuse"]="fungicide"
table_2.loc[23,"report_funcuse"]="fungicide"
table_2.loc[25,"report_funcuse"]="herbicide"
table_2.loc[26,"report_funcuse"]="herbicide"
table_2.loc[27,"report_funcuse"]="Biological herbicide"
table_2["raw_cas"]=''
table_2["data_document_id"]="1400358"
table_2["data_document_filename"]="Arizona 2014 Pesticide Report Table 2.pdf"
table_2["doc_date"]="2014"
table_2["raw_category"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]=""
table_2["component"]=""
table_2["chem_detected_flag"]=""
table_2["author"]=""
table_2["doi"]=""
table_2.to_csv("Arizona 2014 Pesticides Annual Report Table 2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

#Table 3
table = []
table_3_1=read_pdf("Arizona 2014 Pesticide Report Table 3.pdf", pages="8", lattice=True, pandas_options={'header': None})[0]
table_3_2=read_pdf("Arizona 2014 Pesticide Report Table 3.pdf", pages="9", lattice=True, pandas_options={'header': None})[0]
table_3_3=read_pdf("Arizona 2014 Pesticide Report Table 3.pdf", pages="10", lattice=True, pandas_options={'header': None})[0]
table_3_4=read_pdf("Arizona 2014 Pesticide Report Table 3.pdf", pages="11", lattice=True, pandas_options={'header': None})[0]

table_3_1.drop([0,1,2,3],axis=0,inplace=True)
table_3_1.drop([0,1,3],axis=1,inplace=True)
table_3_1.reset_index(drop=True,inplace=True)
#Need to add 2 to the names of several chemcials
i = 0
while i < 8:
    table_3_1.iloc[i,1] = "2" + str(table_3_1.iloc[i,1])
    i = i + 1
table_3_1.iloc[8,1] = "Acibenzolar-S-Methyl"
table_3_1.iloc[9,1] = "Amicarbazone"
table.append(table_3_1)

table_3_2.drop([0,1,2,3],axis=0,inplace=True)
table_3_2.drop([0,1,3],axis=1,inplace=True)
table_3_2.reset_index(drop=True,inplace=True)
table.append(table_3_2)
table_3_3.drop([0,1,2,3],axis=0,inplace=True)
table_3_3.drop([0,1,3],axis=1,inplace=True)
table_3_3.reset_index(drop=True,inplace=True)
table.append(table_3_3)
table_3_4.drop([0,1,2,3],axis=0,inplace=True)
table_3_4.drop([0,1,3],axis=1,inplace=True)
table_3_4.reset_index(drop=True,inplace=True)
table.append(table_3_4)
tables = [table_3_1,table_3_2,table_3_3,table_3_4]
table_3 = pd.concat(table,ignore_index=True)
table_3["raw_cas"]=table_3.iloc[:,0]
table_3["raw_chem_name"]=table_3.iloc[:,1]
table_3=table_3.dropna(subset=["raw_chem_name"])
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
table_3["data_document_id"]="1400359"
table_3["data_document_filename"]="Arizona 2014 Pesticide Report Table 3.pdf"
table_3["doc_date"]="2014"
table_3["raw_category"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]=""
table_3["report_funcuse"]=""
table_3["component"]=""
table_3["chem_detected_flag"]=""
table_3["author"]=""
table_3["doi"]=""
#Exporting to CSV
table_3.to_csv("Arizona 2014 Pesticides Annual Report Table 3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

#Table 4
i = 12
table = []
while i < 54:
    table_4=read_pdf("Arizona 2014 Pesticide Report Table 4.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
    table.append(table_4)
    table_4=read_pdf("Arizona 2014 Pesticide Report Table 4.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[1]
    table.append(table_4)
    i = i + 1

table_4=pd.concat(table,ignore_index=True)
table_4.drop([0,1,2,3,6,7,8,9,10,11,12,13,14,15,16,17],axis=1,inplace=True)
table_4.reset_index(drop=True,inplace=True)

table_4["raw_cas"] = table_4.iloc[:,0]
table_4["raw_chem_name"] = table_4.iloc[:,1]

i = 0
while i < len(table_4):
    if(str(table_4.loc[i,"raw_chem_name"])=="nan"):
        table_4.drop([i],axis=0,inplace=True)
        table_4.reset_index(drop=True,inplace=True)
    else:
        i = i+1

i = 0
while i < len(table_4):
    if(str(table_4.loc[i,"raw_cas"])=="nan"):
        table_4.loc[i-1,"raw_chem_name"]=str(table_4.loc[i-1,"raw_chem_name"])+str(table_4.loc[i,"raw_chem_name"])
        table_4.drop([i],axis=0,inplace=True)
        table_4.reset_index(drop=True,inplace=True)
    else:
        i = i+1
table_4=table_4.dropna(subset=["raw_chem_name"])
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace("*","")
table_4["data_document_id"]="1400360"
table_4["data_document_filename"]="Arizona 2014 Pesticide Report Table 4.pdf"
table_4["doc_date"]="2014"
table_4["raw_category"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]=""
table_4["report_funcuse"]=""
table_4["component"]=""
table_4["chem_detected_flag"]=""
table_4["author"]=""
table_4["doi"]=""
table_4.to_csv("Arizona 2014 Pesticides Annual Report Table 4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"], index=False)

#Table 5
table = []
table_5=read_pdf("Arizona 2014 Pesticide Report Table 5.pdf", pages=54, lattice=True, pandas_options={'header': None})[0]
table_5.drop([0,1,2,3,4],axis=0,inplace=True)
table_5.drop([3,4,5,6],axis=1,inplace=True)
table_5.reset_index(drop=True,inplace=True)
table.append(table_5)
table_5=read_pdf("Arizona 2014 Pesticide Report Table 5.pdf", pages=55, lattice=True, pandas_options={'header': None})[0]
table_5.drop([0,1,2,3,4],axis=0,inplace=True)
table_5.drop([3,4,5,6],axis=1,inplace=True)
table_5.reset_index(drop=True,inplace=True)
table.append(table_5)
table_5 = pd.concat(table,ignore_index=True)

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
table_5["data_document_id"]="1400361"
table_5["data_document_filename"]="Arizona 2014 Pesticide Report Table 5.pdf"
table_5["doc_date"]="2014"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]=""
table_5["component"]=""
table_5["chem_detected_flag"]=""
table_5["author"]=""
table_5["doi"]=""
table_5.to_csv("Arizona 2014 Pesticides Annual Report Table 5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","raw_min_comp","raw_max_comp","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse","component","chem_detected_flag","author","doi"], index=False)

#Table 6
i = 57
table = []
while i < 64:
     table_6=read_pdf("Arizona 2014 Pesticide Report Table 6.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
     table.append(table_6)
     table_6=read_pdf("Arizona 2014 Pesticide Report Table 6.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[1]
     table.append(table_6)
     i = i + 1
table_6 = pd.concat(table,ignore_index=True)

j = 0
while j < len(table_6):
    if(str(table_6.iloc[j,10])=="nan" or str(table_6.iloc[j,10])=="Applied"):
        table_6.drop([j],axis=0,inplace=True)
        table_6.reset_index(drop=True,inplace=True)
    elif(str(table_6.iloc[j,0])=="Product Brand Name"):
        table_6.drop([j],axis=0,inplace=True)
        table_6.reset_index(drop=True,inplace=True)
    else:
        j = j + 1
table_6.drop([0,2,3,4,7,8,9,10,11],axis=1,inplace=True)
table_6.reset_index(drop=True,inplace=True)
table_6["raw_chem_name"]=table_6.iloc[:,1]
table_6.loc[39,"raw_chem_name"]=str(table_6.loc[39,"raw_chem_name"])+str(table_6.loc[40,"raw_chem_name"])
table_6.drop([40],axis=0,inplace=True)
table_6.reset_index(drop=True,inplace=True)
table_6["raw_chem_name"]=table_6["raw_chem_name"].replace(regex='\\r',value='')
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower()
table_6["raw_cas"]=''
table_6["report_funcuse"]=table_6.iloc[:,0]
table_6["raw_central_comp"]=table_6.iloc[:,2]
table_6["raw_central_comp"]=table_6["raw_central_comp"].replace(regex=' ',value='')
table_6["data_document_id"]="1400362"
table_6["data_document_filename"]="Arizona 2014 Pesticide Report Table 6.pdf"
table_6["doc_date"]="2014"
table_6["raw_category"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]=""
table_6["component"]=""
table_6["chem_detected_flag"]=""
table_6["author"]=""
table_6["doi"]=""
table_6.to_csv("Arizona 2014 Pesticides Annual Report Table 6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","raw_central_comp","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse","component","chem_detected_flag","author","doi"], index=False)

#Table_7
i = 64
table = []
while i < 76:
     table_7=read_pdf("Arizona 2014 Pesticide Report Table 7.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[0]
     table.append(table_7)
     table_7=read_pdf("Arizona 2014 Pesticide Report Table 7.pdf", pages=str(i), lattice=True, pandas_options={'header': None})[1]
     table.append(table_7)
     i = i + 1
table_7 = pd.concat(table,ignore_index=True)
table_7.drop([0,1,3,4,5,8,9,10,11,12],axis=1,inplace=True)

i = 0
while i < len(table_7):
    if(str(table_7.iloc[i,1])=="nan"):
        table_7.drop([i],inplace=True)
        table_7.reset_index(drop=True,inplace=True)
    elif(str(table_7.iloc[i,1])=="Active Ingredient"):
        table_7.drop([i],inplace=True)
        table_7.reset_index(drop=True,inplace=True)
    else:
        i = i + 1
table_7["report_funcuse"]=table_7.iloc[:,0]
table_7["raw_chem_name"]=table_7.iloc[:,1]
table_7['raw_cas']=''
#Need to combine rows that go over two pages
table_7.loc[101,"raw_chem_name"] = str(table_7.loc[101,"raw_chem_name"]) + str(table_7.loc[102,"raw_chem_name"])
table_7.drop([102],axis=0,inplace=True)
table_7.loc[145,"raw_chem_name"] = str(table_7.loc[145,"raw_chem_name"]) + str(table_7.loc[146,"raw_chem_name"])
table_7.drop([146],axis=0,inplace=True)
table_7.loc[167,"raw_chem_name"] = str(table_7.loc[167,"raw_chem_name"]) + str(table_7.loc[168,"raw_chem_name"])
table_7.drop([168],axis=0,inplace=True)
table_7.reset_index(drop=True,inplace=True)
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).strip().lower()
table_7["raw_central_comp"]=table_7.iloc[:,2]
table_7["raw_central_comp"]=table_7["raw_central_comp"].replace(regex=' ',value='')
table_7["data_document_id"]="1400363"
table_7["data_document_filename"]="Arizona 2014 Pesticide Report Table 7.pdf"
table_7["doc_date"]="2014"
table_7["raw_category"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]=""
table_7["component"]=""
table_7["chem_detected_flag"]=""
table_7["author"]=""
table_7["doi"]=""
table_7.to_csv("Arizona 2014 Pesticides Annual Report Table 7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","raw_central_comp","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse","component","chem_detected_flag","author","doi"], index=False)
# %%
