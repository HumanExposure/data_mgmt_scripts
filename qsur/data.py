# -*- coding: utf-8 -*-
"""Read functional use data.

Created on Mon Jan 27 10:46:40 2020

@author: SBURNS
"""

import json
import re
import os
import sys

# import nltk
# from nltk.corpus import stopwords
import numpy as np
import spacy
from sqlalchemy import create_engine
from pymysql import escape_string
import pandas as pd
from multiprocessing import Pool


# def load_stopwords():
#     """Load NLTK stopwords."""
#     nltk.download('stopwords')
#     nltk.download('punkt')
#     stop_words = set(stopwords.words('english'))
#     return stop_words


def load_spacy():
    """Load spacy model."""
    if os.name == 'nt':
        nlpname1 = 'Lib\\site-packages\\en_core_web_sm\\'
        nlpname2 = os.path.join(os.path.dirname(sys.executable), nlpname1)
        model = max([i for i in os.listdir(nlpname2) if re.fullmatch(
                    r'(?:en_core_web_sm-\d{1,2}[\.]\d{1,2}[\.]\d{1,2})', i)])
        nlpname = os.path.join(nlpname2, model)
    else:
        nlpname = 'en_core_web_sm'
    spacy_nlp = spacy.load(nlpname)
    return spacy_nlp


# load vars
# stop_words = load_stopwords()
spacy_nlp = load_spacy()


def read_df(table, engine):
    """Read info from factotum."""
    sql = 'SELECT raw_chem_name, raw_cas, dsstox_id, report_funcuse ' + \
          'FROM (SELECT chem_id as rawchem_ptr_id, report_funcuse FROM ' + \
          table + ') AS t1 INNER JOIN ' + \
          '(SELECT id, raw_cas, raw_chem_name, dsstox_id FROM ' + \
          'dashboard_rawchem) AS t2 ON t1.rawchem_ptr_id = t2.id;'
    df = pd.read_sql(escape_string(sql), engine)
    return df.apply(lambda x: x.str.strip().str.lower()
                    if x.dtype == object else x).replace('', np.nan)


def read_data(tables):
    """Make SQL connectable."""
    with open('mysql.json', 'r') as f:
        cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           convert_unicode=True, echo=False)

    data_list = [read_df(i, engine) for i in tables]
    engine.dispose()
    return data_list


def check_funcuse(x):
    """Check if the functional use is valid, remove some weird ones."""
    if type(x) is not str:
        if pd.notna(x):
            print(x)
        return np.nan
    if not re.search(r'\w{2,}', x):
        return np.nan
    if 'unknown' in x.lower():
        return np.nan
    if 'none' in x.lower():
        return np.nan
    if '%' in x:
        return np.nan
    if len(x) > 70 and x.endswith('.'):
        return np.nan
    sen = spacy_nlp(x)
    if len([1 for token in sen if token.is_stop]) > 4:
        return np.nan
    if len([1 for token in sen]) > 10:
        return np.nan
    # if len([i for i in x.split() if i in stop_words]) > 4:
    #     return np.nan
    x = re.sub(r'[\(].*[\)]', ' ', x).strip()
    x = re.sub(r'\s+', ' ', x)
    if x.strip() == '':
        return np.nan
    return x.strip()


def make_lower(x):
    """Make lowercase."""
    if type(x) is not str:
        if pd.notna(x):
            print(x)
        return np.nan
    return x.strip().lower()


def split_funcuse(x):
    """Split the functional uses into a list."""
    if pd.isna(x):
        return np.nan
    y = [x]
    syms = [', ', '/ ', '; ', '|']

    for s in syms:
        y = [j.strip() for i in y for j in i.split(s)]

    return y


def replace_hyphen(x):
    """Remove spacing with certain hyphens."""
    x = x.replace('anti-', 'anti')
    x = x.replace('de-', 'de')
    x = x.replace('re-', 're')
    x = x.replace('non-', 'non')
    x = x.replace('un-', 'un')
    return x


