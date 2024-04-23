import os
import pandas as pd
import numpy as np
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files')
directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files\CSV Files'
state_products_df = pd.read_csv('State_Industrial_Products.csv')
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join(directory, filename))
        
        df['data_document_filename'] = filename.replace('.csv', '.pdf')
        
        if not df.empty:
            matching_row = state_products_df[state_products_df['data_document_filename'] == df['data_document_filename'][0]]
            
            if not matching_row.empty:
                df['prod_name'] = matching_row['title'].values[0]

            df['rev_num'] = ''
            df['report_funcuse'] = ''
            df['unit_type'] = '3'
            df['ingredient_rank'] = np.arange(1, len(df) + 1)
            df['component'] = ''
             # convert 'raw_central_comp' to string and remove "%" symbol
            df['raw_central_comp'] = df['raw_central_comp'].astype(str).str.replace('%', '')
            
            # split 'raw_central_comp' column on "-", and assign to 'raw_min_comp' and 'raw_max_comp'
            mask = df['raw_central_comp'].str.contains('-')
            df.loc[mask, ['raw_min_comp', 'raw_max_comp']] = df.loc[mask, 'raw_central_comp'].str.split('-', expand=True)
            
            # delete data in 'raw_central_comp' if there was a dash
            df.loc[mask, 'raw_central_comp'] = ''
            df['raw_central_comp'] = df['raw_central_comp'].replace('nan', '')


        df.to_csv(os.path.join(directory, filename), index=False)

directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files\CSV Files'
dfs = []

for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join(directory, filename))
        dfs.append(df)
combined_df = pd.concat(dfs, ignore_index=True)
combined_df.to_csv(os.path.join(directory, 'combined.csv'), index=False)