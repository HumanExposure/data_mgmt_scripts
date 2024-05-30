import glob
import pandas as pd
import os

os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\Functional CSVs')

# Get a list of all CSV files in the current directory
csv_files = glob.glob('*.csv')

# Initialize an empty list to hold dataframes
dfs = []

# Loop through each CSV file
for csv_file in csv_files:
    # Read each CSV file into a DataFrame and append it to the list
    dfs.append(pd.read_csv(csv_file))

# Concatenate all dataframes in the list
combined_df = pd.concat(dfs, ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv('combined.csv', index=False)