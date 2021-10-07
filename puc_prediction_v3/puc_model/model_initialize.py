#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 09:57:42 2021

@author: jwall01
"""

import datetime
import joblib
import pandas as pd
import numpy as np
import os
from puc_model.data_processing import (read_df_uber, read_group, read_puc_types, 
                                       clean_str, standardize)

#from puc_model.puc_model import get_vector, load_model
#import torch

def create_model_dir(label='', overwrite=False):
    '''Check if directory exists, if not, create it, unless overwrite is False.
    Args:
        label (str)
    '''
    # If folder doesn't exist, then create it.
    if not os.path.isdir(f'models/model{label}'):
        os.makedirs(f'models/model{label}')
        os.makedirs(f'models/model{label}/components')
        os.makedirs(f'models/model{label}/input')
        os.makedirs(f'models/model{label}/output')
        os.makedirs(f'models/model{label}/output/cross validation')
        os.makedirs(f'models/model{label}/output/domain')
        print(f"Created model folder : model{label}")
    else: #If exists, check if overwrite is true
        if overwrite:
            print(f'Overwriting previous model : model{label}')
        else:    
            print(f"model{label} folder already exists.")
            return(False)
    return(True)

def model_initialize(add_groups=[], label='', pucType='all', recordMin=30, overwrite=False):
    """Initialize the model by pulling and cleaning data.

    Will pull all of the products with PUCs, as well as all of the products
    in data groups that are in the input. The products within these data groups
    should not requie PUCs (e.g. a pure chemical). This is to train the model
    on products that should not have a PUC.

    Args:
        add_groups (list, optional): A list of data groups. Defaults to [].
        label (str, optional): Label for the saved data. Defaults to ''.
        pucType(str, optional): Abbreviation of puc kind/type code to filter to. Defaults to 'all'.
        recordMin (num, optional): Threshold to drop PUCs with limited records
        overwrite (boolean, optional): Whether to overwrite a previous model

    """
    print(f'----- Initializing model ----- {str(datetime.datetime.now())}')
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    #Create Model Directory (Returns boolean)
    if not create_model_dir(lab, overwrite):
        print("Choose a different model name or set overwrite to True")
        return(None)
    #Variables to store input and components directories
    inputDir=f'models/model{lab}/input/'
    compDir=f'models/model{lab}/components/'
    #Convert to list if an int
    if isinstance(add_groups, int):
        add_groups = [add_groups]

    print(f'Pulling products {str(datetime.datetime.now())}')
    #df = read_df() #Pull product data for training/testing data
    df = read_df_uber()
    #Filter to specific PUC Type (e.g. formulation vs. article)
    df = df[df['puc_id'].isin(read_puc_types(puc_type=pucType)['id'])]
    df['product_id_index'] = df['product_id']
    df = df.set_index("product_id_index")
    #Save copy of original brand/title with cleaned name
    joblib.dump(df, f'{inputDir}orig_uncleaned_input_product_data{lab}.joblib')
    
    print(f'Cleaning product data {str(datetime.datetime.now())}')
    df = df.apply(standardize)
    df['name'] = clean_str(df.brand_name, df.title, df.manufacturer)
    #Combine desired columns
    comb = df[['product_id','brand_name', 'title', 'manufacturer',
               'name', 'gen_cat', 'prod_fam', 'prod_type', 'kind']]
    
    chem_df = read_group(add_groups)
    chem_df['product_id_index'] = chem_df['product_id']
    chem_df = chem_df.set_index("product_id_index")
    if len(chem_df) > 0:
        chem_df = chem_df.apply(standardize)
        chem_df['name'] = clean_str(chem_df.brand_name,chem_df.title, chem_df.manufacturer)
        chem_df['gen_cat'] = 'not_applicable'
        chem_df['prod_fam'] = ''
        chem_df['prod_type'] = ''
        chem_df['kind'] = ''
        chem_df = chem_df[['product_id','brand_name', 'title', 'manufacturer',
               'name', 'gen_cat', 'prod_fam', 'prod_type', 'kind']]
    else:
        print(f'Groups not added: {add_groups}')
        
    #Combine datasets
    df_comb = pd.concat([comb] + [chem_df])        
    #Filter to PUCs with at least the recordMin 
    df_comb['PUC'] = df_comb[['gen_cat', 'prod_fam', 'prod_type']].agg('_'.join, axis=1)
    #Filter to unique product and brand_name and title pairs
    df_comb = df_comb[['product_id', 'title','brand_name', 'manufacturer', 'name', 'gen_cat',
            'prod_fam','prod_type', 'kind', 'PUC']].drop_duplicates()
    df_comb = df_comb.groupby('PUC').filter(lambda x: len(x) >= recordMin)
    #Fill empty with NaN, shuffle dataset, drop NA name
    df_comb = df_comb.replace('', np.nan).sample(frac=1).dropna(subset=['name'])# \
        #.reset_index(drop=True)
    #Drop PUC field
    df_comb = df_comb.drop('PUC', axis=1)
    
    #Filter to unique name entries (since product_id field prevents duplicate drop)
    #Sample 1 from each group of duplicate name
    df_comb = df_comb.groupby('name').sample(n=1, random_state=1234)
    
    #Save copy of original brand/title with cleaned name
    joblib.dump(df_comb, f'{inputDir}orig_input_product_data{lab}.joblib')
    df_comb.to_excel(f'{inputDir}orig_input_product_data{lab}.xlsx')
    #Save training data without brand/title
    joblib.dump(df_comb.drop(columns=['brand_name','title', 'manufacturer']), 
                f'{inputDir}training_data{lab}.joblib') #Save shuffled data
    #Create PUC dictionary
    pkey = pd.concat([df_comb[['kind', 'gen_cat', 'prod_fam', 'prod_type']],
                      (df_comb['gen_cat'] + ' ' + df_comb['prod_fam']
                       .fillna('none')
                       + ' ' + df_comb['prod_type'].fillna('none'))
                      .str.strip()],
                     axis=1).drop_duplicates().set_index(0).fillna('')
    joblib.dump(pkey, f'{compDir}PUC_key{lab}.joblib')
    return(print(f'Done...run script run_xdata_components_dump.py --- {str(datetime.datetime.now())}'))