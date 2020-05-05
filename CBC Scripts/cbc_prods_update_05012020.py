import os
import string
import pandas as pd
import re

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//covid_19")

#########################################################################################################################################################################################################
#########################################################################################################################################################################################################
#                                               Extracts Product Name and EPA Reg No. from CBC List
#########################################################################################################################################################################################################
#########################################################################################################################################################################################################


text_file="CBC-COVID19-Product-List-05012020.txt"#downloaded pdf from https://www.americanchemistry.com/Novel-Coronavirus-Fighting-Products-List.pdf?mod=article_inline and converted it to a text file for parsing with XpdfReader application

prods=[]
epa_num=[]

ifile=open(text_file, encoding='utf-8')
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #clean function to remove non-printable characters

epa_reg_pattern=re.compile('^\d+-{1}\d+-*\d*') #used to identify epa registration numbers in the cleaned lines. Note this pattern was written from observation and seems to work but I do not have confirmation that this is 100% correct
bad_pattern=re.compile('^-{1}\d+-')

temp_name=""#place holder for when a product name is split onto multiple lines but the second line contains the registration number
start=False
for line in ifile:#loop through each line in file
    if line=='\n': continue
    cline=clean(line)
    cline=cline.lower()
    cline=cline.replace(';',',')
    cline=cline.strip()
    cline=cline.strip("")
    cline=cline.split(" ")
    if "commercially" in cline:#start looking at the beginning of each table
        start=True
        epa_num.append("")
    elif ("tier" in cline) or ("ebola." in cline):#stop looking at the end of each table
        start=False

    if start==True:
        if cline[0][0]=="#" and len(cline[0])>3 and cline[1]=="":#removes empty string from product names that had non printable characters which were replaced with empty string. Specifically targets a certain brand where this happened and all product names started with "#"
            del(cline[1])

        if "" in cline:#most lines have the product name, company, EPA Reg No, and some have a formulation type. Usually these pieces of information are split on empty strings
            prod_end=cline.index("")
            if cline[prod_end+1]!="":#prod name is the first piece of information so find where that ends and add the product name to the list
                prods.append(temp_name+" ".join(cline[:prod_end]))
            else:#in rare instances a product name has a empty string in between words usually where a non printable character was removed. This cuts off the product name. Remove the empty string and at the product name to the list.
                del(cline[prod_end])
                prod_end=cline.index("")
                prods.append(temp_name+" ".join(cline[:prod_end]))
            cline=cline[prod_end+1:]#remove the product name from the line
            cline = [x.strip() for x in cline if x != ""]#remove all empty strings from the line
            epa_ind=""
            temp_name=""
            for word in cline:#loop through the rest of the line and check to see if there is an EPA Reg No. If there is, add to the list, if not, add an empty string to the list
                if bool(epa_reg_pattern.match(word)):
                    epa_ind=cline.index(word)
                    break

            if epa_ind!="":
                epa_num.append(cline[epa_ind])
            elif epa_ind=="" and "reg" not in cline:
                epa_num.append("")
        else:#if there are no empty strings in the line, it means a single product entry was broken into multiple lines. Specific corrections, often by brand, are made here.
            if len(cline)>1:
                if "lysol" in cline:
                    prods.append(" ".join(cline))
                    epa_num.append("")
                elif ("lysol" not in cline) and ("construction" not in cline) and ("ncl" not in cline):
                    prods[-1]=prods[-1]+" "+" ".join(cline)
                elif "ncl" in cline:#this is the brand where the first only contains part of the product name and the second row contains the rest of the product name as well as the other information. Store the first part of the prod name as a temp variable that can be accessed in the next iteration of the loop
                    temp_name=" ".join(cline)
            elif (len(cline)==1) and (cline[0].isdigit()==False):
                if ("clinics" in cline) or ("bleach" in cline) or ("bleach1" in cline) or ("disinfectant" in cline):
                    prods[-1]=prods[-1]+" "+cline[0]



#make df of product names and EPA registration numbers.
cbc_prods=pd.DataFrame()
cbc_prods["prod_name"]=prods
cbc_prods["EPA_Reg_No"]=epa_num
cbc_prods=cbc_prods.loc[cbc_prods.prod_name.str.contains("commercially", regex=False)==False]

#corrected some observed incosistencies
cbc_prods.loc[cbc_prods.prod_name=="boost 3200 cip", ["EPA_Reg_No"]]="63761-8-1677"
cbc_prods.loc[cbc_prods.prod_name=="neutra-clean rx", ["EPA_Reg_No"]]="1839-168-38398"
cbc_prods.loc[cbc_prods.prod_name=="sono disinfecting wipes", ["EPA_Reg_No"]]="6836-340-89018"
cbc_prods.loc[cbc_prods.prod_name=="sono ultrasound wipes", ["EPA_Reg_No"]]="6836-340-89018"

#make abbreviated EPA Reg Nos to match back to Factotum Docs.
cbc_prods["sets"]=""
for i in range(len(cbc_prods)):
    split_num=cbc_prods.EPA_Reg_No.iloc[i].split("-")
    short_num="-".join(split_num[:2])
    cbc_prods.sets.iloc[i]=short_num

#write d to csv
cbc_prods.to_csv("cbc_covid19_products_list_updated_05012020.csv", index=False)

#read in last df of products and registration numbers
cbc_prods_old=pd.read_csv("cbc_covid19_products_list_updated_4272020.csv", dtype=str)

#looks at new product names
cur=set(cbc_prods.prod_name)
old=set(cbc_prods_old.prod_name)
new=list(cur-old)

