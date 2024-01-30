import os
import pandas as pd
import numpy as np
import math

pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Airgas\Airgas_Puregas Composition Cleaning')
df = pd.read_csv('Factotum_Airgas_PureGas_raw_extracted_records_20240130.csv')

for index, row in df.iterrows():
    if not math.isnan(row['raw_min_comp']) and not math.isnan(row['raw_max_comp']):
        x = row['raw_min_comp']
        y = row['raw_max_comp']
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = y / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '<' in str(row['raw_central_comp']):
        x = float(str(row['raw_central_comp']).replace('<', '').strip())
        df.at[index, 'lower_wf_analysis'] = 0
        df.at[index, 'upper_wf_analysis'] = x / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '>' in str(row['raw_central_comp']):
        x = float(str(row['raw_central_comp']).replace('>', '').strip())
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = 1
        df.at[index, 'central_wf_analysis'] = ''
    elif not math.isnan(float(row['raw_central_comp'])):
        x = float(row['raw_central_comp'])
        df.at[index, 'lower_wf_analysis'] = ''
        df.at[index, 'upper_wf_analysis'] = ''
        df.at[index, 'central_wf_analysis'] = x / 100

df = df[['ExtractedComposition_id', 'lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']]

df = df.fillna('')

df.to_csv('Airgas_Puregas Composition Cleaning.csv', index=False)
