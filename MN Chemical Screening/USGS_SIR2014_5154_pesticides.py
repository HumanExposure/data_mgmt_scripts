#lkoval
#12-4-19

import pandas as pd
import string
import os
from tabula import read_pdf

os.chdir("//home//lkoval//MN")
#reads in each page of the table as a separate df then selects the appropriate rows based on formatting which varied slightly between pages.
#once formatting is uniform all pages are concatenated into a single df.
table=read_pdf("Overview Pesticides Streams Rivers USA 1992-2011.pdf", pages="20-23", lattice=False, multiple_tables=True)
df=pd.DataFrame()
for page in table:
    if len(page.columns)==7:
        page=page.iloc[:,[0,1,2,5]]
        page.columns=["raw_chem_name","report_funcuse","raw_cas","early_detect"]
        page.raw_chem_name=page.raw_chem_name.str.lower()
        page.report_funcuse=page.report_funcuse.str.lower()
        page=page.loc[~((page.raw_chem_name.str.contains("pesticide compound|synonym")) & (pd.isnull(page.raw_chem_name)==False))]
    else:
        page=page.iloc[:,[0,2,3,6]]
        page.columns=["raw_chem_name","report_funcuse","raw_cas","early_detect"]
        page.raw_chem_name=page.raw_chem_name.str.lower()
        page.report_funcuse=page.report_funcuse.str.lower()
        page=page.dropna(subset=["raw_chem_name"])
    df=pd.concat([df,page], ignore_index=True)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

#creates df for all chemicals detected from 1992-2001
early_years=df[["raw_chem_name","raw_cas","report_funcuse","early_detect"]]
early_years=early_years.dropna(subset=["early_detect"])
early_years=early_years.reset_index()
early_years=early_years[["raw_chem_name","raw_cas","report_funcuse"]]
early_years.raw_chem_name=early_years.raw_chem_name.apply(clean)
early_years.raw_cas=early_years.raw_cas.apply(clean)

#creates df for all chemicals detected from 2002-2011. df required some cleanup due chemical names and functional uses being
#split onto multiuple lines
later_years=df[["raw_chem_name","raw_cas","report_funcuse"]]

drop=[]
for i in range(len(later_years)):
    if pd.isnull(later_years.raw_chem_name.iloc[i]):
        later_years.report_funcuse.iloc[i-1]=later_years.report_funcuse.iloc[i-1]+" "+later_years.report_funcuse.iloc[i]
        drop.append(i)
    if pd.isnull(later_years.report_funcuse.iloc[i]):
        if i-1 not in drop:
            later_years.raw_chem_name.iloc[i-1]=later_years.raw_chem_name.iloc[i-1]+" "+later_years.raw_chem_name.iloc[i]
        else:
            later_years.raw_chem_name.iloc[i-2]=later_years.raw_chem_name.iloc[i-2]+" "+later_years.raw_chem_name.iloc[i]
        drop.append(i)

later_years=later_years.drop(drop)
later_years=later_years.reset_index()
later_years=later_years[["raw_chem_name","raw_cas","report_funcuse"]]
later_years.raw_chem_name=later_years.raw_chem_name.apply(clean)
later_years.raw_cas=later_years.raw_cas.apply(clean)


#Fill in rest of template for both dfs and write to csv
early_years["data_document_id"]="1497392"
early_years["data_document_filename"]="Overview Pesticides Streams Rivers USA 1992-2011_a.pdf"
early_years["doc_date"]="2014"
early_years["raw_category"]=""
early_years["cat_code"]=""
early_years["description_cpcat"]=""
early_years["cpcat_code"]=""
early_years["cpcat_sourcetype"]=""

early_years=early_years[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]
early_years.to_csv("Overview_Pesticides_Streams_Rivers_USA_1992_2001.csv", index=False)


later_years["data_document_id"]="1497393"
later_years["data_document_filename"]="Overview Pesticides Streams Rivers USA 1992-2011_b.pdf"
later_years["doc_date"]="2014"
later_years["raw_category"]=""
later_years["cat_code"]=""
later_years["description_cpcat"]=""
later_years["cpcat_code"]=""
later_years["cpcat_sourcetype"]=""

later_years=later_years[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]
later_years.to_csv("Overview_Pesticides_Streams_Rivers_USA_2002_2011.csv", index=False)
