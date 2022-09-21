#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Various functions to help process modeling datasets.

Created on Thu Jun 17 10:26:19 2021

@author: jwall01
"""

import os
import sys
import json
from sqlalchemy import create_engine
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy
#from joblib import Parallel, delayed
import joblib
#import pandas as pd
from flair.data import Sentence
from flair.embeddings import (WordEmbeddings, FlairEmbeddings,
                              DocumentPoolEmbeddings,
                              BytePairEmbeddings)

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
stop_words = set(stopwords.words('english'))
# words to exclude
exclude = ['count', 'percent', 'inc', 'llc', 'ltd', 'co', 
           'corp', 'company', 'enterprise', 'group', 'div', 
           'corporation', 'mfg', 'division', 'incorporate', 
           'dept', 'department', 'brand', 'manufacture']

if os.name == 'nt':
    nlpname1 = 'Lib\\site-packages\\en_core_web_sm\\'
    nlpname2 = os.path.join(os.path.dirname(sys.executable), nlpname1)
    model = max([i for i in os.listdir(nlpname2) if re.fullmatch(
                r'(?:en_core_web_sm-\d{1,2}[\.]\d{1,2}[\.]\d{1,2})', i)])
    nlpname = os.path.join(nlpname2, model)
else:
    nlpname = 'en_core_web_sm'

spacy_nlp = spacy.load(nlpname)

def escape_string(s):
    if isinstance(s, str):
        return s.replace("'", "''")
    
def load_env_file(f, l=None):
    """
    Parameters
    ----------
    f : str, required
        File name of environmental variable file to load (in JSON format).
    l : str, optional
        JSON level to return.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    with open(f, 'r') as f:
        if l: #Select level if provided
            return json.load(f)[l]
        else: #Return whole env file JSON
            return json.load(f)

def read_df():
    """Read df of brand name and puc from factotum."""
    cfg = load_env_file("env.json", "mysql")
    # with open('mysql.json', 'r') as f:
    #     cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           echo=False)
    #puc_id, product_id, brand_name, title, gen_cat, prod_fam, prod_type, description
    p = pd.read_sql('select id As product_id, brand_name, title , manufacturer '+ \
                    'from dashboard_product', engine)
    #Get producttopuc without model assignments (AU)
    ptp = pd.read_sql('select product_id, puc_id, classification_method_id, updated_at '+ \
                      'from dashboard_producttopuc WHERE classification_method_id ' + \
                      '!= "AU"', engine)
    puc = pd.read_sql('select p.id As puc_id, p.gen_cat, p.prod_fam, p.prod_type, pk.code As kind, p.description '+ \
                      'from dashboard_puc p left join dashboard_puckind pk ' + \
                      'on p.kind_id = pk.id'    , engine)
    engine.dispose()
    #Filter ptp to Uber PUC (MA > RU > MB > BA > AU)
    #Get list of product_id with only 1 PUC assignment
    tmp = ptp.groupby('product_id').classification_method_id.count()
    tmp = tmp[tmp == 1].index.tolist()
    #Split ptp into 2 dfs by PUC assignment count
    ptp_1 = ptp[ptp.product_id.isin(tmp)] #1 PUC Assignment
    ptp_2 = ptp[~ptp.product_id.isin(tmp)] #>1 PUC Assignment
    #Subset each by classificaiton method, but without products in previous sets
    ptp_2_MA = ptp_2[ptp_2.classification_method_id == "MA"]
    filterList = ptp_2_MA.product_id.unique().tolist()
    ptp_2_RU = ptp_2[(ptp_2.classification_method_id == "RU") & 
                     (~ptp_2.product_id.isin(filterList))]
    filterList = ptp_2_MA.product_id.unique().tolist() + \
                 ptp_2_RU.product_id.unique().tolist()
    ptp_2_MB = ptp_2[(ptp_2.classification_method_id == "MB") & 
                     (~ptp_2.product_id.isin(filterList))]
    filterList = ptp_2_MA.product_id.unique().tolist() + \
                 ptp_2_RU.product_id.unique().tolist() + \
                 ptp_2_MB.product_id.unique().tolist()
    ptp_2_BA = ptp_2[(ptp_2.classification_method_id == "BA") &
                     (~ptp_2.product_id.isin(filterList))]
    
    #Filter to most recent assignment date (if multiple within a subset)
    ptp_2_MA = ptp_2_MA.groupby('product_id').agg(lambda x: x.iloc[x.updated_at.argmax()])        
    ptp_2_RU = ptp_2_RU.groupby('product_id').agg(lambda x: x.iloc[x.updated_at.argmax()])
    ptp_2_MB = ptp_2_MB.groupby('product_id').agg(lambda x: x.iloc[x.updated_at.argmax()])
    ptp_2_BA = ptp_2_BA.groupby('product_id').agg(lambda x: x.iloc[x.updated_at.argmax()])
    
    #Combine filtered ptp subsets
    ptp_filtered = ptp_1.append(ptp_2_MA, ignore_index=True)
    ptp_filtered = ptp_filtered.append(ptp_2_RU, ignore_index=True)
    ptp_filtered = ptp_filtered.append(ptp_2_MB, ignore_index=True)
    ptp_filtered = ptp_filtered.append(ptp_2_BA, ignore_index=True)
    #Merge final dataset
    df = p.merge(ptp_filtered, left_on='product_id', right_on='product_id', suffixes=(False, False))
    df = df.merge(puc, left_on='puc_id', right_on='puc_id', suffixes=(False, False))
    
    return df.fillna('')

