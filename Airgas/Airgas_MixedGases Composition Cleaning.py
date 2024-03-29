import os
import pandas as pd
import numpy as np
import math

pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Airgas\Airgas_MixedGases Composition Cleaning')
df = pd.read_csv('Factotum_Airgas_MixedGases_raw_extracted_records_20240329.csv')

df = df[df['unit_type'] == 'percent']

#This is to split up the huge CSV file (dataframe) into smaller chunks, then iterating through them. This lets factotum accept the CSV files
chunks = [df[i:i+4000] for i in range(0,len(df),4000)]

for i, chunk in enumerate(chunks):
    for index, row in chunk.iterrows():
        if not math.isnan(row['raw_min_comp']) and not math.isnan(row['raw_max_comp']):
            x = row['raw_min_comp']
            y = row['raw_max_comp']
            chunk.at[index, 'lower_wf_analysis'] = x / 100
            chunk.at[index, 'upper_wf_analysis'] = y / 100
            chunk.at[index, 'central_wf_analysis'] = ''
        elif '<' in str(row['raw_central_comp']):
            x = float(str(row['raw_central_comp']).replace('<', '').strip())
            chunk.at[index, 'lower_wf_analysis'] = 0
            chunk.at[index, 'upper_wf_analysis'] = x / 100
            chunk.at[index, 'central_wf_analysis'] = ''
        elif '>' in str(row['raw_central_comp']):
            x = float(str(row['raw_central_comp']).replace('>', '').strip())
            chunk.at[index, 'lower_wf_analysis'] = x / 100
            chunk.at[index, 'upper_wf_analysis'] = 1
            chunk.at[index, 'central_wf_analysis'] = ''
        elif not math.isnan(float(row['raw_central_comp'])):
            x = float(row['raw_central_comp'])
            chunk.at[index, 'lower_wf_analysis'] = ''
            chunk.at[index, 'upper_wf_analysis'] = ''
            chunk.at[index, 'central_wf_analysis'] = x / 100
        elif math.isnan(row['raw_min_comp']) and math.isnan(row['raw_max_comp']) and math.isnan(row['raw_central_comp']):
            chunk.drop(index, inplace=True)
    chunk = chunk[['ExtractedComposition_id', 'lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']]
    chunk = chunk.fillna('')
    filename = f'Airgas_MixedGases_Composition_Cleaning_{i+1}.csv'
    chunk.to_csv(filename, index=False)
