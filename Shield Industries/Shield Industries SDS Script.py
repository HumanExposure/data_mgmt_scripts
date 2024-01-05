#%%
from tabula import read_pdf
import pandas as pd
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Shield Industries\SDS Files')
pdf_directory = r'C:\Users\mmetcalf\Documents and Scripts\Shield Industries\SDS Files'

pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]


#for pdf_file in pdf_files:
    

# %%
