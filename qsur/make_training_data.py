# -*- coding: utf-8 -*-
"""Load training data and calculate vectors."""


from data import clean_text, run_cleaning, split_funcuse
# from data import cpdat_data
from oecd import oecd_def, oecd_ont, maps, manual_fix
from embeddings import make_list

import os
import re
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
    ont_match = match_oecd_syn(oecd_ont, oecd_clean)
    maps_match = match_oecd_syn(maps, oecd_clean)
    df_comb = pd.concat([df, ont_match, maps_match]) \
        .drop_duplicates().reset_index(drop=True)
    return df_comb


def match_oecd_syn(oecd_syn_dict, oecd_clean):
    """Match training data to harmonized functional use.

    Matches harmonized functional uses in a traning set to ones used for
    training. This is useful since different training sets have some
    variations in capitolization/cleaning.
    """
    temp_list = []
    if isinstance(oecd_syn_dict, dict):
        to_iter = oecd_syn_dict.items()
        isdict = True
    else:
        to_iter = oecd_syn_dict.iterrows()
        isdict = False
    for key1, val1 in to_iter:
        rawchem = np.nan
        if isdict:
            key = key1
            val = val1
        else:
            key = val1['harmonized_funcuse']
            val = val1['report_funcuse']
            if 'raw_chem_name' in val1:
                rawchem = val1['raw_chem_name']
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
                try:
                    new_fu = manual_fix[key]
                except KeyError:
                    print(f'Could not match functional use: {key}')
                else:
                    print(f'Manually matched {key} to {new_fu}')
        if new_fu is not None:
            df_temp['report_funcuse'] = (val + [key]) if isdict else val
            df_temp['harmonized_funcuse'] = new_fu
            df_temp['raw_chem_name'] = rawchem
        df_temp = df_temp.drop_duplicates()
        temp_list.append(df_temp)
    df_comb_temp = pd.concat(temp_list).reset_index(drop=True)
    return df_comb_temp.drop_duplicates() if isdict else df_comb_temp


def format_training_set(df1):
    """Format training set."""
    # in this dataset, there are sometimes multiple assigned harmonized uses
    # this splits them up when they couldn't be matched by the other function
    temp = []
    for name, row in df1.iterrows():
        n1 = [row['report_funcuse']]
        split_harm = split_funcuse(row['harmonized_funcuse'])
        for n2 in split_harm:
            new_series = {'report_funcuse': n1, 'harmonized_funcuse': n2}
            if 'raw_chem_name' in row:
                new_series['raw_chem_name'] = row['raw_chem_name']
            s = pd.Series(new_series)
            temp.append(s)
    df1_split = pd.concat(temp, axis=1).T

    # send to cleaning function
    oecd_clean = {clean_text(key.lower().strip(), ensure_word=True): key
                  for key in oecd_def.keys()}
    df1_fixed = match_oecd_syn(df1_split, oecd_clean)
    return df1_fixed


