# -*- coding: utf-8 -*-
"""Make RR for List N.

Created on Fri Apr  3 12:58:24 2020

@author: SBURNS
"""

import pandas as pd


label = 'list_n'
date = '2020-04-24'
df = pd.read_csv(label + '_extracted_info_' + date + '.csv')
df = df.dropna(subset=['pdf_filename'])

# filename,title,document_type,url,organization

df_rr = pd.DataFrame()
df_rr['filename'] = df['pdf_filename']
df_rr['title'] = df['product_name']
df_rr['document_type'] = 'FI'
df_rr['url'] = df['pdf_url']
df_rr['organization'] = 'US Environmental Protection Agency'
df_rr.to_csv(label + '_registered_documents_' + date + '.csv', index=False)
