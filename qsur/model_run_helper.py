# -*- coding: utf-8 -*-
"""Helper functions to run model.

@author: scott
"""

from train_model import build_model
from make_training_data import clean_testing_data
from embeddings import cosine_function

import joblib
import pandas as pd
import numpy as np
import os
from fuzzywuzzy import fuzz
import torch


def model_opts(**kwargs):
    """Set options for embeddings."""
    opts = {'ref': 'key',  # keep as 'key'
            'bert': 'bio',  # which bert model to use
            'document': True,  # whether to do document embeddings, keep true
            'flair': False,  # whether to use flair embeddings, keep false
            'reset': False,  # resets the embeddings
            'label': '',  # label for model files
            'cosine': False,  # use cosine similarity for model
            'cval': 1  # C param for SVM
            }
    for key, value in kwargs.items():
        opts[key] = value
    return opts


def mode_fun(x):
    """Get the most frequent PUC."""
    if x.value_counts(normalize=True).max() > 0.5:
        return x.mode()
    return pd.Series('')


def format_probs(all_list, proba_pred, fu_pred, limit=0, label=''):
    """Return the probabilities."""
    # checks for number of model
    print('Parsing probabilities...')
    if None in proba_pred:
        print('Probability list not found, ' +
              'please train the model with proba=True')
        return None, None
    label = '' if len(label) == 0 else '_' + label.strip('_')
    num_runs = 0
    for i in range(len(os.listdir('store'))):
        lab = label + '_' + str(i)
        fname = 'OECD_model' + lab + '.joblib'
        if os.path.exists(os.path.join('store', fname)):
            num_runs += 1
        else:
            print(str(num_runs) + ' runs detected')
            break
    if num_runs == 0:
        print('Please build the model or change the label parameter')
        return [], []

    all_df = pd.DataFrame(0, index=range(len(all_list)),
                          columns=range(num_runs))
    all_pick = pd.DataFrame('', index=range(len(all_list)),
                            columns=range(num_runs))
    for run in range(num_runs):
        make_prob = proba_pred[run]
        prob_choice = fu_pred[run]
        top_per = [make_prob[i][prob_choice[i]] for i in
                   range(len(make_prob))]
        all_df[run] = top_per
        all_pick[run] = prob_choice

    newpuc = []
    newprobs = []
    for name, row in all_df.iterrows():
        over_lim = row.loc[row >= limit]
        over_names = all_pick.loc[name, over_lim.index]

        if (len(over_lim) > num_runs/2 and
                over_names.value_counts(normalize=True).max() > 0.5):
            modeval = over_names.mode().values[0]
            avg_prob = over_lim.loc[over_names == modeval].mean()
            if avg_prob > limit:
                newpuc.append(modeval)
                newprobs.append(avg_prob)
            else:
                newpuc.append('')
                newprobs.append(0)
        else:
            newpuc.append('')
            newprobs.append(0)
    print('Done')
    return newpuc, newprobs


def model_predict(sen_vec, label=''):
    """Load model and predict PUCS.

    This is not meant to be called outside of 'model_run'.

    Args:
        sen_vec (list): List of word embeddings.
        label (str, optional): File label. Defaults to ''.

    Returns:
        proba_out (list): List of probabilites.
        pred1 (list): List of predicted functional uses.

    """
    # load models
    print('Loading model data')
    label = '' if len(label) == 0 else '_' + label.strip('_')

    minmax = joblib.load(os.path.join('store', 'scale' + label + '.joblib'))
    sen_vec = minmax.transform(sen_vec)

    clf = joblib.load(os.path.join('store', 'OECD_model' + label + '.joblib'))

    # use model
    print('Gathering pedictions')
    pred1 = clf.predict(sen_vec)

    proba_out = None
    if clf.probability:
        print('Predicting probabilities')
        proba1 = [{i: p[n] for n, i in enumerate(clf.classes_)}
                  for p in clf.predict_proba(sen_vec)]
        proba_out = proba1

    return pred1, proba_out


