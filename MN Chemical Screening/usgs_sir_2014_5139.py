#lkoval
#2-27-2020

import pandas as pd
import os
from tabula import read_pdf
import string

os.chdir("//home//lkoval//MN")

##############################   Appendix 2   ###################################################################################################

#appendix 2 spans pages 94-105 but tabula reads in a couple different formats due to spacing, so read in each page as its own table
a2_tabs=read_pdf("Organics in Source Water USA 2002-2010.pdf", pages="94-105", multiple_tables=True )

#create master df for all data starting with first page
a2=a2_tabs[0].iloc[:,:3].rename(columns={0:"raw_chem_name",1:"raw_cas",2:"detects"})

#list of raw categories
cats=["disinfection by-products",
"fumigant-related compounds",
"fungicides and fungicide degradates",
"gasoline hydrocarbons, oxygenates, and oxygenate degradates",
"herbicide and herbicide degradates",
"insecticide and insecticde degradates",
"manufacturing additives",
"organic synthesis compounds",
"pavement and combustion derived compounds",
"personal care and domestic use products",
"plant or animal derived biochemicals",
"solvents",
"herbicide and herbicide degradates"]

#cas numbers where raw category switches
cat_switch=["75-25-2","10061-02-6","107534-96-3","98-06-6","6967-29-9","56070-15-6","115-86-6","75-01-4","85-01-8","119-65-3","75-69-4","156-60-5"]

#clean function to remove non-printable characters
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

#look at the rest of the tables and determine if column 3 or 4 contains the number of detects then add it to the master df
for i in range(1,len(a2_tabs)):
    a2_tabs[i]=a2_tabs[i].iloc[:,:5]
    temp=a2_tabs[i].applymap(str)
    detects_count=temp.iloc[:,4].str.isdigit().value_counts().to_dict()
    if len(detects_count)>1:
        a2_tabs[i]=a2_tabs[i].iloc[:,[0,1,4]]
        a2_tabs[i]=a2_tabs[i].rename(columns={0:"raw_chem_name",1:"raw_cas",4:"detects"})
    else:
        a2_tabs[i]=a2_tabs[i].iloc[:,[0,1,3]]
        a2_tabs[i]=a2_tabs[i].rename(columns={0:"raw_chem_name",1:"raw_cas",3:"detects"})
    a2=pd.concat([a2, a2_tabs[i]], ignore_index=True)

#address issue where on some pages tabula joined cas number with other data. Replace hyphen with a dash becasue hyphen isn't printable
a2.loc[(pd.isnull(a2.raw_cas)==False) & (a2.raw_cas.str.contains("^\d+–\d{2}–\d|^[tc]")), ["raw_cas"]]=a2.raw_cas.str.split(" ", expand=True)[0]
a2=a2.loc[(pd.isnull(a2.raw_chem_name)==False) | ((pd.isnull(a2.raw_chem_name)==True) & (a2.raw_cas.str.contains("\d+–\d{2}–\d")))]
a2["raw_cas"]=a2.raw_cas.str.replace("–", "-")
a2=a2.reset_index()
a2=a2[["raw_chem_name","raw_cas","detects"]]

#find indices where cas number and chemical names are split onto multiple lines
fix_cas_i=a2.loc[pd.isnull(a2.raw_chem_name)].index[0]
fix_names_i=a2.loc[pd.isnull(a2.raw_cas)].index

#correct data on multiple lines
for j in range(len(a2)):
    if j==fix_cas_i:
        a2.raw_cas.iloc[j-1]=a2.raw_cas.iloc[j-1]+" "+a2.raw_cas.iloc[j]

    if j in fix_names_i:
        a2.raw_chem_name.iloc[j-1]=a2.raw_chem_name.iloc[j-1]+" "+a2.raw_chem_name.iloc[j]

a2=a2.dropna(subset=["detects"])

#create raw_category column
a2["raw_category"]=""

#clean chemical names and assign raw category to chemicals
c=0
for k in range(len(a2)):
    rc=cats[c]
    a2.raw_chem_name.iloc[k]=clean(a2.raw_chem_name.iloc[k])
    a2.raw_category.iloc[k]=rc
    if a2.raw_cas.iloc[k] in cat_switch:
        c+=1


#remove all non detected chemicals
a2=a2.loc[a2.detects!="0"]
a2=a2[["raw_category","raw_cas","raw_chem_name"]]

#finish template
a2["data_document_id"]="1511924"
a2["data_document_filename"]="Organics in Source Water USA 2002-2010_a.pdf"
a2["doc_date"]="2014"
a2["cat_code"]=""
a2["description_cpcat"]=""
a2["cpcat_sourcetype"]=""
a2["report_funcuse"]=""
a2["component"]=""

a2=a2[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]


a2.to_csv("usgs_sir_2014_5139_appendix_2.csv", index=False)



