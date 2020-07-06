# -*- coding: utf-8 -*-
"""Train model.

@author: scott
"""

# import pandas as pds
import os
from sklearn import svm
import joblib
import numpy as np
from sklearn import preprocessing
from embeddings import cosine_function


def build_model(data, embed_dict, label='',
                nrun='0', sample='all', proba=False, cosine=False,
                original_dict=None):
    """Build models.

    Builds the and saves the models for predicting the PUCs.
    Args:
        label (str, optional): File labels. Defaults to ''.
        nrun (str, optional): Run number for label. Defaults to '0'.
        sample (optional): Specifies how to sample the data. See script for
            details. Defaults to 'all'.
        proba (bool): Whether to calculate probabilities.
    Returns:
        None.

    """
    print('building model')
    label = '' if len(label) == 0 else '_' + label.strip('_')
    lab = label + '_' + nrun

    xdata = prepare_data(data, embed_dict, label, cosine=cosine,
                         original_dict=original_dict)
    ydata = data['harmonized_funcuse'].str.strip().to_list()

    if isinstance(sample, str):
        print('Using all data')
        xdata_s = xdata
        ydata_s1 = ydata
    else:
        if isinstance(sample, list) or isinstance(sample, np.ndarray):
            print('Using provided index')
            inds = sample
        else:
            print('Picking ' + str(sample) + ' random samples')
            inds = np.random.randint(0, len(data), sample)
            # note: this samples with replacement
        xdata_s = [xdata[i] for i in inds]
        ydata_s1 = [ydata[i] for i in inds]

    # c parameter values
    cval1 = 500

    # fit gen_cat model
    print('Fitting data...')
    clf = svm.SVC(gamma='scale', decision_function_shape='ovo',
                  cache_size=20000, kernel='linear', C=cval1,
                  probability=proba, class_weight='balanced')
    clf.fit(xdata_s, ydata_s1)

    print('Done')
    joblib.dump(clf, os.path.join('store', 'OECD_model' + lab + '.joblib'))


def prepare_data(df, embed_dict, label, cosine, original_dict):
    """Prepare training data for model."""
    print('Preparing data for model...')
    if not cosine:
        xdata = df['clean_funcuse_hash'].apply(lambda x:
                                               embed_dict[x[0]][0]).to_list()
    else:
        xdata = cosine_function(df, original_dict, embed_dict,
                                label, reset=False)

    min_max_scaler = preprocessing.MinMaxScaler()
    xdata = min_max_scaler.fit_transform(xdata)
    joblib.dump(min_max_scaler, os.path.join('store',
                                             'scale' + label + '.joblib'))
    print('Done')
    return xdata
