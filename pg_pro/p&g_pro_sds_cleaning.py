import os
import pandas as pd
import numpy as np
import math

pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\p&g pro sds\Composition Cleaning')
df = pd.read_csv('Factotum_Proctor_&_Gamble_Pro_SDS_raw_extracted_records_20240711.csv')

for index, row in df.iterrows():
    #row['raw_max_comp'] = str(row['raw_max_comp']).replace('<','')
    if str(row['raw_min_comp']).isnumeric() and str(row['raw_max_comp']).isnumeric():
        x = row['raw_min_comp']
        y = row['raw_max_comp']
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = y / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '<' in str(row['raw_central_comp']):
        x = float(str(row['raw_central_comp']).replace('<', '').strip())
        y = 0
        df.at[index, 'lower_wf_analysis'] = y / 100
        df.at[index, 'upper_wf_analysis'] = x / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '<' in str(row['raw_max_comp']):
        x = float(str(row['raw_max_comp']).replace('<', '').strip())
        y = float(row['raw_min_comp'])
        df.at[index, 'lower_wf_analysis'] = y / 100
        df.at[index, 'upper_wf_analysis'] = x / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '<' in str(row['raw_central_comp']):
        x = float(str(row['raw_central_comp']).replace('<', '').strip())
        df.at[index, 'lower_wf_analysis'] = 0
        df.at[index, 'upper_wf_analysis'] = x / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif not math.isnan(float(row['raw_min_comp'])) and not math.isnan(float(row['raw_max_comp'])):
        x = float(row['raw_min_comp'])
        y = float(row['raw_max_comp'])
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = y / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif not math.isnan(float(row['raw_central_comp'])):
        x = float(row['raw_central_comp'])
        x = round(x / 100, 15)
        df.at[index, 'lower_wf_analysis'] = ''
        df.at[index, 'upper_wf_analysis'] = ''
        df.at[index, 'central_wf_analysis'] = x
    elif math.isnan(row['raw_min_comp']) and math.isnan(float(row['raw_max_comp'])) and math.isnan(float(row['raw_central_comp'])):
        df.drop(index, inplace=True)

df = df[['ExtractedComposition_id', 'lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']]

df = df.fillna('')

df.to_csv('p&gprosds_Cleaned_Data.csv', index=False)