def clean_text(x, do_lemma=True, remove_symbols=True, ensure_word=False):
    """Clean a string."""
    # words to exclude
    exclude = []

    # remove umlauts
    char = {"ä": "a", "ö": "o", "ü": "u", "Ä": "A", "Ö": "O", "Ü": "U"}
    for key, val in char.items():
        if key in x:
            x = x.replace(key, val)

    # remove hyphenated things
    x = replace_hyphen(x)

    # things at end to remove
    resplit = re.split(r'(?:see also|see (?:closely )?related)[\:][^\.]+[.]$',
                       x, flags=re.I)
    if len(resplit) > 1:
        x = ' '.join(resplit[:-1]).strip()

    # remove posessives
    x = re.sub(r'([\w]+)[\'][s]\b', r'\g<1>', x)

    # remove numbers
    x = re.sub(r'\d', '', x)

    # taking regex stuff from here
    # https://stackabuse.com/text-classification-with-python-and-scikit-learn/
    # x = x.replace('-', '')
    x = re.sub(r'([^\s])(?!\s+)[\W_]([^\s])', r'\g<1> \g<2>', x)
    x = re.sub(r'[\W_]', ' ', x) if remove_symbols else x

    # remove short words
    x = re.sub(r'\s+[a-zA-Z]{1,2}\s+', ' ', x)
    x = re.sub(r'^[a-zA-Z]{1,2}\s+', ' ', x)
    x = re.sub(r'\s+[a-zA-Z]{1,2}$', ' ', x)
    x = re.sub(r'^[a-zA-Z]{1,2}$', ' ', x)

    sen = spacy_nlp(x)

    # lemmatization and remove stopwords
    def get_lemma(redo=False):
        if do_lemma:
            lem = ' '.join([token.lemma_ for token in sen if
                            ((token.is_alpha or not remove_symbols)
                             and (not token.is_stop or redo))
                            and token.lemma_ not in exclude])
        else:
            lem = ' '.join([token.text for token in sen if
                            ((token.is_alpha or not remove_symbols)
                             and (not token.is_stop or redo))
                            and token.text not in exclude])
        return lem

    lem = get_lemma()
    if ensure_word and len(lem) == 0:
        lem = get_lemma(redo=True)

    # clean again
    lem = re.sub(r'(?:-PRON-)', '', lem)
    lem = re.sub(r'[\W_]', ' ', lem) if remove_symbols else lem
    lem = re.sub(r'\s+', ' ', lem, flags=re.I)
    lem = re.sub(r'\s+[a-zA-Z]{1,2}\s+', ' ', lem)
    lem = re.sub(r'^[a-zA-Z]{1,2}\s+', ' ', lem)
    lem = re.sub(r'\s+[a-zA-Z]{1,2}$', ' ', lem)
    lem = re.sub(r'^[a-zA-Z]{1,2}$', ' ', lem)

    return lem.strip()


def clean_funcuse(xlist):
    """Clean up the functional use a little bit."""
    if type(xlist) is float and \
            pd.isna(xlist):
        return np.nan
    elif pd.isna(xlist).sum() > 0:
        return np.nan
    newlist = []
    for x in xlist:
        y = x
        y = y.replace('proprietary', '')

        reg = re.match(r'\w+[:]\s?(.{3,})$', y)
        if reg:
            y = reg.group(1).strip()
        y = re.sub(r'\s?[\(][^\)]+$', '', y)
        y = clean_text(y, do_lemma=True, ensure_word=True)

        if len(y) != 0:
            newlist.append(y.strip())
    if len(newlist) == 0:
        return np.nan
    return newlist


