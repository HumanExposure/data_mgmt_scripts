#lkoval
#updated 4/13/2020

import os
import string
import csv
import glob
import pandas as pd

os.chdir("L://Lab//HEM//Health Product Declaration//Lauren2")

filelist=glob.glob("*.txt")



#text was originally extracted in August 2019 for Kristin. After functionality was added in Factotum the output csv was revised to only include the fields that Factotum accepts, though the extraction itself was unchanged.



#make rr for factotum

# rr=pd.DataFrame()
# rr["filename"]=filelist
# rr.filename=rr.filename.str.replace(".txt",".pdf")
# rr["title"]=rr.filename.str.replace(".pdf","")
# rr["document_type"]="HD"
# rr["url"]=""
# rr["organization"]="Health Product Declaration Collaborative"
# rr.to_csv("hpd_2_rr.csv", index=False)


filenames=[]
prod_name_list=[]
date_list=[]
classification_list=[]
manufacturer_list=[]
component_list=[]
component_id_list=[]
component_per_list=[]
chem_name_list=[]
cas_list=[]
weight_per_list=[]
nano_list=[]
func_use_list=[]
prod_id_list=[]
product_id=0

for file in filelist:
    print(file)
    prod_name=""
    date=""
    classification=""
    manufacturer=""
    component=""
    chem_name=""
    cas=""
    weight_per=""
    nano=""
    func_use=""
    component_per=""
    x=len(chem_name_list)
    product_id+=1
    component_id=0

    prod_name_flag=False
    man_flag=False
    component_flag=False
    chem_name_flag=False
    sec2_flag=False
    func_use_flag=False
    weight_flag=False

    ifile=open(file)
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    for line in ifile:
        if line=='\n': continue
        cline=clean(line)
        cline=cline.lower()
        cline=cline.strip()
        cline=cline.split(" ")
        cline = [x.strip() for x in cline if x != ""]

        if "classification:" in cline:
            prod_name_flag=True

        if prod_name_flag==False:
            if "product" in cline:
                if "by" in cline:
                    prod_name=" ".join(cline[:cline.index("by")]).replace("tm","")
                elif "health" in cline:
                    prod_name=" ".join(cline[:cline.index("health")]).replace("tm","")
                elif cline[-1]=="product":
                    prod_name=" ".join(cline[:cline.index("product")]).replace("tm","")
                else:
                    prod_name=""


        if len(cline)>1 and ("release" in cline and "date:" in cline):
            if "*" in cline:
                date=" ".join(cline[cline.index("date:")+1:cline.index("*")])
            else:
                date=" ".join(cline[cline.index("date:")+1:])

        if len(cline)>1 and (cline[0]=="section" and cline[1]=="2:"):
            sec2_flag=True

        if len(cline)>1 and (cline[0]=="section" and cline[1]=="3:"):
            sec2_flag=False

        if "classification:" in cline:
            if "created" in cline:
                classification=" ".join(cline[cline.index("classification:")+1: cline.index("created")])
            else:
                classification=" ".join(cline[cline.index("classification:")+1:])

        if "manufacturer:" in cline:
            man_flag=True

        if "address:" in cline:
            man_flag=False

        if man_flag==True:
            if "contact" in cline:
                manufacturer=" ".join(cline[cline.index("manufacturer:")+1: cline.index("contact")])
                man_flag=False
            else:
                manufacturer=" ".join(cline[cline.index("manufacturer:")+1:])
                man_flag=False
        if sec2_flag==True:
            if len(cline)>1 and ("hpd" in cline and "%:" in cline and "url:" in cline):
                component_flag=True

            if len(cline)>1 and ("inventory" in cline and "threshold:" in cline and "residuals" in cline):
                component_flag=False
                component_id+=1

            if component_flag==True:
                if len(cline)>1 and ("hpd" in cline and "%:" in cline and "url:" in cline):
                    component=" ".join(cline[:cline.index("%:")])
                    component_per="".join(cline[cline.index("%:")+1: cline.index("hpd")])
                else:
                    component=component+" "+" ".join(cline)


            if "id:" in cline:
                chem_name_flag=True

            if "%:" in cline or "notes:" in cline:
                chem_name_flag=False
            if chem_name_flag==True:
                if  "id:" in cline:
                    chem_name=" ".join(cline[:cline.index("id:")])
                    chem_name_list.append(chem_name)
                    cas=" ".join(cline[cline.index("id:")+1:])
                    cas_list.append(cas)
                    component_list.append(component)
                    component_id_list.append(component_id)
                    component_per_list.append(component_per)
                elif "%:" not in cline and "created" not in cline:
                    chem_name=chem_name+" "+" ".join(cline)
                    chem_name_list[len(chem_name_list)-1]=chem_name
                    chem_name_flag=False

            if len(cline)==1 and cline[0]=="undisclosed":
                chem_name=cline[0]
                chem_name_list.append(chem_name)
                cas=""
                cas_list.append(cas)
                component_list.append(component)
                component_id_list.append(component_id)
                component_per_list.append(component_per)

            if len(cline)>1 and ("%:" in cline and "gs:" in cline and "rc:" in cline):
                func_use_flag=True

            if "hazards:" in cline or "created" in cline:
                    func_use_flag=False

            if func_use_flag==True:
                if len(cline)>1 and ("%:" in cline and "gs:" in cline and "rc:" in cline):
                    func_use=" ".join(cline[cline.index("role:")+1:])
                    func_use_list.append(func_use)

                elif len(cline)==1:
                    func_use=func_use+" "+cline[0]
                    func_use_list[len(func_use_list)-1]=func_use

                elif len(cline)>1 and "hazards:" not in cline:
                    func_use=func_use+" "+" ".join(cline)
                    func_use_list[len(func_use_list)-1]=func_use

            if "id:" in cline or (len(cline)==1 and cline[0]=="undisclosed"):
                weight_flag=True

            if weight_flag==True:
                if cline[0]=="%:":
                    weight_per=" ".join(cline[cline.index("%:")+1: cline.index("gs:")])
                    if cline[cline.index("nano:")+1]=="no":
                        nano="N"
                    elif cline[cline.index("nano:")+1]=="yes":
                        nano="Y"
                    else:
                        nano=""
                    weight_per_list.append(weight_per)
                    nano_list.append(nano)
                    weight_flag=False

                elif cline[0]!="%:" and ("id:" not in cline and "created" not in cline and "undisclosed" not in cline):
                    if "substance" in cline:
                        weight_flag=False

    manufacturer_list=manufacturer_list+([manufacturer]*(len(chem_name_list)-x))
    filenames=filenames+([file.replace(".txt",".pdf")]*(len(chem_name_list)-x))
    prod_name_list=prod_name_list+([prod_name]*(len(chem_name_list)-x))
    prod_id_list=prod_id_list+([product_id]*(len(chem_name_list)-x))
    date_list=date_list+([date]*(len(chem_name_list)-x))
    classification_list=classification_list+([classification]*(len(chem_name_list)-x))

    df=pd.DataFrame()
    df["filename"]=filenames
    df["prod_id"]=prod_id_list
    df["prod_name"]=prod_name_list
    df["date"]=date_list
    df["classification"]=classification_list
    df["manufacturer"]=manufacturer_list
    df["component_id"]=component_id_list
    df["component"]=component_list
    df["component_per"]=component_per_list
    df["chem_name"]=chem_name_list
    df["cas"]=cas_list
    df["weight_per"]=weight_per_list
    df["raw_min_comp"]=""
    df["raw_central_comp"]=""
    df["raw_max_comp"]=""
    df["nano"]=nano_list
    df["func_use"]=func_use_list

    #add factotum fields    
    df["rev_num"]=""
    df["raw_category"]=""
    df["unit_type"]=""
    df["ingredient_rank"]=""




