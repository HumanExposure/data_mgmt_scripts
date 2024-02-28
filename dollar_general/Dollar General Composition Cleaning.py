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
        processed_cell = re.sub(r'[^\d.-]','', cell)
        processed_cell = re.sub(r'^-+(?=\d)', '', processed_cell)
        return processed_cell
    else:
        return cell

df['raw_central_comp'] = df['raw_central_comp'].apply(process_cell)

def split_and_assign(cell):
    if isinstance(cell,str) and '-' in cell:
        lower, upper = cell.split('-', 1)
        try:
            lower = float(lower)
            upper = float(upper)
        except ValueError:
            lower = None
            upper = None
        return lower, upper, None
    else:
        return None, None, cell

df['lower_wf_analysis'], df['upper_wf_analysis'], df['central_wf_analysis'] = zip(*df['raw_central_comp'].apply(split_and_assign))

# Convert columns to numeric to ensure proper division
df['lower_wf_analysis'] = pd.to_numeric(df['lower_wf_analysis'], errors='coerce')
df['upper_wf_analysis'] = pd.to_numeric(df['upper_wf_analysis'], errors='coerce')
df['central_wf_analysis'] = pd.to_numeric(df['central_wf_analysis'], errors='coerce')

# Divide all cells under the three analysis columns by 100
df['lower_wf_analysis'] /= 100
df['upper_wf_analysis'] /= 100
df['central_wf_analysis'] /= 100

df = df.fillna('')

df = df[['ExtractedComposition_id', 'lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']]

df.to_csv('DGCC.csv', index=False)
