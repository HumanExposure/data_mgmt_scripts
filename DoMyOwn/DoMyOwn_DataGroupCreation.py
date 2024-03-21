import os
import pandas as pd

directory = r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\SDS Files'

filenames = []
titles = []

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        filenames.append(filename)
        titles.append(filename[:-4])

df = pd.DataFrame({'filename': filenames, 'title': titles, 'document_type': ['SD'] * len(filenames)})

df.to_csv(r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\DoMyOwn_DataGroupCreation.csv', index=False)
