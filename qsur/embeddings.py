# -*- coding: utf-8 -*-
"""Create the word embeddings for this project.

Created on Mon Feb 10 14:45:26 2020

@author: SBURNS
"""

from data import clean_text
from flair.data import Sentence
from flair.embeddings import (BertEmbeddings, FlairEmbeddings,
                              DocumentPoolEmbeddings,
                              StackedEmbeddings)
import torch
import os.path
import hashlib
import pandas as pd
import numpy as np
import joblib


def load_model(bert=None, document=False):
    """Load word embeddings model."""
    if bert == 'bio':
        # https://github.com/flairNLP/flair/issues/1085
        # also see readme for instructions
        bertpath = 'bert/bert-base-biobert-cased'
    elif bert == 'sci':
        # https://github.com/flairNLP/flair/issues/744
        # https://github.com/flairNLP/flair/issues/1239
        bertpath = 'bert/scibert_scivocab_uncased'
    else:
        bertpath = 'bert-base-uncased'

    bert_embedding = BertEmbeddings(
        bert_model_or_path=bertpath,
        pooling_operation='mean')
    flair_embedding_forward = FlairEmbeddings('en-forward')
    flair_embedding_backward = FlairEmbeddings('en-backward')

    if document:
        document_embeddings = DocumentPoolEmbeddings([bert_embedding,
                                                      # flair_embedding_backward,
                                                      # flair_embedding_forward,
                                                      ],
                                                     fine_tune_mode='nonlinear'
                                                     )
    else:
        document_embeddings = StackedEmbeddings([bert_embedding,
                                                 # flair_embedding_backward,
                                                 # flair_embedding_forward
                                                 ])

    return document_embeddings


def get_vector(sentence, document_embeddings, raw=False):
    """Get the document vector for input."""
    # sentence = Sentence(sen)
    document_embeddings.embed(sentence)

    if raw:
        return sentence.embedding

    def extract_embed(x):
        if x.device.type == 'cuda':
            return x.cpu().numpy()
        return x.numpy()

    if document_embeddings.embedding_type == 'word-level':
        embed_list = [extract_embed(token.embedding) for token in sentence]
    else:
        get_embed = sentence.get_embedding().detach()
        embed_list = [extract_embed(get_embed)]

    return embed_list


# oecd_dict = oecd_def
# ref = 'key'
# bert = 'bio'
# document = True
# raw_embeddings = False
# reset = False
# label = 'testing'


