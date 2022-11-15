# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:51:52 2022

@author: CLUTZ01
"""


import os
import pandas as pd
import numpy as np
import string
import tabula
import glob

os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Desktop/Extraction Scripts/Pest Residue/doc_files')

#Subpart C
execpath = r"C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64\pdftotext.exe"
file = 'tolerances&exemptions for pesticide chemical residues in food_a.pdf'
cmd = " ".join([execpath, "-margint 30", "-marginb 30",
               "-layout", "-f 1", "-l 8", '"'+file+'"'])
os.system(cmd)  # Convert pdf to txt

ifile = open(file.replace('.pdf', '.txt'))
text = ifile.read()
table = text.split('Specific')[-1].split('Subpart D')[0]  # Get text in table 3

table = table.split('\n')  # split table into a list of rows

table_1 = pd.DataFrame(table, columns=['raw_chem_name'])

table_1.at[249,'raw_chem_name'] = str(table_1.loc[249, 'raw_chem_name']) + ' ' + table_1.loc[250, 'raw_chem_name']



table_1['raw_chem_name'] = table_1['raw_chem_name'].str[9:]
table_1['raw_chem_name'] = table_1['raw_chem_name'].str.strip().str.lower()
table_1['raw_chem_name'] = table_1['raw_chem_name'].str.split(';').str[0]

table_1.at[0, 'raw_chem_name'] = ''
table_1['raw_chem_name'].replace('', np.nan, inplace=True)
table_1.dropna(subset=['raw_chem_name'], inplace=True)

table_1 = table_1[table_1["raw_chem_name"].str.contains("reserved") == False]


table_1['raw_chem_name'] = table_1["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_1["raw_chem_name"]))


table_1["data_document_id"]="1646890"
table_1["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_a.pdf"
table_1["doc_date"]="1/30/2019"
table_1["raw_category"]=""
table_1["cat_code"]=""
table_1["raw_cas"]=""
table_1["report_funcuse"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"

table_1.to_csv("pest_residue_table_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)




#Subpart D

filed ='tolerances&exemptions for pesticide chemical residues in food_a.pdf'
cmd_d = " ".join([execpath,"-margint 30", "-marginb 30","-layout","-f 8", "-l 12",'"'+filed+'"'])
os.system(cmd_d) #Convert pdf to txt

ifile_d = open(filed.replace('.pdf','.txt'))
text_d = ifile_d.read()
table_d = text_d.split('Exemptions From Tolerances')[-1].split('Subpart E')[0] #Get text in table 3
table_d = table_d.split('\n')  # split table into a list of rows


table_d= pd.DataFrame(table_d, columns = ['raw_chem_name'])
table_d = table_d[table_d["raw_chem_name"].str.contains('§')]

table_d['raw_chem_name'] = table_d['raw_chem_name'].str[9:]
table_d['raw_chem_name'] = table_d['raw_chem_name'].str.strip().str.lower()
table_d['raw_chem_name'] = table_d['raw_chem_name'].str.split(';').str[0]

table_d.at[0, 'raw_chem_name'] = ''
table_d['raw_chem_name'].replace('', np.nan, inplace=True)
table_d.dropna(subset=['raw_chem_name'], inplace=True)

table_d = table_d.drop(index=[2,3,4,5,6,7,9,10,11])

table_d['raw_chem_name'] = table_d["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_d["raw_chem_name"]))


table_d["data_document_id"]="1646891"
table_d["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_b.pdf"
table_d["doc_date"]="1/30/2019"
table_d["raw_category"]=""
table_d["cat_code"]=""
table_d["raw_cas"]=""
table_d["report_funcuse"]=""
table_d["description_cpcat"]=""
table_d["cpcat_code"]=""
table_d["cpcat_sourcetype"]="ACToR Assays and Lists"

table_d.to_csv("pest_residue_table_d.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)






#pre and post harvest
tables2=tabula.read_pdf("tolerances&exemptions for pesticide chemical residues in food_c.pdf", pages="390-400", lattice=True, multiple_tables=True, pandas_options={'header': None})


table_2=pd.concat([tables2[0], tables2[1],tables2[2],tables2[3], tables2[4], tables2[5],tables2[6],tables2[7], tables2[8], tables2[9],tables2[10],tables2[11]], ignore_index=True)

table_2=table_2.iloc[:,[0,2]]
table_2.columns = ['chem_w_cas', 'report_funcuse']
table_2_split= table_2['chem_w_cas'].str.split("\(CAS", expand=True)



table_2_df = pd.concat([table_2,table_2_split], axis=1)
table_2_df = table_2_df.iloc[:, [2,3,1]]
table_2_df.columns = ['raw_chem_name','raw_cas', 'report_funcuse']

table_2_df=table_2_df.dropna(subset=["raw_chem_name"])



To_remove_lst = ["Reg.", "reg\.", "No\.", "no\.", "\)", "No", "Nos", ":", "\.", "s"]
table_2_df['raw_cas'] = table_2_df['raw_cas'].str.replace('|'.join(To_remove_lst), '')
table_2_df['raw_cas'] = table_2_df['raw_cas'].str.strip()




clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2_df)):
    table_2_df["raw_chem_name"].iloc[j]=str(table_2_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("ω","omega").replace("β","beta").replace("γ","gamma")
    table_2_df["raw_chem_name"].iloc[j]=clean(str(table_2_df["raw_chem_name"].iloc[j]))


table_2_df.raw_cas.fillna(value=np.nan, inplace=True)

table_2_df['raw_chem_name'] = table_2_df["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_2_df["raw_chem_name"]))
table_2_df['raw_cas'] = table_2_df["raw_cas"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_2_df["raw_cas"]))


table_2_df['report_funcuse'] = table_2_df['report_funcuse'].str.replace('Do.', '')

i = table_2_df[((table_2_df.raw_chem_name == 'inert ingredients'))].index
table_2_df = table_2_df.drop(i)



table_2_df["data_document_id"]="1646892"
table_2_df["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_c.pdf"
table_2_df["doc_date"]="1/30/2019"
table_2_df["raw_category"]=""
table_2_df["cat_code"]=""
table_2_df["description_cpcat"]=""
table_2_df["cpcat_code"]=""
table_2_df["cpcat_sourcetype"]="ACToR Assays and Lists"

table_2_df.to_csv("pest_residue_table_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)




#########pre harvest
tables3=tabula.read_pdf("tolerances&exemptions for pesticide chemical residues in food_c.pdf", pages="400-406", lattice=True, multiple_tables=True, pandas_options={'header': None})


table_3=pd.concat([tables3[1],tables3[2],tables3[3], tables3[4], tables3[5],tables3[6],tables3[7]], ignore_index=True)

table_3=table_3.iloc[:,[0,2]]
table_3.columns = ['chem_w_cas', 'report_funcuse']
table_3_split= table_3['chem_w_cas'].str.split("\(CAS", expand=True)



table_3_df = pd.concat([table_3,table_3_split], axis=1)
table_3_df = table_3_df.iloc[:, [2,3,1]]
table_3_df.columns = ['raw_chem_name','raw_cas', 'report_funcuse']

table_3_df=table_3_df.dropna(subset=["raw_chem_name"])



To_remove_lst_3 = ["Reg.", "reg\.", "No\.", "no\.", "\)", "No", "Nos", ":", "\.", "s"]
table_3_df['raw_cas'] = table_3_df['raw_cas'].str.replace('|'.join(To_remove_lst_3), '')
table_3_df['raw_cas'] = table_3_df['raw_cas'].str.strip()




clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3_df)):
    table_3_df["raw_chem_name"].iloc[j]=str(table_3_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("ω","omega").replace("β","beta").replace("γ","gamma")
    table_3_df["raw_chem_name"].iloc[j]=clean(str(table_3_df["raw_chem_name"].iloc[j]))


table_3_df.raw_cas.fillna(value=np.nan, inplace=True)

table_3_df['raw_chem_name'] = table_3_df["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_2_df["raw_chem_name"]))
table_3_df['raw_cas'] = table_3_df["raw_cas"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_2_df["raw_cas"]))

table_3_df['report_funcuse'] = table_3_df['report_funcuse'].str.replace('Do.', '')

i3 = table_3_df[((table_3_df.raw_chem_name == 'inert ingredients'))].index
table_3_df = table_3_df.drop(i3)



table_3_df["data_document_id"]="1646893"
table_3_df["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_d.pdf"
table_3_df["doc_date"]="1/30/2019"
table_3_df["raw_category"]=""
table_3_df["cat_code"]=""
table_3_df["description_cpcat"]=""
table_3_df["cpcat_code"]=""
table_3_df["cpcat_sourcetype"]="ACToR Assays and Lists"

table_3_df.to_csv("pest_residue_table_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


#####Inert ingredients applied to animals

tables4=tabula.read_pdf("tolerances&exemptions for pesticide chemical residues in food_c.pdf", pages="406-413", lattice=True, multiple_tables=True, pandas_options={'header': None})


table_4=pd.concat([tables4[1],tables4[2],tables4[3], tables4[4], tables4[5],tables4[6],tables4[7],tables4[8]], ignore_index=True)

table_4=table_4.iloc[:,[0,2]]
table_4.columns = ['chem_w_cas', 'report_funcuse']
table_4_split= table_4['chem_w_cas'].str.split("\(CAS", expand=True)



table_4_df = pd.concat([table_4,table_4_split], axis=1)
table_4_df = table_4_df.iloc[:, [2,3,1]]
table_4_df.columns = ['raw_chem_name','raw_cas', 'report_funcuse']

table_4_df=table_4_df.dropna(subset=["raw_chem_name"])



To_remove_lst_4 = ["Reg.", "reg\.", "No\.", "no\.", "\)", "No", "Nos", ":", "\.", "s"]
table_4_df['raw_cas'] = table_4_df['raw_cas'].str.replace('|'.join(To_remove_lst_4), '')
table_4_df['raw_cas'] = table_4_df['raw_cas'].str.strip()




clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4_df)):
    table_4_df["raw_chem_name"].iloc[j]=str(table_4_df["raw_chem_name"].iloc[j]).strip().lower().replace("α","alpha").replace("ω","omega").replace("β","beta").replace("γ","gamma")
    table_4_df["raw_chem_name"].iloc[j]=clean(str(table_4_df["raw_chem_name"].iloc[j]))



table_4_df.raw_cas.fillna(value=np.nan, inplace=True)
table_4_df['raw_chem_name'] = table_4_df["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_2_df["raw_chem_name"]))
table_4_df['raw_cas'] = table_4_df["raw_cas"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_2_df["raw_cas"]))


table_4_df['report_funcuse'] = table_4_df['report_funcuse'].str.replace('Do.', '')

i4 = table_4_df[((table_4_df.raw_chem_name == 'inert ingredients'))].index
table_4_df = table_4_df.drop(i4)



table_4_df["data_document_id"]="1646894"
table_4_df["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_e.pdf"
table_4_df["doc_date"]="1/30/2019"
table_4_df["raw_category"]=""
table_4_df["cat_code"]=""
table_4_df["description_cpcat"]=""
table_4_df["cpcat_code"]=""
table_4_df["cpcat_sourcetype"]="ACToR Assays and Lists"

table_4_df.to_csv("pest_residue_table_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



#####Tolerance Exemptions Food Contact surfaces


tables5=tabula.read_pdf("tolerances&exemptions for pesticide chemical residues in food_c.pdf", pages="413-423", lattice=True, multiple_tables=True, pandas_options={'header': None})
table_5_prelim=pd.concat([tables5[1],tables5[2],tables5[3], tables5[4], tables5[5],tables5[6],tables5[7],tables5[8],tables5[9],tables5[10],tables5[11],tables5[12],tables5[13]], ignore_index=True)
table_5_prelim=table_5_prelim.iloc[:,[0,1]]
table_5_prelim.columns = ['raw_chem_name', 'raw_cas']
table_5=table_5_prelim.drop_duplicates(['raw_chem_name'])
table_5=table_5.dropna(subset=["raw_chem_name"])

table_5=table_5[table_5["raw_chem_name"].str.contains("Pesticide Chemical")==False]







clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("ω","omega").replace("β","beta").replace("γ","gamma")
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))



table_5.raw_cas.fillna(value=np.nan, inplace=True)
table_5['raw_chem_name'] = table_5["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_5["raw_chem_name"]))
table_5['raw_cas'] = table_5["raw_cas"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_5["raw_cas"]))


To_remove_lst_5 = ["Reg.", "reg\.","CAS", "None","No\.", "no\.","\(" ,"\)", "No", "Nos", ":", "\.", "s"]
table_5['raw_cas'] = table_5['raw_cas'].str.replace('|'.join(To_remove_lst_5), '')
table_5['raw_cas'] = table_5['raw_cas'].str.strip()

table_5 = table_5.replace('None','', regex=True)
table_5 = table_5.replace('None','', regex=True)



table_5["data_document_id"]="1646895"
table_5["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_f.pdf"
table_5["doc_date"]="1/30/2019"
table_5["raw_category"]=""
table_5["cat_code"]=""
table_5["report_funcuse"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

table_5.to_csv("pest_residue_table_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


##Tolerance Exemptions for minimal risk active and inert ingredients


tables6=tabula.read_pdf("tolerances&exemptions for pesticide chemical residues in food_c.pdf", pages="424-425", lattice=True, multiple_tables=True, pandas_options={'header': None})


table_6=pd.concat([tables6[0],tables6[1]], ignore_index=True)

table_6.columns = ['raw_chem_name', 'raw_cas']


table_6_df=table_6.dropna(subset=['raw_chem_name'])



To_remove_lst_6 = ["None"]
table_6_df['raw_cas'] = table_6_df['raw_cas'].str.replace('|'.join(To_remove_lst_6), '')
table_6_df['raw_cas'] = table_6_df['raw_cas'].str.strip()





clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_df)):
    table_6_df["raw_chem_name"].iloc[j]=str(table_6_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("ω","omega").replace("β","beta").replace("γ","gamma")
    table_6_df["raw_chem_name"].iloc[j]=clean(str(table_6_df["raw_chem_name"].iloc[j]))



table_6_df.raw_cas.fillna(value=np.nan, inplace=True)

table_6_df['raw_chem_name'] = table_6_df["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_6_df["raw_chem_name"]))


i6 = table_6_df[((table_6_df.raw_chem_name == 'chemical'))].index
table_6_df = table_6_df.drop(i6)



table_6_df["data_document_id"]="1646896"
table_6_df["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_g.pdf"
table_6_df["doc_date"]="1/30/2019"
table_6_df["raw_category"]=""
table_6_df["report_funcuse"]=""
table_6_df["cat_code"]=""
table_6_df["description_cpcat"]=""
table_6_df["cpcat_code"]=""
table_6_df["cpcat_sourcetype"]="ACToR Assays and Lists"

table_6_df.to_csv("pest_residue_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)


##Polymers - exemptions from tolerance requirement

tables7=tabula.read_pdf("tolerances&exemptions for pesticide chemical residues in food_c.pdf", pages="426-437", lattice=True, multiple_tables=True, pandas_options={'header': None})


table_7=pd.concat([tables7[0],tables7[1],tables7[2],tables7[3], tables7[4],tables7[5],tables7[6],tables7[7],tables7[8], tables7[9], tables7[10], tables7[11]], ignore_index=True)
table_7=table_7.iloc[:,[0,1]]
table_7.columns = ['raw_chem_name', 'raw_cas']

table_7_df=table_7.dropna(subset=["raw_chem_name"])

table_7_df.loc[190, 'raw_cas']="52832-04-6" #misplaced cas number in third dummy column moved and column deleted

To_remove_lst_7 = ["CAS Reg. No.", "None", "CASRN"]
table_7_df['raw_cas'] = table_7_df['raw_cas'].str.replace('|'.join(To_remove_lst_7), '')
table_7_df['raw_cas'] = table_7_df['raw_cas'].str.strip()





clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7_df)):
    table_7_df["raw_chem_name"].iloc[j]=str(table_7_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace("ω","omega").replace("β","beta").replace("γ","gamma")
    table_7_df["raw_chem_name"].iloc[j]=clean(str(table_7_df["raw_chem_name"].iloc[j]))



table_7_df.raw_cas.fillna(value=np.nan, inplace=True)
table_7_df['raw_chem_name'] = table_7_df["raw_chem_name"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_7_df["raw_chem_name"]))
table_7_df['raw_cas'] = table_7_df["raw_cas"].apply(lambda x: str(x[0:96]) + "..." if len(str(x)) > 100 else x, list(table_7_df["raw_cas"]))

i7 = table_7_df[((table_7_df.raw_chem_name == 'CAS No.'))].index
table_7_df = table_7_df.drop(i7)



table_7_df["data_document_id"]="1646897"
table_7_df["data_document_filename"]="tolerances&exemptions for pesticide chemical residues in food_h.pdf"
table_7_df["doc_date"]="1/30/2019"
table_7_df["raw_category"]=""
table_7_df["report_funcuse"]=""
table_7_df["cat_code"]=""
table_7_df["description_cpcat"]=""
table_7_df["cpcat_code"]=""
table_7_df["cpcat_sourcetype"]="ACToR Assays and Lists"

table_7_df.to_csv("pest_residue_table_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype"], index=False)



###Joining files

path = os.getcwd()
files = os.path.join(path, "pest_residue_table_*.csv")

files = glob.glob(files)


# joining files with concat and read_csv
pest_residue_df = pd.concat(map(pd.read_csv, files), ignore_index=True)


pest_residue_df.to_csv("pest_residue_tables44.csv", index=False)




