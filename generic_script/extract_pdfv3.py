# -*- coding: utf-8 -*-
"""Script for procsssing MSDS and produt labels.

Created on Fri Oct 18 11:34:22 2019

@author: SBURNS
"""

import os
import re
import time
import json
from sqlalchemy import create_engine
from pymysql import escape_string
import numpy as np
import pandas as pd
from tika import parser
from fuzzywuzzy import fuzz  # used to use this more but was inefficient
# from fuzzywuzzy import process
# NEEDS MANUAL FIX https://github.com/seatgeek/fuzzywuzzy/pull/243/files
# I also added the autojunk parameter
# https://github.com/seatgeek/fuzzywuzzy/issues/224

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

# use these to change OCR behavior
do_OCR = True  # requires tessaract
# do OCR on all files or just those with no text
# required to get scans bundled with text
all_OCR = False

# change the folder names here
folder = os.path.join(os.getcwd(), 'pdf')
pdfs = os.listdir(folder)
out_folder = os.path.join(os.getcwd(), 'output')

# regex patterns
s3 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d]' +
                r'(?:[23]|(?:[i1]{3}|ii))\W{0,8}(?![ ]?\d)[\w\/\& ]*?' +
                r'(?:composition|(?:components|ingredients))', re.IGNORECASE)
s4 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d](?:4|iv)' +
                r'\W{0,8}(?![ ]?\d)[\w\/\& ]*?(?:(?:first.?aid)|(?:fire' +
                r'[a-z ]{0,7}explosion))', re.IGNORECASE)
sds = re.compile(r'(?:s\s?d\s?s|d\s?a\s?t\s?a\s{0,3}s\s?h\s?e\s?e\s?t)',
                 re.IGNORECASE)
sds2 = re.compile(r'(?:first.?aid|composition)', re.IGNORECASE)
ecno = re.compile(r'\s?(\d{3})[\—\–\-\° ]{1,3}(\d{3})[\—\–\-\° ]{1,3}' +
                  r'([\d])\s?', re.IGNORECASE)
cas = re.compile(r'(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})[\—\–\-\° ]{1,3}([\d])',
                 re.IGNORECASE)
cas1 = re.compile(r'[^\d](?!0\d[\—\–\-\° ]{1,3}[0-3]\d[\—\–\-\° ]{1,3}' +
                  r'(?:[01]\d|20[01]\d))(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})' +
                  r'[\—\–\-\° ]{1,3}([\d])(?!\d{2,})', re.IGNORECASE)
cas12 = re.compile(r'[^\d](?!0\d[\—\–\-\° ]{1,3}[0-3]\d[\—\–\-\° ]{1,3}' +
                   r'(?:[01]\d|20[01]\d))(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})' +
                   r'[\—\–\-\° ]{1,3}[0]([\d])(?!\d{2,})', re.IGNORECASE)
cas2 = re.compile(r'^(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})[\—\–\-\° ]{1,3}([\d])$',
                  re.IGNORECASE)
fa = re.compile(r'(?:(?:first.?aid)|(?:fire[a-z ]{0,7}explosion))',
                re.IGNORECASE)

# these are needed to sort out some exceptions
s3_2 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d](?:[2]|' +
                  r'(?:ii))\W{0,8}(?![ ]?\d)[\w\/\& ]*?(?:composition|' +
                  r'(?:components|ingredients))', re.IGNORECASE)
s3_3 = re.compile(r'^[\W]{0,8}(?:sectio|chapte)?[rn]?\W{0,2}[^\d](?:[3]|' +
                  r'(?:[i1]{3}))\W{0,8}(?![ ]?\d)[\w\/\& ]*?(?:composition|' +
                  r'(?:components|ingredients))', re.IGNORECASE)

# look for wt percent
r_wt = re.compile(r'(?:(?<=\+\+\+)\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}\s{0,2}' +
                  r'|\b)\d{1,3}(?:[\.\,]\d{1,6})?)[\s\%\*]{0,2}(?:\s{0,4}' +
                  r'[\-]\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})?' +
                  r'\d{1,3}(?:[\,\.]\d{1,6})?)\b)?[\%\*]{0,2}(?![^\s])\s*?|' +
                  r'\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}' +
                  r'\s?|\b)\d{1,3}(?:[\.\,]\d{1,6})?)[\s\%\*]{0,2}' +
                  r'(?:\s{0,4}[\-]\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})' +
                  r'?\d{1,3}(?:[\,\.]' +
                  r'\d{1,6})?)\b)?[\%\*]{0,2}(?![^\s])\s+?(?=\+\+\+))',
                  re.IGNORECASE)

r_wt_pig = re.compile(r'(?:(?<=\+\+\+)\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}' +
                      r'\s{0,2}|\b)\d{1,3}(?:[\.\,]\d{1,6}))[\s\%\*]{0,2}' +
                      r'(?:\s{0,4}[\-]\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})?' +
                      r'\d{1,3}(?:[\,\.]\d{1,6}))\b)?[\%\*]{0,2}(?![^\s])' +
                      r'\s*?|\s+?(?<![^\s])((?:[\<\>\=\≥\≤' +
                      r']{1,2}\s?|\b)\d{1,3}(?:[\.\,]\d{1,6}))[\s' +
                      r'\%\*]{0,2}(?:\s{0,4}[\-]\s{0,4}((?:[\<\>\=\≥\≤]' +
                      r'{1,2}\s{0,2})?\d{1,3}(?:[\,\.]' +
                      r'\d{1,6}))\b)?[\%\*]{0,2}(?![^\s])\s+?(?=\+\+\+))',
                      re.IGNORECASE)

