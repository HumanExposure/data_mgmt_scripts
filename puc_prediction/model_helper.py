# -*- coding: utf-8 -*-
"""Predict a PUC from a string.

@author: SBURNS
"""

from data_processing import clean, read_df, read_group
from puc_model import get_vector, build_model, load_model
# from sklearn import preprocessing
import joblib
import pandas as pd
import numpy as np
import os
import re
import torch


def format_probs(chem_puclist, chem_problist, chem_pucs_all,
                 limit=0, label=''):
    """Format probability columns.

    Most of the inputs come from model_run.

    Args:
        chem_puclist (list): List of predicted PUCs.
        chem_problist (list): List of probability for PUCs and levels.
        chem_pucs_all (list): List of PUCs for each run and level.
        limit (float, optional): Probability cutoff.
        label (str, optional): File label. Defaults to ''.

    Returns:
        comb3 (list): List of probability-chosen PUCs.
        new_prob_list (list): List of probabilites.

    """
    if len(chem_problist) == 0 or len(chem_problist[0]) == 0:
        return [], []

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
        return [], []

    comb = []
    comb_probs = []
    rem = [[], [], []]
    for level in range(3):
        all_df = pd.DataFrame(0, index=range(len(chem_puclist)),
                              columns=range(num_runs))
        all_pick = pd.DataFrame('', index=range(len(chem_puclist)),
                                columns=range(num_runs))
        for run in range(num_runs):
            make_prob = chem_problist[run][level]
            prob_choice = chem_pucs_all[run][level]
            top_per = [make_prob[i][prob_choice[i]] for i in
                       range(len(make_prob))]
            all_df[run] = top_per
            all_pick[run] = prob_choice

        newpuc = []
        newprobs = []
        rem_store = []
        for name, row in all_pick.iterrows():
            if (level > 0 and name in [j for i in rem[:level] for j in i]):
                newpuc.append('removed')
                newprobs.append('')
            else:
                if row.value_counts(normalize=True).max() > 0.5:
                    mode_val = row.mode().values[0]

                    # get prob for all mode_val
                    prob_list = []
                    for run in range(num_runs):
                        make_prob = chem_problist[run][level]
                        try:
                            mode_prob = make_prob[name][mode_val]
                        except KeyError:
                            # assign 0 for different groups
                            mode_prob = 0
                        prob_list.append(mode_prob)

                    # take median of all probs
                    med_prob = pd.Series(prob_list).median()

                    if med_prob > limit:
                        newpuc.append(mode_val)
                        newprobs.append(med_prob)
                    else:
                        newpuc.append('removed')
                        newprobs.append('')
                        rem_store.append(name)
                else:
                    newpuc.append('removed')
                    newprobs.append('')
                    rem_store.append(name)

        rem[level] = rem_store
        comb.append(newpuc)
        comb_probs.append([str(i) for i in newprobs])

    combt = np.array(comb).T
    comb2 = []
    for r in combt:
        ap = [''] * 3
        ap[0] = r[0].replace('none', '').strip()
        ap[2] = re.sub(f'^{r[1]}\\s*', '', r[2]).replace('none', '').strip()
        ap[1] = re.sub(f'^{r[0]}\\s*', '', r[1]).replace('none', '').strip()
        comb2.append(ap)

    comb3 = [[j if j != 'removed' else '' for j in i] for i in comb2]

    new_prob_list = np.array(comb_probs).T

    return comb3, new_prob_list


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