def format_splits(df2, df_default, strict=True):
    """Split both funcuse columns and check if they're even.

    This function looks at if there are multiple functional uses in the
    reported and harmonized columns in one line. If there are, it tries to
    match them up. If it can't, it either won't do anything or it will get
    rid of extra uses. To prevent this, have a training set with 1 to 1
    correlation between reported and harmonized functional use.

    The line 'len(harm) == 1 or len(rep) == 1' makes it so that only many
    to many rows will go through this filter. If every row went through it,
    it would probably be more accurate but throw out more data. This line
    is changed with the 'strict' parameter.
    """
    def split_list(x):
        """Split an input list."""
        x = x.replace('"', "'")
        x = x.lstrip('[').rstrip(']').strip("'")
        x = x.split("', '")
        return x

    def do_nothing(rep, harm, row, chems):
        """Return the originl values."""
        newrep = '|'.join(rep)
        newharm = '|'.join(harm)
        new_d = {'report_funcuse': newrep,
                 'harmonized_funcuse': newharm}
        if chems:
            new_d['raw_chem_name'] = row['raw_chem_name']
        new_s = pd.Series(new_d)
        return new_s

    def match_lists(rep, harm, row, chems, same=None):
        """Match values on lists."""
        if same is None:
            if len(rep) == len(harm):
                same = True
            else:
                same = False
        rem = []
        new_rep = []
        new_harm = []
        bad = False
        harm_clean = [clean_text(i.lower().strip(), ensure_word=True)
                      for i in harm]
        harm_d = {harm_clean[n]: i for n, i in enumerate(harm)}
        no_use_rep = []
        no_use_harm = []
        for i in rep:
            if same:
                match_list = [j for n, j in enumerate(harm_clean)
                              if n not in rem]
            else:
                match_list = harm_clean
            clean_i = clean_text(i.lower().strip(), ensure_word=True)

            if clean_i == '':
                continue

            if not same:
                map_match = df_default.loc[
                    (df_default['report_funcuse'] == i) |
                    (df_default['report_funcuse'] == clean_i),
                    'harmonized_funcuse'].to_list()
                new_l = [i for i in (harm+harm_clean) if i in map_match]
                if len(new_l) > 0:
                    new_val = [i for i in map_match if i in new_l][0]
                    new_rep.append(i)
                    new_harm.append(new_val)
                    continue
            if clean_i == '':
                print(f'------- Empty string: {row.name} -------')
            fuzzy_match = process.extractBests(clean_i,
                                               match_list,
                                               limit=2,
                                               scorer=fuzz.token_set_ratio)
            qual = len(fuzzy_match) == 1 or \
                fuzzy_match[0][1] - fuzzy_match[1][1] > 10
            if not same and fuzzy_match[0][1] < 50:
                qual = False
            if qual:
                new_rep.append(i)
                new_harm.append(harm_d[fuzzy_match[0][0]])
                rem_val = [n for n, j in enumerate(harm_clean)
                           if j == fuzzy_match[0][0] and n not in rem]
                if same:
                    rem.append(rem_val[0])
                else:
                    if len(rem_val) > 0:
                        rem.append(rem_val[0])
            elif same:
                bad = True
                break
            else:
                no_use_rep.append(i)

        if len(new_harm) == 0 or len(new_rep) == 0:
            bad = True

        if bad:
            if same:
                s_list = match_lists(rep, harm, row, chems, same=False)
            else:
                s_list = [do_nothing(rep, harm, row, chems)]
        else:
            s_list = []
            for n, i in enumerate(new_rep):
                new_d = {'report_funcuse': i,
                         'harmonized_funcuse': new_harm[n]}
                if chems:
                    new_d['raw_chem_name'] = row['raw_chem_name']
                new_s = pd.Series(new_d)
                s_list.append(new_s)
            if len(new_harm) < len(harm) and len(new_rep) < len(rep):
                no_use_harm = [i for n, i in enumerate(harm) if n not in rem]
                s_list.append(do_nothing(no_use_rep, no_use_harm, row, chems))
                print(f'------- Row {row.name} -------\n' +
                      'Added: ' + '|'.join(no_use_rep) + ' -> ' +
                      '|'.join(no_use_harm))

        if not same and not bad:
            no_harm = ', '.join([i for i in harm
                                 if i not in (new_harm+no_use_harm)])
            no_rep = ', '.join([i for i in rep
                                if i not in (new_rep+no_use_rep)])
            if len(no_harm) > 0 or len(no_rep) > 0:
                print(f'------- Row {row.name} -------\n' +
                      f'Removed from report_funcuse: {no_rep}\n' +
                      f'Removed from harmonized_funcuse: {no_harm}')
        return s_list

    new_rows = []
    chems = False
    if 'raw_chem_name' in df2.columns:
        chems = True

    for name, row in df2.iterrows():
        rep = row['report_funcuse']
        harm = row['harmonized_funcuse']
        if rep.startswith('[') and rep.endswith(']'):
            rep = split_list(rep)
        else:
            add = []
            if 'uv' not in rep.lower():
                add.append('/')
            if 'humectant' in rep.lower() or 'cleaning' in rep.lower():
                add.append('-')
            rep = split_funcuse(rep, add=add)
        if harm.startswith('[') and harm.endswith(']'):
            harm = split_list(harm)
        else:
            add = ['/'] if 'uv' not in rep.lower() else []
            harm = split_funcuse(harm, add=add)

        if strict and (len(harm) == 1 or len(rep) == 1):
            new_rows.append(do_nothing(rep, harm, row, chems))
        else:
            new_lists = match_lists(rep, harm, row, chems)
            for v in new_lists:
                new_rows.append(v)

    df_comb = pd.concat(new_rows, axis=1).T
    return df_comb