#make df of new products with full and partial registration numbers
new_prods=cbc_prods.loc[cbc_prods.prod_name.isin(new)]
new_prods.drop_duplicates(inplace=True)
new_prods.reset_index(inplace=True, drop=True)



#########################################################################################################################################################################################################
#########################################################################################################################################################################################################
#                                               Matches products to docs
#########################################################################################################################################################################################################
#########################################################################################################################################################################################################



#Function to get the abbreviated EPA registration number from the data_document_filename. Reads in a dataframe (targeting the downloaded product template for each group) and returns the data frame with a new column of abbreviated EPA Reg Nos.
def EPA_Reg_No_from_filename(df):
    df["sets"]=df.data_document_filename.str.rsplit("-", n=1, expand=True)[0]
    for i in range(len(df)):
        s=df.sets.iloc[i]
        s=s.split("-")
        full_set=[]
        for part in s:
            while part[0]=="0":
                part=part[1:]
            full_set.append(part)
        df.sets.iloc[i]="-".join(full_set)
    return df



#only merge in new prods for the April 3, 10, 17, & 24 pulls of List N which already had the products from the 3-27-2020 and 4-27-2020 CBC lists
prod_temp_apr3=pd.read_csv("product_csv_template_736.csv", dtype=str)
prod_cols=prod_temp_apr3.columns
prod_temp_apr3=EPA_Reg_No_from_filename(prod_temp_apr3)
prod_temp_apr3=prod_temp_apr3.loc[prod_temp_apr3.sets.isin(list(new_prods.sets))]
prod_temp_apr3=prod_temp_apr3.merge(new_prods, on="sets", how="left")
prod_temp_apr3.title=prod_temp_apr3.prod_name
prod_temp_apr3.model_number=prod_temp_apr3.EPA_Reg_No
prod_temp_apr3=prod_temp_apr3[prod_cols]
prod_temp_apr3.fillna("", inplace=True)

prod_temp_apr3.to_csv("new_cbc_prods_05012020_for_listN_04032020.csv", index=False)



prod_temp_apr10=pd.read_csv("product_csv_template_769.csv", dtype=str)
prod_cols=prod_temp_apr10.columns
prod_temp_apr10=EPA_Reg_No_from_filename(prod_temp_apr10)
prod_temp_apr10=prod_temp_apr10.loc[prod_temp_apr10.sets.isin(list(new_prods.sets))]
prod_temp_apr10=prod_temp_apr10.merge(new_prods, on="sets", how="left")
prod_temp_apr10.title=prod_temp_apr10.prod_name
prod_temp_apr10.model_number=prod_temp_apr10.EPA_Reg_No
prod_temp_apr10=prod_temp_apr10[prod_cols]
prod_temp_apr10.fillna("", inplace=True)

prod_temp_apr10.to_csv("new_cbc_prods_05012020_for_listN_04102020.csv", index=False)




prod_temp_apr17=pd.read_csv("product_csv_template_773.csv", dtype=str)
prod_temp_apr17=EPA_Reg_No_from_filename(prod_temp_apr17)
prod_temp_apr17=prod_temp_apr17.loc[prod_temp_apr17.sets.isin(list(new_prods.sets))]
prod_temp_apr17=prod_temp_apr17.merge(new_prods, on="sets", how="left")
prod_temp_apr17.title=prod_temp_apr17.prod_name
prod_temp_apr17.model_number=prod_temp_apr17.EPA_Reg_No
prod_temp_apr17=prod_temp_apr17[prod_cols]
prod_temp_apr17.fillna("", inplace=True)

prod_temp_apr17.to_csv("new_cbc_prods_05012020_for_listN_04172020.csv", index=False)



#No new products to match for April 24th. Dataframe is empty.

# prod_temp_apr24=pd.read_csv("product_csv_template_775.csv", dtype=str)
# prod_temp_apr24=EPA_Reg_No_from_filename(prod_temp_apr24)
# prod_temp_apr24=prod_temp_apr24.loc[prod_temp_apr24.sets.isin(list(new_prods.sets))]
# prod_temp_apr24=prod_temp_apr24.merge(new_prods, on="sets", how="left")
# prod_temp_apr24.title=prod_temp_apr24.prod_name
# prod_temp_apr24.model_number=prod_temp_apr24.EPA_Reg_No
# prod_temp_apr24=prod_temp_apr24[prod_cols]
# prod_temp_apr24.fillna("", inplace=True)
#
# prod_temp_apr24.to_csv("new_cbc_prods_05012020_for_listN_04242020.csv", index=False)




#merge in all prods from the 4-27-2020 CBC list for EPA List N pulls from April 10, 17, & 24 which did not have any exisitng products
prod_temp_may1=pd.read_csv("product_csv_template_780.csv", dtype=str)
prod_cols=prod_temp_may1.columns
prod_temp_may1=EPA_Reg_No_from_filename(prod_temp_may1)
prod_temp_may1=prod_temp_may1.loc[prod_temp_may1.sets.isin(list(cbc_prods.sets))]
prod_temp_may1=prod_temp_may1.merge(cbc_prods, on="sets", how="left")
prod_temp_may1.title=prod_temp_may1.prod_name
prod_temp_may1.model_number=prod_temp_may1.EPA_Reg_No
prod_temp_may1=prod_temp_may1[prod_cols]
prod_temp_may1.fillna("", inplace=True)

prod_temp_may1.to_csv("all_cbc_prods_05012020_for_listN_05012020.csv", index=False)
