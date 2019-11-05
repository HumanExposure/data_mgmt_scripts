# -*- coding: utf-8 -*-
"""Search a product label's text.

Created on Thu Oct 31 17:43:34 2019

@author: SBURNS
"""

import re
import pandas as pd
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from chem_match import fuzzy_match, exclude, terms, re_cont4, colorlist
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

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
re_2per = re.compile(r'[\.\;]?(?:\scontains)?' +
                     r'(?: \d(?:\%|percent) or less of| ' +
                     r'(?:less than |[\＜\﹤\<]\s?)\d(?:\%|percent) of)' +
                     r'(?: the following)?[:]?',
                     re.I)
re_free = re.compile(r'(?<![\-])\b(?:free)\b', re.I)


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
drug_no = ['vehicle']
amino = ['amino acid', 'alanine', 'arginine', 'asparagine', 'aspartic acid',
         'cysteine', 'glutamine', 'glutamic acid', 'glycine', 'histidine',
         'isoleucine', 'leucine', 'lysine', 'methionine', 'phenylalanine',
         'proline', 'serine', 'threonine', 'tryptophan', 'tyrosine',
         'valine', 'amino acids']
amino_all = [qq for q in [['l-'+j, 'd-'+j, j] for j in amino] for qq in q]


# search labels
def fun_label_search(key, val, tcomb):
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
        logging.debug('Error with free thing')
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
    chems_fuzz_all = fuzzy_match(filt, sds=False, tcomb=tcomb)
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
