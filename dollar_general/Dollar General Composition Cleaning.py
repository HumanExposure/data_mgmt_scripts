#%%
import os
import pandas as pd
import re

pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Dollar General')
df = pd.read_csv('Factotum_Dollar_General_SDS_raw_extracted_records_20240227.csv')
df = df[df['raw_central_comp'] != 'NP']
df = df[df['raw_central_comp'] != 'N']
df = df[df['raw_central_comp'] != 'n']
df = df[df['raw_central_comp'] != 'Balance']
df = df[df['raw_central_comp'] != 'Propietary']
df = df[df['raw_central_comp'] != 'Proprietary']
df = df[df['raw_central_comp'] != 'SODIUM LACTATE']
df = df[df['raw_central_comp'] != 'Trace']
df = df[df['raw_central_comp'] != 'v16']
df = df[df['raw_central_comp'] != '10,000 PPb']
df = df[df['raw_central_comp'] != '300.0000 PPM']

def remove_accidental_dash(cell):
    if isinstance(cell,str):
        cell = re.sub(r'-+', '-', cell)
        return re.sub(r'(?<!\d)-(?=\d)', '', cell)
    else:
        return cell

df['raw_central_comp'] = df['raw_central_comp'].apply(remove_accidental_dash)

def process_composition(composition):
    if isinstance(composition, str):
        if '-' in composition:
            if composition.startswith('1..00-5.00'):
                lower = round(1 / 100, 15)
                upper = round(5 / 100, 15)
                return lower, '', upper
            else:
                composition = composition.replace('<','').replace('>','').replace('=','').replace('≥', '').replace('≤','').replace('+','').replace(' ppm', '')
                lower, upper = map(float, composition.split('-'))
                lower = round(lower / 100, 15)
                upper = round(upper / 100, 15)
                return lower, '', upper
        elif composition.startswith('<2<5'):
            lower = round(2 / 100, 15)
            upper = round(5 / 100, 15)
            return lower, '', upper
        elif composition.startswith('<') or composition.startswith('≤'):
            upper = float(composition.lstrip('<').lstrip('≤').lstrip('=')) / 100
            upper = round(upper, 15)
            return 0, '', upper
        elif composition.startswith('>') or composition.startswith('≥') or composition.endswith('+'):
            lower = float(composition.lstrip('>').lstrip('≥').lstrip('=').replace('+','')) / 100
            lower = round(lower, 15)
            return lower, '', 1
        elif composition.startswith('6.0+0.20'):
            central = float(6.0) / 100
            central = round(central, 15)
            return '', central, ''
        elif composition.startswith('to 100'):
            lower = round(0 / 100, 15)
            upper = round(100 / 100, 15)
            return lower, '', upper
        elif composition.startswith('1.2.5'):
            lower = round(1 / 100, 15)
            upper = round(2.5 / 100, 15)
            return lower, '', upper
        elif composition.startswith('80 100'):
            lower = round(80 / 100, 15)
            upper = round(100 / 100, 15)
            return lower, '', upper
        elif composition.startswith('1.00 to 5.00'):
            lower = round(1 / 100, 15)
            upper = round(5 / 100, 15)
            return lower, '', upper
        elif composition.startswith('0 < 1'):
            lower = round(0 / 100, 15)
            upper = round(1 / 100, 15)
            return lower, '', upper
        elif composition.startswith('0< .4'):
            lower = round(0 / 100, 15)
            upper = round(0.4 / 100, 15)
            return lower, '', upper
        else:
            central = float(composition) / 100
            central = round(central, 15)
            return '', central, ''
    else:
        return '', '', ''

# Drop rows with empty composition data
df.dropna(subset=['raw_central_comp'], inplace=True)
df = df.fillna('')
df.dropna()
df = df[df['raw_central_comp'] != '']
df[['lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']] = df.apply(lambda row: pd.Series(process_composition(row['raw_central_comp'])), axis=1)
df = df[['ExtractedComposition_id', 'lower_wf_analysis', 'central_wf_analysis', 'upper_wf_analysis']]
df = df[df['central_wf_analysis'] != 0]

df.reset_index(drop=True,inplace=True)
df.to_csv('DGCC.csv', index=False)
# %%
