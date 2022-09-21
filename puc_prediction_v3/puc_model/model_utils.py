#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 13:21:21 2021

@author: jwall01
"""

#Feature selection pipeline inspired by:
##https://towardsdatascience.com/designing-a-feature-selection-pipeline-in-python-859fec4d1b12

#Load packages
from puc_model.data_processing import load_doc_embeddings, get_vector, clean_str
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn.feature_selection import f_classif
from sklearn.dummy import DummyClassifier
from sklearn.utils import parallel_backend
import joblib
from joblib import Parallel, delayed
import datetime
import os
import unicodedata
import re
#Modified package/script from the above towardsdatascience link
from puc_model.feature_selection import FeatureSelector

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def convert_PUC_numeric(y, key):
    """
    
    Parameters
    ----------
    y : str
        The input PUC string to be converted to it's numeric ID.
    key : pd.DataFrame
        A dataframe that contains a data dictionary for PUCs, 
        with numeric ID values.

    Returns
    -------
    y : numeric
        The converted y str input as a num ID based on the key.

    """
    y = pd.Series(y, name='Value')
    #Normalize case
    #y['Value'] = y.str.lower()
    key['Value'] = key['Value'].str.lower()
    y = pd.merge(y.str.lower(), key, on=['Value'], how='left')
    y = y['id']
    return y

#https://towardsdatascience.com/using-stochastic-gradient-descent-to-train-linear-classifiers-c80f6aeaff76
def find_best_sgd_svm_estimator(X, y, cv, random_seed, n_jobs):
        """Exhaustive search over specified parameter values for svm using sgd.
        Returns:
            optimized svm estimator.
        """
        max_iter = max(np.ceil(10**6 / len(X)), 1000)
        small_alphas = [10.0e-08, 10.0e-09, 10.0e-10]
        alphas = [10.0e-04, 10.0e-05, 10.0e-06, 10.0e-07]
        l1_ratios = [0.075, 0.15, 0.30]
        param_grid = [
            {'alpha': alphas, 'penalty': ['l1', 'l2'], 'average':[False]},
            {'alpha': alphas, 'penalty': ['elasticnet'], 'average':[False],
            'l1_ratio': l1_ratios},
            {'alpha': small_alphas, 'penalty': ['l1', 'l2'], 'average':[True]},
            {'alpha': small_alphas, 'penalty': ['elasticnet'], 'average':[True],
            'l1_ratio': l1_ratios}
            ]
        init_est = SGDClassifier(loss='log', max_iter=max_iter,
            random_state=random_seed, n_jobs=n_jobs, warm_start=True)
        grid_search = GridSearchCV(estimator=init_est,
            param_grid=param_grid, verbose=0, n_jobs=n_jobs, cv=cv)
        grid_search.fit(X, y)
        #print('\n All results:')
        #print(grid_search.cv_results_)
        #logger.info('\n Best estimator:')
        #logger.info(grid_search.best_estimator_)
        #logger.info('\n Best score for {}-fold search:'.format(folds))
        #logger.info(grid_search.best_score_)
        #logger.info('\n Best hyperparameters:')
        #logger.info(grid_search.best_params_)
        return grid_search.best_estimator_
    
def get_modeltype_estimator(modelType='', file_size=None):
    """
    

    Parameters
    ----------
    modelType : str, optional
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    file_size : num, optional
        The size of the dataset in kilobytes. The default is None.

    Returns
    -------
    estimator
        The estimator formatted to a set of specifications.
    str
        The model type which may have been modified due to file_size.

    """
    #Set an estimator with the best specifications based on modelType
    if modelType == 'SVM':
        best_params = {'gamma': 'scale',
                       'decision_function_shape':'ovo',
                       'cache_size':20000,
                       'kernel':'linear',
                       'C': 500,
                       'probability':True,
                       'class_weight':'balanced'}
        estimator = svm.SVC()
        estimator.set_params(**best_params)
    elif modelType == 'RF':
        best_params = {'n_estimators': 1000,
                          'max_features': 'auto',
                          'max_depth': 50,
                          'min_samples_split': 2,
                          'min_samples_leaf': 1,
                          'bootstrap': False,
                          'n_jobs':60}
        estimator = RandomForestClassifier(n_jobs = 60, random_state=42)
        estimator.set_params(**best_params)
    elif modelType == 'SGD':
        best_params = {'loss': 'log',
                       'max_iter': 1000, 
                       'tol': 1e-3,
                       'n_jobs': 10,
                       'random_state': 42}
        estimator = SGDClassifier()
        estimator.set_params(**best_params)
    else: 
        print('Error: Select a suported modelType of SVM or RF...')
        return None, None
    #Set modelType and estimator to SVM if file_size is > 300 megabytes
    if file_size > 300000 and modelType not in ['SVM', 'SGD']:
        print('Error: Cannot support a file_size > 30000 that is not SVM or SGD')
        
    return estimator, modelType

def prep_sample_df(label='', sample='all', df=None):
    """
    Function to pull/prep sample x and y data for an input dataframe

    Parameters
    ----------
    label : str, optional
        The unique model identifier string. The default is ''.
    sample : list or str, optional
        A numeric list of indexes to sample to, or 'all'. If using all the
        data in df. The default is 'all'.
    df : pd.DataFrame, required
        DESCRIPTION. The default is None, which will throw an error.

    Returns
    -------
    xdata_s : np.Series or np.ndarray
        A series of sampled embedded product name vectors.
    name : list
        A series of product names.
    ydata_s0 : list
        A series of PUC kind labels.
    ydata_s1 : list
        A series of PUC gen_cat labels.
    ydata_s2 : list
        A series of PUC prod_fam labels.
    ydata_s3 : list
        A series of PUC prod_type labels.

    """
    
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    #inputDir='models/model'+lab+'/input/'
    compDir='models/model'+lab+'/components/'
    
    #Pull cached embedded data
    xdata = joblib.load(compDir+'xdata' + lab + '.joblib')
    data = df[['product_id', 'name', 'gen_cat', 'prod_fam',
               'prod_type', 'kind']].copy()
    #Split up product name and PUC levels into lists
    #name = data['name']
    data['ydata0'] = data['kind'].str.strip()
    #ydata0 = (data['kind']).str.strip()#.to_list()
    data['ydata1'] = data['gen_cat'].str.strip()
    #ydata1 = (data['gen_cat']).str.strip()#.to_list()
    data['ydata2'] = (data['gen_cat'] + ' ' + data['prod_fam'].fillna('none')) \
        .str.strip() 
    #ydata2 = (data['gen_cat'] + ' ' + data['prod_fam'].fillna('none')) \
    #    .str.strip()#.to_list()
    data['ydata3'] = (data['gen_cat'] + ' ' + data['prod_fam'].fillna('none') + ' ' +
              data['prod_type'].fillna('none')).str.strip()
    # ydata3 = (data['gen_cat'] + ' ' + data['prod_fam'].fillna('none') + ' ' +
    #           data['prod_type'].fillna('none')).str.strip()#.to_list()
    #Sample all or by input index list
    if isinstance(sample, str):
        #print('Using all data')
        xdata_s = xdata
        ydata_s0 = data.ydata0
        ydata_s1 = data.ydata1
        ydata_s2 = data.ydata2
        ydata_s3 = data.ydata3
    else:
        if isinstance(sample, list) or isinstance(sample, np.ndarray):
            #print('Using provided index')
            inds = sample
        else:
            inds = np.random.randint(0, len(data), sample)
            # note: this samples with replacement
        #Convert to lists
        #Filter to sample product_id
        data = data[data.product_id.isin(inds)]
        #Sort by sample product_id list (inds)
        sorterIndex = dict(zip(inds, range(len(inds))))
        data['inds'] = data['product_id'].map(sorterIndex)
        data.sort_values(['inds'],
                       ascending = [True], inplace = True)
        data.drop('inds', 1, inplace = True)
        #data = data.set_index('product_id', drop=False)
        
        ydata_s0 = data.ydata0
        ydata_s1 = data.ydata1
        ydata_s2 = data.ydata2
        ydata_s3 = data.ydata3
        name = data.name#[name[i] for i in inds]
        del data
        #Reformat to float32 (instead of floar 64) to save space/memory
        xdata_s = [xdata[i].astype('float32') for i in inds]
        del xdata
    #Load scaler to normalize data
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    #Scale xdata
    #xdata_s = min_max_scaler.fit_transform(xdata_s)
    xdata_s = np.transpose(min_max_scaler.fit_transform(np.transpose(xdata_s)))
    return xdata_s, name, ydata_s0, ydata_s1, ydata_s2, ydata_s3
    
def prep_puc_key(label='', pucKind='all'):
    """
    
    Parameters
    ----------
    label : str, optional
        The unique model identifier string. The default is ''.
    pucKind : str, optional
        A string to filter the input dataframes down to a specific PUC Kind.
        The default is 'all'.

    Returns
    -------
    puc_key : np.DataFrame
        A data dictionary of all PUCs with unique ID values.

    """
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    inputDir='models/model'+lab+'/input/'
    #If already exists, load and return data
    if os.path.isfile(f'{inputDir}puc_key_dict_{pucKind}.joblib'):
        return joblib.load(f'{inputDir}puc_key_dict_{pucKind}.joblib')
    #Prep PUC Key conversion of string ydata labels to numerics
    puc_key = joblib.load(f'models/model_{label}/components/PUC_key_{label}.joblib')
    puc_key = puc_key.replace(r'^\s*$', 'NA', regex=True).fillna('none')
    puc_key_s0 = puc_key[['kind']].drop_duplicates()
    puc_key_s1 = puc_key[['gen_cat']].drop_duplicates()
    puc_key_s2 = puc_key[['gen_cat', 'prod_fam']].drop_duplicates()
    puc_key_s3 = puc_key[['gen_cat', 'prod_fam', 'prod_type']].drop_duplicates()
    
    puc_key_s0['Value'] = puc_key_s0['kind']
    puc_key_s1['Value'] = puc_key_s1['gen_cat']
    puc_key_s2['Value'] = puc_key_s2['gen_cat'] + ' ' + puc_key_s2['prod_fam']   
    puc_key_s3['Value'] = puc_key_s3['gen_cat'] + ' ' + puc_key_s3['prod_fam'] + ' ' + puc_key_s3['prod_type']
    
    #Create Master PUC to ID list
    puc_key = pd.concat([puc_key_s0, puc_key_s1, puc_key_s2, puc_key_s3])
    puc_key = puc_key.reset_index(drop=True)
    puc_key['id']= puc_key.index
    
    joblib.dump(puc_key, f'{inputDir}puc_key_dict_{pucKind}.joblib')
    puc_key.to_excel(f'{inputDir}puc_key_dict_{pucKind}.xlsx')

    return puc_key
    
def prep_split_dataset(df = None, df_val=None, label='', pucKind='all', 
                       sample_size='all', bootstrap=False):
    """
    

    Parameters
    ----------
    df : pd.DataFrame, optional
        DESCRIPTION. The default is None, which will throw an error.
    df_val : TYPE, optional
        DESCRIPTION. The default is None, which will throw an error.
    label : str, optional
        The unique model identifier string. The default is ''.
    pucKind : str, optional
        A string to filter the input dataframes down to a specific PUC Kind.
        The default is 'all'.
    sample_size : list, np.ndarray, str, optional
        An optional list or array of indees to sample the data to. The default is 'all'.
    bootstrap : boolean, optional
        Whether to sample with replacement or not. The default is False.

    Returns
    -------
    split_set : dict
        A dictionary of the input dataframes now split into PUC subsets and
        paired with their product embedding vectors.

    """
    
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    inputDir='models/model'+lab+'/input/'
    #If already exists, load and return data
    if os.path.isfile(f'{inputDir}split_dataset_{pucKind}.joblib'):
        return joblib.load(f'{inputDir}split_dataset_{pucKind}.joblib')
    #Concat to make PUC grouping variable
    df['PUC'] = df[['gen_cat', 'prod_fam', 'prod_type']].agg('_'.join, axis=1)
    groups = df['PUC'].drop_duplicates().reset_index(drop=True)
    #Split into 80% training, 20% testing data, stratified equally by UC
    df_train, df_test = train_test_split(df, test_size=0.2, 
                                         stratify=df['PUC'], 
                                         random_state=12345)
    #Filter the datasets by PUC Kind, or get all
    genCatFilter=None
    if pucKind == 'all':
        print("Using all PUC Kinds")
    elif pucKind == 'FO':
        print("Using only Formulation PUCs")
        #Formulation gen_cat
        genCatFilter=['Arts and crafts/Office supplies', 'Cleaning products and household care', 
                      'Electronics/small appliances', 'Home maintenance', 'Landscape/Yard', 
                      'Other consumer products', 'Personal care', 'Pesticides', 
                      'Pet care', 'Sports equipment', 'Vehicle', 'not_applicable']
    elif pucKind == 'AR':
        #Article gen_cat
        genCatFilter=['Batteries', 'Cons. electronics, mech. appliances, and machinery', 
                      'Construction and building materials','Food contact items',
                      'Furniture and Furnishings','Industrial machinery',
                      'Other direct contact consumer goods','Other indirect contact consumer goods',
                      'Other vehicles/mass transit','Packaging (non-food contact)','Road vehicles',
                      'Toys and children\'s products', 'not_applicable']
        print("Using only Article PUCs")
    elif pucKind == 'OR':
        #Occupation gen_cat
        genCatFilter=['Cleaning and Safety','Laboratory supplies','Manufactured formulations',
                      'Medical/Dental','Raw materials','Specialty occupational products', 'not_applicable']
        print("Using only Occupational PUCs")
    
    if not genCatFilter is None:
        genCatFilter = [x.lower() for x in genCatFilter]
        #prodTypeFilter = ['bleach', 'pens and markers', 'shampoo', 'baby shampoo']
        #genCatFilter = ['not_applicable', 'batteries', 'vehicle', 'personal care']
        df_train = df_train[df_train.gen_cat.isin(genCatFilter)]
        df_test = df_test[df_test.gen_cat.isin(genCatFilter)]
        df_val = df_val[df_val.gen_cat.isin(genCatFilter)]
    
    print('----- Prepping ' + label + ' ----- ' + str(datetime.datetime.now()))
    #Shuffle datasets
    sz = len(df_train) if isinstance(sample_size, str) else sample_size
    sample_train = np.random.choice(df_train.product_id, size=sz, replace=bootstrap)
    
    sz = len(df_test) if isinstance(sample_size, str) else sample_size
    sample_test = np.random.choice(df_test.product_id, size=sz, replace=bootstrap)
    
    sz = len(df_val) if isinstance(sample_size, str) else sample_size
    sample_val = np.random.choice(df_val.product_id, size=sz, replace=bootstrap)
    #Prep training, test, and validation datasets
    print('...sampling training...')
    xdata_s, name_data, ydata_s0, ydata_s1, ydata_s2, ydata_s3 = prep_sample_df(label, sample_train, df=df_train)
    #Change type to save memory
    xdata_s = xdata_s.astype('float32')
    print('...sampling testing...')
    xtest_s, name_test, ytest_s0, ytest_s1, ytest_s2, ytest_s3 = prep_sample_df(label, sample_test, df=df_test)
    xtest_s = xtest_s.astype('float32')
    print('...sampling validation...')
    xval_s, name_val, yval_s0, yval_s1, yval_s2, yval_s3 = prep_sample_df(label, sample_val, df=df_val)
    xval_s = xval_s.astype('float32')
    del bootstrap, df, df_test, df_train, groups, sample_size, sz
    print('...exporting splits...')
    #Combine all into dictionary set
    split_set = {'train_products':sample_train, 'train_name':name_data, 'train_x':xdata_s, 'train_y0':ydata_s0, 'train_y1': ydata_s1, 'train_y2': ydata_s2, 'train_y3': ydata_s3,
            'test_products':sample_test, 'test_name':name_test, 'test_x':xtest_s, 'test_y0':ytest_s0, 'test_y1': ytest_s1, 'test_y2': ytest_s2, 'test_y3': ytest_s3,
            'val_products':sample_val, 'val_name':name_val, 'val_x':xval_s, 'val_y0':yval_s0, 'val_y1': yval_s1, 'val_y2': yval_s2, 'val_y3': yval_s3}
    #Save XLSX copies for later reference/validation checking
    print("...Saving output...")
    with pd.ExcelWriter(f'{inputDir}df_training.xlsx') as writer:  
        pd.DataFrame.from_dict({a: split_set[a] 
                                for a in ['train_products', 'train_name', 'train_y0', 
                                          'train_y1', 'train_y2', 'train_y3']}) \
            .to_excel(writer, sheet_name='training_dat')
    #    pd.DataFrame.from_dict(split_set['train_x']).to_excel(writer, sheet_name='vector_embedding')
    with pd.ExcelWriter(f'{inputDir}df_testing.xlsx') as writer:  
        pd.DataFrame.from_dict({a: split_set[a] 
                                for a in ['test_products', 'test_name', 'test_y0', 
                                          'test_y1', 'test_y2', 'test_y3']}) \
            .to_excel(writer, sheet_name='testing_dat')
    #    pd.DataFrame.from_dict(split_set['test_x']).to_excel(writer, sheet_name='vector_embedding')
    with pd.ExcelWriter(f'{inputDir}df_validation.xlsx') as writer:  
        pd.DataFrame.from_dict({a: split_set[a] 
                                for a in ['val_products','val_name', 'val_y0', 
                                          'val_y1', 'val_y2', 'val_y3']}) \
            .to_excel(writer, sheet_name='validation_dat')
    #    pd.DataFrame.from_dict(split_set['val_x']).to_excel(writer, sheet_name='vector_embedding')
    joblib.dump(split_set, f'{inputDir}split_dataset_{pucKind}.joblib')
    return split_set

###############################################################################
#  4a. Feature Selection: Removing with a large fraction of constant values   #
###############################################################################
def model_feature_selection(label='', modelName='', modelType='', estimator=None, xdata_s=None, 
                            ydata_s1=None, xtest_s=None, ytest_s1=None, file_size=None):
    """
    

    Parameters
    ----------
    label : str, optional
        The unique model identifier string. The default is ''.
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    estimator: estimator, required
        The estimator formatted to a set of specifications. The default is None.
    xdata_s : pd.DataFrame, required
        A series of sampled embedded product name vectors for training.
    ydata_s1 : list, required
        A list of PUC labels for training. The default is None.
    xtest_s : np.ndarray, required
        A series of sampled embedded product name vectors for testing.
    ytest_s1 : TYPE, required
        A list of PUC labels for testing. The default is None.
    file_size : num, required
        The size of the dataset in kilobytes. The default is None.
    
    Returns
    -------
    fs : FeatureSelector
        A feature selector with attributes relevant to the PUC model's training.

    """
    
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    #inputDir='models/model'+lab+'/input/'
    compDir='models/model'+lab+'/components/'
    # Define potential feature selection steps
    step1 = {'Constant Features': {'frac_constant_values': 0.95}}
    #step2 = {'Correlated Features': {'correlation_threshold': 0.95}}
    step3 = {'Relevant Features': {'cv': 5,
                                   'estimator': estimator,
                                    'n_estimators': 1000,
                                    'max_iter': 50,
                                    'verbose': 0,
                                    'random_state': 42,
                                    'perc': 80}}
    step4 = {'RFECV Features': {'cv': 2,
                                'estimator': estimator,
                                'step': 50,
                                'scoring': 'accuracy',
                                'verbose': 0}}
    step5 = {'ANOVA Features': {'score_func':f_classif,#chi2,
                                'percentile':25}}
    
    #Select steps based on modelType
    if modelType in ['SVM', 'SGD']:#Cannot do Boruta, so do ANOVA
        steps = [step1,# step2, 
                 step5, step4]
    elif modelType == 'RF':
        steps = [step1,# step2, 
                 step3, step4]
    else:
        print(f"Feature selection steps cannot be determined for model type: {modelType}")
        return None
    
    # Handle large file processing
    #print("Using np.ndarrays instead of pd.DataFrame!")
    #Convert to array to save on memory
    xdata_s = np.asarray(xdata_s)
    xtest_s = np.asarray(xtest_s)
    #print("Scaling data...")
    #Load scaler to normalize data
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    #xdata_s = min_max_scaler.fit_transform(xdata_s)
    xdata_s = np.transpose(min_max_scaler.fit_transform(np.transpose(xdata_s)))
    #xtest_s = min_max_scaler.fit_transform(xtest_s)
    xtest_s = np.transpose(min_max_scaler.fit_transform(np.transpose(xtest_s)))
            
    # Initialize FeatureSelector()
    fs = FeatureSelector()
    print(f'----- Performing {modelName} {modelType} Feature Selection {label} ----- {str(datetime.datetime.now())}')
    fs.fit(xdata_s, ydata_s1, steps)
    #Save feature selector
    joblib.dump(fs, f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
    print(f'Done...Feature Selector Created ----- {str(datetime.datetime.now())}')
    return fs
    
def model_train_selection(label = '', fs=None, modelName='', modelType='', estimator=None, 
                          xdata_s=None, ydata_s1=None, xtest_s=None, ytest_s1=None,
                          file_size=0, n_models=1, parallel=False):
    """
    
    Parameters
    ----------
    label : str, optional
        The unique model identifier string. The default is ''.
    fs : FeatureSelector, required
        A feature selector with attributes relevant to the PUC model's training.
        The default is None.
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    estimator: estimator, required
        The estimator formatted to a set of specifications. The default is None.
    xdata_s : pd.DataFrame, required
        A series of sampled embedded product name vectors for training.
    ydata_s1 : list, required
        A list of PUC labels for training. The default is None.
    xtest_s : np.ndarray, required
        A series of sampled embedded product name vectors for testing.
    ytest_s1 : TYPE, required
        A list of PUC labels for testing. The default is None.
    file_size : num, required
        The size of the dataset in kilobytes. The default is None.   
    n_models : num, optional
        The number of models to train. The default is 1.
    parallel : bool, optional
        Whether to train n_models in parallel or not. The default is False.

    Returns
    -------
    None. All produced objects are cached in the model's directory

    """
    
    print(f'Training {modelName} {modelType}')
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    #inputDir='models/model'+lab+'/input/'
    compDir='models/model'+lab+'/components/'
    outputDir='models/model'+lab+'/output/'
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    #Convert to array to save memory
    xdata_s = np.array(xdata_s)
    xtest_s = np.array(xtest_s)
    #Loop to create n_models
    #https://scikit-image.org/docs/dev/user_guide/tutorial_parallelization.html
    #https://scikit-learn.org/stable/modules/generated/sklearn.utils.parallel_backend.html
    if parallel:
        print('...Training models in parallel...')
        with parallel_backend('loky'):
            Parallel(n_jobs=10)(delayed(model_train)(xdata_s=xdata_s, ydata_s1=ydata_s1, xtest_s=xtest_s, ytest_s1=ytest_s1, 
                                                     min_max_scaler=min_max_scaler, fs=fs, estimator=estimator,
                                                     modelName=modelName, modelType=modelType, i=i, compDir=compDir,
                                                     outputDir=outputDir) for i in range(n_models))
    else:
        print('...Training models in series...')
        for i in range(n_models):
            model_train(xdata_s=xdata_s, ydata_s1=ydata_s1, xtest_s=xtest_s, ytest_s1=ytest_s1, 
                        min_max_scaler=min_max_scaler, fs=fs, estimator=estimator,
                        modelName=modelName, modelType=modelType, i=i, compDir=compDir,
                        outputDir=outputDir)
    
        
def model_train(xdata_s=None, ydata_s1=None, xtest_s=None, ytest_s1=None, 
                min_max_scaler=None, fs=None, estimator=None,
                modelName='', modelType='', i=None, compDir='', outputDir=''):
    """

    Parameters
    ----------
    xdata_s : pd.DataFrame, required
        A series of sampled embedded product name vectors for training.
    ydata_s1 : list, required
        A list of PUC labels for training. The default is None.
    xtest_s : np.ndarray, required
        A series of sampled embedded product name vectors for testing.
    ytest_s1 : TYPE, required
        A list of PUC labels for testing. The default is None.
    min_max_scaler : sklearn.preprocessing.MinMaxScaler, required
        The min_max_scaler that was cached in an earlier step. The default is None.
    fs : FeatureSelector, required
        A feature selector with attributes relevant to the PUC model's training.
        The default is None.
    estimator: estimator, required
        The estimator formatted to a set of specifications. The default is None.
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    i : num, required
        Which model (0 to n_models-1) is being trained. The default is None.
    compDir : str, required
        The model's components directory. The default is ''.
    outputDir : TYPE, optional
        The model's output directory. The default is ''.

    Returns
    -------
    None. All objects produced are cached in the model's directory

    """
    
    #Shuffle between n_models so models are not identical
    if isinstance(xdata_s, list):
        inds = list(range(len(xdata_s)))
        np.random.shuffle(inds)
        xdata_s = [xdata_s[i] for i in inds]
        ydata_s1 = ydata_s1.iloc[inds]
        xdata_s = np.array(xdata_s)
    elif isinstance(xdata_s, np.ndarray):
        inds = list(range(len(xdata_s)))
        np.random.shuffle(inds)
        xdata_s = xdata_s[inds]
        ydata_s1 = ydata_s1.iloc[inds]
    else:
        print("Can't shuffle xdata_s type {type(xdata_s)}")
        return None
        
    # Get selected features
    if fs is None: #Convert to array since no selection
        X_selected_train = xdata_s
        X_selected_test = xtest_s
    else:#Convert to df because selection requires named columns
        X_selected_train = fs.transform(xdata_s)
        X_selected_test = fs.transform(xtest_s)
    #Scale selected data
    # X_selected_train = min_max_scaler.fit_transform(X_selected_train)
    X_selected_train = np.transpose(min_max_scaler.fit_transform(np.transpose(X_selected_train)))
    # X_selected_test = min_max_scaler.fit_transform(X_selected_test)
    X_selected_test = np.transpose(min_max_scaler.fit_transform(np.transpose(X_selected_test)))
    #https://towardsdatascience.com/designing-a-feature-selection-pipeline-in-python-859fec4d1b12
    # Initiate classifier instance
    print(f'Training model {i}: {modelName} ---- {str(datetime.datetime.now())}')
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_{modelType}_{i}.joblib'):
        # Fit classifier (and handle errors)
        try:
            estimator.fit(X_selected_train, ydata_s1)
        except Exception as error:
            if 'got 1 class' in str(error):
                print(f"Only 1 class to train on for {modelName} - saving DummyClassifier")
                estimator = DummyClassifier(strategy="constant", constant=ydata_s1[0])
                estimator.fit(X_selected_train, ydata_s1)        
            else:
                print(f'Unhandled model fitting error: {error}')
                return
                #asdf #Purposefully left to cause stop error to retrace this fit error
         #Cache trained model  
        joblib.dump(estimator, f'{compDir}{slugify(modelName)}_model_{modelType}_{i}.joblib')
    else:
        print(f'{modelName}_{modelType}_{i} found...Loading Saved Estimator...')
        return #Temp control flow stop if model already made, assumes logged
        estimator_size = os.stat(os.path.abspath(f'{compDir}{slugify(modelName)}_model_{modelType}_{i}.joblib')).st_size / 1000
        if estimator_size > 2000000:
            print(f'Estimator too large to load ({estimator_size})...skipping...')
            return
        estimator = joblib.load(f'{compDir}{slugify(modelName)}_model_{modelType}_{i}.joblib')
    
    # Make predictions
    if not hasattr(estimator, 'predict'):
        print('Setting Single Class For Estimator Predictions')
        y_pred_train = [estimator for i in range(len(X_selected_train))]
        y_pred_test = [estimator for i in range(len(X_selected_test))]
        # Measure performance
        accuracy_train = metrics.accuracy_score(ydata_s1, y_pred_train)
        accuracy_test = metrics.accuracy_score(ytest_s1, y_pred_test)
    else:
        y_pred_train = estimator.predict(X_selected_train)
        y_pred_test = estimator.predict(X_selected_test)
        # Measure performance
        accuracy_train = metrics.accuracy_score(ydata_s1, y_pred_train)
        accuracy_test = metrics.accuracy_score(ytest_s1, y_pred_test)
            
    # Message to user
    print(f'The accuracy of the classifier on the train set was: {accuracy_train*100}')
    print(f'The accuracy of the classifier on the test set was: {accuracy_test*100}')
    #Log model accuracies
    export_model_accuracies(outputDir=outputDir, fs=fs, modelName=modelName, 
                            modelType=modelType, n_model=i, accuracy_train=(accuracy_train*100), 
                            accuracy_test=(accuracy_test*100),
                            n_classes=len(estimator.classes_))
    return

def split_puc_tiers(pucKind='all', xdata_s=None, ydata_s0=None, 
                    ydata_s1=None, ydata_s2=None, ydata_s3=None):
    """    

    Parameters
    ----------
    pucKind : str, optional
        A string to filter the input dataframes down to a specific PUC Kind.
        The default is 'all'.
    xdata_s : np.Series or np.ndarray, required
        A series of sampled embedded product name vectors. The default is None.
    ydata_s0 : list, required
        A series of PUC kind labels. The default is None.
    ydata_s1 : list, required
        A series of PUC gen_cat labels. The default is None.
    ydata_s2 : list, required
        A series of PUC prod_fam labels. The default is None.
    ydata_s3 : list, required
        A series of PUC prod_type labels. The default is None.

    Returns
    -------
    models : dict.
        A dictionary of the input data split into named subsets by PUC level.
        
    """

    models = {}
    #Create model dictionary for PUC kind level
    #No need to subset since whole dataset is at the kind level
    models['kind'] = {'X': xdata_s, 'Y': ydata_s0}
    #models[f'gen_cat_{pucKind}'] = {'X': xdata_s, 'Y': ydata_s1}
    
    print("Splitting gen_cat")
    y0_gp = pd.Series(ydata_s0, name='s0').reset_index().groupby('s0')
    for name, group in y0_gp:
        X1 = [i for n, i in enumerate(xdata_s) if n in group.index.values]#group['index'].values]
        Y1 = [i for n, i in enumerate(ydata_s1) if n in group.index.values]#group['index'].values]
        models[name] = {'X': X1, 'Y': Y1}
    
    print("Splitting prod_fam")
    y1_gp = pd.Series(ydata_s1, name='s1').reset_index().groupby('s1')
    for name, group in y1_gp:
        X2 = [i for n, i in enumerate(xdata_s) if n in group.index.values]#group['index'].values]
        Y2 = [i for n, i in enumerate(ydata_s2) if n in group.index.values]#group['index'].values]
        models[name] = {'X': X2, 'Y': Y2}

    y2_gp = pd.Series(ydata_s2, name='s2').reset_index().groupby('s2')
    print("Splitting prod_type")
    for name, group in y2_gp:
        X3 = [i for n, i in enumerate(xdata_s) if n in group.index.values]#group['index'].values]
        Y3 = [i for n, i in enumerate(ydata_s3) if n in group.index.values]#group['index'].values]
        if len(pd.unique(Y3)) == 1:
            models[name] = pd.unique(Y3)[0]
            continue
        models[name] = {'X': X3, 'Y': Y3}
        
    return models

def export_model_accuracies(outputDir, fs, modelName, n_model, 
                            modelType, accuracy_train, accuracy_test,
                            n_classes):
   """
    
    Parameters
    ----------
    outputDir : str, required
        The model's output directory. The default is ''.
    fs : FeatureSelector, required
        A feature selector with attributes relevant to the PUC model's training.
        The default is None.
    modelName : str, required
        The name of the PUC model. The default is ''.
    n_model : num, required
        The model number (0 to n_models-1). The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    accuracy_train : num, required
        The numeric accuracy of the model predicting on the training dataset.
        The default is ''.
    accuracy_test : num, required
        The numeric accuracy of the model predicting on the test dataset.
        The default is ''.
    n_classes : num, required
        The number of classes the model is able to predict. Helps determine which
        models are full models or dummy models.

    Returns
    -------
    None. A log file is made for the input PUC model details

    """
    
   if fs is None:
        n_features = 'All'
   else:
        n_features = len(fs.selected_features)
   output = pd.DataFrame(data={'modelName': [slugify(modelName)],
                               'modelType': modelType,
                               'n_model': n_model,
                               'accuracy_train': [accuracy_train],
                               'accuracy_test': [accuracy_test],
                               'n_features': n_features,
                               'n_classes': n_classes,
                               'timestamp': [pd.to_datetime(str(datetime.datetime.now()), errors='ignore').strftime("%Y-%m-%d %H:%M:%S")]
                        })
    
   output.to_csv(f'{outputDir}logs/{modelType}/model_accuracies_log_{slugify(modelName)}_{modelType}_{n_model}.csv',
                 index=False,
                 date_format='%Y-%m-%d %H:%M:%S')
    
   print('Report Logged...')
    
def combine_model_accuracies_logs(outputDir='', modelType=''):
    """
    
    Parameters
    ----------
    outputDir : str, required
        The model's output directory. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.

    Returns
    -------
    None. All produced objects are saved in the model's directory'
    
    """
    
    print(f'...Combining {modelType} Logs')
    if modelType == 'CV':
        files = os.listdir(f'{outputDir}cross validation')
        loadPath = f'{outputDir}cross validation'
        outPath = f'{outputDir}cross_validation_log.csv'
    else:
        files = os.listdir(f'{outputDir}logs/{modelType}')
        loadPath = f'{outputDir}logs/{modelType}'
        outPath = f'{outputDir}model_accuracies_log_{modelType}.csv'
    
    if len(files) == 0:
        return print('Not logs to combine...')
    else:
        output = pd.concat([pd.read_csv(f'{loadPath}/{i}') for i in files])
        output.to_csv(outPath,
                      index=False,
                      date_format='%Y-%m-%d %H:%M:%S')

def export_model_accuracies_old(outputDir='', fs=None, modelName='', n_model='', modelType='', accuracy_train='', accuracy_test=''):
    """
    Deprecated function used to log model accuracies before a parallel option was added.
    """
    if fs is None:
        n_features = 'All'
    else:
        n_features = len(fs.selected_features)
    output = pd.DataFrame(data={'modelName': [slugify(modelName)],
                                'modelType': modelType,
                                'n_model': n_model,
                                'accuracy_train': [accuracy_train],
                                'accuracy_test': [accuracy_test],
                                'n_features': n_features,
                                'timestamp': [pd.to_datetime(str(datetime.datetime.now()), errors='ignore').strftime("%Y-%m-%d %H:%M:%S")]
                       })
    if not os.path.isfile(f'{outputDir}model_accuracies_log_{modelType}.csv'):
        print("Creating New Report Log")
    else:
        print("Appending Results to Existing Report")
        output = pd.concat([pd.read_csv(f'{outputDir}model_accuracies_log_{modelType}.csv'), output])
    output.to_csv(f'{outputDir}model_accuracies_log_{modelType}.csv',
              index=False,
              date_format='%Y-%m-%d %H:%M:%S')
    print('Report Logged...')

def prep_prediction_clean(sen_itr=None, label=''):
    """
    
    Parameters
    ----------
    sen_itr : str or pd.DataFrame, required
        An input product name string or pd.DataFrame od product names
        To prepare for model predictions. The default is None.
    label : str, optional
        The unique model identifier string. The default is ''.

    Returns
    -------
    sen_vec : pd.DataFrame
        A cleaned, embedded, and scaled pd.DataFrame of product names ready for
        model predictions.

    """
    
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    compDir='models/model'+lab+'/components/'
    # load embeddings
    # doc_embeddings = joblib.load('PUC_doc_embedding' + label + '.joblib')
    #Load embedding model
    doc_embeddings = load_doc_embeddings()
    doc_embeddings.load_state_dict(
        torch.load(compDir + 'PUC_doc_embedding' + lab + '.pt'))
    doc_embeddings.eval()
    
    # clean input
    print('Cleaning input ' + str(datetime.datetime.now()))
    #Convert string input to DataFrame
    if isinstance(sen_itr, str):
        sen_itr = [[sen_itr]]
        sen_itr = [[i] if isinstance(i, str) else i for i in sen_itr]
        sen_itr = [['', i[0]] if len(i) == 1 else i for i in sen_itr]
        sen_itr = pd.DataFrame(sen_itr, columns=['brand_name','title', 'manufacturer'])
    sen_clean = clean_str(sen_itr['brand_name'], sen_itr['title'], sen_itr['manufacturer'])
    #sen_clean = [clean_str(i[0], i[1]) for i in sen_itr]
    #Temporarily removed this logic...20211130 jwall01
    removed = []#[n for n, i in enumerate(sen_clean) if len(i) < 1]
    sen_clean = [i for n, i in enumerate(sen_clean) if n not in removed]
    for i in removed:
        print(f'Invalid name in position {str(i)}, removing from list')
    if len(sen_clean) < 1:
        print('Error: No valid samples found')
        return [], [], [], []
    
    # convert to document embedding
    print('Converting text ' + str(datetime.datetime.now()))
    #Embed into numeric vectors
    sen_vec = [get_vector(i, doc_embeddings) for i in sen_clean]
    print("...Scaling data...")
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    sen_vec = np.transpose(min_max_scaler.fit_transform(np.transpose(sen_vec)))
    # sen_vec = min_max_scaler.fit_transform(sen_vec)

    return sen_vec, sen_clean
    
    
def prep_validation_dataset(df = None, pucKind='all', label='', sample_size='all', bootstrap=False):
    """
    Deprecated function used to prep the validation dataset splitting. 
    Now performed in prep_split_dataset() with the training and test datasets.
    """
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    inputDir='models/model'+lab+'/input/'
    #compDir='models/model'+lab+'/components/'
    sz = len(df) if isinstance(sample_size, str) else sample_size
    sample = df.index.values#np.random.choice(df.index, size=sz, replace=bootstrap)
    xdata_s, ydata_s0, ydata_s1, ydata_s2, ydata_s3 = prep_sample_df(label, sample, df=df)
    xdata_s = xdata_s.astype('float32')
    del bootstrap, sample_size, sample, sz
    
    puc_key = joblib.load(f'{inputDir}puc_key_dict_{pucKind}.joblib')
        
    split_set = {'validate_x':xdata_s, 'validate_y0':ydata_s0, 'validate_y1':ydata_s1,
                 'validate_y2':ydata_s2, 'validate_y3':ydata_s3}
    joblib.dump(split_set, f'{inputDir}validation_split_dataset_{pucKind}.joblib')
    return split_set, puc_key

def select_model_predict(modelName='', model=None, df_input = None, xdata_s=None, 
                         pred_type='pred', min_max_scaler=None, pred_proba=False):
    """
    
    Parameters
    ----------
    modelName : str, required
        The name of the PUC model. The default is ''.
    model : dict, required
        A dictionary that contains the cached model to make predictions with,
        and the associated feature selector. Typically a subset of the output from
        get_model_dict(). The default is None.
    df_input : pd.DataFrame, required
        A DataFrame or product information to append prediction into.
        The default is None.
    xdata_s : pd.DataFrame, required
        Cleaned and vectorized data to make predictions upon. Typically the output
        from prep_prediction_clean(). The default is None.
    pred_type : str, optional
        A string for the column name to append predictions into df_input.
        The default is 'pred'.
    min_max_scaler : sklearn.preprocessing.MinMaxScaler, required
        The min_max_scaler that was cached in an earlier step. The default is None.
    pred_proba : bool, optional
        A boolean for whether to calculate the prediction probability (time intensive).
        The default is False.
    
    Returns
    -------
    df_input : pd.DataFrame
        A modified version of the df_input parameter with model predictions added
        to the pred_type parameter's string column name.

    """
    print(f"Predicting model: {modelName}")
    #Set result as model string name (no predictions to make)
    if isinstance(model, str):
        df_input.loc[:, pred_type] = model
    #Set result as model string name (no predictions to make)
    elif not hasattr(model['estimator'], 'predict'): 
        df_input.loc[:, pred_type] = model['estimator']
    else: #Make predictions using the estimator/feature selector
        #Convert to np.ndarray to save memory    
        xdata_s = np.asarray(xdata_s)
        # Get selected features
        if model['fs'] is None:
            X_selected = xdata_s
        else:
            X_selected = model['fs'].transform(xdata_s)
        # Scale data ROWWISE!!!
        # https://predictivehacks.com/?all-tips=how-to-apply-a-sklearn-scaler-to-rows-of-a-pandas-dataframe
        # X_selected = min_max_scaler.fit_transform(X_selected) - not column-wise default
        X_selected = np.transpose(min_max_scaler.fit_transform(np.transpose(X_selected)))
        # Make predictions
        print(f'...Making predictions...{str(datetime.datetime.now())}')
        df_input.loc[:, pred_type] = model['estimator'].predict(X_selected)
        if pred_proba:
            print(f'...Calculating probabilities...{str(datetime.datetime.now())}')
            tmp = [{i: p[n] for n, i in enumerate(model['estimator'].classes_)}
                              for p in model['estimator'].predict_proba(X_selected)]
            #df_input[f'{pred_type}_proba'] = [tmp[i][df_input[pred_type][df_input.index[i]]] for i,a in enumerate(tmp)]
            df_input.loc[:, f'{pred_type}_proba'] = [tmp[i][df_input[pred_type][df_input.index[i]]] for i,a in enumerate(tmp)]
        print(f'...Done...{str(datetime.datetime.now())}')
        
    return df_input

def get_model_dict(modelName = '', modelType='', n_model='', label='', voting_classifier=False):
    """
    
    Parameters
    ----------
    modelName : str or list, required
        The name (or list of names) of the cached PUC model to be pulled.
        The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    n_model : numeric, optional
        Which model number to pull from cached models. If blank, will attempt
        to load a cached model without a number. The default is ''.
    label : str, optional
        The unique model identifier string. The default is ''.
    voting_classifier : bool, required
        A boolean of whether the models being pulled are VotingClassifiers.
        The default is False.

    Returns
    -------
    model_dict : dict
        A dictionary of cached PUC models with PUC model names as keys. Includes
        the associated feature selector.

    """
    
    compDir='models/model_'+label+'/components/'
    if n_model is None or n_model == '':
        n_model= ''
    else:
        n_model = f'_{n_model}'
        
    model_dict = {}
    if not voting_classifier:
        #Load model and feature selector for a given model and number
        for name in modelName:    
            if not os.path.isfile(f'{compDir}{slugify(name)}_model_{modelType}{n_model}.joblib'):
                model_dict[name] = name
                continue
            else:
                model_dict[name] = {'estimator': joblib.load(f'{compDir}{slugify(name)}_model_{modelType}{n_model}.joblib'),
                                    'fs': joblib.load(f'{compDir}{slugify(name)}_feature_selection_{modelType}.joblib')}
    else:
        #Load Voting Classifier model and feature selector for a given model
        for name in modelName:    
            if not os.path.isfile(f'{compDir}{slugify(name)}_model_VC.joblib'):
                model_dict[name] = name
                continue
            else:
                model_dict[name] = {'estimator': joblib.load(f'{compDir}{slugify(name)}_model_VC.joblib'),
                                    'fs': joblib.load(f'{compDir}{slugify(name)}_feature_selection_{modelType}.joblib')}
    return model_dict

def get_model_feature_selector(modelName = '', modelType='', label=''):
    """
    
    Parameters
    ----------
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    label : str, optional
        The unique model identifier string. The default is ''.

    Returns
    -------
    FeatureSelector
        A feature selector with attributes relevant to the PUC model's training.

    """
    return joblib.load(f'models/model_{label}/components/{slugify(modelName)}_feature_selection_{modelType}.joblib')

def get_model(modelName='', label='', modelType='', n_model=''):
    """

    Parameters
    ----------
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    label : str, optional
        The unique model identifier string. The default is ''.
    n_model : num, required
        The model number (0 to n_models-1). The default is ''.

    Returns
    -------
    sklearn model (SVM, RF, etc.)
        A cached PUC model.

    """
    return joblib.load(f'models/model_{label}/components/{slugify(modelName)}_model_{modelType}_{n_model}.joblib')

def get_puc_by_id(df=None, key=None):
    """
    Function to get PUC string labels based on PUC ID values in the PUC dictionary.
    
    Parameters
    ----------
    df : pd.DataFrame, required
        A DataFrame with PUC ID values. The default is None.
    key : pd.DataFrame, required
        A DataFrame with PUC ID and Value pairs. The default is None.

    Returns
    -------
    pd.DataFrame
        A merged DataFrame of the input df and key parameters, matching PUC ID
        and key values.

    """
    return pd.merge(pd.DataFrame(data=df, columns=['id']), key, 
                    on=['id'], how='left')['Value']

def get_voting_classifier_params(modelName = '', modelType = '', label=''):
    """
    
    Parameters
    ----------
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    label : str, optional
        The unique model identifier string. The default is ''.

    Returns
    -------
    sklearn VotingClassifier
        The VotingClassifier with associated PUC models as parameters.
    pd.DataFrame or pd.Series
        A series of weights matched to PUC models based on logged accuracy.

    """
    compDir=f'models/model_{label}/components/'
    modelName = slugify(modelName)
    files = [f for f in os.listdir(compDir) if re.match(rf'{modelName}_model_{modelType}*', f)]
    files.sort()
    if len(files) == 0:
        print(f"No estimators present for {modelName} {modelType}")
        return None, None
    voting_classifier=[(os.path.splitext(f.replace(f'{modelName}_model_', ''))[0],#Get model name/number
                        joblib.load(f'{compDir}{f}')) for f in files] #Load estimator
    weights = pd.read_csv(f'models/model_{label}/output/model_accuracies_log_{modelType}.csv')
    weights['model_tag'] = weights['modelType'] + '_' + weights['n_model'].astype(str)
    weights = weights.sort_values(by=['modelName', 'model_tag'])
    weights = weights.loc[weights.modelType == modelType]
    weights = weights.loc[weights.modelName == modelName, ['modelType', 'accuracy_test']]
    #Standardize by group size
    weights = weights.groupby('modelType').apply(lambda x: x['accuracy_test']/len(x) / 100)
    if len(weights) != len(voting_classifier):
        #print("Transposing weights")
        weights = weights.transpose()
    if len(weights) != len(voting_classifier):
        print("Error...Weights don't match classifier count...")
    #Combine modelName and n_model column, then sort
    #weights = weights.loc[weights.modelName == modelName, 'accuracy_test']
    return voting_classifier, weights  

def select_voting_classifier_predict(modelName='', modelType='', model=None, df_input=None, 
                                     xdata_s=None, pred_type='pred'):
    """
    A function to make predictions with an input VotingClassifier. Works
    the same way as select_model_predict().
    """
    print(f'Predicting model: {modelName}')
    xdata_s = pd.DataFrame(xdata_s) #Convert to dataframe
    xdata_s.columns = xdata_s.columns.astype(str) #Convert column names
    
    #Need to scale data...
    
    # Get selected features
    if model['fs'] is None:
        X_selected = xdata_s
    else:     
        X_selected = model['fs'].transform(xdata_s)
    # Make predictions
    df_input.loc[:, pred_type] = model['estimator'].predict(X_selected)
    return df_input

def get_prediction_ranks(e, x):
    #https://stackoverflow.com/questions/32461246/how-to-get-top-3-or-top-n-predictions-using-sklearns-sgdclassifier/48572046
    best_n = np.argsort(e.predict_proba(x), axis=1)[:,-len(e.classes_):]
    #https://stackoverflow.com/questions/33529593/how-to-use-a-dictionary-to-translate-replace-elements-of-an-array
    class_dict = {i : e.classes_[i] for i in range(len(e.classes_)) }
    sort_idx = np.argsort(list(class_dict.keys()))
    idx = np.searchsorted(list(class_dict.keys()),best_n,sorter = sort_idx)
    return np.asarray(list(class_dict.values()))[sort_idx][idx]

def select_voting_classifier_train(label = '', fs=None, modelName='', modelType='',
                          xdata_s=None, ydata_s1=None, xtest_s=None, ytest_s1=None,
                          file_size=0, get_cv=False, get_DA=False):
    """
    A function to train a voting classifier. Works the same as
    model_train_selection(), just without parallelization.
    """
    print(f'Training Voting classifier for: {modelName}')
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    #inputDir='models/model'+lab+'/input/'
    compDir='models/model'+lab+'/components/'
    outputDir='models/model'+lab+'/output/'
    
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
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    #X_selected_train = min_max_scaler.fit_transform(X_selected_train)
    X_selected_train = np.transpose(min_max_scaler.fit_transform(np.transpose(X_selected_train)))
    #X_selected_test = min_max_scaler.fit_transform(X_selected_test)
    X_selected_test = np.transpose(min_max_scaler.fit_transform(np.transpose(X_selected_test)))
    #https://towardsdatascience.com/designing-a-feature-selection-pipeline-in-python-859fec4d1b12
    # Initiate classifier instance
    print(f'Training VC model: {modelName} ---- {str(datetime.datetime.now())}')
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_VC.joblib'):
        print('Creating New Voting Classifier...')
        estimators, weights = get_voting_classifier_params(modelName=modelName, 
                                                           modelType=modelType,
                                                           label=label)
        weights = weights[modelType].tolist()
        estimator = VotingClassifier(estimators=estimators, voting='soft', 
                                     weights=weights, n_jobs=10)
        
        #Cross validation if file size isn't too large
        if get_cv:
            print('...performing CV analysis...')
            if file_size < 1500000:
                if not os.path.isfile(f'{outputDir}cross validation/{slugify(modelName)}_VC_CV_scores.csv'):
                    #/home/jwall01/puc_prediction_v3/models/model_FAIO5/output/cross validation/
                    vc_cv = vc_cross_validation(model=estimator, X=X_selected_train,
                                        Y=ydata_s1, cv=5, n_jobs=5)
                    vc_cv.insert(0, 'modelName', pd.Series(modelName))
                    #vc_cv['modelName']=modelName
                    print('...saving VC cv scores...')
                    vc_cv.to_csv(f'{outputDir}cross validation/{slugify(modelName)}_VC_CV_scores.csv')#, index=False)
            else:
                print(f"Skipping CV for {modelName}")
        # Fit classifier
        try:
            estimator.fit(X_selected_train, ydata_s1)
            joblib.dump(estimator, f'{compDir}{slugify(modelName)}_model_VC.joblib')
        except Exception as error:
            print(error)
            if 'excessive memory usage' in str(error) or 'Unable to allocate' in str(error) or 'allocate memory' in str(error):
                print('Handling case where memory usage is too high')
                for i in range(len(estimators)):
                    #Randomly drop an estimator and retry fitting
                    ind = np.random.choice(range(len(estimators)))
                    estimators.remove(estimators[ind])
                    #weights = weights.drop(weights.index[ind])
                    weights.remove(weights[ind])
                    estimator = VotingClassifier(estimators=estimators, voting='soft', 
                                     weights=weights, n_jobs=10)
                    try:
                        estimator.fit(X_selected_train, ydata_s1)
                        print('Large model fit!')
                        joblib.dump(estimator, f'{compDir}{slugify(modelName)}_model_VC.joblib')
                        break
                    except:
                        print("Model memory overload, removing estimator...")
            elif any([type(t[1]).__name__ == 'DummyClassifier' for t in estimators]):
                print('Dummy Classifier present, setting VC to constant')
                estimator = DummyClassifier(strategy="constant", constant=ydata_s1[0])
                estimator.fit(X_selected_train, ydata_s1)
                joblib.dump(estimator, f'{compDir}{slugify(modelName)}_model_VC.joblib')   
            else:
                print(f'Voting Classifier Fit Error for {modelName}. Look into it...')
    else:
        print(f'{slugify(modelName)}_model_VC found...Loading Saved Estimator...')
        estimator_size = os.stat(os.path.abspath(f'{compDir}{slugify(modelName)}_model_VC.joblib')).st_size / 1000
        if estimator_size > 2000000:
            print(f'Estimator too large to load ({estimator_size})...skipping...')
            return
        estimator = joblib.load(f'{compDir}{slugify(modelName)}_model_VC.joblib')
    
    # Make predictions
    if not hasattr(estimator, 'predict'):
        print('Setting Single Class For Estimator Predictions')
        y_pred_train = [estimator for i in range(len(X_selected_train))]
        y_pred_test = [estimator for i in range(len(X_selected_test))]
        # Measure performance
        accuracy_train = metrics.accuracy_score(ydata_s1, y_pred_train)
        accuracy_test = metrics.accuracy_score(ytest_s1, y_pred_test)
    else:
        #Get top prediction
        y_pred_train = estimator.predict(X_selected_train)
        y_pred_test = estimator.predict(X_selected_test)
        # Measure performance
        accuracy_train = metrics.accuracy_score(ydata_s1, y_pred_train)
        accuracy_test = metrics.accuracy_score(ytest_s1, y_pred_test)
    
    #Export accuracy log
    print(f'The accuracy of the classifier on the train set was: {accuracy_train*100}')
    print(f'The accuracy of the classifier on the test set was: {accuracy_test*100}')
    export_model_accuracies(outputDir=outputDir, fs=fs, modelName=modelName, 
                            modelType='VC', n_model=0, accuracy_train=(accuracy_train*100), 
                            accuracy_test=(accuracy_test*100),
                            n_classes=len(estimator.classes_))
    
    #Save Domain of Applicability Report
    if get_DA:
        print('...getting Domain of Applicability results...')
        # Get Prediction Ranks
        y_rank_train = get_prediction_ranks(e=estimator, x=X_selected_train)
        y_rank_test = get_prediction_ranks(e=estimator, x=X_selected_test)
        #Save copy of predictions for applicability domain measuring
        if not hasattr(fs, 'selected_features'):
            beta = []
        else:
            beta = fs.selected_features
        print('Exporting domain of applicability data...')
        report = {'xdata': pd.DataFrame(X_selected_train),
                  'xtest': pd.DataFrame(X_selected_test),
                  'ydata': pd.DataFrame(ydata_s1),
                  'ytest': pd.DataFrame(ytest_s1),
                  'pred_data':pd.DataFrame(y_pred_train),
                  'pred_test':pd.DataFrame(y_pred_test),
                  'rank_data':pd.DataFrame(y_rank_train),
                  'rank_test':pd.DataFrame(y_rank_test),
                  'beta': pd.DataFrame(beta).transpose()}
        with pd.ExcelWriter(f'{outputDir}/domain/{slugify(modelName)}_data.xlsx') as writer:
                for key in report:
                    report[key].to_excel(writer, key)#, index=False)
                writer.save()
    
    return

def create_dummy_model(modelName='', modelType='', n_models=0, constant='',
                       label=''):
    """
    
    Parameters
    ----------
    modelName : str, required
        The name of the PUC model. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    n_models : numeric, optional
        The number of DummyClassifiers to create. The default is 0.
    constant : str, required
        The constant string value the DummyClassifiers should output. 
        The default is ''.
    label : str, optional
        The unique model identifier string. The default is ''.

    Returns
    -------
    None. All objects produced as cached in the model's directory

    """
    
    print(f"Creating fs, dummy estimators or Voting classifier for: {modelName}")
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    outputDir='models/model'+lab+'/output/'
    compDir='models/model'+lab+'/components/'
    
    estimator = DummyClassifier(strategy="constant", constant=constant.lower())
    estimator.fit([0], [constant.lower()])
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib'):
        fs = None
        joblib.dump(fs, f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
    else:
        fs = joblib.load(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
        
    if modelType != 'VC':
        for i in range(n_models):
            if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_{modelType}_{i}.joblib'):
                joblib.dump(estimator, f'{compDir}{slugify(modelName)}_model_{modelType}_{i}.joblib')
                export_model_accuracies(outputDir=outputDir, fs=fs, modelName=modelName, 
                                        modelType=modelType, n_model=i, accuracy_train=100, 
                                        accuracy_test=100,
                                        n_classes=len(estimator.classes_))
    else:
        if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_VC.joblib'):
            joblib.dump(estimator, f'{compDir}{slugify(modelName)}_model_VC.joblib')
            export_model_accuracies(outputDir=outputDir, fs=fs, modelName=modelName, 
                                    modelType=modelType, n_model=0, accuracy_train=100, 
                                    accuracy_test=100,
                                    n_classes=len(estimator.classes_))
            
def run_model_validation(setName='', predKindBool=True, label='', modelType='', 
                         pucKind = 'all', n_model=None, pred_proba=False):
    """
    
    Parameters
    ----------
    setName : str, required
        A str value of 'train', 'test', or 'val', to determine which dataset to
        use for model validation. The default is ''.
    predKindBool : bool, optional
        A boolean of whether to predict the PUC kind or not. The default is True.
    label : str, optional
        The unique model identifier string. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    pucKind : str, optional
        A string to filter the input dataframes down to a specific PUC Kind.
        The default is 'all'.
    n_model : num, required
        The model number (0 to n_models-1). The default is None.
    pred_proba : bool, optional
        A boolean for whether to calculate the prediction probability (time intensive).
        The default is False.

    Returns
    -------
    df_validation_orig : pd.DataFrame
        A DataFrame with validation data and predicted PUC values.
    report : dict
        A dictionary of various reporting metrics based on the model predictions.

    """
    #Load Specified dataset
    if setName not in ['train', 'test', 'val']:
        print("Select allowed setName of: train, test, val")
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    inputDir='models/model'+lab+'/input/'
    outputDir='models/model'+lab+'/output/'
    compDir='models/model'+lab+'/components/'
    
    #Load Cached split
    df_split = joblib.load(f'{inputDir}split_dataset_{pucKind}.joblib')
    #Get product name embeddings
    df_validation = df_split[f'{setName}_x']
    #df_validation=df_validation[0:10,:]
    #Get setName values                    
    key_list = [key for key in df_split.keys() if key.startswith(setName) and '_x' not in key]
    df_split = {key: df_split[key] for key in key_list}
    #Create dataframe of values
    df_validation_orig = pd.DataFrame.from_dict(df_split)
    df_validation_orig = df_validation_orig.rename(columns={f"{setName}_name": "name", f"{setName}_y0": "kind", f"{setName}_y1": "gen_cat", 
                                                            f"{setName}_y2":"prod_fam", f"{setName}_y3":"prod_type"})
    #Add temp ID like a product ID
    df_validation_orig['temp_id'] = np.arange(df_validation_orig.shape[0])
    df_validation_orig['PUC'] = df_validation_orig[['gen_cat', 'prod_fam', 'prod_type']].agg('_'.join, axis=1)
    df_validation_orig['kind'] = df_validation_orig['kind'].str.lower()
    #df_validation_orig = df_validation_orig[0:10]
    
    puc_key_dict = joblib.load(f'{inputDir}puc_key_dict_{pucKind}.joblib')
    puc_key_dict['Value'] = puc_key_dict['Value'].str.lower()
    #Load the data scaler
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    #Boolean whether to predict kind or not
    if predKindBool:
        kind_model = get_model_dict(modelName = ["kind"], modelType=modelType, 
                                    n_model=n_model, label=label, voting_classifier=True)
        print('Gathering predictions for PUC Kind ' + str(datetime.datetime.now()))
        df_validation_orig = select_model_predict(modelName='kind', model=kind_model['kind'], df_input = df_validation_orig.copy(),
                                                  xdata_s=df_validation, pred_type="pred_kind", min_max_scaler=min_max_scaler,
                                                  pred_proba=pred_proba)
        print(f'Done: ---- {str(datetime.datetime.now())}')
        del kind_model
        #Converting to string from puc key
        df_validation_orig['pred_kind']= get_puc_by_id(df_validation_orig['pred_kind'].tolist(), puc_key_dict).str.lower().values
    else:
        df_validation_orig['pred_kind'] = df_validation_orig['kind']
    
    print('Gathering gen_cat predictions ' + str(datetime.datetime.now()))
    gen_cat_models = get_model_dict(modelName = df_validation_orig['pred_kind'].unique(), 
                                    modelType=modelType, n_model=n_model,label=label,
                                    voting_classifier=True)
    pred_groups = {_:x for _, x in df_validation_orig.groupby('pred_kind')}
    #Loop through prediction groups, predict, return list of predictions, concat   
    df_validation_orig = pd.concat([select_model_predict(modelName=x, model=gen_cat_models[x],
                                     df_input=df_validation_orig.loc[df_validation_orig['temp_id'].isin(pred_groups[x]['temp_id'])].copy(),
                                     xdata_s=df_validation[pred_groups[x]['temp_id']],
                                     pred_type='pred_gencat', min_max_scaler=min_max_scaler,
                                     pred_proba=pred_proba) for x in pred_groups.keys()])
    
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del gen_cat_models
    df_validation_orig['pred_gencat'] = pd.concat([puc_key_dict[puc_key_dict.Value == i]['Value'] if isinstance(i, str) else
            puc_key_dict[puc_key_dict.id == i]['Value'] for i in df_validation_orig['pred_gencat']]).values
    print('Gathering prod_fam predictions ' + str(datetime.datetime.now()))
    prod_fam_models = get_model_dict(modelName = df_validation_orig['pred_gencat'].unique(),
                                     modelType=modelType, n_model=n_model, label=label,
                                     voting_classifier=True)
    pred_groups = {_:x for _, x in df_validation_orig.groupby('pred_gencat')}
    #Loop through prediction groups, predict, return list of predictions, concat
    df_validation_orig = pd.concat([select_model_predict(modelName=x, 
                                                         model=prod_fam_models[x],
                                                         df_input=df_validation_orig.loc[df_validation_orig['temp_id'].isin(pred_groups[x]['temp_id'])].copy(),
                                                         xdata_s=df_validation[pred_groups[x]['temp_id']],
                                                         pred_type='pred_prodfam', 
                                                         min_max_scaler=min_max_scaler,
                                                         pred_proba=pred_proba) for x in pred_groups.keys()])
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del prod_fam_models
    #df_validation_orig['pred_prodfam']= get_puc_by_id(df_validation_orig['pred_prodfam'].tolist(), puc_key_dict).str.lower().values
    df_validation_orig['pred_prodfam'] = pd.concat([puc_key_dict[puc_key_dict.Value == i]['Value'] if isinstance(i, str) else
            puc_key_dict[puc_key_dict.id == i]['Value'] for i in df_validation_orig['pred_prodfam']]).values
    print('Gathering prod_type predictions ' + str(datetime.datetime.now()))
    prod_type_models = get_model_dict(modelName = df_validation_orig['pred_prodfam'].unique(),
                                      modelType=modelType, n_model=n_model, label=label,
                                      voting_classifier=True)
    pred_groups = {_:x for _, x in df_validation_orig.groupby('pred_prodfam')}
    #Loop through prediction groups, predict, return list of predictions, concat
    df_validation_orig = pd.concat([select_model_predict(modelName=x, 
                                                         model=prod_type_models[x],
                                     df_input=df_validation_orig.loc[df_validation_orig['temp_id'].isin(pred_groups[x]['temp_id'])].copy(),
                                     xdata_s=df_validation[pred_groups[x]['temp_id']],
                                     pred_type='pred_prodtype', min_max_scaler=min_max_scaler,
                                     pred_proba=pred_proba) for x in pred_groups.keys()])
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del prod_type_models
    df_validation_orig['pred_prodtype'] = pd.concat([puc_key_dict[puc_key_dict.Value == i]['Value'] if isinstance(i, str) else
            puc_key_dict[puc_key_dict.id == i]['Value'] for i in df_validation_orig['pred_prodtype']]).values
        
    df_validation_orig.gen_cat = df_validation_orig.gen_cat.str.lower()
    df_validation_orig.prod_fam = df_validation_orig.prod_fam.str.lower()
    df_validation_orig.prod_type = df_validation_orig.prod_type.str.lower()
    test = df_validation_orig
    #Print metrics (will also be in the returned report)
    print(f"Overall Accuracy (n_products={test.shape[0]})")
    print(f'-kind: {metrics.accuracy_score(test.kind, test["pred_kind"])}') 
    print(f'-gen_cat: {metrics.accuracy_score(test.gen_cat, test["pred_gencat"])}') 
    print(f'-prod_fam: {metrics.accuracy_score(test.prod_fam, test["pred_prodfam"])}')
    print(f'-prod_type: {metrics.accuracy_score(test["prod_type"], test["pred_prodtype"])}')
    for k in test.kind.drop_duplicates():
        t = test[test.kind == k]
        print(f"{k} Accuracy (n_products={t.shape[0]})")
        print(f'-kind: {metrics.accuracy_score(t.kind, t["pred_kind"])}') 
        print(f'-gen_cat: {metrics.accuracy_score(t.gen_cat, t["pred_gencat"])}') 
        print(f'-prod_fam: {metrics.accuracy_score(t.prod_fam, t["pred_prodfam"])}')
        print(f'-prod_type: {metrics.accuracy_score(t["prod_type"], t["pred_prodtype"])}')
        
    print('Done... ' + str(datetime.datetime.now()))
    
    #Select appropriate output file name base on input parameters
    if predKindBool:    
        df_validation_orig.to_csv(f'{outputDir}{label}_predictions_{setName}_predKind_{str(datetime.datetime.now())}.csv')
        reportPath = f'{outputDir}{label}_report_{setName}_predKind_{str(datetime.datetime.now())}.xlsx'
    else:
        df_validation_orig.to_csv(f'{outputDir}{label}_predictions_{setName}_givenKind_{str(datetime.datetime.now())}.csv')
        reportPath = f'{outputDir}{label}_report_{setName}_givenKind_{str(datetime.datetime.now())}.xlsx'
        
    print(f'Writing report...: ---- {str(datetime.datetime.now())}')
    report = get_model_metrics(model_predictions=df_validation_orig)
    for key in report:
        if key == 'accuracies':#Don't transpose the accuracies dataframe
            report[key] = pd.DataFrame.from_dict(report[key])
        else:
            report[key] = pd.DataFrame.from_dict(report[key]).transpose()
    with pd.ExcelWriter(reportPath) as writer:
        for key in report:
            report[key].to_excel(writer, key)
            #pd.DataFrame.from_dict(report[key]).transpose().to_excel(writer, key)
        writer.save()
        
    return df_validation_orig, report


def run_model_prediction(label='', modelType='', n_model=None, pucKind='', df=None, pred_proba=False):
    
    """
    
    Parameters
    ----------
    label : str, optional
        The unique model identifier string. The default is ''.
    modelType : str, required
        A string describing the desired model type (e.g. SVM, RF). The default is ''.
    n_model : num, required
        The model number (0 to n_models-1). The default is None.
    pucKind : str, optional
        A string to filter the input dataframes down to a specific PUC Kind.
        The default is 'all'.
    df : pd.DataFrame, required
        An input DataFrame of products information to predict.
    pred_proba : bool, optional
        A boolean for whether to calculate the prediction probability (time intensive).
        The default is False.

    Returns
    -------
    df : pd.DataFrame
        A modified version of df with predicted PUC values.
    
    """
    if df is None:
        print("...Must pass data to predict...")
        return None
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    inputDir='models/model'+lab+'/input/'
    #outputDir='models/model'+lab+'/output/'
    compDir='models/model'+lab+'/components/'
    #Load the data scaler
    min_max_scaler = joblib.load(f'{compDir}scale{lab}.joblib')
    print("Prepping data: cleaning and embedding...")
    name_vector, name_clean = prep_prediction_clean(sen_itr=df, label=label)
    df['name'] = name_clean
    df['xdata'] = name_vector.tolist()
    
    #Add temp ID like a product ID
    df['temp_id'] = np.arange(df.shape[0])
    
    puc_key_dict = joblib.load(f'{inputDir}puc_key_dict_{pucKind}.joblib')
    puc_key_dict['Value'] = puc_key_dict['Value'].str.lower()
    kind_model = get_model_dict(modelName = ["kind"], modelType=modelType, 
                                n_model=n_model, label=label, voting_classifier=True)
    print('Gathering predictions for PUC Kind ' + str(datetime.datetime.now()))
    df = select_model_predict(modelName='kind', model=kind_model['kind'], df_input = df.copy(),
                                              xdata_s=name_vector, pred_type="pred_kind", min_max_scaler=min_max_scaler,
                                              pred_proba=pred_proba)
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del kind_model
    #Converting to string from puc key
    df['pred_kind']= get_puc_by_id(df['pred_kind'].tolist(), puc_key_dict).str.lower().values
    print('Gathering gen_cat predictions ' + str(datetime.datetime.now()))
    gen_cat_models = get_model_dict(modelName = df['pred_kind'].unique(), 
                                    modelType=modelType, n_model=n_model,label=label,
                                    voting_classifier=True)
    pred_groups = {_:x for _, x in df.groupby('pred_kind')}
    #Loop through prediction groups, predict, return list of predictions, concat
    df = pd.concat([select_model_predict(modelName=x, model=gen_cat_models[x],
                                     df_input=df.loc[df['temp_id'].isin(pred_groups[x]['temp_id'])].copy(),
                                     xdata_s=name_vector[pred_groups[x]['temp_id']],
                                     pred_type='pred_gencat', min_max_scaler=min_max_scaler,
                                     pred_proba=pred_proba) for x in pred_groups.keys()])
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del gen_cat_models
    df['pred_gencat'] = pd.concat([puc_key_dict[puc_key_dict.Value == i]['Value'] if isinstance(i, str) else
            puc_key_dict[puc_key_dict.id == i]['Value'] for i in df['pred_gencat']]).values
    print('Gathering prod_fam predictions ' + str(datetime.datetime.now()))
    prod_fam_models = get_model_dict(modelName = df['pred_gencat'].unique(),
                                     modelType=modelType, n_model=n_model, label=label,
                                     voting_classifier=True)
    pred_groups = {_:x for _, x in df.groupby('pred_gencat')}
    #Loop through prediction groups, predict, return list of predictions, concat
    df = pd.concat([select_model_predict(modelName=x, model=prod_fam_models[x],
                                     df_input=df.loc[df['temp_id'].isin(pred_groups[x]['temp_id'])].copy(),
                                     xdata_s=name_vector[pred_groups[x]['temp_id']],
                                     pred_type='pred_prodfam', min_max_scaler=min_max_scaler,
                                     pred_proba=pred_proba) for x in pred_groups.keys()])
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del prod_fam_models
    df['pred_prodfam'] = pd.concat([puc_key_dict[puc_key_dict.Value == i]['Value'] if isinstance(i, str) else
            puc_key_dict[puc_key_dict.id == i]['Value'] for i in df['pred_prodfam']]).values
    print('Gathering prod_type predictions ' + str(datetime.datetime.now()))
    prod_type_models = get_model_dict(modelName = df['pred_prodfam'].unique(),
                                      modelType=modelType, n_model=n_model, label=label,
                                      voting_classifier=True)
    pred_groups = {_:x for _, x in df.groupby('pred_prodfam')}
    #Loop through prediction groups, predict, return list of predictions, concat
    df = pd.concat([select_model_predict(modelName=x, model=prod_type_models[x],
                                     df_input=df.loc[df['temp_id'].isin(pred_groups[x]['temp_id'])].copy(),
                                     xdata_s=name_vector[pred_groups[x]['temp_id']],
                                     pred_type='pred_prodtype', min_max_scaler=min_max_scaler,
                                     pred_proba=pred_proba) for x in pred_groups.keys()])
    print(f'Done: ---- {str(datetime.datetime.now())}')
    del prod_type_models
    df['pred_prodtype'] = pd.concat([puc_key_dict[puc_key_dict.Value == i]['Value'] if isinstance(i, str) else
            puc_key_dict[puc_key_dict.id == i]['Value'] for i in df['pred_prodtype']]).values
            
    return df

#A function to run accuracy, precision, recall, and F-test metrics on model predictions
def get_model_metrics(model_predictions=None):
    """
    
    Parameters
    ----------
    model_predictions : pd.DataFrame, required
        A DataFrame with model predictions and actual product PUC label.
        The default is None.

    Returns
    -------
    reportList : dict
        A dictionary of dictionaries and DataFrames with various model metric
        data.

    """
    #Prepare dictionary of PUC levels and associated columns to run metrics
    levelList = {'kind': {'true':model_predictions.kind, 
                          'predicted':model_predictions.pred_kind,
                          'labels':model_predictions.kind.drop_duplicates().tolist().sort()},#None},
                 'gen_cat':{'true':model_predictions.gen_cat,
                            'predicted':model_predictions.pred_gencat,
                            'labels':model_predictions.gen_cat.drop_duplicates().tolist().sort()},#None},
                 'prod_fam':{'true':model_predictions.prod_fam,
                             'predicted':model_predictions.pred_prodfam,
                            'labels':model_predictions.prod_fam.drop_duplicates().tolist().sort()},#None},
                 'prod_type':{'true':model_predictions.prod_type,
                             'predicted':model_predictions.pred_prodtype,
                            'labels':model_predictions.prod_type.drop_duplicates().tolist().sort()},#None},
                 }
    
    reportList = {}
    #Generate reports by PUC level
    for l in levelList.keys():
        true=levelList[l]['true']
        predicted=levelList[l]['predicted']
        labels=levelList[l]['labels']

        reportList[l] = classification_report(true, predicted, 
                                              target_names=labels,
                                              output_dict=True)
    
    #Creating dataframe of accuracy metrics overall and by kind
    accuracyList = {}
    for t in ['Overall', 'ar', 'fo', 'oc', 'na']:    
        report = {'accuracy_level': [t, t, t, t],
                  'PUC_level': ["kind", "gen_cat", "prod_fam", "prod_type"]}
        if t == 'Overall':
            test = model_predictions
        else:
            test = model_predictions[model_predictions.kind == t]
        report['value'] = [metrics.accuracy_score(test[p], test["pred_"+p.replace('_', '')]) for p in report['PUC_level']]
        report['n_products'] = [test.shape[0] for p in report['PUC_level']]
        accuracyList[t] = report
    reportList['accuracies'] = pd.concat([pd.DataFrame.from_dict(accuracyList[x]) for x in accuracyList])
    
    return reportList

def vc_cross_validation(model=None, X=None, Y = None, cv=5, n_jobs=1):
    #https://scikit-learn.org/stable/modules/cross_validation.html
    #Split the training data for the VC into 5 folds
    #Output a log of the cross validation score (combine into report)
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    print('...performing cross validation on VC...')
    scoring = ['balanced_accuracy', 'precision_macro', 'recall_macro', 
               'f1_macro']#, 'roc_auc']
    
    scores = cross_validate(model, X, Y, scoring=scoring, cv=cv, n_jobs=n_jobs)
    tmp = pd.DataFrame.from_dict(scores).mean(axis=0)
    
    return pd.DataFrame(tmp).transpose()

def format_prediction_input(X):
    #Convert all to DataFrame if not DataFrame. Replace None with "".
    #Handle if not already a DataFrame
    if X is None:
        return None
    
    if not isinstance(X, pd.DataFrame):
        if not isinstance(X, dict):
            #If string, make tuple with empty brand/manufacturer
            if isinstance(X, str):
                X = (X, "", "")
            if not isinstance(X, list):
                X = [X]
            else: #Convert list of strings to tuples with empty brand/manufacturer
                X = [x if not isinstance(x, str) else (x, "", "") for x in X]
            df = pd.DataFrame(X,
                              columns = ['title', 'brand_name', 'manufacturer'])
        else:
            df = pd.DataFrame.from_dict(X)
    else:
        df = X
    
    if not set(['title','brand_name', 'manufacturer']).issubset(df.columns):
        print("Input dataframe must have title, brand_name, and manufacturer columns (even if blank)")
        return None
    #Fill missing values with empty string
    df = df.fillna("")
    #Add temp ID like a product ID
    df['temp_id'] = np.arange(df.shape[0])
    return df
    
