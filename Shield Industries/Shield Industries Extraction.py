import pandas as pd
import string
import os
import re
import PyPDF2
import numpy as np
pd.options.mode.chained_assignment = None

#Code to extract raw_category
pdf_directory = r'C:\Users\mmetcalf\Documents and Scripts\Shield Industries\SDS Files'
pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]
df2 = pd.DataFrame()
for pdf_file in pdf_files:
    with open(os.path.join(pdf_directory,pdf_file), 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        page = reader.getPage(0)
        text = page.extractText()
        start = text.find('/Class:') + len('/Class:')
        end = text.find('Product ID:')
        raw_category = text[start:end].strip()
        start2 = text.find('Product Name:') + len('Product Name:')
        end2 = text.find('Date')
        product_name = text[start2:end2].strip()
        match = re.search(r'\b\d+/\d+/\d+\b',text)
        if match:
            doc_date = match.group()
        else:
            date = ''
        new_row = pd.DataFrame({'raw_category':[raw_category], 'filename': [pdf_file], 'title': [product_name],'doc_date':[doc_date]})
        df2 = pd.concat([df2,new_row], ignore_index=True)


source_directory = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Tabula CSVs"
target_directory = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\CSVs"
id_filename_csv = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Factotum_Shield_Industries_Products_SDS_unextracted_documents_20240108.csv"
filename_title_csv = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Shield Industries CSV.csv"

id_filename_df = pd.read_csv(id_filename_csv)
filename_title_df = pd.read_csv(filename_title_csv)

csv_files = [f for f in os.listdir(source_directory) if f.endswith('.csv')]

new_columns = ["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingredient_rank","raw_central_comp","component"]

for csv_file in csv_files:
    pdf_name = csv_file.replace('tabula-', '').replace('.csv','.pdf')
    data_document_id = id_filename_df.loc[id_filename_df['data_document_filename'] == pdf_name, 'data_document_id'].values[0]
    data_document_filename = pdf_name

    prod_name = filename_title_df.loc[filename_title_df['filename'] == pdf_name,'title'].values[0]

    df = pd.read_csv(os.path.join(source_directory, csv_file), header=None)

    df['raw_chem_name'] = df.iloc[:,0]
    df['raw_cas'] = df.iloc[:,1]
    df['raw_central_comp'] = df.iloc[:,2]
    df['raw_central_comp'] = df['raw_central_comp'].apply(lambda x: re.sub('%','', str(x)))
    df.drop(df.columns[[0, 1, 2]],axis=1,inplace=True)


    df['data_document_id'] = data_document_id
    df['data_document_filename'] = data_document_filename
    df['unit_type'] = '3'
    df['prod_name'] = prod_name

    if data_document_filename in df2['filename'].values:
        doc_date = df2.loc[df2['filename'] == data_document_filename,'doc_date'].values[0]
        df['doc_date'] = doc_date
        raw_category = df2.loc[df2['filename'] == data_document_filename,'raw_category'].values[0]
        df['raw_category'] = raw_category

    for column in new_columns:
        if column not in df.columns:
            df[column] = ''
    
    for index, row in df.iterrows():
        value = str(row['raw_central_comp'])
        if '-' in value or '–' in value:
            min_val, max_val = [x.strip() for x in value.replace('–', '-').split('-')]
            try:
                df.at[index, 'raw_min_comp'] = float(min_val)
                df.at[index, 'raw_max_comp'] = float(max_val)
                df.at[index, 'raw_central_comp'] = " "
            except ValueError:
                print(f"Cannot convert {min_val} and/or {max_val} to float.")
    
    df['raw_cas'] = df['raw_cas'].astype(str)

    for index, row in df.iterrows():
        value = str(row['raw_chem_name'])
        match = re.search(r'(\d+-\d+-\d+)', value)
        if match:
            cas_number = match.group()
            chem_name = value.replace(cas_number, '').strip()
            df.at[index, 'raw_chem_name'] = chem_name
            df.at[index, 'raw_cas'] = cas_number

    df['raw_central_comp'] = df['raw_central_comp'].astype(str)  # Convert to string for comparison

    for index in range(len(df) - 1, 0, -1):  # Loop backwards to avoid skipping rows after deletion
        if df.at[index, 'raw_central_comp'] == 'nan':
            df.at[index - 1, 'raw_chem_name'] += ' ' + str(df.at[index, 'raw_chem_name'])
            df.drop(index, inplace=True)

    df['raw_cas'] = df['raw_cas'].replace('nan', '')
    df['ingredient_rank'] = range(1, len(df) + 1)
    df.reset_index(drop=True, inplace=True)  # Reset the index after row deletion

    new_csv_file = csv_file.replace('tabula-', '')
    df.to_csv(os.path.join(target_directory, new_csv_file), index=False)

source = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\CSVs"

dfs = []

for filename in os.listdir(source):
    if filename.endswith(".csv"):
        dft = pd.read_csv(os.path.join(source,filename))
        dfs.append(dft)

combined_df = pd.concat(dfs)

combined_df.to_csv('combined.csv', index=False)
