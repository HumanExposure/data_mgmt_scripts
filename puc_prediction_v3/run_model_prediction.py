#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 10:13:44 2021

@author: jwall01
"""
#Workflow to make predictions based on input string, tuple, list, or DataFrame (from csv or otherwise)

import pandas as pd
import numpy as np
import os
import datetime
import math
from puc_model.model_utils import (run_model_prediction, format_prediction_input)
from puc_model.data_processing import (clean_str, load_env_file)
from joblib import Parallel, delayed
from sklearn.utils import parallel_backend

env = load_env_file("env.json")
#Set parameters
label = env["model_label"]#'factotum_20211129' #Unique identifier for the model
pucKind = env["run_model_selection_train"]['pucKind']# 'all'#'FO'
modelType = env["run_model_selection_train"]['modelType']#'SGD'#'SVM' #Model Type (e.g. SVM, RF, SGD)
pred_proba = env["run_model_selection_train"]['pred_proba']# True
run_parallel = env['run_model_prediction']['parallel']

dat = None
# #Load Data
# #625535	ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)	-- Act -- Johnson & Johnson
# #651871	AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)	 -- AHAVA -- Dead Sea Laboratories Ltd.
# #String
# dat = 'ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation) Act Johnson & Johnson'
# #String List
# dat = ['ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation) Act Johnson & Johnson', 
#        'AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation) AHAVA Dead Sea Laboratories Ltd.']
# #Tuple
# dat = ('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', 'Act', 'Johnson & Johnson')
# #Tuple List
# dat = [('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', 'Act', 'Johnson & Johnson'), 
#        ('AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)', 'AHAVA', 'Dead Sea Laboratories Ltd.')]
# #Missing value
# dat = [('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', None, 'Johnson & Johnson'), 
#        ('AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)', 'AHAVA', np.nan)]
# #Dictionary
# dat = {'title': ['ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)',
#                  'AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)'],
#        'brand_name': ['Act', 'AHAVA'],
#        'manufacturer': ['Johnson & Johnson', 'Dead Sea Laboratories Ltd.']}
# #DataFrame
# dat = pd.DataFrame(data=[('ACT Alcohol Free Anticavity Fluoride Mouthwash, Cinnamon (2016 formulation)', 'Act', 'Johnson & Johnson'), 
#                          ('AHAVA Deadsea Algae Rich Mineral Makeup Care Foundation, Terra (old formulation)', 'AHAVA', 'Dead Sea Laboratories Ltd.')],
#                    columns = ['title', 'brand_name', 'manufacturer'])
# Load and shuffle (helps wiht later tests for reproducibility)
dat = pd.read_csv(rf"{env['run_model_prediction']['dat_file']}").sample(frac=1).reset_index(drop=True)
dat = dat.rename(columns={"prod_title":"title"})
#Ensure input data fits prediction format
dat = format_prediction_input(X=dat)

#Batch model predictions (save file with batch number)
outputDir = f'models/model_{label}/output/predictions/'
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)

batchSize = env['run_model_prediction']['batchSize']#12500
batchCount = math.ceil(len(dat) / batchSize) #Round up on size division
start = 0 + (batchSize + 1) * 0 #Skipping already complete batches
# Create list of batch ranges to predict
batchList = {}
for n in range(1, batchCount+1):
    #if(n > 2):
     #   break
    end = start + batchSize
    if(end > len(dat)):
        end = len(dat)
    batchList[n] = [start, end]
    #Increment Start
    start = end# + 1
    if(end == len(dat)):
        break

def batch_prediction(start, end, df):
    print(str(n) + ' : Start ' + str(start) + ' : End ' + str(end))
    # df = dat[start:end] #Subset overall dataset
    
    #Filter out any empty or illegal names now
    df['name_check'] = clean_str(df['brand_name'], df['title'], df['manufacturer'])
    removed_products = df[df.name_check.str.len() == 0]
    df = df[~(df.name_check.str.len() == 0)]
    
    predictions = run_model_prediction(label=label, modelType=modelType, 
                          n_model=None, pucKind=pucKind, df=df, pred_proba=pred_proba)
    
    if(len(predictions) == 0):
        print('No PUC predictions to push...skipping...')
    else:
        print("Saving predictions")
        #Filtering output to 80% predicted probability threshold
        # out = predictions.loc[(predictions.pred_kind_proba > 0.8) &
        #                       (predictions.pred_gencat_proba > 0.8) &
        #                       (predictions.pred_prodfam_proba > 0.8) &
        #                       (predictions.pred_prodtype_proba > 0.8) & 
        #                       (predictions.pred_kind != 'oc')]
        #out = out[['product_id', 'pred_kind', 'pred_gencat', 'pred_prodfam', 'pred_prodtype']]
        out = predictions.drop(['xdata'], axis=1) #Drop large column
        out.to_csv(f'{outputDir}batched_predictions_{str(start)}_{str(end)}.csv', index=False)
        print('Done' + ' : Start ' + str(start) + ' : End ' + str(end))

# Make predictions
if run_parallel != 1:
    n_jobs = 1
else:
    n_jobs = 1# env['run_model_prediction']['n_jobs']

# with parallel_backend('loky'):
#         Parallel(n_jobs=n_jobs)(delayed(batch_prediction)(start=batchList[n][0], 
#                                                           end=batchList[n][1], 
#                                                           df=dat[batchList[n][0]:batchList[n][1]])
#                             for n in range(1, batchCount+1))

for n in range(1, batchCount+1):
    batch_prediction(start=batchList[n][0], 
                     end=batchList[n][1], 
                     df=dat[batchList[n][0]:batchList[n][1]])
                            

print('Done - ' + str(datetime.datetime.now()))