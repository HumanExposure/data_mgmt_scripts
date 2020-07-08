# -*- coding: utf-8 -*-
"""Load training data and calculate vectors."""


from data import clean_text, run_cleaning
# from data import cpdat_data
from oecd import oecd_def, oecd_ont, maps
from embeddings import make_list

import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


# add default names and subgroup names
def get_default_set():
    """Make a training set with the default OECD names and synonyms."""
    # make df of harmonized uses for training
    df = pd.DataFrame(
        columns=['report_funcuse', 'harmonized_funcuse', 'raw_chem_name'])
    df['report_funcuse'] = oecd_def.keys()
    df['harmonized_funcuse'] = oecd_def.keys()
    oecd_clean = {clean_text(key.lower().strip(), ensure_word=True): key
                  for key in oecd_def.keys()}

    # add functional uses from oecd_ont
    def match_oecd_syn(oecd_syn_dict):
        temp_list = []
        for key, val in oecd_syn_dict.items():
            clean_key = clean_text(key.lower().strip(), ensure_word=True)
            df_temp = pd.DataFrame(columns=['report_funcuse',
                                            'harmonized_funcuse',
                                            'raw_chem_name'])
            new_fu = None
            try:
                new_fu = oecd_clean[clean_key]
            except KeyError:
                fuzzy_match = process.extractBests(clean_key,
                                                   list(oecd_clean.keys()),
                                                   limit=2,
                                                   scorer=fuzz.token_set_ratio)
                if fuzzy_match[0][1] - fuzzy_match[1][1] > 10:
                    new_fu = oecd_clean[fuzzy_match[0][0]]
                    print(f'Matched {key} to {new_fu}')
                else:
                    print(f'Could not match functional use: {key}')
            if new_fu is not None:
                df_temp['report_funcuse'] = val + [key]
                df_temp['harmonized_funcuse'] = new_fu
            temp_list.append(df_temp)
        df_comb_temp = pd.concat(temp_list).reset_index(drop=True)
        return df_comb_temp.drop_duplicates()

    ont_match = match_oecd_syn(oecd_ont)
    maps_match = match_oecd_syn(maps)
    df_comb = pd.concat([df, ont_match, maps_match]) \
        .drop_duplicates().reset_index(drop=True)
    return df_comb


def get_training_set():
    """Get training data.

    Should be a dataframe with the following columns:
        report_funcuse: functional use
        harmonized_funcuse: assigned OECD functional use
        raw_chem_name: name of chemical, set to NAN if missing
    """
    # makes a blank dataframe
    df = pd.DataFrame(
        columns=['report_funcuse', 'harmonized_funcuse', 'raw_chem_name'])

    # this is an example function reads the cpdat functional use table
    # feel free to make your own training data and combine multiple sources
    # df = codat_data()
    return df


def clean_training_data(opts):
    """Clean the training data and get embeddings."""
    # combine dataframes
    print('Getting training data...')
    df_default = get_default_set()
    df_training = get_training_set()
    df = pd.concat([df_default, df_training]).reset_index(drop=True)
    # df['report_funcuse'] = df['report_funcuse']
    print('Done')

    # clean data
    print('Cleaning training data...')
    df_clean = run_cleaning(df, keep_na=True)
    df_class = pd.DataFrame(
        columns=['report_funcuse', 'clean_funcuse', 'clean_funcuse_hash',
                 'harmonized_funcuse'])
    df_class['report_funcuse'] = df['report_funcuse']
    df_class['clean_funcuse'] = df_clean['report_funcuse']
    df_class['harmonized_funcuse'] = df['harmonized_funcuse']
    df_class = df_class.replace('', np.nan) \
        .dropna(subset=['clean_funcuse', 'harmonized_funcuse'])
    print('Done')

    # un-split the functional uses
    # df_class['clean_funcuse'] = df_class['clean_funcuse'] \
    #     .apply(lambda x: [' '.join(x)])

    # mix up data
    df_class = df_class.sample(frac=1).reset_index(drop=True)

    # make embeddings
    original_dict, original_dict_key, text_dict, embed_dict, \
        sen_dict, use_list = \
        make_list(oecd_def, df_class['clean_funcuse'], opts)

    reverse_text = {val: key for key, val in text_dict.items()}
    if len(reverse_text) != len(text_dict):
        print('Duplicate values in text_dict')

    df_class['clean_funcuse_hash'] = df_class['clean_funcuse'].apply(
        lambda x: [reverse_text[i] for i in x if i in reverse_text])

    # turn columns from lists to strings
    # df_class['clean_funcuse'] = df_class['clean_funcuse'] \
    #     .apply(lambda x: x[0] if len(x) == 1 else np.nan)
    # df_class['clean_funcuse_hash'] = df_class['clean_funcuse_hash'] \
    #     .apply(lambda x: x[0] if len(x) == 1 else np.nan)
    df_class['clean_funcuse'] = df_class['clean_funcuse'] \
        .apply(lambda x: ';;-;'.join(x))
    df_class['clean_funcuse_hash'] = df_class['clean_funcuse_hash'] \
        .apply(lambda x: ';;-;'.join(x))

    return df_class, [original_dict, original_dict_key, text_dict,
                      embed_dict, sen_dict, use_list]


