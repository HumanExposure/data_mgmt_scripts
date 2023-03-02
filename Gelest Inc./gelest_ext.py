# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 15:49:48 2023

@author: CLUTZ01
"""


# %%

import os, string, csv, re
import pandas as pd
import numpy as np
import tabula as tb


from glob import glob
from pikepdf import Pdf


from tqdm import tqdm


# %%
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


os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs') #Folder pdfs are in
pdfs = glob("*.pdf")
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs') #Folder pdfs are in  
for file in pdfs:
     new_pdf = Pdf.new()
     with Pdf.open(file) as pdf:
         pdf.save(file.replace('.pdf', '_edited.pdf'))
   
pdfs = glob("*_edited.pdf")

 
###
#converting pdf to text outside of def for troubleshooting   
execfile = "pdftotext.exe"
execpath = r'C:\Users\CLUTZ01\xpdf-tools-win-4.04\bin64'
   
for file in pdfs:
   pdf = '"'+file+'"'
   cmd = os.path.join(execpath,execfile)
   cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
   os.system(cmd)



# %% Extraction



"""
Extracts data from txt files into a pandas dataframe based on pdf variation
"""

#file location set up
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc/pdfs')
fileList = glob("*_edited.pdf")


dfs = []
for file in tqdm(fileList):
    #set up values for document data
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
    template = csv.reader(open(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Gelest Inc\Factotum_Gelest_Inc._documents_20230224.csv"))
    for row in template:
        if row[6] == file.replace('_edited',''):
            id = row[0]
    
            
    #open txt file and clean text
    ifile = open(file.replace('.pdf', '.txt'), encoding='utf-8')
    text = ifile.read()
    
    
    cleaned = text
    cleaned = cleanLine(text)
    cleaned = re.sub(' +', ' ', cleaned)
    # re.sub(' +', ' ', cleaned)
    
    if cleaned == '': print(file)    
    
    #getting repeated info
    prodname = cleaned.split('product name :')[-1].split('\n')[0].strip().replace('®', '').replace('â','') #get product name
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
    
    
    
    
    #extract tables from file using tabula
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
    

        
###Variation 1: Mixtures in header 
    ingreds = ingreds_l  
    
    if 'Mixtures' in ingreds.columns[0]:
        print(file+' a mixtures one')
        #intial fix and removal of unneeded columns
        ingreds.columns = ingreds.iloc[0]
        ingreds.rename(columns={ingreds.columns[1]: 'take out', ingreds.columns[2]:'cas'},inplace=True)
        ingreds.drop('take out', axis=1, inplace=True)
        ingreds = ingreds.iloc[1:]
        ingreds = ingreds[ingreds.iloc[:,0].notna()]
        
        #renaming and fixing columns
        ingreds.rename(columns={'Name': 'chem', '%': 'centC'}, inplace=True)
        ingreds=ingreds.replace(regex=['\\(CAS\\-No\\.\\) '], value='')
        ingreds=ingreds.replace(regex=['CAS\\-No\\.\\: '], value='')
        ingreds=ingreds[["chem","cas", str("centC")]]
        
        #fill in repeated info
        n = len(ingreds)
        idList.extend([id]*n)
        filenameList.extend([file]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)

        #create rank and create df
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':ingreds['cas'], 'raw_chem_name':ingreds['chem'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        df['rank'] = np.arange(len(df))
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        
        
        dfs.append(df)
        
###Variation 2: Unnamed in intial df headers     
    elif 'Unnamed' in ingreds.columns[0]:
        print(file+' an unnamed one')
        #intial fix and removal of unneeded columns
        ingreds_e = ingreds[ingreds.iloc[:,0].notna()]
        if len(ingreds_e) == 0:
            ingreds_e = ingreds[ingreds.iloc[:,1].notna()]
        else:
            ingreds_e = ingreds[ingreds.iloc[:,0].notna()]
           
        ingreds_e = ingreds_e.dropna(axis=1, how='all')
        ingreds_e = ingreds_e.dropna(axis=0, how='all')
            
        ingreds_e.rename(columns={ingreds_e.columns[0]:'chem',ingreds_e.columns[1]:'cas', ingreds_e.columns[2]:'centC'},inplace=True)
                       
           
       
        if 'Name' in ingreds_e.iloc[0,0]:
           ingreds_e = ingreds_e.iloc[1:,:]
      
       
       #renaming and fixing columns
        ingreds_e=ingreds_e.replace(regex=['\\(CAS\\-No\\.\\) '], value='')
        ingreds_e=ingreds_e.replace(regex=['CAS\\-No\\.\\: '], value='')
        ingreds_e=ingreds_e[["chem","cas", str("centC")]]  
    
    
    #fill in repeated info
        n = len(ingreds_e)
        idList.extend([id]*n)
        filenameList.extend([file]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
    #create rank and create df
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':ingreds_e['cas'], 'raw_chem_name':ingreds_e['chem'],'raw_central_comp':ingreds_e['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
        df['rank'] = np.arange(len(df))
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
            
        dfs.append(df)
        
###Variation 3: Name in headers     
    elif 'Name' in ingreds.columns[0]:
        print(file+'a name one')
        
        #intial fix and removal of unneeded columns
        ingreds = ingreds[ingreds.iloc[:,0].notna()]
        
        #renaming and fixing columns
        ingreds.rename(columns={ingreds.columns[1]:'cas', 'Name': 'chem', '%': 'centC'},inplace=True)
        ingreds=ingreds.replace(regex=['\\(CAS\\-No\\.\\) '], value='')
        ingreds=ingreds.replace(regex=['CAS\\-No\\.\\: '], value='')
        ingreds=ingreds[["chem","cas", str("centC")]]
    
        #fill in repeated info
        n = len(ingreds)
        idList.extend([id]*n)
        filenameList.extend([file]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        
        #create rank and append new df to list of dfs
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':ingreds['cas'], 'raw_chem_name':ingreds['chem'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        df['rank'] = np.arange(len(df))
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        dfs.append(df)
    
#all other files that do not contain any ingredients

    elif 'this mixture does not contain any substances to be mentioned' in cleaned:
        print(file+' doesnt have ingredients')
        
        temp_df = {'chem':[''], 'cas':[''], 'centC':['']}
        ingreds = pd.DataFrame(temp_df)
        
        idList = [] #list of product IDs
        filenameList = [] #list of file names matching those in the extacted text template
        prodnameList = [] #list of product names
        dateList = [] #list of msdsDates
        revList = [] #list of revision numbers
        catList = [] #list of product categories
        unitList = []
        
        
        n = len(ingreds)
        idList.extend([id]*n)
        filenameList.extend([file]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':ingreds['cas'], 'raw_chem_name':ingreds['chem'],'raw_central_comp':ingreds['centC']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        df['rank'] = np.arange(len(df))
        df=pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':df['raw_cas'], 'raw_chem_name':df['raw_chem_name'], 'rank':df['rank'],'raw_central_comp':df['raw_central_comp']}) #'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})            
        dfs.append(df)
        

        
#concat all dfs in dfs together  
ingreds_df=pd.concat(dfs, axis=0, ignore_index=True)  

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



#export
os.chdir(r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Gelest Inc')
final_df.to_csv('gelest_ext_text.csv')

    
    
    


# %%