def get_training_set(df_default):
    """Get training data.

    Should be a dataframe with the following columns:
        report_funcuse: functional use
        harmonized_funcuse: assigned OECD functional use
        raw_chem_name: name of chemical, set to NAN if missing

    Load each training set and combine them at the end. There are a few
    functions you can use for cleaning help, format_training_set and
    format_splits.
    """
    # makes a blank dataframe
    df_blank = pd.DataFrame(
        columns=['report_funcuse', 'harmonized_funcuse', 'raw_chem_name'])

    # this is an example function reads the cpdat functional use table
    # feel free to make your own training data and combine multiple sources
    # df = cpdat_data()

    """
    Begin reading categorized_functions_05242018.xlsx
    """
    df1 = pd.read_excel('categorized_functions_05242018.xlsx') \
        .rename(columns={'reported_function': 'report_funcuse',
                         'technical_function': 'harmonized_funcuse'})
    df1 = df1[['report_funcuse', 'harmonized_funcuse']]
    df1['raw_chem_name'] = np.nan
    df1_formatted = format_training_set(df1)

    """
    Begin reading functional_use_data_cleaning_7-10-2020.csv
    """
    # df2 = pd.read_csv(
    #     'functional_use_data_cleaning_7-10-2020.csv', index_col=0) \
    #     .reset_index(drop=True) \
    #     .rename(columns={'reported_functional_use': 'report_funcuse',
    #                      'technical_function': 'harmonized_funcuse'})
    # df2 = df2[['report_funcuse', 'harmonized_funcuse']]
    # df2['raw_chem_name'] = np.nan

    # df2_formatted = format_training_set(df2)

    """
    Begin reading fudc_7-15-20.csv
    """
    df2 = pd.read_csv(
        'fudc_7-15-20.csv', index_col=0) \
        .reset_index(drop=True) \
        .rename(columns={'reported_functional_use': 'report_funcuse',
                         'technical_function': 'harmonized_funcuse'})
    df2 = df2[['report_funcuse', 'harmonized_funcuse']]
    # df2_split = format_splits(df2, df_default)
    df2_split = format_splits(df2, df_default, strict=False)
    df2_split['raw_chem_name'] = np.nan

    df2_formatted = format_training_set(df2_split)

    # combine
    df = pd.concat([df_blank, df1_formatted, df2_formatted])

    return df


def clean_training_data(opts):
    """Clean the training data and get embeddings."""
    # combine dataframes
    print('Getting training data...')
    df_default = get_default_set()
    df_training = get_training_set(df_default)
    df = pd.concat([df_default, df_training]).reset_index(drop=True)
    df['report_funcuse'] = df['report_funcuse'].apply(
        lambda x: re.sub(r'\s', ' ', x) if isinstance(x, str) else x)
    print('Done')

    # clean data
    print('Cleaning training data...')
    df_clean = run_cleaning(df, keep_na=True, multi=False)
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


def clean_testing_data(test_list, opts, raw_chems=None):
    """Clean the training data and get embeddings."""
    df = pd.DataFrame(
        columns=['report_funcuse', 'raw_chem_name'])
    df['report_funcuse'] = test_list
    df['raw_chem_name'] = raw_chems if raw_chems is not None else np.nan

    df['report_funcuse'] = df['report_funcuse'].apply(
        lambda x: re.sub(r'\s', ' ', x) if isinstance(x, str) else x)

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
    """Load training data or create new data. Reset re-cleans the data."""
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
