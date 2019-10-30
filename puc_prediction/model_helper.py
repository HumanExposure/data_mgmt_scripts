# -*- coding: utf-8 -*-
"""Predict a PUC from a string.

@author: SBURNS
"""

from data_processing import clean
from puc_model import get_vector, build_model
import joblib
import pandas as pd
import numpy as np
import os


def clean_str(brand, title):
    """Clean a product brand and name to prepare it for the model."""
    brand = brand.strip().lower()
    title = title.strip().lower()
    brand = '' if brand in ['generic', 'unknown'] else brand
    name = clean(brand, title)
    return name


def model_predict(sen_vec, pkey, label=''):
    """Load model and predict PUCS.

    Args:
        sen_vec (list): List of word embeddings.
        pkey(pd.DataFrame): Dataframe matching classes back to PUCS.
        label (str, optional): File label. Defaults to ''.

    Returns:
        puclist (list): List of list with PUC info.

    """
    # load models
    print('Loading model data')
    label = '' if len(label) == 0 else '_' + label.strip('_')
    clf = joblib.load('PUC_model1' + label + '.joblib')
    clf_d2 = joblib.load('PUC_model2_dict' + label + '.joblib')
    clf_d3 = joblib.load('PUC_model3_dict' + label + '.joblib')

    # use model
    print('Gathering pedictions')
    pred1 = clf.predict(sen_vec)
    pred2 = [clf_d2[pred1[n]] if type(clf_d2[pred1[n]]) == str else
             clf_d2[pred1[n]].predict([i])[0] for n, i in enumerate(sen_vec)]

    pred3 = [clf_d3[pred2[n]] if type(clf_d3[pred2[n]]) == str else
             clf_d3[pred2[n]].predict([i])[0] for n, i in enumerate(sen_vec)]

    puclist = [pkey.loc[i].to_list() for i in pred3]

    return puclist


def model_run(sen_itr, label=''):
    """Clean the new data and run the model.

    Args:
        sen_itr (list or array): List of ['brand', 'title'].
        label (str, optional): File label. Defaults to ''.

    Returns:
        all_list (list): List of product pucs

    """
    doc_embeddings = joblib.load('PUC_doc_embedding.joblib')
    pkey = pd.read_csv('PUC_key.csv', index_col='cat').fillna('')

    # clean input
    print('Cleaning input')
    if type(sen_itr) == str:
        sen_itr = [[sen_itr]]
    sen_itr = [[i] if type(i) == str else i for i in sen_itr]
    sen_itr = [['', i[0]] if len(i) == 1 else i for i in sen_itr]
    sen_clean = [clean_str(i[0], i[1]) for i in sen_itr]

    # checks for number of model run
    num_runs = 0
    for i in range(len(os.listdir())):
        lab = label + '_' + str(i)
        lab = '' if len(lab) == 0 else '_' + lab.strip('_')
        fname = 'PUC_model1' + lab + '.joblib'
        if os.path.exists(fname):
            num_runs += 1
        else:
            print(str(num_runs) + ' runs detected')
            break
    if num_runs == 0:
        print('Please build the model or change the label parameter')
        return []

    # convert to document embedding
    print('Converting text')
    sen_vec = [get_vector(i, doc_embeddings) for i in sen_clean]

    minmax = joblib.load('scale.joblib')
    sen_vec = minmax.transform(sen_vec)

    puc_pred = []
    for n in range(num_runs):
        lab = label + '_' + str(n)
        print('----- Predicting ' + lab + ' -----')
        puclist = model_predict(sen_vec, pkey, lab)
        puc_pred.append(puclist)
    all_list = pd.DataFrame(puc_pred).mode().values[0]

    return all_list


def model_build(df, df_train, bootstrap=False, num_runs=1,
                sample_size='all', label='', probab=False):
    """Generate the model.

    xdata.joblib should already exist. To get more control over the model, run
    build_model directly.

    Args:
        df (pd.DataFrame): Dataframe from data processing script.
        df_train (pd.DataFrame): Training subset of df.
        bootstrap (bool, optional): Whether to sample with replacement or not.
            Defaults to False.
        num_runs (int, optional): Number of runs to aggregate. Defaults to 1.
        sample_size (int, str, optional): Size of training set for each run,
            sampled from the training set. Defaults to 'all'.
        label (str, optional): File label. Defaults to ''.
        probab (bool, optional): Whether to calculate class probability.

    """
    sz = len(df_train) if type(sample_size) == str else sample_size

    for n in range(num_runs):
        lab = label + '_' + str(n)
        print('----- Training ' + lab + ' -----')
        boot_sample = np.random.choice(df_train.index, size=sz,
                                       replace=bootstrap)
        build_model(df, label=lab, sample=boot_sample, proba=probab)
