# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 15:54:15 2022

@author: MHORTON

Methamphetamine and Illicit Drugs, Precursors and Adulterants on Wipes by Liquid-Liquid Extraction
"""

import tabula as tb
import math
import re
import pandas as pd

# %%
pdf = 'C:\\Users\\mhorton\\OneDrive - Environmental Protection Agency (EPA)\\Profile\\Documents\\Methamphetamine and Illicit Drugs\\601a361f-4fea-4ab2-be2d-3991e2af0d5e.pdf'

df = tb.read_pdf(pdf, pages='10', area=(100, 0, 606, 610), guess=True)
df = df[0]

chems = df['(alphabetically)'].tolist()
cas = df['CAS #(2)'].tolist()

for i, c in enumerate(cas):
    if '(' in c:
        cas[i] = c.split('(')[0]

# some quick manual cleanup
cas[35] = '321-97-1'
cas[29] = '37577-28-9'
cas[18] = '4846-07-5'
cas[13] = '82801-81-8'
cas[6] = '90-81-3'

pattern = re.compile(r'\([\d]')
for i, c in reversed(list(enumerate(chems))):
    if type(c) is not str and math.isnan(c) == True:
        cas[i-1] = cas[i-1] + '; ' + cas[i]
        del chems[i]
        del cas[i]
    elif len(pattern.findall(c)) != 0:
        chems[i] = c.rsplit('(', 1)[0]

prods = ['1371487']*len(cas)
tempname = ['NIOSH_Amph_PhysProp_orig.pdf']*len(cas)
date = ['17 October 2011']*len(cas)
recuse = ['']*len(cas)
desc = ['']*len(cas)
code = ['']*len(cas)
source = ['ACToR Assays and Lists']*len(cas)

extdf = pd.DataFrame({'data_document_id':prods, 'data_document_filename':tempname, 
                      'doc_date':date, 'raw_category':recuse, 'raw_cas':cas, 
                      'raw_chem_name':chems, 'cat_code':code, 'description_cpcat': desc, 
                      'cpcat_code':code, 'cpcat_sourcetype':source})