def model_run(sen_itr, opts, raw_chems=None, mode=True, proba=False):
    """Clean the new data and run the model.

    Args:
        sen_itr (list or array): List of values to predict.
        label (str, optional): File label. Defaults to ''.
        mode (bool, optional): Whether to take mode of predictions.
        proba (bool, optional): Whether to predict probabilities.

    Returns:
        all_list (list): List of product pucs.
        removed (list): List of indices with names that were removed.
        proba_pred (list): List of probabilites.
        puc_list (list): List of predicted PUC for each level.

    """
    label = opts['label']
    label = '' if len(label) == 0 else '_' + label.strip('_')

    # clean input
    print('Cleaning input')
    if isinstance(sen_itr, str):
        sen_itr = [sen_itr]
    if raw_chems is not None and len(raw_chems) != len(sen_itr):
        print('Raw chems list must be same length as sen_itr')
        raw_chems = None
    sen_clean, data_s = clean_testing_data(sen_itr, opts, raw_chems)
    original_dict_s = data_s[0]
    embed_dict_s = data_s[3]

    if len(sen_clean) < len(sen_itr):
        print('Some samples were invalid and removed')
    if len(sen_clean) < 1:
        print('Error: No valid samples found')
        return [], [], [], []

    # checks for number of model run
    num_runs = 0
    for i in range(len(os.listdir('store'))):
        lab = label + '_' + str(i)
        fname = 'OECD_model' + lab + '.joblib'
        if os.path.exists(os.path.join('store', fname)):
            num_runs += 1
        else:
            print(str(num_runs) + ' runs detected')
            break
    if num_runs == 0:
        print('Please build the model or change the label parameter')
        return [], [], [], []

    # convert to document embedding
    if not opts['cosine']:
        sen_vec = [[embed_dict_s[j][0] for j in i]
                   for i in sen_clean['clean_funcuse_hash']]
    else:
        sen_vec = cosine_function(sen_clean, original_dict_s, embed_dict_s,
                                  label, reset=False)

    # flatten and create map
    sen_vec_flat = []
    ind_map = []
    ct = 0
    for i in sen_vec:
        temp_map = []
        for j in i:
            temp_map.append(ct)
            sen_vec_flat.append(j)
            ct += 1
        ind_map.append(temp_map)

    # make predictions
    fu_pred = []
    proba_pred = []
    for n in range(num_runs):
        lab = label + '_' + str(n)
        print('----- Predicting ' + lab + ' -----')
        predlist, problist = model_predict(sen_vec_flat, lab)
        fu_pred.append(predlist)
        proba_pred.append(problist)
    all_list = pd.DataFrame(fu_pred).apply(mode_fun).values[0] if mode else \
        pd.DataFrame(fu_pred)

    return all_list, fu_pred, proba_pred, sen_clean, ind_map, data_s


def combine_results(
        sen_old, sen_itr, ind_map, all_list, opts,
        prob_choice=None, prob_val=None,
        calc_similarity=False, data=None, sep=' / '):
    """Combine all results into one dataframe."""
    print('Formatting output table...')
    sen_old = sen_old.reset_index(drop=True)

    # add columns
    all_list_format = [';;-;'.join([str(all_list[j])
                                    for j in i]) for i in ind_map]
    sen_old['harmonized_funcuse'] = all_list_format

    if prob_choice is not None:
        prob_choice_format = [';;-;'.join([str(prob_choice[j]) for j in i])
                              for i in ind_map]
        sen_old['prob_choice'] = prob_choice_format
    if prob_val is not None:
        prob_val_format = [';;-;'.join([str(prob_val[j]) for j in i])
                           for i in ind_map]
        sen_old['avg_prob'] = prob_val_format

    if calc_similarity:
        fuzz_sim, cos_sim = similarity_columns(sen_old, data, opts)
        if fuzz_sim is not None:
            sen_old['fuzzy_similarity'] = [';;-;'.join([str(j) for j in i])
                                           for i in fuzz_sim]

        if cos_sim is not None:
            sen_old['cosine_similarity'] = [';;-;'.join([str(j) for j in i])
                                            for i in cos_sim]

    # combine other list cols
    sen_old['clean_funcuse'] = sen_old['clean_funcuse'] \
        .apply(lambda x: ';;-;'.join(x))
    sen_old['clean_funcuse_hash'] = sen_old['clean_funcuse_hash'] \
        .apply(lambda x: ';;-;'.join(x))

    # change separator
    sen_old = sen_old.apply(lambda x: x.str.replace(';;-;', sep, regex=False))

    # add missing rows
    new_df = []
    idx_ct = 0
    for val in sen_itr:
        # print(idx_ct)
        clean_val = sen_old.loc[idx_ct, 'report_funcuse']
        if clean_val == val:
            new_df.append(sen_old.loc[idx_ct])
            idx_ct += 1
        else:
            new_s = pd.Series(['']*len(sen_old.columns), index=sen_old.columns)
            new_s['report_funcuse'] = val
            new_df.append(new_s)
    # for n, i in enumerate(new_df):
        # print(str(n)+': '+str(type(i)))
    # print(new_df[440])
    df2 = pd.concat(new_df, axis=1).T
    if idx_ct != len(sen_old):
        print('error combining results')
        return None
    print('Finished formatting')
    return df2


