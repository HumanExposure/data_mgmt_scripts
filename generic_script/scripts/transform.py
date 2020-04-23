# -*- coding: utf-8 -*-
"""Transform the script output into the correct format for factotum.

Created on Tue Mar  3 10:26:09 2020

@author: SBURNS
"""

import pandas as pd
import numpy as np
import os
import re

import requests
from bs4 import BeautifulSoup
import unicodedata
import time
import random

from fuzzywuzzy import fuzz

from formatting import chem_format, fix_dict, symbol_cleanup


# regex taken from chem_match.py
r_sym = re.compile(r'\d(?:[\.]|\s?[\-]{1,3}\s?)\d', re.I)
r_num = re.compile(r'\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}\s{0,2}|\b)' +
                   r'\d{1,3}(?:[\.\,]\d{1,6})?)[\s\%\*]{0,2}(?:\s{0,4}' +
                   r'[\-]{1,3}\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})?' +
                   r'\d{1,3}(?:[\,\.]\d{1,6})?)\b)?[\%\*]{0,2}(?![^\s])\s*?',
                   re.I)
r_num2 = re.compile(r'\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}\s{0,2}|\b)' +
                    r'\d{1,3}(?:[\.\,]\d{1,6})?)[\s\%\*]{0,2}(?:\s{0,4}' +
                    r'[\-]{1,3}\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})?' +
                    r'\d{1,3}(?:[\,\.]\d{1,6})?)\b)?[\%\*]{0,2}' +
                    r'(?![^\s\-\<\=])\s*?',
                    re.I)
r_docid = re.compile(r'(?:document_)(\d{6})(?:\.pdf)')
pmap = {0: [0],
        1: [1],
        2: [2],
        3: [1, 2],
        4: [4],
        5: [1, 4],
        6: [2, 4],
        7: [1, 2, 4]}


def check_line(x):
    """Check a line to see if it still has weights.

    Input is a row from a dataframe (series). Return edited series.
    """
    r = ' ' + x['name'] + ' '
    xnew = x.copy()

    # if (re.search(r_sym, r) or '%' in r) and (x['cent_wt'] != '' and
    #                                           int(x['cent_wt']) == 100):
    r_search = re.search(r_sym, r)
    if (r_search or '%' in r) and \
            (x['cent_wt'] != '' and (
                int(x['cent_wt']) == 100 or
                ((r_search and
                  re.search(r_search.group(0) + r'[\s\d]*[\%]', r)) and
                 (x['cent_wt'] > 50 and '.' not in str(x['cent_wt']))
                 ))):
        d = {}
        new_name = r
        for gwt in re.finditer(r_num, r):

            full_match = gwt.group(0)
            if '.' not in full_match and '%' not in full_match:
                continue

            wt = ''
            unit = ''
            gp = [i for i in gwt.groups() if i is not None]
            if len(gp) == 1:
                wt = str(gp[0])
            elif len(gp) == 2:
                wt = str(gp[0]) + '-' + str(gp[1])
            elif len(gp) > 2:
                print('WT Error: ' + str(gp))
                continue
            wt = wt.replace(' ', '') + unit

            new_name = r.replace(full_match, ' ')
            new_name = re.sub(r'\s+', ' ', new_name).strip()

            print('---- ' + str(x.name) + ' ----')
            print(r + ' ---> ' + new_name)

            dtemp = {'cas': x['cas'], 'wt': wt}
            if not (pd.isna(x['ci_color']) or x['ci_color'] == ''):
                dtemp['ci_color'] = x['ci_color']
            d[new_name] = dtemp

        if len(d) > 0:
            dfix = fix_dict(d)
            dnew = chem_format(dfix)[0]

            for key, val in dnew.items():
                xnew[key] = val

    return xnew


