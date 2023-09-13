# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 14:13:57 2023

@author: CLUTZ01
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:49:48 2023

@author: CLUTZ01
"""
# %% imports

import os, string, csv, re
import pandas as pd
import numpy as np
import tabula as tb


import sys
print (sys.version)


from glob import glob


from tqdm import tqdm
import pickle

# %% Definitions
# %%% DEFINITION cleaning text
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

# %%% DEFINITION findchars
def findchars(stringx):
    res = ""
    # Nonetype = type(None)
    # if isinstance(stringx, NoneType):
    #     return False
    for i in stringx:
        if i.isalpha():
            res = "".join([res, i])
    return res




# %% finding files with no hazardous chemicals


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs')
all_files = glob('*.pdf')

pdfs_no_hazards = {}
for file in tqdm(all_files):
    
    print('\n')
    print('###################################################')
    print('\n')
    print('working on: ' + file)
    ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    lines = cleaned.split('\n')
    
    chemical_sect_clean = [e for i,e in enumerate(lines) if len(e) != 0]
    
    
    #find chemical section
  
        
    for index,line in enumerate(chemical_sect_clean):
        if 'concentration' in line:
            chem_sect_start = index
            break
        elif 'section 3' in str(line).lower():
            chem_sect_start = index
            break
        else:
            continue
            
    
    for index,line in enumerate(chemical_sect_clean):
        if 'firstaid' in line.replace(' ',''):
            chem_sect_end = index + 1
            break
                 
    chemical_sect = chemical_sect_clean[chem_sect_start:chem_sect_end]
   
    

            
    no_hazards = False            
    for line in chemical_sect:
        if "no hazardous ingredients" in line or "non-hazardous ingredients" in line:
            print('no hazardous ingredients')
            no_hazards = True
            break
            
            
    if no_hazards == True:
        pdfs_no_hazards[file] = chemical_sect
        print('no hazards')
        print('continue')

    
        
        


# %% pre_filtering

hazard_files = [i for i in all_files if i not in pdfs_no_hazards]



# %%
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs')
all_files = glob('*.pdf')
pdfs_weird = {}
pdf_normal = {}
other= []
# cleaned_dict = {}
for file in tqdm(hazard_files):

    print('\n')
    print('###################################################')
    print('\n')
    print('working on: ' + file)
    ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    lines = cleaned.split('\n')
    
    
    lines_clean = [e for i,e in enumerate(lines) if len(e) != 0]
    
    
    #find chemical section
    lines_no_space = []
    for line in lines_clean:
        new_line = line.replace(' ','').strip()
        lines_no_space.append(new_line)
        
    for index,line in enumerate(lines_clean):
        if 'concentration' in line:
            chem_sect_start = index
            print('found concentration')
            break
        elif 'section 3' in str(line).lower():
            print('found sectino 3')
            chem_sect_start = index
            break
        else:
            continue
            
    #find first aid section
    for index,line in enumerate(lines_no_space):
        if 'firstaid' in line:
            chem_sect_end = index + 1
                 
    chemical_sect = lines_clean[chem_sect_start:chem_sect_end]
    
    
            
        
    #cut down to table beginning  
    for index,line in enumerate(chemical_sect):
        if 'concentration' in line:
            chem_table_beg = index
            break
        else:
            continue

    chemical_sect = chemical_sect[chem_table_beg:]

        
    ## page break check        
    has_pb = False
    for index, line in enumerate(chemical_sect):
        
        if re.search(r'(\s\d\s)/(\s\d\d)', line):
            print('page break present')
            i_pb = index
            has_pb = True
            print(index)
            print('\n')
            print(has_pb)
            break
        else:
            i_pb = 1000
            continue
        
     # find end of pg break section    
    for index, line in enumerate(chemical_sect):
        if 'sdseu / en / 0001' in line:
            i_pgbr_end = index
            print('end of page break found')
            break
        else:
            # print('continue')
            i_pgbr_end = 1000
            print('no page break?')
            continue
  
    no_page_break = False
    for i,c in enumerate(chemical_sect):
        if i_pb != 1000:
            if i == i_pb:
                chemical_sect[i] = 'page break'
            elif i > i_pb and i <= (i_pgbr_end):
                chemical_sect[i] = ''
            elif i > i_pgbr_end:
                break
        else:
            no_page_break = True
            continue
        
  
    if no_page_break == True:
        pdf_normal[file] = chemical_sect
        continue
        
        
    chemical_sect = [e for e in chemical_sect if len(e) != 0]
            
  
    for i,c in enumerate(chemical_sect):

        if 'page break' in c:
            print('page break found')
            pb_i = i
        elif 'for explanation' in c:
            print('has explanation')
            i_expl = i
        elif 'eastman is committed' in c:
            i_commit = i
            print('has committment')
    
    
    
    try:
        if (pb_i + 1) == i_expl:
            print('footer is next line')
            pdf_normal[file] = chemical_sect
        else:
            pdfs_weird[file] = chemical_sect
            
    except:
        if (pb_i + 1) == i_commit:
            print('footer is next line')
            pdf_normal[file] = chemical_sect
        else:
            pdfs_weird[file] = chemical_sect
        
    
# %%    
   

# %% Extraction
# %%% extracting normal formatted pdfs

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs')
normal_dfs = {}
for file, value in tqdm(pdf_normal.items()):
    
    test_tbls = tb.read_pdf(file , pages = "1-3", lattice = True, pandas_options={'header': None})
    
    
    
    
    if len(test_tbls) < 1:
        test_tbls = tb.read_pdf(file , pages = "4", lattice = True, pandas_options={'header': None})
        normal_dfs[file] = test_tbls
    else:
        normal_dfs[file] = test_tbls

#%%% load pickle from eastman folder
#%%%% load narmal_dfs       
       
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Eastman')
normal_dfs = pd.read_pickle(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\normal_dfs.pickle')
    
objects = []
with (open("normal_dfs.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
        




# %% DF SETS NORMAL


# %%% DF SET 0: splitting pdf's with no hazardous ingredients from main ext
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Eastman/pdfs/og_pdfs')
no_hazards = {}
df_set_0 = {}
these_are_zero = {}
for k, value in normal_dfs.items():
    print('working on: ' + k)
   
    if len(value) == 0:
        no_hazards[k] = value    
    else:
        ifile = open(k.replace('.pdf', '.txt'), encoding='utf-8')
        text = ifile.read()
    
    
        cleaned = text
        cleaned = cleanLine(text)
        cleaned = re.sub(' +', ' ', cleaned)
        try:
            hazards_present = cleaned.split("3.2 mixtures")[1].split("section 4:")[0]
        except:
            try:
                hazards_present = cleaned.split("3.1")[1].split("section 4:")[0]
            except:
                try:
                    hazards_present = cleaned.split("section 3.")[1].split("section 4:")[0]
                except:
                    try:
                        hazards_present = cleaned.split("section 3:")[1].split("section 4:")[0]
                    except:
                        print('idk')
                        # df_set_0[k] = value
        if "no hazardous ingredients" in hazards_present or "non-hazardous ingredients" in hazards_present:
            no_hazards[k] = value
        else:
            df_set_0[k] = value 
            
 # %%% DF SET 0.5: flatten list
#flatten and consolidate list of dataframes extracted from each pdf
####key = pdf file name + dataframe count
####value = dataframe value


df_set_0_5  = pd.DataFrame(columns = ['file and number', 'df'])
for k, value in df_set_0.items():
   
    intermediate = pd.DataFrame(columns = ['file and number', 'df'])
    c  = 0
        
    for df in value:
        
        
        if df.empty == False: 
           
            c += 1
            name ='Dataframe: ' + str(c)
            empty_status = "not empty"
            type_of_df = type(df)
            temporary = pd.DataFrame([{'file and number': k + ': ' + name, 'df': df}])
           
            intermediate = pd.concat([intermediate, temporary])
            
        else:    
            continue
        
        
    df_set_0_5 = pd.concat([df_set_0_5, intermediate])
        
 

df_set_0_5 = df_set_0_5.set_index('file and number').T.to_dict('list')    


# %%% DF SET 1: separate dataframes
#this will make a dictionary of file name and dateframe number as key and the dataframes as the value        
## aka flattens values from list of data frames to having dataframes as direct value
df_set_1 = {}

for k,value in df_set_0_5.items():
    new_value = []
    new_value = pd.concat(value)
   
    df_set_1[k] = new_value



# %%% DF SET 2: takes out tables with hazard info or tables that extracted the page number as a 1 by 1 matrix



take_out = {}
df_set_2 = {}
for k,value in df_set_1.items():
    
    print('working on ' + k)

    
    new_v = value.dropna(axis=1,how='all')
    new_v = new_v.dropna(axis=0,how='all')
    
    if new_v.empty:
        take_out[k] = new_v
        continue
        
    elif 'nan' in str(new_v.iat[0,0]):
        shifted_df = new_v.apply(lambda x: pd.Series(x.dropna().values), axis=1).fillna('')
        new_v = shifted_df
    
    
    find_letters = findchars(str(new_v.iat[0,0]))
   
    
    if new_v.shape[0] >= 1 and new_v.shape[1] >= 2:
        # print("has one or more columns and 2 or more columns")
        if 'Hazard' in str(new_v.iat[0,0]) and len(str(new_v.iat[0,1])) < 3:
           take_out[k] = new_v
           # print(len(str(new_v.iat[0,0])))
        elif "Source" in new_v.values:
            take_out[k] = new_v
            
            
        elif len(find_letters) == 0:
            take_out[k] = new_v
            
        else:
            df_set_2[k] = new_v
        
    else:
        take_out[k] = value
        # print(len(str(value.iat[0,0])))



# %%%% *TROUBLESHOOTING* DF SET 2
# testing the above code for errors
testing_mistakes = {}
testing_correct = {}
for k,value in take_out.items():
    new_v = value.dropna(axis=1,how='all')
    new_v = new_v.dropna(axis=0,how='all')
    
    if value.empty:
        testing_correct[k] = new_v
    elif ('Hazard' in str(value.iat[0,0])) or ("/" in str(value.iat[0,0]) and len(str(value.iat[0,0])) <= 7):
        testing_correct[k] = new_v
    else:
        testing_mistakes[k] = new_v
        
        
for k,value in testing_mistakes.items():
    if value.empty:
        continue
    elif 'SECTION' in str(value.iat[0,0]):
        continue
    else:
        print('###########################################')
        print('\n'+ '\n' + k)
        print(value.head())



# %%% DF SET 3: check for files not extracted
# check remaining dfs and concetante together into a new dataframe
# 1 key = combined dfs


###establishes a unique list of file names found in the main extraction method
df_set_2_keys = []
for k,value in df_set_2.items():
    new_k = k.split(':')[0].strip()
    df_set_2_keys.append(new_k)
    
df_set_2_keys= set(df_set_2_keys)

# =============================================================================
# finds values in the dictionary for each file name in list and 
# concatenates all of the remaining dataframes into one value 
# dictionary with one dataframe per file as the key
# =============================================================================

filtered_dict = {}
df_set_3 = {}
for j in tqdm(df_set_2_keys):
    combined_dfs = []
    filtered_dict = {}
    for k, value in df_set_2.items():
        if str(j) in k:
            filtered_dict[k] = value
    combined_dfs = pd.concat(filtered_dict.values(), ignore_index=True)
    df_set_3[j] = combined_dfs

# %%% DF SET 3.5
df_set_3_5 = {}
manual_ext= {}
for k, value in df_set_3.items():
   
    
    i = 0
    i_col_num = 0
    for name, values in value.items():
       
        values = value[name]
        column_list = value[name].to_list()
        searchable_string = ''.join(str(v) for v in column_list)
        num_check = str(searchable_string.replace("\r", "").strip())
        num_check2 = re.sub("[^\d-]", '', num_check).replace('-','')
        
        cas_check = cleanLine(num_check)
        if re.search(r'(\d+)-(\d\d)-(\d)',cas_check) or "proprietary" in cas_check or "not applicable" in cas_check or "not assigned" in cas_check or num_check2.isdigit():
            i_col_num += 1
            
        else:
            continue
    print(k + ' scanned')
    if i_col_num == 0:
        manual_ext[k] = value
    else:
        df_set_3_5[k] = value
    







 # %%% Pre DF SET 4
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Eastman/pdfs/og_pdfs')
fileList = glob("*.pdf")

fileList_test_4 = fileList[0:857]

df_set_4_test = {}
for file in fileList:
    k = file
    value = df_set_3_5.get(k)
    df_set_4_test[k] = value

df_set_4_test2 = {}
for k, value in df_set_4_test.items():
    NoneType = type(None)
    if isinstance(value, NoneType):
        continue
    else:
        df_set_4_test2[k] = value

        


# %%% DF SET 4: 
df_set_4  = {}
for k, value in df_set_4_test2.items():
    print("working on " + k)

    print(k + "\n" + str(value.iat[0,0]) + "\n")
    new_v = value.dropna(axis=1,how='all')
    new_v = new_v.dropna(axis=0,how='all')
    new_v.columns = range(new_v.columns.size)
    new_v.reset_index(inplace=True, drop=True)
    
    
    
    new_v_str = new_v.fillna('nan')
    
    if 'nan' in str(new_v_str.iat[0,0]):
        shifted_df = new_v.apply(lambda x: pd.Series(x.dropna().values), axis=1)#.fillna('')
        new_v = shifted_df
    elif 'Chemical' in str(new_v_str.iat[0,0]):
        shifted_df = new_v.apply(lambda x: pd.Series(x.dropna().values), axis=1)#.fillna('')
        new_v = shifted_df
    
    values = new_v.iloc[:,0]
    column_list = values.to_list()
    searchable_string = ''.join(str(v) for v in column_list)
    num_check = str(searchable_string.replace("\r", "").strip())
    
    
  
    try:
        for index, row in new_v.iterrows():
            row_testing = row.iloc[0]
            if 'Chemical name' not in row_testing:
                continue
            else:
                index_start = index
                break
    except:
        manual_ext[k] = value
        print(k + " special case")    
    try:
        for index, row in new_v.iterrows():
            print("working on row" + str(index))
            row_testing = row.iloc[0]
            # row_testing = cleanLine(row_testing)
            if 'Section 4' in str(row_testing):
                index_stop = index
                print(index_stop)
                # if 'nan' in index_stop:
                break
            else:
                continue
        try:
            print(index_stop)
            print('worked')
        except:
            print('didnt stop')
            index_stop = 'nan'
            
    except:
        #put in manual_ext group if error occurs
        manual_ext[k] = value
        
    print(index_stop)

    if 'nan' in str(index_stop):
        print('stop in nan')
        new_v = new_v.iloc[index_start:len(new_v)]
        new_v = new_v.dropna(axis=1,how='all')
        new_v = new_v.dropna(axis=0,how='all')
        new_v.columns = range(new_v.columns.size)
        new_v.reset_index(inplace=True, drop=True)
        
        
        
        
    else:
        new_v = new_v.iloc[index_start:index_stop]
        new_v = new_v.dropna(axis=1,how='all')
        new_v = new_v.dropna(axis=0,how='all')
        new_v.columns = range(new_v.columns.size)
        new_v.reset_index(inplace=True, drop=True)
    
 
    df_set_4[k] = new_v
 
# %%% DF SET 4.5:
df_set_4_5  = {}



pd.set_option('mode.chained_assignment', None)
for k, value in df_set_4.items():
    

    
   
    filtered = []
    for name, values in value.items():
        # name = 2
        # values = value[name]
        column_list = value[name].to_list()
        # print(column_list)
        searchable_string = ''.join(str(v) for v in column_list)
        cas_check = str(searchable_string.replace("\r", "").strip())
        if re.search(r'(\d+)-(\d\d)-(\d)',cas_check) or "proprietary" in cas_check or "not applicable" in cas_check or "Not Assigned" in cas_check:
            # print(name)
            cas_check_2 = values.replace("\r", "").str.strip()
            cas_check_2.fillna('nan', inplace=True)
            cas_check_2.reset_index(inplace=True, drop=True)
            filtered = [i for i, n in enumerate(cas_check_2) if re.search(r'(\d+)-(\d\d)-(\d)',n) or any(x in n for x in ("proprietary", "not applicable", "Not Assigned"))]
        else:
            continue
    value_filtered = value.loc[value.index[filtered]] #SHOULD BE IN LINE WITH INNER FOR LOOP
    
    if len(value_filtered)==0:
        index_list = []
        column_list = value.iloc[:,0].to_list()
        # print(column_list)
        for index, l in enumerate(column_list):
            if "No." in str(l) or "Chemical" in str(l):
                # print(l)
                continue
                # index_list.append(index
            else:
                index_list.append(index)
                
        value_filtered = value.loc[value.index[index_list]]
        
        
    value_filtered = value_filtered.reset_index(drop=True) #SHOULD BE IN LINE WITH INNER FOR LOOP
    value_filtered = value_filtered.replace(r'', np.NaN)
    value_filtered = value_filtered.replace(r'#', np.NaN)
    value_filtered = value_filtered.dropna(axis=1,how='all') #SHOULD BE IN LINE WITH INNER FOR LOOP
    
   
    for name, values in value_filtered.items():
        for i,j in enumerate(values):
            if re.search(r'\d+-\d\d-\d', str(j)):
                continue
            elif re.search(r'\d+-\d{3,5}-\d+', str(j)):
                value_filtered[name].iloc[i] = np.NaN
    value_filtered = value_filtered.dropna(axis = 1, how = 'all')
    value_filtered.reset_index(drop = True, inplace = True)
    vf_col_list = [x for x in range(value_filtered.shape[1])]
    value_filtered.columns = vf_col_list
    
  
    if value_filtered.shape[1] > 4:
        value_filtered = value_filtered.iloc[:,[0,1,2,3]]
        
    drop = []    
    for name, values in value_filtered.items():
        for i,j in enumerate(values):
            new_j = str(j).replace("\r\n", "").replace("\r", "").replace("\n", "");
            if re.search(r'H\d\d\d', new_j) or 'M-Factor' in new_j or 'mg' in new_j or 'ppm' in new_j:
                drop.append(name)
                break
    value_filtered = value_filtered.drop(drop, axis = 1)
    
    print(len(value_filtered.columns))
    if len(value_filtered.columns) >3:
        manual_ext[k] = value_filtered
        print('has issues')
    else:
        df_set_4_5[k] = value_filtered
        
     
        
    
# %%%

df_set_4_75 = {}
not_three = {}
for k,v in df_set_4_5.items():
   
    print('working on: ' + str(k))
    if len(v.columns) != 3:
        manual_ext[k] = v
        print('not three')
        continue
    
    
        
    
    for name, values in v.items():
        print('name' + str(name))
        print(type(name))
        for i,j in enumerate(values):
            j_clean = str(j).replace('\r','').replace('\n','')
            print(str(name) +': ' +str(j_clean))
            if re.search(r'\d+-\d\d-\d', str(j_clean)) or 'proprietary' in str(j_clean) or 'assigned' in str(j_clean) or 'applicable' in str(j_clean):
                cas_column = name
                
                break
            elif '<' in str(j_clean) or '>' in str(j_clean) or '=' in str(j_clean) or re.search(r'\d{2,3}', str(j_clean)):
                concentration_column = name
               
                break
            else:
                
                chem_column = name

                
    
    col_order = [chem_column, cas_column, concentration_column]
    value_filtered = v.loc[:,col_order]
          
    value_filtered = value_filtered.dropna(axis = 1, how = 'all')
    value_filtered.reset_index(drop = True, inplace = True)
    
    value_filtered.columns = ['raw_chem_name', 'raw_cas', 'centC']
         
    
    
    
    
    
    
    for i,j in enumerate(value_filtered['raw_cas']):
        if 'proprietary' in str(j).lower():
            value_filtered['raw_cas'].iloc[i] = 'proprietary'
        elif 'assigned' in str(j).lower():
            value_filtered['raw_cas'].iloc[i] = 'not assigned'
        elif 'applicable' in str(j).lower():
            value_filtered['raw_cas'].iloc[i] = 'applicable'
        elif re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            value_filtered['raw_cas'].iloc[i] = str(match)
            
            

        
    
    filtered_df = value_filtered
    
    filtered_df = filtered_df.replace('',np.nan)
    filtered_df = filtered_df.dropna(axis=1,how='all')
    filtered_df = filtered_df.dropna(axis=0,how='all')
  
    filtered_df = filtered_df.drop_duplicates(subset = 'raw_chem_name', keep='first')
    filtered_df.reset_index(inplace=True,drop=True)
    filtered_df = filtered_df[filtered_df.columns[0:3]]
    
  
        
        
    df_set_4_75[k] = filtered_df
 
# %%%% finding chem names for check
file = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs\eastar mn006 copolyester - natural.txt'
find_chem_names = {}
find_chem_names_v2 = {} 
for file in tqdm(fileList):
    ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    chemical_sect = cleaned.split('3.2 mixtures')[-1].split('first aid')[0]
    lines = chemical_sect.split('\n')
    
    
    
    lines_one = []
    characters_list = []
    for line in lines:
        if len(line) == 0:
            continue
        else:
            lines_one.append(line)
            
    lines_two = []
    for line in lines_one:
        # line = lines_one[5]
        line_list = line.strip().split(' ')
        for i,n in enumerate(line_list):
            if 'proprietary' in n or re.search(r'(\d+)-(\d\d)-(\d)',n) or 'not assigned' in n:
                 index_stop = i
                 print(index_stop)
                 break
            else:
                 index_stop = 100
        if index_stop != 100:
            n_new = line_list[0:index_stop]
            n_new = ' '.join(n_new)
            print(n_new)
            n_new = n_new.replace('cas-no. :','').replace(':','')
            if 'registration' in n_new:
                n_new = ''
        else:
            continue
        n_new = n_new.split(r'(\d\d\s)-(\s\d\d)|(\d\s)-(\s\d\d)')[0]
        n_new = n_new.split(r'(\d\d)|(\d)%')[0]
        lines_two.append(n_new)
        NoneType = type(None)
        lines_two = [x for x in lines_two if len(x) != 0]
    
    
        lines_three = []
        for l in lines_two:
            # lines_two[0]
            if '%' in l:
                print('yes')
                l_n = re.split(r'(\d\d\s)-(\s\d\d)%', l)[0].strip()
                lines_three.append(l_n)
            elif 'chemical name' in l or 'index' in l:
                continue
            else:
                lines_three.append(l)
        
    find_chem_names_v2[file] = lines_two    
    find_chem_names[file] = lines_three
    
is_zero = {}
for k,v in find_chem_names.items():
    if len(v) == 0:
        is_zero[k] = v
        
idk = {}        
for k,v in is_zero.items():
    value = df_set_4_5.get(k)
    idk[k] = value



# %%% DF SET 5
df_set_5  = {}
df_set_5_sc = {}
for k, value in df_set_4_75.items():
   
    
    
    new_value = value.dropna(subset=['raw_cas'])
    
    for name, v in new_value.items():
     print(v)
     for c in v:
         print(c)
         print(type(c))
         
         if re.search(r'(\d+)-(\d\d)-(\d)', str(c).lower()) or 'proprietary' in str(c).lower() or 'not applicable' in str(c).lower() or 'not assigned' in str(c).lower():
             cas_column = name
             break
         elif 'nan' in str(c).lower():
             continue
         elif re.search(r'[A-Za-z]', str(c)):
             chem_name_column = name
             break
         elif '%' in  str(c) or '>' in  str(c) or '<' in  str(c) or '100' in str(c) or re.search(r'\d+\s-\s+\d+', str(c)) or re.search(r'\s+\d+', str(c)):
             cent_c_column = name
             break
         

        
        
   
    new_value = value.loc[:, [chem_name_column, cas_column, cent_c_column]]
    new_value.columns = ['raw_chem_name', 'raw_cas', 'concentration']
    
    print(new_value['raw_cas'].iloc[:2])
    print('last assignment worked')
    df_set_5[k] = new_value
    


# %%% DF SET 6


df_set_6 = {}
no_cas = {}
for k, value in df_set_5.items():

    
    new_value = value
    new_value = new_value.dropna(subset=['raw_cas'], how='any')
    new_value.loc[new_value['raw_cas'].str.contains('\r'), 'raw_cas'] = new_value['raw_cas'].str.replace('\r', '')

    
    new_value['raw_cas'] = new_value['raw_cas'].replace(r'\r','')
    print(value['raw_cas'])
    

    for i, j in enumerate(new_value['raw_cas']):
        print(j)
        if 'proprietary' in str(j) or 'applicable' in str(j) or 'assigned' in str(j).lower():
            if 'applicable' in str(j).lower():
                new_value['raw_cas'].iloc[i] = 'not applicable'
            elif 'assigned' in str(j).lower():
                new_value['raw_cas'].iloc[i] = 'not assigned'

        
        elif re.search(r'\d+-\d\d-\d', str(j)):
                    cas_match = re.findall(r'(^\d{2,7}-\d\d-\d|\s\d{2,7}-\d\d-\d)', j)
                    new_value['raw_cas'].iloc[i] = cas_match[0]
    for i,j in enumerate(new_value['raw_cas']):
        
        new_value['raw_cas'].iloc[i] = j.lower().replace('cas-no.:', '').strip()
        
    for i,j in enumerate(new_value['raw_cas']):
        if re.search(r'\d+-\d\d\d-\d', str(j)):
            new_value['raw_cas'].iloc[i] = np.NaN
        else:
            continue
        
    new_value['rank'] = np.NaN
    
    
    num = 0
    for i,j in enumerate(new_value['raw_cas']):
        if 'nan' in str(j).lower():
            continue
        else:
            num += 1
            new_value['rank'].iloc[i] = str(num)
   
                
    df_set_6[k] = new_value


# %%%
df_set_final = {}

for k,v in df_set_6.items():
    for i,j in enumerate(v['raw_chem_name']):
        if 'nan' in str(j):
            manual_ext[k] = v
            break
        
        
for k,v in df_set_6.items():
    
    results = manual_ext.get(k)
    print(str(k) + ': '+str(results))
    
    if str(results) == 'None':
        df_set_final[k] = v
    else:
        continue
    



# %%%Concentration cleaning
# %%%%splitting between centc and range

df_set_concentration_cleaned = {}

for k,value in df_set_final.items():
    print(k)
    new_value = value
    new_value['minC'] = np.NaN
    new_value['maxC'] = np.NaN
    for i,j in enumerate(new_value['concentration']):
        if '-' in str(j):
            new_value['minC'].iloc[i] = str(j).split('-')[0].replace('%','').strip()
            new_value['maxC'].iloc[i] = str(j).split('-')[-1].replace('%','').strip()
            new_value['concentration'].iloc[i] = np.NaN

        else:
            new_value['concentration'].iloc[i] = str(j).replace('%','').strip()

    
    df_set_concentration_cleaned[k] = new_value


# %%Final extraction    
# %%% W/ Hazardous Chemicals: extracting all data together


dfs = []
something_wrong = {}
for k, value in df_set_concentration_cleaned.items():
    print('#############')
    print(k)
    print('\n')
    
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    id = ''
    unit = ''
    component = ''
    
    
    
    #set up lists for document data
    
    idList = [] #list of product IDs
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    unitList = []
    
###Getting all of the document info
   #Get factotum document ids    
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\Factotum_Eastman_Products_documents_20230802 (1).csv"))
    for row in template:
        if row[6] ==k:
            id = row[0]
            print(id)
    
            
    #open txt file and clean text
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs')
    ifile = open(k.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(file) 
    
    #get prod name
    # prod_sect = cleaned.split('section 1. identification',1)[-1].split('1.2 relevant', 1)[0].split('\n')
    
    lines = cleaned.split('\n')
    lines = [j for i,j in enumerate(lines) if len(j)>0]
    
    for i,l in enumerate(lines):
        # print(l)
        if 'section 1' in l:
            start_index = i
            # print('start index found')
            # print('start index: ' + str(start_index))
            break
        elif '1. identif' in l:
            start_index = i
            # print('start index found')
            # print('start index: ' + str(start_index))
            break
        else:
            continue
    
    for i, l in enumerate(lines):
        if 'product name' in l:
            print(len(l))
            if len(l) < 15:
                stop_index = i + 1
                # print('stop index found')
                # print('stop index: ' + str(stop_index))
            else:
                stop_index = i
                # print('stop index found')
                # print('stop index: ' + str(stop_index))
            break
        elif 'product no.' in l:
            stop_index = i
            # print('stop index found')
            # print('stop index: ' + str(stop_index))
            # print(stop_index)
            break
        
        elif 'product code' in l:
            stop_index = i
            # print('stop index found')
            # print('stop index: ' + str(stop_index))
            # print(stop_index)
            break
        else:
            continue
        
    lines = lines[start_index:(stop_index+1)]
    

    for l in lines:
        print(l)
        if 'identification' in l:
            continue
        elif 'name' in l:
            if ':' in l:
                prodname = l.split(':', 1)[-1].strip()
                break
            elif len(l) > 11:
                prodname = l.split(' ', 2)[-1].strip()
                
            else:
                continue
        elif ':' in l:
            prodname = l.split(':', 1)[-1].strip()
            break
                
        else:
            continue
        
        
    print(prodname)
            
    
    
    
   
        
    
    
    
    #get category/recommended uses
    
    if 'recommended use of the chemical and restrictions on use' in cleaned:
        cat = cleaned.split('recommended use of the chemical and restrictions on use', 1)[-1].split('restrictions on use',1)[0].split(':', 1)[-1].strip().split('\n', 1)[0]
    elif 'relevant identified uses of the substance or mixture' in cleaned:
        cat_sect = cleaned.split('relevant identified uses of the substance or mixture', 1)[-1].split('details of the supplier')[0].split('\n')
    
    
    cat_sect2 = []
    for c in cat_sect:
        if len(c) == 0:
            continue
        else:
            cat_sect2.append(c)
    cat_sect2 = cat_sect2[1] 
    
    if ':' in cat_sect2:
        cat = cat_sect2.split(':',1)[-1].strip()
    else:   
        cat = cat_sect2.split(' ')
        cat_filtered = []
        for c in cat:
            if 'recommended' in c or 'use' in c or '1.3' in c:
                continue
            elif len(c) == 0:
                continue
            else:
                cat_filtered.append(c)
            
        if len(cat_filtered) == 1:
            cat = cat_filtered[0].strip()
        elif len(cat_filtered) < 1:
            cat = ''
            something_wrong[k] = cat_sect
        else:
            cat = ' '.join(cat_filtered)
            
    cat = cat.replace(':','').replace('.','').strip()

            
            
            
        

    
    #get version
    rev_sect = cleaned.split('version', 1)[-1].split('section 1', 1)[0]
    rev_lines = rev_sect.split('\n')
    rev_lines = [j for j in rev_lines if len(j) > 0]
    
    rev_assigned = False
    for i,r in enumerate(rev_lines):
        if 'preparation' in r:
            if i < 3:
                rev = r.split('revision number')[-1].strip()
                rev_assigned = True
                break
            else:
                continue
        
        else:    
            continue
        
    
    if rev_assigned == False:
        rev = rev_lines[0].replace(':','').strip()
    
    if len(rev) > 4:
        rev = rev_lines[1].split(' ', 1)[0].strip()
    
    
    os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs/copied (_edited) pdfs')
    #get product name
    
    
    lines = cleaned.split('\n')
    lines_cl = []
    for line in lines:
        if len(line) == 0:
            continue
        else:
            lines_cl.append(line)
    
    # get date
    lines_date = []
    for line in lines_cl:
        if 'date' in line:
            lines_date.append(line) 
    
    dates = []
    for line in lines_date:
        if re.search(r'\d\d\.\d\d\.\d\d\d\d', line):
            date_match = re.findall(r'\d\d\.\d\d\.\d\d\d\d', line)
        elif re.search(r'\d\d/\d\d/\d\d\d\d', line):
            date_match = re.findall(r'\d\d/\d\d/\d\d\d\d', line)

        
        # print(date_match)
        
        if len(date_match) == 0:
            continue
        else:
            for d in date_match:
                dates.append(d)
            
            
            # dates.append(date_match)
    dates = list(set(dates))
    
    
  
    
    
    
    dates = pd.DataFrame(dates)
    dates.columns = ['raw_date']
    dates['year'] = np.NaN
    dates['month'] = np.NaN
    dates['day'] = np.NaN
    if len(dates) == 1:
        rev_date = str(dates.iat[0,0])
    else:      
        for i,d in enumerate(dates['raw_date']):
            
            if re.search(r'\d\d\.\d\d\.\d\d\d\d', d):
                year_match = re.findall(r'\.\d\d\d\d', d)[0].replace('.','')
                month_match = re.findall(r'\.\d\d\.', d)[0].replace('.','')
                day_match = re.findall(r'^\d\d',d)[0]
                dates['year'].iloc[i] = year_match
                dates['month'].iloc[i] = month_match
                dates['day'].iloc[i] = day_match
                

            
            elif re.search(r'\d\d/\d\d/\d\d\d\d', d):
                year_match = re.findall(r'/\d\d\d\d', d)[0].replace('/','')
                month_match = re.findall(r'/\d\d/', d)[0].replace('/','')
                day_match = re.findall(r'^\d\d',d)[0]
                dates['year'].iloc[i] = year_match
                dates['month'].iloc[i] = month_match
                dates['day'].iloc[i] = day_match

            
            
        mx_yr = int(max(dates['year']))
        mx_mn = int(max(dates['month']))
        mx_day = int(max(dates['day']))
        dates_max_year = [i for i,j in enumerate(dates['year']) if int(j)==mx_yr]
        dates = dates.iloc[dates_max_year]
      
                

        
        if len(dates) > 1:
            dates_max_month = [i for i,j in enumerate(dates['month']) if int(j)==mx_mn]
            dates = dates.iloc[dates_max_month]
            if len(dates)>1:
                dates_max_day = [i for i,j in enumerate(dates['day']) if int(j)==mx_day]
                dates = dates.iloc[dates_max_day]
            elif len(dates)==0:
                print('something just went wrong')
            else:
                rev_date = str(dates.iat[0,0])

            
            
        else:
            dates_max_year = dates_max_year[0] 
            rev_date = str(dates.iat[0,0])
            
        if len(dates) == 1:
            rev_date = str(dates.iat[0,0])
            
     #fill in repeated info
    n = len(value)
    idList.extend([id]*n)
    filenameList.extend([k]*n)
    prodnameList.extend([prodname]*n)
    dateList.extend([rev_date]*n)
    revList.extend([rev]*n)
    catList.extend([cat]*n)
    
    #create rank and append new df to list of dfs
    df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas': value['raw_cas'], 'raw_chem_name':value['raw_chem_name'],'raw_central_comp':value['concentration'], 'raw_min_comp': value['minC'], 'raw_max_comp': value['maxC'], 'rank': value['rank']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
    df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'raw_min_comp': df['raw_min_comp'], 'raw_max_comp': df['raw_max_comp'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
    dfs.append(df)

# %%% W/O Hazardous Chemicals: extracting all data together


for n in pdfs_no_hazards:
    print('#############')
    print(n)
    print('\n')
    
    
    # n = pdfs_no_hazards[0]
    
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    id = ''
    unit = ''
    component = ''
    min_C = np.NaN
    max_C = np.NaN
    rank = np.NaN
    raw_chem_name = np.NaN
    raw_cas = np.NaN
    centC = np.NaN
    
    
    #set up lists for document data
    
    idList = [] #list of product IDs
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    unitList = []
    min_cList = []
    max_cList = []
    raw_chem_nameList = []
    raw_casList = []
    centCList = []
    
    
###Getting all of the document info
   #Get factotum document ids    
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\Factotum_Eastman_Products_documents_20230802 (1).csv"))
    for row in template:
        if row[6] ==n:
            id = row[0]
            print(id)
    
            
    #open txt file and clean text
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs')
    ifile = open(n.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(n) 
    
    #get prod name

    
    lines = cleaned.split('\n')
    lines = [j for i,j in enumerate(lines) if len(j)>0]
    
    for i,l in enumerate(lines):
        # print(l)
        if 'section 1' in l:
            start_index = i
            # print('start index found')
            # print('start index: ' + str(start_index))
            break
        elif '1. identif' in l:
            start_index = i
            # print('start index found')
            # print('start index: ' + str(start_index))
            break
        else:
            continue
    
    for i, l in enumerate(lines):
        if 'product name' in l:
            print(len(l))
            if len(l) < 15:
                stop_index = i + 1
                # print('stop index found')
                # print('stop index: ' + str(stop_index))
            else:
                stop_index = i
                # print('stop index found')
                # print('stop index: ' + str(stop_index))
            break
        elif 'product no.' in l:
            stop_index = i
            # print('stop index found')
            # print('stop index: ' + str(stop_index))
            # print(stop_index)
            break
        
        elif 'product code' in l:
            stop_index = i
            # print('stop index found')
            # print('stop index: ' + str(stop_index))
            # print(stop_index)
            break
        else:
            continue
        
    lines = lines[start_index:(stop_index+1)]
    

    for l in lines:
        print(l)
        if 'identification' in l:
            continue
        elif 'name' in l:
            if ':' in l:
                prodname = l.split(':', 1)[-1].strip()
                break
            elif len(l) > 11:
                prodname = l.split(' ', 2)[-1].strip()
                
            else:
                continue
        elif ':' in l:
            prodname = l.split(':', 1)[-1].strip()
            break
                
        else:
            continue
        
        
    print(prodname)
            
    
    
    
   
        
    
    
    
    #get category/recommended uses
    
    if 'recommended use of the chemical and restrictions on use' in cleaned:
        cat = cleaned.split('recommended use of the chemical and restrictions on use', 1)[-1].split('restrictions on use',1)[0].split(':', 1)[-1].strip().split('\n', 1)[0]
    elif 'relevant identified uses of the substance or mixture' in cleaned:
        cat_sect = cleaned.split('relevant identified uses of the substance or mixture', 1)[-1].split('details of the supplier')[0].split('\n')
    
    
    cat_sect2 = []
    for c in cat_sect:
        if len(c) == 0:
            continue
        else:
            cat_sect2.append(c)
    cat_sect2 = cat_sect2[1] 
    
    if ':' in cat_sect2:
        cat = cat_sect2.split(':',1)[-1].strip()
    else:   
        cat = cat_sect2.split(' ')
        cat_filtered = []
        for c in cat:
            if 'recommended' in c or 'use' in c or '1.3' in c:
                continue
            elif len(c) == 0:
                continue
            else:
                cat_filtered.append(c)
            
        if len(cat_filtered) == 1:
            cat = cat_filtered[0].strip()
        elif len(cat_filtered) < 1:
            cat = ''
            something_wrong[k] = cat_sect
        else:
            cat = ' '.join(cat_filtered)
            
    cat = cat.replace(':','').replace('.','').strip()

            
            
            
        
    
    #get version
    rev_sect = cleaned.split('version', 1)[-1].split('section 1', 1)[0]
    rev_lines = rev_sect.split('\n')
    rev_lines = [j for j in rev_lines if len(j) > 0]
    
    rev_assigned = False
    for i,r in enumerate(rev_lines):
        if 'preparation' in r:
            if i < 3:
                rev = r.split('revision number')[-1].strip()
                rev_assigned = True
                break
            else:
                continue
        
        else:    
            continue
        
    
    if rev_assigned == False:
        rev = rev_lines[0].replace(':','').strip()
    
    if len(rev) > 4:
        rev = rev_lines[1].split(' ', 1)[0].strip()
    
    
    os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs/copied (_edited) pdfs')
    #get product name
    
    
    lines = cleaned.split('\n')
    lines_cl = []
    for line in lines:
        if len(line) == 0:
            continue
        else:
            lines_cl.append(line)
    
    # get date
    lines_date = []
    for line in lines_cl:
        if 'date' in line:
            lines_date.append(line) 
    
    dates = []
    for line in lines_date:
        if re.search(r'\d\d\.\d\d\.\d\d\d\d', line):
            date_match = re.findall(r'\d\d\.\d\d\.\d\d\d\d', line)
        elif re.search(r'\d\d/\d\d/\d\d\d\d', line):
            date_match = re.findall(r'\d\d/\d\d/\d\d\d\d', line)

        
        # print(date_match)
        
        if len(date_match) == 0:
            continue
        else:
            for d in date_match:
                dates.append(d)
            
            
            # dates.append(date_match)
    dates = list(set(dates))
    
    
  
    dates = pd.DataFrame(dates)
    dates.columns = ['raw_date']
    dates['year'] = np.NaN
    dates['month'] = np.NaN
    dates['day'] = np.NaN
    if len(dates) == 1:
        rev_date = str(dates.iat[0,0])
    else:      
        for i,d in enumerate(dates['raw_date']):
            # print(i)
            # print(d)

            if re.search(r'\d\d\.\d\d\.\d\d\d\d', d):
                # print('w/ period')
                year_match = re.findall(r'\.\d\d\d\d', d)[0].replace('.','')
                month_match = re.findall(r'\.\d\d\.', d)[0].replace('.','')
                day_match = re.findall(r'^\d\d',d)[0]
                dates['year'].iloc[i] = year_match
                dates['month'].iloc[i] = month_match
                dates['day'].iloc[i] = day_match
                

            
            elif re.search(r'\d\d/\d\d/\d\d\d\d', d):
                # print('w/ back slash')
                year_match = re.findall(r'/\d\d\d\d', d)[0].replace('/','')
                month_match = re.findall(r'/\d\d/', d)[0].replace('/','')
                day_match = re.findall(r'^\d\d',d)[0]
                dates['year'].iloc[i] = year_match
                dates['month'].iloc[i] = month_match
                dates['day'].iloc[i] = day_match

            
            
        mx_yr = int(max(dates['year']))
        mx_mn = int(max(dates['month']))
        mx_day = int(max(dates['day']))
        dates_max_year = [i for i,j in enumerate(dates['year']) if int(j)==mx_yr]
        dates = dates.iloc[dates_max_year]
      
                

        
        if len(dates) > 1:
            dates_max_month = [i for i,j in enumerate(dates['month']) if int(j)==mx_mn]
            dates = dates.iloc[dates_max_month]
            if len(dates)>1:
                dates_max_day = [i for i,j in enumerate(dates['day']) if int(j)==mx_day]
                dates = dates.iloc[dates_max_day]
            elif len(dates)==0:
                print('something just went wrong')
            else:
                rev_date = str(dates.iat[0,0])

            
            
        else:
            dates_max_year = dates_max_year[0] 
            rev_date = str(dates.iat[0,0])
            
        if len(dates) == 1:
            rev_date = str(dates.iat[0,0])
            
    
    
            
     #fill in repeated info
    num = len(value)
    idList.extend([id]*num)
    filenameList.extend([n]*num)
    prodnameList.extend([prodname]*num)
    dateList.extend([rev_date]*num)
    revList.extend([rev]*num)
    catList.extend([cat]*num)
    min_cList.extend([min_C]*num)
    max_cList.extend([max_C]*num)
    raw_chem_nameList.extend([raw_chem_name]*num)
    raw_casList.extend([raw_cas]*num)
    centCList.extend([centC]*num)
    
    #create rank and append new df to list of dfs
    df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas': raw_casList, 'raw_chem_name': raw_chem_nameList,'raw_central_comp':centCList, 'raw_min_comp': min_cList, 'raw_max_comp': max_cList}) 
    df['rank'] = ''
    df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'raw_min_comp': df['raw_min_comp'], 'raw_max_comp': df['raw_max_comp'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
    dfs.append(df)
    
#%%% final combining and extraction    
extracted_dfs=pd.concat(dfs, axis=0, ignore_index=True)

        
extracted_dfs = extracted_dfs.replace('nan', np.NaN)
extracted_dfs = extracted_dfs.replace('', np.NaN)

    
# %% to csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\ext_csv")
extracted_dfs.to_csv('eastman_ext.csv', index=False)



