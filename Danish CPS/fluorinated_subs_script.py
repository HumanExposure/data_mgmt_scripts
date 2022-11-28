# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 14:49:17 2022

@author: CLUTZ01
"""


import os
import pandas as pd
import numpy as np
import string
import tabula
import glob


os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Desktop/Extraction Scripts/fluorinated_substances')



#table 4

table4=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="21", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4=table4[1]



table_4["raw_chem_name"]=table_4.iloc[0:,0]
table_4=table_4.dropna(subset=["raw_chem_name"])
table_4=table_4[["raw_chem_name"]]
table_4 = table_4[table_4["raw_chem_name"].str.contains("INCI name|stance") == False]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha")
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))
  


table_4["data_document_id"]="1656714"
table_4["data_document_filename"]="k.pdf"
table_4["doc_date"]="October 2018"
table_4["raw_category"]=""
table_4["raw_cas"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4.to_csv("fluorinated_substances_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)




#table 5
table5=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="22-23", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5=pd.concat([table5[0], table5[1]], ignore_index=True)



table_5["raw_chem_name"]=table_5.iloc[0:,0]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5[["raw_chem_name"]]
table_5 = table_5[table_5["raw_chem_name"].str.contains("INCI name|stance") == False]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
  


table_5["data_document_id"]="1374372"
table_5["data_document_filename"]="b.pdf"
table_5["doc_date"]="October 2018"
table_5["raw_category"]=""
table_5["raw_cas"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5.to_csv("fluorinated_substances_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)




#table 6
table6=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="23-24", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6=pd.concat([table6[0], table6[1]], ignore_index=True)



table_6["raw_chem_name"]=table_6.iloc[0:,0]
table_6=table_6.dropna(subset=["raw_chem_name"])
table_6=table_6[["raw_chem_name"]]
table_6 = table_6[table_6["raw_chem_name"].str.contains("INCI name") == False]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha")
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
  


table_6["data_document_id"]="1374373"
table_6["data_document_filename"]="c.pdf"
table_6["doc_date"]="October 2018"
table_6["raw_category"]=""
table_6["raw_cas"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6.to_csv("fluorinated_substances_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 7
table7=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="24", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_7=table7[1]


table_7["raw_chem_name"]=table_7.iloc[0:,0]
table_7=table_7.dropna(subset=["raw_chem_name"])
table_7=table_7[["raw_chem_name"]]
table_7 = table_7[table_7["raw_chem_name"].str.contains("Substance") == False]



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).strip().replace("α","alpha")
    table_7["raw_chem_name"].iloc[j]=clean(str(table_7["raw_chem_name"].iloc[j]))
  


table_7["data_document_id"]="1374374"
table_7["data_document_filename"]="d.pdf"
table_7["doc_date"]="October 2018"
table_7["raw_category"]=""
table_7["raw_cas"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_7.to_csv("fluorinated_substances_table_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 8
table8=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="25-26", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_8=pd.concat([table8[0], table8[1]], ignore_index=True)


table_8["raw_chem_name"]=table_8.iloc[0:,1]
table_8=table_8.dropna(subset=["raw_chem_name"])
table_8=table_8[["raw_chem_name"]]
table_8=table_8[~table_8.raw_chem_name.str.contains("Product|not specified")]


table_8=table_8['raw_chem_name'].unique()

table_8 = pd.DataFrame(table_8, columns = ['raw_chem_name'])

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8)):
    table_8["raw_chem_name"].iloc[j]=str(table_8["raw_chem_name"].iloc[j]).strip().replace("α","alpha")
    table_8["raw_chem_name"].iloc[j]=clean(str(table_8["raw_chem_name"].iloc[j]))
  


table_8["data_document_id"]="1374375"
table_8["data_document_filename"]="e.pdf"
table_8["doc_date"]="OCtober 2018"
table_8["raw_category"]=""
table_8["raw_cas"]=""
table_8["cat_code"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_8.to_csv("fluorinated_substances_table_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)




#table 14
table14=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="70", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_14=table14[0]

table_14["raw_chem_name"]=table_14.iloc[0:,0]
table_14=table_14.dropna(subset=["raw_chem_name"])
table_14=table_14[["raw_chem_name"]]


To_remove_lst = ["stance", "Sub-"]
table_14['raw_chem_name'] = table_14['raw_chem_name'].str.replace('|'.join(To_remove_lst), '')
table_14['raw_chem_name'] = table_14['raw_chem_name'].str.strip()

table_14['raw_chem_name'].replace('', np.nan, inplace=True)
table_14.dropna(subset=['raw_chem_name'], inplace=True)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_14)):
    table_14["raw_chem_name"].iloc[j]=str(table_14["raw_chem_name"].iloc[j]).strip().replace("α","alpha")
    table_14["raw_chem_name"].iloc[j]=clean(str(table_14["raw_chem_name"].iloc[j]))
  


table_14["data_document_id"]="1374377"
table_14["data_document_filename"]="g.pdf"
table_14["doc_date"]="October 2018"
table_14["raw_category"]=""
table_14["raw_cas"]=""
table_14["cat_code"]=""
table_14["description_cpcat"]=""
table_14["cpcat_code"]=""
table_14["cpcat_sourcetype"]="ACToR Assays and Lists"

table_14.to_csv("fluorinated_substances_table_14.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



#table 15
table15=tabula.read_pdf("flourinated_substances_cosmetic.pdf", pages="73", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_15=table15[0]

table_15["raw_chem_name"]=table_15.iloc[0:,0]
table_15=table_15.dropna(subset=["raw_chem_name"])
table_15=table_15[["raw_chem_name"]]
To_remove_lst_15 = ["stance", "Substance name", "CASRN"]
table_15['raw_chem_name'] = table_15['raw_chem_name'].str.replace('|'.join(To_remove_lst_15), '')


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_15)):
    table_15["raw_chem_name"].iloc[j]=str(table_15["raw_chem_name"].iloc[j]).strip().replace("α","alpha")
    table_15["raw_chem_name"].iloc[j]=clean(str(table_15["raw_chem_name"].iloc[j]))


table_15['raw_chem_name'].replace('', np.nan, inplace=True)
table_15.dropna(subset=['raw_chem_name'], inplace=True)


table_15["data_document_id"]="1374378"
table_15["data_document_filename"]="h.pdf"
table_15["doc_date"]="October 2018"
table_15["raw_category"]=""
table_15["raw_cas"]=""
table_15["cat_code"]=""
table_15["description_cpcat"]=""
table_15["cpcat_code"]=""
table_15["cpcat_sourcetype"]="ACToR Assays and Lists"

table_15.to_csv("fluorinated_substances_table_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)






###Joining files

path = os.getcwd()
files = os.path.join(path, "fluorinated_substances_table_*.csv")

files = glob.glob(files)


# joining files with concat and read_csv
fluorinated_df = pd.concat(map(pd.read_csv, files), ignore_index=True)


fluorinated_df.to_csv("fluorinated_substances.csv", index=False)














