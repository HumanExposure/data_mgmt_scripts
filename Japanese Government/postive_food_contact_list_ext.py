
"""
Created on Wed Apr 24 8:05:35 2023
@author: CLUTZ01
"""
# %% imports
import os, string, csv, re
import camelot
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from glob import glob
from pikepdf import Pdf
from tqdm import tqdm
import unicodedata



# %% cleanline
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('ー', '-')
    cline = cline.lower()
    cline = unicodedata.normalize('NFKC', cline)
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)

# %% Group polymers (plastics)

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Japan Food Contact Lists')
plastics = pd.read_csv('plastics_v4.csv')
plastics.columns = ['raw_chem_name', 'raw_cas']
plastics['component'] = np.NaN


# %%

for i,j in enumerate(plastics['raw_chem_name']):
    if re.search(r'^[\uff10-\uff19]+\uff0e|^\d+\uff0e', str(j)):
        plastics["component"].iloc[i] = re.sub(r'\d{0,3}[^\u0000-\u007F]+', '', str(j)).strip()
        plastics['raw_chem_name'].iloc[i] = ''

plastics['component'] = plastics['component'].ffill()

# %%
# for i,j in enumerate(plastics['raw_chem_name']):
#     if re.search(r'^[A-Z]\.', str(j)):
#         print('#####################')
#         print(i)
#         print(j)
#         print('\n')

#changing out full width '-' (\uff0d) with normal '-'
plastics.raw_cas = plastics.raw_cas.str.replace(r'\uff0d', '-')
# take out headers such as A. OR C.
plastics = plastics[~plastics["raw_chem_name"].str.contains(r'^[A-Z]\.')]

# take out "^copolymer"
plastics = plastics[~plastics["raw_chem_name"].str.contains(r'^Copolymer')]


# take out special brackets and everything in them


plastics = plastics[~((plastics["raw_chem_name"].str.len() <=20) & (plastics['raw_cas'].isnull()))]
plastics = plastics[~((plastics["raw_chem_name"].str.contains(r'^[A-Z]-\d\.')) & (plastics['raw_cas'].eq('-')))]


# %% split up mult-cas lines

list_of_lists = []
for i,j in enumerate(plastics['raw_cas']):
    match = re.findall(r'\d+-\d\d-\d', str(j))
    count = len(match)
    if count <= 1:
        continue
    if count > 1:
        plastics['raw_cas'].iloc[i] = match[0]
        for ix,x in enumerate(match):
            if ix == 0:
                continue
            else:
                new_chem_name = plastics['raw_chem_name'].iloc[i]
                new_cas = str(x)
                new_list = [str(new_chem_name), str(new_cas)]
                list_of_lists.append(new_list)


merge_df = pd.DataFrame(list_of_lists,columns=['raw_chem_name','raw_cas'])
df_lists = [plastics,merge_df]
plastics_ext = pd.concat(df_lists)
plastics_ext.reset_index(inplace=True, drop=True)

plastics_ext = plastics_ext.drop_duplicates()

