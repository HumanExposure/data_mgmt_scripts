# -*- coding: utf-8 -*-
"""Script for procsssing MSDS and produt labels.

Created on Fri Oct 18 11:34:22 2019

@author: SBURNS
"""

import os
import pandas as pd

from pdf_import import pdf_sort
from label_search import fun_label_search
from chem_search import (fun_chemicals, fun_chemicals_add, fun_chemicals_old,
                         fun_sec_search, fun_wide_search)
from formatting import chem_format, fix_dict


# blank variables
# step0_fail = 0  # pdfs which were not read successfully
# step1_fail = 0  # where a section was not found
# step1_success = 0  # pdfs with text successfully extracted

# not_pdf = []  # don't do anything with these
# not_sds = []  # not detected as an SDS
# too_3or4 = []  # examine and fix
# no_3or4 = []  # examine and fix
# needs_ocr = []  # pdfs that need ocr
# failed_files = []  # files that failed to load
# split_pdfs = []  # list of pdfs that had multiple msds (successful only)

# keys for all these were removed
# chemicals: key to section to list
# chemicals_old: key to list
# chemicals_add: key to list

# sec_search: key to section to list of dicts
# sec_search_wide: key to list of dicts
# old_search: key to list of dicts

# label_search: key to list
# label_search2: key to list (not anymore)


def pdf_extract(f, folder, do_OCR=True, all_OCR=False):
    """Take a filename and return chemical info."""
    # read pdf
    comb = pdf_sort(f, folder, do_OCR, all_OCR)

    # break out output (this info will be used to log)
    step0_fail = comb[3]
    step1_fail = comb[4]
    step1_success = comb[5]
    not_pdf = comb[6]
    not_sds = comb[7]
    too_3or4 = comb[8]
    no_3or4 = comb[9]
    needs_ocr = comb[10]
    failed_files = comb[11]
    split_pdfs = comb[12]

    # data for processing
    to_sec = comb[0]  # text and pdf where the important parts were parsed
    to_old = comb[1]  # text and pdf where the parsing failed
    to_label = comb[2]  # images of labels to parse

    # run functions
    sc = []
    named = []
    casno = []
    nlabel = []

    # search for information
    # all of these loops are 1 item long
    for key, val in to_sec.items():
        sc.append('sec')

        chemicals = fun_chemicals(key, val)
        chemicals_add = fun_chemicals_add(key, val, chemicals)
        sec_search = fun_sec_search(key, val)
        sec_search_wide = fun_wide_search(key, val)

        named = named + [j for i in sec_search for j in i]
        named = named + sec_search_wide
        casno = casno + [j for i in chemicals for j in i]
        casno = casno + chemicals_add

    for key, val in to_old.items():
        sc.append('old')

        chemicals_old = fun_chemicals_old(key, val)
        old_search = fun_wide_search(key, val)

        named = named + old_search
        casno = casno + chemicals_old

    for key, val in to_label.items():
        sc.append('label')

        label_search = fun_label_search(key, val)

        nlabel = nlabel + label_search

    # aggregate names
    named = [j for i in named for j in fix_dict(i)]
    df_search = pd.DataFrame(chem_format(named))
    df_search.drop_duplicates(inplace=True)

    # aggregate cas
    casno = [i for i in list(pd.unique(casno))
             if'cas' in df_search.columns and i not in df_search['cas'].values]
    to_add = []
    for n in casno:
        to_add.append({'name': '', 'cas': n, 'min_wt': '', 'cent_wt': '',
                       'max_wt': '', 'ci_color': ''})
    to_add_df = pd.DataFrame(to_add)

    # aggregate label info
    nlabel = chem_format([i for i in list(pd.unique(nlabel))
                          if 'name' in df_search.columns and
                          i not in df_search['name'].values])
    to_add_label = []
    for n in nlabel:
        to_add_label.append({'name': n, 'cas': '', 'min_wt': '', 'cent_wt': '',
                             'max_wt': '', 'ci_color': ''})
    to_add_label_df = pd.DataFrame(to_add_label)

    # combine
    df_comb = pd.concat([df_search, to_add_df, to_add_label_df]) \
        .reset_index(drop=True)
    if len(df_comb) == 0:
        df_comb = pd.DataFrame({'name': '', 'cas': '', 'min_wt': '',
                                'cent_wt': '', 'max_wt': '', 'ci_color': ''},
                               index=[0])
    df_comb = df_comb.loc[df_comb.apply(lambda x: 0 if x.sum().strip()
                                        == '' else 1, axis=1) == 1]

    df_comb.insert(0, 'filename', f.split('.pdf')[0] + '.csv')
    # df_store.append(df_comb)

    # create file info for log
    dinfo = {}
    dinfo['filename'] = f
    dinfo['OCR'] = True if len([i for i in needs_ocr if f in i]) > 0 else False
    dinfo['split'] = True if len([i for i in split_pdfs if f in i]) > 0 \
        else False
    if f in failed_files:
        dinfo['debug'] = 'failed'
    elif len(sc) == 0:
        dinfo['debug'] = 'missing'
    else:
        dinfo['debug'] = ','.join(list(pd.unique(sc)))
        if len(sc) > 1:
            print(sc)
    dinfo['num_found'] = len(df_comb)

    # info_df.append(dinfo)

    return df_comb, dinfo


# change the folder names here
folder = os.path.join(os.getcwd(), 'pdf')
out_folder = os.path.join(os.getcwd(), 'output')

# iterate through files
df_store = []
info_df = []
for f in os.listdir(folder):
    d1, d2 = pdf_extract(f, folder)
    df_store.append(d1)
    info_df.append(d2)


df_all = pd.concat(df_store).reset_index(drop=True)
file_prop = pd.DataFrame(info_df)

# write info file
df_all.to_csv(os.path.join(out_folder, 'chemical_data.csv'), index_label='row')
file_prop.to_csv(os.path.join(out_folder, 'file_info.csv'), index=False)