def clean_testing_data(test_list, opts):
    """Clean the training data and get embeddings."""
    df = pd.DataFrame(
        columns=['report_funcuse', 'raw_chem_name'])
    df['report_funcuse'] = test_list

    # clean data
    print('Cleaning test data...')
    df_clean = run_cleaning(df, keep_na=True)
    df_class = pd.DataFrame(
        columns=['report_funcuse', 'clean_funcuse', 'clean_funcuse_hash',
                 'harmonized_funcuse'])
    df_class['report_funcuse'] = df['report_funcuse']
    df_class['clean_funcuse'] = df_clean['report_funcuse']
    # df_class['harmonized_funcuse'] = ''
    df_class = df_class.replace('', np.nan) \
        .dropna(subset=['clean_funcuse'])
    print('Done')

    # un-split the functional uses
    # df_class['clean_funcuse'] = df_class['clean_funcuse'] \
    #     .apply(lambda x: [' '.join(x)])

    # make embeddings
    original_dict_s, original_dict_key_s, text_dict_s, embed_dict_s, \
        sen_dict_s, use_list_s = \
        make_list(oecd_def, df_class['clean_funcuse'], opts, reset=False)

    reverse_text = {val: key for key, val in text_dict_s.items()}
    if len(reverse_text) != len(text_dict_s):
        print('Duplicate values in text_dict')

    df_class['clean_funcuse_hash'] = df_class['clean_funcuse'].apply(
        lambda x: [reverse_text[i] for i in x if i in reverse_text])

    # turn columns from lists to strings
    # df_class['clean_funcuse'] = df_class['clean_funcuse'] \
    #     .apply(lambda x: x[0] if len(x) == 1 else np.nan)
    # df_class['clean_funcuse_hash'] = df_class['clean_funcuse_hash'] \
    #     .apply(lambda x: x[0] if len(x) == 1 else np.nan)

    return df_class, [original_dict_s, original_dict_key_s, text_dict_s,
                      embed_dict_s, sen_dict_s, use_list_s]


def load_training_data(opts, reset=False):
    """Load training data or create new data."""
    fname = f"training_data_{opts['label']}.csv"

    def string_to_list(df):
        """Turn string columns into lists."""
        df['clean_funcuse'] = df['clean_funcuse'] \
            .apply(lambda x: x.split(';;-;') if not pd.isna(x) else np.nan)
        df['clean_funcuse_hash'] = df['clean_funcuse_hash'] \
            .apply(lambda x: x.split(';;-;') if not pd.isna(x) else np.nan)
        return df

    if os.path.isfile(fname) and not reset:
        print('Saved table found, loading...')
        df_train = pd.read_csv(fname)
        df_train = string_to_list(df_train)
        original_dict, original_dict_key, text_dict, embed_dict, \
            sen_dict, use_list = \
            make_list(oecd_def, df_train['clean_funcuse'], opts)
        data = [original_dict, original_dict_key, text_dict,
                embed_dict, sen_dict, use_list]
    else:
        print('No saved files found, loading new data...')
        if os.path.exists(fname):
            os.rename(fname, os.path.splitext(fname)[0] + '_old.csv')
        df_train, data = clean_training_data(opts)
        df_train.to_csv(fname, index=False)
        df_train = string_to_list(df_train)
    print('Done')
    return df_train, data
