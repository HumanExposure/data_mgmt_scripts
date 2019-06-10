#lkoval
#6/10/19

from tabula import read_pdf
import pandas as pd
import string

#Table 6.15
table_6_15=read_pdf("document_1372478.pdf", pages="81", lattice=True, pandas_options={'header': None})
table_6_15["raw_chem_name"]=table_6_15.iloc[1:,0]
table_6_15=table_6_15.dropna(subset=["raw_chem_name"])
table_6_15=table_6_15.reset_index()
table_6_15=table_6_15[["raw_chem_name"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_15)):
    table_6_15["raw_chem_name"].iloc[j]=str(table_6_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    table_6_15["raw_chem_name"].iloc[j]=clean(str(table_6_15["raw_chem_name"].iloc[j]))
    if len(table_6_15["raw_chem_name"].iloc[j].split())>1:
        table_6_15["raw_chem_name"].iloc[j]=" ".join(table_6_15["raw_chem_name"].iloc[j].split())


table_6_15["data_document_id"]="1372478"
table_6_15["data_document_filename"]="dcps39_a.pdf"
table_6_15["doc_date"]="2004"
table_6_15["raw_category"]=""
table_6_15["cat_code"]=""
table_6_15["description_cpcat"]=""
table_6_15["cpcat_code"]=""
table_6_15["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_15.to_csv("dcps_39_table_6_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix A
appen_a=read_pdf("document_1372480.pdf", pages="97,98", lattice=True, pandas_options={'header': None})
appen_a["raw_chem_name"]=appen_a.iloc[:-2,1]
appen_a["raw_cas"]=appen_a.iloc[:-2,2]
appen_a=appen_a.loc[appen_a["raw_chem_name"]!="Component"]
appen_a=appen_a.loc[appen_a["raw_chem_name"]!="?"]
appen_a=appen_a.loc[appen_a["raw_chem_name"]!="-"]
appen_a=appen_a.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_a=appen_a.reset_index()
appen_a=appen_a[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_a)):
    appen_a["raw_chem_name"].iloc[j]=str(appen_a["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    appen_a["raw_chem_name"].iloc[j]=clean(str(appen_a["raw_chem_name"].iloc[j]))
    if len(appen_a["raw_chem_name"].iloc[j].split())>1:
        appen_a["raw_chem_name"].iloc[j]=" ".join(str(appen_a["raw_chem_name"].iloc[j]).split())
    if len(str(appen_a["raw_cas"].iloc[j]).split())>1:
        appen_a["raw_cas"].iloc[j]=" ".join(str(appen_a["raw_cas"].iloc[j]).split())

appen_a=appen_a.drop_duplicates()
appen_a=appen_a.reset_index()
appen_a=appen_a[["raw_chem_name","raw_cas"]]

appen_a["data_document_id"]="1372480"
appen_a["data_document_filename"]="dcps39_c.pdf"
appen_a["doc_date"]="2004"
appen_a["raw_category"]=""
appen_a["cat_code"]=""
appen_a["description_cpcat"]=""
appen_a["cpcat_code"]=""
appen_a["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_a.to_csv("dcps_39_appen_a.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix B
#Tabula does not recognize some rows including all of p.101 even when lattice is False. No error is thrown, just doesn't find rows so all missing rows are added to end.
appen_b=read_pdf("document_1372481.pdf", pages="99-100", lattice=False, pandas_options={'header': None})
appen_b["raw_chem_name"]=appen_b.iloc[:,0]
appen_b["raw_cas"]=appen_b.iloc[:,1]
appen_b=appen_b.loc[appen_b["raw_chem_name"]!="Component"]
appen_b=appen_b.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_b=appen_b.reset_index()
appen_b=appen_b[["raw_chem_name","raw_cas"]]

j_drop=[]
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_b)):
    appen_b["raw_chem_name"].iloc[j]=str(appen_b["raw_chem_name"].iloc[j]).strip().lower().replace(".","")
    appen_b["raw_chem_name"].iloc[j]=clean(str(appen_b["raw_chem_name"].iloc[j]))
    if appen_b["raw_chem_name"].iloc[j]=="nan":
        appen_b["raw_cas"].iloc[j]=appen_b["raw_cas"].iloc[j-1]+""+appen_b["raw_cas"].iloc[j]
        appen_b["raw_chem_name"].iloc[j]=appen_b["raw_chem_name"].iloc[j-1]
        j_drop.append(j-1)
    if appen_b["raw_chem_name"].iloc[j]=="toluidine)":
        appen_b["raw_cas"].iloc[j]=appen_b["raw_cas"].iloc[j-1]
        appen_b["raw_chem_name"].iloc[j]=appen_b["raw_chem_name"].iloc[j-1]+""+appen_b["raw_chem_name"].iloc[j]
        j_drop.append(j-1)

appen_b=appen_b.drop(j_drop)
appen_b=appen_b.reset_index()
appen_b=appen_b[["raw_chem_name","raw_cas"]]

missedChems=pd.DataFrame([["acenaphthylene","208-96-8"],
                          ["acetaldehyde","75-07-0"],
                          ["acetyl-4-hydroxy-6-methyl-2h-pyran-2-on","771-03-9"],
                          ["acrolein","107-02-8"],
                          ["d-allose (7283-09-2)","1000126-28-1"],
                          ["3-allyl-6-methoxyphenol","501-19-9"],
                          ["anthracene","120-12-7"],
                          ["azulene","275-51-4"],
                          ["3,7-dimethyl-1,6-octadien-3-ol","78-70-6"],
                          ["3,7-dimethyl-1,6-octadien-3-ol","10281-55-7"],
                          ["3,7-dimethyl-1,6-octadien-3-ol, acetate","115-95-7"],
                          ["3,7-dimethyl-2,6-octadien-1-ol (geraniol)","106-24-1"],
                          ["3,7-dimethyl-6-octenal (citronellal)","106-23-0"],
                          ["2,6-dimethyl-7-octen-2-ol","18479-58-8"],
                          ["3,7-dimethyl-6-octen-1-ol","117-61-9"],
                          ["nerylnitrile","1000108-90-5"],
                          ["octadecanoic acid","112-79-8"],
                          ["octahydro-dimethylazulene","3691-11-0"],
                          ["octahydro-methanoazulene","514-51-2"],
                          ["octahydro-trimethyl-methanoazulene","546-28-1"],
                          ["1,1-oxybis-2-propanol","110-98-5"],
                          ["patchouli alcohol","5986-55-0"],
                          ["phenanthrene","1517-22-2"],
                          ["phenol","108-95-2"],
                          ["phenylethylalcohol","60-12-8"],
                          ["phenylethyn","536-74-3"],
                          ["2-(phenylmethylen)-octanal","1014-86-0"],
                          ["2-propenoic acid,3-phenyl,methylester","103-26-4"],
                          ["santatol alpha (98718-53-7)","115-71-9"],
                          ["styrene","100-42-5"],
                          ["a-terpineol (p-menth-1-en-8-ol)","98-55-5"],
                          ["b-terpineol","1000150-76-1"],
                          ["tetradecanal","124-25-4"],
                          ["tetrahydro-trimethlnapthalene","475-03-6"],
                          ["thujopsene","470-40-6"],
                          ["toluene","108-88-3"],
                          ["tricyclonona-3,6-diene","6006-24-2"],
                          ["trihydroxyphenyl-2-pentanone","1000116-2"],
                          ["4-trimethyl-3-cyclohexen-1-methanol","80-26-2"],
                          ["triphenyl-1-pentanol","2294-95-3"],
                          ["undecene","821-95-4"],
                          ["vanillin","121-33-5"],
                          ["o,m,p-xylene","106-42-3"]], columns=["raw_chem_name","raw_cas"])

appen_b=appen_b.append(missedChems)

appen_b["data_document_id"]="1372481"
appen_b["data_document_filename"]="dcps39_d.pdf"
appen_b["doc_date"]="2004"
appen_b["raw_category"]=""
appen_b["cat_code"]=""
appen_b["description_cpcat"]=""
appen_b["cpcat_code"]=""
appen_b["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_b.to_csv("dcps_39_appen_b.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