# %%% clean chem names
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(plastics_ext)):
    plastics_ext["raw_chem_name"].iloc[j]=str(plastics_ext["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('β', 'beta').replace('γ', 'gamma')
    plastics_ext["raw_chem_name"].iloc[j]=clean(str(plastics_ext["raw_chem_name"].iloc[j]))
    if len(plastics_ext["raw_chem_name"].iloc[j].split())>1:
        plastics_ext["raw_chem_name"].iloc[j]=" ".join(plastics_ext["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration 
plastics_ext["data_document_id"]="1724078"
plastics_ext["data_document_filename"]="japan_fc_plastics.pdf"
plastics_ext["doc_date"]="2020"
plastics_ext["raw_category"]=""
plastics_ext["report_funcuse"]=""
plastics_ext["cat_code"]=""
plastics_ext["description_cpcat"]=""
plastics_ext["cpcat_code"]=""
plastics_ext["cpcat_sourcetype"]="ACToR Assays and Lists"




# %% coatings

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Japan Food Contact Lists')
coatings = pd.read_csv('coatings_v6_3_.csv')
coatings = coatings.dropna(how = 'all', axis = 0)
coatings.columns = ['raw_chem_name', 'raw_cas']
coatings['component'] = np.NaN


for i,j in enumerate(coatings['raw_chem_name']):
    if re.search(r'^[\uff10-\uff19]+\uff0e|^\d+\uff0e', str(j)):
        coatings["component"].iloc[i] = re.sub(r'\d{0,3}[^\u0000-\u007F]+', '', str(j)).strip()
        coatings['raw_chem_name'].iloc[i] = ''

coatings['component'] = coatings['component'].ffill()

# %%
# 【19.B】
# %%

#changing out full width '-' (\uff0d) with normal '-'
coatings.raw_cas = coatings.raw_cas.str.replace(r'\uff0d', '-')

# take out headers such as A. OR C.
coatings = coatings[~coatings.raw_chem_name.eq('')]
coatings = coatings[~coatings["raw_chem_name"].str.contains(r'^[A-Z]\.')]

# take out "^copolymer"
coatings = coatings[~coatings["raw_chem_name"].str.contains(r'^Copolymer')]
coatings = coatings[~coatings["raw_chem_name"].str.contains(r'^copolymer')]



# take out special brackets and everything in them

for i,j in enumerate(coatings['raw_chem_name']):
    if re.search(r'\u3010', str(j)):
        if ',' in str(j):
            new_j = str(j).split(',', 1)[0]
            coatings['raw_chem_name'].iloc[i] = new_j
        else:
            coatings['raw_chem_name'].iloc[i] = str(j).replace(r'\u3010.+\u3011', '')
        
coatings = coatings[~((coatings.raw_chem_name.str.contains('following')) & (coatings.raw_cas.eq('-')))]


# %% split up mult-cas lines
list_of_lists = []
for i,j in enumerate(coatings['raw_cas']):
    match = re.findall(r'\d+-\d\d-\d', str(j))
    count = len(match)
    if count <= 1:
        continue
    if count > 1:
        # print('##############')
        # print(match)
        coatings['raw_cas'].iloc[i] = match[0]
        for ix,x in enumerate(match):
            if ix == 0:
                continue
            else:
                new_chem_name = coatings['raw_chem_name'].iloc[i]
                new_cas = str(x)
                new_component = coatings['component'].iloc[i]
                new_list = [str(new_chem_name), str(new_cas), str(new_component).lower()]
                list_of_lists.append(new_list)
            

merge_df = pd.DataFrame(list_of_lists,columns=['raw_chem_name','raw_cas','component'])
df_lists = [coatings,merge_df]
coatings_ext = pd.concat(df_lists)

coatings_ext.reset_index(inplace=True, drop=True)

# coatings_ext.columns = ['raw_chem_name', 'raw_cas', 'component']
# %% coatings clean up

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(coatings_ext)):
    coatings_ext["raw_chem_name"].iloc[j]=str(coatings_ext["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('β', 'beta').replace('γ', 'gamma')
    coatings_ext["raw_chem_name"].iloc[j]=clean(str(coatings_ext["raw_chem_name"].iloc[j]))
    if len(coatings_ext["raw_chem_name"].iloc[j].split())>1:
        coatings_ext["raw_chem_name"].iloc[j]=" ".join(coatings_ext["raw_chem_name"].iloc[j].split())




coatings_ext["data_document_id"]="1724079"
coatings_ext["data_document_filename"]="japan_fc_coatings.pdf"
coatings_ext["doc_date"]="2020"
coatings_ext["raw_category"]=""
coatings_ext["report_funcuse"]=""
coatings_ext["cat_code"]=""
coatings_ext["description_cpcat"]=""
coatings_ext["cpcat_code"]=""
coatings_ext["cpcat_sourcetype"]="ACToR Assays and Lists"



# %%trace monomers


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Japan Food Contact Lists')
trace_monomers = pd.read_csv('trace_monomers.csv')
trace_monomers = trace_monomers.dropna(how = 'all', axis = 0)
for i,j in enumerate(trace_monomers['raw_cas']):
    trace_monomers['raw_cas'].iloc[i] = unicodedata.normalize('NFKC', str(j))

trace_monomers = trace_monomers.loc[:,'raw_chem_name':]
# %%split up mult-cas lines
list_of_lists = []
for i,j in enumerate(trace_monomers['raw_cas']):
    match = re.findall(r'\d+-\d\d-\d', str(j))
    count = len(match)
    if count <= 1:
        continue
    if count > 1:
        # print('##############')
        # print(match)
        trace_monomers['raw_cas'].iloc[i] = match[0]
        for ix,x in enumerate(match):
            if ix == 0:
                continue
            else:
                new_chem_name = trace_monomers['raw_chem_name'].iloc[i]
                new_cas = str(x)
                new_list = [str(new_chem_name), str(new_cas)]
                list_of_lists.append(new_list)
            

merge_df = pd.DataFrame(list_of_lists,columns=['raw_chem_name','raw_cas'])
df_lists = [trace_monomers,merge_df]
trace_monomers_ext = pd.concat(df_lists)

trace_monomers_ext.reset_index(inplace=True, drop=True)




# %% trace monomers clean up


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(trace_monomers_ext)):
    trace_monomers_ext["raw_chem_name"].iloc[j]=str(trace_monomers_ext["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('β', 'beta').replace('γ', 'gamma')
    trace_monomers_ext["raw_chem_name"].iloc[j]=clean(str(trace_monomers_ext["raw_chem_name"].iloc[j]))
    if len(trace_monomers_ext["raw_chem_name"].iloc[j].split())>1:
        trace_monomers_ext["raw_chem_name"].iloc[j]=" ".join(trace_monomers_ext["raw_chem_name"].iloc[j].split())


trace_monomers_ext["data_document_id"]="1724080"
trace_monomers_ext["data_document_filename"]="japan_fc_trace_monomers_ext.pdf"
trace_monomers_ext["doc_date"]="2020"
trace_monomers_ext["raw_category"]=""
trace_monomers_ext["component"]=""
trace_monomers_ext["report_funcuse"]=""
trace_monomers_ext["cat_code"]=""
trace_monomers_ext["description_cpcat"]=""
trace_monomers_ext["cpcat_code"]=""
trace_monomers_ext["cpcat_sourcetype"]="ACToR Assays and Lists"


# %% reference information

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Japan Food Contact Lists')
appendix = pd.read_csv('appendix.csv')
appendix.columns = ['raw_chem_name', 'raw_cas']

# %%

for i,j in enumerate(appendix['raw_chem_name']):
    appendix['raw_chem_name'].iloc[i] = unicodedata.normalize('NFKC', str(j))
    appendix['raw_cas'].iloc[i] = unicodedata.normalize('NFKC', appendix['raw_cas'].iloc[i])
appendix  = appendix.fillna('nan')

chem_list = []
cas_list = []

for i,j in enumerate(appendix['raw_cas']):
    # print(str(j))
    # i = 743
    if str(j) == '-':
        chem = str(appendix['raw_chem_name'].iloc[i])
        chem_ext = [chem]
        chem_list.extend(chem_ext)
        # print(chem)
        cas_list.extend([str(j)]*1)
    else:
        splits = str(j).split('\n')
        n = len(splits)
        chem_name = [str(appendix['raw_chem_name'].iloc[i])]
        chem_list.extend(chem_name*n)
        cas_list.extend(splits)

# new_appendix
appendix_df = pd.DataFrame({'raw_chem_name':chem_list, 'raw_cas':cas_list})
appendix_df = appendix_df[~appendix_df.raw_chem_name.str.contains("English Name")]
appendix_df = appendix_df.drop_duplicates()



 # %% reference info clean up
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(appendix_df)):
    appendix_df["raw_chem_name"].iloc[j]=str(appendix_df["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('β', 'beta').replace('γ', 'gamma')
    appendix_df["raw_chem_name"].iloc[j]=clean(str(appendix_df["raw_chem_name"].iloc[j]))
    if len(appendix_df["raw_chem_name"].iloc[j].split())>1:
        appendix_df["raw_chem_name"].iloc[j]=" ".join(appendix_df["raw_chem_name"].iloc[j].split())


appendix_df["data_document_id"]="1724081"
appendix_df["data_document_filename"]="japan_fc_appendix.pdf"
appendix_df["doc_date"]="2020"
appendix_df["raw_category"]=""
appendix_df["component"]=""
appendix_df["report_funcuse"]=""
appendix_df["cat_code"]=""
appendix_df["description_cpcat"]=""
appendix_df["cpcat_code"]=""
appendix_df["cpcat_sourcetype"]="ACToR Assays and Lists"

appendix_df.to_csv('japan_fc_appendix.csv', columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %% merging all data together

all_ext_dfs = [plastics_ext, coatings_ext, trace_monomers_ext, appendix_df]
japan_fc_ext = pd.concat(all_ext_dfs)
japan_fc_ext.drop_duplicates(inplace = True)
japan_fc_ext.reset_index(inplace=True, drop=True)
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Japan Food Contact Lists\output files')
japan_fc_ext.to_csv('japan_fc_ext.csv', columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)

# %%

filenames = japan_fc_ext.loc[:,['data_document_filename']]
filenames = filenames.drop_duplicates()
print(type(filenames))


# %% Registered records file creation
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Japan Food Contact Lists')

filenames = filenames['data_document_filename'].to_list()
n = len(filenames)
titles = ['Appended Table 1 (1)', 'Appended Table 1 (2)', 'Appended Table 1 (3)', 'Appended Table 2']
doc_type = ['FO']*n
url = ['https://translation.mhlw.go.jp/LUCMHLW/ns/tl.cgi/https://www.mhlw.go.jp/stf/newpage_36419.html?SLANG=ja&TLANG=en&XMODE=0&XCHARSET=utf-8&XJSID=0']*n    
organization = ['Ministry of Health, Labour and Welfare']*n
subtitle = ['Base Polymer (Plastics)',  'Base Polymer (Coatings)', 'Base Polymer (Trace monomers)', 'Reference Information']
epa_reg_number = ['']*n
pmid = ['']*n
hero_id = ['']*n



rr = pd.DataFrame({'filename': filenames, 'title': titles, 'document_type':doc_type, 'url': url, 'organization': organization, 'subtitle': subtitle, 'epa_reg_number': epa_reg_number, 'pmid': pmid, 'hero_id': hero_id})
rr.to_csv('japan_fc_rr.csv', index=False)

