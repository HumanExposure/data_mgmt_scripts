# -*- coding: utf-8 -*-
"""
Created on Thursday Oct 12 16:26:29 2023

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

pd.options.mode.chained_assignment = None



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
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_DIY\DCPS_diy_survey_assessment_and_report.pdf"
diy_products_dfs = []


# %% Table 4
table_4_raw = read_pdf(file, pages = '21-23', stream = True, pandas_options={'header': None})
#extraction and clean up
table_4 = pd.concat([table_4_raw[0],table_4_raw[1], table_4_raw[2]])
table_4.reset_index(drop = True, inplace = True)

for i,j in enumerate(table_4[0]):
    if 'table 5' in str(j).lower():
        stop = i
        

table_4 = table_4.iloc[:stop,[0,1]]

table_4 = table_4.dropna(subset=[0])
table_4 = table_4[~table_4[0].str.contains('Substance')]


for i,j in enumerate(table_4[0]):
    if re.search(r'ID\s\d{1,2}', str(j)):
        table_4[1].iloc[i] = 'component'
table_4.columns = ['raw_chem_name', 'raw_cas']
table_4['order'] = np.NaN

for i,j in enumerate(table_4['raw_cas']):
    if 'nan' in str(j):
        table_4['order'].iloc[i] = i-1
    else:
        table_4['order'].iloc[i] = i
    




table_4['raw_cas'].fillna(method='ffill', inplace=True)
table_4 = table_4.groupby(['raw_cas', 'order'], as_index=False)['raw_chem_name'].apply(''.join)
table_4 = table_4.sort_values('order')
table_4.reset_index(inplace = True, drop = True)

table_4 = table_4.loc[:,['raw_chem_name', 'raw_cas']]




# %%% ID 4: 1C Paint – painting of ceiling and wall
table_4_id4 = table_4.iloc[1:12,:]
table_4_id4.reset_index(inplace = True, drop = True )

componentList = []
n = len(table_4_id4)
component = 'ID 4: 1C Paint – painting of ceiling and wall'
componentList.extend([component]*n)

table_4_id4=pd.DataFrame({'raw_chem_name':table_4_id4['raw_chem_name'], 'raw_cas':table_4_id4['raw_cas'], 'component':componentList}) 

# %%% ID 11: 1C Paint - painting of ceiling and wall
table_4_id11 = table_4.iloc[13:25,:]
table_4_id11.reset_index(inplace = True, drop = True)

table_4_id11['raw_cas'][11] = '64742-82-1/64742-48-9'

componentList = []
n = len(table_4_id11)
component = 'ID 11: 1C Paint - painting of ceiling and wall'
componentList.extend([component]*n)

table_4_id11=pd.DataFrame({'raw_chem_name':table_4_id11['raw_chem_name'], 'raw_cas':table_4_id11['raw_cas'], 'component':componentList}) 


# %%% ID 29: 1C Lacquer – lacquering of floors
table_4_id29 = table_4.iloc[26:35,:]
table_4_id29.reset_index(inplace = True, drop = True)

table_4_id29['raw_cas'][8] = '64742-82-1/64742-48-9'


componentList = []
n = len(table_4_id29)
component = 'ID 29: 1C Lacquer – lacquering of floors'
componentList.extend([component]*n)

table_4_id29=pd.DataFrame({'raw_chem_name':table_4_id29['raw_chem_name'], 'raw_cas':table_4_id29['raw_cas'], 'component':componentList}) 


# %%% ID 32: 1C Paint – painting of floors
table_4_id32 = table_4.iloc[36:,:]
table_4_id32.reset_index(inplace = True, drop = True)

table_4_id32['raw_chem_name'][12] = 'Naphtha C7-C13'
table_4_id32['raw_cas'][12] = '64742-82-1/64742-48-9'



componentList = []
n = len(table_4_id32)
component = 'ID 32: 1C Paint – painting of floors'
componentList.extend([component]*n)

table_4_id32=pd.DataFrame({'raw_chem_name':table_4_id32['raw_chem_name'], 'raw_cas':table_4_id32['raw_cas'], 'component':componentList}) 



# %%% merge back

df_list = [table_4_id4,table_4_id11,table_4_id29,table_4_id32]
table_4 = pd.concat(df_list)

# %%% cleaning
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_4)):
    table_4["raw_chem_name"].iloc[j]=str(table_4["raw_chem_name"].iloc[j]).replace('#','').replace('–', '-').strip().lower()
    table_4["raw_chem_name"].iloc[j]=clean(str(table_4["raw_chem_name"].iloc[j]))
    if len(table_4["raw_chem_name"].iloc[j].split())>1:
        table_4["raw_chem_name"].iloc[j]=" ".join(table_4["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_4["data_document_id"]="1679449"
table_4["data_document_filename"]="diy_projects_table_4.pdf"
table_4["doc_date"]="April 2020"
table_4["raw_category"]=""
table_4["report_funcuse"]=""
table_4["cat_code"]=""
table_4["description_cpcat"]=""
table_4["cpcat_code"]=""
table_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(table_4)

# %% Table 5
table_5_raw = read_pdf(file, pages = '23-24', stream = True, pandas_options={'header': None})
# %%% extraction and clean up
table_5 = pd.concat([table_5_raw[0],table_5_raw[1]])
table_5.reset_index(drop = True, inplace = True)

for i,j in enumerate(table_5[0]):
    if 'table 5' in str(j).lower():
        start = i
    elif 'table 6' in str(j).lower():
        stop = i

table_5 = table_5.iloc[start:stop,[0,2]]


table_5.columns = ['raw_chem_name', 'other']

table_5['raw_cas'] = np.NaN


for i,j in enumerate(table_5['raw_chem_name']):
    if re.search(r'ID\s\d{1,2}', str(j)):
        table_5['raw_cas'].iloc[i] = 'component'
        
    elif not re.search(r'[a-zA-Z]', str(j)):
        table_5['raw_cas'].iloc[i] = str(j)
        table_5['raw_chem_name'].iloc[i] = np.NaN
    elif re.search(r'\d+-\d\d-\d', str(j)):
        table_5['raw_cas'].iloc[i] = re.findall(r'\d+-\d\d-\d', str(j))[0]
        table_5['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-\d', '', str(j))
    elif re.search(r'\d+-\d\d-', str(j)):
        table_5['raw_cas'].iloc[i] = 'input manually'
        table_5['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-', '', str(j))

table_5 = table_5.dropna(subset=['raw_chem_name'])
table_5 = table_5[~table_5['raw_chem_name'].str.contains('Substance')]

table_5 = table_5.iloc[1:, [0,2]]

table_5['order'] = np.NaN
for i,j in enumerate(table_5['raw_cas']):
    if 'nan' in str(j):
        table_5['order'].iloc[i] = i-1

    else:
        table_5['order'].iloc[i] = i
        

table_5['raw_cas'].fillna(method='ffill', inplace=True)
table_5 = table_5.groupby(['raw_cas', 'order'], as_index=False)['raw_chem_name'].apply(''.join)
table_5 = table_5.sort_values('order')
table_5.reset_index(inplace = True, drop = True)

table_5 = table_5.loc[:,['raw_chem_name', 'raw_cas']]



# %%% ID 2: 2C Paint – painting of floors:
table_5_id2 = table_5.iloc[1:15,:]
table_5_id2.reset_index(inplace = True, drop = True )

table_5_id2['raw_cas'][13] = '64742-82-1/64742-48-9'

componentList = []
n = len(table_5_id2)
component = 'ID 2: 2C Paint – painting of floors'
componentList.extend([component]*n)

table_5_id2=pd.DataFrame({'raw_chem_name':table_5_id2['raw_chem_name'], 'raw_cas':table_5_id2['raw_cas'], 'component':componentList}) 

# %%% ID 5: 2C Paint – painting of floors:
table_5_id5 = table_5.iloc[16:29,:]
table_5_id5.reset_index(inplace = True, drop = True)


componentList = []
n = len(table_5_id5)
component = 'ID 5: 2C Paint – painting of floors'
componentList.extend([component]*n)

table_5_id5=pd.DataFrame({'raw_chem_name':table_5_id5['raw_chem_name'], 'raw_cas':table_5_id5['raw_cas'], 'component':componentList}) 


# %%% ID 20: 2C Paint – painting of floors
table_5_id20 = table_5.iloc[30:39,:]
table_5_id20.reset_index(inplace = True, drop = True)

table_5_id20['raw_cas'][8] = '64742-82-1/64742-48-9'


componentList = []
n = len(table_5_id20)
component = 'ID 20: 2C Paint – painting of floors'
componentList.extend([component]*n)

table_5_id20=pd.DataFrame({'raw_chem_name':table_5_id20['raw_chem_name'], 'raw_cas':table_5_id20['raw_cas'], 'component':componentList}) 


# %%% ID 30: 2C Paint - painting of floors:
table_5_id30 = table_5.iloc[40:,:]
table_5_id30.reset_index(inplace = True, drop = True)



componentList = []
n = len(table_5_id30)
component = 'ID 30: 2C Paint - painting of floors'
componentList.extend([component]*n)

table_5_id30=pd.DataFrame({'raw_chem_name':table_5_id30['raw_chem_name'], 'raw_cas':table_5_id30['raw_cas'], 'component':componentList}) 



# %%% merging separated dfs

df_list = [table_5_id2,table_5_id5,table_5_id20,table_5_id30]
table_5 = pd.concat(df_list)

# %%% cleaning 
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_5)):
    table_5["raw_chem_name"].iloc[j]=str(table_5["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    table_5["raw_chem_name"].iloc[j]=clean(str(table_5["raw_chem_name"].iloc[j]))
    if len(table_5["raw_chem_name"].iloc[j].split())>1:
        table_5["raw_chem_name"].iloc[j]=" ".join(table_5["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_5["data_document_id"]="1679450"
table_5["data_document_filename"]="diy_projects_table_5.pdf"
table_5["doc_date"]="April 2020"
table_5["raw_category"]=""
table_5["report_funcuse"]=""
table_5["cat_code"]=""
table_5["description_cpcat"]=""
table_5["cpcat_code"]=""
table_5["cpcat_sourcetype"]="ACToR Assays and Lists"


#add to list of dfs
diy_products_dfs.append(table_5)


# %% Table 6
table_6_raw = read_pdf(file, pages = '24-25', stream = True,area=[[10,10,800,5000]], pandas_options={'header': None})
# %%% extraction and clean up
table_6 = pd.concat([table_6_raw[0],table_6_raw[1]])
table_6.reset_index(drop = True, inplace = True)

for i,j in enumerate(table_6[0]):
    if 'table 6' in str(j).lower():
        start = i
    elif 'table 7' in str(j).lower():
        stop = i

table_6 = table_6.iloc[start:stop,[0,2]]


table_6.columns = ['raw_chem_name', 'other']

table_6['raw_cas'] = np.NaN


for i,j in enumerate(table_6['raw_chem_name']):
    if re.search(r'ID\s\d{1,2}', str(j)):
        table_6['raw_cas'].iloc[i] = 'component'
        
    elif not re.search(r'[a-zA-Z]', str(j)):
        table_6['raw_cas'].iloc[i] = str(j)
        table_6['raw_chem_name'].iloc[i] = np.NaN
    elif re.search(r'\d+-\d\d-\d', str(j)):
        table_6['raw_cas'].iloc[i] = re.findall(r'\d+-\d\d-\d', str(j))[0]
        table_6['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-\d', '', str(j))
    elif re.search(r'\d+-\d\d-', str(j)):
        table_6['raw_cas'].iloc[i] = 'input manually'
        table_6['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-', '', str(j))

table_6 = table_6.dropna(subset=['raw_chem_name'])
table_6 = table_6[~table_6['raw_chem_name'].str.contains('Substance')]
table_6 = table_6.dropna(subset=['raw_cas'])


table_6 = table_6.iloc[1:, [0,2]]


table_6 = table_6.loc[:,['raw_chem_name', 'raw_cas']]
table_6.reset_index(inplace = True, drop = True)




# %%% ID 14: 1C Filler –Wood surface repair & levelling
table_6_id14 = table_6.iloc[:9,:]
table_6_id14.reset_index(inplace = True, drop = True )

table_6_id14['raw_cas'][8] = '64742-82-1/64742-48-9'

componentList = []
n = len(table_6_id14)
component = 'ID 14: 1C Filler –Wood surface repair & levelling'
componentList.extend([component]*n)

table_6_id14=pd.DataFrame({'raw_chem_name':table_6_id14['raw_chem_name'], 'raw_cas':table_6_id14['raw_cas'], 'component':componentList}) 

# %%% ID 26: 2C Filler –Wood surface repair & levelling
table_6_id26 = table_6.iloc[10:20,:]
table_6_id26.reset_index(inplace = True, drop = True)

table_6_id26['raw_cas'][9] = '64742-82-1/64742-48-9'
table_6_id26['raw_chem_name'][9] = 'Naphtha C7-C13'

componentList = []
n = len(table_6_id26)
component = 'ID 26: 2C Filler –Wood surface repair & levelling'
componentList.extend([component]*n)

table_6_id26=pd.DataFrame({'raw_chem_name':table_6_id26['raw_chem_name'], 'raw_cas':table_6_id26['raw_cas'], 'component':componentList}) 


# %%% ID 36: 1C Filler –Wood surface repair & levelling
table_6_id36 = table_6.iloc[21:26,:]
table_6_id36.reset_index(inplace = True, drop = True)




componentList = []
n = len(table_6_id36)
component = 'ID 36: 1C Filler –Wood surface repair & levelling'
componentList.extend([component]*n)

table_6_id36=pd.DataFrame({'raw_chem_name':table_6_id36['raw_chem_name'], 'raw_cas':table_6_id36['raw_cas'], 'component':componentList}) 


# %%% ID 71: 1C Filler –Wood surface repair & levelling
table_6_id71 = table_6.iloc[27:33,:]
table_6_id71.reset_index(inplace = True, drop = True)

table_6_id71['raw_cas'][5] = '64742-82-1/64742-48-9'

componentList = []
n = len(table_6_id71)
component = 'ID 71: 1C Filler –Wood surface repair & levelling'
componentList.extend([component]*n)

table_6_id71=pd.DataFrame({'raw_chem_name':table_6_id71['raw_chem_name'], 'raw_cas':table_6_id71['raw_cas'], 'component':componentList}) 

# %%% ID 88: 2C Sealant – Repair of concrete
table_6_id88 = table_6.iloc[34:,:]
table_6_id88.reset_index(inplace = True, drop = True)



componentList = []
n = len(table_6_id88)
component = 'ID 88: 2C Sealant – Repair of concrete'
componentList.extend([component]*n)

table_6_id88=pd.DataFrame({'raw_chem_name':table_6_id88['raw_chem_name'], 'raw_cas':table_6_id88['raw_cas'], 'component':componentList}) 
# %%% merging separated dfs

df_list = [table_6_id14,table_6_id26,table_6_id36,table_6_id71,table_6_id88]
table_6 = pd.concat(df_list)

# %%% cleaning 
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_6)):
    table_6["raw_chem_name"].iloc[j]=str(table_6["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    table_6["raw_chem_name"].iloc[j]=clean(str(table_6["raw_chem_name"].iloc[j]))
    if len(table_6["raw_chem_name"].iloc[j].split())>1:
        table_6["raw_chem_name"].iloc[j]=" ".join(table_6["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_6["data_document_id"]="1679451"
table_6["data_document_filename"]="diy_projects_table_6.pdf"
table_6["doc_date"]="April 2020"
table_6["raw_category"]=""
table_6["report_funcuse"]=""
table_6["cat_code"]=""
table_6["description_cpcat"]=""
table_6["cpcat_code"]=""
table_6["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(table_6)


# %% Table 7
table_7_raw = read_pdf(file, pages = '25-26', stream = True, pandas_options={'header': None})
# %%% extraction and clean up
table_7 = pd.concat([table_7_raw[0],table_7_raw[1]])
table_7.reset_index(drop = True, inplace = True)

for i,j in enumerate(table_7[0]):
    if 'table 7' in str(j).lower():
        start = i
    

table_7 = table_7.iloc[start:,[0,1]]


table_7.columns = ['raw_chem_name', 'raw_cas']


for i,j in enumerate(table_7['raw_chem_name']):
    
    if re.search(r'ID\s\d{1,2}', str(j)):
        match = re.findall(r'ID\s\d{1,2}', str(j))[0]
        table_7['raw_cas'].iloc[i] = 'component ' + str(match)
        
    elif not re.search(r'[a-zA-Z]', str(j)):
        table_7['raw_cas'].iloc[i] = str(j)
        table_7['raw_chem_name'].iloc[i] = np.NaN
    elif re.search(r'\d+-\d\d-\d', str(j)):
        table_7['raw_cas'].iloc[i] = re.findall(r'\d+-\d\d-\d', str(j))[0]
        table_7['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-\d', '', str(j))
    elif re.search(r'\d+-\d\d-', str(j)):
        table_7['raw_cas'].iloc[i] = 'input manually'
        table_7['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-', '', str(j))



table_7.reset_index(drop = True, inplace = True)
table_7 = table_7.iloc[3:,:]
table_7 = table_7.dropna(axis = 0, how = 'all')

table_7['raw_cas'] = table_7['raw_cas'].replace(np.NaN, 'nan')





table_7['order'] = np.NaN
for i,j in enumerate(table_7['raw_chem_name']):
    if 'nan' in str(j):
        table_7['order'].iloc[i] = i-1

    else:
        table_7['order'].iloc[i] = i
        
table_7.fillna(method='ffill', inplace=True)
table_7 = table_7.groupby(['raw_chem_name', 'order'], as_index=False)['raw_cas'].apply(''.join)
table_7 = table_7.sort_values('order')
table_7.reset_index(inplace = True, drop = True)

table_7 = table_7.loc[:,['raw_chem_name', 'raw_cas']]
table_7['raw_cas'] = table_7['raw_cas'].replace('nan',np.NaN)


table_7['order'] = np.NaN

for i,j in enumerate(table_7['raw_cas']):
    if 'nan' in str(j):
        table_7['order'].iloc[i] = i-1
    else:
        table_7['order'].iloc[i] = i
    




table_7['raw_cas'].fillna(method='ffill', inplace=True)
table_7 = table_7.groupby(['raw_cas', 'order'], as_index=False)['raw_chem_name'].apply(''.join)
table_7 = table_7.sort_values('order')
table_7.reset_index(inplace = True, drop = True)

table_7 = table_7.loc[:,['raw_chem_name', 'raw_cas']]

table_7 = table_7[~table_7['raw_chem_name'].str.contains('Substance')]




# %%% ID 72: Floor wax, polish & care product – Oil for polish and care of wood
table_7_id72 = table_7.iloc[1:10,:]
table_7_id72.reset_index(inplace = True, drop = True )


componentList = []
n = len(table_7_id72)
component = 'ID 72: Floor wax, polish & care product – Oil for polish and care of wood'
componentList.extend([component]*n)

table_7_id72=pd.DataFrame({'raw_chem_name':table_7_id72['raw_chem_name'], 'raw_cas':table_7_id72['raw_cas'], 'component':componentList}) 

# %%% ID 80: Floor wax, polish & care product – Oil for polish & care of wood and stone floors
table_7_id80 = table_7.iloc[12:20,:]
table_7_id80.reset_index(inplace = True, drop = True)


componentList = []
n = len(table_7_id80)
component = 'ID 80: Floor wax, polish & care product – Oil for polish & care of wood and stone floors'
componentList.extend([component]*n)

table_7_id80=pd.DataFrame({'raw_chem_name':table_7_id80['raw_chem_name'], 'raw_cas':table_7_id80['raw_cas'], 'component':componentList}) 


# %%% ID 83: Floor wax, polish & care product – Oil for polish & care of wood and stone floors
table_7_id83 = table_7.iloc[21:28,:]
table_7_id83.reset_index(inplace = True, drop = True)



componentList = []
n = len(table_7_id83)
component = 'ID 83: Floor wax, polish & care product – Oil for polish & care of wood and stone floors'
componentList.extend([component]*n)

table_7_id83=pd.DataFrame({'raw_chem_name':table_7_id83['raw_chem_name'], 'raw_cas':table_7_id83['raw_cas'], 'component':componentList}) 


# %%% ID 85: Floor wax, polish & care product Linseed-oil for polish of wood floors
table_7_id85 = table_7.iloc[29:,:]
table_7_id85.reset_index(inplace = True, drop = True)



componentList = []
n = len(table_7_id85)
component = 'ID 85: Floor wax, polish & care product Linseed-oil for polish of wood floors'
componentList.extend([component]*n)

table_7_id85=pd.DataFrame({'raw_chem_name':table_7_id85['raw_chem_name'], 'raw_cas':table_7_id85['raw_cas'], 'component':componentList}) 



# %%% merging separated dfs

df_list = [table_7_id72,table_7_id80,table_7_id83,table_7_id85]
table_7 = pd.concat(df_list)

# %%% cleaning 
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_7)):
    table_7["raw_chem_name"].iloc[j]=str(table_7["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    table_7["raw_chem_name"].iloc[j]=clean(str(table_7["raw_chem_name"].iloc[j]))
    if len(table_7["raw_chem_name"].iloc[j].split())>1:
        table_7["raw_chem_name"].iloc[j]=" ".join(table_7["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_7["data_document_id"]="1679452"
table_7["data_document_filename"]="diy_projects_table_7.pdf"
table_7["doc_date"]="April 2020"
table_7["raw_category"]=""
table_7["report_funcuse"]=""
table_7["cat_code"]=""
table_7["description_cpcat"]=""
table_7["cpcat_code"]=""
table_7["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(table_7)

# %% Table 8
table_8_raw = read_pdf(file, pages = 27, stream = True, pandas_options={'header': None})
# %%% extraction and clean up
table_8 = table_8_raw[0]
table_8.reset_index(drop = True, inplace = True)
table_8 = table_8.iloc[:,[0,1]]
table_8.columns = ['raw_chem_name', 'raw_cas']
table_8 = table_8.dropna(axis = 0, how = 'all')
table_8 = table_8[~table_8['raw_chem_name'].str.contains('Substance')]
table_8.reset_index(inplace = True, drop = True )





# %%% ID 56: Membrane - Bathroom waterproof coat-ing membrane
table_8_id56 = table_8.iloc[2:5,:]
table_8_id56.reset_index(inplace = True, drop = True )


componentList = []
n = len(table_8_id56)
component = 'ID 56: Membrane - Bathroom waterproof coat-ing membrane'
componentList.extend([component]*n)

table_8_id56=pd.DataFrame({'raw_chem_name':table_8_id56['raw_chem_name'], 'raw_cas':table_8_id56['raw_cas'], 'component':componentList}) 

# %%% ID 60: Adhesive - Mounting of fiberglass fabric
table_8_id60 = table_8.iloc[6:14,:]
table_8_id60.reset_index(inplace = True, drop = True)


componentList = []
n = len(table_8_id60)
component = 'ID 60: Adhesive - Mounting of fiberglass fabric'
componentList.extend([component]*n)

table_8_id60=pd.DataFrame({'raw_chem_name':table_8_id60['raw_chem_name'], 'raw_cas':table_8_id60['raw_cas'], 'component':componentList}) 


# %%% ID 65: Adhesive - Mounting of fiberglass fabric
table_8_id65 = table_8.iloc[15:,:]
table_8_id65.reset_index(inplace = True, drop = True)



componentList = []
n = len(table_8_id65)
component = 'ID 65: Adhesive - Mounting of fiberglass fabric'
componentList.extend([component]*n)

table_8_id65=pd.DataFrame({'raw_chem_name':table_8_id65['raw_chem_name'], 'raw_cas':table_8_id65['raw_cas'], 'component':componentList}) 




# %%% merging separated dfs

df_list = [table_8_id56,table_8_id60,table_8_id65]
table_8 = pd.concat(df_list)

# %%% cleaning 
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(table_8)):
    table_8["raw_chem_name"].iloc[j]=str(table_8["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    table_8["raw_chem_name"].iloc[j]=clean(str(table_8["raw_chem_name"].iloc[j]))
    if len(table_8["raw_chem_name"].iloc[j].split())>1:
        table_8["raw_chem_name"].iloc[j]=" ".join(table_8["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
table_8["data_document_id"]="1679453"
table_8["data_document_filename"]="diy_projects_table_8.pdf"
table_8["doc_date"]="April 2020"
table_8["raw_category"]=""
table_8["report_funcuse"]=""
table_8["cat_code"]=""
table_8["description_cpcat"]=""
table_8["cpcat_code"]=""
table_8["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(table_8)
# %%% DEFINITION pdftotext

def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64' #Path to execfile
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return

    os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Eastman/pdfs')
    remainder = glob('*.pdf')
    
    
    pdfToText(remainder)



# %% appendix 4


append_4_raw = read_pdf(file, pages = "64-71", stream = True, pandas_options={'header': None})
# %%% extraction and clean up


append_4 = pd.concat([append_4_raw[0], append_4_raw[1], append_4_raw[2], append_4_raw[3], append_4_raw[4], append_4_raw[5], append_4_raw[6], append_4_raw[7]])
append_4 = append_4.iloc[:,[2,3,5]]
append_4.reset_index(drop = True, inplace = True)
append_4.columns = ['funcuse', 'raw_chem_name', 'raw_cas']

append_4['raw_cas_cleaned'] = np.NaN
for i,j in enumerate(append_4['raw_cas']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.match(r'\d+-\d\d-\d', str(j))
        append_4['raw_cas_cleaned'].iloc[i] = match[0]
    elif re.search(r'\d+-\d\d-$', str(j)) or re.search(r'\d+-$', str(j)):
        append_4['raw_cas_cleaned'].iloc[i] = str(j) + str(append_4['raw_cas'].iloc[i+1])
    elif str(j).strip() == '-' or str(j).lower().strip() == 'n/a':
        append_4['raw_cas_cleaned'].iloc[i] = 'no cas'

        
        
append_4 = append_4.loc[:,[ 'raw_cas_cleaned','funcuse', 'raw_chem_name']]
append_4 = append_4.fillna('nan')
append_4 = append_4[~append_4['raw_chem_name'].str.contains('Substance')]
append_4 = append_4.replace('nan', np.NaN)
append_4 = append_4.dropna(axis = 0, how = 'all')

append_4['funcuse_cleaned'] = np.NaN
for i,j in enumerate(append_4['funcuse']):
    if str(j) == 'quer' or str(j) == 'polish & care' or str(j) == 'product':
        continue
    elif 'Floor wax' in str(j):
        append_4['funcuse_cleaned'].iloc[i] = 'Floor wax, polish & care product'
        append_4['funcuse_cleaned'].iloc[i+1] = np.NaN
        append_4['funcuse_cleaned'].iloc[i+2] = np.NaN
    elif 'Paint' in str(j):
        append_4['funcuse_cleaned'].iloc[i] = 'Paint & lacquer'
        append_4['funcuse_cleaned'].iloc[i+1] = np.NaN
    elif str(j) == 'nan':
        append_4['funcuse_cleaned'].iloc[i] = np.NaN
    else:
        append_4['funcuse_cleaned'].iloc[i] = str(j)


append_4 = append_4.loc[:,[ 'raw_cas_cleaned','funcuse_cleaned', 'raw_chem_name']]
append_4 = append_4.dropna(axis = 0, how = 'all')



append_4['takeout'] = 'keep'
for i,j in enumerate(append_4['raw_chem_name']):
    if 'SDS missing' in str(j) or 'Does not contain any substance' in str(j) or 'not relevant' in str(j):
        append_4['takeout'].iloc[i] = np.NaN
    else:
        continue
    
append_4 = append_4[append_4['takeout'].notna()]
append_4 = append_4.loc[:,[ 'raw_cas_cleaned','funcuse_cleaned', 'raw_chem_name']]

append_4['first line'] = np.NaN
o = 0
for i,j in enumerate(append_4['funcuse_cleaned']):
    if str(j) == 'nan':
        continue
    else:
        append_4['first line'].iloc[i] = o
        o += 1
    
append_4.fillna(method='ffill', inplace=True)
append_4 = append_4.groupby(['first line', 'raw_cas_cleaned', 'funcuse_cleaned'], as_index=False)['raw_chem_name'].apply(' '.join)
append_4.reset_index(inplace = True, drop = True)

append_4 = append_4.loc[:,['raw_chem_name', 'raw_cas_cleaned', 'funcuse_cleaned']]
append_4.columns = ['raw_chem_name', 'raw_cas', 'report_funcuse']


# %%% cleaning 
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_4)):
    append_4["raw_chem_name"].iloc[j]=str(append_4["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').replace('- ','').strip().lower()
    append_4["report_funcuse"].iloc[j]=str(append_4["report_funcuse"].iloc[j]).strip().lower()
    append_4["raw_chem_name"].iloc[j]=clean(str(append_4["raw_chem_name"].iloc[j]))
    if len(append_4["raw_chem_name"].iloc[j].split())>1:
        append_4["raw_chem_name"].iloc[j]=" ".join(append_4["raw_chem_name"].iloc[j].split())


for i,j in enumerate(append_4['raw_cas']):
    if str(j) == 'no cas':
        append_4['raw_cas'].iloc[i] = np.NaN
    else:
        continue

#Repeating values declaration 
append_4["data_document_id"]="1679454"
append_4["data_document_filename"]="diy_projects_append_4.pdf"
append_4["doc_date"]="April 2020"
append_4["raw_category"]=""
append_4["component"]=""
append_4["cat_code"]=""
append_4["description_cpcat"]=""
append_4["cpcat_code"]=""
append_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_4)

# %% Appendix 6.1
append_6_1_raw = read_pdf(file, pages = 75, stream = True, pandas_options={'header': None})
# %%% extraction and clean up
append_6_1 = append_6_1_raw[0]

for i,j in enumerate(append_6_1[1]):
    if 'Rt' in str(j):
        stop = i
        break
        
append_6_1 = append_6_1.iloc[:stop,[0,1]]
append_6_1.columns = ['raw_chem_name','raw_cas']


append_6_1 = append_6_1.fillna('nan') 
append_6_1 = append_6_1[~append_6_1['raw_chem_name'].str.contains('Unknown|Substance')]
append_6_1 = append_6_1.replace('nan',np.NaN)
append_6_1 = append_6_1.dropna(axis = 0, how = 'all')


for i,j in enumerate(append_6_1['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_1["raw_cas"].iloc[i]=str(append_6_1["raw_cas"].iloc[i]).lstrip('0')


append_6_1.fillna(method='ffill', inplace=True)
append_6_1 = append_6_1.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_1.reset_index(inplace = True, drop = True)
append_6_1 = append_6_1.loc[:,['raw_chem_name','raw_cas']]




# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_1)):
    append_6_1["raw_chem_name"].iloc[j]=str(append_6_1["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_1["raw_chem_name"].iloc[j]=clean(str(append_6_1["raw_chem_name"].iloc[j]))
    if len(append_6_1["raw_chem_name"].iloc[j].split())>1:
        append_6_1["raw_chem_name"].iloc[j]=" ".join(append_6_1["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_1["data_document_id"]="1679455"
append_6_1["data_document_filename"]="diy_projects_append_6_1.pdf"
append_6_1["doc_date"]="April 2020"
append_6_1["component"]=""
append_6_1["raw_category"]=""
append_6_1["component"]=""
append_6_1["report_funcuse"]=""
append_6_1["cat_code"]=""
append_6_1["description_cpcat"]=""
append_6_1["cpcat_code"]=""
append_6_1["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_1)


# %% Appendix 6.2
append_6_2_raw = read_pdf(file, pages = '76-77', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_2 = pd.concat([append_6_2_raw[0],append_6_2_raw[1]])


append_6_2 = append_6_2.dropna(axis = 0, how = 'all')
for i,j in enumerate(append_6_2[0]):
    if 'Appendix 6.2' in str(j):
        start = i
    elif 'Appendix 6.3' in str(j):
        stop = i
        
append_6_2 = append_6_2.iloc[start:stop,[0,1]]
append_6_2['raw_cas'] = np.NaN
append_6_2 = append_6_2.iloc[start:stop,[0,2]]
append_6_2.columns = ['raw_chem_name','raw_cas']


for i,j in enumerate(append_6_2['raw_chem_name']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_2['raw_cas'].iloc[i] = match
        append_6_2['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
append_6_2 = append_6_2.fillna('nan')
append_6_2 = append_6_2[~append_6_2['raw_chem_name'].str.contains('Rt|Substance')]
append_6_2 = append_6_2.replace('nan', np.NaN)    

append_6_2 = append_6_2.fillna('nan') 
append_6_2 = append_6_2[~append_6_2['raw_chem_name'].str.contains('Unknown|Substance')]
append_6_2 = append_6_2[~append_6_2['raw_chem_name'].str.contains('equivalents')]
append_6_2 = append_6_2.replace('nan',np.NaN)
append_6_2 = append_6_2.dropna(axis = 0, how = 'all')


for i,j in enumerate(append_6_2['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_2["raw_cas"].iloc[i]=str(append_6_2["raw_cas"].iloc[i]).lstrip('0')


append_6_2.fillna(method='ffill', inplace=True)
append_6_2 = append_6_2.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_2.reset_index(inplace = True, drop = True)
append_6_2 = append_6_2.loc[:,['raw_chem_name','raw_cas']]



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_2)):
    append_6_2["raw_chem_name"].iloc[j]=str(append_6_2["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_2["raw_chem_name"].iloc[j]=clean(str(append_6_2["raw_chem_name"].iloc[j]))
    if len(append_6_2["raw_chem_name"].iloc[j].split())>1:
        append_6_2["raw_chem_name"].iloc[j]=" ".join(append_6_2["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_2["data_document_id"]="1679456"
append_6_2["data_document_filename"]="diy_projects_append_6_2.pdf"
append_6_2["doc_date"]="April 2020"
append_6_2["raw_category"]=""
append_6_2["report_funcuse"]=""
append_6_2["cat_code"]=""
append_6_2["description_cpcat"]=""
append_6_2["component"]=""
append_6_2["cpcat_code"]=""
append_6_2["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_2)


# %% Appendix 6.3
append_6_3_raw = read_pdf(file, pages = '77-78', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_3 = pd.concat([append_6_3_raw[0],append_6_3_raw[1]])


append_6_3 = append_6_3.dropna(axis = 0, how = 'all')
append_6_3.reset_index(inplace = True, drop = True)
for i,j in enumerate(append_6_3[0]):
    if 'Appendix 6.3' in str(j):
        start = i
    elif 'Rt' in str(j):
        stop = i
        break
    
for i,j in enumerate(append_6_3[0]):
    if 'Appendix 6.3' in str(j):
        start = i
        break
append_6_3 = append_6_3.iloc[start:,[0,1]]   
    
for i,j in enumerate(append_6_3[0]):
    if 'Rt' in str(j):
        stop = i
        break   

append_6_3 = append_6_3.iloc[:stop,[0,1]]
append_6_3['raw_cas'] = np.NaN
append_6_3 = append_6_3.iloc[:,[0,2]]
append_6_3.columns = ['raw_chem_name','raw_cas']


append_6_3 = append_6_3.dropna(axis = 0, how = 'all')
append_6_3 = append_6_3[~append_6_3['raw_chem_name'].str.contains('Substance')]

for i,j in enumerate(append_6_3['raw_chem_name']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_3['raw_cas'].iloc[i] = match
        append_6_3['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
        

append_6_3 = append_6_3.dropna(subset=['raw_cas'])
append_6_3.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_3['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_3["raw_cas"].iloc[i]=str(append_6_3["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_3)):
    append_6_3["raw_chem_name"].iloc[j]=str(append_6_3["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_3["raw_chem_name"].iloc[j]=clean(str(append_6_3["raw_chem_name"].iloc[j]))
    if len(append_6_3["raw_chem_name"].iloc[j].split())>1:
        append_6_3["raw_chem_name"].iloc[j]=" ".join(append_6_3["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_3["data_document_id"]="1679457"
append_6_3["data_document_filename"]="diy_projects_append_6_3.pdf"
append_6_3["doc_date"]="April 2020"
append_6_3["raw_category"]=""
append_6_3["report_funcuse"]=""
append_6_3["cat_code"]=""
append_6_3["component"]=""
append_6_3["description_cpcat"]=""
append_6_3["cpcat_code"]=""
append_6_3["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_3)

# %% Appendix 6.4
append_6_4_raw = read_pdf(file, pages = '78-79', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_4 = pd.concat([append_6_4_raw[0],append_6_4_raw[1]])


append_6_4 = append_6_4.dropna(axis = 0, how = 'all')
append_6_4.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_4[0]):
    if 'Appendix 6.4' in str(j):
        start = i
        break
append_6_4 = append_6_4.iloc[start:,[0,1]]   
    
for i,j in enumerate(append_6_4[0]):
    if 'Rt' in str(j):
        stop = i
        break   

append_6_4 = append_6_4.iloc[:stop,[0,1]]
append_6_4['raw_cas'] = np.NaN
append_6_4 = append_6_4.iloc[:,[0,2]]
append_6_4.columns = ['raw_chem_name','raw_cas']


append_6_4 = append_6_4.dropna(axis = 0, how = 'all')
append_6_4 = append_6_4[~append_6_4['raw_chem_name'].str.contains('Substance')]

for i,j in enumerate(append_6_4['raw_chem_name']):
    
    if '/' in str(j):
        match = re.findall(r'\d+/\d+-\d\d-\d', str(j))[0]
        append_6_4['raw_cas'].iloc[i] = match
        append_6_4['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
        
    elif re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_4['raw_cas'].iloc[i] = match
        append_6_4['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))

for i,j in enumerate(append_6_4['raw_chem_name']):
    if str(j).strip().endswith('-'):
        append_6_4['raw_chem_name'].iloc[i] = str(j).strip().removesuffix('-') 

append_6_4.fillna(method='ffill', inplace=True)
append_6_4 = append_6_4.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_4.reset_index(inplace = True, drop = True)
append_6_4 = append_6_4.loc[:,['raw_chem_name','raw_cas']]


append_6_4.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_4['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_4["raw_cas"].iloc[i]=str(append_6_4["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_4)):
    append_6_4["raw_chem_name"].iloc[j]=str(append_6_4["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_4["raw_chem_name"].iloc[j]=clean(str(append_6_4["raw_chem_name"].iloc[j]))
    if len(append_6_4["raw_chem_name"].iloc[j].split())>1:
        append_6_4["raw_chem_name"].iloc[j]=" ".join(append_6_4["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_4["data_document_id"]="1679458"
append_6_4["data_document_filename"]="diy_projects_append_6_4.pdf"
append_6_4["doc_date"]="April 2020"
append_6_4["raw_category"]=""
append_6_4["report_funcuse"]=""
append_6_4["component"]=""
append_6_4["cat_code"]=""
append_6_4["description_cpcat"]=""
append_6_4["cpcat_code"]=""
append_6_4["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_4)


# %% Appendix 6.5
append_6_5_raw = read_pdf(file, pages = '79-80', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_5 = pd.concat([append_6_5_raw[0],append_6_5_raw[1]])


append_6_5 = append_6_5.dropna(axis = 0, how = 'all')
append_6_5.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_5[0]):
    if 'Appendix 6.5' in str(j):
        start = i
        break
append_6_5 = append_6_5.iloc[start:,[0,1]]   
    
for i,j in enumerate(append_6_5[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_5 = append_6_5.iloc[:stop,[0,1]]
append_6_5.columns = ['raw_chem_name','raw_cas']


append_6_5 = append_6_5.dropna(axis = 0, how = 'all')
append_6_5 = append_6_5[~append_6_5['raw_chem_name'].str.contains('Substance')]
append_6_5.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_5['raw_chem_name']):
    if str(append_6_5['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):
            match = re.findall(r'\d+/\d+-\d\d-\d', str(j))[0]
            append_6_5['raw_cas'].iloc[i] = match
            append_6_5['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_5['raw_cas'].iloc[i] = match
            append_6_5['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue

for i,j in enumerate(append_6_5['raw_chem_name']):
    if str(j).strip().endswith('-'):
        append_6_5['raw_chem_name'].iloc[i] = str(j).strip().removesuffix('-') 

append_6_5.fillna(method='ffill', inplace=True)
append_6_5 = append_6_5.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_5.reset_index(inplace = True, drop = True)
append_6_5 = append_6_5.loc[:,['raw_chem_name','raw_cas']]


append_6_5.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_5['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_5["raw_cas"].iloc[i]=str(append_6_5["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_5)):
    append_6_5["raw_chem_name"].iloc[j]=str(append_6_5["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_5["raw_chem_name"].iloc[j]=clean(str(append_6_5["raw_chem_name"].iloc[j]))
    if len(append_6_5["raw_chem_name"].iloc[j].split())>1:
        append_6_5["raw_chem_name"].iloc[j]=" ".join(append_6_5["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_5["data_document_id"]="1679459"
append_6_5["data_document_filename"]="diy_projects_append_6_5.pdf"
append_6_5["doc_date"]="April 2020"
append_6_5["raw_category"]=""
append_6_5["component"]=""
append_6_5["report_funcuse"]=""
append_6_5["cat_code"]=""
append_6_5["description_cpcat"]=""
append_6_5["cpcat_code"]=""
append_6_5["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_5)

# %% Appendix 6.6
append_6_6_raw = read_pdf(file, pages = '81', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_6 = append_6_6_raw[0]


append_6_6 = append_6_6.dropna(axis = 0, how = 'all')
append_6_6.reset_index(inplace = True, drop = True)

    
for i,j in enumerate(append_6_6[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_6 = append_6_6.iloc[:stop,[0,1]]
append_6_6.columns = ['raw_chem_name','raw_cas']


append_6_6 = append_6_6.dropna(axis = 0, how = 'all')
append_6_6 = append_6_6[~append_6_6['raw_chem_name'].str.contains('Substance')]
append_6_6.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_6['raw_chem_name']):
    if str(append_6_6['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):
            match = re.findall(r'\d+-\d\d-\d/\d+-\d\d-\d', str(j))[0]
            append_6_6['raw_cas'].iloc[i] = match
            append_6_6['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_6['raw_cas'].iloc[i] = match
            append_6_6['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue

for i,j in enumerate(append_6_6['raw_chem_name']):
    if str(j).strip().endswith('-'):
        append_6_6['raw_chem_name'].iloc[i] = str(j).strip().removesuffix('-') 

append_6_6.fillna(method='ffill', inplace=True)
append_6_6 = append_6_6.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_6.reset_index(inplace = True, drop = True)
append_6_6 = append_6_6.loc[:,['raw_chem_name','raw_cas']]


append_6_6.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_6['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_6["raw_cas"].iloc[i]=str(append_6_6["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_6)):
    append_6_6["raw_chem_name"].iloc[j]=str(append_6_6["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_6["raw_chem_name"].iloc[j]=clean(str(append_6_6["raw_chem_name"].iloc[j]))
    if len(append_6_6["raw_chem_name"].iloc[j].split())>1:
        append_6_6["raw_chem_name"].iloc[j]=" ".join(append_6_6["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_6["data_document_id"]="1679460"
append_6_6["data_document_filename"]="diy_projects_append_6_6.pdf"
append_6_6["doc_date"]="April 2020"
append_6_6["raw_category"]=""
append_6_6["report_funcuse"]=""
append_6_6["cat_code"]=""
append_6_6["description_cpcat"]=""
append_6_6["component"]=""
append_6_6["cpcat_code"]=""
append_6_6["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_6)


# %% Appendix 6.7
append_6_7_raw = read_pdf(file, pages = '81-82', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_7 = pd.concat([append_6_7_raw[0],append_6_7_raw[1]])


append_6_7 = append_6_7.dropna(axis = 0, how = 'all')
append_6_7.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_7[0]):
    if 'Appendix 6.7' in str(j):
        start = i
        break
append_6_7 = append_6_7.iloc[start:,[0,1]]
   
for i,j in enumerate(append_6_7[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_7 = append_6_7.iloc[:stop,[0,1]]
append_6_7.columns = ['raw_chem_name','raw_cas']


append_6_7 = append_6_7.dropna(axis = 0, how = 'all')
append_6_7 = append_6_7[~append_6_7['raw_chem_name'].str.contains('Substance')]
append_6_7.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_7['raw_chem_name']):
    if str(append_6_7['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):
            match = re.findall(r'\d+-\d\d-\d/\d+-\d\d-\d', str(j))[0]
            append_6_7['raw_cas'].iloc[i] = match
            append_6_7['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_7['raw_cas'].iloc[i] = match
            append_6_7['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue

append_6_7 = append_6_7.dropna(axis = 0)
append_6_7.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_7['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_7["raw_cas"].iloc[i]=str(append_6_7["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_7)):
    append_6_7["raw_chem_name"].iloc[j]=str(append_6_7["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_7["raw_chem_name"].iloc[j]=clean(str(append_6_7["raw_chem_name"].iloc[j]))
    if len(append_6_7["raw_chem_name"].iloc[j].split())>1:
        append_6_7["raw_chem_name"].iloc[j]=" ".join(append_6_7["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_7["data_document_id"]="1679461"
append_6_7["data_document_filename"]="diy_projects_append_6_7.pdf"
append_6_7["doc_date"]="April 2020"
append_6_7["raw_category"]=""
append_6_7["report_funcuse"]=""
append_6_7["cat_code"]=""
append_6_7["component"]=""
append_6_7["description_cpcat"]=""
append_6_7["cpcat_code"]=""
append_6_7["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_7)

# %% Appendix 6.8
append_6_8_raw = read_pdf(file, pages = '82-83', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_8 = pd.concat([append_6_8_raw[0],append_6_8_raw[1]])


append_6_8 = append_6_8.dropna(axis = 0, how = 'all')
append_6_8.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_8[0]):
    if 'Appendix 6.8' in str(j):
        start = i
        break
append_6_8 = append_6_8.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_8[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_8 = append_6_8.iloc[:stop,[0,1]]
append_6_8.columns = ['raw_chem_name','raw_cas']


append_6_8 = append_6_8.dropna(axis = 0, how = 'all')
append_6_8 = append_6_8[~append_6_8['raw_chem_name'].str.contains('Substance')]
append_6_8.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_8['raw_chem_name']):
    if str(append_6_8['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):
            match = re.findall(r'\d+-\d\d-\d/\d+-\d\d-\d', str(j))[0]
            append_6_8['raw_cas'].iloc[i] = match
            append_6_8['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_8['raw_cas'].iloc[i] = match
            append_6_8['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue

for i,j in enumerate(append_6_8['raw_chem_name']):
    if str(j).strip().endswith('-'):
        append_6_8['raw_chem_name'].iloc[i] = str(j).strip().removesuffix('-') 

append_6_8.fillna(method='ffill', inplace=True)
append_6_8 = append_6_8.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_8.reset_index(inplace = True, drop = True)
append_6_8 = append_6_8.loc[:,['raw_chem_name','raw_cas']]


append_6_8.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_8['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_8["raw_cas"].iloc[i]=str(append_6_8["raw_cas"].iloc[i]).lstrip('0')

append_6_8['raw_chem_name'].iloc[26] = 'Unknown ether (?)'

# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_8)):
    append_6_8["raw_chem_name"].iloc[j]=str(append_6_8["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_8["raw_chem_name"].iloc[j]=clean(str(append_6_8["raw_chem_name"].iloc[j]))
    if len(append_6_8["raw_chem_name"].iloc[j].split())>1:
        append_6_8["raw_chem_name"].iloc[j]=" ".join(append_6_8["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_8["data_document_id"]="1679462"
append_6_8["data_document_filename"]="diy_projects_append_6_8.pdf"
append_6_8["doc_date"]="April 2020"
append_6_8["raw_category"]=""
append_6_8["report_funcuse"]=""
append_6_8["cat_code"]=""
append_6_8["description_cpcat"]=""
append_6_8["component"]=""
append_6_8["cpcat_code"]=""
append_6_8["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_8)
# %% Appendix 6.9
append_6_9_raw = read_pdf(file, pages = '84-85', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_9 = pd.concat([append_6_9_raw[0],append_6_9_raw[1]])


append_6_9 = append_6_9.dropna(axis = 0, how = 'all')
append_6_9.reset_index(inplace = True, drop = True)


   
    
for i,j in enumerate(append_6_9[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_9 = append_6_9.iloc[:stop,[0,1]]
append_6_9.columns = ['raw_chem_name','raw_cas']


append_6_9 = append_6_9.dropna(axis = 0, how = 'all')
append_6_9 = append_6_9.fillna('nan')
append_6_9 = append_6_9[~append_6_9['raw_chem_name'].str.contains('Substance|nan')]
append_6_9.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_9['raw_cas']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_9['raw_cas'].iloc[i] = str(match)



append_6_9.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_9['raw_cas']):
    append_6_9["raw_cas"].iloc[i]=str(append_6_9["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_9)):
    append_6_9["raw_chem_name"].iloc[j]=str(append_6_9["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_9["raw_chem_name"].iloc[j]=clean(str(append_6_9["raw_chem_name"].iloc[j]))
    if len(append_6_9["raw_chem_name"].iloc[j].split())>1:
        append_6_9["raw_chem_name"].iloc[j]=" ".join(append_6_9["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_9["data_document_id"]="1679463"
append_6_9["data_document_filename"]="diy_projects_append_6_9.pdf"
append_6_9["doc_date"]="April 2020"
append_6_9["raw_category"]=""
append_6_9["report_funcuse"]=""
append_6_9["cat_code"]=""
append_6_9["description_cpcat"]=""
append_6_9["component"]=""
append_6_9["cpcat_code"]=""
append_6_9["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_9)

# %% Appendix 6.10

append_6_10_raw = read_pdf(file, pages = '85-86', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_10 = pd.concat([append_6_10_raw[0],append_6_10_raw[1]])


append_6_10 = append_6_10.dropna(axis = 0, how = 'all')
append_6_10.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_10[0]):
    if 'Appendix 6.10' in str(j):
        start = i
        break
append_6_10 = append_6_10.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_10[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_10 = append_6_10.iloc[:stop,[0,1]]
append_6_10.columns = ['raw_chem_name','raw_cas']


append_6_10 = append_6_10.dropna(axis = 0, how = 'all')
append_6_10 = append_6_10.fillna('nan')
append_6_10 = append_6_10[~append_6_10['raw_chem_name'].str.contains('Substance')]
append_6_10 = append_6_10.replace('nan', np.NaN)
append_6_10.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_10['raw_chem_name']):

    if str(append_6_10['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):
            match = re.findall(r'\d+/\d+-\d\d-\d', str(j))[0]
            append_6_10['raw_cas'].iloc[i] = match
            append_6_10['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_10['raw_cas'].iloc[i] = match
            append_6_10['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue

append_6_10 = append_6_10.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_10 = append_6_10[~append_6_10['raw_chem_name'].str.contains('ppendix')]
append_6_10.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_10['raw_cas']):
    if ' ' in str(j).strip():
        append_6_10['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
        
 

append_6_10.fillna(method='ffill', inplace=True)
append_6_10 = append_6_10.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_10.reset_index(inplace = True, drop = True)
append_6_10 = append_6_10.loc[:,['raw_chem_name','raw_cas']]




for i,j in enumerate(append_6_10['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_10["raw_cas"].iloc[i]=str(append_6_10["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_10)):
    append_6_10["raw_chem_name"].iloc[j]=str(append_6_10["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_10["raw_chem_name"].iloc[j]=clean(str(append_6_10["raw_chem_name"].iloc[j]))
    if len(append_6_10["raw_chem_name"].iloc[j].split())>1:
        append_6_10["raw_chem_name"].iloc[j]=" ".join(append_6_10["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_10["data_document_id"]="1679464"
append_6_10["data_document_filename"]="diy_projects_append_6_10.pdf"
append_6_10["doc_date"]="April 2020"
append_6_10["raw_category"]=""
append_6_10["report_funcuse"]=""
append_6_10["cat_code"]=""
append_6_10["description_cpcat"]=""
append_6_10["component"]=""
append_6_10["cpcat_code"]=""
append_6_10["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_10)
# %% Appendix 6.11

append_6_11_raw = read_pdf(file, pages = '86-87', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_11 = pd.concat([append_6_11_raw[0],append_6_11_raw[1]])


append_6_11 = append_6_11.dropna(axis = 0, how = 'all')
append_6_11.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_11[0]):
    if 'Appendix 6.11' in str(j):
        start = i
        break
append_6_11 = append_6_11.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_11[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_11 = append_6_11.iloc[:stop,[0,1]]
append_6_11.columns = ['raw_chem_name','raw_cas']


append_6_11 = append_6_11.dropna(axis = 0, how = 'all')
append_6_11 = append_6_11.fillna('nan')
append_6_11 = append_6_11[~append_6_11['raw_chem_name'].str.contains('Substance')]
append_6_11 = append_6_11.replace('nan', np.NaN)
append_6_11.reset_index(inplace = True, drop = True)

append_6_11 = append_6_11.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_11 = append_6_11[~append_6_11['raw_chem_name'].str.contains('ppendix')]

for i,j in enumerate(append_6_11['raw_chem_name']):

    if str(append_6_11['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):

            match = re.findall(r'\d+/\d+-\d\d-\d', str(j))[0]
            append_6_11['raw_cas'].iloc[i] = match
            append_6_11['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_11['raw_cas'].iloc[i] = match
            append_6_11['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue


append_6_11.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_11['raw_cas']):
    if ' ' in str(j).strip():
        append_6_11['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
        
 



for i,j in enumerate(append_6_11['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_11["raw_cas"].iloc[i]=str(append_6_11["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_11)):
    append_6_11["raw_chem_name"].iloc[j]=str(append_6_11["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_11["raw_chem_name"].iloc[j]=clean(str(append_6_11["raw_chem_name"].iloc[j]))
    if len(append_6_11["raw_chem_name"].iloc[j].split())>1:
        append_6_11["raw_chem_name"].iloc[j]=" ".join(append_6_11["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_11["data_document_id"]="1679465"
append_6_11["data_document_filename"]="diy_projects_append_6_11.pdf"
append_6_11["doc_date"]="April 2020"
append_6_11["raw_category"]=""
append_6_11["report_funcuse"]=""
append_6_11["cat_code"]=""
append_6_11["component"]=""
append_6_11["description_cpcat"]=""
append_6_11["cpcat_code"]=""
append_6_11["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_11)

# %% Appendix 6.12

append_6_12_raw = read_pdf(file, pages = '87', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_12 = append_6_12_raw[0]


append_6_12 = append_6_12.dropna(axis = 0, how = 'all')
append_6_12.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_12[0]):
    if 'Appendix 6.12' in str(j):
        start = i
        break
append_6_12 = append_6_12.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_12[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_12 = append_6_12.iloc[:stop,[0,1]]
append_6_12.columns = ['raw_chem_name','raw_cas']


append_6_12 = append_6_12.dropna(axis = 0, how = 'all')
append_6_12 = append_6_12.fillna('nan')
append_6_12 = append_6_12[~append_6_12['raw_chem_name'].str.contains('Substance')]
append_6_12 = append_6_12.replace('nan', np.NaN)
append_6_12.reset_index(inplace = True, drop = True)

append_6_12 = append_6_12.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_12 = append_6_12[~append_6_12['raw_chem_name'].str.contains('ppendix')]
append_6_12.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_12['raw_chem_name']):

    if str(append_6_12['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):
            match = re.findall(r'\d+/\d+-\d\d-\d', str(j))[0]
            append_6_12['raw_cas'].iloc[i] = match
            append_6_12['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_12['raw_cas'].iloc[i] = match
            append_6_12['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue



for i,j in enumerate(append_6_12['raw_cas']):
    if ' ' in str(j).strip():
        append_6_12['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
        
 



for i,j in enumerate(append_6_12['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_12["raw_cas"].iloc[i]=str(append_6_12["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_12)):
    append_6_12["raw_chem_name"].iloc[j]=str(append_6_12["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_12["raw_chem_name"].iloc[j]=clean(str(append_6_12["raw_chem_name"].iloc[j]))
    if len(append_6_12["raw_chem_name"].iloc[j].split())>1:
        append_6_12["raw_chem_name"].iloc[j]=" ".join(append_6_12["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_12["data_document_id"]="1679466"
append_6_12["data_document_filename"]="diy_projects_append_6_12.pdf"
append_6_12["doc_date"]="April 2020"
append_6_12["raw_category"]=""
append_6_12["report_funcuse"]=""
append_6_12["component"]=""
append_6_12["cat_code"]=""
append_6_12["description_cpcat"]=""
append_6_12["cpcat_code"]=""
append_6_12["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_12)
# %% Appendix 6.13

append_6_13_raw = read_pdf(file, pages = '88', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_13 = append_6_13_raw[0]


append_6_13 = append_6_13.dropna(axis = 0, how = 'all')
append_6_13.reset_index(inplace = True, drop = True)


   
    
for i,j in enumerate(append_6_13[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_13 = append_6_13.iloc[:stop,[0,1]]
append_6_13.columns = ['raw_chem_name','raw_cas']


append_6_13 = append_6_13.dropna(axis = 0, how = 'all')
append_6_13 = append_6_13.fillna('nan')
append_6_13 = append_6_13[~append_6_13['raw_chem_name'].str.contains('Substance')]
append_6_13 = append_6_13.replace('nan', np.NaN)
append_6_13.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_13['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_13["raw_cas"].iloc[i]=str(append_6_13["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_13)):
    append_6_13["raw_chem_name"].iloc[j]=str(append_6_13["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_13["raw_chem_name"].iloc[j]=clean(str(append_6_13["raw_chem_name"].iloc[j]))
    if len(append_6_13["raw_chem_name"].iloc[j].split())>1:
        append_6_13["raw_chem_name"].iloc[j]=" ".join(append_6_13["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_13["data_document_id"]="1679467"
append_6_13["data_document_filename"]="diy_projects_append_6_13.pdf"
append_6_13["doc_date"]="April 2020"
append_6_13["raw_category"]=""
append_6_13["report_funcuse"]=""
append_6_13["component"]=""
append_6_13["cat_code"]=""
append_6_13["description_cpcat"]=""
append_6_13["cpcat_code"]=""
append_6_13["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_13)

# %% Appendix 6.14

append_6_14_raw = read_pdf(file, pages = '88-89', stream = True, pandas_options={'header': None},  area=[[70,65,800,475]])

# %%% extraction and clean up
append_6_14 = pd.concat([append_6_14_raw[0],append_6_14_raw[1]])


append_6_14 = append_6_14.dropna(axis = 0, how = 'all')
append_6_14.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_14[0]):
    if 'Appendix 6.14' in str(j):
        start = i
        break
append_6_14 = append_6_14.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_14[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_14 = append_6_14.iloc[:stop,[0,1]]
append_6_14.columns = ['raw_chem_name','raw_cas']


append_6_14 = append_6_14.dropna(axis = 0, how = 'all')
append_6_14 = append_6_14.fillna('nan')
append_6_14 = append_6_14[~append_6_14['raw_chem_name'].str.contains('Substance')]
append_6_14 = append_6_14.replace('nan', np.NaN)
append_6_14.reset_index(inplace = True, drop = True)

append_6_14 = append_6_14.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_14 = append_6_14[~append_6_14['raw_chem_name'].str.contains('ppendix')]

for i,j in enumerate(append_6_14['raw_chem_name']):
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_14['raw_cas'].iloc[i] = match
        append_6_14['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue


append_6_14.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_14['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_14["raw_cas"].iloc[i]=str(append_6_14["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_14)):
    append_6_14["raw_chem_name"].iloc[j]=str(append_6_14["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_14["raw_chem_name"].iloc[j]=clean(str(append_6_14["raw_chem_name"].iloc[j]))
    if len(append_6_14["raw_chem_name"].iloc[j].split())>1:
        append_6_14["raw_chem_name"].iloc[j]=" ".join(append_6_14["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_14["data_document_id"]="1679468"
append_6_14["data_document_filename"]="diy_projects_append_6_14.pdf"
append_6_14["doc_date"]="April 2020"
append_6_14["raw_category"]=""
append_6_14["report_funcuse"]=""
append_6_14["component"]=""
append_6_14["cat_code"]=""
append_6_14["description_cpcat"]=""
append_6_14["cpcat_code"]=""
append_6_14["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_14)

# %% Appendix 6.15


append_6_15_raw = read_pdf(file, pages = '89-90', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_15 = pd.concat([append_6_15_raw[0],append_6_15_raw[1]])


append_6_15 = append_6_15.dropna(axis = 0, how = 'all')
append_6_15['raw_cas'] = np.NaN
append_6_15 = append_6_15.iloc[:,[0,5]]


append_6_15.reset_index(inplace = True, drop = True)
append_6_15.columns = ['raw_chem_name','raw_cas']

for i,j in enumerate(append_6_15['raw_chem_name']):
    if 'Appendix 6.15' in str(j):
        start = i
        break
append_6_15 = append_6_15.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_15['raw_chem_name']):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_15 = append_6_15.iloc[:stop,[0,1]]



append_6_15 = append_6_15.dropna(axis = 0, how = 'all')
append_6_15 = append_6_15.fillna('nan')
append_6_15 = append_6_15[~append_6_15['raw_chem_name'].str.contains('Substance')]
append_6_15 = append_6_15.replace('nan', np.NaN)
append_6_15.reset_index(inplace = True, drop = True)

append_6_15 = append_6_15.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_15 = append_6_15[~append_6_15['raw_chem_name'].str.contains('ppendix')]

for i,j in enumerate(append_6_15['raw_chem_name']):

    if str(append_6_15['raw_cas'].iloc[i]) == 'nan':
        if '/' in str(j):

            match = re.findall(r'\d+/\d+-\d\d-\d', str(j))[0]
            append_6_15['raw_cas'].iloc[i] = match
            append_6_15['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
            
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            append_6_15['raw_cas'].iloc[i] = match
            append_6_15['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue


append_6_15.reset_index(inplace = True, drop = True)

for i,j in enumerate(append_6_15['raw_cas']):
    if ' ' in str(j).strip():
        append_6_15['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
        
 



for i,j in enumerate(append_6_15['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_15["raw_cas"].iloc[i]=str(append_6_15["raw_cas"].iloc[i]).lstrip('0')


append_6_15 = append_6_15[append_6_15['raw_cas'].notna()]

for i,j in enumerate(append_6_15['raw_chem_name']):
    if '#' in str(j):
        split = str(j).split('#', 1)[0]
        append_6_15['raw_chem_name'].iloc[i] = split
    elif 'aphtha' in str(j):
        append_6_15['raw_chem_name'].iloc[i] = 'Naphtha C7-C13'
        append_6_15['raw_cas'].iloc[i] = '64742-82-1/64742-48-9'






# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_15)):
    append_6_15["raw_chem_name"].iloc[j]=str(append_6_15["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_15["raw_chem_name"].iloc[j]=clean(str(append_6_15["raw_chem_name"].iloc[j]))
    if len(append_6_15["raw_chem_name"].iloc[j].split())>1:
        append_6_15["raw_chem_name"].iloc[j]=" ".join(append_6_15["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_15["data_document_id"]="1679469"
append_6_15["data_document_filename"]="diy_projects_append_6_15.pdf"
append_6_15["doc_date"]="April 2020"
append_6_15["raw_category"]=""
append_6_15["component"]=""
append_6_15["report_funcuse"]=""
append_6_15["cat_code"]=""
append_6_15["description_cpcat"]=""
append_6_15["cpcat_code"]=""
append_6_15["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_15)
# %% Appendix 6.16


append_6_16_raw = read_pdf(file, pages = '90-91', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_16 = pd.concat([append_6_16_raw[0],append_6_16_raw[1]])


append_6_16 = append_6_16.dropna(axis = 0, how = 'all')
append_6_16.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_16[0]):
    if 'Appendix 6.16' in str(j):
        start = i
        break
append_6_16 = append_6_16.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_16[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_16 = append_6_16.iloc[:stop,[0,1]]
append_6_16.columns = ['raw_chem_name','raw_cas']


append_6_16 = append_6_16.dropna(axis = 0, how = 'all')
append_6_16 = append_6_16.fillna('nan')
append_6_16 = append_6_16[~append_6_16['raw_chem_name'].str.contains('Substance')]
append_6_16 = append_6_16.replace('nan', np.NaN)
append_6_16.reset_index(inplace = True, drop = True)

append_6_16 = append_6_16.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_16 = append_6_16[~append_6_16['raw_chem_name'].str.contains('ppendix')]

for i,j in enumerate(append_6_16['raw_chem_name']):
            
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_16['raw_cas'].iloc[i] = match
        append_6_16['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue



append_6_16.fillna(method='ffill', inplace=True)
append_6_16 = append_6_16.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_16.reset_index(inplace = True, drop = True)
append_6_16 = append_6_16.loc[:,['raw_chem_name','raw_cas']]
append_6_16.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_16['raw_chem_name']):
    if re.search(r'/\d+-\d\d-\d', str(j)):
        match = re.findall(r'/\d+-\d\d-\d', str(j))[0]
        append_6_16['raw_cas'].iloc[i] = str(append_6_16['raw_cas'].iloc[i]) + str(match)
        append_6_16['raw_chem_name'].iloc[i] = re.sub(match,'' ,str(j))




for i,j in enumerate(append_6_16['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_16["raw_cas"].iloc[i]=str(append_6_16["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_16)):
    append_6_16["raw_chem_name"].iloc[j]=str(append_6_16["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_16["raw_chem_name"].iloc[j]=clean(str(append_6_16["raw_chem_name"].iloc[j]))
    if re.search(r'[o]-\s[m]',append_6_16['raw_chem_name'].iloc[j]):
        append_6_16['raw_chem_name'].iloc[j] = re.sub(r'-\s','',append_6_16['raw_chem_name'].iloc[j])
    if len(append_6_16["raw_chem_name"].iloc[j].split())>1:
        append_6_16["raw_chem_name"].iloc[j]=" ".join(append_6_16["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_16["data_document_id"]="1679470"
append_6_16["data_document_filename"]="diy_projects_append_6_16.pdf"
append_6_16["doc_date"]="April 2020"
append_6_16["raw_category"]=""
append_6_16["component"]=""
append_6_16["report_funcuse"]=""
append_6_16["cat_code"]=""
append_6_16["description_cpcat"]=""
append_6_16["cpcat_code"]=""
append_6_16["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_16)
# %% Appendix 6.17


append_6_17_raw = read_pdf(file, pages = '91-92', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_17 = pd.concat([append_6_17_raw[0],append_6_17_raw[1]])


append_6_17 = append_6_17.dropna(axis = 0, how = 'all')
append_6_17.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_17[0]):
    if 'Appendix 6.17' in str(j):
        start = i
        break
append_6_17 = append_6_17.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_17[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_17 = append_6_17.iloc[:stop,[0,1]]
append_6_17.columns = ['raw_chem_name','raw_cas']


append_6_17 = append_6_17.dropna(axis = 0, how = 'all')
append_6_17 = append_6_17.fillna('nan')
append_6_17 = append_6_17[~append_6_17['raw_chem_name'].str.contains('Substance')]
append_6_17 = append_6_17.replace('nan', np.NaN)
append_6_17.reset_index(inplace = True, drop = True)

append_6_17 = append_6_17.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_17 = append_6_17[~append_6_17['raw_chem_name'].str.contains('ppendix')]

for i,j in enumerate(append_6_17['raw_chem_name']):
            
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_17['raw_cas'].iloc[i] = match
        append_6_17['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue


for i,j in enumerate(append_6_17['raw_cas']):
    if ' ' in str(j).strip():
        append_6_17['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
        

append_6_17.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_17['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_17["raw_cas"].iloc[i]=str(append_6_17["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_17)):
    append_6_17["raw_chem_name"].iloc[j]=str(append_6_17["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_17["raw_chem_name"].iloc[j]=clean(str(append_6_17["raw_chem_name"].iloc[j]))
    if re.search(r'[o]-\s[m]',append_6_17['raw_chem_name'].iloc[j]):
        append_6_17['raw_chem_name'].iloc[j] = re.sub(r'-\s','',append_6_17['raw_chem_name'].iloc[j])
    if len(append_6_17["raw_chem_name"].iloc[j].split())>1:
        append_6_17["raw_chem_name"].iloc[j]=" ".join(append_6_17["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_17["data_document_id"]="1679471"
append_6_17["data_document_filename"]="diy_projects_append_6_17.pdf"
append_6_17["doc_date"]="April 2020"
append_6_17["raw_category"]=""
append_6_17["report_funcuse"]=""
append_6_17["component"]=""
append_6_17["cat_code"]=""
append_6_17["description_cpcat"]=""
append_6_17["cpcat_code"]=""
append_6_17["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_17)

# %% Appendix 6.18


append_6_18_raw = read_pdf(file, pages = '92-93', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_18 = pd.concat([append_6_18_raw[0],append_6_18_raw[1]])


append_6_18 = append_6_18.dropna(axis = 0, how = 'all')
append_6_18.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_18[0]):
    if 'Appendix 6.18' in str(j):
        start = i
        break
append_6_18 = append_6_18.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_18[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_18 = append_6_18.iloc[:stop,[0,1]]
append_6_18.columns = ['raw_chem_name','raw_cas']


append_6_18 = append_6_18.dropna(axis = 0, how = 'all')
append_6_18 = append_6_18.fillna('nan')
append_6_18 = append_6_18[~append_6_18['raw_chem_name'].str.contains('Substance')]
append_6_18 = append_6_18.replace('nan', np.NaN)
append_6_18.reset_index(inplace = True, drop = True)

append_6_18 = append_6_18.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_18 = append_6_18[~append_6_18['raw_chem_name'].str.contains('ppendix')]



for i,j in enumerate(append_6_18['raw_chem_name']):
            
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_18['raw_cas'].iloc[i] = match
        append_6_18['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue



append_6_18.fillna(method='ffill', inplace=True)
append_6_18 = append_6_18.groupby(['raw_cas'], as_index=False)['raw_chem_name'].apply(''.join)
append_6_18.reset_index(inplace = True, drop = True)
append_6_18 = append_6_18.loc[:,['raw_chem_name','raw_cas']]
append_6_18.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_18['raw_chem_name']):
    if re.search(r'/\d+-\d\d-\d', str(j)):
        match = re.findall(r'/\d+-\d\d-\d', str(j))[0]
        append_6_18['raw_cas'].iloc[i] = str(append_6_18['raw_cas'].iloc[i]) + str(match)
        append_6_18['raw_chem_name'].iloc[i] = re.sub(match,'' ,str(j))





for i,j in enumerate(append_6_18['raw_cas']):
    if ' ' in str(j).strip():
        append_6_18['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
        

append_6_18.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_18['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_18["raw_cas"].iloc[i]=str(append_6_18["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_18)):
    append_6_18["raw_chem_name"].iloc[j]=str(append_6_18["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_18["raw_chem_name"].iloc[j]=clean(str(append_6_18["raw_chem_name"].iloc[j]))
    if re.search(r'[o]-\s[m]',append_6_18['raw_chem_name'].iloc[j]):
        append_6_18['raw_chem_name'].iloc[j] = re.sub(r'-\s','',append_6_18['raw_chem_name'].iloc[j])
    if len(append_6_18["raw_chem_name"].iloc[j].split())>1:
        append_6_18["raw_chem_name"].iloc[j]=" ".join(append_6_18["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_18["data_document_id"]="1679472"
append_6_18["data_document_filename"]="diy_projects_append_6_18.pdf"
append_6_18["doc_date"]="April 2020"
append_6_18["raw_category"]=""
append_6_18["component"]=""
append_6_18["report_funcuse"]=""
append_6_18["cat_code"]=""
append_6_18["description_cpcat"]=""
append_6_18["cpcat_code"]=""
append_6_18["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_18)

# %% Appendix 6.19


append_6_19_raw = read_pdf(file, pages = '93-94', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_19 = pd.concat([append_6_19_raw[0],append_6_19_raw[1]])


append_6_19 = append_6_19.dropna(axis = 0, how = 'all')
append_6_19.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_19[0]):
    if 'Appendix 6.19' in str(j):
        start = i
        break
append_6_19 = append_6_19.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_19[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_19 = append_6_19.iloc[:stop,[0,1]]
append_6_19.columns = ['raw_chem_name','raw_cas']


append_6_19 = append_6_19.dropna(axis = 0, how = 'all')
append_6_19 = append_6_19.fillna('nan')
append_6_19 = append_6_19[~append_6_19['raw_chem_name'].str.contains('Substance')]
append_6_19 = append_6_19.replace('nan', np.NaN)
append_6_19.reset_index(inplace = True, drop = True)

append_6_19 = append_6_19.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_19 = append_6_19[~append_6_19['raw_chem_name'].str.contains('ppendix')]



for i,j in enumerate(append_6_19['raw_chem_name']):
            
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_19['raw_cas'].iloc[i] = match
        append_6_19['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue



for i,j in enumerate(append_6_19['raw_chem_name']):
    if re.search(r'/\d+-\d\d-\d', str(j)):
        match = re.findall(r'/\d+-\d\d-\d', str(j))[0]
        append_6_19['raw_cas'].iloc[i] = str(append_6_19['raw_cas'].iloc[i]) + str(match)
        append_6_19['raw_chem_name'].iloc[i] = re.sub(match,'' ,str(j))

        

append_6_19.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_19['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_19["raw_cas"].iloc[i]=str(append_6_19["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_19)):
    append_6_19["raw_chem_name"].iloc[j]=str(append_6_19["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_19["raw_chem_name"].iloc[j]=clean(str(append_6_19["raw_chem_name"].iloc[j]))
    if re.search(r'[o]-\s[m]',append_6_19['raw_chem_name'].iloc[j]):
        append_6_19['raw_chem_name'].iloc[j] = re.sub(r'-\s','',append_6_19['raw_chem_name'].iloc[j])
    if len(append_6_19["raw_chem_name"].iloc[j].split())>1:
        append_6_19["raw_chem_name"].iloc[j]=" ".join(append_6_19["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_19["data_document_id"]="1679473"
append_6_19["data_document_filename"]="diy_projects_append_6_19.pdf"
append_6_19["doc_date"]="April 2020"
append_6_19["raw_category"]=""
append_6_19["report_funcuse"]=""
append_6_19["component"]=""
append_6_19["cat_code"]=""
append_6_19["description_cpcat"]=""
append_6_19["cpcat_code"]=""
append_6_19["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_19)

# %% Appendix 6.20


append_6_20_raw = read_pdf(file, pages = '94-95', stream = True, pandas_options={'header': None})

# %%% extraction and clean up
append_6_20 = pd.concat([append_6_20_raw[0],append_6_20_raw[1]])


append_6_20 = append_6_20.dropna(axis = 0, how = 'all')
append_6_20.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_20[0]):
    if 'Appendix 6.20' in str(j):
        start = i
        break
append_6_20 = append_6_20.iloc[start:,[0,1]]
   
    
for i,j in enumerate(append_6_20[0]):
    if 'Sum' in str(j):
        stop = i
        break   

append_6_20 = append_6_20.iloc[:stop,[0,1]]
append_6_20.columns = ['raw_chem_name','raw_cas']


append_6_20 = append_6_20.dropna(axis = 0, how = 'all')
append_6_20 = append_6_20.fillna('nan')
append_6_20 = append_6_20[~append_6_20['raw_chem_name'].str.contains('Substance')]
append_6_20 = append_6_20.replace('nan', np.NaN)
append_6_20.reset_index(inplace = True, drop = True)

append_6_20 = append_6_20.dropna(subset = ['raw_chem_name'], axis = 0)
append_6_20 = append_6_20[~append_6_20['raw_chem_name'].str.contains('ppendix')]



for i,j in enumerate(append_6_20['raw_chem_name']):
            
    if re.search(r'\d+-\d\d-\d', str(j)):
        match = re.findall(r'\d+-\d\d-\d', str(j))[0]
        append_6_20['raw_cas'].iloc[i] = match
        append_6_20['raw_chem_name'].iloc[i] = re.sub(match,'',str(j))
    else:
        continue


for i,j in enumerate(append_6_20['raw_cas']):
    if ' ' in str(j).strip():
        append_6_20['raw_cas'].iloc[i] = str(j).split(' ')[0]
    elif 'nan' in str(j):
        continue
    elif not re.search(r'\d+-\d\d-\d', str(j)):
        append_6_20['raw_cas'].iloc[i] = ''
        

append_6_20.reset_index(inplace = True, drop = True)


for i,j in enumerate(append_6_20['raw_cas']):
    if str(j) == 'nan':
        continue
    else:
        append_6_20["raw_cas"].iloc[i]=str(append_6_20["raw_cas"].iloc[i]).lstrip('0')



# %%% cleaning 


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(append_6_20)):
    append_6_20["raw_chem_name"].iloc[j]=str(append_6_20["raw_chem_name"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    append_6_20["raw_chem_name"].iloc[j]=clean(str(append_6_20["raw_chem_name"].iloc[j]))
    if re.search(r'[o]-\s[m]',append_6_20['raw_chem_name'].iloc[j]):
        append_6_20['raw_chem_name'].iloc[j] = re.sub(r'-\s','',append_6_20['raw_chem_name'].iloc[j])
    if len(append_6_20["raw_chem_name"].iloc[j].split())>1:
        append_6_20["raw_chem_name"].iloc[j]=" ".join(append_6_20["raw_chem_name"].iloc[j].split())


#Repeating values declaration 
append_6_20["data_document_id"]="1679474"
append_6_20["data_document_filename"]="diy_projects_append_6_20.pdf"
append_6_20["doc_date"]="April 2020"
append_6_20["raw_category"]=""
append_6_20["component"]=""
append_6_20["report_funcuse"]=""
append_6_20["cat_code"]=""
append_6_20["description_cpcat"]=""
append_6_20["cpcat_code"]=""
append_6_20["cpcat_sourcetype"]="ACToR Assays and Lists"

#add to list of dfs
diy_products_dfs.append(append_6_20)


# %% merge all table records together


diy_projects_df = pd.concat(diy_products_dfs)




# %% split chemicals with multiple cas numbers

diy_projects_df = diy_projects_df.fillna('nan')
repeats = diy_projects_df[diy_projects_df['raw_cas'].str.contains('/')] 


for i,j in enumerate(diy_projects_df['raw_cas']):
    if '/' in str(j):
        split = str(j).split('/', 1)[0]
        diy_projects_df['raw_cas'].iloc[i] = split
    else:
        continue
    
    
for i,j in enumerate(repeats['raw_cas']):
    split = str(j).split('/', 1)[1]
    repeats['raw_cas'].iloc[i] = split
    
# %% export

#combine dataframes in list together 
diy_projects_ext = pd.concat([diy_projects_df,repeats])



#final cleaning
diy_projects_ext = diy_projects_ext.replace(to_replace='nan', value = np.NaN)
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(diy_projects_ext)):
    diy_projects_ext["component"].iloc[j]=str(diy_projects_ext["component"].iloc[j]).replace('–', '-').replace('#','').strip().lower()
    diy_projects_ext["component"].iloc[j]=clean(str(diy_projects_ext["component"].iloc[j]))
    if re.search(r'[o]-\s[m]',diy_projects_ext['component'].iloc[j]):
        diy_projects_ext['component'].iloc[j] = re.sub(r'-\s','',diy_projects_ext['component'].iloc[j])
    if len(diy_projects_ext["component"].iloc[j].split())>1:
        diy_projects_ext["component"].iloc[j]=" ".join(diy_projects_ext["component"].iloc[j].split())


#export
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\DCPS_DIY\csvs')
diy_projects_ext.to_csv('diy_projects_ext_2.csv', index=False)