def model_build(df_train, opts, data, bootstrap=False, num_runs=1,
                sample_size='all', probab=False):
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
    label = opts['label']
    cosine = opts['cosine']
    cval = opts['cval']
    original_dict = data[0]
    embed_dict = data[3]
    df = df_train
    sz = len(df) if isinstance(sample_size, str) else sample_size

    for n in range(num_runs):
        print('----- Training ' + label + '_' + str(n) + ' -----')
        boot_sample = np.random.choice(df.index, size=sz,
                                       replace=bootstrap)
        build_model(df, embed_dict, cval=cval, label=label,
                    nrun=str(n), sample=boot_sample, proba=probab,
                    cosine=cosine, original_dict=original_dict)


def similarity_columns(df, data, opts):
    """Output similarity between reported and predicted."""
    print('Calculating column similarity...')
    original_dict = data[0]
    text_dict = data[2]
    embed_dict = data[3]

    reverse_original = {val: key for key, val in original_dict.items()}
    if len(reverse_original) != len(original_dict):
        print('Duplicate values in text_dict')
        return None, None

    def convert_embeddings(h):
        """Get embedding from hash."""
        if opts['cosine']:
            return embed_dict[h]
        else:
            return torch.from_numpy(embed_dict[h][0])

    fuzz_col = []
    cosine_col = []
    for name, row in df.iterrows():
        harm_names = row['harmonized_funcuse'].split(';;-;')
        report_names = row['clean_funcuse']
        report_hash = row['clean_funcuse_hash']
        if len(harm_names) != len(report_names) or \
                len(report_names) != len(report_hash):
            print('Error matching list length')
            return None, None

        # fuzzywuzzy between clean col and clean harmonized
        fuzz_scores = []
        for n, i in enumerate(harm_names):
            if i.strip() == '' or pd.isna(i):
                fuzz_scores.append('')
                continue
            name1 = report_names[n]
            name2 = text_dict[reverse_original[i]]
            newscore = fuzz.token_sort_ratio(name1, name2)
            fuzz_scores.append(newscore)
        fuzz_col.append(fuzz_scores)

        # cosine similarity between clean embeddings and harmonized embedding
        cos_scores = []
        for n, i in enumerate(harm_names):
            if i.strip() == '' or pd.isna(i):
                cos_scores.append('')
                continue
            embed1 = report_hash[n]
            embed2 = reverse_original[i]
            cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
            sim = cos(convert_embeddings(embed1), convert_embeddings(embed2))
            cos_scores.append(float(sim))
        cosine_col.append(cos_scores)
    print('Done')
    return fuzz_col, cosine_col


def predict_values(sen_itr, opts, raw_chems=None,
                   proba_limit=False, calc_similarity=False):
    """Wraper for other functions in this file."""
    sep = ' / '
    if isinstance(proba_limit, bool):
        proba = proba_limit
        limit = 0
    else:
        proba = True
        limit = proba_limit

    all_list, fu_pred, proba_pred, sen_clean, ind_map, data_s = \
        model_run(sen_itr, opts, raw_chems=raw_chems,
                  mode=True, proba=proba)

    if proba:
        prob_choice, prob_val = format_probs(
            all_list, proba_pred, fu_pred, limit, opts['label'])
    else:
        prob_choice = None
        prob_val = None

    final_df = combine_results(
        sen_clean, sen_itr, ind_map, all_list, opts,
        prob_choice=prob_choice, prob_val=prob_val,
        calc_similarity=calc_similarity, data=data_s, sep=sep)

    return final_df
