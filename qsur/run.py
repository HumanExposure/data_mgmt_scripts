# -*- coding: utf-8 -*-
"""Run code."""


from make_training_data import load_training_data
from model_run_helper import model_build, predict_values, model_opts
import pandas as pd

# load the training data and create the embeddings
opts = model_opts(label='bio_oecd_only')
df_train, data = load_training_data(opts, reset=False)

# original_dict = data[0]
# original_dict_key = data[1]
# text_dict = data[2]
# embed_dict = data[3]
# sen_dict = data[4]
# use_list = data[5]


model_build(df_train, opts, data,
            bootstrap=True, num_runs=5, probab=False)

# fake test data
from data import cpdat_data
df_test = cpdat_data().head(100)

# sen_itr = df_train['report_funcuse'].sample(100).to_list()
# df_test = pd.read_excel('categorized_functions_05242018.xlsx') \
#     .rename(columns={'reported_function': 'report_funcuse',
#                      'technical_function': 'harmonized_funcuse'})

sen_itr = df_test['report_funcuse'].to_list()

# run
final_df = predict_values(sen_itr, opts,
                          proba_limit=True, calc_similarity=True)

final_df['correct_funcuse'] = df_test['harmonized_funcuse']
final_df.to_csv(opts['label'] + '_results.csv', index=False)
