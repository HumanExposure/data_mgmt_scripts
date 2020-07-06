# -*- coding: utf-8 -*-
"""Run code.

@author: scott
"""

from make_training_data import load_training_data
from model_run_helper import (model_build, model_run, format_probs,
                              combine_results)
import pandas as pd

# options for embeddings
opts = {'ref': 'key',  # keep as 'key'
        'bert': 'bio',  # which bert model to use
        'document': True,  # whether to do document embeddings, keep true
        'reset': False,  # resets the embeddings
        'label': 'bio_oecd_only',  # label for model files
        'raw_embeddings': False,  # return raw embeddings
        }

# load the training data and create the embeddings
df_train, data = load_training_data(opts, reset=False)

# original_dict = data[0]
# original_dict_key = data[1]
# text_dict = data[2]
embed_dict = data[3]
# sen_dict = data[4]
# use_list = data[5]

model_build(df_train, embed_dict, opts,
            bootstrap=True, num_runs=5, probab=False)

# fake test data

# sen_itr = df_train['report_funcuse'].sample(100).to_list()
df_test = pd.read_excel('categorized_functions_05242018.xlsx') \
    .rename(columns={'reported_function': 'report_funcuse',
                     'technical_function': 'harmonized_funcuse'})
sen_itr = df_test['report_funcuse'].to_list()

all_list, fu_pred, proba_pred, sen_clean = \
    model_run(sen_itr, opts, mode=True, proba=False)

# prob_choice, prob_val = format_probs(
#     all_list, proba_pred, fu_pred, 0, opts['label'])

final_df = combine_results(
    sen_clean, sen_itr, all_list)  # , prob_choice, prob_val)

final_df['correct_funcuse'] = df_test['harmonized_funcuse']
final_df.to_csv(opts['label'] + '_results.csv', index=False)
