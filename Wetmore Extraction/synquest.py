#lkoval
#4/23/19

import os, string, csv
import glob
import pandas as pd

os.chdir("L://Lab//HEM//Wetmore-PFAS-PDFs//SynQuest Laboratories, Inc")

#files that were a different format. These were manually added to the spreadsheet after the script was run.
bad_files=["B02469222_MSDS.txt", "B02488489_msds.txt", "B02488507_msds.txt"]

#get files in directory
filelist=glob.glob("*.txt")

#make list of all files of the same format
good_files=[]
for f in filelist:
    if f not in bad_files:
        good_files.append(f)

filenames=[]
date_list=[]
version_list=[]
prod_form_list=[]
prod_name_list=[]
cas_list=[]
prod_code_list=[]
formula_list=[]
synonyms_list=[]
other_id_list=[]
handling_list=[]
hygiene_list=[]
technical_list=[]
storage_cond_list=[]
storage_area_list=[]
state_list=[]
color_list=[]
odor_list=[]
odor_threshold_list=[]
ph_list=[]
melt_pt_list=[]
freeze_pt_list=[]
boil_pt_list=[]
flash_pt_list=[]
evaporation_rate_list=[]
flammability_list=[]
explosion_limits_list=[]
explosive_props_list=[]
oxidising_list=[]
vapor_pressure_list=[]
rel_density_list=[]
rel_vapor_density_list=[]
specific_gravity_list=[]
molec_mass_list=[]
solubility_list=[]
log_pow_list=[]
autoignition_temp_list=[]
decomp_temp_list=[]
viscosity_list=[]
viscosity_k_list=[]
viscosity_d_list=[]
refractive_index_list=[]
reactivity_list=[]
chem_stability_list=[]
haz_reactions_list=[]
cond_to_avoid_list=[]
mats_to_avoid_list=[]
haz_decomp_prods_list=[]