def model_predict(sen_vec, pkey, label=''):
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

    minmax = joblib.load('scale' + label + '.joblib')
    sen_vec = minmax.transform(sen_vec)

    clf = joblib.load('PUC_model1' + label + '.joblib')
    clf_d2 = joblib.load('PUC_model2_dict' + label + '.joblib')
    clf_d3 = joblib.load('PUC_model3_dict' + label + '.joblib')

    # use model
    print('Gathering pedictions')
    pred1 = clf.predict(sen_vec)
    pred2 = [clf_d2[pred1[n]] if isinstance(clf_d2[pred1[n]], str) else
             clf_d2[pred1[n]].predict([i])[0] for n, i in enumerate(sen_vec)]

    pred3 = [clf_d3[pred2[n]] if isinstance(clf_d3[pred2[n]], str) else
             clf_d3[pred2[n]].predict([i])[0] for n, i in enumerate(sen_vec)]

    puclist = [pkey.loc[i].to_list() for i in pred3]

    proba_out = []
    pucs_all = []
    if clf.probability:
        print('Predicting probabilities')
        proba1 = [{i: p[n] for n, i in enumerate(clf.classes_)}
                  for p in clf.predict_proba(sen_vec)]

        proba2 = [{clf_d2[pred1[n]]: 1} if isinstance(clf_d2[pred1[n]], str)
                  else
                  [{ii: p[nn] for nn, ii in enumerate(
                      clf_d2[pred1[n]].classes_)} for p in
                      clf_d2[pred1[n]].predict_proba([i])][0]
                  for n, i in enumerate(sen_vec)]

        proba3 = [{clf_d3[pred2[n]]: 1} if isinstance(clf_d3[pred2[n]], str)
                  else
                  [{ii: p[nn] for nn, ii in enumerate(
                      clf_d3[pred2[n]].classes_)} for p in
                      clf_d3[pred2[n]].predict_proba([i])][0]
                  for n, i in enumerate(sen_vec)]
        proba_out = [proba1, proba2, proba3]
        pucs_all = [pred1, pred2, pred3]

    return puclist, proba_out, pucs_all


def model_run(sen_itr, label='', mode=True):
    """Clean the new data and run the model.

    Args:
        sen_itr (list or array): List of ['brand', 'title'].
        label (str, optional): File label. Defaults to ''.
        mode (bool, optional): Whether to take mode of predictions.

    Returns:
        all_list (list): List of product pucs.
        removed (list): List of indices with names that were removed.
        proba_pred (list): List of probabilites.
        puc_list (list): List of predicted PUC for each level.

    """
    label = '' if len(label) == 0 else '_' + label.strip('_')

    # load embeddings
    # doc_embeddings = joblib.load('PUC_doc_embedding' + label + '.joblib')
    doc_embeddings = load_model()
    doc_embeddings.load_state_dict(
        torch.load('PUC_doc_embedding' + label + '.pt'))
    doc_embeddings.eval()

    pkey = joblib.load('PUC_key' + label + '.joblib')

    # clean input
    print('Cleaning input')
    if isinstance(sen_itr, str):
        sen_itr = [[sen_itr]]
    sen_itr = [[i] if isinstance(i, str) else i for i in sen_itr]
    sen_itr = [['', i[0]] if len(i) == 1 else i for i in sen_itr]
    sen_clean = [clean_str(i[0], i[1]) for i in sen_itr]
    removed = [n for n, i in enumerate(sen_clean) if len(i) < 1]
    sen_clean = [i for n, i in enumerate(sen_clean) if n not in removed]
    for i in removed:
        print(f'Invalid name in position {str(i)}, removing from list')
    if len(sen_clean) < 1:
        print('Error: No valid samples found')
        return [], [], [], []

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
        return [], [], [], []

    # convert to document embedding
    print('Converting text')
    sen_vec = [get_vector(i, doc_embeddings) for i in sen_clean]

    puc_pred = []
    proba_pred = []
    puc_list = []
    for n in range(num_runs):
        lab = label + '_' + str(n)
        print('----- Predicting ' + lab + ' -----')
        puclist, problist, pucs_all = model_predict(sen_vec, pkey, lab)
        puc_pred.append(puclist)
        proba_pred.append(problist)
        puc_list.append(pucs_all)
    all_list = pd.DataFrame(puc_pred).apply(mode_fun).values[0] if mode else \
        pd.DataFrame(puc_pred)

    return all_list, removed, proba_pred, puc_list


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
    df = load_df(label=label) if isinstance(df_train, str) else df_train
    sz = len(df) if isinstance(sample_size, str) else sample_size
    if not isinstance(sz, int):
        print('Please enter valid sample size')
        return None

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

    if isinstance(add_groups, int):
        add_groups = [add_groups]

    print('Pulling products')
    df = read_df()

    def standardize(x):
        try:
            return x.str.strip().str.lower()
        except AttributeError:
            return x

    df = df.apply(standardize)
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
            chem_df = chem_df.apply(standardize)
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
        .replace('', np.nan).sample(frac=1).dropna(subset=['name']) \
        .reset_index(drop=True)
    joblib.dump(df_comb, 'training_data' + label + '.joblib')

    pkey = pd.concat([df_comb[['gen_cat', 'prod_fam', 'prod_type']],
                      (df_comb['gen_cat'] + ' ' + df_comb['prod_fam']
                       .fillna('none')
                       + ' ' + df_comb['prod_type'].fillna('none'))
                      .str.strip()],
                     axis=1).drop_duplicates().set_index(0).fillna('')
    joblib.dump(pkey, 'PUC_key' + label + '.joblib')

    doc_embeddings = load_model()
    # joblib.dump(doc_embeddings, 'PUC_doc_embedding' + label + '.joblib')
    torch.save(doc_embeddings.state_dict(),
               'PUC_doc_embedding' + label + '.pt')

    print('Making xdata')
    data = df_comb[['name', 'gen_cat', 'prod_fam', 'prod_type']].copy()
    xdata = data['name'].apply(get_vector, args=(doc_embeddings,
                                                 )).to_list()
    joblib.dump(xdata, 'xdata' + label + '.joblib')

    print('Done')
    # moved to model
    # min_max_scaler = preprocessing.MinMaxScaler()
    # xdata = min_max_scaler.fit_transform(xdata)
    # joblib.dump(xdata, 'xdata' + label + '.joblib')
    # joblib.dump(min_max_scaler, 'scale' + label + '.joblib')


