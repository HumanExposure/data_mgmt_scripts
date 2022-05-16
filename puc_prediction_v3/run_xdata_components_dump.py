#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vectorize cleaned model data in batch.

Created on Fri Feb 19 15:03:38 2021

@author: jwall01
"""
#Control script to loop through xdata_components_dump.py until all files are vectorized
import joblib
from joblib import Parallel, delayed
from sklearn.utils import parallel_backend
import os
import shutil
import re
import subprocess
import torch
from puc_model.data_processing import (load_doc_embeddings, load_env_file)
import datetime
env = load_env_file("env.json")
parallel = env["xdata_components_dump"]["parallel"] #True
label = env["model_label"]#'factotum_20211129'
group_size = env["xdata_components_dump"]["group_size"]
lab = '' if len(label) == 0 else '_' + label.strip('_')
inputDir=f'models/model{lab}/input/'
compDir=f'models/model{lab}/components/'

print(f'----- Starting xdata splitting ----- {str(datetime.datetime.now())}')
if not os.path.isfile(f'{compDir}xdata{lab}_components.joblib'):
    #Load data
    df_comb = joblib.load(f'{inputDir}training_data{lab}.joblib')
    data = df_comb[['product_id', 'name', 'gen_cat', 'prod_fam', 'prod_type']].copy()
    del df_comb
    #Load embedding model
    doc_embeddings = load_doc_embeddings()
    #Save copy of embedding model
    joblib.dump(doc_embeddings, f'{compDir}PUC_doc_embedding{lab}.joblib')
    torch.save(doc_embeddings.state_dict(),
                f'{compDir}PUC_doc_embedding{lab}.pt')
    
    #Divide data into groups of size 500 (embedding can't handle large lists)
    n=group_size# 500#6250#, 12500
    data = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )]
    #Save copy of split dataset for batch
    joblib.dump(data, f'{compDir}xdata{lab}_components.joblib')
    del doc_embeddings, data, n
    data_n = len(joblib.load(f'{compDir}xdata{lab}_components.joblib'))

#Get number of batch sets
data_n = len(joblib.load(f'{compDir}xdata{lab}_components.joblib'))
#Get number of batches already complete
files = [f for f in os.listdir(compDir) if re.match(r'xdata_vector*', f)]
#Loop through and perform batch embedding until all sets are complete
while len(files) != data_n:
    if parallel:
        with parallel_backend('loky'):
                Parallel(n_jobs=5)(delayed(subprocess.call)(args = f'/home/jwall01/puc_prediction_v3/puc_model/xdata_components_dump.py {lab} {compDir} {str(i)}', 
                                                         shell=True)
                                    for i in range(data_n))
    else:    
        for i in range(data_n):
            #subprocess call arguments
            #args = ['/home/jwall01/puc_prediction_v3/xdata_components_dump.py', lab, compDir, i]
            #args = [ str(x) for x in args ]
            args = f'/home/jwall01/puc_prediction_v3/puc_model/xdata_components_dump.py {lab} {compDir} {str(i)}'
            subprocess.call(args, shell=True)
    files = [f for f in os.listdir(compDir) if re.match(r'xdata_vector*', f)]
    i = 0

data_n = len(joblib.load(f'{compDir}xdata{lab}_components.joblib'))
#Get list of all vectorized batches
xdata = [joblib.load(f'{compDir}xdata_vector_{i}.joblib') for i in range(data_n)]

#Unnest list of lists to list
#xdata = [item for sublist in xdata for item in sublist]
#Unnest list of dictionaries to dictionary
xdata = {k: v for d in xdata for k, v in d.items()}
    
#xdata = data['name'].apply(get_vector, args=(doc_embeddings,
#                                             )).to_list()
#Save vectorized dataset
joblib.dump(xdata, f'{compDir}xdata{lab}.joblib')
        
if not os.path.isdir(f'{compDir}xdata_vectors'):
    os.makedirs(f'{compDir}xdata_vectors')
dest1 = os.path.abspath(f'{compDir}xdata_vectors')
files = [f for f in os.listdir(compDir) if re.match(r'xdata_vector*', f)]
#Move batch components to separate folder
for f in files:
    shutil.move(os.path.abspath(f'{compDir}{f}'), dest1)
    
#os.remove(os.path.abspath(f'{compDir}xdata{lab}_components.joblib'))
print(f'----- Done ----- {str(datetime.datetime.now())}')