#lkoval
#4/23/19

import os, string, csv
import glob
import pandas as pd

#change directory to folder with files
os.chdir("L://Lab//HEM//Wetmore-PFAS-PDFs//INDOFINE Chemical Company, Inc")

#make list of files
filelist=glob.glob("*.txt")

filenames=[]
rev_date_list=[]
prod_name_list=[]
synonyms_list=[]
prod_code_list=[]
cas_list=[]
supp_list=[]
handling_requirements_list=[]
appearance_list=[]
molec_form_list=[]
molec_weight_list=[]
melt_boil_list=[]
ph_list=[]
flash_pt_list=[]
ignition_temp_list=[]
autoignition_temp_list=[]
decomp_list=[]
temperature_list=[]
lwr_explosion_list=[]
upr_explosion_list=[]
vapor_pressure_list=[]
density_list=[]
viscosity_list=[]
water_sol_list=[]
part_coeff_list=[]
rel_vap_density_list=[]
odor_list=[]
odor_threshold_list=[]
evaporation_rate_list=[]
reactivity_list=[]
chem_stability_list=[]
haz_reactions_list=[]
cond_to_avoid_list=[]
mats_to_avoid_list=[]
haz_decomp_prods_list=[]

for file in filelist:
    rev_date=""
    prod_name=""
    synonyms=""
    prod_code=""
    cas=""
    supp=""
    handling_requirements=""
    appearance=""
    molec_form=""
    molec_weight=""
    melt_boil=""
    ph=""
    flash_pt=""
    ignition_temp=""
    autoignition_temp=""
    decomp=""
    temperature=""
    lwr_explosion=""
    upr_explosion=""
    vapor_pressure=""
    density=""
    viscosity=""
    water_sol=""
    part_coeff=""
    rel_vap_density=""
    odor=""
    odor_threshold=""
    evaporation_rate=""
    reactivity=""
    chem_stability=""
    haz_reactions=""
    cond_to_avoid=""
    mats_to_avoid=""
    haz_decomp_prods=""

    rev_date_flag=False
    cas_flag=False
    syn_flag=False
    reqs_flag=False
    decomp_flag=False
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

        if rev_date_flag==False:
            if cline[0]=="revision" and cline[1]=="date:":
                rev_date=cline[2]
                rev_date_flag=True

        if cline[0]=="product" and cline[1]=="name:":
            prod_name=" ".join(cline[2:])

        if syn_flag==False:
            if cline[0]=="synonyms:":
                synonyms=synonyms+"; "+" ".join(cline)
                if cline[0]=="cas#:":
                    syn_flag=True

        if cas_flag==False:
            if cline[0]=="cas#:":
                cas=cline[1]
                cas_flag=True

        if cline[0]=="product" and cline[1]=="number":
            prod_code=cline[2]

        if cline[0]=="supplier:":
            supp=" ".join(cline[1:])

        if "section" in cline and "7:" in cline:
            reqs_flag=True

        if reqs_flag==True:
            if "section" in cline and "8:" in cline:
                reqs_flag=False
            else:
                handling_requirements=handling_requirements+" "+" ".join(cline)


        if cline[0]=="appearance:":
            try:
                appearance=cline[1]
            except:
                appearance=""

        if "molecular" in cline and "formula:" in cline:
            molec_form=" ".join(cline[2:])

        if "molecular" in cline and "weight:" in cline:
            molec_weight=" ".join(cline[2:])

        if "melting" in cline:
            melt_boil=" ".join(cline[2:])

        if "ph:" in cline:
            ph=" ".join(cline[1:])

        if "flash" in cline:
            flash_pt=" ".join(cline[2:])

        if "ignition" in cline and "temperature:" in cline:
            ignition_temp=" ".join(cline[2:])

        if "autoignition:" in cline:
            autoignition=" ".join(cline[2:])

        if cline[0]=="decomposition" and len(cline)==1:
            decomp=" ".join(cline[1:])

        if cline[0]=="temperature:":
            temperature=" ".join(cline[1:])

        if "lower" in cline and "explosion" in cline:
            lwr_explosion=" ".join(cline[3:])

        if "upper" in cline and "explosion" in cline:
            upr_explosion=" ".join(cline[3:])

        if "vapor" in cline and "pressure:" in cline:
            vapor_pressure=" ".join(cline[2:])

        if cline[0]=="density:":
            density=" ".join(cline[1:])

        if cline[0]=="viscosity:":
            viscosity=" ".join(cline[1:])

        if "water" in cline and "solubility:" in cline:
            water_sol=" ".join(cline[2:])

        if "partition" in cline and "coefficient:" in cline:
            part_coeff=" ".join(cline[2:])

        if "vapor" in cline and "density:" in cline:
            rel_vap_density=" ".join(cline[3:])

        if cline[0]=="odor:":
            odor=" ".join(cline[1:])

        if cline[0]=="odor" and cline[1]=="threshold:":
            odor_threshold=" ".join(cline[2:])

        if "evaporation" in cline and "rate:" in cline:
            evaporation_rate=" ".join(cline[2:])

        if cline[0]=="reactivity":
            reactivity_flag=True

        if reactivity_flag==True:
            if cline[0]=="chemical" and cline[1]=="stability":
                reactivity_flag=False
            else:
                reactivity=reactivity+" "+" ".join(cline)

        if cline[0]=="chemical" and cline[1]=="stability":
            chem_stab_flag=True

        if chem_stab_flag==True:
            if "possibility" in cline and "hazardous" in cline:
                chem_stab_flag=False
            else:
                chem_stability=chem_stability+" "+" ".join(cline)

        if "possibility" in cline and "hazardous" in cline:
            haz_rx_flag=True

        if haz_rx_flag==True:
            if "conditions" in cline and "avoid" in cline:
                haz_rx_flag=False
            else:
                haz_reactions=haz_reactions+" "+" ".join(cline)

        if "conditions" in cline and "avoid" in cline:
            cond_to_avoid_flag=True

        if cond_to_avoid_flag==True:
            if "incompatible" in cline and "materials" in cline:
                cond_to_avoid_flag=False
            else:
                cond_to_avoid=cond_to_avoid+" "+" ".join(cline)

        if "incompatible" in cline and "materials" in cline:
            mats_to_avoid_flag=True

        if mats_to_avoid_flag==True:
            if "hazardous" in cline and "decomposition" in cline:
                mats_to_avoid_flag=False
            else:
                mats_to_avoid=mats_to_avoid+" "+" ".join(cline)

        if "hazardous" in cline and "decomposition" in cline:
            haz_decomp_flag=True

        if haz_decomp_flag==True:
            if "toxicological" in cline:
                haz_decomp_flag=False
            else:
                haz_decomp_prods=haz_decomp_prods+" "+" ".join(cline)

    synonyms=synonyms.split()
    synonyms=" ".join(synonyms[2:])
    handling_requirements=handling_requirements.split()
    handling_requirements=" ".join(handling_requirements[5:])
    reactivity=reactivity.strip(" reactivity ")
    chem_stability=chem_stability.split()
    chem_stability=" ".join(chem_stability[2:])
    haz_reactions=haz_reactions.split()
    haz_reactions=" ".join(haz_reactions[4:])
    cond_to_avoid=cond_to_avoid.split()
    cond_to_avoid=" ".join(cond_to_avoid[3:])
    mats_to_avoid=mats_to_avoid.split()
    mats_to_avoid=" ".join(mats_to_avoid[2:])
    haz_decomp_prods=haz_decomp_prods.split()
    haz_decomp_prods=" ".join(haz_decomp_prods[3:])

    file=file.replace(".txt",".pdf")
    filenames.append(file)
    rev_date_list.append(rev_date)
    prod_name_list.append(prod_name)
    cas_list.append(cas)
    prod_code_list.append(prod_code)
    synonyms_list.append(synonyms)
    supp_list.append(supp)
    handling_requirements_list.append(handling_requirements)
    appearance_list.append(appearance)
    molec_form_list.append(molec_form)
    molec_weight_list.append(molec_weight)
    melt_boil_list.append(melt_boil)
    ph_list.append(ph)
    flash_pt_list.append(flash_pt)
    ignition_temp_list.append(ignition_temp)
    autoignition_temp_list.append(autoignition_temp)
    decomp_list.append(decomp)
    temperature_list.append(temperature)
    lwr_explosion_list.append(lwr_explosion)
    upr_explosion_list.append(upr_explosion)
    vapor_pressure_list.append(vapor_pressure)
    density_list.append(density)
    viscosity_list.append(viscosity)
    water_sol_list.append(water_sol)
    part_coeff_list.append(part_coeff)
    rel_vap_density_list.append(rel_vap_density)
    odor_list.append(odor)
    odor_threshold_list.append(odor_threshold)
    evaporation_rate_list.append(evaporation_rate)
    reactivity_list.append(reactivity)
    chem_stability_list.append(chem_stability)
    haz_reactions_list.append(haz_reactions)
    cond_to_avoid_list.append(cond_to_avoid)
    mats_to_avoid_list.append(mats_to_avoid)
    haz_decomp_prods_list.append(haz_decomp_prods)

