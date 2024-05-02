#%%
from tabula import read_pdf
import numpy as np
import pandas as pd
import string
import os
import re
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\Dutch Government\Docs')
i = 18
tableI1 = []
while i < 25:
     table=read_pdf("Dutch Packagings and Consumer Articles Regulation from July 1st 2022.pdf", pages=str(i), lattice=False, pandas_options={'header': None})[0]
     table.drop([0,3,4],axis=1,inplace=True)
     table.drop([0,1],axis=0,inplace=True)
     table.reset_index(drop=True,inplace=True)
     tableI1.append(table)
     i = i + 1
tableI1 = pd.concat(tableI1,ignore_index=True)
# %%