def fix_range(x):
    """Fix entire range not being picked up."""
    # 11963, 11962, 55824
    if x['cent_wt'] == '':
        return x
    r = ' ' + x['name'] + ' '
    cwt = x['cent_wt']

    # handle secret at end
    secret = False
    if len(r) > 0:
        if re.search(r'\s*(?:- secret)\s?$', r):
            r = re.sub(r'\s*(?:- secret)\s?$', '', r).strip()
            secret = True

    d = {}
    xnew = x.copy()
    gwt = re.search(r_num2, r)
    if (re.search(r_sym, r) or '%' in r) and (gwt and gwt.group(2) is None):
        # make sure full match is at the end, ends with - or to or something
        full_match = gwt.group(0)
        r_end = re.compile(full_match + r'\s*(?:to|[\-\<\=]{1,2})\s*$')
        match_end = re.search(r_end, r)
        if match_end:
            unit = ''
            wt = str(gwt.group(1)).strip(' <>=') + '-' + str(cwt)
            wt = wt.replace(' ', '') + unit

            new_name = r.replace(match_end.group(0), '').strip()
            if secret:
                new_name = new_name + ' - secret'

            dtemp = {'cas': x['cas'], 'wt': wt}
            if not (pd.isna(x['ci_color']) or x['ci_color'] == ''):
                dtemp['ci_color'] = x['ci_color']
            d[new_name] = dtemp

            if len(d) > 0:
                dfix = fix_dict(d)
                dnew = chem_format(dfix)[0]

                for key, val in dnew.items():
                    xnew[key] = val

                print('---- ' + str(x.name) + ' ----')
                print(r + ' / ' + str(cwt) + ' ---> ' + new_name + ' / ' +
                      str(xnew['min_wt']) + ' / ' + str(xnew['max_wt']))

    return xnew


def clean_row(x):
    """Clean the row a little bit."""
    xnew = x.copy()

    # clean name
    r = x['name']
    if len(r) > 0:

        sec = False
        if re.search(r'\s*(?:- secret)$', r):
            sec = True
        r = re.sub(r'\s*(?:- secret)$', '', r).strip('*').strip()
        s_list = ['proprietary', 'supplier', 'secret']
        if (r in s_list) or len(r) == 0:
            r = 'trade secret / proprietary / other'

        if re.search(r'^[\W\d\s]+$', r):
            r = ''

        rem_end = ['|', '_', '&', '*']
        for s in rem_end:
            r = r.rstrip(s).strip()

        r = re.sub(r'\s*(?:\d{1,2}[\.]\d{1,}\s?[\%]\s*){2,}\s*',
                   ' ', r).strip()

        rem_seq = ['n/a']
        for s in rem_seq:
            r = r.replace(s, '').strip()
        r = re.sub(r'[\(]\s*[\)]', '', r).strip()
        r = re.sub(r'[\[]\s*[\]]', '', r).strip()

        if sec and len(r) == 0:
            r = 'trade secret / proprietary / other'

        if r != x['name']:
            print('---- ' + str(x.name) + ' ----')
            print(x['name'] + ' ---> ' + r)

            xnew['name'] = r

    # add ci color to name
    if x['ci_color'] != '':
        xnew['name'] = x['name'] + ' (CI ' + x['ci_color'] + ')'

    # make sure max_wt and min_wt are filled out correctly
    if x['cent_wt'] == '':
        if x['max_wt'] != '' and x['min_wt'] == '':
            xnew['min_wt'] = 0
        elif x['max_wt'] == '' and x['min_wt'] != '':
            print('completing max_wt, min_wt is ' + str(x['min_wt']))
            xnew['max_wt'] = 100
        if xnew['max_wt'] != '' and xnew['max_wt'] == xnew['min_wt']:
            xnew['cent_wt'] = xnew['min_wt']
            xnew['max_wt'] = ''
            xnew['min_wt'] = ''

    # add unit type
    if x['min_wt'] != '' or (x['cent_wt'] != '' or x['max_wt'] != ''):
        xnew['unit_type'] = 2

    return xnew