for file in good_files:
    date=""
    version=""
    prod_form=""
    prod_name=""
    cas=""
    prod_code=""
    formula=""
    synonyms=""
    other_id=""
    handling=""
    hygiene=""
    technical=""
    storage_cond=""
    storage_area=""
    state=""
    color=""
    odor=""
    odor_threshold=""
    ph=""
    melt_pt=""
    freeze_pt=""
    boil_pt=""
    flash_pt=""
    evaporation_rate=""
    flammability=""
    explosion_limits=""
    explosive_props=""
    oxidising=""
    vapor_pressure=""
    rel_density=""
    rel_vapor_density=""
    specific_gravity=""
    molec_mass=""
    solubility=""
    log_pow=""
    autoignition_temp=""
    decomp_temp=""
    viscosity=""
    viscosity_k=""
    viscosity_d=""
    refractive_index=""
    reactivity=""
    chem_stability=""
    haz_reactions=""
    cond_to_avoid=""
    mats_to_avoid=""
    haz_decomp_prods=""

    cas_flag=False
    hand_flag=False
    storage_flag=False
    hygiene_flag=False
    reactivity_flag=False
    chem_stab_flag=False
    haz_rx_flag=False
    cond_to_avoid_flag=False
    mats_to_avoid_flag=False
    haz_decomp_flag=False


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

        if "date" in cline and "issue:" in cline:
            date=cline[3]

        if "version:" in cline:
            version=cline[5]

        if "product" in cline and "form" in cline:
            prod_form=" ".join(cline[3:])

        if "substance" in cline and "name" in cline:
            prod_name=" ".join(cline[3:])

        if cas_flag==False:
            if "cas" in cline:
                cas=cline[3]
                cas_flag=True

        if "product" in cline and "code" in cline:
            prod_code=" ".join(cline[3:])

        if "formula" in cline:
            formula=cline[2]

        if "synonyms" in cline:
            synonyms=" ".join(cline[2:])

        if "other" in cline and "identification" in cline:
            other_id=" ".join(cline[5:])

        if "precautions" in cline and "handling" in cline:
            hand_flag=True

        if hand_flag==True:
            if "hygiene" in cline:
                hand_flag=False
            else:
                if handling=="":
                    handling=" ".join(cline[5:])
                else:
                    handling=handling+" "+" ".join(cline)

        if "hygiene" in cline:
            hygiene_flag=True

        if hygiene_flag==True:
            if "7.2." in cline:
                hygiene_flag=False
            else:
                if hygiene=="":
                    hygiene=" ".join(cline[3:])
                else:
                    hygiene=hygiene+" "+" ".join(cline)

        if "technical" in cline and "measures" in cline:
            technical=" ".join(cline[3:])

        if cline[0]=="storage" and cline[1]=="conditions":
                storage_cond=" ".join(cline[3:])

        if "storage" in cline and "area" in cline:
            storage_area=" ".join(cline[3:])

        if "physical" in cline and "state" in cline:
            state=" ".join(cline[3:])

        if "color" in cline:
            color=" ".join(cline[2:])

        if cline[0]=="odor" and cline[1]!="threshold":
            odor=" ".join(cline[2:])

        if cline[0]=="odor" and cline[1]=="threshold":
            odor_threshold=" ".join(cline[3:])

        if "ph" in cline:
            ph=" ".join(cline[2:])

        if "melting" in cline:
            melt_pt=" ".join(cline[3:])

        if "freezing" in cline:
            freeze_pt=" ".join(cline[3:])

        if cline[0]=="boiling":
            boil_pt=" ".join(cline[3:])

        if cline[0]=="flash" and cline[2]==":":
            flash_pt=" ".join(cline[3:])

        if "evaporation" in cline and "rate" in cline:
            evaporation_rate=" ".join(cline[6:])

        if cline[0]=="flammability" and cline[1]!= ":":
            flammability=" ".join(cline[4:])

        if "explosion" in cline:
            explosion_limits=" ".join(cline[3:])

        if "explosive" in cline:
            explosive_props=" ".join(cline[3:])

        if cline[0]=="oxidizing" and cline[1]=="properties":
            oxidising=" ".join(cline[3:])

        if cline[0]=="vapor" and cline[1]=="pressure" and cline[2]==":":
            vapor_pressure=" ".join(cline[3:])

        if cline[0]=="relative" and cline[1]=="density":
            rel_density=" ".join(cline[3:])

        if cline[0]=="relative" and cline[1]=="vapor":
            rel_vapor_density=" ".join(cline[7:])

        if "specific" in cline and "gravity" in cline:
            specific_gravity=" ".join(cline[5:])

        if "molecular" in cline and "mass" in cline:
            molec_mass=" ".join(cline[3:])

        if "solubility" in cline:
            solubility=" ".join(cline[2:])

        if "log" in cline and "pow" in cline:
            log_pow=" ".join(cline[3:])

        if "auto-ignition" in cline:
            autoignition_temp=" ".join(cline[3:])

        if "decomposition" in cline and "temperature" in cline:
            decomp_temp=" ".join(cline[3:])

        if cline[0]=="viscosity" and cline[1]==":":
            viscosity=" ".join(cline[2:])

        if cline[0]=="viscosity," and cline[1]=="kinematic":
            viscosity_k=" ".join(cline[3:])

        if cline[0]=="viscosity," and cline[1]=="dynamic":
            viscosity_d=" ".join(cline[3:])

        if "refractive" in cline and "index" in cline:
            refractive_index=" ".join(cline[3:])

        if "10.1." in cline:
            reactivity_flag=True

        if reactivity_flag==True:
            if "10.2." in cline:
                reactivity_flag=False
            else:
                reactivity=reactivity+" "+" ".join(cline)

        if "10.2." in cline:
            chem_stab_flag=True

        if chem_stab_flag==True:
            if "10.3." in cline:
                chem_stab_flag=False
            else:
                chem_stability=chem_stability+" "+" ".join(cline)

        if "10.3." in cline:
            haz_rx_flag=True

        if haz_rx_flag==True:
            if "10.4." in cline:
                haz_rx_flag=False
            else:
                haz_reactions=haz_reactions+" "+" ".join(cline)

        if "10.4." in cline:
            cond_to_avoid_flag=True

        if cond_to_avoid_flag==True:
            if "10.5." in cline:
                cond_to_avoid_flag=False
            else:
                cond_to_avoid=cond_to_avoid+" "+" ".join(cline)

        if "10.5." in cline:
            mats_to_avoid_flag=True

        if mats_to_avoid_flag==True:
            if "10.6." in cline:
                mats_to_avoid_flag=False
            else:
                mats_to_avoid=mats_to_avoid+" "+" ".join(cline)

        if "10.6." in cline:
            haz_decomp_flag=True

        if haz_decomp_flag==True:
            if "11:" in cline:
                haz_decomp_flag=False
            else:
                haz_decomp_prods=haz_decomp_prods+" "+" ".join(cline)



    reactivity=reactivity.split()
    reactivity=" ".join(reactivity[2:])
    chem_stability=chem_stability.split()
    chem_stability=" ".join(chem_stability[3:])
    haz_reactions=haz_reactions.split()
    haz_reactions=" ".join(haz_reactions[5:])
    cond_to_avoid=cond_to_avoid.split()
    cond_to_avoid=" ".join(cond_to_avoid[4:])
    mats_to_avoid=mats_to_avoid.split()
    mats_to_avoid=" ".join(mats_to_avoid[3:])
    haz_decomp_prods=haz_decomp_prods.split()
    haz_decomp_prods=" ".join(haz_decomp_prods[4:])


    file=file.replace(".txt",".pdf")
    filenames.append(file)
    date_list.append(date)
    version_list.append(version)
    prod_form_list.append(prod_form)
    prod_name_list.append(prod_name)
    cas_list.append(cas)
    prod_code_list.append(prod_code)
    formula_list.append(formula)
    synonyms_list.append(synonyms)
    other_id_list.append(other_id)
    handling_list.append(handling)
    hygiene_list.append(hygiene)
    storage_cond_list.append(storage_cond)
    technical_list.append(technical)
    storage_area_list.append(storage_area)
    state_list.append(state)
    color_list.append(color)
    odor_list.append(odor)
    odor_threshold_list.append(odor_threshold)
    ph_list.append(ph)
    melt_pt_list.append(melt_pt)
    freeze_pt_list.append(freeze_pt)
    boil_pt_list.append(boil_pt)
    flash_pt_list.append(flash_pt)
    evaporation_rate_list.append(evaporation_rate)
    flammability_list.append(flammability)
    explosion_limits_list.append(explosion_limits)
    explosive_props_list.append(explosive_props)
    oxidising_list.append(oxidising)
    vapor_pressure_list.append(vapor_pressure)
    rel_density_list.append(rel_density)
    rel_vapor_density_list.append(rel_vapor_density)
    specific_gravity_list.append(specific_gravity)
    molec_mass_list.append(molec_mass)
    solubility_list.append(solubility)
    log_pow_list.append(log_pow)
    autoignition_temp_list.append(autoignition_temp)
    decomp_temp_list.append(decomp_temp)
    viscosity_list.append(viscosity)
    viscosity_k_list.append(viscosity_k)
    viscosity_d_list.append(viscosity_d)
    refractive_index_list.append(refractive_index)
    reactivity_list.append(reactivity)
    chem_stability_list.append(chem_stability)
    haz_reactions_list.append(haz_reactions)
    cond_to_avoid_list.append(cond_to_avoid)
    mats_to_avoid_list.append(mats_to_avoid)
    haz_decomp_prods_list.append(haz_decomp_prods)

