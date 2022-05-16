#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perform domain of applicability data prep (if not performed with run_model_selection_train.py).

Created on Thu Aug  5 08:59:37 2021

@author: jwall01
"""
#import datetime
import joblib
from puc_model.model_utils import get_prediction_ranks, slugify, convert_PUC_numeric
from puc_model.data_processing import (load_env_file)
import numpy as np
import pandas as pd
import os

env = load_env_file("env.json")
#Set parameters
label = env["model_label"]#'factotum_20211129' #Unique identifier for the model
pucKind = env["run_model_selection_train"]['pucKind']# 'all'#'FO'
modelType = env["run_model_selection_train"]['modelType']#'SGD'#'SVM' #Model Type (e.g. SVM, RF, SGD)
n_models=env["run_model_selection_train"]['n_models']#5 #Number of models to train for Voting Classification

inputDir='models/model_'+label+'/input/'
compDir='models/model_'+label+'/components/'
outputDir='models/model_'+label+'/output/'
#Get puc dictionary
puc_key_dict = joblib.load(f'{inputDir}puc_key_dict_{pucKind}.joblib')
#Load training and test datasets (help reference product_id)
train_prod = pd.read_excel(f'{inputDir}df_training.xlsx', engine='openpyxl', index_col=0)
test_prod = pd.read_excel(f'{inputDir}df_testing.xlsx', engine='openpyxl', index_col=0)

for modelName in sorted(puc_key_dict.Value, reverse=True) + ['kind']:
    
    #Manual process of removing PUCs that are too large for DA data prep
    if modelName in ['personal care make-up and related']:
        continue 
    #Skip already prepped DA data
    if os.path.isfile(f'{outputDir}/domain/{slugify(modelName)}_data.xlsx'):
        continue
    #Filter to model's products
    tr_prod = train_prod[(train_prod.train_y0 == modelName) | 
                         (train_prod.train_y1 == modelName) |
                         (train_prod.train_y2 == modelName) |
                         (train_prod.train_y3 == modelName)]
    te_prod = test_prod[(test_prod.test_y0 == modelName) | 
                         (test_prod.test_y1 == modelName) |
                         (test_prod.test_y2 == modelName) |
                         (test_prod.test_y3 == modelName)]
    #Skip PUCs without training data
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_train_data.joblib'):
            continue
    #Pull datasets
    puc_tiers_train = joblib.load(f'{compDir}{slugify(modelName)}_train_data.joblib')
    puc_tiers_test = joblib.load(f'{compDir}{slugify(modelName)}_test_data.joblib')
    #file_size = os.stat(os.path.abspath(f'{compDir}{slugify(modelName)}_train_data.joblib')).st_size / 1000
    
    #If training data is a string, create a dummy model to return that string
    #If training data only has 1 classification, create dummy model
    if isinstance(puc_tiers_train, str) or len(set(puc_tiers_train['Y'])) == 1:
        continue
    
    #Load product IDs
    d = pd.read_excel(f'{inputDir}df_training.xlsx', engine='openpyxl', index_col=0)
    #Convert PUCs to numeric (save both)
    xdata_s=puc_tiers_train['X']
    ydata_s1 = convert_PUC_numeric(puc_tiers_train['Y'], puc_key_dict)
    ydata = pd.DataFrame(ydata_s1)
    ydata['PUC'] = puc_tiers_train['Y']
    
    xtest_s=puc_tiers_test['X']
    ytest_s1 = convert_PUC_numeric(puc_tiers_test['Y'], puc_key_dict)
    ytest = pd.DataFrame(ytest_s1)
    ytest['PUC'] = puc_tiers_test['Y']
    
    fs = joblib.load(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
    
    xdata_s = np.asarray(xdata_s)
    xtest_s = np.asarray(xtest_s)
    
    # Get selected features
    if fs is None:
        X_selected_train = xdata_s
        X_selected_test = xtest_s
    else:
        X_selected_train = fs.transform(xdata_s)
        X_selected_test = fs.transform(xtest_s)
    #Scale data
    min_max_scaler = joblib.load(f'{compDir}scale_{label}.joblib')
    X_selected_train = min_max_scaler.fit_transform(X_selected_train)
    X_selected_test = min_max_scaler.fit_transform(X_selected_test)
    print(f"model: {modelName}")
    print('...getting Domain of Applicability results...')
    estimator = joblib.load(f'{compDir}{slugify(modelName)}_model_VC.joblib')
    # Make predictions
    if not hasattr(estimator, 'predict'):
        print('Setting Single Class For Estimator Predictions')
        y_pred_train = [estimator for i in range(len(X_selected_train))]
        y_pred_test = [estimator for i in range(len(X_selected_test))]
    else:
        #Get top prediction
        y_pred_train = estimator.predict(X_selected_train)
        y_pred_test = estimator.predict(X_selected_test)
    
    #Add PUC from numeric conversion for predictions
    tmp = [''.join(puc_key_dict[puc_key_dict.Value == i]['Value'].values) if isinstance(i, str) else
               ''.join(puc_key_dict[puc_key_dict.id == i]['Value'].values) for i in y_pred_train]
    y_pred_train = pd.DataFrame(y_pred_train)
    y_pred_train['PUC'] = tmp
    
    tmp = [''.join(puc_key_dict[puc_key_dict.Value == i]['Value'].values) if isinstance(i, str) else
               ''.join(puc_key_dict[puc_key_dict.id == i]['Value'].values) for i in y_pred_test]
    y_pred_test = pd.DataFrame(y_pred_test)
    y_pred_test['PUC'] = tmp
    
    # Get Prediction Ranks
    y_rank_train = get_prediction_ranks(e=estimator, x=X_selected_train)
    y_rank_test = get_prediction_ranks(e=estimator, x=X_selected_test)
    
    #Get selected features features
    if not hasattr(fs, 'selected_features'):
        beta = []
    else:
        beta = fs.selected_features
    print('Exporting domain of applicability data...')
    report = {'train':tr_prod[['train_products', 'train_name']],
              'test':te_prod[['test_products', 'test_name']],
              'xdata': pd.DataFrame(X_selected_train),
              'xtest': pd.DataFrame(X_selected_test),
              'ydata': ydata,#pd.DataFrame(ydata_s1),
              'ytest': ytest,#pd.DataFrame(ytest_s1),
              'pred_data':y_pred_train,#pd.DataFrame(y_pred_train),
              'pred_test':y_pred_test,#pd.DataFrame(y_pred_test),
              'rank_data':pd.DataFrame(y_rank_train),
              'rank_test':pd.DataFrame(y_rank_test),
              'beta': pd.DataFrame(beta).transpose()}
    with pd.ExcelWriter(f'{outputDir}/domain/{slugify(modelName)}_data.xlsx') as writer:
            for key in report:
                report[key].to_excel(writer, key)#, index=False)
            writer.save()