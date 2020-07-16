# -*- coding: utf-8 -*-
"""Run code."""


from make_training_data import load_training_data
from model_run_helper import model_build, predict_values, model_opts
# import pandas as pd

# from data import cpdat_data
from data import factotum_data


def run_all(opts, df_test):
    """Run all functions."""
    # load the training data and create the embeddings
    df_train, data = load_training_data(opts, reset=False)

    # build model
    model_build(df_train, opts, data,
                bootstrap=True, num_runs=11, probab=True)

    # test data
    sen_itr = df_test['report_funcuse'].to_list()
    raw_chems = df_test['raw_chem_name'].to_list()

    # run
    final_df = predict_values(sen_itr, opts, raw_chems,
                              proba_limit=True, calc_similarity=True)

    # final_df['correct_funcuse'] = df_test['harmonized_funcuse']
    final_df.to_csv(opts['label'] + '_results.csv', index=False)


# import training data. you could load this from somewhere else.
df_test_all = factotum_data()
df_test = df_test_all.sample(2000) \
    .drop_duplicates(subset=['report_funcuse']).sample(500)
df_test.to_csv('testing_dataset.csv', index=False)


# load options and run
opts = model_opts(label='test_data', bert='bio', cval=1)
run_all(opts, df_test)
