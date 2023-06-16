# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:45:56 2023

@author: CLUTZ01
"""


# %% imports
from tabula import read_pdf
import pandas as pd
import string
import os
import glob
import re
import numpy as np



# %%% CleanLine Def
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('–','-').replace('≤','<=').replace('®', '').replace('â', '').replace('€“', '-')
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)


# %%% has numbers def

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)



# %% Table 6

file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\dcps_teeth_whitening_report.pdf'
raw_table_6 = read_pdf(file, pages = '28-53', stream = True, area=[[91,93,443,738]],pandas_options={'header': None})



############################################################
#######need to add in other data that was taken out#########
############################################################


#extraction and clean up
table_6=pd.concat([raw_table_6[0], raw_table_6[1], raw_table_6[2], raw_table_6[3], raw_table_6[4], raw_table_6[5], raw_table_6[6], raw_table_6[7]], ignore_index=True)


#shift over mis-extraction for records of last component
table_6.iloc[198, :] = table_6.iloc[198, :].shift()
table_6.iloc[199, :] = table_6.iloc[199, :].shift()
table_6.iloc[200, :] = table_6.iloc[200, :].shift()
table_6 = table_6.astype(str)

#create component labels [product type] [product no.]
table_6[1] = table_6[1] + ' ' + table_6[2]

#clean-up
table_6 = table_6.replace('nan', np.NaN)
table_6 = table_6.replace('nan nan', np.NaN)
table_6 = table_6.dropna(subset=[3])
table_6.reset_index(drop = True, inplace = True)

#removal of unusual formatted component
table_6_sc = table_6.iloc[21:30,[1,3]]

# %%
take_out = [21, 22, 23, 24, 25, 26, 27, 28, 29]
table_6 = table_6.drop(take_out,axis=0)


table_6 = table_6.iloc[:,[1,3]]
table_6.reset_index(drop = True, inplace = True)
table_6.columns = ['component', 'raw_chem_name']

    
table_6.fillna(method='ffill', inplace=True)
table_6 = table_6.groupby(['component'], as_index=False)['raw_chem_name'].apply(' '.join)
table_6 = table_6[table_6["raw_chem_name"].str.contains("eclaration") == False]



table_6 = table_6.iloc[:,[1,0]]
table_6.reset_index(drop = True, inplace = True)

#manual fix

table_6['component'].iloc[0] = table_6['component'].iloc[0].split('EU')[-1].strip() 

save = table_6
table_6 = save



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).replace('% ', '%, ').replace('- ', '').replace('. ', ', ').replace('-', '').replace(',,', ',').strip().lower()
    table_6["component"].iloc[j]=str(table_6["component"].iloc[j]).replace('.0', '').strip().lower()
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())
        
        

table_6 = (table_6.set_index(['component'])
   .apply(lambda x: x.str.split(', ').explode())
   .reset_index())

table_6['raw_chem_name'].iloc[114] = 'd. l-menthol 0.20%'
table_6['raw_chem_name'].iloc[115] = np.NaN
table_6 = table_6.dropna(subset=['raw_chem_name'])
table_6.reset_index(drop = True, inplace = True)
table_6 = table_6.iloc[:,[1,0]]


# %%
#add back in special cases

table_6_sc.fillna(method='ffill', inplace=True)
table_6_sc.reset_index(inplace = True, drop = True) 
table_6_sc[1] = table_6_sc[1] + ' ' + table_6_sc[3]

# table_6[['raw_chem_name', 'raw_cas']] = table_6['raw_chem_name'].str.rsplit(' ', 1, expand=True)
table_6_sc.columns = ['column a', 'column b']

for j in range(0, len(table_6_sc)):
    # j = 0
    if 'INGREDIENTS' in table_6_sc['column a'].iloc[j]:
        continue
    else:
        table_6_sc['column a'].iloc[j] = np.NaN
        
table_6_sc.fillna(method='ffill', inplace=True)

for j in range(0, len(table_6_sc)):
    # j = 0
    if '--------' in table_6_sc['column b'].iloc[j] or 'INGREDIENTS' in table_6_sc['column b'].iloc[j]:
        table_6_sc['column b'].iloc[j] = np.NaN
    else:
        continue
    
table_6_sc = table_6_sc.dropna(subset=['column b'])
table_6_sc.columns = ['component', 'raw_chem_name']
table_6_sc = table_6_sc.groupby(['component'], as_index=False)['raw_chem_name'].apply(' '.join)

# %%
table_6_sc = (table_6_sc.set_index(['component'])
   .apply(lambda x: x.str.split(', ').explode())
   .reset_index())
    
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6_sc)):
    table_6_sc["raw_chem_name"].iloc[j]=str(table_6_sc["raw_chem_name"].iloc[j]).replace('- ', '').strip().lower()
    table_6_sc["component"].iloc[j]=str(table_6_sc["component"].iloc[j]).replace(':', '').replace('.0', '').replace('- ', '').replace('INGREDIENTS', '').strip().lower()
    table_6_sc["raw_chem_name"].iloc[j]=clean(str(table_6_sc["raw_chem_name"].iloc[j]))
    if len(table_6_sc["raw_chem_name"].iloc[j].split())>1:
        table_6_sc["raw_chem_name"].iloc[j]=" ".join(table_6_sc["raw_chem_name"].iloc[j].split())
        
        
table_6_sc = table_6_sc.iloc[:,[1,0]]
table_6_sc.reset_index(inplace = True, drop = True)        
table_6_all = [table_6, table_6_sc]

table_6_all = pd.concat([table_6, table_6_sc])


#Repeating values declaration 
table_6["data_document_id"]="1670804"
table_6["data_document_filename"]="dcps_teeth_whitening_report_table_6.pdf"
table_6["doc_date"]="September 2021"
table_6["raw_cas"]=""
table_6["raw_category"]=""
table_6["report_funcuse"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\csvs')
table_6.to_csv("teeth_whitening_table_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)



# %% Table 10
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\dcps_teeth_whitening_report.pdf'
raw_table_10 = read_pdf(file, pages = '43', area=[[137,69,300,275]], stream = True,pandas_options={'header': None})

table_10 = raw_table_10[0]
table_10 = table_10.iloc[2:,:]

table_10.columns = ['raw_chem_name']


#extraction and clean up
table_10[['raw_chem_name', 'raw_cas']] = table_10['raw_chem_name'].str.rsplit(' ', 1, expand=True)


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_10)):
    table_10["raw_chem_name"].iloc[j]=str(table_10["raw_chem_name"].iloc[j]).strip().lower()
    table_10["raw_chem_name"].iloc[j]=clean(str(table_10["raw_chem_name"].iloc[j]))
    if len(table_10["raw_chem_name"].iloc[j].split())>1:
        table_10["raw_chem_name"].iloc[j]=" ".join(table_10["raw_chem_name"].iloc[j].split())
        


#Repeating values declaration 
table_10["data_document_id"]="1671696"
table_10["data_document_filename"]="dcps_teeth_whitening_report_table_10.pdf"
table_10["doc_date"]="September 2021"
table_10["component"]=""
table_10["raw_category"]=""
table_10["report_funcuse"]=""
table_10["cat_code"]=""
table_10["description_cpcat"]=""
table_10["cpcat_code"]=""
table_10["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\csvs')
table_10.to_csv("teeth_whitening_table_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% Table 12
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\dcps_teeth_whitening_report.pdf'
raw_table_12 = read_pdf(file, pages = '46', stream = True,pandas_options={'header': None}) #area=[[137,69,300,275]]

table_12 = raw_table_12[0]
# table_12 = table_12.iloc[2:,0]

table_12.columns = ['raw_chem_name', 'takeout1', 'takeout2', 'takeout3']


#extraction and clean up
table_12[['raw_chem_name', 'raw_cas']] = table_12['raw_chem_name'].str.rsplit(' ', 1, expand=True)
table_12 = table_12.iloc[2:,[0,4]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_12)):
    table_12["raw_chem_name"].iloc[j]=str(table_12["raw_chem_name"].iloc[j]).strip().lower()
    table_12["raw_chem_name"].iloc[j]=clean(str(table_12["raw_chem_name"].iloc[j]))
    if len(table_12["raw_chem_name"].iloc[j].split())>1:
        table_12["raw_chem_name"].iloc[j]=" ".join(table_12["raw_chem_name"].iloc[j].split())
        


#Repeating values declaration 
table_12["data_document_id"]="1671697"
table_12["data_document_filename"]="dcps_teeth_whitening_report_table_12.pdf"
table_12["doc_date"]="September 2021"
table_12["component"]=""
table_12["raw_category"]=""
table_12["report_funcuse"]=""
table_12["cat_code"]=""
table_12["description_cpcat"]=""
table_12["cpcat_code"]=""
table_12["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\csvs')
table_12.to_csv("teeth_whitening_table_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% Table 15
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\dcps_teeth_whitening_report.pdf'
raw_table_15 = read_pdf(file, pages = '53', stream = True,pandas_options={'header': None}) #area=[[137,69,300,275]]

table_15 = raw_table_15[0]
table_15 = table_15.replace('-', np.NaN)
# table_15 = table_15.iloc[2:,0]
table_15 = table_15.dropna(subset=[2])
table_15 = table_15.iloc[[0,2,3,4], 0:3 ]
table_15.reset_index(inplace = True, drop = True)

table_15[1] = table_15[0] + ' ' + table_15[1]
table_15 = table_15.iloc[:, 1:3 ]


table_15.columns = ['component', 'raw_chem_name']
table_15 = table_15.replace ('EU','', regex=True)
table_15 = table_15.replace ('Denmark','', regex=True)

# manual fixes
table_15['component'].iloc[0] = ''
table_15['raw_chem_name'].iloc[0] = 'boron'


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_15)):
    table_15["raw_chem_name"].iloc[j]=str(table_15["raw_chem_name"].iloc[j]).strip().lower()
    table_15["component"].iloc[j]=str(table_15["component"].iloc[j]).strip().lower()
    table_15["raw_chem_name"].iloc[j]=clean(str(table_15["raw_chem_name"].iloc[j]))
    if len(table_15["raw_chem_name"].iloc[j].split())>1:
        table_15["raw_chem_name"].iloc[j]=" ".join(table_15["raw_chem_name"].iloc[j].split())
        


#Repeating values declaration 
table_15["data_document_id"]="1671698"
table_15["data_document_filename"]="dcps_teeth_whitening_report_table_15.pdf"
table_15["doc_date"]="September 2021"
table_15["raw_cas"]=""
table_15["raw_category"]=""
table_15["report_funcuse"]=""
table_15["cat_code"]=""
table_15["description_cpcat"]=""
table_15["cpcat_code"]=""
table_15["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_ Teeth Whitening\csvs')
table_15.to_csv("teeth_whitening_table_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %%


# Joining files

path = os.getcwd()
files = os.path.join(path, "teeth_whitening_table_*.csv")

files = glob.glob(files)


# joining files with concat and read_csv
pest_residue_df = pd.concat(map(pd.read_csv, files), ignore_index=True)


pest_residue_df.to_csv("teeth_whitening_ext.csv", index=False)

