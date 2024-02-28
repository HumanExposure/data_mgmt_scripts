#%%
import os
import pandas as pd
import numpy as np
import math
import re

pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Dollar General')
df = pd.read_csv('Factotum_Dollar_General_SDS_raw_extracted_records_20240227.csv')

def process_cell(cell):
    if isinstance(cell,str):
        # If dash is present, keep only the dash and remove other symbols
        processed_cell = re.sub(r'[^\d.-]','', cell)
        processed_cell = re.sub(r'^-+(?=\d)', '', processed_cell)
        return processed_cell
    else:
        # If no dash, return the original value
        return cell

# Apply the processing function to each cell in the column
df['raw_central_comp'] = df['raw_central_comp'].apply(process_cell)


# for index, row in df.iterrows():
#     if not math.isnan(row['raw_min_comp']) and not math.isnan(row['raw_max_comp']):
#         x = row['raw_min_comp']
#         y = row['raw_max_comp']
#         df.at[index, 'lower_wf_analysis'] = x / 100
#         df.at[index, 'upper_wf_analysis'] = y / 100
#         df.at[index, 'central_wf_analysis'] = ''
#     elif '<' in str(row['raw_central_comp']):
#         x = float(str(row['raw_central_comp']).replace('<', '').strip())
#         df.at[index, 'lower_wf_analysis'] = 0
#         df.at[index, 'upper_wf_analysis'] = x / 100
#         df.at[index, 'central_wf_analysis'] = ''
#     elif '>' in str(row['raw_central_comp']):
#         x = float(str(row['raw_central_comp']).replace('>', '').strip())
#         df.at[index, 'lower_wf_analysis'] = x / 100
#         df.at[index, 'upper_wf_analysis'] = 1
#         df.at[index, 'central_wf_analysis'] = ''
#     elif not math.isnan(float(row['raw_central_comp'])):
#         x = float(row['raw_central_comp'])
#         df.at[index, 'lower_wf_analysis'] = ''
#         df.at[index, 'upper_wf_analysis'] = ''
#         df.at[index, 'central_wf_analysis'] = x / 100

# df = df[['ExtractedComposition_id', 'lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']]

# df = df.fillna('')

# df.to_csv('DGCC.csv', index=False)
# %%
