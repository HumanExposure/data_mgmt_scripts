#lkoval
#6-13-19

from tabula import read_pdf
import pandas as pd
import string

#Appendix 3-printer
appen_3_printer=read_pdf("document_1372414.pdf", pages="41", lattice=False, pandas_options={'header': None})
appen_3_printer["raw_chem_name"]=appen_3_printer.iloc[:,0]
appen_3_printer["raw_cas"]=appen_3_printer.iloc[:,1]
appen_3_printer=appen_3_printer.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_printer=appen_3_printer.loc[appen_3_printer["raw_chem_name"]!="Substance"]
appen_3_printer=appen_3_printer.loc[appen_3_printer["raw_cas"]!="CAS no."]
appen_3_printer=appen_3_printer.reset_index()
appen_3_printer=appen_3_printer[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_printer)):
    appen_3_printer["raw_chem_name"].iloc[j]=str(appen_3_printer["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_printer["raw_chem_name"].iloc[j]=clean(str(appen_3_printer["raw_chem_name"].iloc[j]))

appen_3_printer["data_document_id"]="1372414"
appen_3_printer["data_document_filename"]="dcps_66_a.pdf"
appen_3_printer["doc_date"]="2005"
appen_3_printer["raw_category"]=""
appen_3_printer["cat_code"]=""
appen_3_printer["description_cpcat"]=""
appen_3_printer["cpcat_code"]=""
appen_3_printer["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_printer.to_csv("dcps_66_appen_3_printer.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-oven
appen_3_oven=read_pdf("document_1372415.pdf", pages="42", lattice=False, pandas_options={'header': None})
appen_3_oven["raw_chem_name"]=appen_3_oven.iloc[:,0]
appen_3_oven["raw_cas"]=appen_3_oven.iloc[:,1]
appen_3_oven=appen_3_oven.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_oven=appen_3_oven.loc[appen_3_oven["raw_chem_name"]!="Substance"]
appen_3_oven=appen_3_oven.loc[appen_3_oven["raw_cas"]!="CAS no."]
appen_3_oven=appen_3_oven.reset_index()
appen_3_oven=appen_3_oven[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_oven)):
    appen_3_oven["raw_chem_name"].iloc[j]=str(appen_3_oven["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_oven["raw_chem_name"].iloc[j]=clean(str(appen_3_oven["raw_chem_name"].iloc[j]))

appen_3_oven["data_document_id"]="1372415"
appen_3_oven["data_document_filename"]="dcps_66_b.pdf"
appen_3_oven["doc_date"]="2005"
appen_3_oven["raw_category"]=""
appen_3_oven["cat_code"]=""
appen_3_oven["description_cpcat"]=""
appen_3_oven["cpcat_code"]=""
appen_3_oven["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_oven.to_csv("dcps_66_appen_3_oven.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-hd
appen_3_hd=read_pdf("document_1372416.pdf", pages="43", lattice=False, pandas_options={'header': None})
appen_3_hd["raw_chem_name"]=appen_3_hd.iloc[:,0]
appen_3_hd["raw_cas"]=appen_3_hd.iloc[:,1]
appen_3_hd=appen_3_hd.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_hd=appen_3_hd.loc[appen_3_hd["raw_chem_name"]!="Substance"]
appen_3_hd=appen_3_hd.loc[appen_3_hd["raw_cas"]!="CAS no."]
appen_3_hd=appen_3_hd.reset_index()
appen_3_hd=appen_3_hd[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_hd)):
    appen_3_hd["raw_chem_name"].iloc[j]=str(appen_3_hd["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_hd["raw_chem_name"].iloc[j]=clean(str(appen_3_hd["raw_chem_name"].iloc[j]))

appen_3_hd["data_document_id"]="1372416"
appen_3_hd["data_document_filename"]="dcps_66_c.pdf"
appen_3_hd["doc_date"]="2005"
appen_3_hd["raw_category"]=""
appen_3_hd["cat_code"]=""
appen_3_hd["description_cpcat"]=""
appen_3_hd["cpcat_code"]=""
appen_3_hd["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_hd.to_csv("dcps_66_appen_3_hd.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-iron
appen_3_iron=read_pdf("document_1372417.pdf", pages="44", lattice=False, pandas_options={'header': None})
appen_3_iron["raw_chem_name"]=appen_3_iron.iloc[:,0]
appen_3_iron["raw_cas"]=appen_3_iron.iloc[:,1]
appen_3_iron=appen_3_iron.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_iron=appen_3_iron.loc[appen_3_iron["raw_chem_name"]!="Substance"]
appen_3_iron=appen_3_iron.loc[appen_3_iron["raw_cas"]!="CAS no."]
appen_3_iron=appen_3_iron.reset_index()
appen_3_iron=appen_3_iron[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_iron)):
    appen_3_iron["raw_chem_name"].iloc[j]=str(appen_3_iron["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_iron["raw_chem_name"].iloc[j]=clean(str(appen_3_iron["raw_chem_name"].iloc[j]))

appen_3_iron["data_document_id"]="1372417"
appen_3_iron["data_document_filename"]="dcps_66_d.pdf"
appen_3_iron["doc_date"]="2005"
appen_3_iron["raw_category"]=""
appen_3_iron["cat_code"]=""
appen_3_iron["description_cpcat"]=""
appen_3_iron["cpcat_code"]=""
appen_3_iron["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_iron.to_csv("dcps_66_appen_3_iron.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-lamp
appen_3_lamp=read_pdf("document_1372418.pdf", pages="45", lattice=False, pandas_options={'header': None})
appen_3_lamp["raw_chem_name"]=appen_3_lamp.iloc[:,0]
appen_3_lamp["raw_cas"]=appen_3_lamp.iloc[:,1]
appen_3_lamp=appen_3_lamp.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_lamp=appen_3_lamp.loc[appen_3_lamp["raw_chem_name"]!="Substance"]
appen_3_lamp=appen_3_lamp.loc[appen_3_lamp["raw_cas"]!="CAS no."]
appen_3_lamp=appen_3_lamp.reset_index()
appen_3_lamp=appen_3_lamp[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_lamp)):
    appen_3_lamp["raw_chem_name"].iloc[j]=str(appen_3_lamp["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_lamp["raw_chem_name"].iloc[j]=clean(str(appen_3_lamp["raw_chem_name"].iloc[j]))

appen_3_lamp["data_document_id"]="1372418"
appen_3_lamp["data_document_filename"]="dcps_66_e.pdf"
appen_3_lamp["doc_date"]="2005"
appen_3_lamp["raw_category"]=""
appen_3_lamp["cat_code"]=""
appen_3_lamp["description_cpcat"]=""
appen_3_lamp["cpcat_code"]=""
appen_3_lamp["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_lamp.to_csv("dcps_66_appen_3_lamp.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-phone1
tables=read_pdf("document_1372419.pdf", pages="46", lattice=False, multiple_tables=True, pandas_options={'header': None})
appen_3_phone1=tables[0]
appen_3_phone1["raw_chem_name"]=appen_3_phone1.iloc[:,0]
appen_3_phone1["raw_cas"]=appen_3_phone1.iloc[:,1]
appen_3_phone1=appen_3_phone1.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_phone1=appen_3_phone1.loc[appen_3_phone1["raw_chem_name"]!="Substance"]
appen_3_phone1=appen_3_phone1.loc[appen_3_phone1["raw_cas"]!="CAS no."]
appen_3_phone1=appen_3_phone1.reset_index()
appen_3_phone1=appen_3_phone1[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_phone1)):
    appen_3_phone1["raw_chem_name"].iloc[j]=str(appen_3_phone1["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_phone1["raw_chem_name"].iloc[j]=clean(str(appen_3_phone1["raw_chem_name"].iloc[j]))

appen_3_phone1["data_document_id"]="1372419"
appen_3_phone1["data_document_filename"]="dcps_66_f.pdf"
appen_3_phone1["doc_date"]="2005"
appen_3_phone1["raw_category"]=""
appen_3_phone1["cat_code"]=""
appen_3_phone1["description_cpcat"]=""
appen_3_phone1["cpcat_code"]=""
appen_3_phone1["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_phone1.to_csv("dcps_66_appen_3_phone1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-phone2
tables=read_pdf("document_1372420.pdf", pages="46", lattice=False, multiple_tables=True, pandas_options={'header': None})
appen_3_phone2=tables[1]
appen_3_phone2["raw_chem_name"]=appen_3_phone2.iloc[:,0]
appen_3_phone2["raw_cas"]=appen_3_phone2.iloc[:,1]
appen_3_phone2=appen_3_phone2.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_phone2=appen_3_phone2.loc[appen_3_phone2["raw_chem_name"]!="Substance"]
appen_3_phone2=appen_3_phone2.loc[appen_3_phone2["raw_cas"]!="CAS no."]
appen_3_phone2=appen_3_phone2.reset_index()
appen_3_phone2=appen_3_phone2[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_phone2)):
    appen_3_phone2["raw_chem_name"].iloc[j]=str(appen_3_phone2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_phone2["raw_chem_name"].iloc[j]=clean(str(appen_3_phone2["raw_chem_name"].iloc[j]))

appen_3_phone2["data_document_id"]="1372420"
appen_3_phone2["data_document_filename"]="dcps_66_g.pdf"
appen_3_phone2["doc_date"]="2005"
appen_3_phone2["raw_category"]=""
appen_3_phone2["cat_code"]=""
appen_3_phone2["description_cpcat"]=""
appen_3_phone2["cpcat_code"]=""
appen_3_phone2["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_phone2.to_csv("dcps_66_appen_3_phone2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-pc
import re

appen_3_pc=read_pdf("document_1372421.pdf", pages="47", lattice=False, pandas_options={'header': None})
appen_3_pc["chem_cas"]=appen_3_pc.iloc[3:,0]
appen_3_pc=appen_3_pc.dropna(subset=["chem_cas"])
appen_3_pc=appen_3_pc.reset_index()
appen_3_pc=appen_3_pc[["chem_cas"]]
appen_3_pc["raw_chem_name"]=""
appen_3_pc["raw_cas"]=""

casPattern=re.compile("\d+-\d{2}-\d{1}")
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_pc)):
    appen_3_pc["chem_cas"].iloc[j]=str(appen_3_pc["chem_cas"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_pc["chem_cas"].iloc[j]=clean(str(appen_3_pc["chem_cas"].iloc[j]))
    for element in appen_3_pc["chem_cas"].iloc[j].split():
        if casPattern.match(element):
            appen_3_pc["raw_cas"].iloc[j]=element
            appen_3_pc["raw_chem_name"].iloc[j]=" ".join(appen_3_pc["chem_cas"].iloc[j].split()[:appen_3_pc["chem_cas"].iloc[j].split().index(element)])

        if appen_3_pc["raw_chem_name"].iloc[j]=="" and element=="-":
            appen_3_pc["raw_cas"].iloc[j]=element
            appen_3_pc["raw_chem_name"].iloc[j]=" ".join(appen_3_pc["chem_cas"].iloc[j].split()[:appen_3_pc["chem_cas"].iloc[j].split().index(element)])


appen_3_pc=appen_3_pc[["raw_chem_name","raw_cas"]]

appen_3_pc["data_document_id"]="1372421"
appen_3_pc["data_document_filename"]="dcps_66_h.pdf"
appen_3_pc["doc_date"]="2005"
appen_3_pc["raw_category"]=""
appen_3_pc["cat_code"]=""
appen_3_pc["description_cpcat"]=""
appen_3_pc["cpcat_code"]=""
appen_3_pc["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_pc.to_csv("dcps_66_appen_3_pc.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-tv
appen_3_tv=read_pdf("document_1372422.pdf", pages="48", lattice=False, pandas_options={'header': None})
appen_3_tv["raw_chem_name"]=appen_3_tv.iloc[:,0]
appen_3_tv["raw_cas"]=appen_3_tv.iloc[:,1]
appen_3_tv=appen_3_tv.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_tv=appen_3_tv.loc[appen_3_tv["raw_chem_name"]!="Substance"]
appen_3_tv=appen_3_tv.loc[appen_3_tv["raw_cas"]!="CAS no."]
appen_3_tv=appen_3_tv.reset_index()
appen_3_tv=appen_3_tv[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_tv)):
    appen_3_tv["raw_chem_name"].iloc[j]=str(appen_3_tv["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_tv["raw_chem_name"].iloc[j]=clean(str(appen_3_tv["raw_chem_name"].iloc[j]))

appen_3_tv["data_document_id"]="1372422"
appen_3_tv["data_document_filename"]="dcps_66_i.pdf"
appen_3_tv["doc_date"]="2005"
appen_3_tv["raw_category"]=""
appen_3_tv["cat_code"]=""
appen_3_tv["description_cpcat"]=""
appen_3_tv["cpcat_code"]=""
appen_3_tv["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_tv.to_csv("dcps_66_appen_3_tv.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-el
appen_3_el=read_pdf("document_1372423.pdf", pages="49", lattice=False, pandas_options={'header': None})
appen_3_el["raw_chem_name"]=appen_3_el.iloc[:,0]
appen_3_el["raw_cas"]=appen_3_el.iloc[:,1]
appen_3_el=appen_3_el.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_el=appen_3_el.loc[appen_3_el["raw_chem_name"]!="Substance"]
appen_3_el=appen_3_el.loc[appen_3_el["raw_cas"]!="CAS no."]
appen_3_el=appen_3_el.reset_index()
appen_3_el=appen_3_el[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_el)):
    appen_3_el["raw_chem_name"].iloc[j]=str(appen_3_el["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_el["raw_chem_name"].iloc[j]=clean(str(appen_3_el["raw_chem_name"].iloc[j]))

appen_3_el["data_document_id"]="1372423"
appen_3_el["data_document_filename"]="dcps_66_j.pdf"
appen_3_el["doc_date"]="2005"
appen_3_el["raw_category"]=""
appen_3_el["cat_code"]=""
appen_3_el["description_cpcat"]=""
appen_3_el["cpcat_code"]=""
appen_3_el["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_el.to_csv("dcps_66_appen_3_el.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-heater
import re

appen_3_heat=read_pdf("document_1372424.pdf", pages="50", lattice=False, pandas_options={'header': None})
appen_3_heat["chem_cas"]=appen_3_heat.iloc[3:,0]
appen_3_heat=appen_3_heat.dropna(subset=["chem_cas"])
appen_3_heat=appen_3_heat.reset_index()
appen_3_heat=appen_3_heat[["chem_cas"]]
appen_3_heat["raw_chem_name"]=""
appen_3_heat["raw_cas"]=""

casPattern=re.compile("\d+-\d{2}-\d{1}")
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_heat)):
    appen_3_heat["chem_cas"].iloc[j]=str(appen_3_heat["chem_cas"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_heat["chem_cas"].iloc[j]=clean(str(appen_3_heat["chem_cas"].iloc[j]))
    for element in appen_3_heat["chem_cas"].iloc[j].split():
        if casPattern.match(element):
            appen_3_heat["raw_cas"].iloc[j]=element
            appen_3_heat["raw_chem_name"].iloc[j]=" ".join(appen_3_heat["chem_cas"].iloc[j].split()[:appen_3_heat["chem_cas"].iloc[j].split().index(element)])

        if appen_3_heat["raw_chem_name"].iloc[j]=="" and element=="-":
            appen_3_heat["raw_cas"].iloc[j]=element
            appen_3_heat["raw_chem_name"].iloc[j]=" ".join(appen_3_heat["chem_cas"].iloc[j].split()[:appen_3_heat["chem_cas"].iloc[j].split().index(element)])


appen_3_heat=appen_3_heat[["raw_chem_name","raw_cas"]]

appen_3_heat["data_document_id"]="1372424"
appen_3_heat["data_document_filename"]="dcps_66_k.pdf"
appen_3_heat["doc_date"]="2005"
appen_3_heat["raw_category"]=""
appen_3_heat["cat_code"]=""
appen_3_heat["description_cpcat"]=""
appen_3_heat["cpcat_code"]=""
appen_3_heat["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_heat.to_csv("dcps_66_appen_3_heat.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#Appendix 3-batteries
appen_3_batteries=read_pdf("document_1372425.pdf", pages="51", lattice=False, pandas_options={'header': None})
appen_3_batteries["raw_chem_name"]=appen_3_batteries.iloc[:,0]
appen_3_batteries["raw_cas"]=appen_3_batteries.iloc[:,1]
appen_3_batteries=appen_3_batteries.dropna(subset=["raw_chem_name","raw_cas"], how="all")
appen_3_batteries=appen_3_batteries.loc[appen_3_batteries["raw_chem_name"]!="Substance"]
appen_3_batteries=appen_3_batteries.loc[appen_3_batteries["raw_cas"]!="CAS no."]
appen_3_batteries=appen_3_batteries.reset_index()
appen_3_batteries=appen_3_batteries[["raw_chem_name","raw_cas"]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appen_3_batteries)):
    appen_3_batteries["raw_chem_name"].iloc[j]=str(appen_3_batteries["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("*","")
    appen_3_batteries["raw_chem_name"].iloc[j]=clean(str(appen_3_batteries["raw_chem_name"].iloc[j]))

appen_3_batteries["data_document_id"]="1372425"
appen_3_batteries["data_document_filename"]="dcps_66_l.pdf"
appen_3_batteries["doc_date"]="2005"
appen_3_batteries["raw_category"]=""
appen_3_batteries["cat_code"]=""
appen_3_batteries["description_cpcat"]=""
appen_3_batteries["cpcat_code"]=""
appen_3_batteries["cpcat_sourcetype"]="ACToR Assays and Lists"

appen_3_batteries.to_csv("dcps_66_appen_3_batteries.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)