def load_df(label=''):
    """Load the training data."""
    label = '' if len(label) == 0 else '_' + label.strip('_')
    return joblib.load('training_data' + label + '.joblib')


def results_df(sen_itr, all_list, removed, proba_pred, puc_list,
               proba_limit=False, label=''):
    """Format results into a dataframe.

    Most inputs come from model_run.

    Args:
        sen_itr (list or array): List of ['brand', 'title'].
        all_list (list): List of predicted PUCs.
        removed (list): List of PUCs not predicted.
        proba_pred (list): List of probabilities for each run and level.
        puc_list (list): List of PUCs for each prediction run and level.
        proba_limit (float or bool): Whether to include probability, or cutoff.
        label (str, optional): File label. Defaults to ''.

    Returns:
        df_comb (DataFrame): Combined DataFrame with inputs and outputs.

    """
    if isinstance(proba_limit, bool) or proba_limit is None:
        do_prob = proba_limit
        limit = 0
    else:
        do_prob = True
        limit = proba_limit

    if isinstance(sen_itr, str):
        sen_itr = [[sen_itr]]
    sen_itr = [[i] if isinstance(i, str) else i for i in sen_itr]
    sen_itr = [['', i[0]] if len(i) == 1 else i for i in sen_itr]

    if do_prob:
        prob_pucs, probs = format_probs(all_list, proba_pred, puc_list,
                                        limit=limit, label=label)
        if len(prob_pucs) != len(all_list):
            do_prob = False
            print('Please build model with probabilities')
    else:
        prob_pucs = []
        probs = []

    # add back removed rows
    all_list_fixed = []
    prob_pucs_fixed = []
    probs_fixed = []
    all_ct = 0
    for n, i in enumerate(sen_itr):
        if n in removed:
            all_list_fixed.append(['', '', ''])
            if do_prob:
                prob_pucs_fixed.append(['', '', ''])
                probs_fixed.append(['', '', ''])
        else:
            all_list_fixed.append(all_list[all_ct])
            if do_prob:
                prob_pucs_fixed.append(prob_pucs[all_ct])
                probs_fixed.append(probs[all_ct])
            all_ct += 1
    if all_ct != len(all_list):
        print('Error fixing removed')
        return None

    df_sen = pd.DataFrame.from_records(
        sen_itr, columns=['brand', 'title'])

    # make sure there is no weird whitespace in output
    for col in df_sen.columns:
        df_sen[col] = df_sen[col].apply(
            lambda x: re.sub(r'\s', ' ', x) if isinstance(x, str) else x)

    df_results = pd.DataFrame.from_records(
        all_list_fixed, columns=['gen_cat', 'prod_fam', 'prod_type'])

    df_probs = pd.DataFrame.from_records(
        prob_pucs_fixed,
        columns=['prob_name_gen_cat', 'prob_name_prod_fam',
                 'prob_name_prod_type'])
    df_probs_values = pd.DataFrame.from_records(
        probs_fixed,
        columns=['prob_val_gen_cat', 'prob_val_prod_fam',
                 'prob_val_prod_type'])

    to_comb = [df_sen, df_results]
    if do_prob:
        to_comb.append(df_probs)
        to_comb.append(df_probs_values)

    df_comb = pd.concat(to_comb, axis=1)

    df_comb.to_csv('results_' + label + '.csv', index=False)

    print('Done')
    return df_comb
