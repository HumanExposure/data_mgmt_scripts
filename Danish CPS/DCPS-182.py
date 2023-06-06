# -*- coding: utf-8 -*-
"""
Created on Wed May 31 16:44:56 2023

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



# %% raw table ext with tabula
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\vocs_in_pu_foams_report.pdf'
raw_tables = read_pdf(file, pages = '26-90', lattice = True, pandas_options={'header': None})

raw_tables_2 = []
for r in raw_tables:
    r_test = r.dropna(how = 'all', axis = 1)
    r_test = r_test.dropna(how = 'all', axis = 0)
    if r_test.empty == True:
        continue
    else:
        raw_tables_2.append(r)
        
raw_tables = raw_tables_2

# %% Table 1

#extraction and clean up
table_1=raw_tables[0]
table_1 = table_1.dropna(subset=[1])
table_1 = table_1.iloc[1:,[0,1]]

table_1.columns = ['raw_chem_name', 'raw_cas']


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_1)):
    table_1["raw_chem_name"].iloc[j]=str(table_1["raw_chem_name"].iloc[j]).split('(')[0].strip().lower()
    table_1["raw_chem_name"].iloc[j]=clean(str(table_1["raw_chem_name"].iloc[j]))
    if len(table_1["raw_chem_name"].iloc[j].split())>1:
        table_1["raw_chem_name"].iloc[j]=" ".join(table_1["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_1["data_document_id"]="1669895"
table_1["data_document_filename"]="vocs_pu_foams_table_1.pdf"
table_1["doc_date"]="September 2020"
table_1["component"]=""
table_1["raw_category"]=""
table_1["report_funcuse"]=""
table_1["cat_code"]=""
table_1["description_cpcat"]=""
table_1["cpcat_code"]=""
table_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#download as csv
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_1.to_csv("vocs_pu_foams_1.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)





# %% TABLE 2

#Extraction and clean up 
table_2 = raw_tables[2]
table_2 = table_2.dropna(subset=[0])
table_2.reset_index(inplace = True, drop = True)
table_2 = table_2.iloc[1:,[0,1]]
table_2.columns = ['raw_chem_name', 'raw_cas']


table_2.fillna(method='ffill', inplace=True)
table_2 = table_2.groupby('raw_cas', as_index=False)['raw_chem_name'].apply(' '.join)
table_2 = table_2.iloc[:,[1,0]]



# clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_2)):
    table_2["raw_chem_name"].iloc[j]=str(table_2["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_2["raw_chem_name"].iloc[j]=clean(str(table_2["raw_chem_name"].iloc[j]))
    table_2["raw_cas"].iloc[j]=str(table_2["raw_cas"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_2["raw_cas"].iloc[j]=clean(str(table_2["raw_cas"].iloc[j]))
    
    if len(table_2["raw_chem_name"].iloc[j].split())>1:
        table_2["raw_chem_name"].iloc[j]=" ".join(table_2["raw_chem_name"].iloc[j].split())
        
        
# Repeating values declaration and csv creation
table_2["data_document_id"]="1669896"
table_2["data_document_filename"]="vocs_pu_foams_table_2.pdf"
table_2["doc_date"]="September 2020"
table_2["report_funcuse"]=""
table_2["raw_category"]=""
table_2["component"]=""
table_2["cat_code"]=""
table_2["description_cpcat"]=""
table_2["cpcat_code"]=""
table_2["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_2.to_csv("vocs_pu_foams_2.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% TABLE 3

#extraction and cleanup
table_3 = raw_tables[3]
table_3 = table_3.iloc[1:12,0]
table_3 = table_3.dropna()
table_3.reset_index(inplace = True, drop = True)
table_3 = pd.DataFrame({'raw_chem_name':table_3.values})

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_3)):
    table_3["raw_chem_name"].iloc[j]=str(table_3["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_3["raw_chem_name"].iloc[j]=clean(str(table_3["raw_chem_name"].iloc[j]))
    
    if len(table_3["raw_chem_name"].iloc[j].split())>1:
        table_3["raw_chem_name"].iloc[j]=" ".join(table_3["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_3["data_document_id"]="1669897"
table_3["data_document_filename"]="vocs_pu_foams_table_3.pdf"
table_3["doc_date"]="September 2020"
table_3["report_funcuse"]=""
table_3["raw_cas"]=""
table_3["raw_category"]=""
table_3["component"]=""
table_3["cat_code"]=""
table_3["description_cpcat"]=""
table_3["cpcat_code"]=""
table_3["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_3.to_csv("vocs_pu_foams_3.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)




# %% TABLE 4
table_4 = raw_tables[4]
table_4 = table_4.dropna(subset=[0])
table_4.reset_index(inplace = True, drop = True)
table_4 = table_4.iloc[1:,[0,1]]
table_4.columns = ['raw_chem_name', 'raw_cas']


table_4.fillna(method='ffill', inplace=True)
table_4 = table_4.groupby('raw_cas', as_index=False)['raw_chem_name'].apply(' '.join)
table_4 = table_4.iloc[:,[1,0]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))
    
    if len(table_4["raw_chem_name"].iloc[j].split())>1:
        table_4["raw_chem_name"].iloc[j]=" ".join(table_4["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_4["data_document_id"]="1669898"
table_4["data_document_filename"]="vocs_pu_foams_table_4.pdf"
table_4["doc_date"]="September 2020"
table_4["report_funcuse"]=""
table_4["raw_category"]=""
table_4["component"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_4.to_csv("vocs_pu_foams_4.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)




# %% TABLE 5
table_5 = raw_tables[5]
table_5 = table_5.dropna(subset=[0])
table_5.reset_index(inplace = True, drop = True)
table_5 = table_5.iloc[1:4,[0,1]]
table_5.columns = ['raw_chem_name', 'raw_cas']


table_5.fillna(method='ffill', inplace=True)
table_5 = table_5.groupby('raw_cas', as_index=False)['raw_chem_name'].apply(' '.join)
table_5 = table_5.iloc[:,[1,0]]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]=" ".join(table_5["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_5["data_document_id"]="1669899"
table_5["data_document_filename"]="vocs_pu_foams_table_5.pdf"
table_5["doc_date"]="September 2020"
table_5["report_funcuse"]=""
table_5["raw_category"]=""
table_5["component"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_5.to_csv("vocs_pu_foams_5.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 6
table_6 = raw_tables[6]
table_6 = table_6.iloc[1:,0]
table_6 = pd.DataFrame({'raw_chem_name':table_6.values})
table_6.reset_index(inplace = True, drop = True)

table_6['raw_chem_name'][3] = table_6['raw_chem_name'][3] + ' ' + table_6['raw_chem_name'][4]
table_6 = table_6.iloc[:4,0]
table_6 = pd.DataFrame({'raw_chem_name':table_6.values})
table_6_raw_chem_name = table_6['raw_chem_name'].tolist()

table_6_funcuse = ['foaming agents'] * len(table_6)
table_6 = pd.DataFrame({'raw_chem_name':table_6_raw_chem_name, 'report_funcuse':table_6_funcuse})


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_6["data_document_id"]="1669900"
table_6["data_document_filename"]="vocs_pu_foams_table_6.pdf"
table_6["doc_date"]="September 2020"
table_6["raw_cas"]=""
table_6["raw_category"]=""
table_6["component"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_6.to_csv("vocs_pu_foams_6.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 7 (still need to finish)

#extraction and clean up
table_7 = pd.concat([raw_tables[7], raw_tables[8]])
table_7 = table_7.iloc[2:,0:2]
table_7.reset_index(inplace = True, drop = True)
table_7.columns = ['raw_chem_name', 'raw_cas']


table_7_dummy = [''] * len(table_7)
table_7 = pd.DataFrame({'raw_chem_name':table_7['raw_chem_name'], 'raw_cas':table_7['raw_cas'], 'dummy_column':table_7_dummy})
table_7 = table_7.dropna(subset=['raw_chem_name', 'raw_cas'], how = 'all')
table_7.reset_index(inplace = True, drop = True)


i = 0
for j in range(0,len(table_7)):
    print('row ' + str(j))
    if str(table_7.iloc[j,0])[0].isupper() == True:
        table_7.iloc[j,2] = i
        i += 1
    else:
        continue
table_7 = table_7.fillna('nan')
for j in range(0,len(table_7)):
    print('row ' + str(j))
    if re.search(r'(\d+)-(\d\d)-(\d)',table_7.iloc[j,0]):
        table_7.iloc[j,1] = table_7.iloc[j,0]
        table_7.iloc[j,0] = 'nan'
    elif 'x' in str(table_7.iloc[j,1]):
        table_7.iloc[j,1] = 'nan'
    else:
        continue
# table_7 = table_7.replace('nan', np.NaN)
table_7 = table_7.replace('', np.NaN)

# table_7['dummy_column'] = table_7['dummy_column'].fillna(method='ffill', inplace=True)
table_7.fillna(method='ffill', inplace=True)
table_7 = table_7.replace('nan', '')
table_7 = table_7.groupby(['dummy_column', 'raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
table_7 = table_7.iloc[:,[2,1]]
table_7['raw_cas'] = table_7['raw_cas'].shift(-1)


table_7 = table_7[~table_7.iloc[:,0].str.contains("Substance name")]
table_7 = table_7.replace('', np.NaN)
table_7.dropna(how = 'all', inplace = True)

table_7 = table_7[table_7['raw_chem_name'].notna()]
table_7.iloc[1,0] = 'Chlorinated hydrocarbons (1,1,2,2-Tetrachloroethane, Pentachloroethane, 1,1,2-Trichloroethane, 1,1-Dichloroethylene)'
table_7.reset_index(inplace = True, drop = True)
table_7 = table_7.iloc[[0,1,3,4,5,6,7,8,9,10,11,12,13,14,15,16],:]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_7["raw_chem_name"].iloc[j]=clean(str(table_7["raw_chem_name"].iloc[j]))
    
    if len(table_7["raw_chem_name"].iloc[j].split())>1:
        table_7["raw_chem_name"].iloc[j]=" ".join(table_7["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_7["data_document_id"]="1669901"
table_7["data_document_filename"]="vocs_pu_foams_table_7.pdf"
table_7["doc_date"]="September 2020"
table_7["report_funcuse"]=""
table_7["raw_category"]=""
table_7["component"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_7.to_csv("vocs_pu_foams_7.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 8

# dataframe creation and cleaning
table_8 = raw_tables[9]
table_8_chem_names = table_8.iloc[:,0]
table_8 = table_8.apply(lambda x: pd.Series(x.dropna().values))
table_8_chem_names = table_8_chem_names.dropna().to_list()


for j in range(0,len(table_8_chem_names)):
    if str(table_8_chem_names[j])[0].isupper() == True or ():
        if ')' in table_8_chem_names[j] and '(' not in table_8_chem_names[j]:
            print(str(table_8_chem_names[j]) + ': no')
            table_8_chem_names[j-1] = table_8_chem_names[j-1]  + table_8_chem_names[j]
            table_8_chem_names[j] = np.nan
            continue
        else:
            print(str(table_8_chem_names[j]) + ': yes')

    
    else:
        print(str(table_8_chem_names[j]) + ': no')
        table_8_chem_names[j-1] = table_8_chem_names[j-1] + ' ' + table_8_chem_names[j]
        table_8_chem_names[j] = np.nan
        
table_8_chem_names = [x for x in table_8_chem_names if str(x) != 'nan']
table_8_chem_names = table_8_chem_names[1:7]

table_8_cas_nos = table_8.iloc[:,1]
table_8_cas_nos = table_8_cas_nos[1:7]
table_8_cas_nos[6] = ''


table_8 = pd.DataFrame({'raw_chem_name': table_8_chem_names, 'raw_cas': table_8_cas_nos})


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8)):
    table_8["raw_chem_name"].iloc[j]=str(table_8["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_8["raw_chem_name"].iloc[j]=clean(str(table_8["raw_chem_name"].iloc[j]))
    
    if len(table_8["raw_chem_name"].iloc[j].split())>1:
        table_8["raw_chem_name"].iloc[j]=" ".join(table_8["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_8["data_document_id"]="1669902"
table_8["data_document_filename"]="vocs_pu_foams_table_8.pdf"
table_8["doc_date"]="September 2020"
table_8["report_funcuse"]=""
table_8["raw_category"]=""
table_8["component"]=""
table_8["cat_code"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_8.to_csv("vocs_pu_foams_8.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% TABLE 9
table_9 = pd.concat([raw_tables[10], raw_tables[11], raw_tables[12]])
table_9 = table_9.iloc[2:,[0,1]]
table_9.reset_index(drop = True, inplace = True)
table_9.columns = ['raw_chem_name', 'raw_cas']

table_9 = table_9.fillna('nan')

for j in range(0,len(table_9)):
    if re.search(r'(\d+)-(\d\d)-(\d)', table_9['raw_cas'].iloc[j]) or 'nan' in table_9['raw_cas'].iloc[j] or 'above' in table_9['raw_cas'].iloc[j] or 'listed' in table_9['raw_cas'].iloc[j]:
        continue
    else:
        table_9['raw_cas'].iloc[j] = ''

for j in range(0,len(table_9)):    
    if 'STOT' in table_9['raw_chem_name'].iloc[j] or 'Substance' in table_9['raw_chem_name'].iloc[j]:
        table_9['raw_chem_name'].iloc[j] = ''
        
        
table_9 = table_9.replace('nan', np.NaN)
table_9 = table_9.replace('', np.NaN)
table_9 = table_9.dropna(how = 'all', axis = 0)         
table_9.fillna(method='ffill', inplace=True)
table_9 = table_9.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
table_9 = table_9.iloc[:,[1,0]]
table_9['raw_cas'].iloc[40] = 'all listed above'
table_9 = table_9.iloc[:41, :]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_9)):
    table_9["raw_chem_name"].iloc[j]=str(table_9["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-').replace('All listed,', 'All listed')
    table_9["raw_chem_name"].iloc[j]=clean(str(table_9["raw_chem_name"].iloc[j]))
    if len(table_9["raw_chem_name"].iloc[j].split())>1:
        table_9["raw_chem_name"].iloc[j]=" ".join(table_9["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_9["data_document_id"]="1669903"
table_9["data_document_filename"]="vocs_pu_foams_table_9.pdf"
table_9["doc_date"]="September 2020"
table_9["report_funcuse"]=""
table_9["raw_category"]=""
table_9["component"]=""
table_9["cat_code"]=""
table_9["description_cpcat"]=""
table_9["cpcat_code"]=""
table_9["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_9.to_csv("vocs_pu_foams_9.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% TABLE 10
# dataframe creation and cleaning
table_10 = raw_tables[13]
table_10 = table_10.iloc[:,0:3]
table_10 = table_10.dropna(how = 'all', axis = 0)
table_10.columns = ['raw_cas', 'ec_no', 'raw_chem_name']

mask = table_10[['ec_no', 'raw_chem_name']].isna().all(axis=1)
table_10.loc[mask, 'raw_cas':'raw_chem_name'] = table_10.loc[mask, 'raw_cas':'raw_chem_name'].shift(2, axis=1)
table_10.fillna(method='ffill', inplace=True)
table_10 = table_10.groupby(['ec_no','raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)


table_10 = table_10[~table_10.raw_chem_name.str.contains("name")]
table_10 = table_10.iloc[:,[1,2]]
table_10.reset_index(drop = True, inplace = True)
table_10 = table_10.loc[:3, ['raw_chem_name', 'raw_cas']]

table_10_funcuse = ['additives'] * len(table_10)
table_10 = pd.DataFrame({'raw_chem_name':table_10['raw_chem_name'], 'raw_cas':table_10['raw_cas'], 'report_funcuse':table_10_funcuse})



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_10)):
    table_10["raw_chem_name"].iloc[j]=str(table_10["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_10["raw_chem_name"].iloc[j]=clean(str(table_10["raw_chem_name"].iloc[j]))
    
    if len(table_10["raw_chem_name"].iloc[j].split())>1:
        table_10["raw_chem_name"].iloc[j]=" ".join(table_10["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_10["data_document_id"]="1669904"
table_10["data_document_filename"]="vocs_pu_foams_table_10.pdf"
table_10["doc_date"]="September"
table_10["raw_category"]=""
table_10["component"]=""
table_10["cat_code"]=""
table_10["description_cpcat"]=""
table_10["cpcat_code"]=""
table_10["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_10.to_csv("vocs_pu_foams_10.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% TABLE 12
# dataframe creation and cleaning

table_12 = pd.concat([raw_tables[16], raw_tables[17], raw_tables[18]])
table_12 = table_12.iloc[8:,0:2]
table_12 = table_12.dropna(how = 'all', axis = 0)
table_12.columns = ['raw_cas', 'raw_chem_name']
table_12 = table_12.fillna('nan')
table_12.reset_index(drop = True, inplace = True)

p = 0
for j in range(0, len(table_12)):
    if '-' in table_12['raw_cas'].iloc[j] and len(table_12['raw_cas'].iloc[j]) < 2 :
        table_12['raw_cas'].iloc[j] = '-: ' + str(p)
        p += 1
     
    
# Check if last character is 't'
    remove_last_char = ""    
    if table_12['raw_chem_name'].iloc[j].endswith('-'):
            print('yes')
            for i in range( len(table_12['raw_chem_name'].iloc[j])-1 ):
                remove_last_char += table_12['raw_chem_name'].iloc[j][i]
                
            table_12['raw_chem_name'].iloc[j] = remove_last_char

table_12 = table_12.replace('nan', np.NaN)


table_12.fillna(method='ffill', inplace=True)
table_12 = table_12.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)

for j in range(0, len(table_12)):
    if '-:' in str(table_12['raw_cas'].iloc[j]):
        table_12['raw_cas'].iloc[j] = '-'
table_12 = table_12.loc[:, ['raw_chem_name', 'raw_cas']]

table_12 = table_12[~table_12.raw_chem_name.str.contains("name")]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_12)):
    table_12["raw_chem_name"].iloc[j]=str(table_12["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_12["raw_chem_name"].iloc[j]=clean(str(table_12["raw_chem_name"].iloc[j]))
    
    if len(table_12["raw_chem_name"].iloc[j].split())>1:
        table_12["raw_chem_name"].iloc[j]=" ".join(table_12["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_12["data_document_id"]="1669905"
table_12["data_document_filename"]="vocs_pu_foams_table_12.pdf"
table_12["doc_date"]="September 2020"
table_12["report_funcuse"]=""
table_12["raw_category"]=""
table_12["component"]=""
table_12["cat_code"]=""
table_12["description_cpcat"]=""
table_12["cpcat_code"]=""
table_12["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_12.to_csv("vocs_pu_foams_12.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 13
# dataframe creation and cleaning
table_13 = raw_tables[19]
table_13 = table_13.iloc[6:,0:2]
table_13.reset_index(inplace = True, drop = True)
table_13.iloc[1,0] = ''
# table_13 = table_13.dropna(how = 'all', axis = 0)
table_13.columns = ['raw_cas', 'raw_chem_name']
table_13 = table_13.fillna('nan')
table_13.reset_index(drop = True, inplace = True)

table_13 = table_13.replace('nan', np.NaN)
table_13.fillna(method='ffill', inplace=True)
table_13 = table_13.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
table_13 = table_13.iloc[:,[1,0]]


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_13)):
    table_13["raw_chem_name"].iloc[j]=str(table_13["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_13["raw_chem_name"].iloc[j]=clean(str(table_13["raw_chem_name"].iloc[j]))
    
    if len(table_13["raw_chem_name"].iloc[j].split())>1:
        table_13["raw_chem_name"].iloc[j]=" ".join(table_13["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_13["data_document_id"]="1669906"
table_13["data_document_filename"]="vocs_pu_foams_table_13.pdf"
table_13["doc_date"]="September 2020"
table_13["report_funcuse"]=""
table_13["raw_category"]=""
table_13["component"]=""
table_13["cat_code"]=""
table_13["description_cpcat"]=""
table_13["cpcat_code"]=""
table_13["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_13.to_csv("vocs_pu_foams_13.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 15
# dataframe creation and cleaning
table_15 = raw_tables[22]
table_15 = table_15.iloc[8:17,0:2]
table_15 = table_15.dropna(how = 'all', axis = 0)
table_15.columns = ['raw_chem_name','raw_cas']
table_15.reset_index(drop = True, inplace = True)


table_15 = table_15.replace('nan', np.NaN)


table_15.fillna(method='ffill', inplace=True)
table_15 = table_15.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)

table_15 = table_15.loc[:, ['raw_chem_name', 'raw_cas']]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_15)):
    table_15["raw_chem_name"].iloc[j]=str(table_15["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_15["raw_chem_name"].iloc[j]=clean(str(table_15["raw_chem_name"].iloc[j]))
    
    if len(table_15["raw_chem_name"].iloc[j].split())>1:
        table_15["raw_chem_name"].iloc[j]=" ".join(table_15["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_15["data_document_id"]="1669907"
table_15["data_document_filename"]="vocs_pu_foams_table_15.pdf"
table_15["doc_date"]="September 2020"
table_15["report_funcuse"]=""
table_15["raw_category"]=""
table_15["component"]=""
table_15["cat_code"]=""
table_15["description_cpcat"]=""
table_15["cpcat_code"]=""
table_15["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_15.to_csv("vocs_pu_foams_15.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% TABLE 17 & 18
# dataframe creation and cleaning
table_17_18 = raw_tables[26]
table_17_18 = table_17_18.iloc[2:19,0:2]
table_17_18 = table_17_18.dropna(how = 'all', axis = 0)
table_17_18.columns = ['raw_chem_name','raw_cas']
table_17_18.reset_index(drop = True, inplace = True)


table_17_18.fillna(method='ffill', inplace=True)
table_17_18 = table_17_18.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)

table_17_18 = table_17_18.loc[:, ['raw_chem_name', 'raw_cas']]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_17_18)):
    table_17_18["raw_chem_name"].iloc[j]=str(table_17_18["raw_chem_name"].iloc[j]).lower().replace(".","").replace("*","").strip()
    table_17_18["raw_chem_name"].iloc[j]=clean(str(table_17_18["raw_chem_name"].iloc[j]))
    
    if len(table_17_18["raw_chem_name"].iloc[j].split())>1:
        table_17_18["raw_chem_name"].iloc[j]=" ".join(table_17_18["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_17_18["data_document_id"]="1669894"
table_17_18["data_document_filename"]="vocs_pu_foams_table_17&18.pdf"
table_17_18["doc_date"]="September 2020"
table_17_18["report_funcuse"]=""
table_17_18["raw_category"]=""
table_17_18["component"]=""
table_17_18["cat_code"]=""
table_17_18["description_cpcat"]=""
table_17_18["cpcat_code"]=""
table_17_18["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_17_18.to_csv("vocs_pu_foams_17_18.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 19
# dataframe creation and cleaning
table_19 = raw_tables[28]
table_19 = table_19.iloc[[2,3,5,6,7,8,9,10,11,12,13],0:2]
table_19 = table_19.dropna(how = 'all', axis = 0)
table_19.columns = ['raw_chem_name','raw_cas']
table_19.reset_index(drop = True, inplace = True)

table_19 = table_19.fillna('nan')


p = 0
for j in range(0, len(table_19)):
    if '-' in table_19['raw_cas'].iloc[j] and len(table_19['raw_cas'].iloc[j]) < 2 :
        table_19['raw_cas'].iloc[j] = '-: ' + str(p)
        p += 1

   
table_19 = table_19.replace('nan', np.NaN)


table_19.fillna(method='ffill', inplace=True)
table_19 = table_19.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(' '.join)

table_19 = table_19.loc[:, ['raw_chem_name', 'raw_cas']]


for j in range(0, len(table_19)):
    if '-:' in str(table_19['raw_cas'].iloc[j]):
        table_19['raw_cas'].iloc[j] = '-'
table_19 = table_19.loc[:, ['raw_chem_name', 'raw_cas']]




clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_19)):
    table_19["raw_chem_name"].iloc[j]=str(table_19["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_19["raw_chem_name"].iloc[j]=clean(str(table_19["raw_chem_name"].iloc[j]))
    
    if len(table_19["raw_chem_name"].iloc[j].split())>1:
        table_19["raw_chem_name"].iloc[j]=" ".join(table_19["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_19["data_document_id"]="1669908"
table_19["data_document_filename"]="vocs_pu_foams_table_19.pdf"
table_19["doc_date"]="September 2020"
table_19["raw_category"]=""
table_19["report_funcuse"]=""
table_19["component"]=""
table_19["cat_code"]=""
table_19["description_cpcat"]=""
table_19["cpcat_code"]=""
table_19["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_19.to_csv("vocs_pu_foams_19.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% TABLE 20 & 21
# dataframe creation and cleaning
table_20_21 = raw_tables[29]
table_20_21 = table_20_21.iloc[2:,0:2]
table_20_21.columns = ['raw_chem_name','raw_cas']
table_20_21.reset_index(drop = True, inplace = True)


table_20_21.fillna(method='ffill', inplace=True)
table_20_21 = table_20_21.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(' '.join)
table_20_21 = table_20_21.loc[:, ['raw_chem_name', 'raw_cas']]

table_20_21_funcuse = ['flame retardant'] * len(table_20_21)
table_20_21 = pd.DataFrame({'raw_chem_name':table_20_21['raw_chem_name'], 'raw_cas':table_20_21['raw_cas'], 'report_funcuse':table_20_21_funcuse})

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_20_21)):
    table_20_21["raw_chem_name"].iloc[j]=str(table_20_21["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('- ', '-')
    table_20_21["raw_chem_name"].iloc[j]=clean(str(table_20_21["raw_chem_name"].iloc[j]))
    
    if len(table_20_21["raw_chem_name"].iloc[j].split())>1:
        table_20_21["raw_chem_name"].iloc[j]=" ".join(table_20_21["raw_chem_name"].iloc[j].split())
#Repeating values declaration and csv creation

table_20_21["data_document_id"]="1669909"
table_20_21["data_document_filename"]="vocs_pu_foams_table_20&21.pdf"
table_20_21["doc_date"]="September 2020"
table_20_21["raw_category"]=""
table_20_21["component"]=""
table_20_21["cat_code"]=""
table_20_21["description_cpcat"]=""
table_20_21["cpcat_code"]=""
table_20_21["cpcat_sourcetype"]="ACToR Assays and Lists"

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
table_20_21.to_csv("vocs_pu_foams_20_21.csv", columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %% CONCAT ALL csv's TOGETHER
# %%% get files
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\PU Foam\csvs')
path = os.getcwd()
files = os.path.join(path, "vocs_pu_foams_*.csv")

files = glob.glob(files)


# %%% joining files with concat and read_csv
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv("vocs_pu_foams_ext.csv", index = False)