def read_df_uber():
    """Read df of brand name and puc from factotum."""
    cfg = load_env_file("env.json", "mysql")
    # with open('mysql.json', 'r') as f:
    #     cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           echo=False)
    #puc_id, product_id, brand_name, title, gen_cat, prod_fam, prod_type, description
    p = pd.read_sql('select id As product_id, brand_name, title , manufacturer '+ \
                    'from dashboard_product', engine)
    #Get producttopuc without model assignments (AU)
    ptp = pd.read_sql('select product_id, puc_id, classification_method_id, updated_at '+ \
                      'from dashboard_producttopuc WHERE classification_method_id ' + \
                      '!= "AU" AND is_uber_puc = 1', engine)
    puc = pd.read_sql('select p.id As puc_id, p.gen_cat, p.prod_fam, p.prod_type, pk.code As kind, p.description '+ \
                      'from dashboard_puc p left join dashboard_puckind pk ' + \
                      'on p.kind_id = pk.id'    , engine)
    engine.dispose()
    
    df = p.merge(ptp, left_on='product_id', right_on='product_id', suffixes=(False, False))
    df = df.merge(puc, left_on='puc_id', right_on='puc_id', suffixes=(False, False))
        
    return df.fillna('')

def read_group(group):
    """Read df of brand name and puc from factotum."""
    cfg = load_env_file("env.json", "mysql")
    # with open('mysql.json', 'r') as f:
    #     cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           echo=False)
    sqq = 'select p.id As product_id, p.brand_name, p.title, p.manufacturer, dd.data_group_id ' + \
          'from dashboard_datadocument dd ' + \
          'left join dashboard_productdocument pd on dd.id = pd.document_id ' + \
          'left join dashboard_product p on p.id = pd.product_id ' + \
          'left join dashboard_producttopuc ptp on p.id = ptp.product_id ' + \
          f'where data_group_id in ({",".join([str(x) for x in group])}) and puc_id IS NULL; '
    df = pd.read_sql(escape_string(sqq), engine)
    engine.dispose()
    return df.fillna('')

def read_puc_types(puc_type='all'):
    """Get list of pucs by type"""
    if puc_type == 'all':
        puc_type = '(\'UN\', \'FO\', \'AR\', \'OC\')'
    else:
        puc_type = '(\'' + puc_type  + '\')'
    
    cfg = load_env_file("env.json", "mysql")
    # with open('mysql.json', 'r') as f:
    #     cfg = json.load(f)['mysql']
    engine = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                           f'{cfg["password"]}@{cfg["server"]}:' +
                           f'{cfg["port"]}/{cfg["database"]}?charset=utf8mb4',
                           echo=False)
    sqq = 'SELECT puc.id, puc.gen_cat, puc.prod_fam, puc.prod_type ' + \
          'FROM prod_factotum.dashboard_puc puc ' + \
          'LEFT JOIN dashboard_puckind pk on puc.kind_id=pk.id ' + \
          f'WHERE pk.code IN {puc_type};'
    df = pd.read_sql(sqq, engine)
    engine.dispose()
    return df.fillna('')

def load_df(label=''):
    """Load the training data."""
    lab = '' if len(label) == 0 else '_' + label.strip('_')
    return joblib.load(f'models/model{lab}/input/training_data{lab}.joblib')

def standardize(x): #Function to strip whitespace and lowercase strings
        try:
            return x.str.strip().str.lower()
        except AttributeError:
            return x
        
def clean_str(brand, title, manufacturer):
    """Clean a product brand and name to prepare it for the model."""
    brand = brand.str.strip().str.lower()
    brand = brand.str.replace('generic|unknown', '')
    title = title.str.strip().str.lower()
    manufacturer = manufacturer.str.strip().str.lower()
    name = clean(brand, title, manufacturer)
    return name

#https://prrao87.github.io/blog/spacy/nlp/performance/2020/05/02/spacy-multiprocess.html#Option-2:-Use-nlp.pipe
def lemmatize_pipe(doc):
    lemma_list = [str(tok.lemma_).lower() for tok in doc
                  if tok.is_alpha and tok.text.lower() not in stop_words] 
    return lemma_list

def preprocess_pipe(texts):
    preproc_pipe = []
    for doc in spacy_nlp.pipe(texts, batch_size=1000):
        preproc_pipe.append(' '.join(lemmatize_pipe(doc)))
    return preproc_pipe