df=pd.DataFrame()
df=df.assign(filename=filenames, date=date_list, version=version_list, product_form=prod_form_list, product_name=prod_name_list, cas=cas_list, product_code=prod_code_list, formula=formula_list, synonyms=synonyms_list, other_identification=other_id_list, handling_requirements=handling_list, hygiene_measures=hygiene_list, technical_measures=technical_list, storage_conditions=storage_cond_list, storage_area=storage_area, physical_state=state_list, color=color_list, odor=odor_list, odor_threshold=odor_threshold_list, ph=ph_list, melting_point=melt_pt_list, freezing_point=freeze_pt_list, boiling_point=boil_pt_list, flash_point=flash_pt_list, evaporation_rate=evaporation_rate_list, flammability=flammability_list, explosion_limits=explosion_limits_list, explosive_properties=explosive_props_list, oxidising=oxidising_list, vapor_pressure=vapor_pressure_list, relative_denisty=rel_density_list, relative_vapor_density=rel_vapor_density_list, specific_gravity_density=specific_gravity_list, molecular_mass=molec_mass_list, solubility=solubility_list, log_pow=log_pow_list, autoignition_temp=autoignition_temp_list, decomposition_temp=decomp_temp_list, viscosity=viscosity_list, viscosity_kinematic=viscosity_k_list, viscosity_dynamic=viscosity_d_list, refractive_index=refractive_index_list, reactivity=reactivity_list, chemical_stability=chem_stability_list, hazardous_reactions=haz_reactions_list, conditions_to_avoid=cond_to_avoid_list, incompatible_materials=mats_to_avoid_list, hazardous_decomoposition_products=haz_decomp_prods_list)

df.to_excel("C://Users//lkoval//Documents//wetmore extractions//synquest.xlsx", index=False)
