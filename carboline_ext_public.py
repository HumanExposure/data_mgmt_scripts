# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 17:02:35 2023
@author: CLUTZ01
"""


import os, string, csv, re
import camelot
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from glob import glob
from pikepdf import Pdf
from tqdm import tqdm



# %% def pdftotxt
def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64' #Path to execfile
    for file in tqdm(files):
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return


# %% cleanline
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


# %% findsection 
def startnstop(x, string_one, string_two):
    
    lis = x


    for i,j in enumerate(lis):
        if re.search(string_one, str(j)):
            start_found = i
        
    for i,j in enumerate(lis):
        if re.search(string_two,str(j)):
            end_found = i

    if 'start_found' not in locals():
        print("start not found")
        return
    if 'end_found' not in locals():
        print("end not found")
        return
    new_list = lis[start_found:(end_found+1)]
    return new_list



# %% data set up
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Carboline\pdfs')
pdfs = glob('*.pdf')

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Carboline\txt files')
txt_files = glob('*.txt')


# %% ext data
def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    
    global minList
    
    
    
    dfs = {}
    no_hazards = {}
    no_hazards_ls = []
    unusuals = []
    for file in tqdm(fileList):


        idList = [] #list of product IDs
        filenameList = [] #list of file names matching those in the extacted text template
        prodnameList = [] #list of product names
        dateList = [] #list of msdsDates
        revList = [] #list of revision numbers
        catList = [] #list of product categories
        casList = [] #list of CAS numbers
        chemList = [] #list of chemical names
        useList = [] #list of functional uses of each chemical
        unitList = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...)
        rankList = [] #list of ingredient ranks
        centList = [] #list of central concentrations
        componentList = [] #List of components




        os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Carboline\txt files')
   

        ifile = open(file)
        text = ifile.read()
       
        global cas, centC, df, lines, prodname
        
        cleaned = text
        cleaned = cleanLine(text)
        cleaned = re.sub(' +', ' ', cleaned)
        # re.sub(' +', ' ', cleaned)
        
        
        
        lines = cleaned.split('\n')
        lines = [line for line in cleaned.split('\n') if len(line)>0]
        
        if cleaned == '' or 'typical mixing instructions' in cleaned: 
            print(str(file)+' is empty')
            unusuals.append(file)
            continue
        
        
       
        
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        component = []
        chem = []
        cas = []
        concentration = []
        unit = []
        
        
        
                                    
        template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Carboline\carboline_doc_records.csv")) #Get factotum document ids
        for row in template:
            if row[6] == file.replace('.txt', '.pdf'):
                ID = row[0]
                break
        # if ID == '':
        #     continue
        

        prodname = cleaned.split('product name:')[-1].split('\n')[0].strip().replace('®', '').replace('â','') #get product name
        prodname = re.sub(' +', ' ', prodname) #get rid of extra spaces
        prodname = prodname.split('supercedes', maxsplit=1)[0]
        date = cleaned.split('revision date:')[-1].strip(': ').split(' ')[0].strip() #get date
        


        cat_key_phrases = ['relevant identified uses of the','substance or mixture and uses','advised against']
        take_out_pat = '|'.join(cat_key_phrases)
        for i,j in enumerate(lines):
           
            if re.search(r'product use/class|^\s{0,2}relevant identified uses|[0-9.]{0,3}\s{0,2}relevant identified uses', str(j)):
                if re.search(r'^\s{0,2}relevant identified uses|[0-9.]{0,3}\s{0,2}relevant identified uses', str(j)):
                    # print(str(j))
                    # print('found')
                    cat_section = lines[(i):(i+3)]
                    # print(cat_section)
                    cat_section = [re.sub(take_out_pat, '', x).strip() for x in cat_section]
                    cat = ' '.join(cat_section)

                elif re.search(r'product use/class', str(j)):
                    cat = str(j).split(':',1)[-1].strip()

                else:
                    print('another variation')
                    break


            else:
                continue
        
        if cat == '':
            print('###########' + '\n' + file + '\n'+ 'no cat')
        elif re.search(r'^\d\.\d\s', str(cat)):
            cat = re.sub(r'^\d\.\d\s', '',str(cat))

        # COMPOSITION
        try:
            composition = startnstop(lines, r'3\.\scomposition|section 2 - composition', r'4\.\sfirst-aid| section 3 - hazards identification')
        except:
            unusual.append(file)
            continue

        comp_df = pd.DataFrame(composition, columns = ['raw_chem_name'])
        
        comp_df['raw_cas'] = np.NaN
        comp_df['concentration'] = np.NaN
        first_cas_found = False
        end = False
        drop_index = []
        no_hazard = False
        any_chemicals = True
        for i,j in enumerate(comp_df['raw_chem_name']):
            working_x = str(j)
            if 'no hazard' in str(j):
                no_hazards_ls.append(file)
                no_hazard = True
                break
            #check if splling into next table
            if end == True:
                
                if first_cas_found == True:
                    drop_index.append(i)
                    continue
                else:
                    
                    if no_hazard == False:
                        no_hazards_ls.append(file)
                        no_hazard = True

                        

            #check for and drop hazard codes
            if re.search(r'\sh\d{1,3}', working_x):
                working_x = re.split(r'\sh\d{1,3}', working_x, maxsplit=1)[0]

            if re.search(r'\s\d\d\d-\d\d\d-\d\s', working_x):
                working_x = re.sub(r'\s\d\d\d-\d\d\d-\d\s', '', working_x)
            #where proprietary is found
            if 'propriet' in working_x: 
                comp_df['raw_cas'].iloc[i] = 'proprietary'

                if re.search(r'^propriet', working_x):
                    split_by_cas = re.split(r'\s(?=[0-9<>=]\.)', working_x, maxsplit=1)
                    comp_df['concentration'].iloc[i] = split_by_cas[-1]
                    comp_df['raw_chem_name'].iloc[i] = re.sub(r'propriet|proprietary', '', split_by_cas[0])

                else:
                    comp_df['concentration'].iloc[i] = working_x.split('propriet', maxsplit=1)[-1]
                    comp_df['raw_chem_name'].iloc[i] = working_x.split('propriet', maxsplit=1)[0]
                    if first_cas_found == False:
                        first_cas_found = True
                        continue
                    else:
                        continue
            
            #where trade secret is found
            if 'trade' in working_x:
                comp_df['raw_cas'].iloc[i] = 'trade secret'
                
                if re.search(r'^trade', working_x):
                    split_by_cas = re.split(r'\s(?=[0-9<>=\.])', working_x, maxsplit=1)
                    comp_df['concentration'].iloc[i] = split_by_cas[-1]
                    comp_df['raw_chem_name'].iloc[i] = re.sub(r'trade|secret|trade secret', '', split_by_cas[0])

                else:
                    comp_df['concentration'].iloc[i] = working_x.split('trade', maxsplit=1)[-1]
                    comp_df['raw_chem_name'].iloc[i] = working_x.split('trade', maxsplit=1)[0]
                if first_cas_found == False:
                    first_cas_found = True
                    continue
                else:
                    continue

 
            if re.search(r'\d+-\d\d-\d', working_x) and end == False:
                
                #cas first
                if re.search(r'^\s{0,3}\d+-\d\d-\d', working_x):
                    comp_df['raw_cas'].iloc[i] = re.findall(r'\d+-\d\d-\d', str(j))[0]
                    
                    split_by_cas = re.split(r'\s(?=[0-9<>=])', working_x, maxsplit=1)
                    comp_df['concentration'].iloc[i] = split_by_cas[-1]
                    comp_df['raw_chem_name'].iloc[i] = re.sub(r'\d+-\d\d-\d', '', split_by_cas[0])
                else:                    
                    comp_df['raw_cas'].iloc[i] = re.findall(r'\d+-\d\d-\d', str(j))[0]
                    split_by_cas = re.split(r'\d+-\d\d-\d', working_x, maxsplit=1)
                    comp_df['raw_chem_name'].iloc[i] = split_by_cas[0]
                    comp_df['concentration'].iloc[i] = split_by_cas[-1]
                
                if first_cas_found == False:    
                    first_cas_found = True
                else:
                    continue

            else:

                if re.search(r'\d\d\d-\d\d\d', working_x):
                    split = re.split(r'\d\d\d-\d\d\d', working_x, maxsplit=1)
                    comp_df['raw_chem_name'].iloc[i] =split[0]
            
            if 'm-factor' in str(j) or 'section 3 - hazards identification' in str(j):
                end = True
                drop_index.append(i)
            if first_cas_found == False:
                drop_index.append(i)
          
            if i == (len(comp_df)-1) and first_cas_found == False:
                no_hazards_ls.append(file)
                no_hazard = True

        if no_hazard == True:


            n = 1
            idList.extend([ID]*n)
            filenameList.extend([file.replace('.txt','.pdf')]*n)
            prodnameList.extend([prodname]*n)
            dateList.extend([date]*n)
            revList.extend([rev]*n)
            useList.extend([cat]*n)
            unitList.extend([unit]*n)
            catList.extend(['']*n)
            
            df = pd.DataFrame({'data_document_id':idList, 
                            'data_document_filename':filenameList, 
                            'prod_name':prodnameList, 
                            'doc_date':dateList, 
                            'rev_num':revList, 
                            'raw_category':'', 
                            'raw_cas':[''], 
                            'raw_chem_name':[''], 
                            'raw_min_comp': [''],
                            'raw_max_comp': [''],
                            'report_funcuse':useList, 
                            'unit_type':[''], 
                            'ingredient_rank':[''],
                            'raw_central_comp':['']})
            

            no_hazards[file] = df
            continue
            

        comp_df.drop(comp_df.index[drop_index], inplace = True)
        comp_df['raw_cas'] = comp_df['raw_cas'].ffill()
        comp_df['concentration'] = comp_df['concentration'].ffill()
        comp_df = comp_df.groupby(['raw_cas', 'concentration'], sort=False, as_index=False)['raw_chem_name'].apply(' '.join)
        
        comp_df = comp_df.loc[:,['raw_chem_name', 'raw_cas', 'concentration']]

        unit = 3

        n = len(comp_df)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        useList.extend([cat]*n)
        unitList.extend([unit]*n)
        catList.extend(['']*n)
        

        comp_df['minc'] = np.NaN
        comp_df['maxc'] = np.NaN

        for i,j in enumerate(comp_df['concentration']):
            

            working_c = str(j)
            working_c = re.sub(r'[a-zA-Z]','', working_c)

            if len(working_c.split(' ')) >= 4:
                c_split = re.split(' ', working_c)[-3:]
                working_c = ' '.join(c_split)


            if '-' in working_c:
                split_c = working_c.split('-', maxsplit=1)
                comp_df['minc'].iloc[i] = split_c[0]
                comp_df['maxc'].iloc[i] = split_c[1]
                comp_df['concentration'].iloc[i] = np.NaN
            else:
                continue

        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))


        df = pd.DataFrame({'data_document_id':idList, 
                           'data_document_filename':filenameList, 
                           'prod_name':prodnameList, 
                           'doc_date':dateList, 
                           'rev_num':revList, 
                           'raw_category':catList, 
                           'raw_cas':comp_df['raw_cas'], 
                           'raw_chem_name':comp_df['raw_chem_name'], 
                           'raw_min_comp': comp_df['minc'],
                           'raw_max_comp': comp_df['maxc'],
                           'report_funcuse':useList, 
                           'unit_type':unitList, 
                           'ingredient_rank':rankList,
                           'raw_central_comp':comp_df['concentration']})
                           
        

        dfs[file] = df




    return dfs, no_hazards, unusuals


# %%

all_the_data, no_hazard_files, unusuals = extractData(txt_files)


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\Carboline')
ext_df.to_csv('ext_df.csv')





# %% CLEANING



haz_keywords = [' chronic',' irrit',' eye irrit',' flam',' skin',' liq',' tox', '\s-\d\d\d', ' stot', ' carc', ' aquatic', ' acute']
pat = '|'.join(haz_keywords)
print(pat)


ext_df = pd.concat(all_the_data.values(), ignore_index=True)
ext_df_nh = pd.concat(no_hazard_files.values(), ignore_index=True)




# %% NO HAZARDS CLEANING

for i,j in enumerate(ext_df_nh['prod_name']):
    if 'revision' in str(j):
        new = str(j).split('revision', maxsplit=1)[0]
        ext_df_nh['prod_name'].iloc[i] = new

ext_df_nh.to_csv('ext_df_nh.csv')

# %%
for i,j in enumerate(ext_df['raw_chem_name']):
    cleaned_value = str(j)
    if 'page' in str(j):
        cleaned_value = str(j).split('page', maxsplit=1)[0]
    for y in haz_keywords:
        if str(y) in cleaned_value:
            matches = re.findall(pat, cleaned_value)
            matched = matches[0]
            cleaned_value_split = cleaned_value.split(str(matched), maxsplit=1)
            cleaned_value = cleaned_value_split[0]
            break

    ext_df['raw_chem_name'].iloc[i] = cleaned_value


# %% no hazards
ext_df.to_csv('ext_df_v3.csv')
