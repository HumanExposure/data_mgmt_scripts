#lkoval
#4/23/19

import os, string, csv
import glob
import pandas as pd

#change directory to folder with files
os.chdir("L://Lab//HEM//Wetmore-PFAS-PDFs//Apollo Scientific Ltd")

#files with different format
bad_files=["B02463059_msds.txt","B02463060_msds.txt","B02480974_msds.txt"]

#make list of files in folder
filelist=glob.glob("*.txt")

#make list of files with same format
good_files=[]
for f in filelist:
    if f not in bad_files:
        good_files.append(f)

filenames=[]
rev_num_list=[]
compilation_date_list=[]
rev_date_list=[]
prod_name_list=[]
cas_list=[]
prod_code_list=[]
synonyms_list=[]
comp_list=[]
reqs_list=[]
storage_cond_list=[]
packaging_list=[]
end_use_list=[]
state_list=[]
color_list=[]
evaporation_list=[]
oxidising_list=[]
water_sol_list=[]
viscosity_list=[]
boil_pt_list=[]
melt_pt_list=[]
flam_lwr_list=[]
flam_upr_list=[]
flash_pt_list=[]
part_coeff_list=[]
autoflam_list=[]
vapor_pressure_list=[]
relative_density_list=[]
ph_list=[]
voc_gpl_list=[]
reactivity_list=[]
chem_stability_list=[]
haz_reactions_list=[]
cond_to_avoid_list=[]
mats_to_avoid_list=[]
haz_decomp_prods_list=[]


