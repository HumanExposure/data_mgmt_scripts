# -*- coding: utf-8 -*-
"""Functions to help with various formatting issues.

Created on Thu Oct 31 18:03:43 2019

@author: SBURNS
"""

import re
from pymysql import escape_string
import pandas as pd

r_words = re.compile(r'[^\w\s\d\-\_\=\+\)\(\*\&\^\%\$\#\@\!\~\}\]\{\[\'\"\;' +
                     r'\:\/\?\.\>\,\|\<\\]', re.I)


def symbol_cleanup(t):
    """Replace strange alternative symbols with normal counterparts.

    Args:
        t (str): String to cleanup.

    Returns:
        t (str): String with symbols replaces.

    """
    t = re.sub(r'[\＜\﹤\<]', '<', t)
    t = re.sub(r'\b(?:less than)\b', '<', t)
    t = re.sub(r'[\﹥\＞\>]', '>', t)
    t = re.sub(r'[\＝\﹦\=\゠]', '=', t)
    t = re.sub(r'[\≥\≧]', '>=', t)
    t = re.sub(r'[\≤\≦]', '<=', t)

    t = re.sub(r'[\,\，\﹐]', ',', t)
    t = re.sub(r'[\.\．\﹒]', '.', t)
    t = re.sub(r'[\%\﹪\％]', '%', t)
    t = re.sub(r'[\*\⁎\∗\﹡\＊]', '*', t)
    t = re.sub(r'[\–\—\‒\⁓\〜\﹘\-\‐\‑\﹣\－\—\–\-\～\~]', '-', t)

    return t


def chem_format(val):
    """Format the chemical names and weights for output.

    This function cleans up the dicts and list from other functions and
    standardizes them to be combined for output.

    Args:
        val (list): List of dicts or chemical names (strings).

    Returns:
        val_new (list): List of corrected dicts or chemical names.

    """
    def str_format(v):
        """Format the input string."""
        if v.startswith('CASRN='):
            return ''
        v_new = v.lstrip('-., ').rstrip('( ').replace('  ', ' ').strip(' \\/|')
        v_new = re.sub(r'(?:^[\(\)]|[\(\)]$)', '', v_new).strip() \
            if ('(' in v_new and ')' not in v_new) or \
            (')' in v_new and '(' not in v_new) \
            else v_new
        return escape_string(re.sub(r_words, '', symbol_cleanup(v_new)))

    def wt_format(v):
        """Split the weight apart into 3 sections."""
        wt_new = {'min_wt': '', 'cent_wt': '', 'max_wt': ''}
        if len(v) == 0:
            return wt_new
        v2 = v.replace(',', '.').split('-')
        if len(v2) == 1:
            if '<' in v2[0]:
                wt_new['max_wt'] = str(float(v2[0].strip('<>= ')))
            elif '>' in v2[0]:
                wt_new['min_wt'] = str(float(v2[0].strip('<>= ')))
            else:
                wt_new['cent_wt'] = str(float(v2[0].strip('= ')))
        elif len(v2) == 2:
            wt_t = [float(i.strip('<>= ')) for i in v2]
            wt_new['max_wt'] = str(max(wt_t))
            wt_new['min_wt'] = str(min(wt_t))
        else:
            print('WT Error' + ' - ' + v)
        return wt_new

    # loop through list items, call earlier functions and change dict format
    val_new = []
    for i in val:
        if type(i) == str:
            val_new.append(str_format(i))
        elif type(i) == dict:
            key = list(i.keys())[0]  # should only be one key
            tval = i[key]
            dnew = {**{'name': str_format(key), 'cas': tval['cas']},
                    **wt_format(tval['wt']), **{'ci_color': ''}}
            if 'ci_color' in tval:
                dnew['ci_color'] = ', '.join(tval['ci_color'])
                if dnew['name'] == '':
                    dnew['name'] = 'Ci ' + dnew['ci_color']
            val_new.append(dnew)
        else:
            print('Type error: ' + str(type(i)) + ' - ' + str(val))

    return val_new


def fix_dict(d):
    """Fix the dict of chemical names.

    Sometimes, the search functions product 2 dicts when really only 1 should
    exist. This function combines them.

    Args:
        d (dict): Dict of chemical info.

    Returns:
        list: List of corrected dicts.

    """
    def dict_for(d, check=True):
        """Combine dicts that do not contradict."""
        ct_cas2 = []
        ct_wt2 = []
        ct_color = 0
        newd = {'cas': '', 'wt': ''}
        nm = ''
        for key, val in d.items():
            nm += key + ' / '
            if val['cas'] != '':
                newd['cas'] = val['cas']
                ct_cas2.append(key)
            if val['wt'] != '':
                newd['wt'] = val['wt']
                ct_wt2.append(key)
                if 'ci_color' in val:
                    newd['ci_color'] = val['ci_color']
                    ct_color += 1
        if ct_color > 1:
            print('Too many colors')  # should never happen
        nm = nm.strip(' /')
        if ct_cas2 != ct_wt2 and check:
            print('Dict error:')
            print(d)
            return [{i: d[i]} for i in d.keys()]
        else:
            return [{nm: newd}]

    # see if dict needs to be fixed
    if len(d) < 2:
        return [d]
    ct_cas = 0
    ct_wt = 0
    for key, val in d.items():
        if val['cas'] != '':
            ct_cas += 1
        if val['wt'] != '':
            ct_wt += 1

    # check if it can be fixed
    if ct_cas < 2 and ct_wt < 2:
        return dict_for(d)
    else:
        dd1 = [i['cas'] for i in d.values() if len(i['cas']) > 0]
        dd2 = [i['wt'] for i in d.values() if len(i['wt']) > 0]
        if len(list(pd.unique(dd1))) <= 1 and len(list(pd.unique(dd2))) <= 1:
            return dict_for(d, check=False)
        else:
            return [{i: d[i]} for i in d.keys()]
