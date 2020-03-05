# -*- coding: utf-8 -*-
"""Build and save the model files.

@author: SBURNS
"""

# https://github.com/zalandoresearch/flair/blob/master/resources/docs/

import pandas as pd
from flair.embeddings import (WordEmbeddings, FlairEmbeddings,
                              DocumentPoolEmbeddings, Sentence,
                              BytePairEmbeddings)
from sklearn import svm
import joblib
import numpy as np


def load_model():
    """Load word embeddings model."""
    fasttext_embedding = WordEmbeddings('en-crawl')
    byte_embedding = BytePairEmbeddings('en')
    flair_embedding_forward = FlairEmbeddings('en-forward')
    flair_embedding_backward = FlairEmbeddings('en-backward')

    document_embeddings = DocumentPoolEmbeddings([fasttext_embedding,
                                                  byte_embedding,
                                                  flair_embedding_backward,
                                                  flair_embedding_forward],
                                                 fine_tune_mode='nonlinear')
    return document_embeddings


def get_vector(sen, document_embeddings):
    """Get the document vector for input."""
    sentence = Sentence(sen)
    document_embeddings.embed(sentence)
    get_embed = sentence.get_embedding().detach()
    if get_embed.device.type == 'cuda':
        return get_embed.cpu().numpy()
    return get_embed.numpy()


def build_model(label='', nrun='0', sample='all', proba=False):
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

    df = joblib.load('training_data' + label + '.joblib')

    data = df[['name', 'gen_cat', 'prod_fam',
               'prod_type']].copy()

    xdata = joblib.load('xdata' + label + '.joblib')

    ydata1 = (data['gen_cat']).str.strip().to_list()

    ydata2 = (data['gen_cat'] + ' ' + data['prod_fam'].fillna('none')) \
        .str.strip().to_list()

    ydata3 = (data['gen_cat'] + ' ' + data['prod_fam'].fillna('none') + ' ' +
              data['prod_type'].fillna('none')).str.strip().to_list()

    if isinstance(sample, str):
        print('Using all data')
        xdata_s = xdata
        ydata_s1 = ydata1
        ydata_s2 = ydata2
        ydata_s3 = ydata3
    else:
        if isinstance(sample, list) or isinstance(sample, np.ndarray):
            print('Using provided index')
            inds = sample
        else:
            print('Picking ' + str(sample) + ' random samples')
            inds = np.random.randint(0, len(data), sample)
            # note: this samples with replacement
        xdata_s = [xdata[i] for i in inds]
        ydata_s1 = [ydata1[i] for i in inds]
        ydata_s2 = [ydata2[i] for i in inds]
        ydata_s3 = [ydata3[i] for i in inds]

    # c parameter values
    cval1 = 500
    cval2 = 500
    cval3 = 500

    # fit gen_cat model
    print('Fitting gen_cat')
    clf = svm.SVC(gamma='scale', decision_function_shape='ovo',
                  cache_size=20000, kernel='linear', C=cval1,
                  probability=proba, class_weight='balanced')
    clf.fit(xdata_s, ydata_s1)

    # fit prod_fam models
    print('Fitting prod_fam')
    y1_gp = pd.Series(ydata_s1, name='s1').reset_index().groupby('s1')
    clf_d2 = {}
    for name, group in y1_gp:
        X2 = [i for n, i in enumerate(xdata_s) if n in group['index'].values]
        Y2 = [i for n, i in enumerate(ydata_s2) if n in group['index'].values]
        if len(pd.unique(Y2)) == 1:
            clf_d2[name] = pd.unique(Y2)[0]
            continue
        clf_s2 = svm.SVC(gamma='scale', decision_function_shape='ovo',
                         cache_size=20000, kernel='linear', C=cval2,
                         probability=proba, class_weight='balanced')
        clf_s2.fit(X2, Y2)
        clf_d2[name] = clf_s2

    # fit prod_type models
    print('Fitting prod_type')
    y2_gp = pd.Series(ydata_s2, name='s2').reset_index().groupby('s2')
    clf_d3 = {}
    for name, group in y2_gp:
        X3 = [i for n, i in enumerate(xdata_s) if n in group['index'].values]
        Y3 = [i for n, i in enumerate(ydata_s3) if n in group['index'].values]
        if len(pd.unique(Y3)) == 1:
            clf_d3[name] = pd.unique(Y3)[0]
            continue
        clf_s3 = svm.SVC(gamma='scale', decision_function_shape='ovo',
                         cache_size=20000, kernel='linear', C=cval3,
                         probability=proba, class_weight='balanced')
        clf_s3.fit(X3, Y3)
        clf_d3[name] = clf_s3

    print('Done')
    joblib.dump(clf, 'PUC_model1' + lab + '.joblib')
    joblib.dump(clf_d2, 'PUC_model2_dict' + lab + '.joblib')
    joblib.dump(clf_d3, 'PUC_model3_dict' + lab + '.joblib')