for file in good_files:
    rev_num=""
    compilation_date=""
    rev_date=""
    prod_name=""
    cas=""
    prod_code=""
    synonyms=""
    comp=""
    reqs=""
    storage_cond=""
    packaging=""
    end_use=""
    state=""
    color=""
    evaporation=""
    oxidising=""
    water_sol=""
    viscosity=""
    boil_pt=""
    melt_pt=""
    flam_lwr=""
    flam_upr=""
    flash_pt=""
    part_coeff=""
    autoflam=""
    vapor_pressure=""
    relative_density=""
    ph=""
    voc_gpl=""
    reactivity=""
    chem_stability=""
    haz_reactions=""
    cond_to_avoid=""
    mats_to_avoid=""
    haz_decomp_prods=""


    hand_flag=False
    conditions_flag=False
    properties_flag=False
    cas_flag=False
    reactivity_flag=False
    haz_rx_flag=False
    decomp_flag=False
    syn_flag=False

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

        for i in range(0,len(cline)):
            if cline[i]=="revision" and cline[i+1]=="no:":
                rev_num=cline[i+2]

            if cline[i]=="compilation" and cline[i+1]=="date:":
                compilation_date=cline[i+2]

            if cline[0]=="issued:":
                compilation_date=cline[1]

            if cline[i]=="revision" and cline[i+1]=="date:":
                rev_date=cline[i+2]

            if cline[i]=="product" and cline[i+1]=="name:":
                prod_name=" ".join(cline[i+2:])

            if cas_flag==False:
                if cline[i]=="cas" and cline[i+1]=="number:":
                    cas=cline[i+2]
                    cas_flag=True

            if cline[i]=="product" and cline[i+1]=="code:":
                prod_code=" ".join(cline[i+2:])

            if cline[i]=="company" and cline[i+1]=="name:":
                comp=" ".join(cline[i+2:])

            if cline[i]=="suitable" and cline[i+1]=="packaging:":
                packaging=" ".join(cline[i+2:])

            if cline[0]=="specific" and cline[1]=="end":
                end_use= " ".join(cline[3:])


            if cline[i]=="evaporation" and cline[i+1]=="rate:":
                evaporation=" ".join(cline[i+2:])

            if cline[i]=="colour:":
                color=" ".join(cline[i+1:])

            if cline[i]=="solubility" and cline[i+2]=="water:":
                water_sol=" ".join(cline[i+3:])

            if cline[i]=="viscosity:":
                viscosity=" ".join(cline[i+1:])

            if cline[i]=="boiling":
                if "melting" in cline:
                    boil_pt=" ".join(cline[i+2:cline.index("melting")])

                elif "relative" in cline:
                    boil_pt=" ".join(cline[i+2:cline.index("relative")])

                elif "flash" in cline:
                    boil_pt=" ".join(cline[i+2:cline.index("flash")])

                else:
                    boil_pt=" ".join(cline[i+2:])

            if cline[i]=="melting":
                if "relative" in cline:
                    melt_pt=" ".join(cline[i+2:cline.index("relative")])

                elif "flash" in cline:
                    melt_pt=" ".join(cline[i+2:cline.index("flash")])

                else:
                    melt_pt=" ".join(cline[cline.index("melting")+2:])

            if cline[i]=="flammability" and cline[i+3]=="lower:":
                try:
                    flam_lwr=" ".join(cline[i+4: cline.index("upper:")])
                except:
                    flam_lwr=" ".join(cline[i+4:])

            if cline[i]=="upper:":
                flam_upr=" ".join(cline[cline.index("upper:")+1:])

            if cline[i]=="flash":
                if "part.coeff." in cline:
                    flash_pt=" ".join(cline[i+2:cline.index("part.coeff.")])
                elif "relative" in cline:
                    flash_pt=" ".join(cline[i+2:cline.index("relative")])

                elif "vapour" in cline:
                    flash_pt=" ".join(cline[i+2:cline.index("vapour")])

                else:
                    flash_pt=" ".join(cline[i+2:])

            if "part.coeff" in cline[i]:
                part_coeff=" ".join(cline[cline.index("part.coeff.")+2:])

            if "autoflam" in cline[i]:
                try:
                    autoflam=" ".join(cline[i+1: cline.index("vapour")])
                except:
                    autoflam=" ".join(cline[i+1:])

            if cline[i]=="vapour" and cline[i+1]=="pressure:":
                if "relative" in cline:
                    vapor_pressure=" ".join(cline[i+2: cline.index("relative")])
                else:
                    vapor_pressure=" ".join(cline[cline.index("vapour")+2:])

            if cline[i]=="relative" and cline[i+1]=="density:":
                if "ph:" in cline:
                    relative_density=" ".join(cline[i+2: cline.index("ph:")])
                else:
                    relative_density=" ".join(cline[i+2:])

            if cline[i]=="ph:":
                if "voc" in cline:
                    ph=" ".join(cline[i+1: cline.index("voc")])
                else:
                    ph=" ".join(cline[i+1:])

            if cline[i]=="voc" and cline[i+1]=="g/l:":
                voc_gpl=" ".join(cline[i+2:])



        if cline[0]=="synonyms:":
            syn_flag=True

        if syn_flag==True:
            if cline[0]=="1.2.":
                syn_flag=False
            else:
                if synonyms=="":
                    synonyms=synonyms+" ".join(cline[1:])
                else:
                    synonyms=synonyms+"; "+" ".join(cline)

        if cline[0]=="handling" and cline[1]=="requirements:":
            hand_flag=True

        if hand_flag==True:
            if cline[0]=="7.2." or cline[0]=="[cont...]" or cline[0]=="storage":
                hand_flag=False
            else:
                if reqs=="":
                    reqs=reqs+" ".join(cline[2:])
                else:
                    reqs=reqs+" "+" ".join(cline)

        if (cline[0]=="storage" and cline[1]=="conditions:"):
            conditions_flag=True

        if conditions_flag==True:
            if cline[0]=="suitable" or "[cont...]" in cline:
                conditions_flag=False
            else:
                if storage_cond=="":
                    storage_cond=" ".join(cline[2:])
                else:
                    storage_cond=storage_cond+" "+" ".join(cline)



        if "state:" in cline:
            properties_flag=True

        if properties_flag==True:
            if "10" in cline:
                properties_flag=False

            if cline[0]=="state:":
                state=" ".join(cline[1:])

            if cline[0]=="oxidising:":
                oxidising=" ".join(cline[1:])



        if "stability" in cline and "reactivity" in cline:
            reactivity_flag=True

        if reactivity_flag==True:
            if "11" in cline:
                reactivity_flag=False

            if "reactivity:" in cline:
                reactivity=" ".join(cline[1:])

            if cline[0]=="stability:":
                chem_stability=" ".join(cline[1:])

            if cline[0]=="chemical" and cline[1]=="stability:":
                chem_stability=" ".join(cline[2:])

            if cline[0]=="conditions" and cline[2]=="avoid:":
                cond_to_avoid=" ".join(cline[3:])

            if cline[0]=="materials" and cline[2]=="avoid:":
                mats_to_avoid=" ".join(cline[3:])


        if cline[0]=="hazardous" and cline[1]=="reactions:":
            haz_rx_flag=True

        if haz_rx_flag==True:
            if cline[0]=="10.4." or "[cont...]" in cline:
                haz_rx_flag=False
            else:
                if haz_reactions=="":
                    haz_reactions=haz_reactions+" ".join(cline[2:])
                else:
                    haz_reactions=haz_reactions+" "+" ".join(cline)

        if cline[0]=="haz." and cline[2]=="products:":
            decomp_flag=True

        if decomp_flag==True:
            if "toxicological" in cline or "[cont...]" in cline:
                decomp_flag=False
            else:
                if haz_decomp_prods=="":
                    haz_decomp_prods=" ".join(cline[3:])
                else:
                    haz_decomp_prods=haz_decomp_prods+" "+" ".join(cline)


    file=file.replace(".txt",".pdf")
    filenames.append(file)
    rev_num_list.append(rev_num)
    rev_date_list.append(rev_date)
    compilation_date_list.append(compilation_date)
    prod_name_list.append(prod_name)
    cas_list.append(cas)
    prod_code_list.append(prod_code)
    synonyms_list.append(synonyms)
    comp_list.append(comp)
    reqs_list.append(reqs)
    storage_cond_list.append(storage_cond)
    packaging_list.append(packaging)
    end_use_list.append(end_use)
    state_list.append(state)
    color_list.append(color)
    evaporation_list.append(evaporation)
    oxidising_list.append(oxidising)
    water_sol_list.append(water_sol)
    viscosity_list.append(viscosity)
    boil_pt_list.append(boil_pt)
    melt_pt_list.append(melt_pt)
    flam_lwr_list.append(flam_lwr)
    flam_upr_list.append(flam_upr)
    flash_pt_list.append(flash_pt)
    part_coeff_list.append(part_coeff)
    autoflam_list.append(autoflam)
    vapor_pressure_list.append(vapor_pressure)
    relative_density_list.append(relative_density)
    ph_list.append(ph)
    voc_gpl_list.append(voc_gpl)
    reactivity_list.append(reactivity)
    chem_stability_list.append(chem_stability)
    haz_reactions_list.append(haz_reactions)
    cond_to_avoid_list.append(cond_to_avoid)
    mats_to_avoid_list.append(mats_to_avoid)
    haz_decomp_prods_list.append(haz_decomp_prods)