def is_chemical(chem_name, funcuse):
    """Determine if the use is a chemical name."""
    excl = ['color', 'fragrance', 'flavor']
    if chem_name in funcuse and chem_name != funcuse:
        if not [i for i in excl if i in chem_name]:
            val = re.search(r'\b(?:' + re.escape(chem_name) +
                            r'(?:[\-]\w*)*|(?:\w*[\-])*' +
                            re.escape(chem_name) + r')\b',
                            funcuse, flags=re.I)
            if val:
                new = re.sub(r'\b(?:' + val.group(0) + r')\b',
                             '', funcuse).strip()
                return new
            # print('Name in use: ' + chem_name + ' ||| ' + funcuse)
    # check how long/how many words, what percentage it is
    return funcuse


def filter_funcuse(x):
    """Filter out bad uses."""
    name = x['raw_chem_name']
    if pd.isna(name):
        return x
    if type(x['report_funcuse']) is float and \
            pd.isna(x['report_funcuse']):
        return x
    elif pd.isna(x['report_funcuse']).sum() > 0:
        return x
    y = x.copy()
    y['report_funcuse'] = [is_chemical(name, i) for i in x['report_funcuse']]

    if y['report_funcuse'] != x['report_funcuse']:
        # print(str(name) + ': ' + str(x['report_funcuse']) + ' ---> ' +
        #       str(y['report_funcuse']))
        pass

    if len(y['report_funcuse']) == 0:
        y['report_funcuse'] = np.nan
    return y


def run_functions(x):
    """Run functions for cleaning the code."""
    # row['report_funcuse'] = df['report_funcuse'].apply(check_funcuse)
    # row['report_funcuse'] = df['report_funcuse'].apply(split_funcuse)
    # row = df.apply(filter_funcuse, axis=1)
    # row['report_funcuse'] = df['report_funcuse'].apply(clean_funcuse)

    row = x.copy()
    row['report_funcuse'] = make_lower(row['report_funcuse'])
    row['report_funcuse'] = check_funcuse(row['report_funcuse'])
    row['report_funcuse'] = split_funcuse(row['report_funcuse'])
    row = filter_funcuse(row)
    row['report_funcuse'] = clean_funcuse(row['report_funcuse'])

    # df = df.dropna(subset=['report_funcuse'])

    return row


def run_cleaning(df, keep_na=True):
    """Run the cleaning with multiprocessing."""
    with Pool() as p:
        clean_df = [i for i in p.imap(run_functions,
                                      [row for name, row in df.iterrows()],
                                      1000)]

    comb = pd.concat(clean_df, axis=1).T

    if not keep_na:
        comb = comb.dropna(subset=['report_funcuse'])

    return comb


def factotum_data():
    """Read data from factotum."""
    df_list = read_data(['dashboard_functionaluse',
                         ])
    df = pd.concat(df_list).dropna(subset=['report_funcuse']) \
        .dropna(subset=['raw_chem_name', 'raw_cas', 'dsstox_id'], how='all')
    return df


def cpdat_data():
    """Read CPDat table for offline testing."""
    df = pd.read_excel('functional_uses.xlsx')
    df = df[['harmonized_functional_use', 'reported_functional_use']] \
        .dropna(subset=['harmonized_functional_use']) \
        .rename(columns={'harmonized_functional_use':
                         'harmonized_funcuse',
                         'reported_functional_use':
                         'report_funcuse'})
    df['raw_chem_name'] = np.nan
    return df


if __name__ == '__main__':
    """Testing code."""

    df = factotum_data()
    df1 = run_cleaning(df, keep_na=True)
    df2 = run_cleaning(df, keep_na=False)

    df_test = pd.unique([j for i in df['report_funcuse'] for j in i])

    def check(x):
        """Test."""
        val = 'herbicide metabolite'
        for i in x:
            if val in i:
                return True
        return False

    q = df2.loc[df2['report_funcuse'].apply(check)]

    for i in df['report_funcuse'].sample(25):
        print(i)

    for name, row in df.sample(25).iterrows():
        print(row['report_funcuse'] + ' ||||| ' + str(row['raw_chem_name']))

    xlist = df['report_funcuse'].iloc[10] + ['ff']
    if pd.isna(xlist):
        pass
