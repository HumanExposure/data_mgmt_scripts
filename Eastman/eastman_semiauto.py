# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 17:55:00 2023

@author: CLUTZ01
"""

# %% imports

import os, string, csv, re, shutil
import pandas as pd
import numpy as np

import sys
from glob import glob





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

# %%

os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman')
df = pd.read_csv("manual_ext.csv")


df['prodname'] = ''
df['date'] = ''
df['rev'] = ''
df['cat'] = ''
df['id'] = ''
df['unit'] = '3'
df['component'] = ''


for mi,j in enumerate(df['file']):
    
    
    
    # j = '1,3,5-triisopropylbenzene (tipb) - 97.pdf'    
    
    
###Getting all of the document info
   #Get factotum document ids    
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\eastman_semiauto_doc_records.csv"))
    for row in template:
        if row[6] ==j:
            id = row[0]
            print(id)
            
    df['id'].iloc[mi] = id
    
            
    #open txt file and clean text
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\og_pdfs')
    ifile = open(j.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(str(j) + 'cleaned is blank')
    
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
            # print(len(l))
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
        
        
    df['prodname'].iloc[mi] = prodname
            
    
    
    
   
        
    
    
    
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
            
        else:
            cat = ' '.join(cat_filtered)
            
    cat = cat.replace(':','').replace('.','').strip()
    df['cat'].iloc[mi] = cat 
            
            
            
        
        # cat = cleaned.split('identified uses', 1)[-1].split('details of the supplier')[0].split(':', 1)[-1].strip().split('\n', 1)[0]

    
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
    
    
    df['rev'].iloc[mi] = rev
    
    
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
    
    
    # dates_dict[k] = dates

        
    
    # dates = set(map(tuple,dates))  #need to convert the inner lists to tuples so they are hashable
    # dates = list(map(list,dates))
    
    
    
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
            
            
        
        
    df['date'].iloc[mi] = rev_date
    
    

# %% cleaning 

# %%% concentration cleaning

df['minC'] = ''
df['maxC'] = ''

for i,j in enumerate(df['cent_C']):
    if '-' in str(j):
        
        split_centc = str(j).split('-')
        df['minC'].iloc[i] = split_centc[0]
        df['maxC'].iloc[i] = split_centc[1]
        df['cent_C'].iloc[i] = ''



# %%% chem name

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(df)):
    df["raw_chem_name"].iloc[j]=str(df["raw_chem_name"].iloc[j]).strip().lower()
    df["raw_chem_name"].iloc[j]=clean(str(df["raw_chem_name"].iloc[j]))
    if len(df["raw_chem_name"].iloc[j].split())>1:
        df["raw_chem_name"].iloc[j]=" ".join(df["raw_chem_name"].iloc[j].split())


# %%% reorganizing


df['report_funcuse'] = ''
df['component'] = ''


extract_df = df.loc[:,['id', 'file', 'prodname', 'date', 'rev', 'cat', 'raw_cas', 'raw_chem_name', 'report_funcuse','minC', 'maxC','unit', 'rank', 'cent_C', 'component']]
extract_df.columns = ['data_document_id', 'data_document_filename', 'prod_name', 'doc_date', 'rev_num', 'raw_category', 'raw_cas', 'raw_chem_name', 'report_funcuse','raw_min_comp', 'raw_max_comp', 'unit_type', 'ingredient_rank', 'raw_central_comp','component']

    
    
# %% extract to csv
os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\ext_csv")
df.to_csv('eastman_semiauto_ext.csv', index=False)


# %% organize files

manual_files = df['file'].to_list()
manual_files = sorted(list(set(manual_files)))



source = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\all pdfs"
os.chdir(source)


for file in manual_files:
    print(file)
    
    os.chdir(source)
    # file path
    file_name = os.path.join(source, str(file))
      
    # Destination path
    destination = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Eastman\pdfs\manual"
    # Move the content of
    # source to destination
    dest = shutil.copy(file_name, destination)
    print(dest)




