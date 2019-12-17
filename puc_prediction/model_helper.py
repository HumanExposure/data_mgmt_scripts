# -*- coding: utf-8 -*-
"""Predict a PUC from a string.

@author: SBURNS
"""

from data_processing import clean, read_df, read_group
from puc_model import get_vector, build_model, load_model
from sklearn import preprocessing
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


def mode_fun(x):
    """Get the most frequent PUC."""
    if x.value_counts(normalize=True).max() > 0.5:
        return x.mode()
    x2 = x.apply(lambda y: y[:2] + [''])
    if x2.value_counts(normalize=True).max() > 0.5:
        return x2.mode()
    x3 = x.apply(lambda y: y[:1] + ['', ''])
    if x3.value_counts(normalize=True).max() > 0.5:
        return x3.mode()
    return pd.Series([['']*3])


def model_predict(sen_vec, pkey, label='', proba=False):
    """Load model and predict PUCS.

    This is not meant to be called outside of 'model_run'.

    Args:
        sen_vec (list): List of word embeddings.
        pkey(pd.DataFrame): Dataframe matching classes back to PUCS.
        label (str, optional): File label. Defaults to ''.

    Returns:
        puclist (list): List of list with PUC info.
        proba_out (list): List of probabilites.
        pucs_all (list): List of predicted PUC for each level.

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

    proba_out = []
    pucs_all = []
    if proba:
        print('Predicting probabilities')
        proba1 = [{i: p[n] for n, i in enumerate(clf.classes_)}
                  for p in clf.predict_proba(sen_vec)]

        proba2 = [{clf_d2[pred1[n]]: 1} if type(clf_d2[pred1[n]]) == str else
                  [{ii: p[nn] for nn, ii in enumerate(
                      clf_d2[pred1[n]].classes_)} for p in
                      clf_d2[pred1[n]].predict_proba([i])][0]
                  for n, i in enumerate(sen_vec)]

        proba3 = [{clf_d3[pred2[n]]: 1} if type(clf_d3[pred2[n]]) == str else
                  [{ii: p[nn] for nn, ii in enumerate(
                      clf_d3[pred2[n]].classes_)} for p in
                      clf_d3[pred2[n]].predict_proba([i])][0]
                  for n, i in enumerate(sen_vec)]
        proba_out = [proba1, proba2, proba3]
        pucs_all = [pred1, pred2, pred3]

    return puclist, proba_out, pucs_all


def model_run(sen_itr, label='', mode=True, proba=False):
    """Clean the new data and run the model.

    Args:
        sen_itr (list or array): List of ['brand', 'title'].
        label (str, optional): File label. Defaults to ''.
        mode (bool, optional): Whether to take mode of predictions.
        proba (bool, optional): Whether to predict probabilities.

    Returns:
        all_list (list): List of product pucs
        proba_pred (list): List of probabilites.
        puc_list (list): List of predicted PUC for each level.

    """
    label = '' if len(label) == 0 else '_' + label.strip('_')
    doc_embeddings = joblib.load('PUC_doc_embedding' + label + '.joblib')
    pkey = joblib.load('PUC_key' + label + '.joblib')

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

    minmax = joblib.load('scale' + label + '.joblib')
    sen_vec = minmax.transform(sen_vec)

    puc_pred = []
    proba_pred = []
    puc_list = []
    for n in range(num_runs):
        lab = label + '_' + str(n)
        print('----- Predicting ' + lab + ' -----')
        puclist, problist, pucs_all = model_predict(sen_vec, pkey, lab, proba)
        puc_pred.append(puclist)
        proba_pred.append(problist)
        puc_list.append(pucs_all)
    all_list = pd.DataFrame(puc_pred).apply(mode_fun).values[0] if mode else \
        pd.DataFrame(puc_pred)

    return all_list, proba_pred, puc_list


def model_build(df_train='all', bootstrap=False, num_runs=1,
                sample_size='all', label='', probab=False):
    """Generate the model.

    xdata.joblib should already exist. To get more control over the model, run
    build_model directly.

    Args:
        df_train (pd.DataFrame or str, optional): Training subset of df. Can
            be set to a str to use whole df. To get full df to subset, use
            load_df(). Defaults to 'all'.
        bootstrap (bool, optional): Whether to sample with replacement or not.
            Defaults to False.
        num_runs (int, optional): Number of runs to aggregate. Defaults to 1.
        sample_size (int, str, optional): Size of training set for each run,
            sampled from the training set. Defaults to 'all'.
        label (str, optional): File label. Defaults to ''.
        probab (bool, optional): Whether to calculate class probability.

    """
    df = load_df() if type(df_train) == str else df_train
    sz = len(df) if type(sample_size) == str else sample_size

    for n in range(num_runs):
        print('----- Training ' + label + '_' + str(n) + ' -----')
        boot_sample = np.random.choice(df.index, size=sz,
                                       replace=bootstrap)
        build_model(label=label, nrun=str(n), sample=boot_sample, proba=probab)


def model_initialize(add_groups=[], label=''):
    """Initialize the model by pulling and cleaning data.

    Will pull all of the products with PUCs, as well as all of the products
    in data groups that are in the input. The products within these data groups
    should not requie PUCs (e.g. a pure chemical). This is to train the model
    on products that should not have a PUC.

    Args:
        add_groups (list, optional): A list of data groups. Defaults to [].
        label (str, optional): Label for the saved data. Defaults to ''.

    """
    print('----- Initializing model -----')
    label = '' if len(label) == 0 else '_' + label.strip('_')

    if type(add_groups) is int:
        add_groups = [add_groups]

    print('Pulling products')
    df = read_df()
    name = df[['brand_name', 'title']].apply(lambda x: clean_str(
        x['brand_name'], x['title']), axis=1)
    name.name = 'name'
    cat = df['gen_cat']  # .apply(lambda x: clean_str('', x))
    fam = df['prod_fam']  # .apply(lambda x: clean_str('', x))
    typ = df['prod_type']  # .apply(lambda x: clean_str('', x))
    comb = pd.concat([name, cat, fam, typ], axis=1)

    df_add = []
    for i in add_groups:
        chem_df = read_group(i)
        if len(chem_df) > 0:
            print(f'Adding group {i}')
            chem_df['name'] = chem_df.apply(lambda x: clean_str(
                x['brand_name'], x['title']), axis=1)
            chem_df['gen_cat'] = 'not_applicable'
            chem_df['prod_fam'] = ''
            chem_df['prod_type'] = ''
            chem_df = chem_df.drop(columns=['id', 'brand_name', 'title',
                                            'data_group_id'])
            df_add.append(chem_df)
        else:
            print(f'Group {i} not found')

    df_comb = pd.concat([comb] + df_add) \
        .replace('', np.nan).sample(frac=1)  # .drop_duplicates()
    joblib.dump(df_comb, 'training_data' + label + '.joblib')

    pkey = pd.concat([df_comb[['gen_cat', 'prod_fam', 'prod_type']],
                      (df_comb['gen_cat'] + ' ' + df_comb['prod_fam']
                       .fillna('none')
                       + ' ' + df_comb['prod_type'].fillna('none'))
                      .str.strip()],
                     axis=1).drop_duplicates().set_index(0).fillna('')
    joblib.dump(pkey, 'PUC_key' + label + '.joblib')

    doc_embeddings = load_model()
    joblib.dump(doc_embeddings, 'PUC_doc_embedding' + label + '.joblib')

    print('Making xdata')
    data = df_comb[['name', 'gen_cat', 'prod_fam', 'prod_type']].copy()
    xdata = data['name'].apply(get_vector, args=(doc_embeddings,
                                                 )).to_list()
    joblib.dump(xdata, 'xdata_orig' + label + '.joblib')

    min_max_scaler = preprocessing.MinMaxScaler()
    xdata = min_max_scaler.fit_transform(xdata)
    joblib.dump(xdata, 'xdata' + label + '.joblib')
    joblib.dump(min_max_scaler, 'scale' + label + '.joblib')


def load_df(label=''):
    """Load the training data."""
    label = '' if len(label) == 0 else '_' + label.strip('_')
    return joblib.load('training_data' + label + '.joblib')
