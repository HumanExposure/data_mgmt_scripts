
import os, csv, string
import pandas as pd
from glob import glob

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chemical curation files\uncurated_chems_2024_03'
os.chdir(path)


raw_csv=glob('Factotum_uncurated_chemicals*.csv')
cleaned_csv=glob('cleaned_Factotum_uncurated_chemicals*.csv')
for r in raw_csv:
    print(r)
    skipped_ids = []
    if 'cleaned_'+r in cleaned_csv:
        cleaned = pd.read_csv('cleaned_'+r)
        cleaned_ids=cleaned['raw_chem_id'].to_list()
        raw = csv.reader(open(r,encoding='utf8'))
        for row in raw:
            if row[1] != 'raw_chem_id' and int(row[1]) not in cleaned_ids:
                skipped_ids.append(row[1])
    
    n=len(skipped_ids)
    if n>0:
        external_id=skipped_ids
        rid=['NA']*n
        sid=['']*n
        true_chemical_name=['']*n
        true_cas=['']*n
        
        df = pd.DataFrame({'external_id':external_id, 'rid':rid, 'sid':sid, 'true_chemical_name':true_chemical_name, 'true_cas':true_cas})
        df=df.drop_duplicates()
        df.to_csv('skipped_'+r,index=False, header=True, encoding = "utf-8")