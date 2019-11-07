# -*- coding: utf-8 -*-
"""Find chemical names in text.

These functions take a string of text to find chemical names and other info.

Created on Thu Oct 31 17:57:13 2019

@author: SBURNS
"""

import re
import pandas as pd
import logging
from fuzzywuzzy import fuzz  # used to use this more but was inefficient
# from fuzzywuzzy import process
# NEEDS MANUAL FIX https://github.com/seatgeek/fuzzywuzzy/pull/243/files
# I also added the autojunk parameter
# https://github.com/seatgeek/fuzzywuzzy/issues/224


from pdf_import import cas1
from formatting import symbol_cleanup


cas = re.compile(r'(\d{2,7})[\—\–\-\° ]{1,3}(\d{2})[\—\–\-\° ]{1,3}([\d])',
                 re.IGNORECASE)
ecno = re.compile(r'\s?(\d{3})[\—\–\-\° ]{1,3}(\d{3})[\—\–\-\° ]{1,3}' +
                  r'([\d])\s?', re.IGNORECASE)

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

# ones for label search
terms = ['total', 'natural', 'based', 'extract', 'organic', 'root', 'con',
         'film', 'adhesive', 'varnish', 'vehicle', 'purpose', 'date', 'leaf',
         'inc', 'palm', 'key', 'unique', 'pure', 'antioxidant', 'moisture',
         'pet', 'none', 'special', 'liner', 'cardboard', 'sheet', 'filtered',
         'raw', 'allergens', 'organic', 'plant derived', 'balance', 'source',
         'vinyl', 'tox', 'alpha', 'solvent', 'scent', 'dust', 'all natural',
         'electrolyte', 'certified organic', 'light']
colorlist = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'purple',
             'violet', 'pigment']
exclude = ['secret', 'proprietary', 'n/a', 'cbi', 'trade', 'not available']
re_cont4 = re.compile(r'\b(?:contain[s]?)\b', re.I)


def fuzzy_match(row, tcomb, sds=True):
    """Find chemical names in a string.

    Using the list of chemicals from before, search the input string for
    matches. There are filters in place to look for bad matches, since the
    input list has some errors.

    Args:
        row (str): String in which to search for matches.
        tcomb(df): DataFrame of chemicals.
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
            logging.debug(str(rem2))

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
                logging.warning('WT Error: ' + str(gp))
            wt = wt.replace(' ', '') + unit

        # get name from beginning, use regex to remove strange patterns
        if gwt:
            nm = re.sub(gwt.group(0),
                        '+++', rem2).split('+++', 1)[0].strip().lower()
            nm2 = re.sub(cl, '', nm).strip(' .')
            nm2 = re.sub(cl2, '', nm2).strip(' .')
            nm2 = re.sub(r'\s+', ' ', nm2)
            nm2 = re.sub(r'^\d{1,2}[\)\.\:]\s?', '', nm2)
            nm2_old = re.sub(cl_old, '', nm).strip(' .')
            if nm2 != nm2_old:
                print(nm2_old + ' ---> ' + nm2)
            nm2 = nm2 if re.search(r'\w', nm2) else ''
            if nm2 == '' and tcas != '':
                nm2 = 'CASRN='+tcas
            cl_chem = []
            for nn, i in enumerate(chems):
                ntmp = re.sub(r_ci, ' ', i).strip().split('(ci')[0]
                ntmp = re.sub(cl, '', ntmp).strip(' .')
                ntmp = re.sub(cl2, '', ntmp).strip(' .')
                ntmp = re.sub(r'\s+', ' ', ntmp)
                ntmp = re.sub(r'^\d{1,2}[\)\.\:]\s?', '', ntmp)
                cl_chem.append(ntmp)
            newlist = []
            for i in cl_chem:
                inside = False
                for j in cl_chem:
                    if i in j and i != j:
                        inside = True
                        break
                newlist.append(i if not inside else None)
            for nn, i in enumerate(chems):
                ntmp = newlist[nn]
                if (fuzz.ratio(nm2, ntmp) > 60 or ntmp is None) or (
                        (ntmp in nm2 or nm2 in ntmp) or
                        ((ntmp in nm or nm in ntmp) and re.search(r'\w', nm))):
                    # if (ntmp not in nm2 and nm2 not in ntmp) and (
                    #         (ntmp in nm or nm in ntmp) and
                    #         re.search(r'\w', nm)):
                    #     print('CHECK: ' + ntmp + ' - ' + nm2 + ' ++++++++++')
                    if d[i]['cas'] != '' or d[i]['wt'] != '':
                        print('Dict not blank: ' + str(d))
                        logging.warning('Dict not blank: ' + str(d))
                        continue
                    del d[i]
            nm2 = nm2.strip() + ' - secret' if ts == 1 else nm2
            d[nm2] = {'cas': tcas, 'wt': wt}
            if ci_color:
                d[nm2]['ci_color'] = [j.strip() for i in ci_color
                                      for j in i.split(',')
                                      if len(j.strip()) > 0]
                print(d)
                logging.debug(str(d))

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
                        logging.debug(str(d))

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
                                        if k in re.sub(r'\s+', ' ',
                                                       si.lower()):
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
                                                logging.warning('WT Error: ' +
                                                                str(gp))
                                            wt = wt.replace(' ', '') + unit
                                        tmp = v.copy()
                                        tmp['wt'] = wt
                                        d[k.strip()+' '+wval1] = tmp
                                        print('--fix--')
                                        print(rem2)
                                        print(d)
                                        print('-------')
                                        logging.debug('Fixed %s ---> %s',
                                                      str(rem2), str(d))
                                        del d[k]
                                        break
    return d
