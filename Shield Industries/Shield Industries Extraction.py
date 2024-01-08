import pandas as pd
import string
import os
import re
pd.options.mode.chained_assignment = None

source_directory = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Tabula CSVs"
target_directory = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\CSVs"
id_filename_csv = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Factotum_Shield_Industries_Products_SDS_unextracted_documents_20240108.csv"
filename_title_csv = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Shield Industries CSV.csv"


id_filename_df = pd.read_csv(id_filename_csv)
filename_title_df = pd.read_csv(filename_title_csv)

csv_files = [f for f in os.listdir(source_directory) if f.endswith('.csv')]

new_columns = ["data_document_id","data_document_filename","prod_name","doc_date","rev_num","raw_category","raw_cas","raw_chem_name","report_funcuse","raw_min_comp","raw_max_comp","unit_type","ingrediant_rank","raw_central_comp","component"]

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

    for column in new_columns:
        if column not in df.columns:
            df[column] = ''
    
    new_csv_file = csv_file.replace('tabula-', '')
    df.to_csv(os.path.join(target_directory, new_csv_file), index=False)