#########################################    Appendix 3   ###################################################################################################################################

#appendix 3 spans pages 107-118 but tabula reads in a couple different formats due to spacing, so read in each page as its own table
a3_tabs=read_pdf("Organics in Source Water USA 2002-2010.pdf", pages="107-118", multiple_tables=True )

#create master df for all data starting with first page
a3=a3_tabs[0].iloc[:,:3].rename(columns={0:"raw_chem_name",1:"raw_cas",2:"detects"})
a3["detects"]=a3.detects.str.split(expand=True)[2]

#list of raw categories
cats=["disinfection by-products",
"fumigant-related compounds",
"fungicides and fungicide degradates",
"gasoline hydrocarbons, oxygenates, and oxygenate degradates",
"herbicide and herbicide degradates",
"insecticide and insecticde degradates",
"manufacturing additives",
"organic synthesis compounds",
"pavement and combustion derived compounds",
"personal care and domestic use products",
"plant or animal derived biochemicals",
"refrigerants and propellants",
"solvents",
"herbicide and herbicide degradates"]

#cas numbers where raw category switches
cat_switch=["124-48-1","10061-02-6","36734-19-7","108-88-3","1582-09-8","56070-15-6","78-51-3","593-60-2","50-32-8","26027-38-2","83-34-1","76-13-1","67-72-1"]

#clean function to remove non-printable characters
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

#look at the rest of the tables and determine if column 3 or 4 contains the number of detects then add it to the master df
for i in range(1,len(a3_tabs)):
    a3_tabs[i]=a3_tabs[i].iloc[:,:5]
    temp=a3_tabs[i].applymap(str)
    detects_count=temp.iloc[:,4].str.isdigit().value_counts().to_dict()
    if list(detects_count.keys())[0]==True:
            a3_tabs[i]=a3_tabs[i].iloc[:,[0,1,4]]
            a3_tabs[i]=a3_tabs[i].rename(columns={0:"raw_chem_name",1:"raw_cas",4:"detects"})

    else:
        a3_tabs[i]=a3_tabs[i].iloc[:,[0,1,3]]
        a3_tabs[i]=a3_tabs[i].rename(columns={0:"raw_chem_name",1:"raw_cas",3:"detects"})
    a3=pd.concat([a3, a3_tabs[i]], ignore_index=True)

#address issue where on some pages tabula groups detects with other info
a3.loc[a3.detects.str.split().str.len()>1, ["detects"]]=a3.detects.str.split(expand=True)[1]

#replace hyphens with dash becasue hyphens are not printable
a3["raw_cas"]=a3.raw_cas.str.replace("–", "-")
a3=a3.dropna(how="all")
a3=a3.reset_index()
a3=a3[["raw_chem_name","raw_cas","detects"]]

#find indices where cas number and chemical names are split onto multiple lines
fix_cas_i=a3.loc[(pd.isnull(a3.raw_chem_name)) & (pd.isnull(a3.raw_cas)==False)].index[0]
fix_names_i=a3.loc[(pd.isnull(a3.raw_cas)) & (pd.isnull(a3.raw_chem_name)==False)].index

#correct data on multiple lines
for j in range(len(a3)):
    if j==fix_cas_i:
        a3.raw_cas.iloc[j-1]=a3.raw_cas.iloc[j-1]+" "+a3.raw_cas.iloc[j]

    if j in fix_names_i:
        a3.raw_chem_name.iloc[j-1]=a3.raw_chem_name.iloc[j-1]+" "+a3.raw_chem_name.iloc[j]

a3=a3.dropna()

#create raw_category column
a3["raw_category"]=""

#clean chemical names and assign raw category to chemicals
c=0
for k in range(len(a3)):
    rc=cats[c]
    a3.raw_chem_name.iloc[k]=clean(a3.raw_chem_name.iloc[k])
    a3.raw_category.iloc[k]=rc
    if a3.raw_cas.iloc[k] in cat_switch:
        c+=1

#remove all non detected chemicals
a3=a3.loc[a3.detects!="0"]
a3=a3.reset_index()
a3=a3[["raw_category","raw_cas","raw_chem_name"]]

#correct chemical name where tabula missed a piece
a3.raw_chem_name.iloc[151]=a3.raw_chem_name.iloc[151]+" (4-methyl-2-pentanone)"

#finish rest of template
a3["data_document_id"]="1511925"
a3["data_document_filename"]="Organics in Source Water USA 2002-2010_b.pdf"
a3["doc_date"]="2014"
a3["cat_code"]=""
a3["description_cpcat"]=""
a3["cpcat_sourcetype"]=""
a3["report_funcuse"]=""
a3["component"]=""

a3=a3[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]


a3.to_csv("usgs_sir_2014_5139_appendix_3.csv", index=False)