r_wt_pig2 = re.compile(r'(?:(?<=\+\+\+)\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}\s' +
                       r'{0,2}|\b)\d{1,3}(?:[\.\,]\d{1,6})?)[\s\%\*]{0,2}(?:' +
                       r'\s{0,4}[\-]\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})?' +
                       r'\d{1,3}(?:[\,\.]\d{1,6})?)\b)[\%\*]{0,2}(?![^\s])\s' +
                       r'*?|\s+?(?<![^\s])((?:[\<\>\=\≥\≤]{1,2}' +
                       r'\s?|\b)\d{1,3}(?:[\.\,]\d{1,6})?)[\s\%\*]{0,2}' +
                       r'(?:\s{0,4}[\-]\s{0,4}((?:[\<\>\=\≥\≤]{1,2}\s{0,2})' +
                       r'?\d{1,3}(?:[\,\.]' +
                       r'\d{1,6})?)\b)[\%\*]{0,2}(?![^\s])\s+?(?=\+\+\+))',
                       re.IGNORECASE)

# clean up name
cl_old = re.compile(r'\b[\W]*?(?:cas)?[\W]*(?:no|number)[\W]*$', re.IGNORECASE)
cl = re.compile(r'[\W]*\b(?:cas)?[\W]*(?:no|number)[\W]*$', re.IGNORECASE)
cl2 = re.compile(r'[\W]*\b(?:cas)[\W]*(?:no|number)?[\W]*$', re.IGNORECASE)
re_wtnum = re.compile(r'^\W{0,2}(\d{1,3}(?:[\.]\d{1,5})?)(?:[\-]?\W{0,2}' +
                      r'(\d{1,3}(?:[\.]\d{1,5})?))?$', re.I)
r_ci = re.compile(r'\s?[\(]?(?:ci)\s?((?:\d{5}(?:\,\s)?)+)[\)]?\s?', re.I)
r_sym = re.compile(r'\d(?:[\.\,]|\s?[\-]\s?)\d', re.I)

# regex for the label search
r_ing = re.compile(r'^(?:(?:other\s)?ingredients)\s?[\:]', re.I)
r_per = re.compile(r'(?<!\s)[\.]$', re.I)
r_con = re.compile(r'^(?:contains|allergen[s]?)\s?[\:]?\s', re.I)
r_use = re.compile(r'^(?:directions|suggested use)\s?[\:]?\s', re.I)
r_se = re.compile(r'[\(]\s?(?:as\s)([^\)]+?)(?:[\)]|(?:\d[\,]?\d{0,3}\s{0,2}' +
                  r'(?:m[ce]?[g]?|g)\b|\d{1,2}[\s]?[\%])\s)', re.I)
re_cont = re.compile(r'(?:contain[s]?(?:ing)?|(?:warning|information))\s?' +
                     r'[:][^\.]+', re.I)
re_cont2 = re.compile(r'(?:may contain|(?:processes|(?:equipment|' +
                      r'manufactured)))[^\.]+', re.I)
re_cont3 = re.compile(r'[\.](?:[\s\d]*(?:contains|allergen[s]?)[\:]?' +
                      r'[\s\w\(\)\,]+)[\.]?\s*?[\,]?\s*?$',
                      re.I)
re_cont4 = re.compile(r'\b(?:contain[s]?)\b', re.I)
re_2per = re.compile(r'[\.\;]?(?:\scontains)?' +
                     r'(?: \d(?:\%|percent) or less of| ' +
                     r'(?:less than |[\＜\﹤\<]\s?)\d(?:\%|percent) of)' +
                     r'(?: the following)?[:]?',
                     re.I)
re_free = re.compile(r'(?<![\-])\b(?:free)\b', re.I)
r_words = re.compile(r'[^\w\s\d\-\_\=\+\)\(\*\&\^\%\$\#\@\!\~\}\]\{\[\'\"\;' +
                     r'\:\/\?\.\>\,\|\<\\]', re.I)

# lists for label serching
allergen = ['milk', 'egg', 'shellfish', 'peanut', 'wheat', 'soy', 'fish',
            'nut', 'gluten', 'artificial', 'color', 'dairy']
drug_filt = ['taking', 'thinning', 'drug', 'doctor', 'take', 'symptoms',
             'persist', 'perscription', 'inhibitor', 'cure',
             'treat']
minerals = ['iron', 'calcium', 'phosphorus', 'magnesium', 'water', 'glass',
            'potassium', 'sodium', 'cholesterol', 'fiber', 'milk', 'zinc',
            'protein', 'oxide', 'citrate', 'manganese', 'molybdenum',
            'iodine', 'gluten', 'chromium', 'selenium', 'chocolate',
            'chemical', 'soy', 'platinum', 'resin', 'alcohol', 'minerals',
            'serotonin', 'juice', 'concentrate', 'acid', 'acids',
            'fatty acids', 'accelerator']  # filters exact match
minerals2 = ['vitamin', 'ingredient', 'carbohydrate', 'sugar',
             'preservative', 'contain', 'other', 'facts', 'flavor',
             'powder', 'made']  # anything containing one of these removed
terms = ['total', 'natural', 'based', 'extract', 'organic', 'root', 'con',
         'film', 'adhesive', 'varnish', 'vehicle', 'purpose', 'date', 'leaf',
         'inc', 'palm', 'key', 'unique', 'pure', 'antioxidant', 'moisture',
         'pet', 'none', 'special', 'liner', 'cardboard', 'sheet', 'filtered',
         'raw', 'allergens', 'organic', 'plant derived', 'balance', 'source',
         'vinyl', 'tox', 'alpha', 'solvent', 'scent', 'dust', 'all natural',
         'electrolyte', 'certified organic', 'light']
drug_no = ['vehicle']
exclude = ['secret', 'proprietary', 'n/a', 'cbi', 'trade', 'not available']
colorlist = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple',
             'violet', 'pigment']
amino = ['amino acid', 'alanine', 'arginine', 'asparagine', 'aspartic acid',
         'cysteine', 'glutamine', 'glutamic acid', 'glycine', 'histidine',
         'isoleucine', 'leucine', 'lysine', 'methionine', 'phenylalanine',
         'proline', 'serine', 'threonine', 'tryptophan', 'tyrosine',
         'valine', 'amino acids']
