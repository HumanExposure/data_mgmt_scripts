# -*- coding: utf-8 -*-
"""Get extracted text for upload.

Created on Fri Apr  3 13:27:46 2020

@author: SBURNS
"""

import pandas as pd
import os
import re


label = 'list_n'
template_file = 'epa_list_n_-_april_24_2020_documents_20200424.csv'
date = '2020-04-24'

df = pd.read_csv(label + '_extracted_info_' + date + '.csv')
df = df.dropna()

template = pd.read_csv(template_file).set_index('file name')

cols = ['data_document_id', 'data_document_filename', 'prod_name', 'doc_date',
        'rev_num', 'raw_category', 'raw_cas', 'raw_chem_name',
        'report_funcuse', 'raw_min_comp', 'raw_max_comp', 'unit_type',
        'ingredient_rank', 'raw_central_comp', 'component']

new_names = {'1-Decanaminium, N,N-dimethyl-N-octyl-, chloride':
             'Octyl decyl dimethyl ammonium chloride',
             '1-Octanaminium, N,N-dimethyl-N-octyl-, chloride':
                 'Dioctyl dimethyl ammonium chloride',
                 '1-Decanaminium, N-decyl-N,N-dimethyl-, chloride':
                     'Didecyl dimethyl ammonium chloride',
                     'Isopropyl alcohol': 'Isopropanol',
                     'Ethyl alcohol': 'Ethanol'}

reg = re.compile(r'^(?:Alkyl[\*] dimethyl ' +
                 '(ethyl)?benzyl ammonium chloride ' +
                 r'[\*])[\(]((?:\d{1,2}[\%][C][1]\d[\,]?\s*){2,})[\)]$')


def fix_alkyl(x, pname):
    """Reformat alkyl chemicals."""
    m = re.search(reg, x)
    if not m:
        return x
    lonza = True if 'lonza' in pname else False
    vals = [i.strip().split('%') for i in m.group(2).split(',')]

    vals2 = [i[1] + ', ' + i[0] + '%' if lonza else i[0] + '%' + ' ' + i[1]
             for i in vals]
    chems = (', ' if not lonza else '; ').join(vals2)

    y = 'Alkyl (' + chems + ') dimethyl ' + \
        ('ethyl' if m.group(1) is not None else '') + \
        'benzyl ammonium chloride'

    return y


def make_dec(x, maxval):
    """Add decimal places to number."""
    if '.' not in str(x):
        return str(x) + '.' + ''.join(['0'] * maxval)

    x = str(round(x, 7)).rstrip('0')
    toadd = maxval - len(x.split('.')[1])
    return x + ''.join(['0'] * toadd)


done_list = []
for name, row in df.iterrows():
    chem_df = pd.read_csv(os.path.join('chems_' + label, row['chem_filename']))
    fname = row['pdf_filename']

    # fix chemicals
    chem_df['Active Ingredient Name'] = chem_df['Active Ingredient Name'] \
        .apply(lambda x: new_names[x] if x in new_names else x)
    chem_df['Active Ingredient Name'] = chem_df['Active Ingredient Name'] \
        .apply(fix_alkyl, args=(row['product_name'],))
    chem_df = chem_df.append(pd.Series(
        {'Active Ingredient Name': 'Other Ingredients', 'Percent Active':
         100-chem_df['Percent Active'].sum()},
        name=chem_df.index.max()+1))
    maxlen = chem_df['Percent Active'].apply(
        lambda x: len(str(x).split('.')[-1])).tolist()
    maxval = max(max([i for i in maxlen if i < 8]), 2)
    chem_df['Percent Active'] = chem_df['Percent Active'].apply(make_dec,
                                                                args=(maxval,))

    newdf = pd.DataFrame(columns=cols)
    newdf['raw_chem_name'] = chem_df['Active Ingredient Name']
    newdf['raw_central_comp'] = chem_df['Percent Active']
    newdf['data_document_id'] = template.loc[fname, 'ID']
    newdf['data_document_filename'] = template.loc[fname, 'file']
    newdf['prod_name'] = row['product_name']
    newdf['doc_date'] = row['date']
    newdf['unit_type'] = 3
    newdf['ingredient_rank'] = pd.Series(range(len(newdf)))+1

    done_list.append(newdf)

df_all = pd.concat(done_list)
df_all.to_csv(label + '_extracted_text_formatted_' + date + '.csv',
              index=False)