def chunker(iterable, total_length, chunksize):
    return (iterable[pos: pos + chunksize] for pos in range(0, total_length, chunksize))

def flatten(list_of_lists):
    "Flatten a list of lists to a combined list"
    return [item for sublist in list_of_lists for item in sublist]

def process_chunk(texts):
    preproc_pipe = []
    for doc in spacy_nlp.pipe(texts, batch_size=20):
        preproc_pipe.append(' '.join(lemmatize_pipe(doc)))
    return preproc_pipe

def preprocess_parallel(texts, chunksize=100):
    executor = joblib.Parallel(n_jobs=7, backend='multiprocessing', prefer="processes")
    do = joblib.delayed(process_chunk)
    tasks = (do(chunk) for chunk in chunker(texts, len(texts), chunksize=chunksize))
    result = executor(tasks)
    return flatten(result)

# test for reintroduced stopwords
def name_check(a):
    tmp = ' '.join([i.strip() for i in a.split() if i not in
                  stop_words and i not in exclude])
    if len(a) > 0 and len(tmp) == 0:
        print(f'Name error: {a} - {tmp}')
        return ' '.join([i.strip() for i in a.split() if i not in exclude])
    else:
        return tmp
    
#Function to remove duplicate words
#https://www.codegrepper.com/code-examples/python/python+remove+duplicates+words+from+string
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

# name processing
def clean(brand, title, manufacturer):
    """Cleanup name."""
    #Dictionary of things to replace
            # remove umlauts
    char = {"ä": "a", "ö": "o", "ü": "u", "Ä": "A", "Ö": "O", "Ü": "U",
            # remove possessives
            r'([\w]+)[\'][s]\b': r'\g<1>',
            # remove numbers
            r'[\<\>\s]?\d{1,}[.]?\d{0,}[\s\%]?(?:fl)?\s?(?:oz)?' +
                   r'(?:lb[s]?)?\s?(?:mm)?\s?(?:g)?\s?(?:ml)?\s?(?:ct)?' +
                   r'\s?(?:pc)?\s?': ' ',
            # taking regex stuff from here
            # https://stackabuse.com/text-classification-with-python-and-scikit-learn/
            '-': '',
            r'[\W_]': ' ',
            r'\s+[a-zA-Z]\s+': ' ',
            r'^[a-zA-Z]\s+': ' ',
            r'\s+[a-zA-Z]$': ' '
                   }
    #Replace based on the dictionary above
    brand = brand.replace(char, regex=True)
    title = title.replace(char, regex=True)
    manufacturer = manufacturer.replace(char, regex=True)
    
    #Combine brand and title, remove duplicate words
    name = pd.concat([brand,title, manufacturer], axis=1)
    name = name.brand_name + ' ' + name.title + ' ' + name.manufacturer
    name = name.apply(lambda x: ' '.join(unique_list(x.split())))
    # remove double spaces
    name = name.str.replace(r'\s+', ' ', flags=re.I)
    # lemmatization
    
    lem = preprocess_parallel(name, chunksize=1000)    
    lem = pd.Series(lem, index=name.index.tolist()).apply(name_check)
    #lem2 = lem.set_index(name.index.tolist())
    # clean again
    regList = {r'(?:-PRON-)': '',
               r'[\W_]': ' ',
               r'\s+': ' ',
               r'\s+[a-zA-Z]\s+': ' ',
               r'^[a-zA-Z]\s+': ' ',
               r'\s+[a-zA-Z]{1,2}$': ' '
               }
    
    lem = lem.replace(regList, regex=True)#, flags=re.I)
    
    return lem.str.strip()

def load_doc_embeddings():
    """Load word embeddings model."""
    fasttext_embedding = WordEmbeddings('en-crawl')
    byte_embedding = BytePairEmbeddings('en')
    flair_embedding_forward = FlairEmbeddings('en-forward')
    flair_embedding_backward = FlairEmbeddings('en-backward')

    document_embeddings = DocumentPoolEmbeddings([fasttext_embedding,
                                                  byte_embedding,
                                                  flair_embedding_backward,
                                                  flair_embedding_forward#Removed extraneous comma here, suprised it didn't cause an error???
                                                  ],
                                                 fine_tune_mode='nonlinear')
    return document_embeddings

def get_vector(sen, document_embeddings):
    """Get the document vector for input."""
    if isinstance(sen, pd.Series):
        sentence = [Sentence(i) for i in sen]
        document_embeddings.embed(sentence)
        get_embed = [i.get_embedding().detach() for i in sentence]
        if any([i.device.type == 'cuda' for i in get_embed]):
            return [x.cpu().numpy() for x in get_embed]
        return [x.numpy() for x in get_embed]
    else:
        sentence = Sentence(sen)
        document_embeddings.embed(sentence)
        get_embed = sentence.get_embedding().detach()
        if get_embed.device.type == 'cuda':
            return get_embed.cpu().numpy()
        return get_embed.numpy()