amino_all = [qq for q in [['l-'+j, 'd-'+j, j] for j in amino] for qq in q]


# Functions!
def read_df():
    """Produce a list of chemical names.

    This function pulls data from factotum and from an Excel file to create a
    list of unique chemical names.

    Returns:
        tcomb (list): A list containing uique chemical names.

    """
    # search list from comptox
    df_names = pd.read_excel('DSSTox_Identifiers_and_CASRN.xlsx')
    df = df_names[['casrn', 'preferred_name']].copy()
    # df['casrn'].nunique() == len(df)
    df = df.set_index('casrn').dropna().copy()
    df['sort'] = df['preferred_name'].apply(len)
    df1 = df.sort_values(by='sort')[['preferred_name']].copy()

    # get chemicals from factotum
    with open('mysql.json', 'r') as f:
        cfg = json.load(f)['mysql']
    conn = create_engine(f'mysql+pymysql://{cfg["username"]}:' +
                         f'{cfg["password"]}@{cfg["server"]}:' +
                         f'{cfg["port"]}/{cfg["database"]}?charset=utf8',
                         convert_unicode=True, echo=False).connect()
    sql = 'SELECT DISTINCT raw_chem_name from dashboard_rawchem;'
    df = pd.read_sql(sql, conn)
    df = df.rename(columns={'raw_chem_name': 'preferred_name'}).dropna()
    conn.close()

    cq = pd.concat([df1, df]).apply(lambda x: x.str.lower().str.strip())
    cc = cq['preferred_name'].drop_duplicates()

    # format and compile the list of chemicals
    df = cc
    df_u = pd.unique(df.str.strip().str.lower())
    tcomb = [i for i in df_u if not re.search(cas2, i)]

    return tcomb


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


def fuzzy_match(row, sds=True):
    """Find chemical names in a string.

    Using the list of chemicals from before, search the input string for
    matches. There are filters in place to look for bad matches, since the
    input list has some errors.

    Args:
        row (str): String in which to search for matches.
        sds (bool): Whether the source file is an SDS. Defaults to True.

    Returns:
        chems (list): A list of chemicals found.

    """
    chems = []
    row = row.lower()
    # only look for rows if it has a cas (for accuracy and efficiency)
    if not re.search(cas1, ' ' + row) and sds:
        return chems
    row = re.sub(cas, '', row).strip()
    if len(row) < 2:
        return chems

    # search for chemicals from list
    for chem in tcomb:
        if chem in row:
            # match full word
            r = re.compile(r'\b(?:' + re.escape(chem) + r')\b', re.I)
            if re.search(r, row):
                chems.append(chem)

    # filter to a certain length and remove terms
    chems = [i for i in chems if len(i) > 2 and not re.search(re_cont4, i) and
             i not in terms]
    excl = exclude + ['less than']

    # remove overlaping chemicals (i.e. sodium and sodium chloride overlap)
    chems = list(pd.unique(chems))
    if len(chems) > 1:
        newlist = []
        for i in chems:
            inside = False
            for j in chems:
                if i in j and i != j:
                    inside = True
                    break
            if not inside and len(i) > 2:
                oo = [z for z in excl if z in i or i in z]
                if len(oo) == 0:
                    newlist.append(i)
        if len(newlist) > 1 and sds:
            tm = [k.strip() for k in row.split(', ')]
            bd = [q for q in tm if sum([1 for c in newlist if c in q]) > 1]
            newlist2 = [c for c in newlist if sum([1 for q in tm if c in q])
                        > sum([1 for b in bd if c in b])]
            newlist = newlist2 if len(newlist2) > 0 else newlist
        if len(newlist) > 1 and sds:
            row2 = row.split('(')[0].strip()
            newlist3 = [i for i in newlist if i.split('(')[0].strip() in row2]
            newlist = newlist3 if len(newlist3) > 0 else newlist
        chems = newlist
    return chems


