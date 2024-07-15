import os
import pandas as pd
import numpy as np
import math

pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Composition Cleaning')
df = pd.read_csv('Factotum_State_Industrial_Products_SDS_raw_extracted_records_20240711.csv')

for index, row in df.iterrows():
    #row['raw_max_comp'] = str(row['raw_max_comp']).replace('<','')
    if 'NE' in str(row['raw_central_comp']):
        df.drop(index, inplace=True)
    elif '(Proprietar' in str(row['raw_central_comp']):
        df.drop(index, inplace=True)
    elif str(row['raw_min_comp']).isnumeric() and str(row['raw_max_comp']).isnumeric():
        x = row['raw_min_comp']
        y = row['raw_max_comp']
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = y / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif ('-' in str(row['raw_central_comp'])) and ('<' in str(row['raw_central_comp'])):
        print(row['raw_central_comp'])
        x = 0
        y = 5
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = y / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '-' in str(row['raw_central_comp']):
        split = str(row['raw_central_comp']).split('-')
        x = float(split[0].strip())
        y = float(split[1].strip())
        df.at[index, 'lower_wf_analysis'] = x / 100
        df.at[index, 'upper_wf_analysis'] = y / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '<' in str(row['raw_central_comp']):
        x = float(str(row['raw_central_comp']).replace('<', '').strip())
        y = 0
        df.at[index, 'lower_wf_analysis'] = y / 100
        df.at[index, 'upper_wf_analysis'] = x / 100
        df.at[index, 'central_wf_analysis'] = ''
    elif '>' in str(row['raw_central_comp']):
        y = float(str(row['raw_central_comp']).replace('>', '').strip())
        x = 100
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

df.to_csv('State_Industrial_SDS_Cleaned.csv', index=False)