def make_list(oecd_dict, other_use, ref='key', bert='bio', document=False,
              reset=False, label='', raw_embeddings=False):
    """Make a list of all functional uses in model.

    Other_use should be a dataframe of uses from factotum that you want to
    match to the OECD list.
    """
    def oecd_choose(title, text, ref):
        if ref == 'key':
            value = clean_text(title.lower().strip(), ensure_word=True)
        elif ref == 'value':
            value = clean_text(text.lower().strip(), ensure_word=True)
        elif ref == 'comb':
            value = clean_text(
                title.lower().strip() + '. ' + text.lower().strip(),
                ensure_word=True)
        return value

    print('Loading model data...')
    # read stored embeddings
    doc_path = 'store/document_embeddings_' + bert + \
        str('_document' if document else '') + '.pt'
    embed_path = 'store/stored_embeddings_' + bert + \
        str('_document' if document else '') + ('_' + label).rstrip('_') \
        + str('_raw' if raw_embeddings else '') + '.pt'
    document_embeddings = load_model(bert=bert, document=document)
    if (os.path.exists(doc_path) and not reset):
        document_embeddings.load_state_dict(torch.load(doc_path))
        document_embeddings.eval()
        if os.path.exists(embed_path):
            stored_embeddings = torch.load(embed_path)
            try:
                stored_embeddings.eval()
            except AttributeError:
                pass
        else:
            stored_embeddings = {}
    else:
        torch.save(document_embeddings.state_dict(), doc_path)
        stored_embeddings = {}
    print('Done')

    # dictionaries to store info
    original_dict = {}  # dict mapping the oecd keys to names
    original_dict_key = {}  # always generate hashes of clean keys
    text_dict = {}  # dict maping all keys to clean names
    embed_dict = {}  # dict mapping keys to embeddings
    sen_dict = {}  # store sentances for tfidf
    use_list = []

    print('Getting embeddings for OECD functional uses...')
    # put OECD into into dicts
    for key, value in oecd_dict.items():
        # print(key)
        orig_key = oecd_choose(key, value, 'key')
        orig_key_hash = hashlib.sha3_224(orig_key.encode()).hexdigest()
        original_dict_key[orig_key_hash] = key

        newval = oecd_choose(key, value, ref)
        newkey = hashlib.sha3_224(newval.encode()).hexdigest()
        if newkey in original_dict.keys():
            continue
        original_dict[newkey] = key
        sen = Sentence(newval)
        sen_dict[newkey] = sen
        text_dict[newkey] = newval
        if newkey in stored_embeddings.keys():
            embed_dict[newkey] = stored_embeddings[newkey]
        else:
            new_embed = get_vector(sen, document_embeddings, raw_embeddings)
            stored_embeddings[newkey] = new_embed
            embed_dict[newkey] = new_embed
    print('Done')

    # get list of uses from other list
    use_unique = list(pd.unique(
        [i for flist in other_use
         for i in flist if len(i) > 0]
        ))

    print('Getting embeddings for user-specified functional uses...')
    # put other uses into dicts
    for newval in use_unique:
        # print(newval)
        newkey = hashlib.sha3_224(newval.encode()).hexdigest()
        use_list.append(newkey)
        if newkey in original_dict.keys() or newkey in text_dict.keys():
            continue
        sen = Sentence(newval)
        sen_dict[newkey] = sen
        text_dict[newkey] = newval
        if newkey in stored_embeddings.keys():
            embed_dict[newkey] = stored_embeddings[newkey]
        else:
            new_embed = get_vector(sen, document_embeddings, raw_embeddings)
            stored_embeddings[newkey] = new_embed
            embed_dict[newkey] = new_embed
    print('Done')

    torch.save(stored_embeddings, embed_path)
    print('Finished getting embeddings.')

    return original_dict, original_dict_key, text_dict, embed_dict, \
        sen_dict, use_list


def change_to_cosine_distance(val, sorted_oecd_hashes, embed_dict):
    """Calculate cosine similarity."""
    store_vals = []
    for key in sorted_oecd_hashes:
        cos = torch.nn.CosineSimilarity(dim=0, eps=1e-6)
        sim = cos(embed_dict[key], embed_dict[val])
        store_vals.append(float(sim))
    return np.array(store_vals)


def cosine_function(df, original_dict, embed_dict, label, reset=False):
    """Measure the cosine distance to each OECD functional use."""
    # ensure the order of the OECD keys
    label = '' if len(label) == 0 else '_' + label.strip('_')
    print('Building model with cosine similarity')
    sorted_keys = sorted(original_dict.keys())
    sorted_fname = os.path.join('store', f'sorted_oecd_hashes{label}.joblib')
    if os.path.exists(sorted_fname) and not reset:
        old_keys = joblib.load(sorted_fname)
        if old_keys != sorted_keys:
            print('OECD dictionary has changed, cannot calculate cosine sim')
            return None
    else:
        joblib.dump(sorted_keys, sorted_fname)

    # iterate through provided data
    store_data = {}
    store_name = os.path.join('store', f'cosine_sim_data{label}.joblib')
    if os.path.exists(store_name) and not reset:
        store_data = joblib.load(store_name)
    hashlist = df['clean_funcuse_hash'] \
        .apply(lambda x: x if isinstance(x, str)
               else (x[0] if len(x) == 1 else np.nan)) \
        .dropna().drop_duplicates()
    for val in hashlist:
        if val not in store_data.keys():
            new_arr = change_to_cosine_distance(val, sorted_keys, embed_dict)
            store_data[val] = new_arr
    joblib.dump(store_data, store_name)

    # actually assign names
    return_val = [store_data[val] if isinstance(val, str) else
                  store_data[val[0]] for val in df['clean_funcuse_hash']]

    return return_val
