#6-8-2020

import pandas as pd
import os
from datetime import date

today=date.today()
today=today.strftime("%m_%d_%Y")

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents")

df=pd.read_excel("EAFUS.xlsx", usecols=[0,1,3], skiprows=[0,1,2,3])
df.rename(columns={df.columns[0]:"cas", df.columns[1]:"chem", df.columns[2]:"use"}, inplace=True)
df.use=df.use.str.replace("<br />", "").str.replace(",",";")

df["data_document_id"]="1556901"
df["data_document_filename"]="EAFUS.xlsx"
df["doc_date"]="March 21, 2019"
df["raw_category"]=""
df["raw_cas"]=df.cas
df["raw_chem_name"]=df.chem
df["cat_code"]=""
df["description_cpcat"]=""
df["cpcat_sourcetype"]=""
df["report_funcuse"]=df.use
df=df[df.columns[3:]]

df.to_csv("EAFUS_extracted_chems_%s.csv"%today, index=False)