def match2(r, chems, val):
    """Find chemical names and weights in a string.

    This function searches a string for chemical names and weights. It relies
    on many of the regex statements above. Much of the code here is designed to
    deal with strange scenarios.

    Args:
        r (str): String to search.
        chems (list): List of chemicals found.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).

    Returns:
        d (dict): Dictionary with chemical info.

    """
    d = {}
    for i in chems:
        d[i] = {'cas': '', 'wt': ''}

    # get index of row
    ind = val['raw'].index(r)
    move = False
    rem = r
    ts = 0
    if ind in val['indCAS']:
        move = True
    else:
        for e in exclude:
            rem = re.sub(re.compile(r'\b(?:' + re.escape(e) + r')\b',
                                    re.I), '+++', rem)
        if '+++' in rem:
            ts = 1
            move = True

    unit = ''
    if move:
        # get cas
        tcas = ''
        # if len(chems) > 0 and ind in val['indCAS']:
        if ind in val['indCAS']:
            tcas = val['secCAS'][val['indCAS'].index(ind)]

        # get weights
        rem = re.sub(cas, '+++', rem)
        rem2 = re.sub(ecno, ' ', rem)
        ci_color = re.findall(r_ci, rem2)
        rem2 = re.sub(r_ci, ' ', rem2)
        rem2 = symbol_cleanup(rem2)
        gwt = re.search(r_wt, rem2)

        # check if there's a color/pigment, and correct if there is
        colorct = False
        for icol in colorlist:
            if re.search(re.compile(r'\b(?:' + re.escape(icol) + r')\b',
                                    re.I), rem2.lower()):
                colorct = True
                break
        # colorct = sum([1 for i in colorlist if
        #                re.search(re.compile(r'\b(?:' + re.escape(i) + r')\b',
        #                                     re.I), rem2.lower())])
        if colorct and (gwt and r_sym):
            gwt2 = re.search(r_wt_pig, rem2)
            if gwt2:
                gwt = gwt2
            else:
                gwt3 = re.search(r_wt_pig2, rem2)
                gwt = gwt3 if gwt3 else gwt
            print(rem2)

        # create weights
        wt = ''
        if gwt:
            gp = [i for i in gwt.groups() if i is not None]
            if len(gp) == 1:
                wt = str(gp[0])
            elif len(gp) == 2:
                wt = str(gp[0]) + '-' + str(gp[1])
            elif len(gp) > 2:
                print('WT Error: ' + str(gp))
            wt = wt.replace(' ', '') + unit

        # get name from beginning, use regex to remove strange patterns
        if gwt:
            nm = re.sub(gwt.group(0),
                        '+++', rem2).split('+++', 1)[0].strip().lower()
            nm2 = re.sub(cl, '', nm).strip(' .')
            nm2 = re.sub(cl2, '', nm2).strip(' .')
            nm2 = re.sub(r'\s+', ' ', nm2)
            nm2_old = re.sub(cl_old, '', nm).strip(' .')
            if nm2 != nm2_old:
                print(nm2_old + ' ---> ' + nm2)
            nm2 = nm2 if re.search(r'\w', nm2) else ''
            if nm2 == '' and tcas != '':
                nm2 = 'CASRN='+tcas
            for i in chems:
                ntmp = re.sub(r_ci, ' ', i).strip().split('(ci')[0]
                if fuzz.ratio(nm2, ntmp) > 95 or ntmp in nm2:
                    del d[i]
            nm2 = nm2.strip() + ' - secret' if ts == 1 else nm2
            d[nm2] = {'cas': tcas, 'wt': wt}
            if ci_color:
                d[nm2]['ci_color'] = [j.strip() for i in ci_color
                                      for j in i.split(',')
                                      if len(j.strip()) > 0]
                print(d)

            # sometimes there are 2 dicts when there should be 1
            if len(d) == 2:
                ct = 0
                for kk, vv in d.items():
                    if 'CASRN=' in kk and (vv['cas'] != '' and vv['wt'] != ''):
                        ct += 1
                        cass = vv['cas']
                        wtt = vv['wt']
                    elif ('CASRN=' not in kk and kk != '') and \
                            (vv['cas'] == '' and vv['wt'] == ''):
                        ct += 10
                        nmm = kk
                if ct == 11:
                    d = {}
                    d[nmm] = {'cas': cass, 'wt': wtt}
                    if ci_color:
                        d[nmm]['ci_color'] = [j.strip() for i in ci_color
                                              for j in i.split(',')
                                              if len(j.strip()) > 0]
                        print(d)

            # fixes regex interpreting a color (e.g. red 5) as a weight
            for k, v in d.copy().items():
                wsch = re.search(re_wtnum, v['wt'])
                if wsch:
                    wval1 = v['wt']
                    wval = [i for i in list(wsch.groups()) if i is not None]
                    if len(wval) == 1:
                        if ('<' not in wval1 and '>' not in wval1) and \
                                ('.' not in wval1 and float(wval[0]) >= 1):
                            for c in colorlist:
                                if c in k:
                                    test1 = rem2.split('+++')
                                    if len(test1) < 2:
                                        continue
                                    q = gwt.group(0)
                                    score = [0] * len(test1)
                                    for ns, si in enumerate(test1):
                                        if k in si.lower():
                                            score[ns] += 1
                                        if q in si.lower():
                                            score[ns] += 1
                                    if max(score) > 1:
                                        rem3 = rem2.replace(q, ' ')
                                        gwt5 = re.search(r_wt, rem3)
                                        wt = ''
                                        if gwt5:
                                            gp = [i for i in gwt5.groups()
                                                  if i is not None]
                                            if len(gp) == 1:
                                                wt = str(gp[0])
                                            elif len(gp) == 2:
                                                wt = str(gp[0]) + '-' + \
                                                     str(gp[1])
                                            elif len(gp) > 2:
                                                print('WT Error: ' + str(gp))
                                            wt = wt.replace(' ', '') + unit
                                        tmp = v.copy()
                                        tmp['wt'] = wt
                                        d[k.strip()+' '+wval1] = tmp
                                        print('--fix--')
                                        print(rem2)
                                        print(d)
                                        print('-------')
                                        del d[k]
                                        break
    return d


def fun_chemicals(key, val):  # to_sec
    """Extract CAS numbers.

    This function extracts CAS numbers from each file. The locations of the CAS
    numbers were found previously. This function looks in Section 3.

    Args:
        key (str): Filename.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).

    Returns:
        doc (list): List of lists of CAS numbers.

    """
    # print('----- '+key+' -----')
    thisCAS = val['indCAS']
    doc = []
    if len(thisCAS) > 0:
        filt_all = val['filt']
        for n, filt in enumerate(filt_all):
            cas_sec = [val['secCAS'][nn] for nn, i in enumerate(thisCAS)
                       if i > val['ind3'][n] and i < val['ind4'][n]]
            doc.append(cas_sec)
    else:
        doc.append([])
        print('No hazards: '+key)
    return doc


def fun_chemicals_add(key, val, chems):  # to_sec
    """Extract CAS numbers.

    This function extracts CAS numbers from each file. The locations of the CAS
    numbers were found previously. This function looks in areas around
    Section 3.

    Args:
        key (str): Filename.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).
        chems (list): A list of chemicals found in Section 3.

    Returns:
        cnames (list): List of CAS numbers.

    """
    # print('----- '+key+' -----')
    thisCAS = val['indCAS']
    cnames = []
    if len(thisCAS) > 0:
        found = [i for j in chems for i in j]
        indlist = val['ind3']+val['ind4']
        # find names of CAS nos near sections that werent found
        cnames = [c  # df.loc[c] if c in df.index else cas_to_name(c)
                  for n, c in enumerate(val['secCAS'])
                  if c not in found and len([i for i in indlist
                                             if (i-thisCAS[n]) > -25 and
                                             (i-thisCAS[n]) < 50]) > 0]
    return cnames


