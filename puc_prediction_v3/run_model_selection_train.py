
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Split dataset, train individual models, train voting classifiers, evaluate performance.

Created on Thu Feb  4 13:05:51 2021

@author: jwall01
"""
#Import packages and functions
from puc_model.data_processing import (load_df)
from puc_model.model_utils import (prep_puc_key, prep_split_dataset, model_feature_selection, 
                               split_puc_tiers, convert_PUC_numeric, model_train_selection,
                               slugify, get_modeltype_estimator,
                               create_dummy_model, get_model, select_voting_classifier_train,
                               run_model_validation, combine_model_accuracies_logs,
                               find_best_sgd_svm_estimator)
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn import preprocessing
import numpy as np
import datetime
import joblib
import os

#Set parameters
label = 'envTest' #Unique identifier for the model
pucKind = 'all'#'FO'
modelType = 'SGD'#'SVM' #Model Type (e.g. SVM, RF, SGD)
n_models=5 #Number of models to train for Voting Classification
inputDir='models/model_'+label+'/input/'
compDir='models/model_'+label+'/components/'
outputDir='models/model_'+label+'/output/'
del_models = False #Boolean to delete models (quick reset)
parallel = True #Boolean to train n_models in parallel
get_fs = True#False
get_cv=True#False
get_DA=True#False
setName='val'
predKindBool=True#False
pred_proba=True

if not get_fs and modelType != 'SGD':
    print("get_fs set to False is only recommended for SGD models...")
    quit()

#Create log directories to export reports
if not os.path.isdir(f'{outputDir}logs'):
    os.makedirs(f'{outputDir}logs')
    os.makedirs(f'{outputDir}logs/SVM')
    os.makedirs(f'{outputDir}logs/VC')
    os.makedirs(f'{outputDir}logs/SGD')

#Set/dump or load minmax scaler for all models to use
if not os.path.isfile(f'{compDir}scale_{label}.joblib'):
    min_max_scaler = preprocessing.MinMaxScaler()
    joblib.dump(min_max_scaler, f'{compDir}scale_{label}.joblib')
    #joblib.dump(label, f'{compDir}scale_.joblib')
else:
    min_max_scaler = joblib.load(f'{compDir}scale_{label}.joblib')
       
#Prep dataset or load already cached data
if not os.path.isfile(f'{inputDir}puc_tiers_datasets_{pucKind}.joblib'):
    print('Pulling and splitting data')
    df = load_df(label=label) #Load cleaned data
    df = df.replace(np.nan, 'NA', regex=True)
    #Concat to make PUC grouping variable
    df['PUC'] = df[['gen_cat', 'prod_fam', 'prod_type']].agg('_'.join, axis=1)
    
    #Remove 10% of data for validation
    if not os.path.isfile(f'models/model_{label}/input/df_training_{label}_{pucKind}.joblib'):
        #Split datasets into 90% training/testing vs. 10% validation datasets
        df_90, df_10 = train_test_split(df, test_size=0.1, 
                                        stratify=df['PUC'], 
                                        random_state=12345)
        #Cache datasets
        joblib.dump(df_90, f'models/model_{label}/input/df_training_{label}_{pucKind}.joblib')
        joblib.dump(df_10, f'models/model_{label}/input/df_validation_{label}_{pucKind}.joblib')
    else:
        df_90 = joblib.load(f'models/model_{label}/input/df_training_{label}_{pucKind}.joblib')
        df_10 = joblib.load(f'models/model_{label}/input/df_validation_{label}_{pucKind}.joblib')
    #Prep Test, Training, and Validation datasets (get puc_key_dict and splits)
    puc_key_dict = prep_puc_key(label=label, pucKind=pucKind)
    df_split = prep_split_dataset(df = df_90, df_val=df_10, label=label, pucKind=pucKind)
    del df, df_90#, groups
    #Split datasets into PUC subsets
    puc_tiers_train = split_puc_tiers(pucKind=pucKind, 
                                      xdata_s=df_split['train_x'], 
                                      ydata_s0=df_split['train_y0'], 
                                      ydata_s1=df_split['train_y1'], 
                                      ydata_s2=df_split['train_y2'], 
                                      ydata_s3=df_split['train_y3'])
    puc_tiers_test = split_puc_tiers(pucKind, 
                                     df_split['test_x'], 
                                     df_split['test_y0'], 
                                     df_split['test_y1'], 
                                     df_split['test_y2'],
                                     df_split['test_y3'])
    #Save split sets
    joblib.dump([puc_tiers_train, puc_tiers_test], f'{inputDir}puc_tiers_datasets_{pucKind}.joblib')
    del df_split
    #Subsetting puc_tier dictionaries
    #Cache all split PUC subsets
    print('Dumping Test PUC Tiers')
    for p in puc_tiers_test.keys():
        if not os.path.isfile(f'{compDir}{slugify(p)}_test_data.joblib'):    
            joblib.dump(puc_tiers_test[p], f'{compDir}{slugify(p)}_test_data.joblib')
    del puc_tiers_test
    print('Dumping Train PUC Tiers')
    for p in puc_tiers_train.keys():
        if not os.path.isfile(f'{compDir}{slugify(p)}_train_data.joblib'):
            joblib.dump(puc_tiers_train[p], f'{compDir}{slugify(p)}_train_data.joblib')
    del puc_tiers_train
else:
    print('Data already pulled and split...loading joblib file')
    puc_key_dict = joblib.load(f'{inputDir}puc_key_dict_{pucKind}.joblib')

#Loop through all PUC levels, feature select, train model, and test model
#Adding kind manually since missing from puc_key_dict.Value
for modelName in sorted(puc_key_dict.Value, reverse=True) + ['kind']:
    #Optionally delete models and feature selectors (reset run)
    if del_models:
        for a in range(n_models):
            if os.path.isfile(f'{compDir}{slugify(modelName)}_model_{modelType}_{a}.joblib'):
                os.remove(f'{compDir}{slugify(modelName)}_model_{modelType}_{a}.joblib')
        if os.path.isfile(f'{compDir}{slugify(modelName)}_model_VC.joblib'):
            os.remove(f'{compDir}{slugify(modelName)}_model_VC.joblib')
        #if(os.path.isfile(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')):
        #    os.remove(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
        if os.path.isfile(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib'):
            os.remove(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
        print(f'{modelName} {modelType} and VC models deleted...')
        continue
    #Check if all individual models are made
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_{modelType}_{n_models-1}.joblib'):
        print(f'--- Model {modelName} ---')
        #Check if there's training data for a PUC level
        if not os.path.isfile(f'{compDir}{slugify(modelName)}_train_data.joblib'):
            continue
        #Pull datasets
        puc_tiers_train = joblib.load(f'{compDir}{slugify(modelName)}_train_data.joblib')
        puc_tiers_test = joblib.load(f'{compDir}{slugify(modelName)}_test_data.joblib')
        file_size = os.stat(os.path.abspath(f'{compDir}{slugify(modelName)}_train_data.joblib')).st_size / 1000
        
        #If training data is a string, create a dummy model to return that string
        #If training data only has 1 classification, create dummy model
        if isinstance(puc_tiers_train, str) or len(set(puc_tiers_train['Y'])) == 1:
            if isinstance(puc_tiers_train, dict): #Convert to string and get the value (all the same)
                puc_tiers_train = puc_tiers_train['Y'][0]
            create_dummy_model(modelName=modelName, modelType=modelType, n_models=n_models, 
                               constant=puc_tiers_train, label=label)
            continue
        
        #Special GirdSearch Hyperparameter tuning for SGD
        if modelType == 'SGD': 
            try:
                print('...Attempting grid search to find optimal model for feature selection')
                X = min_max_scaler.fit_transform(puc_tiers_train['X'])
                y = convert_PUC_numeric(puc_tiers_train['Y'], 
                                        puc_key_dict)
                estimator = find_best_sgd_svm_estimator(X, y, 
                                                        StratifiedKFold(n_splits=5).split(X, y),
                                                        random_seed=42, n_jobs=50)
            except:# Exception as error:
                print("...GridSearch Error, using default SGD...")
                estimator, modelType = get_modeltype_estimator(modelType=modelType, file_size=file_size)
        else:
            #Get estimator and model type based on file_size (larger files need special treatment)
            estimator, modelType = get_modeltype_estimator(modelType=modelType, file_size=file_size)
        
        #Convert PUC classification to numeric value from dictionary
        #Eventually move this into the model_feature_selection and train methods...
        puc_tiers_train['Y'] = convert_PUC_numeric(puc_tiers_train['Y'], 
                                                              puc_key_dict)
        puc_tiers_test['Y'] = convert_PUC_numeric(puc_tiers_test['Y'], 
                                                             puc_key_dict)
        
        #Check for feature selector
        if not os.path.isfile(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib'):
            #Set fs to None if get_fs is False or only 1 class to predict
            if (not get_fs and modelName not in ['fo', 'kind']) or len(puc_tiers_test['Y'].unique()) == 1:# or file_size > 1000000:
                #print('No selection necessary with 1 class')# OR file_size too large')
                fs = None #Create dummy feature selector
                joblib.dump(fs, f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
            else:
                print('Performing Feature Selection')
                fs = model_feature_selection(label=label, 
                                             modelName = modelName, 
                                             modelType=modelType,
                                             estimator=estimator,
                                             xdata_s=puc_tiers_train['X'],
                                             ydata_s1=puc_tiers_train['Y'],
                                             xtest_s=puc_tiers_test['X'],
                                             ytest_s1=puc_tiers_test['Y'],
                                             file_size = file_size)
        else:
            print("Loading Saved Feature Selector")
            fs = joblib.load(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
        
        #kind data too large and often crashes in parallel unless SGD model
        if modelName == 'kind' and modelType != 'SGD':
            parallel = False
        else:
            parallel = True
        
        #Find new optimized hyperparameters for selected features for SGD model
        if modelType == 'SGD': 
            if fs is not None:
                try:
                    print('...Attempting grid search to find optimal model for model training')
                    X = fs.transform(np.array(puc_tiers_train['X'])) #Select features
                    X = min_max_scaler.fit_transform(X) #Minmax scale
                    y = puc_tiers_train['Y']
                    
                    estimator = find_best_sgd_svm_estimator(X, y, 
                                                            StratifiedKFold(n_splits=5).split(X, y),
                                                            random_seed=42, n_jobs=50)
                except:# Exception as error:
                    print("...GridSearch Error, using default SGD...")
                    estimator, modelType = get_modeltype_estimator(modelType=modelType, file_size=file_size)
                
        #Train n_models (parallel or series) for PUC level using feature selector
        model_train_selection(label = label, fs=fs, modelName=modelName, 
                              modelType=modelType, estimator=estimator, 
                              xdata_s=puc_tiers_train['X'],
                              ydata_s1=puc_tiers_train['Y'],
                              xtest_s=puc_tiers_test['X'],
                              ytest_s1=puc_tiers_test['Y'],
                              file_size=file_size,
                              n_models=n_models,
                              parallel=parallel)        

    else:
        print(f'Model {modelName} already trained and reported...')
        #Checks for models that were made incorrectly
        for a in range(n_models):#Clear out where previously made int/str dummy models without predict attribute
            if os.path.isfile(f'{compDir}{slugify(modelName)}_model_{modelType}_{a}.joblib'):
                tmp = get_model(modelName=modelName, label=label, modelType=modelType, n_model=a)
                if not hasattr(tmp, 'predict'):
                    #Delete any cached models without prediction capabilities
                    print(f'Removing string model: {modelName}_model_{modelType}_{a}')
                    os.remove(f'{compDir}{slugify(modelName)}_model_{modelType}_{a}.joblib')
       
        if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_{modelType}_{n_models-1}.joblib'):
           print(f'All {modelName} models deleted due to not having a predict attribute')
           continue
       
print(f"Done training invidiual {modelType} models: ---- {str(datetime.datetime.now())}")
#Combine individually logged model accuracies for modelType
combine_model_accuracies_logs(outputDir=outputDir, modelType=modelType)
print("Starting VC model training...")
#Separate Voting Classifier Loop due to n_models parallel training not always finishing together
for modelName in sorted(puc_key_dict.Value, reverse=True) + ['kind']:
    #Check for PUC training data
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_train_data.joblib'):
        continue
    #Check if a Voting Classifier already exists
    if not os.path.isfile(f'{compDir}{slugify(modelName)}_model_VC.joblib'):
        #Load all necessary data and inputs
        fs = joblib.load(f'{compDir}{slugify(modelName)}_feature_selection_{modelType}.joblib')
        puc_tiers_train = joblib.load(f'{compDir}{slugify(modelName)}_train_data.joblib')
        puc_tiers_test = joblib.load(f'{compDir}{slugify(modelName)}_test_data.joblib')
        file_size = os.stat(os.path.abspath(f'{compDir}{slugify(modelName)}_train_data.joblib')).st_size / 1000
        #Create a dummy Voting Classifier if training data is a string
        if isinstance(puc_tiers_train, str) or len(set(puc_tiers_train['Y'])) == 1:
            if isinstance(puc_tiers_train, dict): #Convert to string and get the value (all the same)
                puc_tiers_train = puc_tiers_train['Y'][0]
            create_dummy_model(modelName=modelName, modelType="VC", n_models=0, 
                               constant=puc_tiers_train, label=label)
            continue
        #Convert PUC classification to numeric value from dictionary
        puc_tiers_train['Y'] = convert_PUC_numeric(puc_tiers_train['Y'], 
                                                              puc_key_dict)
        puc_tiers_test['Y'] = convert_PUC_numeric(puc_tiers_test['Y'], 
                                                              puc_key_dict)
        if file_size > 250000: #Large training sets usually killed for DA
            get_DA = False
        print(f'Fitting Voter Classifier for {modelName}')
        select_voting_classifier_train(label = label, fs=fs, modelName=modelName, 
                                       modelType=modelType,
                                       xdata_s=puc_tiers_train['X'],
                                       ydata_s1=puc_tiers_train['Y'],
                                       xtest_s=puc_tiers_test['X'],
                                       ytest_s1=puc_tiers_test['Y'],
                                       file_size=file_size,
                                       get_cv=get_cv, get_DA=get_DA)
    else:
        print(f'Voting Classifier already created for {modelName}')

#Combine individually logged model accuracies for VC models
combine_model_accuracies_logs(outputDir=outputDir, modelType='VC')
#Combine cross validation logs
combine_model_accuracies_logs(outputDir=outputDir, modelType='CV')
print(f'Done: ---- {str(datetime.datetime.now())}')
#
#
#####################################
#####################################
#
#
#Validation Testing
print(f'Running validation...: ---- {str(datetime.datetime.now())}')
#Run validation and get reporting metrics (all results are cached)
df_validation_orig, report = run_model_validation(setName=setName, predKindBool=predKindBool, label=label, 
                                                  modelType=modelType, pucKind = pucKind, n_model=None,
                                                  pred_proba=pred_proba)

#Test filtering output to 80% predicted probability threshold
# test = df_validation_orig.loc[(df_validation_orig.pred_kind_proba > 0.8) &
#                               (df_validation_orig.pred_gencat_proba > 0.8) &
#                               (df_validation_orig.pred_prodfam_proba > 0.8) &
#                               (df_validation_orig.pred_prodtype_proba > 0.8)]
print(f'Done: ---- {str(datetime.datetime.now())}')