#lkoval
#4-23-20

import pandas as pd
import os
import string

os.chdir("C://Users//lkoval//OneDrive - Environmental Protection Agency (EPA)//Profile//Documents//FUse")

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #clean function to remove non-printable characters

flavis=pd.read_excel("flavis.xlsx", usecols=["Flavis name","CAS No"], dtype=str)
flavis=flavis.rename(columns={"Flavis name":"raw_chem_name","CAS No":"raw_cas"})
flavis=flavis.dropna(how="all").fillna("")

#some cas reading as dates with time stamp. Remove the time stamp
flavis.loc[flavis.raw_cas.str.contains("\d+-\d{2}-\d{1}"), ["raw_cas"]]=flavis.raw_cas.str.extract(r'(\d+-\d{2}-\d{1})', expand=False)
flavis.raw_chem_name=flavis.raw_chem_name.apply(clean)

flavis["data_document_id"]="1513117"
flavis["data_document_filename"]="flavis.pdf"
flavis["doc_date"]="2020"
flavis["raw_category"]=""
flavis["cat_code"]=""
flavis["description_cpcat"]=""
flavis["cpcat_sourcetype"]=""
flavis["report_funcuse"]="flavouring"
flavis["component"]=""

flavis=flavis[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_sourcetype","report_funcuse","component"]]

flavis.to_csv("flavis.csv", index=False)
