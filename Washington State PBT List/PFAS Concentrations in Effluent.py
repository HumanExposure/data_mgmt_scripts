from tabula import read_pdf
import pandas as pd
import string
import os
import re
import math
pd.options.mode.chained_assignment = None
os.chdir(r'C:\Users\mmetcalf\Documents and Scripts\State of Washington\PFAS Concentrations in Effluent\Documents')

table2 = read_pdf("PFAS Concentrations in Effluent Table 2.pdf", pages="16", lattice=False, pandas_options={'header': None})[0]