df=pd.DataFrame()
df=df.assign(filename=filenames, rev_date=rev_date_list, product_name=prod_name_list, cas=cas_list, products_code=prod_code_list, synonyms=synonyms_list, supplier=supp_list, handling_requirements=handling_requirements_list, appearance=appearance_list, molecular_formula=molec_form_list, molecular_weight=molec_weight_list, melting_boiling_pt=melt_boil_list, ph=ph_list, flash_point=flash_pt_list, ignition_temperature=ignition_temp_list, autoignition_temperature=autoignition_temp_list, decomposition=decomp_list, temperature=temperature_list, lower_expolosion_limit=lwr_explosion_list, upper_explosion_limit=upr_explosion_list, vapor_pressure=vapor_pressure_list, density=density_list, viscosity=viscosity_list, water_solubility=water_sol_list, partition_coefficient=part_coeff_list, relative_vapor_density=rel_vap_density_list, odor=odor_list, odor_threshold=odor_threshold_list, evaporation_rate=evaporation_rate_list, reactivity=reactivity_list, chemical_stability=chem_stability_list, possible_hazardous_reactions=haz_reactions_list, conditions_to_avoid=cond_to_avoid_list, incompatible_materials=mats_to_avoid_list, hazardous_decomoposition_products=haz_decomp_prods_list)

df.to_excel("C://Users//lkoval//Documents//wetmore extractions//indofine.xlsx", index=False)