df["component_id"]=df["component_id"].replace(0, "")
for i in range(len(df)):
    if "-" in df["weight_per"].iloc[i].strip().replace("%",""):
        df["raw_min_comp"].iloc[i]="".join(df["weight_per"].iloc[i][:df["weight_per"].iloc[i].index("-")]).strip().replace("%","")
        df["raw_max_comp"].iloc[i]="".join(df["weight_per"].iloc[i][df["weight_per"].iloc[i].index("-")+1:]).strip().replace("%","")

    else:
        df["raw_central_comp"].iloc[i]=df["weight_per"].iloc[i].strip().replace("%","")


#make df of only the fields factotum accepts
df=df[["filename","prod_name","date","rev_num","raw_category","cas","chem_name","func_use","raw_min_comp","raw_max_comp","unit_type","ingredient_rank","raw_central_comp","component"]]
df.rename(columns={"filename":"data_document_filename","date":"doc_date","cas":"raw_cas","chem_name":"raw_chem_name","func_use":"reported_funcuse"}, inplace=True)

#read in template to get document ids
os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents")
extracted_text_template=pd.read_csv("Health_Product_Declaration_2_unextracted_documents.csv", usecols=["data_document_id","data_document_filename"], dtype=str)

#put columns in order
df=df.merge(extracted_text_template, on="data_document_filename", how="left")
cols=df.columns[:-1]
cols=cols.insert(0,df.columns[-1])
df=df[cols]

df.to_csv("hpd2_lk.csv", index=False)
