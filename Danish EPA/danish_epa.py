# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 17:02:23 2022

@author: CLUTZ01
"""


from tabula import read_pdf
import pandas as pd
import string
import os
import glob

#questions
# there are no spaces in the final iteration of the chem name in the csv's is this correct?
# all of the document files are the same, does it matter what the document id or the data document file name is?


#################################### 2.1 ########################

#first table on 64
tables=read_pdf("c.pdf", pages="64", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_1=tables[0]
table_1["raw_chem_name"]=table_1.iloc[1:,2]
table_1=table_1.dropna(subset=["raw_chem_name"])
table_1=table_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1)):
    table_1["raw_chem_name"].iloc[j]=str(table_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_1["raw_chem_name"].iloc[j]=clean(str(table_1["raw_chem_name"].iloc[j]))
    if len(table_1["raw_chem_name"].iloc[j].split())>1:
        table_1["raw_chem_name"].iloc[j]="".join(table_1["raw_chem_name"].iloc[j].split())

table_1["data_document_id"]="1374362"
table_1["data_document_filename"]="c.pdf"
table_1["doc_date"]="March 2019"
table_1["raw_category"]=""
table_1["raw_cas"]=""
table_1["report_funcuse"]="Surfactant"
table_1["cat_code"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_1["component"]=""
table_1["chem_detected_flag"]=""

table_1.to_csv("dan_epa_append2_1_table1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)



#second table start on 64 end on 66
tables2=read_pdf("b.pdf", pages="64,65,66", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2=pd.concat([tables2[1],tables2[2],tables2[3]], ignore_index=True)
table_2["raw_chem_name"]=table_2.iloc[1:,0]
table_2["report_funcuse"]=table_2.iloc[1:,1]
table_2=table_2.dropna(subset=["raw_chem_name"])
table_2=table_2[["raw_chem_name", "report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))
    if len(table_2["raw_chem_name"].iloc[j].split())>1:
        table_2["raw_chem_name"].iloc[j]="".join(table_2["raw_chem_name"].iloc[j].split())

table_2["data_document_id"]="1374362"
table_2["data_document_filename"]="c.pdf"
table_2["doc_date"]="March 2019"
table_2["raw_category"]=""
table_2["raw_cas"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2["component"]=""
table_2["chem_detected_flag"]=""

table_2.to_csv("dan_epa_append2_1_table2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)


#Complexing agents/Builders table
tables3=read_pdf("b.pdf", pages="66", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3=tables3[1]
table_3["raw_chem_name"]=table_3.iloc[1:,0]
table_3=table_3.dropna(subset=["raw_chem_name"])
table_3=table_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3["raw_chem_name"].iloc[j]=clean(str(table_3["raw_chem_name"].iloc[j]))
    if len(table_3["raw_chem_name"].iloc[j].split())>1:
        table_3["raw_chem_name"].iloc[j]="".join(table_3["raw_chem_name"].iloc[j].split())

table_3["data_document_id"]="1374362"
table_3["data_document_filename"]="c.pdf"
table_3["doc_date"]="March 2019"
table_3["raw_category"]=""
table_3["report_funcuse"]="Complexing Agents/Builders"
table_3["raw_cas"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3["component"]=""
table_3["chem_detected_flag"]=""



table_3.to_csv("dan_epa_append2_1_table3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)


#Bleaching Agents table

tables_bleach=read_pdf("b.pdf", pages="66", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_4=tables_bleach[2]
table_4["raw_chem_name"]=table_4.iloc[1:,0]
table_4=table_4.dropna(subset=["raw_chem_name"])
table_4=table_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))
    if len(table_4["raw_chem_name"].iloc[j].split())>1:
        table_4["raw_chem_name"].iloc[j]="".join(table_4["raw_chem_name"].iloc[j].split())

table_4["data_document_id"]="1374362"
table_4["data_document_filename"]="c.pdf"
table_4["doc_date"]="March 2019"
table_4["raw_category"]=""
table_4["report_funcuse"]="Bleaching Agents"
table_4["raw_cas"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_4["component"]=""
table_4["chem_detected_flag"]=""



table_4.to_csv("dan_epa_append2_1_table4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)

#Enzymes table
tables_enz=read_pdf("b.pdf", pages="66", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5=tables_enz[3]
table_5["raw_chem_name"]=table_5.iloc[1:,0]
table_5=table_5.dropna(subset=["raw_chem_name"])
table_5=table_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]="".join(table_5["raw_chem_name"].iloc[j].split())

table_5["data_document_id"]="1374362"
table_5["data_document_filename"]="c.pdf"
table_5["doc_date"]="March 2019"
table_5["raw_category"]=""
table_5["report_funcuse"]="Enzymes"
table_5["raw_cas"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_5["component"]=""
table_5["chem_detected_flag"]=""



table_5.to_csv("dan_epa_append2_1_table5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)

#Fragrances table
tables_frag=read_pdf("b.pdf", pages="66", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_6=tables_frag[3]
table_6["raw_chem_name"]=table_6.iloc[1:,0]
table_6=table_6.dropna(subset=["raw_chem_name"])
table_6=table_6[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]="".join(table_6["raw_chem_name"].iloc[j].split())

table_6["data_document_id"]="1374362"
table_6["data_document_filename"]="c.pdf"
table_6["doc_date"]="March 2019"
table_6["raw_category"]=""
table_6["report_funcuse"]="Fragrances"
table_6["raw_cas"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"
table_6["component"]=""
table_6["chem_detected_flag"]=""



table_6.to_csv("dan_epa_append2_1_table6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)





path = os.getcwd()
files = os.path.join(path, "dan_epa_append2_1_table*.csv")

files = glob.glob(files)


# joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)


df.to_csv("danish_epa_appx2_1.csv")



#################################### 2.2 ########################
#first table
tables221=read_pdf("c.pdf", pages="68", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_1=tables221[0]
table_2_1["raw_chem_name"]=table_2_1.iloc[1:,2]
table_2_1=table_2_1.dropna(subset=["raw_chem_name"])
table_2_1=table_2_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_1)):
    table_2_1["raw_chem_name"].iloc[j]=str(table_2_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2_1["raw_chem_name"].iloc[j]=clean(str(table_2_1["raw_chem_name"].iloc[j]))
    if len(table_2_1["raw_chem_name"].iloc[j].split())>1:
        table_2_1["raw_chem_name"].iloc[j]="".join(table_2_1["raw_chem_name"].iloc[j].split())

table_2_1["data_document_id"]="1374362"
table_2_1["data_document_filename"]="c.pdf"
table_2_1["doc_date"]="March 2019"
table_2_1["raw_category"]=""
table_2_1["raw_cas"]=""
table_2_1["report_funcuse"]="Surfactant"
table_2_1["cat_code"]=""
table_2_1["description_cpcat"]=""
table_2_1["cpcat_code"]=""
table_2_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_1["component"]=""
table_2_1["chem_detected_flag"]=""

table_2_1.to_csv("dan_epa_append2_2_table1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)



#table of ingredients with other function
tables222=read_pdf("b.pdf", pages="68,69", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_2=pd.concat([tables222[1],tables222[2]], ignore_index=True)
table_2_2["raw_chem_name"]=table_2_2.iloc[1:,0]
table_2_2["report_funcuse"]=table_2_2.iloc[1:,1]
table_2_2=table_2_2.dropna(subset=["raw_chem_name"])
table_2_2=table_2_2[["raw_chem_name", "report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_2)):
    table_2_2["raw_chem_name"].iloc[j]=str(table_2_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2_2["raw_chem_name"].iloc[j]=clean(str(table_2_2["raw_chem_name"].iloc[j]))
    if len(table_2_2["raw_chem_name"].iloc[j].split())>1:
        table_2_2["raw_chem_name"].iloc[j]="".join(table_2_2["raw_chem_name"].iloc[j].split())

table_2_2["data_document_id"]="1374362"
table_2_2["data_document_filename"]="c.pdf"
table_2_2["doc_date"]="March 2019"
table_2_2["raw_category"]=""
table_2_2["raw_cas"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_2["component"]=""
table_2_2["chem_detected_flag"]=""


table_2_2.to_csv("dan_epa_append2_2_table2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)


#Complexing agents/Builders table
tables223=read_pdf("b.pdf", pages="69", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_3=tables223[1]
table_2_3["raw_chem_name"]=table_2_3.iloc[1:,0]
table_2_3=table_2_3.dropna(subset=["raw_chem_name"])
table_2_3=table_2_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_3)):
    table_2_3["raw_chem_name"].iloc[j]=str(table_2_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2_3["raw_chem_name"].iloc[j]=clean(str(table_2_3["raw_chem_name"].iloc[j]))
    if len(table_2_3["raw_chem_name"].iloc[j].split())>1:
        table_2_3["raw_chem_name"].iloc[j]="".join(table_2_3["raw_chem_name"].iloc[j].split())

table_2_3["data_document_id"]="1374362"
table_2_3["data_document_filename"]="c.pdf"
table_2_3["doc_date"]="March 2019"
table_2_3["raw_category"]=""
table_2_3["report_funcuse"]="Complexing Agents/Builders"
table_2_3["raw_cas"]=""
table_2_3["cat_code"]=""
table_2_3["description_cpcat"]=""
table_2_3["cpcat_code"]=""
table_2_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_3["component"]=""
table_2_3["chem_detected_flag"]=""



table_2_3.to_csv("dan_epa_append2_2_table3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)


#Bleaching Agents table

tables224=read_pdf("b.pdf", pages="66", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_4=tables224[2]
table_2_4["raw_chem_name"]=table_2_4.iloc[1:,0]
table_2_4=table_2_4.dropna(subset=["raw_chem_name"])
table_2_4=table_2_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_4)):
    table_2_4["raw_chem_name"].iloc[j]=str(table_2_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2_4["raw_chem_name"].iloc[j]=clean(str(table_2_4["raw_chem_name"].iloc[j]))
    if len(table_2_4["raw_chem_name"].iloc[j].split())>1:
        table_2_4["raw_chem_name"].iloc[j]="".join(table_2_4["raw_chem_name"].iloc[j].split())

table_2_4["data_document_id"]="1374362"
table_2_4["data_document_filename"]="c.pdf"
table_2_4["doc_date"]="March 2019"
table_2_4["raw_category"]=""
table_2_4["report_funcuse"]="Bleaching Agents"
table_2_4["raw_cas"]=""
table_2_4["cat_code"]=""
table_2_4["description_cpcat"]=""
table_2_4["cpcat_code"]=""
table_2_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_4["component"]=""
table_2_4["chem_detected_flag"]=""



table_2_4.to_csv("dan_epa_append2_2_table4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)

#Enzymes table
tables225=read_pdf("b.pdf", pages="69", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_5=tables225[3]
table_2_5["raw_chem_name"]=table_2_5.iloc[1:,0]
table_2_5=table_2_5.dropna(subset=["raw_chem_name"])
table_2_5=table_2_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_5)):
    table_2_5["raw_chem_name"].iloc[j]=str(table_2_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2_5["raw_chem_name"].iloc[j]=clean(str(table_2_5["raw_chem_name"].iloc[j]))
    if len(table_2_5["raw_chem_name"].iloc[j].split())>1:
        table_2_5["raw_chem_name"].iloc[j]="".join(table_2_5["raw_chem_name"].iloc[j].split())

table_2_5["data_document_id"]="1374362"
table_2_5["data_document_filename"]="c.pdf"
table_2_5["doc_date"]="March 2019"
table_2_5["raw_category"]=""
table_2_5["report_funcuse"]="Enzymes"
table_2_5["raw_cas"]=""
table_2_5["cat_code"]=""
table_2_5["description_cpcat"]=""
table_2_5["cpcat_code"]=""
table_2_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_5["component"]=""
table_2_5["chem_detected_flag"]=""



table_2_5.to_csv("dan_epa_append2_2_table5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)

#Fragrances table
tables226=read_pdf("b.pdf", pages="70", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_2_6=tables226[0]
table_2_6["raw_chem_name"]=table_2_6.iloc[1:,0]
table_2_6=table_2_6.dropna(subset=["raw_chem_name"])
table_2_6=table_2_6[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_6)):
    table_2_6["raw_chem_name"].iloc[j]=str(table_2_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_2_6["raw_chem_name"].iloc[j]=clean(str(table_2_6["raw_chem_name"].iloc[j]))
    if len(table_2_6["raw_chem_name"].iloc[j].split())>1:
        table_2_6["raw_chem_name"].iloc[j]="".join(table_2_6["raw_chem_name"].iloc[j].split())

table_2_6["data_document_id"]="1374362"
table_2_6["data_document_filename"]="c.pdf"
table_2_6["doc_date"]="March 2019"
table_2_6["raw_category"]=""
table_2_6["report_funcuse"]="Fragrances"
table_2_6["raw_cas"]=""
table_2_6["cat_code"]=""
table_2_6["description_cpcat"]=""
table_2_6["cpcat_code"]=""
table_2_6["cpcat_sourcetype"]="ACToR Assays and Lists"
table_2_6["component"]=""
table_2_6["chem_detected_flag"]=""



table_2_6.to_csv("dan_epa_append2_2_table6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)





path = os.getcwd()
files2 = os.path.join(path, "dan_epa_append2_2_table*.csv")

files2 = glob.glob(files2)


# joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files2), ignore_index=True)


df.to_csv("danish_epa_appx2_2.csv")



#################################### 2.3 ########################
#first table
tables231=read_pdf("c.pdf", pages="68", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_1=tables231[0]
table_3_1["raw_chem_name"]=table_3_1.iloc[1:,2]
table_3_1=table_3_1.dropna(subset=["raw_chem_name"])
table_3_1=table_3_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[j]=str(table_3_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3_1["raw_chem_name"].iloc[j]=clean(str(table_3_1["raw_chem_name"].iloc[j]))
    if len(table_3_1["raw_chem_name"].iloc[j].split())>1:
        table_3_1["raw_chem_name"].iloc[j]="".join(table_3_1["raw_chem_name"].iloc[j].split())

table_3_1["data_document_id"]="1374362"
table_3_1["data_document_filename"]="c.pdf"
table_3_1["doc_date"]="March 2019"
table_3_1["raw_category"]=""
table_3_1["raw_cas"]=""
table_3_1["report_funcuse"]="Surfactant"
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_1["component"]=""
table_3_1["chem_detected_flag"]=""

table_3_1.to_csv("dan_epa_append2_3_table1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)



#table of ingredients with other function
tables232=read_pdf("b.pdf", pages="71", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_2=pd.concat([tables232[1]], ignore_index=True)
table_3_2["raw_chem_name"]=table_3_2.iloc[1:,0]
table_3_2["report_funcuse"]=table_3_2.iloc[1:,1]
table_3_2=table_3_2.dropna(subset=["raw_chem_name"])
table_3_2=table_3_2[["raw_chem_name", "report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    if len(table_3_2["raw_chem_name"].iloc[j].split())>1:
        table_3_2["raw_chem_name"].iloc[j]="".join(table_3_2["raw_chem_name"].iloc[j].split())

table_3_2["data_document_id"]="1374362"
table_3_2["data_document_filename"]="c.pdf"
table_3_2["doc_date"]="March 2019"
table_3_2["raw_category"]=""
table_3_2["raw_cas"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_2["component"]=""
table_3_2["chem_detected_flag"]=""

table_3_2.to_csv("dan_epa_append2_3_table2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)

#Complexing agents/Builders table
tables233=read_pdf("b.pdf", pages="72", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_3=tables233[0]
table_3_3["raw_chem_name"]=table_3_3.iloc[1:,0]
table_3_3=table_3_3.dropna(subset=["raw_chem_name"])
table_3_3=table_3_3[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[j]=str(table_3_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3_3["raw_chem_name"].iloc[j]=clean(str(table_3_3["raw_chem_name"].iloc[j]))
    if len(table_3_3["raw_chem_name"].iloc[j].split())>1:
        table_3_3["raw_chem_name"].iloc[j]="".join(table_3_3["raw_chem_name"].iloc[j].split())

table_3_3["data_document_id"]="1374362"
table_3_3["data_document_filename"]="c.pdf"
table_3_3["doc_date"]="March 2019"
table_3_3["raw_category"]=""
table_3_3["report_funcuse"]="Complexing Agents/Builders"
table_3_3["raw_cas"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_3["component"]=""
table_3_3["chem_detected_flag"]=""



table_3_3.to_csv("dan_epa_append2_3_table3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)

#Bleaching Agents table

tables234=read_pdf("b.pdf", pages="72", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_4=tables234[1]
table_3_4["raw_chem_name"]=table_3_4.iloc[1:,0]
table_3_4=table_3_4.dropna(subset=["raw_chem_name"])
table_3_4=table_3_4[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_4)):
    table_3_4["raw_chem_name"].iloc[j]=str(table_3_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3_4["raw_chem_name"].iloc[j]=clean(str(table_3_4["raw_chem_name"].iloc[j]))
    if len(table_3_4["raw_chem_name"].iloc[j].split())>1:
        table_3_4["raw_chem_name"].iloc[j]="".join(table_3_4["raw_chem_name"].iloc[j].split())

table_3_4["data_document_id"]="1374362"
table_3_4["data_document_filename"]="c.pdf"
table_3_4["doc_date"]="March 2019"
table_3_4["raw_category"]=""
table_3_4["report_funcuse"]="Bleaching Agents"
table_3_4["raw_cas"]=""
table_3_4["cat_code"]=""
table_3_4["description_cpcat"]=""
table_3_4["cpcat_code"]=""
table_3_4["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_4["component"]=""
table_3_4["chem_detected_flag"]=""



table_3_4.to_csv("dan_epa_append2_3_table4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)


#Fragrances table
tables235=read_pdf("b.pdf", pages="72", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_3_5=tables235[2]
table_3_5["raw_chem_name"]=table_3_5.iloc[1:,0]
table_3_5=table_3_5.dropna(subset=["raw_chem_name"])
table_3_5=table_3_5[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_5)):
    table_3_5["raw_chem_name"].iloc[j]=str(table_3_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table_3_5["raw_chem_name"].iloc[j]=clean(str(table_3_5["raw_chem_name"].iloc[j]))
    if len(table_3_5["raw_chem_name"].iloc[j].split())>1:
        table_3_5["raw_chem_name"].iloc[j]="".join(table_3_5["raw_chem_name"].iloc[j].split())

table_3_5["data_document_id"]="1374362"
table_3_5["data_document_filename"]="c.pdf"
table_3_5["doc_date"]="March 2019"
table_3_5["raw_category"]=""
table_3_5["report_funcuse"]="Fragrances"
table_3_5["raw_cas"]=""
table_3_5["cat_code"]=""
table_3_5["description_cpcat"]=""
table_3_5["cpcat_code"]=""
table_3_5["cpcat_sourcetype"]="ACToR Assays and Lists"
table_3_5["component"]=""
table_3_5["chem_detected_flag"]=""



table_3_5.to_csv("dan_epa_append2_3_table5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)




path = os.getcwd()
files3 = os.path.join(path, "dan_epa_append2_3_table*.csv")

files3 = glob.glob(files3)


# joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files3), ignore_index=True)


df.to_csv("danish_epa_appx2_3.csv")



#############################Appendix 3###################
tables3_1=read_pdf("b.pdf", pages="73", lattice=True, multiple_tables=True, pandas_options={'header': None})
table3_1=tables3_1[0]
table3_1["raw_chem_name"]=table3_1.iloc[1:,0]
table3_1["report_funcuse"]=table3_1.iloc[1:,1]
table3_1=table3_1.dropna(subset=["raw_chem_name"])
table3_1=table3_1[["raw_chem_name", "report_funcuse"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table3_1)):
    table3_1["raw_chem_name"].iloc[j]=str(table3_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha")
    table3_1["raw_chem_name"].iloc[j]=clean(str(table3_1["raw_chem_name"].iloc[j]))
    if len(table3_1["raw_chem_name"].iloc[j].split())>1:
        table3_1["raw_chem_name"].iloc[j]="".join(table3_1["raw_chem_name"].iloc[j].split())

table3_1["data_document_id"]="1374362"
table3_1["data_document_filename"]="c.pdf"
table3_1["doc_date"]="March 2019"
table3_1["raw_category"]=""
table3_1["raw_cas"]=""
table3_1["cat_code"]=""
table3_1["description_cpcat"]=""
table3_1["cpcat_code"]=""
table3_1["cpcat_sourcetype"]="ACToR Assays and Lists"
table3_1["component"]=""
table3_1["chem_detected_flag"]=""

table3_1.to_csv("dan_epa_append3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype", "component","chem_detected_flag" ], index=False)






