import pandas as pd
import os

directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\Functional CSVs'

for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)
        df = pd.read_csv(filepath)
        df['ingredient_rank'] = range(1, len(df) + 1)
        df['rev_num'] = ''
        df.to_csv(filepath, index=False)