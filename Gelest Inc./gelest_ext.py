# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:49:48 2023
First one
@author: CLUTZ01

Updated on Tue Sep 5 2023
"""


# %%imports

import os, string, csv, re
import pandas as pd
import numpy as np
import tabula as tb
import random


from glob import glob
from pikepdf import Pdf


from tqdm import tqdm

# %% Definitions
# %%% cleanline definition
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




# %% create copies of files and convert to txt files


# os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\pdfs\pdfs for upload\pdfs_for_upload_p1') #Folder pdfs are in
# pdfs = glob("*.pdf")

# for file in pdfs:
#      new_pdf = Pdf.new()
#      with Pdf.open(file) as pdf:
#          pdf.save(file.replace('.pdf', '_edited.pdf'))
   
# pdfs = glob("*_edited.pdf")

 
# ###
# #converting pdf to text outside of def for troubleshooting   
# execfile = "pdftotext.exe"
# execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64'
   
# for file in pdfs:
#    pdf = '"'+file+'"'
#    cmd = os.path.join(execpath,execfile)
#    cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
#    os.system(cmd)



# %% Extraction


    
    
# %%% composition info extraction    
#file location set up
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs/copied (_edited) pdfs')
fileList = glob("*_edited.pdf")


comp_dfs = {}
# %% find hazards

no_hazards = {}
for file in tqdm(fileList):
    
    # file = 'ta7-sfa_edited.pdf'
    
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\pdfs\txt files')
    ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(file)
    
    lines = cleaned.split('\n')
    cl_lines = []
    for l in lines:
        if len(l) == 0:
            continue
        else:
            cl_lines.append(l)
    
    if 'does not contain any substances' in cleaned:
        print(file)
        no_hazards[file] = cleaned 
        # cleaned_trimmed = cleaned.split('3.2 mixtures', 1)[-1].split('4.1',1)[0]
    else:
        continue
    
           
    
    
    for i,l in enumerate(cl_lines):
        
        if 'section 3' in str(l) or 'composition' in str(l) and not 'decomposition' in str(l):
            start = i
            break
        else:
            continue
      
    
    for i,l in enumerate(cl_lines):
        if 'section 4' in str(l) or 'first aid' in str(l):
            stop = i
            break
        else:
            continue
    lines = cl_lines[start:stop]
            
    
   
    
        
    
    
# %%%

for file in tqdm(fileList):
    
    if file in comp_dfs.keys():
        print(str(file)+ ': already extracted')
        continue
    

    
    # file = 'pdm-7050_edited.pdf'
    #extract tables from file using tabula
    #open txt file and clean text
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\pdfs\txt files')
    ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(file)    
    
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\pdfs\copied (_edited) pdfs')
    ingreds_l = tb.read_pdf(file, pages = "1-4")
    ingreds_li = []
    

        
    #refine results to a single dataframe that includes ingredients    
    if isinstance(ingreds_l, pd.DataFrame):
        # print('yes')
        ingreds_li.append(ingreds_l)
        # ingreds_l = ingred
    else:
        # print('no')
        for ingred in ingreds_l:  
            if len(ingred) > 0: 
                ingred_s = ingred.to_string()
                if 'CAS' in ingred_s or '>' in ingred_s or '<' in ingred_s:
                    # print('This is a cas and we are putting it in there')
                    ingreds_li.append(ingred)
               
                    # ingreds_l = ingred


    

#convert any lists of one dataframe to dataframe
    
    if isinstance(ingreds_l, list):
        ingreds_l = ingreds_li[0]
    else:
        ingreds_l = ingreds_li
    
    # comp_dfs[file] = ingreds_l
    ingreds = ingreds_l
    ingreds = ingreds.dropna(how = 'all', axis = 0)
    ingreds = ingreds.dropna(how = 'all', axis = 1)


    if 'this mixture does not contain any substances to be mentioned' in cleaned:
        print(file+' doesnt have ingredients')
        
        temp_df = {'chem':[''], 'cas':[''], 'centC':['']}
        ingreds = pd.DataFrame(temp_df)
        
        file_comp_df=pd.DataFrame({'raw_chem_name':ingreds['chem'],'raw_cas':ingreds['cas'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
        file_comp_df['rank'] = np.arange(len(file_comp_df))
        file_comp_df=pd.DataFrame({'raw_chem_name':file_comp_df['raw_chem_name'], 'raw_cas':file_comp_df['raw_cas'],'raw_central_comp':file_comp_df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
            
        # comp_dfs[file] = file_comp_df

###Variation 1: Mixtures in header 
    ingreds.reset_index(inplace = True, drop = True) 
    ingreds_header = ingreds.iloc[0,:].tolist()
    
    drop = []
    for name,values in ingreds.items():
        for i,j in enumerate(values):
            if re.search(r'H\d\d\d', str(j)):
                drop.append(name)
                break
          
    ingreds_trim = ingreds.drop(drop, axis = 1)
    
    drop = []
    for i,h in enumerate(ingreds_header):
        print(i)
        print(str(h))
        if 'name' in str(h).lower() or 'identifier' in str(h).lower() or 'product' in str(h).lower():
            print(str(h))
            drop.append(i)
            ingreds_trim = ingreds_trim.drop(0, axis = 0)
            break
        
    ingreds_trim = ingreds_trim.dropna(how = 'all', axis = 1)
            
                
    ingreds = ingreds_trim

    #intial fix and removal of unneeded columns
    for l in ingreds.columns:
        if 'unnamed' in str(l).lower():
            ingreds.columns = ingreds.iloc[0]
            break
    ingreds = ingreds.dropna(how = 'all', axis = 1)
        
    
    keep = []
    for i,j in enumerate(ingreds.columns):
        if 'classification' in str(j).lower() or ' tox' in str(j).lower() or 'classified' in str(j).lower():
            continue
        else:
            keep.append(i)
    ingreds = ingreds.iloc[:,keep]
    ingreds = ingreds.dropna(how = 'all', axis = 0)
    ingreds.reset_index(drop = True, inplace = True)
    
    ingreds = ingreds.dropna(how = 'all', axis = 1)
    
    keep = []
    ingreds_cols = ingreds.columns.tolist()
    for i,j in enumerate(ingreds[ingreds_cols[0]]):
        if 'name' in str(j).lower():
            continue
        else:
            keep.append(i)
            
    ingreds = ingreds.iloc[keep,:]
    ingreds_cols = ingreds.columns.tolist()
    
    if file == 'ombi086_edited.pdf':
        ingreds['raw_cas'] = '593-91-9'
        ingreds.columns = ['raw_chem_name', 'centC', 'raw_cas']
        ingreds = ingreds.loc[:,['raw_chem_name', 'raw_cas','centC']]
    elif file == 'pdm-7050_edited.pdf':
        ingreds['centC'] = np.NaN
        ingreds.columns = ['raw_chem_name', 'raw_cas','centC']
        
    else:
        ingreds.columns = ['raw_chem_name', 'raw_cas','centC']
    
    for i,j in enumerate(ingreds['raw_cas']):
        if re.search(r'\d+-\d\d-\d', str(j)):
            match = re.findall(r'\d+-\d\d-\d', str(j))[0]
            ingreds['raw_cas'].iloc[i] = match
    
    
    nan_columns = []
    for i,j in enumerate(ingreds.values):
        for index,u in enumerate(j):
            if 'nan' in str(u):
                nan_columns.append(index)
    
    no_grouping = False
    if len(nan_columns) == 0:
        no_grouping == True
    
    
    if no_grouping == False:
        group_by_chem = False
        group_by_cas = False
        group_by_concentration = False
        if 0 in nan_columns and 1 in nan_columns:
            print('group by concentration')
            group_by_concentration = True
        elif 0 in nan_columns and 2 in nan_columns:
            print('group by cas')
            group_by_cas = True
        elif 1 in nan_columns and 2 in nan_columns:
            print('group by chem')
            group_by_chem = True
    else:
        print('continue')
        continue
        
    if group_by_chem == True:
        ingreds.fillna(method='ffill', inplace=True)
        ingreds = ingreds.groupby(['raw_cas', 'centC'], as_index=False)['raw_chem_name'].apply(''.join)
        ingreds = ingreds.loc[:,['raw_chem_name', 'raw_cas', 'centC']]
    elif group_by_concentration == True:
        ingreds.fillna(method='ffill', inplace=True)
        ingreds = ingreds.groupby(['raw_chem_name', 'raw_cas'], as_index=False)['centC'].apply(''.join)
        ingreds = ingreds.loc[:,['raw_chem_name', 'raw_cas', 'centC']]
    elif group_by_cas == True:
        ingreds.fillna(method='ffill', inplace=True)
        ingreds = ingreds.groupby(['raw_chem_name', 'centC'], as_index=False)['raw_cas'].apply(''.join)
        ingreds = ingreds.loc[:,['raw_chem_name', 'raw_cas', 'centC']]
    
    
    
    file_comp_df=pd.DataFrame({'raw_chem_name':ingreds['raw_chem_name'],'raw_cas':ingreds['raw_cas'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    file_comp_df['rank'] = np.arange(len(file_comp_df))
    file_comp_df=pd.DataFrame({'raw_chem_name':file_comp_df['raw_chem_name'], 'raw_cas':file_comp_df['raw_cas'],'raw_central_comp':file_comp_df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        

    comp_dfs[file] = file_comp_df

# %%% doc info ext

"""
Extracts data from txt files into a pandas dataframe based on pdf variation
"""



dfs = []
for k,v in tqdm(comp_dfs):
    #set up values for document data
    prodname = ''
    date = ''
    rev = ''
    cat = ''
    id = ''
    unit = ''
    component = ''
    
    # file = r'ams-2202_edited.pdf'
    
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
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\Factotum_Gelest_Inc_documents_20230713.csv"))
    for row in template:
        if row[6] == k.replace('_edited',''):
            id = row[0]
    
            
    #open txt file and clean text
    os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\pdfs\txt files')
    ifile = open(k.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(k)    
    
    
    os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs/copied (_edited) pdfs')
    #getting repeated info
    prodname = cleaned.split('product name :')[-1].split('product code')[0].strip().replace('\n', '').replace('®', '').replace('â','') #get product name
    prodname = re.sub(' +', ' ', prodname) #get rid of extra spaces
    
    #get revision date
    if 'revision' in cleaned:
        date = cleaned.split('revision date')[-1].strip(': ').split(' ')[0].strip() #get date
    elif 'date of issue' in cleaned:
        date = cleaned.split('date of issue')[-1].strip(': ').split(' ')[0].strip() #get date
    elif 'issue date' in cleaned:
            date = cleaned.split('issue date')[-1].strip(': ').split(' ')[0].strip() #get date
    else:
        print('error')
    
    #get version        
    if rev == '' and 'version' in cleaned:
        initial = cleaned.split('version')[-1].strip(': ').split('sds')[0].split('section')[0].strip()
        if 'print date' not in initial:
            rev = cleaned.split('version')[-1].strip(': ').split('sds')[0].split('section')[0].strip() #Get revision number
        else:
            rev = cleaned.split('version')[-1].strip(': ').split('sds')[0].split('section')[0].split('print date')[0].strip() #Get revision number
    cat = cleaned.split('recommended use')[-1].split('1.3')[0].replace(r':', '').strip()#.split('safety data sheet')[0].replace('\n',' ').strip(': ') #Get raw category
    cat = re.sub(' +', ' ', cat) #get rid of extra spaces
    
   
    
    idList = [] #list of product IDs
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    unitList = []
    
    
    n = len(v)
    idList.extend([id]*n)
    filenameList.extend([k]*n)
    prodnameList.extend([prodname]*n)
    dateList.extend([date]*n)
    revList.extend([rev]*n)
    catList.extend([cat]*n)
    
    df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':ingreds['cas'], 'raw_chem_name':ingreds['chem'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
    df['rank'] = np.arange(len(df))
    df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
    dfs.append(df)
# %%          
    
    
    ingreds.loc[0, :].values.tolist()
    
    
    
    
    
    file_comp_df=pd.DataFrame({'raw_chem_name':ingreds['chem'],'raw_cas':ingreds['cas'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    file_comp_df['rank'] = np.arange(len(file_comp_df))
    file_comp_df=pd.DataFrame({'raw_chem_name':file_comp_df['raw_chem_name'], 'raw_cas':file_comp_df['raw_cas'],'raw_central_comp':file_comp_df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        
    comp_dfs[file] = file_comp_df

#all other files that do not contain any ingredients

    

# %%% CONCAT ALL DFS        
#concat all dfs in dfs together  
ingreds_df=pd.concat(dfs, axis=0, ignore_index=True)



# %%
import pickle
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc')
with open('ingreds_df.pickle', 'wb') as handle:
    pickle.dump(ingreds_df, handle, protocol=pickle.HIGHEST_PROTOCOL)



with open('ingreds_df.pickle', 'rb') as handle:
    b = pickle.load(handle)
    
      
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc')
ingreds_df = pd.read_pickle(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\ingreds_df.pickle')
    
objects = []
with (open("ingreds_df.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
        
# %% cleaning extraction data


#intial text clean up
def clean(dirty): return ''.join(filter(string.printable.__contains__, dirty))
ingreds_df['raw_central_comp']=ingreds_df['raw_central_comp'].astype(str).str.strip()
for j in range(0, len(ingreds_df)):
    ingreds_df["raw_central_comp"].iloc[j] = ingreds_df["raw_central_comp"].iloc[j].replace('–', '-')
    ingreds_df["raw_central_comp"].iloc[j] = clean(
    str(ingreds_df["raw_central_comp"].iloc[j]))



#create min and max values for ranged composition values
ingreds_df['minC']=ingreds_df['raw_central_comp'].astype(str).str.split('-', expand=True)[0].str.strip()
ingreds_df['maxC']=ingreds_df['raw_central_comp'].astype(str).str.split('-', expand=True)[1].str.strip()




#mask to get rid of incorrect values in minC column
another_mask = ingreds_df['maxC'].isna()
ingreds_df['minC'][another_mask] = np.nan

#mask to get rid of values in central composition value if it is ranged
mask = ingreds_df['minC'].notna()
ingreds_df['raw_central_comp'][mask] = np.nan

#mask to establish unit and then remove if no composition values present
ingreds_df['unit'] = '3'
ingreds_df.loc[(ingreds_df['minC'].astype(str).str.contains('na', na=False)) & (ingreds_df['raw_central_comp'].astype(str).str.contains('na', na=False)), 'unit'] = ''

#other data and correct rank values
ingreds_df['component'] = ''
ingreds_df['report_func_use'] = ''
ingreds_df['rank']= ingreds_df['rank']+1


#final df creation and file name edits
final_df =pd.DataFrame({'data_document_id':ingreds_df['data_document_id'], 'data_document_filename':ingreds_df['data_document_filename'], 'prod_name':ingreds_df['prod_name'], 'doc_date':ingreds_df['doc_date'], 'rev_num':ingreds_df['rev_num'], 'raw_category':ingreds_df['raw_category'], 'raw_cas':ingreds_df['raw_cas'], 'raw_chem_name':ingreds_df['raw_chem_name'], 'report_func_use':ingreds_df['report_func_use'], 'raw_min_comp': ingreds_df['minC'], 'raw_max_comp' : ingreds_df['maxC'], 'unit_type': ingreds_df['unit'], 'ingredient_rank':ingreds_df['rank'], 'raw_central_comp':ingreds_df['raw_central_comp'], 'component': ingreds_df['component']}) #'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
final_df['data_document_filename'] = final_df['data_document_filename'].replace('_edited','', regex=True)
final_df = final_df.replace('nan', np.NaN)



#export
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc')
final_df.to_csv('gelest_ext_text_9_5_23.csv', index=False)



  
# %% load products_dfs
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc')
products_dfs = pd.read_pickle(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\products_dfs.pickle')

objects = []
with (open("products_dfs.pickle", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break
# %% Product csv

product_csv_df = final_df.iloc[:,[0,1,2]]
print(product_csv_df.columns)
product_csv_df.columns = ['data_document_id', 'data_document_filename', 'title']
product_csv_df = product_csv_df.drop_duplicates()

files = final_df.iloc[:,1].drop_duplicates()


files
gelest_prod_dfs = []
for p in files:
    
    # p = 'xms-5025.2.pdf'# p = files[200]
    os.chdir(r"C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs/txt files")
    ifile = open(p.replace('.pdf', '_edited.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text).lower()
    cleaned = re.sub(' +', ' ', cleaned)
    
    
    title = cleaned.split('product name : ', 1)[-1].split('product', 1)[0].strip().replace('\n','')
    prod_code = cleaned.split('product code : ')[-1].split('product', 1)[0].strip()
    
    prod = pd.DataFrame([[p,title,prod_code]], columns=['data_document_filename','title', 'item_id'])
    
   
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\Gelest_doc_records.csv"))
    for row in template:
        if row[6] == p:
            id = row[0]
    prod['data_document_id'] = id * len(prod['title'])
    prod['manufacturer'] = ['Gelest, Inc.'] * len(prod['title'])
    prod['upc'] = [''] * len(prod['title'])
    prod['brand_name'] = [''] * len(prod['title'])
    prod['size'] = [''] * len(prod['title'])
    prod['color'] = [''] * len(prod['title'])
    prod['parent_item_id'] = [''] * len(prod['title'])
    prod['short_description'] = [''] * len(prod['title'])
    prod['long_description'] = [''] * len(prod['title'])
    prod['epa_reg_number'] = [''] * len(prod['title'])
    prod['thumb_image'] = [''] * len(prod['title'])
    prod['medium_image'] = [''] * len(prod['title'])
    prod['large_image'] = [''] * len(prod['title'])
    prod['image_name'] = [''] * len(prod['title'])
    prod['item_id'] = prod_code * len(prod['title'])
    prod['model_number'] = [''] * len(prod['title'])
    
    prod['url'] = products_dfs.get(p.replace('.pdf',''))
    prod = prod.loc[:,['data_document_id', 'data_document_filename','title' , 'upc' , 'url' , 'brand_name' , 'size' , 'color' , 'item_id' , 'parent_item_id' , 'short_description' , 'long_description' , 'epa_reg_number' , 'thumb_image' , 'medium_image' , 'large_image' , 'model_number' , 'manufacturer' , 'image_name']] 
    

    gelest_prod_dfs.append(prod)
    
    
    
# %% product csv creation 
gelest_product_info=pd.concat(gelest_prod_dfs, axis=0, ignore_index=True) 
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc')
gelest_product_info.to_csv('gelest_products_9_5_2023.csv', index=False)