def read_chems():
    """Read list of comptox chemicals."""
    cas2 = re.compile(r'^(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})[\—\–\-\° ]{1,3}' +
                      r'([\d])$', re.IGNORECASE)
    df_names = pd.read_excel('DSSTox_Identifiers_and_CASRN.xlsx')
    ct_chems = df_names[['casrn', 'preferred_name']].copy().drop_duplicates()

    def is_cas(x):
        xnew = x.copy()
        xnew['casrn'] = symbol_cleanup(x['casrn'])
        xnew['preferred_name'] = x['preferred_name']
        if not re.search(cas2, xnew['casrn']):
            xnew['casrn'] = np.nan
        return xnew

    ct_chems = ct_chems.apply(is_cas, axis=1)
    ct_chems = ct_chems.dropna()
    ct_chems = ct_chems.set_index('casrn')
    return ct_chems


def cas_to_name(x):
    """Scrape chem name from internet."""
    time.sleep(random.random()+1)
    r = requests.get('https://chem.nlm.nih.gov/chemidplus/rn/'+x)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        cname = unicodedata.normalize('NFKD', soup.find(id='summary')
                                      .find(class_='lc2-left').h1
                                      .contents[0]).replace('Substance Name: ',
                                                            '')
    except (AttributeError, TypeError):
        params = {'p_p_id': 'disssimplesearch_WAR_disssearchportlet',
                  'p_p_state': 'normal',
                  '_disssimplesearch_WAR_disssearchportlet_javax.portlet' +
                  '.action': 'doSearchAction',
                  }
        payload = {'_disssimplesearch_WAR_disssearchportlet_search' +
                   'Occurred': 'true',
                   '_disssimplesearch_WAR_disssearchportlet_sskeywordKey':
                       x,
                   }
        r = requests.post('https://echa.europa.eu/search-for-chemicals',
                          params=params,
                          data=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            cname = unicodedata.normalize('NFKD',
                                          soup.find(class_='table-data')
                                          .find('a').string).strip()
        except (AttributeError, TypeError):
            cname = ''
    return cname


def get_name(cas, tcomb):
    """Get chem name from cas.

    Search df first, for speed, then web.
    """
    try:
        name = tcomb.loc[cas, 'preferred_name']
    except KeyError:
        name = cas_to_name(cas)
    return name


def match_cas(df, tcomb):
    """Match cas and name."""
    name_only = df.loc[(df['name'] != '') & (df['cas'] == '')]
    name_only = name_only.loc[
        name_only['name'].apply(lambda x:
                                False if x.endswith('secret') else True)]
    name_only['wt'] = name_only[['min_wt', 'cent_wt', 'max_wt']] \
        .replace('', np.nan).fillna(0).sum(axis=1) \
        .apply(lambda x: True if x > 0 else False)
    name_only = name_only[['name', 'wt']].copy()
    name_only['score'] = 0
    name_only = name_only.loc[~name_only['wt']]

    if len(name_only) == 0:
        return df

    cas_only = df.loc[(df['name'] == '') & (df['cas'] != '')].copy()
    # cas_only['wt'] = cas_only[['min_wt', 'cent_wt', 'max_wt']] \
    #     .replace('', np.nan).fillna(0).sum(axis=1) \
    #     .apply(lambda x: True if x > 0 else False)

    to_remove = []
    new_rows = []
    for name, row in cas_only.iterrows():
        newrow = row.copy()
        cname = get_name(row['cas'], tcomb).lower().strip()
        name_only['score'] = name_only['name'] \
            .apply(lambda x: fuzz.ratio(cname, x))
        maxind = name_only['score'].idxmax()
        if name_only.loc[maxind, 'score'] > 85 and maxind not in to_remove:
            newrow['name'] = name_only.loc[maxind, 'name']
            new_rows.append(newrow)
            to_remove.append(maxind)

    new_df = df.copy()
    for i in new_rows:
        new_df.loc[i.name] = i

    new_df = new_df.loc[[i for i in new_df.index if i not in to_remove]]

    return new_df


def has_dups(x):
    """Check if a df has duplicate chemicals."""
    # remove secret things
    x = x.loc[x['name'] != 'trade secret / proprietary / other']
    x = x.loc[x['name'].apply(
        lambda x: False if 'third party formulation' in x else True)]

    # if nothing is duplicated, return true
    if x.loc[x['name'] != '', 'name'].duplicated().sum() == 0 and \
            x.loc[x['cas'] != '', 'cas'].duplicated().sum() == 0:
        return False

    to_remove = []
    gg = x.loc[x['name'] != ''].groupby('name')
    for n, g in gg:
        if len(g) < 2:
            continue
        break
        # same name, same cas; drop
        if g['cas'].duplicated().sum() > 0:
            return True
        # same name, no cas; drop
        if g['cas'].sum().strip() == '':
            return True
        # same name, one cas; ***
        if '' in g['cas'].tolist():
            to_remove += list(g.loc[g['cas'] == ''].index)
        # same name, diff cas; keep

    gg = x.loc[x['cas'] != ''].groupby('cas')
    for n, g in gg:
        if len(g) < 2:
            continue
        # break
        # same cas, no name; drop
        if g['name'].sum().strip() == '':
            return True
        # same cas, one name; ***
        if '' in g['name'].tolist():
            # could keep, but this could be caused by many things
            return True
        # same cas, diff name; keep

    # if has same cas and diff name, keep
    if len(to_remove) > 0:
        return to_remove
    else:
        return False


def combine_names(df, tcomb):
    """Iterate through files."""
    gp = df.groupby('filename')
    keep = []
    for name, group in gp:
        # print(name)
        new_group = match_cas(group, tcomb)
        dup_check = has_dups(new_group)
        if isinstance(dup_check, list):
            new_group = new_group.loc[~new_group.index.isin(dup_check)]
            keep.append(new_group)
        elif not dup_check:
            keep.append(new_group)
        else:
            print('Removed for duplicates: ' + name)
    dfnew = pd.concat(keep)
    return dfnew


def which_naming(x, docs):
    """Return naming method."""
    method = 0
    val = ['-1'] * 3

    # data_document_id
    idtest = re.search(r_docid, x)
    if idtest:
        method += 1
        val[0] = idtest.group(1)

    # actual fname
    act = docs.loc[docs['file'] == x, 'ID']
    if len(act) > 0:
        method += 2
        val[1] = act.values[0]
        if len(act) > 1:
            print('more than one filename found (act): ' + x)

    # original fname
    orig = docs.loc[docs['file name'] == x, 'ID']
    if len(orig) > 0:
        method += 4
        val[2] = orig.values[0]
        if len(orig) > 1:
            print('more than one filename found (orig): ' + x)

    # check val
    if len(pd.unique([i for i in val if i != '-1'])) > 1:
        print('Multiple unique vals for ' + x)

    return method, val


def get_name_type(fname_list, df_docs):
    """Get name type to match with extracted template.

    Returns doc_id list. All files must be consistently named.
    """
    flist = pd.unique(fname_list)
    docs = df_docs[['ID', 'file', 'file name']]
    vals = {}
    check = []

    for i in flist:
        m = which_naming(i, docs)
        check.append(m[0])
        vals[i] = m[1]

    # checking
    counts = pd.Series(check).value_counts()
    real_counts = [sum([counts.loc[j] for j in counts.index
                        if i in pmap[j]]) for i in [0, 1, 2, 4]]
    ind = np.argmax(real_counts)
    if ind == 0:
        print('No matching filenames found.')
        return None
    ind = ind - 1
    # if counts.iloc[0]/4 > counts.iloc[1:].sum():
    #     ind = counts.index[0]
    # else:
    #     print('error determining filename type')
    #     return None

    # get actual val
    val_clean = {key: int(arr[ind].strip()) if arr[ind] != '-1'
                 else np.nan for key, arr in vals.items()}
    if len(pd.unique(list(val_clean.values()))) != len(val_clean):
        print('Duplicate ids, found')
        return None

    id_list = fname_list.apply(val_clean.__getitem__)

    return id_list


if __name__ == '__main__':
    # file locations
    # folder = r'output/dg18'
    # chem_file = r'chemical_data_dg18_zip_2020-03-04_14-31-52.csv'
    # info_file = r'file_info_dg18_zip_2020-03-04_14-31-52.csv'
    # template_file = r'Walmart_MSDS_2_unextracted_documents.csv'

    folder = r'output/dg17'
    chem_file = r'chemical_data_dg17_zip_2020-04-13_17-40-06.csv'
    info_file = r'file_info_dg17_zip_2020-04-13_17-40-06.csv'
    template_file = r'Walmart_MSDS_1_unextracted_documents.csv'
    documents_file = r'walmart_msds_1_documents_20200423.csv'

    # read files
    chem_path = os.path.join(folder, chem_file)
    info_path = os.path.join(folder, info_file)
    template_path = os.path.join(folder, template_file)
    docfile_path = os.path.join(folder, documents_file)

    print('Reading files...')
    df_chems = pd.read_csv(chem_path)
    df_info = pd.read_csv(info_path)
    df_template = pd.read_csv(template_path)
    df_docs = pd.read_csv(docfile_path)

    print('Reading chemical list...')
    tcomb = read_chems()

    # start operations
    df = df_chems.copy()

    # remove split
    print('Starting cleaning...')
    to_remove = df_info.loc[df_info['split'], 'filename']
    df_clean = df.fillna('').loc[~df['filename'].isin(to_remove)]

    # run functions
    df_clean = df_clean.apply(fix_range, axis=1)
    df_clean = df_clean.apply(check_line, axis=1)
    df_clean['unit_type'] = ''
    df_clean = df_clean.apply(clean_row, axis=1)
    df_clean = combine_names(df_clean, tcomb)  # could add multiprocessing

    # join to table
    print('Creating outputs...')
    df_clean = df_clean.fillna('')
    # df_clean['data_document_id'] = df_clean['filename'] \
    #     .apply(lambda x:
    #            int(re.sub(r_docid, r'\g<1>', x)))
    id_col = get_name_type(df_clean['filename'], df_docs)
    if id_col is None:
        raise Exception('Error when getting filenames')
    df_clean['data_document_id'] = id_col
    df_clean = df_clean.rename(columns={'cas': 'raw_cas',
                                        'name': 'raw_chem_name',
                                        'min_wt': 'raw_min_comp',
                                        'cent_wt': 'raw_central_comp',
                                        'max_wt': 'raw_max_comp',
                                        }) \
        .drop(columns=['row', 'ci_color', 'filename'])
    cols = list(df_template.columns.copy())
    df_all = df_template.drop(columns=[i for i in cols
                                       if i in df_clean.columns
                                       and i != 'data_document_id']) \
        .merge(right=df_clean, how='inner', on='data_document_id',
               validate='1:m', sort=True)
    df_all = df_all[cols]

    # output other info table
    df_info_new = df_info.copy().rename(columns={'split': 'multiple_files',
                                                 'debug': 'msds',
                                                 'filename':
                                                     'data_document_id',
                                                 'num_found': 'chems_found',
                                                 })
    df_info_new['data_document_id'] = df_info_new['data_document_id'] \
        .apply(lambda x:
               int(re.sub(r'(?:document_)(\d{4,})(?:\.pdf)', r'\g<1>', x)))
    df_info_new['msds'] = df_info_new['msds'].apply(lambda x:
                                                    True if x != 'label'
                                                    else False)

    # save files
    df_all.to_csv(os.path.join(folder, 'formatted_' + chem_file), index=False)
    df_info_new.to_csv(os.path.join(folder, 'formatted_' + info_file),
                       index=False)

    # split file before output
    print('Splitting files...')
    split_path = os.path.join(folder, 'split')
    if not os.path.isdir(split_path):
        os.mkdir(split_path)

    nsplit = 15000  # number per split

    gp = df_all.groupby('data_document_id')

    ct = 0
    all_split = []
    current = []
    for name, group in gp:
        ct += len(group)
        current.append(group)
        if ct > nsplit:
            all_split.append(current)
            ct = 0
            current = []
    if len(current) > 0:
        all_split.append(current)

    store = 0
    for n, i in enumerate(all_split):
        df_split = pd.concat(i)
        store += len(df_split)
        df_split.to_csv(os.path.join(
            split_path, 'split' + str(n) + '_' + chem_file), index=False)

    print('Done!')