df=pd.DataFrame()
df=df.assign(filename=filenames, compilation_date=compilation_date_list, rev_date=rev_date_list, revision_num=rev_num_list, product_name=prod_name_list, cas=cas_list, products_code=prod_code_list, synonyms=synonyms_list, company=comp_list, handling_requirements=reqs_list, storage_conditions=storage_cond_list, suitable_packaging=packaging_list, specific_end_use=end_use_list, state=state_list, color=color_list, evaporation_rate=evaporation_list, oxidising=oxidising_list, solubility_in_water=water_sol_list, viscosity=viscosity_list, boiling_pt_celsius=boil_pt_list, melting_pt_celsius=melt_pt_list, flammability_lwr_limit_percent=flam_lwr_list, flammability_upr_limit_percent=flam_upr_list, flash_pt_celsius=flash_pt_list, part_coeff_n_octal_water=part_coeff_list, autoflammability=autoflam_list, vapor_pressure=vapor_pressure_list, relative_density=relative_density_list, ph=ph_list, voc_gpl=voc_gpl_list,  reactivity=reactivity_list, chem_stability=chem_stability_list, hazardous_reactions=haz_reactions_list, conditions_to_avoid=cond_to_avoid_list, materials_to_avoid=mats_to_avoid_list, hazardous_decomoposition_products=haz_decomp_prods_list)



df.to_excel("C://Users//lkoval//Documents//wetmore extractions//apollo scientific ltd.xlsx", index=False)
