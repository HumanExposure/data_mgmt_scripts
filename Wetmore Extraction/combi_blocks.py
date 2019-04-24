#lkoval
#4/24/19

import os, string, csv
import glob
import pandas as pd

#change directory to file location
os.chdir("L://Lab//HEM//Wetmore-PFAS-PDFs//Combi-Blocks, Inc")

#get list of files
filelist=glob.glob("*.txt")
# filelist=["B02463025_MSDS.txt"]

filenames=[]
date_list=[]
prod_name_list=[]
synonyms_list=[]
catalog_num_list=[]
supp_list=[]
cas_list=[]
handling_reqs_list=[]
storage_reqs_list=[]
appearance_list=[]
boil_list=[]
melt_list=[]
flash_pt_list=[]
density_list=[]
molec_form_list=[]
molec_weight_list=[]
cond_to_avoid_list=[]
mats_to_avoid_list=[]
haz_combust_prods_list=[]


for file in filelist:
    date=""
    prod_name=""
    synonyms=""
    catalog_num=""
    supp=""
    cas=""
    handling_reqs=""
    storage_reqs=""
    appearance=""
    boil=""
    melt=""
    flash_pt=""
    density=""
    molec_form=""
    molec_weight=""
    cond_to_avoid=""
    mats_to_avoid=""
    haz_combust_prods=""

    hand_flag=False


    ifile=open(file)
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    for line in ifile:
        if line=='\n': continue
        cline=clean(line)
        cline=cline.lower()
        cline=cline.strip()
        cline=cline.split(" ")
        cline = [x.strip() for x in cline if x != ""]
        # print(cline)

        if "combi-blocks" in cline and "p.1" in cline:
            date=cline[0]

        if "product" in cline and "name:" in cline:
            prod_name=" ".join(cline[2:])

        if "synonyms:" in cline:
            synonyms=" ".join(cline[1:])

        if "catalog" in cline and "number:" in cline:
            catalog_num=" ".join(cline[2:])

        if "supplier:" in cline:
            supp=" ".join(cline[1:3])

        if "cas" in cline and "number:" in cline:
            cas=cline[2]

        if "handling:" in cline:
            hand_flag=True

        if hand_flag==True:
            if "storage:" in cline:
                hand_flag=False
            else:
                if handling_reqs=="":
                    handling_reqs=" ".join(cline[1:])
                else:
                    handling_reqs=handling_reqs+" "+" ".join(cline)

        if "storage:" in cline:
            storage_reqs=" ".join(cline[1:])

        if "appearance:" in cline:
            appearance=" ".join(cline[1:])

        if "boiling" in cline and "point:" in cline:
            boil=" ".join(cline[2:])

        if "melting" in cline and "point:" in cline:
            melt=" ".join(cline[2:])

        if "flash" in cline and "point:" in cline:
            flash_pt=" ".join(cline[2:])

        if "density:" in cline:
            density=" ".join(cline[1:])

        if "molecular" in cline and "formula:" in cline:
            molec_form="".join(cline[2:])

        if "molecular" in cline and "weight:" in cline:
            molec_weight=" ".join(cline[2:])

        if "conditions" in cline and "avoid:" in cline:
            cond_to_avoid=" ".join(cline[3:])

        if "materials" in cline and "avoid:" in cline:
            mats_to_avoid=" ".join(cline[3:])

        if "combustion" in cline and "products:" in cline:
            haz_combust_prods=" ".join(cline[4:])


    file=file.replace(".txt", ".pdf")
    filenames.append(file)
    date_list.append(date)
    prod_name_list.append(prod_name)
    synonyms_list.append(synonyms)
    catalog_num_list.append(catalog_num)
    supp_list.append(supp)
    cas_list.append(cas)
    handling_reqs_list.append(handling_reqs)
    storage_reqs_list.append(storage_reqs)
    appearance_list.append(appearance)
    boil_list.append(boil)
    melt_list.append(melt)
    flash_pt_list.append(flash_pt)
    density_list.append(density)
    molec_form_list.append(molec_form)
    molec_weight_list.append(molec_weight)
    cond_to_avoid_list.append(cond_to_avoid)
    mats_to_avoid_list.append(mats_to_avoid)
    haz_combust_prods_list.append(haz_combust_prods)


df=pd.DataFrame()
df=df.assign(filename=filenames, date=date_list, product_name=prod_name_list, synonyms=synonyms_list, catalog_number=catalog_num_list, supplier=supp_list, cas=cas_list, handling_requirements=handling_reqs_list, storage_requirements=storage_reqs_list, appearance=appearance_list, boiling_point=boil_list, melting_point=melt_list, flash_point=flash_pt_list, density=density_list, molecular_formula=molec_form_list, molecular_weight=molec_weight_list, conditions_to_avoid=cond_to_avoid_list, materials_to_avoid=mats_to_avoid_list, hazardous_combustion_products=haz_combust_prods_list)

df.to_excel("C://Users//lkoval//Documents//wetmore extractions//combi-blocks.xlsx", index=False)
