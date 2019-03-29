#Lauren Koval
#3/29/19

from tabula import read_pdf
import pandas as pd
import string

#Read in tables using tabula
tables=read_pdf("document_1359510.pdf", pages="31-34",  multiple_tables= True, pandas_options={'header': None})     

#clean up frames then concat into one large df
frames=[]
for i in range(0,len(tables)):
    temp= tables[i]
    temp=temp.iloc[:,0:2]
    new_header=temp.iloc[0]
    temp=temp[2:]
    temp.columns= new_header
    frames.append(temp)

df=pd.concat(frames, ignore_index= True)

#Deals with long chemical names that are spread across multiple lines. n-Alkanes
# was the only chemical that didn't have a reported cas so we omit when searching
#for bad names which are identified by not having a cas in all but the first line
#of the name.
for j in range(0,len(df)):
    if df["Identification"][j] != "n-Alkanes (C21+)" and pd.isnull(df["CAS-no."][j])==True:
        corrected_name= df["Identification"][j-1]+" "+df["Identification"][j]
        df["Identification"][j-1]= corrected_name
        df["CAS-no."][j]=df["CAS-no."][j-1]
        df["CAS-no."][j-1]=1
        df["Identification"][j]=corrected_name

#drops bad rows and duplicates
df=df.loc[df["CAS-no."]!=1]
df=df.drop_duplicates()
df=df.reset_index()
df=df.drop(columns=["index"])


#changes column names for cas info and and chem names. Adds rest of information
#specified in ticket
df["raw_category"]="Consumer Products: Toys"
df["raw_cas"]=df["CAS-no."]
df["raw_chem_name"]=df["Identification"]
df["cat_code"]="ACToR_Assays_159"
df["description_cpcat"]="toys arts_crafts child_use detected"
df["cpcat_code"]="DCPS_93_AID_1; DCPS_93_AID_2"
df["cpcat_sourcetype"]="ACToR Assays and Lists"

#removes non ASCII characters and replaces commas with undescores in all
#chemical_names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for k in range(0, len(df)):
    df["raw_chem_name"][k]=clean(df["raw_chem_name"][k])
    df["raw_chem_name"][k]=df["raw_chem_name"][k].replace(",", "_")


#drops no longer relevant columns and writes df to csv
df=df.drop(columns=["Identification","CAS-no."])
df.to_csv("dcps_93_extraction.csv", index=False, header= False)
