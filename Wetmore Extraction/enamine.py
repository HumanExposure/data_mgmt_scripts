#lkoval
#4/23/19

import os, string, csv
import glob
import pandas as pd

#change directory to file location
os.chdir("L://Lab//HEM//Wetmore-PFAS-PDFs//Enamine")

#get list of files
filelist=glob.glob("*.txt")

filenames=[]
issue_date_list=[]
rev_date_list=[]
version_list=[]
prod_name_list=[]
prod_cat_num_list=[]
ec_list=[]
cas_list=[]
rec_use_list=[]
company_list=[]
handling_reqs_list=[]
storage_reqs_list=[]
end_use_list=[]
state_list=[]
odor_list=[]
color_list=[]
ph_list=[]
melt_freeze_list=[]
boil_list=[]
flash_pt_list=[]
vapor_pressure_list=[]
vapor_density_list=[]
rel_density_list=[]
part_coeff_list=[]
autoignition_temp_list=[]
viscosity_list=[]
flammability_list=[]
explosive_props_list=[]
oxidising_list=[]
water_sol_list=[]
evaporation_rate_list=[]
refractive_index_list=[]
chem_stability_list=[]
haz_reactions_list=[]
cond_to_avoid_list=[]
mats_to_avoid_list=[]
haz_decomp_prods_list=[]

for file in filelist:
    issue_date=""
    rev_date=""
    version=""
    prod_name=""
    prod_cat_num=""
    ec=""
    cas=""
    rec_use=""
    company=""
    handling_reqs=""
    storage_reqs=""
    end_use=""
    state=""
    odor=""
    color=""
    ph=""
    melt_freeze=""
    boil=""
    flash_pt=""
    vapor_pressure=""
    vapor_density=""
    rel_density=""
    part_coeff=""
    autoignition_temp=""
    viscosity=""
    flammability=""
    explosive_props=""
    oxidising=""
    water_sol=""
    evaporation_rate=""
    refractive_index=""
    chem_stability=""
    haz_reactions=""
    cond_to_avoid=""
    mats_to_avoid=""
    haz_decomp_prods=""

    cas_flag=False
    hand_flag=False
    storage_flag=False
    end_use_flag=False
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

        if "issued" in cline and "on" in cline:
            issue_date=cline[2]

        if "version" in cline:
            version=cline[1]
            rev_date=cline[4]

        if "product" in cline and "name:" in cline:
            prod_name=" ".join(cline[2:])

        if "product" in cline and "catalogue" in cline:
            prod_cat_num=cline[2]

        if "ec" in cline and "number:" in cline:
            ec=cline[2]

        if cas_flag==False:
            if "cas-no.:" in cline:
                cas=cline[1]
                cas_flag=True

        if "recommended" in cline and "use:" in cline:
            rec_use=" ".join(cline[2:])

        if "company:" in cline:
            company=" ".join(cline[1:])

        if "7.1" in cline:
            hand_flag=True

        if hand_flag==True:
            if "7.2" in cline:
                hand_flag=False
            else:
                handling_reqs=handling_reqs+" "+" ".join(cline)

        if "7.2" in cline:
            storage_flag=True

        if storage_flag==True:
            if "7.3" in cline:
                storage_flag=False
            else:
                storage_reqs=storage_reqs+" "+" ".join(cline)

        if "7.3" in cline:
            end_use_flag=True

        if end_use_flag==True:
            if "8." in cline:
                end_use_flag=False
            else:
                end_use=end_use+" "+" ".join(cline)

        if "physical" in cline and "state:" in cline:
            state=" ".join(cline[2:])

        if "odour:" in cline:
            odor=" ".join(cline[1:])

        if "colour:" in cline:
             color=" ".join(cline[1:])

        if "ph:" in cline:
            ph=" ".join(cline[1:])

        if "melting" in cline:
            melt_freeze=" ".join(cline[2:])

        if "initial" in cline and "boiling" in cline:
            boil=" ".join(cline[4:])

        if "flash" in cline:
            flash_pt=" ".join(cline[3:])

        if "vapour" in cline and "pressure:" in cline:
            vapor_pressure=" ".join(cline[2:])

        if "vapour" in cline and "density:" in cline:
            vapor_density=" ".join(cline[2:])

        if "relative" in cline and "density" in cline:
            rel_density=" ".join(cline[3:])

        if "partition" in cline and "coefficient:" in cline:
            part_coeff=" ".join(cline[3:])

        if "auto-ignition" in cline:
            autoignition_temp=" ".join(cline[1:])

        if "viscosity:" in cline:
            viscosity=" ".join(cline[1:])

        if "flammability:" in cline:
            flammability=" ".join(cline[1:])

        if "explosive" in cline and "properties:" in cline:
            explosive_props=" ".join(cline[2:])

        if "oxidizing" in cline and "properties:" in cline:
            oxidising=" ".join(cline[2:])

        if "water" in cline and "solubility:" in cline:
            water_sol=" ".join(cline[2:])

        if "evaporation" in cline and "rate:" in cline:
            evaporation_rate=" ".join(cline[2:])

        if "refractive" in cline and "index:" in cline:
            refractive_index=" ".join(cline[2:])

        if "10.1" in cline:
            chem_stab_flag=True

        if chem_stab_flag==True:
            if "10.2" in cline:
                chem_stab_flag=False
            else:
                chem_stability=chem_stability+" "+" ".join(cline)

        if "10.2" in cline:
            haz_rx_flag=True

        if haz_rx_flag==True:
            if "10.3" in cline:
                haz_rx_flag=False
            else:
                haz_reactions=haz_reactions+" "+" ".join(cline)

        if "10.3" in cline:
            cond_to_avoid_flag=True

        if cond_to_avoid_flag==True:
            if "10.4" in cline:
                cond_to_avoid_flag=False
            else:
                cond_to_avoid=cond_to_avoid+" "+" ".join(cline)

        if "10.4" in cline:
            mats_to_avoid_flag=True

        if mats_to_avoid_flag==True:
            if "10.5" in cline:
                mats_to_avoid_flag=False
            else:
                mats_to_avoid=mats_to_avoid+" "+" ".join(cline)

        if "10.5" in cline:
            haz_decomp_flag=True

        if haz_decomp_flag==True:
            if "11." in cline:
                haz_decomp_flag=False
            else:
                haz_decomp_prods=haz_decomp_prods+" "+" ".join(cline)


    handling_reqs=handling_reqs.split()
    handling_reqs=" ".join(handling_reqs[5:])
    storage_reqs=storage_reqs.split()
    storage_reqs=" ".join(storage_reqs[8:])
    end_use=end_use.split()
    end_use=" ".join(end_use[4:])
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
    issue_date_list.append(issue_date)
    rev_date_list.append(rev_date)
    version_list.append(version)
    prod_name_list.append(prod_name)
    prod_cat_num_list.append(prod_cat_num)
    ec_list.append(ec)
    cas_list.append(cas)
    rec_use_list.append(rec_use)
    company_list.append(company)
    handling_reqs_list.append(handling_reqs)
    storage_reqs_list.append(storage_reqs)
    end_use_list.append(end_use)
    state_list.append(state)
    odor_list.append(odor)
    color_list.append(color)
    ph_list.append(ph)
    melt_freeze_list.append(melt_freeze)
    boil_list.append(boil)
    flash_pt_list.append(flash_pt)
    vapor_pressure_list.append(vapor_pressure)
    vapor_density_list.append(vapor_density)
    rel_density_list.append(rel_density)
    part_coeff_list.append(part_coeff)
    autoignition_temp_list.append(autoignition_temp)
    viscosity_list.append(viscosity)
    flammability_list.append(flammability)
    explosive_props_list.append(explosive_props)
    oxidising_list.append(oxidising)
    water_sol_list.append(water_sol)
    evaporation_rate_list.append(evaporation_rate)
    refractive_index_list.append(refractive_index)
    chem_stability_list.append(chem_stability)
    haz_reactions_list.append(haz_reactions)
    cond_to_avoid_list.append(cond_to_avoid)
    mats_to_avoid_list.append(mats_to_avoid)
    haz_decomp_prods_list.append(haz_decomp_prods)