def fun_chemicals_old(key, val):  # to_old
    """Extract CAS numbers.

    This function extracts CAS numbers from each file. The locations of the CAS
    numbers were found previously. This function looks is for files where
    Section 3 wasn't found.

    Args:
        key (str): Filename.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).

    Returns:
        chems_out (list): List of CAS numbers.

    """
    # print('----- '+key+' -----')
    thisCAS = val['indCAS']
    cnames = []
    cnames2 = []
    if len(thisCAS) > 0:
        indlist = val['ind3']+val['ind4']
        if len(indlist) > 0:
            cnames = [c  # df.loc[c] if c in df.index else cas_to_name(c)
                      for n, c in enumerate(val['secCAS'])
                      if len([i for i in indlist
                              if (i-thisCAS[n]) > -25 and
                              (i-thisCAS[n]) < 50]) > 0]
        arr = np.array([i for i, r in enumerate(val['raw'])
                        if re.search(fa, r)])
        if len(arr) > 0:
            cnames2 = [c  # df.loc[c] if c in df.index else cas_to_name(c)
                       for n, c in enumerate(val['secCAS'])
                       if (((arr-thisCAS[n]) > -25) &
                           ((arr-thisCAS[n]) < 60)).sum() > 0]

    # (((arr-thisCAS[n])>-20)&((arr-thisCAS[n])<30))
    chems_out = list(pd.unique(cnames+cnames2))

    return chems_out


def fun_sec_search(key, val):  # to_sec
    """Search for chemical names.

    This function searches the Section 3 for chemical names. It calls
    fuzzy_match and match2 for each row.

    Args:
        key (str): Filename.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).

    Returns:
        newchems (list): List of lists of chemical names.

    """
    # search between sections only
    ss = time.time()
    newchems = []
    for filt in val['filt']:
        keep = []
        for r in filt:
            chems = fuzzy_match(r)  # outputs list of chem names in each row
            dd = match2(r, chems, val)  # processes line
            if len(dd) > 0 and len(list(dd.keys())[0]) > 2:
                keep.append(dd)
        newchems.append(keep)
    print(key+': '+str(round(time.time()-ss)))
    return newchems


def fun_wide_search(key, val):  # used in old_serch and sec_search_wide
    """Search for chemical names.

    This function searches the document for chemical names. It calls
    fuzzy_match and match2 for each row. Instead of searching Section 3, it
    looks in the surrounding areas.

    Args:
        key (str): Filename.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).

    Returns:
        keep (list): List of chemical names.

    """
    # use same scheme as with before (search around ind, if not there,
    # search around first aid)
    raw = val['raw']
    indlist = val['ind3']+val['ind4']
    cnames = []
    cnames2 = []
    if len(indlist) > 0:
        cnames = [c for n, c in enumerate(raw)
                  if len([i for i in indlist if (i-n) > -25 and
                          (i-n) < 50]) > 0]
    arr = np.array([i for i, r in enumerate(raw) if re.search(fa, r)])
    if len(arr) > 0:
        cnames2 = [c for n, c in enumerate(raw)
                   if (((arr-n) > -10) & ((arr-n) < 40)).sum() > 0]
    filt = list(pd.unique(cnames+cnames2))

    # call functions
    keep = []
    for r in filt:
        chems = fuzzy_match(r)
        dd = match2(r, chems, val)

        if len(dd) > 0 and len(list(dd.keys())[0]) > 2:
            keep.append(dd)
    return keep


