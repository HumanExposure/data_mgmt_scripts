import os
import pandas as pd

directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files'

filenames = []
titles = []
organization = []

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        filenames.append(filename)
        titles.append(filename[:-4])

df = pd.DataFrame({'filename': filenames, 'title': titles, 'document_type': ['SD'] * len(filenames)})

df['url'] = ''
df['organization'] = df['filename'].str.split('_').str[0]
df['subtitle'] = ''
df['epa_reg_number'] = ''
df['pmid'] = ''
df['hero_id'] = ''

df.to_csv(r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\State_Industrial_DataGroupCreation.csv', index=False)