#lkoval
#5-8-19

from tabula import read_pdf
import pandas as pd
import string

#Table 4.5
table_4_5=read_pdf("document_1372984.pdf", pages="28-30", lattice=True, pandas_options={'header': None})
table_4_5["raw_cas"]=table_4_5.iloc[3:,1]
table_4_5["raw_chem_name"]=table_4_5.iloc[3:,0]
table_4_5=table_4_5.loc[table_4_5["raw_cas"]!= "CAS No."]
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name","raw_cas"]]

table_4_5=table_4_5.loc[table_4_5["raw_chem_name"]!= "CAS No."]
table_4_5=table_4_5.loc[table_4_5["raw_chem_name"]!= "INCI Name"]
table_4_5=table_4_5.loc[table_4_5["raw_chem_name"]!= "Function"]
table_4_5=table_4_5.loc[table_4_5["raw_chem_name"]!= "ist)"]

table_4_5=table_4_5.reset_index()

table_4_5=table_4_5[["raw_chem_name","raw_cas"]]
table_4_5=table_4_5.dropna(how="all")
table_4_5=table_4_5.reset_index()
table_4_5=table_4_5[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_5)):
    table_4_5["raw_chem_name"].iloc[j]=str(table_4_5["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha").replace("ω","omega").replace(".","")
    table_4_5["raw_chem_name"].iloc[j]=clean(str(table_4_5["raw_chem_name"].iloc[j]))
    if len(table_4_5["raw_chem_name"].iloc[j].split())>1:
        table_4_5["raw_chem_name"].iloc[j]=" ".join(table_4_5["raw_chem_name"].iloc[j].split())

table_4_5["data_document_id"]="1372984"
table_4_5["data_document_filename"]="DCPS_88_a.pdf"
table_4_5["doc_date"]="2007"
table_4_5["raw_category"]=""
table_4_5["cat_code"]=""
table_4_5["description_cpcat"]=""
table_4_5["cpcat_code"]=""
table_4_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_5.to_csv("dcps_88_table_4_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 4.7
table_4_7=read_pdf("document_1372986.pdf", pages="33", lattice=True, pandas_options={'header': None})
table_4_7["raw_cas"]=table_4_7.iloc[:,4]
table_4_7["raw_chem_name"]=table_4_7.iloc[:,0]
table_4_7=table_4_7.loc[table_4_7["raw_chem_name"]!= "INCI Name"]
table_4_7=table_4_7.reset_index()
table_4_7=table_4_7[["raw_chem_name","raw_cas"]]
table_4_7=table_4_7.dropna(how="all")
table_4_7=table_4_7.reset_index()
table_4_7=table_4_7[["raw_chem_name","raw_cas"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_7)):
    table_4_7["raw_chem_name"].iloc[i]=str(table_4_7["raw_chem_name"].iloc[i]).strip().lower()
    table_4_7["raw_chem_name"].iloc[i]=clean(str(table_4_7["raw_chem_name"].iloc[i]))
    if str(table_4_7["raw_cas"].iloc[i])=="nan":
        table_4_7["raw_chem_name"].iloc[i-1]=table_4_7["raw_chem_name"].iloc[i-1]+" "+table_4_7["raw_chem_name"].iloc[i]
        i_drop.append(i)

table_4_7=table_4_7.drop(i_drop)
table_4_7=table_4_7.reset_index()
table_4_7=table_4_7[["raw_cas","raw_chem_name"]]

table_4_7["data_document_id"]="1372986"
table_4_7["data_document_filename"]="DCPS_88_b.pdf"
table_4_7["doc_date"]="2007"
table_4_7["raw_category"]=""
table_4_7["cat_code"]=""
table_4_7["description_cpcat"]=""
table_4_7["cpcat_code"]=""
table_4_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_7.to_csv("dcps_88_table_4_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.10
table_4_10=read_pdf("document_1372987.pdf", pages="37,38", lattice=True, pandas_options={'header': None})
table_4_10["raw_chem_name"]=table_4_10.iloc[1:,0]
table_4_10=table_4_10.dropna(subset=["raw_chem_name"])
table_4_10=table_4_10.drop(9)
table_4_10=table_4_10.reset_index()
table_4_10=table_4_10[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_10)):
    table_4_10["raw_chem_name"].iloc[i]=str(table_4_10["raw_chem_name"].iloc[i]).strip().lower().replace("α","alpha")
    table_4_10["raw_chem_name"].iloc[i]=clean(str(table_4_10["raw_chem_name"].iloc[i]))
    if len(table_4_10["raw_chem_name"].iloc[i].split())>1:
        table_4_10["raw_chem_name"].iloc[i]=" ".join(table_4_10["raw_chem_name"].iloc[i].split())

table_4_10["data_document_id"]="1372987"
table_4_10["data_document_filename"]="DCPS_88_c.pdf"
table_4_10["doc_date"]="2007"
table_4_10["raw_category"]=""
table_4_10["cat_code"]=""
table_4_10["description_cpcat"]=""
table_4_10["cpcat_code"]=""
table_4_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_10.to_csv("dcps_88_table_4_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.12
tables=read_pdf("document_1372988.pdf", pages="39,40", multiple_tables=True, lattice=True, pandas_options={'header': None})
table_4_12=pd.concat([tables[1],tables[2]])
table_4_12["raw_chem_name"]=table_4_12.iloc[:,0]
table_4_12["occurence"]=table_4_12.iloc[:,2]
table_4_12=table_4_12.loc[table_4_12["raw_chem_name"]!= "INCI Name"]
table_4_12=table_4_12.reset_index()
table_4_12=table_4_12[["raw_chem_name","occurence"]]
table_4_12=table_4_12.dropna(subset=["raw_chem_name"])
table_4_12=table_4_12.reset_index()
table_4_12=table_4_12[["raw_chem_name","occurence"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_12)):
    table_4_12["raw_chem_name"].iloc[i]=str(table_4_12["raw_chem_name"].iloc[i]).strip().lower()
    table_4_12["raw_chem_name"].iloc[i]=clean(str(table_4_12["raw_chem_name"].iloc[i]))
    if str(table_4_12["occurence"].iloc[i])=="nan":
        table_4_12["raw_chem_name"].iloc[i-1]=table_4_12["raw_chem_name"].iloc[i-1]+" "+table_4_12["raw_chem_name"].iloc[i]
        i_drop.append(i)
    elif str(table_4_12["occurence"].iloc[i])=="formaledehyde":
            table_4_12["raw_chem_name"].iloc[i-2]=table_4_12["raw_chem_name"].iloc[i-2]+" "+table_4_12["raw_chem_name"].iloc[i]
            i_drop.append(i)

table_4_12=table_4_12.drop(i_drop)
table_4_12=table_4_12.reset_index()
table_4_12=table_4_12[["raw_chem_name"]]

for j in range(0,len(table_4_12)):
    if table_4_12["raw_chem_name"].iloc[j].endswith("2"):
        table_4_12["raw_chem_name"].iloc[j]=table_4_12["raw_chem_name"].iloc[j][:-1]

table_4_12["data_document_id"]="1372988"
table_4_12["data_document_filename"]="DCPS_88_d.pdf"
table_4_12["doc_date"]="2007"
table_4_12["raw_category"]=""
table_4_12["cat_code"]=""
table_4_12["description_cpcat"]=""
table_4_12["cpcat_code"]=""
table_4_12["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_12.to_csv("dcps_88_table_4_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 4.13
table_4_13=read_pdf("document_1372989.pdf", pages="41,42", lattice=True, pandas_options={'header': None})
table_4_13["raw_chem_name"]=table_4_13.iloc[:,0]
table_4_13["function"]=table_4_13.iloc[:,2]
table_4_13=table_4_13.loc[table_4_13["raw_chem_name"]!= "INCI Name"]
table_4_13=table_4_13.reset_index()
table_4_13=table_4_13[["raw_chem_name","function"]]
table_4_13=table_4_13.dropna(subset=["raw_chem_name"])
table_4_13=table_4_13.reset_index()
table_4_13=table_4_13[["raw_chem_name","function"]]

i_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_4_13)):
    table_4_13["raw_chem_name"].iloc[i]=str(table_4_13["raw_chem_name"].iloc[i]).strip().lower()
    table_4_13["raw_chem_name"].iloc[i]=clean(str(table_4_13["raw_chem_name"].iloc[i]))
    if str(table_4_13["function"].iloc[i])=="nan":
        table_4_13["raw_chem_name"].iloc[i]=table_4_13["raw_chem_name"].iloc[i-1]+" "+table_4_13["raw_chem_name"].iloc[i]
        i_drop.append(i-1)

table_4_13=table_4_13.drop(i_drop)
table_4_13=table_4_13.reset_index()
table_4_13=table_4_13[["raw_chem_name"]]

table_4_13["data_document_id"]="1372989"
table_4_13["data_document_filename"]="DCPS_88_e.pdf"
table_4_13["doc_date"]="2007"
table_4_13["raw_category"]=""
table_4_13["cat_code"]=""
table_4_13["description_cpcat"]=""
table_4_13["cpcat_code"]=""
table_4_13["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_13.to_csv("dcps_88_table_4_13.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#Table 5.7
table_5_7=read_pdf("document_1372990.pdf", pages="52", lattice=False, pandas_options={'header': None})
table_5_7["raw_chem_name"]=table_5_7.iloc[6:40,0]
table_5_7=table_5_7.dropna(subset=["raw_chem_name"])
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0, len(table_5_7)):
    table_5_7["raw_chem_name"].iloc[i]=str(table_5_7["raw_chem_name"].iloc[i]).strip().lower().replace("α","alpha").replace("ω","omega")
    table_5_7["raw_chem_name"].iloc[i]=clean(str(table_5_7["raw_chem_name"].iloc[i]))

table_5_7["raw_chem_name"].iloc[18]=table_5_7["raw_chem_name"].iloc[18]+table_5_7["raw_chem_name"].iloc[19]+table_5_7["raw_chem_name"].iloc[20]
table_5_7["raw_chem_name"].iloc[23]=table_5_7["raw_chem_name"].iloc[23]+table_5_7["raw_chem_name"].iloc[24]+table_5_7["raw_chem_name"].iloc[25]+table_5_7["raw_chem_name"].iloc[26]
table_5_7["raw_chem_name"].iloc[28]=table_5_7["raw_chem_name"].iloc[28]+table_5_7["raw_chem_name"].iloc[29]+table_5_7["raw_chem_name"].iloc[30]
table_5_7["raw_chem_name"].iloc[31]=table_5_7["raw_chem_name"].iloc[31]+table_5_7["raw_chem_name"].iloc[32]


table_5_7=table_5_7.drop([19,20,24,25,26,29,30,32])
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name"]]

table_5_7["data_document_id"]="1372990"
table_5_7["data_document_filename"]="DCPS_88_f.pdf"
table_5_7["doc_date"]="2007"
table_5_7["raw_category"]=""
table_5_7["cat_code"]=""
table_5_7["description_cpcat"]=""
table_5_7["cpcat_code"]=""
table_5_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_7.to_csv("dcps_88_table_5_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#table 2.2
#Tabula was unable to read the lattice structure for roughly half of the pages of the table. Those that could be read as a lattice were extracted together and those read as stream were extracted together. The two tables were then joined and sorted alphabetically to match the pdf.

latFalseList=[]
latTrueList=[]
b=[]#list of pages not recognized as lattice
g=[]#list of pages recognized as lattice
for k in range(141,170):
    try:
        table=read_pdf("document_1372992.pdf", pages="%d"%k, lattice=True, pandas_options={'header': None})
        latTrueList.append(table)
        g.append(k)
    except:
        table=read_pdf("document_1372992.pdf", pages="%d"%k, lattice=False, pandas_options={'header': None})
        latFalseList.append(table)
        b.append(k)

latTrueTables=pd.concat(latTrueList, ignore_index=True)
latFalseTables=pd.concat(latFalseList, ignore_index=True)

latTrueTables["raw_chem_name"]=latTrueTables.iloc[:,0]
latTrueTables["raw_cas"]=latTrueTables.iloc[:,1]
latTrueTables=latTrueTables[["raw_chem_name","raw_cas"]]
latTrueTables=latTrueTables.dropna(subset=["raw_chem_name"])
latTrueTables=latTrueTables.reset_index()
latTrueTables=latTrueTables[["raw_chem_name","raw_cas"]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for i in range(0,len(latTrueTables)):
    latTrueTables["raw_chem_name"].iloc[i]=clean(str(latTrueTables["raw_chem_name"].iloc[i]))
    latTrueTables["raw_chem_name"].iloc[i]=str(latTrueTables["raw_chem_name"].iloc[i]).strip().lower()
    if len(latTrueTables["raw_chem_name"].iloc[i].split())>1:
        latTrueTables["raw_chem_name"].iloc[i]=" ".join(latTrueTables["raw_chem_name"].iloc[i].split())
    if len(str(latTrueTables["raw_cas"].iloc[i]).split())>1:
        latTrueTables["raw_cas"].iloc[i]="".join(str(latTrueTables["raw_cas"].iloc[i]).split())

latTrueTables=latTrueTables.loc[latTrueTables["raw_chem_name"]!= "inci name"]
latTrueTables=latTrueTables.loc[latTrueTables["raw_chem_name"]!= "function"]
latTrueTables=latTrueTables.loc[latTrueTables["raw_chem_name"]!= "average"]
latTrueTables=latTrueTables.loc[latTrueTables["raw_chem_name"]!= "ranking"]
latTrueTables=latTrueTables.loc[latTrueTables["raw_chem_name"]!= "average ranking"]
latTrueTables=latTrueTables.loc[latTrueTables["raw_chem_name"]!= "chemical name as described in the inci list"]
latTrueTables=latTrueTables.reset_index()
latTrueTables=latTrueTables[["raw_chem_name","raw_cas"]]


latFalseTables["raw_chem_name"]=latFalseTables.iloc[:,0]
latFalseTables["raw_cas"]=latFalseTables.iloc[:,1]
latFalseTables["flag"]=latFalseTables.iloc[:,4]
latFalseTables=latFalseTables[["raw_chem_name","raw_cas","flag"]]
latFalseTables=latFalseTables.dropna(subset=["raw_chem_name","raw_cas"], how="all")
latFalseTables=latFalseTables.loc[latFalseTables["raw_chem_name"]!="INCI Name"]
latFalseTables=latFalseTables.reset_index()
latFalseTables=latFalseTables[["raw_chem_name","raw_cas","flag"]]

digits=["0","1","2","3","4","5","6","7","8","9","79-8","43-3"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0,len(latFalseTables)):
    latFalseTables["raw_chem_name"].iloc[j]=clean(str(latFalseTables["raw_chem_name"].iloc[j]))
    latFalseTables["raw_chem_name"].iloc[j]=str(latFalseTables["raw_chem_name"].iloc[j]).strip().lower()
    if str(latFalseTables["raw_cas"].iloc[j]).strip() in digits and latFalseTables["raw_chem_name"].iloc[j]=="nan": #deals with situation when chemical names on one line and with cas split on two lines
        latFalseTables["raw_chem_name"].iloc[j]=latFalseTables["raw_chem_name"].iloc[j-1]
        latFalseTables["raw_cas"].iloc[j]=latFalseTables["raw_cas"].iloc[j-1]+latFalseTables["raw_cas"].iloc[j]
        j_drop.append(j-1)

    elif str(latFalseTables["raw_cas"].iloc[j]).strip() in digits: #deals with situation when cas is split onto two lines but name isn't on one line. flag uses boolean flags to help with clean up later
        latFalseTables["raw_chem_name"].iloc[j]=latFalseTables["raw_chem_name"].iloc[j-1]+" "+latFalseTables["raw_chem_name"].iloc[j]
        latFalseTables["raw_cas"].iloc[j]=latFalseTables["raw_cas"].iloc[j-1]+latFalseTables["raw_cas"].iloc[j]
        j_drop.append(j-1)
        latFalseTables["flag"].iloc[j]=False

    if (str(latFalseTables["raw_cas"].iloc[j])=="nan" and str(latFalseTables["flag"].iloc[j])!="nan") and str(latFalseTables["flag"].iloc[j+1])!="nan":#Sets up flags for dealing with situation where there is no value for cas on pdf
        latFalseTables["flag"].iloc[j]=True
    elif str(latFalseTables["flag"].iloc[j])!="nan":
        latFalseTables["flag"].iloc[j]=False

latFalseTables=latFalseTables.drop(j_drop)
latFalseTables=latFalseTables.reset_index()
latFalseTables=latFalseTables[["raw_chem_name","raw_cas","flag"]]

k_drop=[]
for k in range(1,len(latFalseTables)):
    if latFalseTables["flag"].iloc[k-1]==False:
        if str(latFalseTables["flag"].iloc[k])=="nan" and str(latFalseTables["raw_cas"].iloc[k-1])=="nan":#Deals with situation for chemical names that are split into multiple lines but dont have a cas
            latFalseTables["raw_chem_name"].iloc[k]=latFalseTables["raw_chem_name"].iloc[k-1]+" "+latFalseTables["raw_chem_name"].iloc[k]
            latFalseTables["flag"].iloc[k]=True
            k_drop.append(k-1)

        elif (str(latFalseTables["flag"].iloc[k])=="nan" and str(latFalseTables["raw_cas"].iloc[k])!="nan") and str(latFalseTables["raw_cas"].iloc[k-1])!="nan":#Skips over complete single lines
            continue

        elif str(latFalseTables["flag"].iloc[k])=="nan" and str(latFalseTables["raw_cas"].iloc[k-1])!="nan":#Deals with situation where name is split up onto multiple lines and cas is on one line
            latFalseTables["raw_chem_name"].iloc[k]=latFalseTables["raw_chem_name"].iloc[k-1]+" "+latFalseTables["raw_chem_name"].iloc[k]
            latFalseTables["raw_cas"].iloc[k]=latFalseTables["raw_cas"].iloc[k-1]
            latFalseTables["flag"].iloc[k]=False
            k_drop.append(k-1)


latFalseTables["raw_chem_name"].iloc[147]=latFalseTables["raw_chem_name"].iloc[147]+latFalseTables["raw_chem_name"].iloc[148]#Faster to manually change than write another conditional to change flag value
k_drop.append(148)
latFalseTables=latFalseTables.drop(k_drop)
latFalseTables=latFalseTables.reset_index()
latFalseTables=latFalseTables[["raw_chem_name","raw_cas"]]

table_2_2=pd.concat([latTrueTables,latFalseTables], ignore_index=True)
table_2_2=table_2_2.sort_values("raw_chem_name")

table_2_2["data_document_id"]="1372992"
table_2_2["data_document_filename"]="DCPS_88_g.pdf"
table_2_2["doc_date"]="2007"
table_2_2["raw_category"]=""
table_2_2["cat_code"]=""
table_2_2["description_cpcat"]=""
table_2_2["cpcat_code"]=""
table_2_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_2.to_csv("dcps_88_table_2_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 3.1
table_3_1=read_pdf("document_1372993.pdf", pages="170-175", lattice=False, pandas_options={'header': None})
table_3_1["raw_chem_name"]=table_3_1.iloc[:,0]
table_3_1["raw_cas"]=table_3_1.iloc[:,1]
table_3_1["flag"]=table_3_1.iloc[:,4]
table_3_1=table_3_1[["raw_chem_name","raw_cas","flag"]]
table_3_1=table_3_1.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_3_1=table_3_1.loc[table_3_1["raw_chem_name"]!="INCI Name"]
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas","flag"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0,len(table_3_1)):
    table_3_1["raw_chem_name"].iloc[j]=clean(str(table_3_1["raw_chem_name"].iloc[j]))
    table_3_1["raw_chem_name"].iloc[j]=str(table_3_1["raw_chem_name"].iloc[j]).strip().lower()

    if table_3_1["raw_cas"].iloc[j]=="17372-87-1" or table_3_1["raw_cas"].iloc[j]=="12227-89-3":
        table_3_1["flag"].iloc[j]=True
    elif (str(table_3_1["raw_cas"].iloc[j])=="nan" and str(table_3_1["flag"].iloc[j])!="nan") and str(table_3_1["flag"].iloc[j+1])!="nan":
        table_3_1["flag"].iloc[j]=True
    elif str(table_3_1["flag"].iloc[j])!="nan":
        table_3_1["flag"].iloc[j]=False

    if table_3_1["flag"].iloc[j-1]==False and table_3_1["flag"].iloc[j]!=True:
        if str(table_3_1["raw_cas"].iloc[j])=="nan" and str(table_3_1["flag"].iloc[j]=="nan"):
            table_3_1["raw_chem_name"].iloc[j]=table_3_1["raw_chem_name"].iloc[j-1]+" "+table_3_1["raw_chem_name"].iloc[j]
            table_3_1["raw_cas"].iloc[j]=table_3_1["raw_cas"][j-1]
            table_3_1["flag"].iloc[j]=False
            j_drop.append(j-1)

table_3_1=table_3_1.drop(j_drop)
table_3_1=table_3_1.reset_index()
table_3_1=table_3_1[["raw_chem_name","raw_cas"]]

table_3_1["data_document_id"]="1372993"
table_3_1["data_document_filename"]="DCPS_88_h.pdf"
table_3_1["doc_date"]="2007"
table_3_1["raw_category"]=""
table_3_1["cat_code"]=""
table_3_1["description_cpcat"]=""
table_3_1["cpcat_code"]=""
table_3_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_1.to_csv("dcps_88_table_3_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#table 3.2
table_3_2=read_pdf("document_1372994.pdf", pages="176-179", lattice=False, pandas_options={'header': None})
table_3_2["raw_chem_name"]=table_3_2.iloc[:,0]
table_3_2["raw_cas"]=table_3_2.iloc[:,1]
table_3_2["flag"]=table_3_2.iloc[:,4]
table_3_2=table_3_2[["raw_chem_name","raw_cas","flag"]]
table_3_2=table_3_2.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_3_2=table_3_2.loc[table_3_2["raw_chem_name"]!="INCI Name"]
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas","flag"]]

digits=["0","1","2","3","4","5","6","7","8","9","79-8","43-3"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0,len(table_3_2)):
    table_3_2["raw_chem_name"].iloc[j]=clean(str(table_3_2["raw_chem_name"].iloc[j]))
    table_3_2["raw_chem_name"].iloc[j]=str(table_3_2["raw_chem_name"].iloc[j]).strip().lower()
    if str(table_3_2["raw_cas"].iloc[j]).strip() in digits and table_3_2["raw_chem_name"].iloc[j]=="nan": #deals with situation when chemical names on one line and with cas split on two lines
        table_3_2["raw_chem_name"].iloc[j]=table_3_2["raw_chem_name"].iloc[j-1]
        table_3_2["raw_cas"].iloc[j]=table_3_2["raw_cas"].iloc[j-1]+table_3_2["raw_cas"].iloc[j]
        j_drop.append(j-1)

    elif str(table_3_2["raw_cas"].iloc[j]).strip() in digits: #deals with situation when cas is split onto two lines but name isn't on one line. flag uses boolean flags to help with clean up later
        table_3_2["raw_chem_name"].iloc[j]=table_3_2["raw_chem_name"].iloc[j-1]+" "+table_3_2["raw_chem_name"].iloc[j]
        table_3_2["raw_cas"].iloc[j]=table_3_2["raw_cas"].iloc[j-1]+table_3_2["raw_cas"].iloc[j]
        j_drop.append(j-1)
        table_3_2["flag"].iloc[j]=False

    if (str(table_3_2["raw_cas"].iloc[j])=="nan" and str(table_3_2["flag"].iloc[j])!="nan") and str(table_3_2["flag"].iloc[j+1])!="nan":#Sets up flags for dealing with situation where there is no value for cas on pdf
        table_3_2["flag"].iloc[j]=True
    elif str(table_3_2["flag"].iloc[j])!="nan":
        table_3_2["flag"].iloc[j]=False


table_3_2=table_3_2.drop(j_drop)
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas","flag"]]

k_drop=[]
for k in range(1,len(table_3_2)):
    if table_3_2["flag"].iloc[k-1]==False:
        if str(table_3_2["flag"].iloc[k])=="nan" and str(table_3_2["raw_cas"].iloc[k-1])=="nan":#Deals with situation for chemical names that are split into multiple lines but dont have a cas
            table_3_2["raw_chem_name"].iloc[k]=table_3_2["raw_chem_name"].iloc[k-1]+" "+table_3_2["raw_chem_name"].iloc[k]
            table_3_2["flag"].iloc[k]=True
            k_drop.append(k-1)

        elif (str(table_3_2["flag"].iloc[k])=="nan" and str(table_3_2["raw_cas"].iloc[k])!="nan") and str(table_3_2["raw_cas"].iloc[k-1])!="nan":#Skips over complete single lines
            continue

        elif str(table_3_2["flag"].iloc[k])=="nan" and str(table_3_2["raw_cas"].iloc[k-1])!="nan":#Deals with situation where name is split up onto multiple lines and cas is on one line
            table_3_2["raw_chem_name"].iloc[k]=table_3_2["raw_chem_name"].iloc[k-1]+" "+table_3_2["raw_chem_name"].iloc[k]
            table_3_2["raw_cas"].iloc[k]=table_3_2["raw_cas"].iloc[k-1]
            table_3_2["flag"].iloc[k]=False
            k_drop.append(k-1)

    elif table_3_2["flag"].iloc[k-1]==True and str(table_3_2["flag"].iloc[k])=="nan":
            table_3_2["raw_chem_name"].iloc[k]=table_3_2["raw_chem_name"].iloc[k-1]+" "+table_3_2["raw_chem_name"].iloc[k]
            table_3_2["raw_cas"].iloc[k]=table_3_2["raw_cas"].iloc[k-1]
            table_3_2["flag"].iloc[k]=False
            k_drop.append(k-1)


table_3_2=table_3_2.drop(k_drop)
table_3_2=table_3_2.reset_index()
table_3_2=table_3_2[["raw_chem_name","raw_cas"]]

table_3_2["data_document_id"]="1372994"
table_3_2["data_document_filename"]="DCPS_88_i.pdf"
table_3_2["doc_date"]="2007"
table_3_2["raw_category"]=""
table_3_2["cat_code"]=""
table_3_2["description_cpcat"]=""
table_3_2["cpcat_code"]=""
table_3_2["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_2.to_csv("dcps_88_table_3_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 3.3
table_3_3=read_pdf("document_1372995.pdf", pages="180-189", lattice=False, pandas_options={'header': None})
table_3_3["raw_chem_name"]=table_3_3.iloc[:,0]
table_3_3["raw_cas"]=table_3_3.iloc[:,1]
table_3_3["flag"]=table_3_3.iloc[:,4]
table_3_3=table_3_3[["raw_chem_name","raw_cas","flag"]]
table_3_3=table_3_3.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_3_3=table_3_3.loc[table_3_3["raw_chem_name"]!="INCI Name"]
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas","flag"]]

digits=["0","1","2","3","4","5","6","7","8","9","79-8","43-3"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0,len(table_3_3)):
    table_3_3["raw_chem_name"].iloc[j]=clean(str(table_3_3["raw_chem_name"].iloc[j]))
    table_3_3["raw_chem_name"].iloc[j]=str(table_3_3["raw_chem_name"].iloc[j]).strip().lower()
    if str(table_3_3["raw_cas"].iloc[j]).strip() in digits and table_3_3["raw_chem_name"].iloc[j]=="nan": #deals with situation when chemical names on one line and with cas split on two lines
        table_3_3["raw_chem_name"].iloc[j]=table_3_3["raw_chem_name"].iloc[j-1]
        table_3_3["raw_cas"].iloc[j]=table_3_3["raw_cas"].iloc[j-1]+table_3_3["raw_cas"].iloc[j]
        j_drop.append(j-1)
        table_3_3["flag"].iloc[j]=True

    elif str(table_3_3["raw_cas"].iloc[j]).strip() in digits: #deals with situation when cas is split onto two lines but name isn't on one line. flag uses boolean flags to help with clean up later
        table_3_3["raw_chem_name"].iloc[j]=table_3_3["raw_chem_name"].iloc[j-1]+" "+table_3_3["raw_chem_name"].iloc[j]
        table_3_3["raw_cas"].iloc[j]=table_3_3["raw_cas"].iloc[j-1]+table_3_3["raw_cas"].iloc[j]
        j_drop.append(j-1)
        table_3_3["flag"].iloc[j]=False

    if (str(table_3_3["raw_cas"].iloc[j])=="nan" and str(table_3_3["flag"].iloc[j])!="nan") and str(table_3_3["flag"].iloc[j+1])!="nan":#Sets up flags for dealing with situation where there is no value for cas on pdf
        table_3_3["flag"].iloc[j]=True
    elif str(table_3_3["flag"].iloc[j])!="nan":
        table_3_3["flag"].iloc[j]=False


table_3_3=table_3_3.drop(j_drop)
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas","flag"]]

k_drop=[]
for k in range(1,len(table_3_3)):
    if table_3_3["flag"].iloc[k-1]==False:
        if str(table_3_3["flag"].iloc[k])=="nan" and str(table_3_3["raw_cas"].iloc[k-1])=="nan":#Deals with situation for chemical names that are split into multiple lines but dont have a cas
            table_3_3["raw_chem_name"].iloc[k]=table_3_3["raw_chem_name"].iloc[k-1]+" "+table_3_3["raw_chem_name"].iloc[k]
            table_3_3["flag"].iloc[k]=True
            k_drop.append(k-1)

        elif (str(table_3_3["flag"].iloc[k])=="nan" and str(table_3_3["raw_cas"].iloc[k])!="nan") and str(table_3_3["raw_cas"].iloc[k-1])!="nan":#Skips over complete single lines
            continue

        elif str(table_3_3["flag"].iloc[k])=="nan" and str(table_3_3["raw_cas"].iloc[k-1])!="nan":#Deals with situation where name is split up onto multiple lines and cas is on one line
            table_3_3["raw_chem_name"].iloc[k]=table_3_3["raw_chem_name"].iloc[k-1]+" "+table_3_3["raw_chem_name"].iloc[k]
            table_3_3["raw_cas"].iloc[k]=table_3_3["raw_cas"].iloc[k-1]
            table_3_3["flag"].iloc[k]=False
            k_drop.append(k-1)

    elif table_3_3["flag"].iloc[k-1]==True and str(table_3_3["flag"].iloc[k])=="nan":
            table_3_3["raw_chem_name"].iloc[k]=table_3_3["raw_chem_name"].iloc[k-1]+" "+table_3_3["raw_chem_name"].iloc[k]
            table_3_3["raw_cas"].iloc[k]=table_3_3["raw_cas"].iloc[k-1]
            table_3_3["flag"].iloc[k]=False
            k_drop.append(k-1)


table_3_3=table_3_3.drop(k_drop)
table_3_3=table_3_3.reset_index()
table_3_3=table_3_3[["raw_chem_name","raw_cas"]]

table_3_3["data_document_id"]="1372995"
table_3_3["data_document_filename"]="DCPS_88_j.pdf"
table_3_3["doc_date"]="2007"
table_3_3["raw_category"]=""
table_3_3["cat_code"]=""
table_3_3["description_cpcat"]=""
table_3_3["cpcat_code"]=""
table_3_3["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_3.to_csv("dcps_88_table_3_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



#table 3.4
table_3_4=read_pdf("document_1372996.pdf", pages="190-195", lattice=False, pandas_options={'header': None})
table_3_4["raw_chem_name"]=table_3_4.iloc[:,0]
table_3_4["raw_cas"]=table_3_4.iloc[:,1]
table_3_4["flag"]=table_3_4.iloc[:,4]
table_3_4=table_3_4[["raw_chem_name","raw_cas","flag"]]
table_3_4=table_3_4.dropna(subset=["raw_chem_name","raw_cas"], how="all")
table_3_4=table_3_4.loc[table_3_4["raw_chem_name"]!="INCI Name"]
table_3_4=table_3_4.reset_index()
table_3_4=table_3_4[["raw_chem_name","raw_cas","flag"]]

digits=["0","1","2","3","4","5","6","7","8","9","79-8","43-3"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0,len(table_3_4)):
    table_3_4["raw_chem_name"].iloc[j]=clean(str(table_3_4["raw_chem_name"].iloc[j]))
    table_3_4["raw_chem_name"].iloc[j]=str(table_3_4["raw_chem_name"].iloc[j]).strip().lower()
    if str(table_3_4["raw_cas"].iloc[j]).strip() in digits and table_3_4["raw_chem_name"].iloc[j]=="nan": #deals with situation when chemical names on one line and with cas split on two lines
        table_3_4["raw_chem_name"].iloc[j]=table_3_4["raw_chem_name"].iloc[j-1]
        table_3_4["raw_cas"].iloc[j]=table_3_4["raw_cas"].iloc[j-1]+table_3_4["raw_cas"].iloc[j]
        j_drop.append(j-1)
        table_3_4["flag"].iloc[j]=True

    elif str(table_3_4["raw_cas"].iloc[j]).strip() in digits: #deals with situation when cas is split onto two lines but name isn't on one line. flag uses boolean flags to help with clean up later
        table_3_4["raw_chem_name"].iloc[j]=table_3_4["raw_chem_name"].iloc[j-1]+" "+table_3_4["raw_chem_name"].iloc[j]
        table_3_4["raw_cas"].iloc[j]=table_3_4["raw_cas"].iloc[j-1]+table_3_4["raw_cas"].iloc[j]
        j_drop.append(j-1)
        table_3_4["flag"].iloc[j]=False

    if (str(table_3_4["raw_cas"].iloc[j])=="nan" and str(table_3_4["flag"].iloc[j])!="nan") and str(table_3_4["flag"].iloc[j+1])!="nan":#Sets up flags for dealing with situation where there is no value for cas on pdf
        table_3_4["flag"].iloc[j]=True
    elif str(table_3_4["flag"].iloc[j])!="nan":
        table_3_4["flag"].iloc[j]=False


table_3_4=table_3_4.drop(j_drop)
table_3_4=table_3_4.reset_index()
table_3_4=table_3_4[["raw_chem_name","raw_cas","flag"]]

k_drop=[]
for k in range(1,len(table_3_4)):
    if table_3_4["flag"].iloc[k-1]==False:
        if str(table_3_4["flag"].iloc[k])=="nan" and str(table_3_4["raw_cas"].iloc[k-1])=="nan":#Deals with situation for chemical names that are split into multiple lines but dont have a cas
            table_3_4["raw_chem_name"].iloc[k]=table_3_4["raw_chem_name"].iloc[k-1]+" "+table_3_4["raw_chem_name"].iloc[k]
            table_3_4["flag"].iloc[k]=True
            k_drop.append(k-1)

        elif (str(table_3_4["flag"].iloc[k])=="nan" and str(table_3_4["raw_cas"].iloc[k])!="nan") and str(table_3_4["raw_cas"].iloc[k-1])!="nan":#Skips over complete single lines
            continue

        elif str(table_3_4["flag"].iloc[k])=="nan" and str(table_3_4["raw_cas"].iloc[k-1])!="nan":#Deals with situation where name is split up onto multiple lines and cas is on one line
            table_3_4["raw_chem_name"].iloc[k]=table_3_4["raw_chem_name"].iloc[k-1]+" "+table_3_4["raw_chem_name"].iloc[k]
            table_3_4["raw_cas"].iloc[k]=table_3_4["raw_cas"].iloc[k-1]
            table_3_4["flag"].iloc[k]=False
            k_drop.append(k-1)

    elif table_3_4["flag"].iloc[k-1]==True and str(table_3_4["flag"].iloc[k])=="nan":
            table_3_4["raw_chem_name"].iloc[k]=table_3_4["raw_chem_name"].iloc[k-1]+" "+table_3_4["raw_chem_name"].iloc[k]
            table_3_4["raw_cas"].iloc[k]=table_3_4["raw_cas"].iloc[k-1]
            table_3_4["flag"].iloc[k]=False
            k_drop.append(k-1)


table_3_4=table_3_4.drop(k_drop)
table_3_4=table_3_4.reset_index()
table_3_4=table_3_4[["raw_chem_name","raw_cas"]]

table_3_4["data_document_id"]="1372996"
table_3_4["data_document_filename"]="DCPS_88_k.pdf"
table_3_4["doc_date"]="2007"
table_3_4["raw_category"]=""
table_3_4["cat_code"]=""
table_3_4["description_cpcat"]=""
table_3_4["cpcat_code"]=""
table_3_4["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_4.to_csv("dcps_88_table_3_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 3.5
table_3_5=read_pdf("document_1372997.pdf", pages="196-204", lattice=True, pandas_options={'header': None})
table_3_5["raw_chem_name"]=table_3_5.iloc[:,0]
table_3_5["raw_cas"]=table_3_5.iloc[:,1]
table_3_5=table_3_5[["raw_chem_name","raw_cas"]]
table_3_5=table_3_5.dropna(how="all")
table_3_5=table_3_5.loc[table_3_5["raw_chem_name"]!="INCI Name"]

table_3_5=table_3_5.reset_index()
table_3_5=table_3_5[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_5)):
    table_3_5["raw_chem_name"].iloc[j]=str(table_3_5["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha").replace("ω","omega").replace(".","")
    table_3_5["raw_chem_name"].iloc[j]=clean(str(table_3_5["raw_chem_name"].iloc[j]))
    if len(table_3_5["raw_chem_name"].iloc[j].split())>1:
        table_3_5["raw_chem_name"].iloc[j]=" ".join(table_3_5["raw_chem_name"].iloc[j].split())
    if len(str(table_3_5["raw_cas"].iloc[j]).split())>1:
        table_3_5["raw_cas"].iloc[j]="".join(str(table_3_5["raw_cas"].iloc[j]).split())

table_3_5=table_3_5.loc[table_3_5["raw_chem_name"]!="average ranking"]
table_3_5=table_3_5.loc[table_3_5["raw_chem_name"]!="average"]
table_3_5=table_3_5.loc[table_3_5["raw_chem_name"]!="ranking"]
table_3_5=table_3_5.reset_index()
table_3_5=table_3_5[["raw_chem_name","raw_cas"]]
table_3_5["raw_chem_name"].iloc[18]=table_3_5["raw_chem_name"].iloc[18]+" "+table_3_5["raw_chem_name"].iloc[19]
table_3_5=table_3_5.drop(19)
table_3_5=table_3_5.reset_index()
table_3_5=table_3_5[["raw_chem_name","raw_cas"]]


table_3_5["data_document_id"]="1372997"
table_3_5["data_document_filename"]="DCPS_88_l.pdf"
table_3_5["doc_date"]="2007"
table_3_5["raw_category"]=""
table_3_5["cat_code"]=""
table_3_5["description_cpcat"]=""
table_3_5["cpcat_code"]=""
table_3_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_5.to_csv("dcps_88_table_3_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#table 3.6
table_3_6=read_pdf("document_1372998.pdf", pages="205-210", lattice=True, pandas_options={'header': None})
table_3_6["raw_chem_name"]=table_3_6.iloc[:,0]
table_3_6["raw_cas"]=table_3_6.iloc[:,1]
table_3_6=table_3_6[["raw_chem_name","raw_cas"]]
table_3_6=table_3_6.dropna(how="all")
table_3_6=table_3_6.loc[table_3_6["raw_chem_name"]!="INCI Name"]

table_3_6=table_3_6.reset_index()
table_3_6=table_3_6[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_6)):
    table_3_6["raw_chem_name"].iloc[j]=str(table_3_6["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha").replace("ω","omega").replace(".","")
    table_3_6["raw_chem_name"].iloc[j]=clean(str(table_3_6["raw_chem_name"].iloc[j]))
    if len(table_3_6["raw_chem_name"].iloc[j].split())>1:
        table_3_6["raw_chem_name"].iloc[j]=" ".join(table_3_6["raw_chem_name"].iloc[j].split())
    if len(str(table_3_6["raw_cas"].iloc[j]).split())>1:
        table_3_6["raw_cas"].iloc[j]="".join(str(table_3_6["raw_cas"].iloc[j]).split())

table_3_6=table_3_6.loc[table_3_6["raw_chem_name"]!="average ranking"]
table_3_6=table_3_6.loc[table_3_6["raw_chem_name"]!="average"]
table_3_6=table_3_6.loc[table_3_6["raw_chem_name"]!="ranking"]
table_3_6=table_3_6.reset_index()
table_3_6=table_3_6[["raw_chem_name","raw_cas"]]


table_3_6["data_document_id"]="1372998"
table_3_6["data_document_filename"]="DCPS_88_m.pdf"
table_3_6["doc_date"]="2007"
table_3_6["raw_category"]=""
table_3_6["cat_code"]=""
table_3_6["description_cpcat"]=""
table_3_6["cpcat_code"]=""
table_3_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_6.to_csv("dcps_88_table_3_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#table 3.7
table_3_7=read_pdf("document_1372999.pdf", pages="211-215", lattice=True, pandas_options={'header': None})
table_3_7["raw_chem_name"]=table_3_7.iloc[:,0]
table_3_7["raw_cas"]=table_3_7.iloc[:,1]
table_3_7=table_3_7[["raw_chem_name","raw_cas"]]
table_3_7=table_3_7.dropna(how="all")
table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!="INCI Name"]

table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_7)):
    table_3_7["raw_chem_name"].iloc[j]=str(table_3_7["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha").replace("ω","omega").replace(".","")
    table_3_7["raw_chem_name"].iloc[j]=clean(str(table_3_7["raw_chem_name"].iloc[j]))
    if len(table_3_7["raw_chem_name"].iloc[j].split())>1:
        table_3_7["raw_chem_name"].iloc[j]=" ".join(table_3_7["raw_chem_name"].iloc[j].split())
    if len(str(table_3_7["raw_cas"].iloc[j]).split())>1:
        table_3_7["raw_cas"].iloc[j]="".join(str(table_3_7["raw_cas"].iloc[j]).split())

table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!="average ranking"]
table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!="average"]
table_3_7=table_3_7.loc[table_3_7["raw_chem_name"]!="ranking"]
table_3_7=table_3_7.reset_index()
table_3_7=table_3_7[["raw_chem_name","raw_cas"]]


table_3_7["data_document_id"]="1372999"
table_3_7["data_document_filename"]="DCPS_88_n.pdf"
table_3_7["doc_date"]="2007"
table_3_7["raw_category"]=""
table_3_7["cat_code"]=""
table_3_7["description_cpcat"]=""
table_3_7["cpcat_code"]=""
table_3_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_7.to_csv("dcps_88_table_3_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)

#table 4.1
table_4_1=read_pdf("document_1373000.pdf", pages="216-218", lattice=False, pandas_options={'header': None})
table_4_1["raw_chem_name"]=table_4_1.iloc[:,0]
table_4_1["raw_cas"]=table_4_1.iloc[:,1]
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]
table_4_1=table_4_1.dropna(how="all")
table_4_1=table_4_1.loc[table_4_1["raw_chem_name"]!="INCI Name"]
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_1)):
    table_4_1["raw_chem_name"].iloc[j]=str(table_4_1["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha").replace("ω","omega").replace(".","")
    table_4_1["raw_chem_name"].iloc[j]=clean(str(table_4_1["raw_chem_name"].iloc[j]))
    if len(table_4_1["raw_chem_name"].iloc[j].split())>1:
        table_4_1["raw_chem_name"].iloc[j]=" ".join(table_4_1["raw_chem_name"].iloc[j].split())

    if str(table_4_1["raw_cas"].iloc[j-1])=="nan":
        table_4_1["raw_chem_name"].iloc[j]=table_4_1["raw_chem_name"].iloc[j-1]+" "+table_4_1["raw_chem_name"].iloc[j]
        j_drop.append(j-1)

table_4_1=table_4_1.drop(j_drop)
table_4_1=table_4_1.reset_index()
table_4_1=table_4_1[["raw_chem_name","raw_cas"]]

table_4_1["data_document_id"]="1373000"
table_4_1["data_document_filename"]="DCPS_88_o.pdf"
table_4_1["doc_date"]="2007"
table_4_1["raw_category"]=""
table_4_1["cat_code"]=""
table_4_1["description_cpcat"]=""
table_4_1["cpcat_code"]=""
table_4_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_1.to_csv("dcps_88_table_4_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