# search labels
def fun_label_search(key, val):
    """Search for chemical names in labels.

    This function looks at product labels for chemical names. It looks at both
    ingredients lists and searches with the list created form read_df.

    Args:
        key (str): Filename.
        val (dict): Dict containing info from searching the file (see pdf_sort
                    function).

    Returns:
        label_all (list): List of chemical names.

    """
    body = [i.strip().lower() for i in val['raw'].splitlines()
            if len(i.strip()) > 2]

    keywords = ['supplement facts', 'percent daily value', 'serving size',
                'directions', 'suggested use', 'ingredient']
    if 'drug facts' in ''.join(body):
        keywords = ['active ingredient', 'drug facts']

    def token_thing(ilist, n, ing):
        """Filter sentances based on stopwords and other key words."""
        filt_token = []
        for nn, qq in enumerate([word_tokenize(i) for i in ilist]):
            head = [i for i in keywords + ['nutrition facts', 'children']
                    if i in ilist[nn]]
            if len(head) > 0 and ing:
                continue
            newlist = [w for w in qq if len(w) > 1 or w in [',', '.']]
            newlist2 = [w for w in newlist if w not in stop_words]
            if len(newlist) - len(newlist2) < n and \
                    len([i for i in drug_filt if i in newlist2]) == 0:
                filt_token.append(ilist[nn])
        return [i for i in filt_token if i not in terms] if ing else filt_token

    # row index for ingredients label
    ing = [n for n, r in enumerate(body) if re.search(r_ing, r)]
    ing2 = []
    for i in ing:
        istore = -1
        for nn, rr in enumerate(body[i:]):
            n2 = nn+i
            if re.search(r_per, rr):
                istore = n2+1
                break
            elif (re.search(r_con, rr) and not re.search(re_2per, rr)) \
                    or re.search(r_use, rr):
                istore = n2
                break
        ing2.append(istore)

    # get rows between row indices
    filt_ing = [body[i:ing2[n]] for n, i in enumerate(ing) if ing2[n] != -1
                and ing2[n] - i <= 45]
    for i in range(len(filt_ing)):
        filt_ing[i][-1] = filt_ing[i][-1].rstrip() + ','
    filt1 = [j for i in filt_ing for j in i]

    # t1 to t3 are all filtering and cleaning the rows
    t1 = [r.split('ingredients', 1) for r in filt1]
    t2 = []
    ct = 0
    for r in t1:
        if len(r) == 1 or ct >= len(filt_ing):
            t2.append(r[0])
        elif ct < len(filt_ing):
            t2.append(r[1].strip(' :'))
            ct += 1
    t2 = [i for i in t2 if len(i) > 0]
    # t2 = [r[0] if len(r) == 1 else r[1].strip(' :') for r in t1]

    # remove allergens and 'free' ingredients
    free = []
    allerg = []
    t22 = t2
    for i in list(range(len(t2)))[::-1]:
        if re.search(re_free, t2[i]):
            free.append(i)
        for j in allergen:
            if j in t2[i]:
                allerg.append(i)
                break
    if len(free) == 1:
        all2 = [i for i in allerg if i >= free[-1]]
        if len(all2) > 0 and len(t2) - free[-1] <= 3:
            t22 = [i for nn, i in enumerate(t2) if nn not in all2]
    elif len(free) > 1:
        print('hmmmm free')

    t225 = [i.strip() for i in re.sub(re_2per, '', '@ '.join(t22)
                                      .replace(';', ',')).split('@')]
    t221 = [i for i in token_thing(t225, 3, True) if len(i) > 0]

    t22_line = []
    for n, i in enumerate(t221):
        if i[-1] == '-' and n < len(t221)-1:
            if re.search(r'^[A-Za-z]', t221[n+1]):
                t22_line.append(n)

    # this loop is a glorified join, followed by regex
    t30 = ''
    for n, i in enumerate(t221):
        jparam = ' '
        toj = i
        if n == len(t221)-1:
            jparam = ''
        if n in t22_line:
            jparam = ''
            toj = toj.rstrip('-')
        t30 += toj + jparam
    t31 = re.sub(re_2per, ', ', t30)
    t31_old = re.sub(re_2per, ', ', ' '.join(t221))
    if t31 != t31_old and len(t22_line) == 0:
        print(t31_old + ' ---> ' + t31)
    t32 = re.sub(re_cont3, '', t31)
    t33 = re.sub(r'(\w)[\,](\w)', r'\g<1>, \g<2>', t32)
    t34 = t33.split('question', 1)[0].strip().replace(' & ', ' and ')
    t344 = re.sub(r'\b(?:contact|distributed)\b.*$', '', t34).strip()
    t345 = re.sub(r'[\*][\s\w]+$', '', t344)
    t35 = ''
    # fix parentheses
    if t345.count('(') == t345.count(')'):
        pct = 0
        for n, c in enumerate(t345):
            tchar = c
            if c == '(':
                pct += 1
            if c == ')':
                pct -= 1
            if c == ',' and pct > 0:
                tchar = ';'
            t35 += tchar
    t36 = t35.strip(',.').replace('  ', ' ').split(', ')
    t3 = [i for i in t36 if not re.match(re_cont4, i)]

    # combine parentheses into one line
    comb = []
    done = []
    for n, r in enumerate(t3):
        tline = []
        if n in done:
            continue
        if '(' in r and ')' not in r:
            for nn, rr in enumerate(t3[n:]):
                if ')' in rr:
                    tline += list(range(n, nn+n+1))
                    break
        else:
            tline.append(n)
        done += tline
        comb.append([t3[q] for q in tline])
    ing_list = [' '.join(i).replace('  ', ' ') for i in comb]

    # remove 'and' in last line
    if len(ing_list) > 0:
        pstore = re.findall(r'[\(].+?[\)]', ing_list[-1].strip())
        ingstore = re.sub(r'[\(].+?[\)]', '+++', ing_list[-1].strip())
        if ' and ' in ingstore:
            tt = ingstore.split(' and ', 1)
            repl = 0
            for nn in range(len(tt)):
                while '+++' in tt[nn]:
                    tt[nn] = re.sub(r'[\+]{3}', pstore[repl], tt[nn])
                    repl += 1
            ing_list[-1] = tt[0].strip()
            ing_list.append(tt[1].strip())
        elif ing_list[-1].strip().startswith('and '):
            ing_list[-1] = ing_list[-1].strip().split('and ', 1)[1].strip()

        if '. ' in ing_list[-1]:
            ing_list[-1] = ing_list[-1].split('.  ')[0].strip()
        ing_list = [i.split('   ')[0].strip() for i in ing_list]
    ing_list = [i.strip('.,') for i in list(pd.unique(ing_list)) if len(i) > 2]
    ing_list = token_thing(ing_list, 5, True)

    # ---------------- look for other sections ---------------
    tol = 10  # tolerance for searching around keywords

    # pull out area to search
    ing_o = [n for n, r in enumerate(body) for k in keywords if k in r]
    filt2 = list(pd.unique([body[j] for i in ing_o for j in
                            range(i-tol, i+tol+1) if j >= 0 and
                            j < len(body)]))
    rem = []
    for nn, rr in enumerate(filt2):
        if re.search(re_free, rr) or (re.search(re_cont, rr) or
                                      re.search(re_cont2, rr)):
            rem.append(nn)
            continue
        for alle in allergen:
            if alle in rr:
                rem.append(nn)
                break
    filt222 = [i for ni, i in enumerate(filt2) if ni not in rem]

    filt12 = [re.sub(re_cont, '', j) for j in filt222]
    filt13 = [re.sub(re_cont2, '', j) for j in filt12]

    filt3 = token_thing(filt13, 2, False)
    filt = ' '.join(filt3).replace('  ', ' ').replace('sugar alcohol', '')

    # seach for things with (as ...)
    asg = re.findall(r_se, filt)
    chems_as = [re.sub(r'\d{1,3}[\%]\s', '', i).strip()
                for i in asg] if asg else []

    # search chemical list
    chems_fuzz_all = fuzzy_match(filt, sds=False)
    chems_fuzz = [i.strip(',. ') for i in chems_fuzz_all
                  if re.search(re.compile(
                          r'(?<![\-])\b(?:' + re.escape(i) + r')\b(?![\-])',
                          re.I), filt)]

    chems = chems_as + [q for q in chems_fuzz if q not in
                        [i for i in chems_fuzz for j in chems_as if i in j]]

    # filter based on lists in beginning of file
    chems2 = [i for i in chems if i not in minerals + terms]
    chems3 = [q for q in chems2 if q not in
              [i for i in chems2 for j in minerals2 if j in i]]

    found = [q for q in chems3 if q not in
             [i for i in chems3 for j in ing_list if i in j]]
    if 'drug facts' in filt:
        found = [i for i in found if i not in drug_no]
    found = [i for i in found if (i+' free' not in filt) and
             (i+'-free' not in filt)]
    found = [i for i in found if
             (('no '+i not in filt) and ('not '+i not in filt))
             and ('non-'+i not in filt)]
    if '_OCR' in key:
        found = [i for i in found if len(i) > 4]
    else:
        found = [i for i in found if len(i) > 2]
    found = [i for i in found if i not in exclude]
    found = [i for i in found if i not in amino_all]
    found = [i for i in found if i not in colorlist]

    label1 = [re.sub(r'\s?\d[\,\.]?\d{0,3}\s{0,3}(?:m[ce]?g|g)\s?',
                     ' ', i) for i in ing_list]
    label2 = [re.sub(r'\s?\d[\,\.]?\d{0,3}\s{0,3}(?:m[ce]?g|g)\s?',
                     ' ', i) for i in found]

    label_all = label1 + label2

    return label_all


