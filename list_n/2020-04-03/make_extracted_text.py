# -*- coding: utf-8 -*-
"""Get extracted text for upload.

Created on Fri Apr  3 13:27:46 2020

@author: SBURNS
"""

import pandas as pd
import os


label = 'list_n'
template_file = 'epa_list_n_-_april_3_2020_documents_20200403.csv'


df = pd.read_csv(label + '_extracted_info.csv')
df = df.dropna()

template = pd.read_csv(template_file).set_index('file name')

cols = ['data_document_id', 'data_document_filename', 'prod_name', 'doc_date',
        'rev_num', 'raw_category', 'raw_cas', 'raw_chem_name',
        'report_funcuse', 'raw_min_comp', 'raw_max_comp', 'unit_type',
        'ingredient_rank', 'raw_central_comp', 'component']

done_list = []
for name, row in df.iterrows():
    chem_df = pd.read_csv(os.path.join('chems_' + label, row['chem_filename']))
    fname = row['pdf_filename']

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
df_all.to_csv(label + '_extracted_text_formatted.csv', index=False)