df=pd.DataFrame()
df=df.assign(filename=filenames, issue_date=issue_date_list, revision_date=rev_date_list, version=version_list, product_name=prod_name_list, product_catalogue_number=prod_cat_num_list, ec_number=ec_list, cas=cas_list, recommended_use=rec_use_list, company=company_list, handling_requirements=handling_reqs_list, storage_requirements=storage_reqs_list, end_use=end_use_list, physical_state=state_list, odor=odor_list, color=color_list, ph=ph_list, melting_freezing_point=melt_freeze_list, boiling_point=boil_list, flash_point=flash_pt_list, vapor_pressure= vapor_pressure_list, vapor_density=vapor_density_list, relative_denisty_gpml=rel_density_list, partition_coefficient=part_coeff_list, autoignition_temp=autoignition_temp_list, viscosity=viscosity_list, flammability=flammability_list, explosive_properties=explosive_props_list, oxidising=oxidising_list, water_solubility=water_sol_list, evaporation_rate=evaporation_rate_list, refractive_index=refractive_index_list, chemical_stability=chem_stability_list, hazardous_reactions=haz_reactions_list, conditions_to_avoid=cond_to_avoid_list, incompatible_materials=mats_to_avoid_list, hazardous_decomoposition_products=haz_decomp_prods)

df.to_excel("C://Users//lkoval//Documents//wetmore extractions//enamine.xlsx", index=False)
