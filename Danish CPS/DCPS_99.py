#lkoval
#5-7-19

from tabula import read_pdf
import pandas as pd
import string

#Table 3_1
table_3_1=read_pdf("document_1372246.pdf", pages="27", lattice=False, pandas_options={'header': None})
table_3_1["raw_cas"]=table_3_1.iloc[:,0]
table_3_1["raw_chem_name"]=table_3_1.iloc[:,1]
table_3_1=table_3_1.loc[table_3_1["raw_chem_name"]!= "Substance name"]
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]
table_3_1=table_3_1.dropna(how="all")
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[i]=table_3_1["raw_chem_name"].iloc[i].lower().strip().replace("α","alpha").replace("ω","omega")
    table_3_1["raw_chem_name"].iloc[i]=clean(table_3_1["raw_chem_name"].iloc[i])
    if str(table_3_1["raw_cas"].iloc[i])=="nan":
        table_3_1["raw_chem_name"].iloc[i]=table_3_1["raw_chem_name"].iloc[i-1]+table_3_1["raw_chem_name"].iloc[i]
        table_3_1["raw_cas"].iloc[i]=table_3_1["raw_cas"].iloc[i-1]
        i_drop.append(i-1)

table_3_1=table_3_1.drop(i_drop)

table_3_1["data_document_id"]="1372246"
table_3_1["data_document_filename"]="DCPS_99_a.pdf"
table_3_1["doc_date"]="2008"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1.to_csv("DCPS_99_table_3_1.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_2
table_3_2=read_pdf("document_1372247.pdf", pages="28-30", lattice=False, pandas_options={'header': None})
table_3_2["raw_cas"]=table_3_2.iloc[:,0]
table_3_2["raw_chem_name"]=table_3_2.iloc[:,1]
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!= "Fluorinated compound"]
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]
table_3_2=table_3_2.dropna(how="all")
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i].lower().strip().replace("α","alpha").replace("ω","omega").replace("γ","gamma")
    table_3_2["raw_chem_name"].iloc[i]=clean(table_3_2["raw_chem_name"].iloc[i])
    if str(table_3_2["raw_cas"].iloc[i])=="355-42-0":
        continue
    elif str(table_3_2["raw_cas"].iloc[i])!="nan" and (str(table_3_2["raw_cas"].iloc[i+1])=="nan" and str(table_3_2["raw_cas"].iloc[i-1]!="nan")):
        table_3_2["raw_cas"].iloc[i-1]=str(table_3_2["raw_cas"].iloc[i-1])+str(table_3_2["raw_cas"].iloc[i])
        table_3_2["raw_cas"].iloc[i]="nan"
    elif str(table_3_2["raw_cas"].iloc[i])!="nan" and table_3_2["raw_chem_name"].iloc[i].split()[0]=="oecd:" or table_3_2["raw_chem_name"].iloc[i].split()[0]=="butanesulfonate":
        table_3_2["raw_cas"].iloc[i-1]=str(table_3_2["raw_cas"].iloc[i-1])+str(table_3_2["raw_cas"].iloc[i])
        table_3_2["raw_cas"].iloc[i]="nan"

    if str(table_3_2["raw_cas"].iloc[i])=="nan":
        table_3_2["raw_chem_name"].iloc[i]=table_3_2["raw_chem_name"].iloc[i-1]+" "+table_3_2["raw_chem_name"].iloc[i]
        table_3_2["raw_cas"].iloc[i]=table_3_2["raw_cas"].iloc[i-1]
        i_drop.append(i-1)

table_3_2=table_3_2.drop(i_drop)
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_cas","raw_chem_name"]]

for j in range(0,len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=table_3_2["raw_chem_name"].iloc[j].strip("nan")
    correct_name_list=table_3_2["raw_chem_name"].iloc[j].split()
    if "oecd:" in correct_name_list:
        correct_name=" ".join(correct_name_list[1:correct_name_list.index("oecd:")])
        table_3_2["raw_chem_name"].iloc[j]=correct_name
    else:
        table_3_2["raw_chem_name"].iloc[j]=" ".join(correct_name_list[1:])



table_3_2["data_document_id"]="1372247"
table_3_2["data_document_filename"]="DCPS_99_b.pdf"
table_3_2["doc_date"]="2008"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("DCPS_99_table_3_2.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 3_3
table_3_3=read_pdf("document_1372248.pdf", pages="32-36", lattice=False, pandas_options={'header': None})
table_3_3["raw_cas"]=table_3_3.iloc[:,0]
table_3_3["raw_chem_name"]=table_3_3.iloc[:,1]
table_3_3=table_3_3.loc[table_3_3["raw_chem_name"]!= "Substance name"]
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]
table_3_3=table_3_3.dropna(how="all")
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i].lower().strip().replace("α","alpha").replace("ω","omega").replace("γ","gamma").replace("β","beta").replace("ε","epsilon").replace("δ","delta")
    table_3_3["raw_chem_name"].iloc[i]=clean(table_3_3["raw_chem_name"].iloc[i])

    if str(table_3_3["raw_cas"].iloc[i])=="65530-83-8":
        table_3_3["raw_chem_name"].iloc[i]=table_3_3["raw_chem_name"].iloc[i]+" "+table_3_3["raw_chem_name"].iloc[i+1]+" "+table_3_3["raw_chem_name"].iloc[i+2]
        table_3_3["raw_cas"].iloc[i+1]=""
        table_3_3["raw_cas"].iloc[i+2]=""
        i_drop.append(i+1)
        i_drop.append(i+2)

    elif str(table_3_3["raw_cas"].iloc[i])=="nan" and (str(table_3_3["raw_cas"].iloc[i+1])=="nan" and table_3_3["raw_chem_name"].iloc[i+1].split()[0]!= "thiols,"):
        table_3_3["raw_chem_name"].iloc[i+1]=table_3_3["raw_chem_name"].iloc[i]+" "+table_3_3["raw_chem_name"].iloc[i+1]
        i_drop.append(i)

table_3_3=table_3_3.drop(i_drop)
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_cas","raw_chem_name"]]

j_drop=[]
for j in range(0,len(table_3_3)):
    if str(table_3_3["raw_cas"].iloc[j])=="nan":
        table_3_3["raw_chem_name"].iloc[j]=table_3_3["raw_chem_name"].iloc[j]+" "+table_3_3["raw_chem_name"].iloc[j+1]
        table_3_3["raw_cas"].iloc[j]=table_3_3["raw_cas"].iloc[j+1]
        j_drop.append(j+1)

table_3_3=table_3_3.drop(j_drop)
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_cas","raw_chem_name"]]

table_3_3["data_document_id"]="1372248"
table_3_3["data_document_filename"]="DCPS_99_c.pdf"
table_3_3["doc_date"]="2008"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("DCPS_99_table_3_3.csv",columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