# input a list of dicts or strings
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
        v_new = v.lstrip('-., ').rstrip('( ').replace('  ', ' ').strip(' \\/')
        return escape_string(re.sub(r_words, '', symbol_cleanup(v_new)))

    def wt_format(v):
        """Split the weight apart into 3 sections."""
        wt_new = {'min_wt': '', 'cent_wt': '', 'max_wt': ''}
        if len(v) == 0:
            return wt_new
        v2 = v.replace(',', '.').split('-')
        if len(v2) == 1:
            if '<' in v2[0]:
                wt_new['max_wt'] = str(float(v2[0].strip('<= ')))
            elif '>' in v2[0]:
                wt_new['min_wt'] = str(float(v2[0].strip('>= ')))
            else:
                wt_new['cent_wt'] = str(float(v2[0]))
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


def pdf_sort(filename):
    """Read and organize the PDFs.

    This function is very important. It reads each file and decides what to do
    with it. After cheching if it needs OCR or if it is an MSDS, the function
    will search for Section 3 in the MSDS.

    Args:
        filename (str): Filename.

    Returns:
        list: List of many variables, see below.

    """
    # organize the files by filename
    not_pdf = []  # don't do anything with these
    not_sds = []  # not detected as an SDS
    too_3or4 = []  # examine and fix
    no_3or4 = []  # examine and fix
    needs_ocr = []  # pdfs that need ocr
    failed_files = []  # files that failed to load
    split_pdfs = []  # list of pdfs that had multiple msds (successful only)

    # counters
    step0_fail = 0  # pdfs which were not read successfully
    step1_fail = 0  # where a section was not found
    step1_success = 0  # pdfs with text successfully extracted

    # these are the categories for further processing
    to_sec = {}  # text and pdf where the important parts were parsed
    to_old = {}  # text and pdf where the parsing failed
    to_label = {}  # images of labels to parse

    for f in [filename]:

        # read and process files
        data = {}
        print('----- '+f+' -----')
        path = os.path.join(folder, f)

        if os.path.splitext(f)[1] != '.pdf':
            print('Not a PDF')
            not_pdf.append(f)
            failed_files.append(f)
            step0_fail += 1
            continue

        headers = {'X-Tika-PDFextractInlineImages': 'false', }
        proc1 = parser.from_file(path, headers=headers)

        if proc1['status'] != 200:
            print('Failed to parse')
            failed_files.append(f)
            step0_fail += 1
            continue

        if proc1['content'] is None:
            needs_ocr.append(f)
            raw1 = []
            if not do_OCR:
                print(f+' needs OCR')
                failed_files.append(f)
                step0_fail += 1
                continue
        else:
            raw1 = [i for i in proc1['content'].splitlines() if
                    len(i.strip()) > 0]
        proc = proc1
        raw = raw1

        # perform OCR if necessary
        # hasOCR = False
        if do_OCR and (all_OCR or len(raw1) == 0):
            headers2 = {'X-Tika-PDFextractInlineImages': 'true', }
            proc2 = parser.from_file(path, headers=headers2)
            if proc2['content'] is not None:
                raw2 = [i for i in proc2['content'].splitlines()
                        if len(i.strip()) > 0]
                if len([1 for i in raw2 if i in raw1]) == len(raw2):
                    pass
                else:
                    # hasOCR = True
                    f = f+'_OCR'
                    print('Uses OCR: '+f)
                    proc = proc2
                    raw = raw2
            else:
                print('OCR Failed: '+f)
                print('Make sure tesseract is installed and restart tika')
                failed_files.append(f)
                step0_fail += 1
                continue

        # determine if MSDS
        if not re.search(sds, proc['content']) or \
                not re.search(sds2, proc['content']):
            # print('Not an SDS: '+f)
            not_sds.append(f)
            step1_success += 1
            data['raw'] = proc['content']
            to_label[f] = data
            continue

    # search for Section 3
        data['raw'] = raw
        ind3 = []
        ind4 = []
        sec3 = []
        sec4 = []
        indCAS = []
        secCAS = []
        for n, val in enumerate(raw):
            if n < len(raw)-1:
                if val.strip()[-1] in ['—', '–', '-', '°']:
                    val = val+raw[n+1].strip()
            if re.search(s3, ' '+val):
                ind3.append(n)
                sec3.append(val)
            if re.search(s4, ' '+val):
                ind4.append(n)
                sec4.append(val)
            se = re.findall(cas1, ' '+val)
            for g in se:
                t = [int(i) for i in (g[0]+g[1])[::-1]]
                if int(g[2]) == np.dot(t, list(range(1, len(t)+1))) % 10:
                    indCAS.append(n)
                    secCAS.append(str(int(g[0])) + '-' +
                                  ('0' + str(int(g[1])))[-2:] +
                                  '-' + str(int(g[2])))
            se2 = re.findall(cas12, ' '+val)
            for g in se2:
                t = [int(i) for i in (g[0]+g[1])[::-1]]
                if int(g[2]) == np.dot(t, list(range(1, len(t)+1))) % 10:
                    indCAS.append(n)
                    secCAS.append(str(int(g[0])) + '-' +
                                  ('0'+str(int(g[1])))[-2:] +
                                  '-' + str(int(g[2])))
                    print('Check: ' + str(int(g[0])) + '-' +
                          ('0' + str(int(g[1])))[-2:] + '-' + str(int(g[2])))

        # special case that needs correcting
        if len(ind3) == 2 and len(ind4) == 1:
            if (re.search(s3_2, ' ' + raw[ind3[0]]) and re.search(
                    s3_3, ' ' + raw[ind3[1]])) and ind3[-1] < ind4[0]:
                s1 = ' '.join(raw[ind3[0]:ind3[1]])
                s2 = ' '.join(raw[ind3[1]:ind4[0]])
                if 'CAS' in s1:
                    ind3 = [ind3[0]]
                    if 'CAS' not in s2:
                        ind4[0] = ind3[1]
                else:
                    if 'CAS' in s2:
                        ind3 = [ind3[1]]
                    else:
                        ind3 = [ind3[0]]

        # repeat headers, remove based on order
        ind3new = []
        if len(pd.unique(sec3)) < len(sec3):
            ind3new.append(ind3[0])
            for n in range(1, len(ind3)):
                if n-1 < len(ind4):
                    if ind3[n] > ind4[n-1]:
                        ind3new.append(ind3[n])
        ind4new = []
        if len(pd.unique(sec4)) < len(sec4):
            ind4new.append(ind4[0])
            for n in range(0, len(ind4)-1):
                if n+1 < len(ind3):
                    if ind4[n] < ind3[n+1] and ind4[n+1] > ind3[n+1]:
                        ind4new.append(ind4[n+1])

        if len(ind3new) > 0:
            ind3 = ind3new
        if len(ind4new) > 0:
            ind4 = ind4new

        # these find  documents which still need to be corrected
        c3 = len(ind3)
        c4 = len(ind4)
        if c3 > 1 and c3 != c4:
            print('Too many section 3 matches: '+f)
        if c3 == 0:
            print('No section 3 matches: '+f)
        if c4 > 1 and c3 != c4:
            print('Too many section 4 matches: '+f)
        if c4 == 0:
            print('No section 4 matches: '+f)

        data['ind3'] = ind3
        data['ind4'] = ind4
        data['indCAS'] = indCAS
        data['secCAS'] = secCAS
        # data['ocr'] = True if hasOCR else False

        if (c3 > 1 or c4 > 1) and c3 != c4:
            too_3or4.append(f)
            to_old[f] = data
            step1_fail += 1
            continue
        if c3 == 0 or c4 == 0:
            no_3or4.append(f)
            to_old[f] = data
            step1_fail += 1
            continue

        # split up files if they have multiple msds
        if c3 == c4:
            # check index
            if len([1 for i in range(len(ind3)-1)
                    if ind3[i+1] > ind4[i]]) != len(ind3)-1:
                print('Mixed up index: '+f)
                to_old[f] = data
                step1_fail += 1
                continue
            filt = [raw[ind3[i]+1:ind4[i]] for i in range(len(ind3))]
            if len(filt) > 1:
                split_pdfs.append(f)
                f += '_split'

        data['filt'] = filt

        to_sec[f] = data
        step1_success += 1

    return [to_sec, to_old, to_label, step0_fail, step1_fail, step1_success,
            not_pdf, not_sds, too_3or4, no_3or4, needs_ocr, failed_files,
            split_pdfs]


