#Lauren Koval
#4/11/19
#Annex to the HYDROCHECK procedure for acceptance of Materials in contact with Drinking Water
#Annex-Positive Lists

from tabula import read_pdf
import pandas as pd
import string

#Primary source only contains one table that spans multiple pages. This reads and concats the pieces of the table on all pages but the first into a single pandas df.
tables=read_pdf("document_1372108.pdf", pages="6,7,8,9,10,11,12", guess=False, multiple_tables=True, pandas_options={'header': None})

df=pd.concat([tables[0],tables[1],tables[2],tables[3],tables[4],tables[5],tables[6]], ignore_index=True)
df=df.iloc[:,0:2]
df.columns=["raw_cas","raw_chem_name"]
df=df.loc[df["raw_cas"]!= "2010-03-23"]
df=df.dropna(how="all")

#This reads in the part of the table on the first page on which the table occurs
first_page= table=read_pdf("document_1370042.pdf", pages="5",stream=True, guess=False)
first_page=first_page.iloc[2:]
first_page=first_page.reset_index()
first_page["combined chem/cas"]=""
first_page["raw_cas"]=""
first_page["raw_chem_name"]=""

#Deals with formatting in first_page where all information for each row is in single string
for i in range(0, len(first_page)):
    first_page["combined chem/cas"].iloc[i]=first_page.iloc[i,1].strip().split()

    if  len(first_page["combined chem/cas"].iloc[i])> 2 and "as" in first_page["combined chem/cas"].iloc[i][-2]:
        first_page["combined chem/cas"].iloc[i]=first_page["combined chem/cas"].iloc[i][:-2]
    elif  len(first_page["combined chem/cas"].iloc[i])> 2 and "(1)" in first_page["combined chem/cas"].iloc[i][-1]:
        first_page["combined chem/cas"].iloc[i]=first_page["combined chem/cas"].iloc[i][:-1]


    if first_page["combined chem/cas"].iloc[i][-1].replace(".","").isdigit():
        first_page["combined chem/cas"].iloc[i]=first_page["combined chem/cas"].iloc[i][:-1]

    if len(first_page["combined chem/cas"].iloc[i])==2:
        first_page["raw_cas"].iloc[i]=first_page["combined chem/cas"].iloc[i][0]
        first_page["raw_chem_name"].iloc[i]=first_page["combined chem/cas"].iloc[i][1]
    else:
        first_page["raw_cas"].iloc[i]=first_page["combined chem/cas"].iloc[i][0]
        first_page["raw_chem_name"].iloc[i]=" ".join(first_page["combined chem/cas"].iloc[i][1:])

first_page=first_page.loc[first_page["raw_cas"]!= "2010-03-23"]
first_page=first_page.reset_index()
first_page=first_page[["raw_cas", "raw_chem_name"]]

#Concats first_page to df with the rest of the table
df=pd.concat([first_page, df], ignore_index=True)

j_drop=[]
for j in range(0, len(df)):
    if (pd.isnull(df["raw_cas"].iloc[j])==False) and (pd.isnull(df["raw_chem_name"].iloc[j])==False):
        good_j=j
    elif (pd.isnull(df["raw_cas"].iloc[j])==True) and (pd.isnull(df["raw_chem_name"].iloc[j])==False):
        df["raw_chem_name"].iloc[good_j]=df["raw_chem_name"].iloc[good_j]+df["raw_chem_name"].iloc[j]
        j_drop.append(j)

df=df.drop(j_drop)
df=df.drop_duplicates()
df=df.reset_index()
df=df.drop(columns="index")

#clean everything up a bit
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for k in range(0, len(df)):
    df["raw_chem_name"].iloc[k]=clean(str(df["raw_chem_name"].iloc[k]))
    df["raw_chem_name"].iloc[k]=df["raw_chem_name"].iloc[k].replace(",", "_")
    df["raw_cas"].iloc[k]=clean(str(df["raw_cas"].iloc[k]))
    df["raw_cas"].iloc[k]=df["raw_cas"].iloc[k].replace(",", "_")

#Add rest of information
df["data_document_id"]=1372108
df["data_document_filename"]="Positive List_a.pdf.pdf"
df["doc_date"]="23 March 2010"

df.to_csv("belgium_hydrocheck_annex_extraction.csv",columns=["data_document_id","data_document_filename","doc_date","raw_cas","raw_chem_name"], index=False)
