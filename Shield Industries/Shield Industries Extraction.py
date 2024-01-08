import pandas as pd
import string
import os
import re
pd.options.mode.chained_assignment = None

source_directory = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Tabula CSVs"
target_directory = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\CSVs"
id_filename_csv = r"C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Factotum_Shield_Industries_Products_SDS_unextracted_documents_20240108.csv"

id_filename_df = pd.read_csv(id_filename_csv)

csv_files = [f for f in os.listdir(source_directory) if f.endswith('.csv')]

new_columns = ["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","component","chem_detected_flag","author","doi"]

for csv_file in csv_files:
    pdf_name = csv_file.replace('tabula-', '').replace('.csv','.pdf')

    data_document_id = id_filename_df.loc[id_filename_df['data_document_filename'] == pdf_name, 'data_document_id'].values[0]
    data_document_filename = pdf_name

    df = pd.read_csv(os.path.join(source_directory, csv_file))
    df['data_document_id'] = data_document_id
    df['data_document_filename'] = data_document_filename

    for column in new_columns:
        if column not in df.columns:
            df[column] = ''
    
    df.to_csv(os.path.join(target_directory, csv_file), index=False)