# ------------------- this is the main part!-----------------

# blank variables
step0_fail = 0  # pdfs which were not read successfully
step1_fail = 0  # where a section was not found
step1_success = 0  # pdfs with text successfully extracted

not_pdf = []  # don't do anything with these
not_sds = []  # not detected as an SDS
too_3or4 = []  # examine and fix
no_3or4 = []  # examine and fix
needs_ocr = []  # pdfs that need ocr
failed_files = []  # files that failed to load
split_pdfs = []  # list of pdfs that had multiple msds (successful only)

# keys for all these were removed
# chemicals: key to section to list
# chemicals_old: key to list
# chemicals_add: key to list

# sec_search: key to section to list of dicts
# sec_search_wide: key to list of dicts
# old_search: key to list of dicts

# label_search: key to list
# label_search2: key to list (not anymore)

info_df = []
# df_store = {}  # temp
tcomb = read_df()

# iterate through files
for f in pdfs:
    # read pdf
    comb = pdf_sort(f)

    # break out output
    step0_fail += comb[3]
    step1_fail += comb[4]
    step1_success += comb[5]
    not_pdf += comb[6]
    not_sds += comb[7]
    too_3or4 += comb[8]
    no_3or4 += comb[9]
    needs_ocr += comb[10]
    failed_files += comb[11]
    split_pdfs += comb[12]

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

    # create file info
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

    info_df.append(dinfo)

    df_comb.to_csv(os.path.join(out_folder, f.split('.pdf')[0] + '.csv'),
                   index=False)
    # df_store[f] = df_comb

# write info file
file_prop = pd.DataFrame(info_df)
file_prop.to_csv('file_info.csv', index=False)
