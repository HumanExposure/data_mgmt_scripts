#lkoval
#5/22/19

from tabula import read_pdf
import pandas as pd
import string

#Table 5.6
tables=read_pdf("document_1372775.pdf", pages="36,37", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_6=pd.concat([tables[0],tables[1]], ignore_index=True)
table_5_6["raw_cas"]=table_5_6.iloc[:,2]
table_5_6["raw_chem_name"]=table_5_6.iloc[:,0]
table_5_6=table_5_6.loc[table_5_6["raw_cas"]!= "CAS No"]
table_5_6=table_5_6[["raw_chem_name","raw_cas"]]
table_5_6=table_5_6.dropna(how="all")
table_5_6=table_5_6.reset_index()
table_5_6=table_5_6[["raw_chem_name","raw_cas"]]

noCas=["parfum","coco-glucoside","aroma"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_6)):
    table_5_6["raw_chem_name"].iloc[j]=str(table_5_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_6["raw_chem_name"].iloc[j]=clean(str(table_5_6["raw_chem_name"].iloc[j]))
    if len(table_5_6["raw_chem_name"].iloc[j].split())>1:
        table_5_6["raw_chem_name"].iloc[j]=" ".join(table_5_6["raw_chem_name"].iloc[j].split())
    if len(str(table_5_6["raw_cas"].iloc[j]).split())>1:
        table_5_6["raw_cas"].iloc[j]="".join(str(table_5_6["raw_cas"].iloc[j]).split())

    if table_5_6["raw_chem_name"].iloc[j] not in noCas:
        if str(table_5_6["raw_cas"].iloc[j])=="nan":
            table_5_6["raw_chem_name"].iloc[j]=table_5_6["raw_chem_name"].iloc[j-1]+" "+table_5_6["raw_chem_name"].iloc[j]
            table_5_6["raw_cas"].iloc[j]=table_5_6["raw_cas"].iloc[j-1]
            j_drop.append(j-1)

table_5_6=table_5_6.drop(j_drop)
table_5_6=table_5_6.reset_index()
table_5_6=table_5_6[["raw_chem_name","raw_cas"]]

table_5_6["data_document_id"]="1372775"
table_5_6["data_document_filename"]="DCPS_111_a.pdf"
table_5_6["doc_date"]="2011"
table_5_6["raw_category"]=""
table_5_6["cat_code"]=""
table_5_6["description_cpcat"]=""
table_5_6["cpcat_code"]=""
table_5_6["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_6.to_csv("dcps_111_table_5_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.7
tables=read_pdf("document_1372776.pdf", pages="37,38", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_7=pd.concat([tables[1],tables[2]], ignore_index=True)
table_5_7["raw_cas"]=table_5_7.iloc[:,2]
table_5_7["raw_chem_name"]=table_5_7.iloc[:,0]
table_5_7=table_5_7.loc[table_5_7["raw_cas"]!= "CAS No"]
table_5_7=table_5_7[["raw_chem_name","raw_cas"]]
table_5_7=table_5_7.dropna(how="all")
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_7)):
    table_5_7["raw_chem_name"].iloc[j]=str(table_5_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_7["raw_chem_name"].iloc[j]=clean(str(table_5_7["raw_chem_name"].iloc[j]))
    if len(table_5_7["raw_chem_name"].iloc[j].split())>1:
        table_5_7["raw_chem_name"].iloc[j]=" ".join(table_5_7["raw_chem_name"].iloc[j].split())
    if len(str(table_5_7["raw_cas"].iloc[j]).split())>1:
        table_5_7["raw_cas"].iloc[j]="".join(str(table_5_7["raw_cas"].iloc[j]).split())

    if str(table_5_7["raw_cas"].iloc[j])=="nan" and table_5_7["raw_chem_name"].iloc[j]!= "aroma":
        table_5_7["raw_chem_name"].iloc[j+1]=table_5_7["raw_chem_name"].iloc[j]+" "+table_5_7["raw_chem_name"].iloc[j+1]
        table_5_7["raw_cas"].iloc[j]=table_5_7["raw_cas"].iloc[j-1]
        j_drop.append(j)

table_5_7=table_5_7.drop(j_drop)
table_5_7=table_5_7.reset_index()
table_5_7=table_5_7[["raw_chem_name","raw_cas"]]

table_5_7["data_document_id"]="1372776"
table_5_7["data_document_filename"]="DCPS_111_b.pdf"
table_5_7["doc_date"]="2011"
table_5_7["raw_category"]=""
table_5_7["cat_code"]=""
table_5_7["description_cpcat"]=""
table_5_7["cpcat_code"]=""
table_5_7["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_7.to_csv("dcps_111_table_5_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.8
tables=read_pdf("document_1372777.pdf", pages="38,39", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_8=pd.concat([tables[1],tables[2]], ignore_index=True)
table_5_8["raw_cas"]=table_5_8.iloc[:,2]
table_5_8["raw_chem_name"]=table_5_8.iloc[:,0]
table_5_8=table_5_8.loc[table_5_8["raw_cas"]!= "CAS No"]
table_5_8=table_5_8[["raw_chem_name","raw_cas"]]
table_5_8=table_5_8.dropna(how="all")
table_5_8=table_5_8.reset_index()
table_5_8=table_5_8[["raw_chem_name","raw_cas"]]

noCas=["parfum","coco-glucoside"]
j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_8)):
    table_5_8["raw_chem_name"].iloc[j]=str(table_5_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_8["raw_chem_name"].iloc[j]=clean(str(table_5_8["raw_chem_name"].iloc[j]))
    if len(table_5_8["raw_chem_name"].iloc[j].split())>1:
        table_5_8["raw_chem_name"].iloc[j]=" ".join(table_5_8["raw_chem_name"].iloc[j].split())
    if len(str(table_5_8["raw_cas"].iloc[j]).split())>1:
        table_5_8["raw_cas"].iloc[j]="".join(str(table_5_8["raw_cas"].iloc[j]).split())
    if table_5_8["raw_chem_name"].iloc[j] not in noCas:
        if str(table_5_8["raw_cas"].iloc[j])=="nan":
            table_5_8["raw_chem_name"].iloc[j+1]=table_5_8["raw_chem_name"].iloc[j]+" "+table_5_8["raw_chem_name"].iloc[j+1]
            table_5_8["raw_cas"].iloc[j]=table_5_8["raw_cas"].iloc[j-1]
            j_drop.append(j)

table_5_8=table_5_8.drop(j_drop)
table_5_8=table_5_8.reset_index()
table_5_8=table_5_8[["raw_chem_name","raw_cas"]]

table_5_8["data_document_id"]="1372777"
table_5_8["data_document_filename"]="DCPS_111_c.pdf"
table_5_8["doc_date"]="2011"
table_5_8["raw_category"]=""
table_5_8["cat_code"]=""
table_5_8["description_cpcat"]=""
table_5_8["cpcat_code"]=""
table_5_8["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_8.to_csv("dcps_111_table_5_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.9
table_5_9=read_pdf("document_1372778.pdf", pages="40", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_5_9["raw_cas"]=table_5_9.iloc[:,2]
table_5_9["raw_chem_name"]=table_5_9.iloc[:,0]
table_5_9=table_5_9.loc[table_5_9["raw_cas"]!= "CAS No"]
table_5_9=table_5_9[["raw_chem_name","raw_cas"]]
table_5_9=table_5_9.dropna(how="all")
table_5_9=table_5_9.reset_index()
table_5_9=table_5_9[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_9)):
    table_5_9["raw_chem_name"].iloc[j]=str(table_5_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_9["raw_chem_name"].iloc[j]=clean(str(table_5_9["raw_chem_name"].iloc[j]))
    if len(table_5_9["raw_chem_name"].iloc[j].split())>1:
        table_5_9["raw_chem_name"].iloc[j]=" ".join(table_5_9["raw_chem_name"].iloc[j].split())
    if len(str(table_5_9["raw_cas"].iloc[j]).split())>1:
        table_5_9["raw_cas"].iloc[j]="".join(str(table_5_9["raw_cas"].iloc[j]).split())

    if str(table_5_9["raw_cas"].iloc[j])=="nan":
        table_5_9["raw_chem_name"].iloc[j+1]=table_5_9["raw_chem_name"].iloc[j]+" "+table_5_9["raw_chem_name"].iloc[j+1]
        j_drop.append(j)

table_5_9=table_5_9.drop(j_drop)
table_5_9=table_5_9.reset_index()
table_5_9=table_5_9[["raw_chem_name","raw_cas"]]

table_5_9["data_document_id"]="1372778"
table_5_9["data_document_filename"]="DCPS_111_d.pdf"
table_5_9["doc_date"]="2011"
table_5_9["raw_category"]=""
table_5_9["cat_code"]=""
table_5_9["description_cpcat"]=""
table_5_9["cpcat_code"]=""
table_5_9["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_9.to_csv("dcps_111_table_5_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.10
table_5_10=read_pdf("document_1372779.pdf", pages="41,42", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_5_10["raw_cas"]=table_5_10.iloc[:,2]
table_5_10["raw_chem_name"]=table_5_10.iloc[:,0]
table_5_10=table_5_10.loc[table_5_10["raw_cas"]!= "CAS No"]
table_5_10=table_5_10[["raw_chem_name","raw_cas"]]
table_5_10=table_5_10.dropna(how="all")
table_5_10=table_5_10.reset_index()
table_5_10=table_5_10[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_10)):
    table_5_10["raw_chem_name"].iloc[j]=str(table_5_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_10["raw_chem_name"].iloc[j]=clean(str(table_5_10["raw_chem_name"].iloc[j]))
    if len(table_5_10["raw_chem_name"].iloc[j].split())>1:
        table_5_10["raw_chem_name"].iloc[j]=" ".join(table_5_10["raw_chem_name"].iloc[j].split())
    if len(str(table_5_10["raw_cas"].iloc[j]).split())>1:
        table_5_10["raw_cas"].iloc[j]="".join(str(table_5_10["raw_cas"].iloc[j]).split())

    if str(table_5_10["raw_cas"].iloc[j])=="nan":
        if table_5_10["raw_chem_name"].iloc[j]== "zolinone" or table_5_10["raw_chem_name"].iloc[j]== "hydroxymethylglycinate":
            table_5_10["raw_chem_name"].iloc[j-1]=table_5_10["raw_chem_name"].iloc[j-1]+" "+table_5_10["raw_chem_name"].iloc[j]
        else:
            table_5_10["raw_chem_name"].iloc[j+1]=table_5_10["raw_chem_name"].iloc[j]+" "+table_5_10["raw_chem_name"].iloc[j+1]
        j_drop.append(j)

table_5_10=table_5_10.drop(j_drop)
table_5_10=table_5_10.reset_index()
table_5_10=table_5_10[["raw_chem_name","raw_cas"]]

table_5_10["data_document_id"]="1372779"
table_5_10["data_document_filename"]="DCPS_111_e.pdf"
table_5_10["doc_date"]="2011"
table_5_10["raw_category"]=""
table_5_10["cat_code"]=""
table_5_10["description_cpcat"]=""
table_5_10["cpcat_code"]=""
table_5_10["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_10.to_csv("dcps_111_table_5_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 5.11
table_5_11=read_pdf("document_1372780.pdf", pages="43-45", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_5_11["raw_chem_name"]=table_5_11.iloc[:,0]
table_5_11=table_5_11.loc[table_5_11["raw_chem_name"]!= "INCI name"]
table_5_11=table_5_11[["raw_chem_name"]]
table_5_11=table_5_11.dropna()
table_5_11=table_5_11.reset_index()
table_5_11=table_5_11[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5_11)):
    table_5_11["raw_chem_name"].iloc[j]=str(table_5_11["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_5_11["raw_chem_name"].iloc[j]=clean(str(table_5_11["raw_chem_name"].iloc[j]))
    if len(table_5_11["raw_chem_name"].iloc[j].split())>1:
        table_5_11["raw_chem_name"].iloc[j]=" ".join(table_5_11["raw_chem_name"].iloc[j].split())

table_5_11["raw_chem_name"].iloc[58]=table_5_11["raw_chem_name"].iloc[58]+" "+table_5_11["raw_chem_name"].iloc[59]
table_5_11=table_5_11.drop(59)
table_5_11=table_5_11.reset_index()
table_5_11=table_5_11[["raw_chem_name"]]

table_5_11["data_document_id"]="1372780"
table_5_11["data_document_filename"]="DCPS_111_f.pdf"
table_5_11["doc_date"]="2011"
table_5_11["raw_category"]=""
table_5_11["cat_code"]=""
table_5_11["description_cpcat"]=""
table_5_11["cpcat_code"]=""
table_5_11["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5_11.to_csv("dcps_111_table_5_11.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Table 7.1
table_7_1=read_pdf("document_1372781.pdf", pages="59,60", lattice=True, multiple_tables=False, pandas_options={'header': None})
table_7_1["raw_chem_name"]=table_7_1.iloc[:,0]
table_7_1=table_7_1[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7_1)):
    table_7_1["raw_chem_name"].iloc[j]=str(table_7_1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","").replace("α","alpha").replace("β","beta")
    table_7_1["raw_chem_name"].iloc[j]=clean(str(table_7_1["raw_chem_name"].iloc[j]))
    if len(table_7_1["raw_chem_name"].iloc[j].split())>1:
        table_7_1["raw_chem_name"].iloc[j]=" ".join(table_7_1["raw_chem_name"].iloc[j].split())

table_7_1=table_7_1.drop_duplicates()
table_7_1=table_7_1.loc[table_7_1["raw_chem_name"]!= "essential oil or essential oil component"]
table_7_1=table_7_1.reset_index()
table_7_1=table_7_1[["raw_chem_name"]]

table_7_1["data_document_id"]="1372781"
table_7_1["data_document_filename"]="DCPS_111_g.pdf"
table_7_1["doc_date"]="2011"
table_7_1["raw_category"]=""
table_7_1["cat_code"]=""
table_7_1["description_cpcat"]=""
table_7_1["cpcat_code"]=""
table_7_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_7_1.to_csv("dcps_111_table_7_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
