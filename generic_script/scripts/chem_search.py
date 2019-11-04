# -*- coding: utf-8 -*-
"""Search text for CAS numbers and chemical names.

These functions search differently sorted texts and extract rows that are
likely to have important information. When searching for chemical names,
name matching functions are called.

Created on Thu Oct 31 17:50:31 2019

@author: SBURNS
"""
import pandas as pd
import numpy as np
import re
import time
import logging

from chem_match import fuzzy_match, match2

fa = re.compile(r'(?:(?:first.?aid)|(?:fire[a-z ]{0,7}explosion))',
                re.IGNORECASE)


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
        logging.debug('%s: No hazards.', key)
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
    logging.debug(key+': '+str(round(time.time()-ss)))
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
