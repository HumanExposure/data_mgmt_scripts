## created by @cnlutz20 at 20240606 13:11.
## 
## lutz.christian@epa.gov
##  



# %% imports
import os, string, csv, re
import camelot
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from glob import glob
from pikepdf import Pdf
from tqdm import tqdm
import unicodedata




# %%
os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\European Medicines EPAR')
epar_raw = pd.read_csv('vet_medicines_epar.csv')
epar_raw = epar_raw.loc[:,'Active substance']
# %%
n = len(epar_raw)
data_document_id=['1724078']*n
# %%
epar = pd.DataFrame({'raw_chem_name': epar,'data_document_id': data_document_id})
# %%
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
for j in range(0, len(epar)):
    epar["raw_chem_name"].iloc[j]=str(epar["raw_chem_name"].iloc[j]).strip().lower().replace(".","").replace("α","alpha").replace('TM', '').replace('β', 'beta').replace('γ', 'gamma')
    epar["raw_chem_name"].iloc[j]=clean(str(epar["raw_chem_name"].iloc[j]))
    if len(epar["raw_chem_name"].iloc[j].split())>1:
        epar["raw_chem_name"].iloc[j]=" ".join(epar["raw_chem_name"].iloc[j].split())

# %%% Repeating values declaration 
epar["data_document_id"]="1724078"
epar["data_document_filename"]="medicines_output_european_public_assessment_reports_en.pdf"
epar["doc_date"]="Tue, 05/12/2023"
epar["raw_category"]=""
epar["report_funcuse"]=""
epar["cat_code"]=""
epar["description_cpcat"]=""
epar["cpcat_code"]=""
epar["cpcat_sourcetype"]="ACToR Assays and Lists"


epar.to_csv('epar_ext.csv', columns=["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","report_funcuse","cat_code","description_cpcat","cpcat_code","component","cpcat_sourcetype"], index=False)


# %%
