# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:14:05 2022

@author: MHORTON

Arizona Department of Environmental Quality Pesticide Groundwater Quality Protection Annual Report 2019

"""

import camelot
import pandas as pd

pdf = r'L:\Lab\HEM\hortonm\ADEQ\2019\documents\PesticdeReport_2019_FINAL.pdf'

tables = camelot.read_pdf(pdf,pages='3-52', flavor='lattice')
# Appendix A: pages 3-41 - i 0 to 39
# Appendix B: pages 43-52 - i 40 to 50
# %%
docID = []
docFilename = []
docDate = []
rawCat = []
casN = []
chemName = []
funcUse = []
catCode = []
descCpcat = []
cpcatCode = []
cpcatSource = []
chemDetect = []

i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])

    if i <= 39: #Appendix A
        chemName.extend(df.loc[:,2])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,1])
        docID.extend(['1644148']*len(df))
        docFilename.extend(['PesticdeReport_2019_FINAL-A.pdf']*len(df))

    else: #Appendix B
        chemName.extend(['']*len(df))
        funcUse.extend(df.loc[:,1])
        casN.extend(df.loc[:,4])
        docID.extend(['1644149']*len(df))
        docFilename.extend(['PesticdeReport_2019_FINAL-B.pdf']*len(df))
    i+=1

j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    if "—" in chemName[j] or "–" in chemName[j] or "‐" in chemName[j] or ' ' in chemName[j]:
        chemName[j] = chemName[j].replace('—','-').replace('–','-').replace('‐','-').replace(' ',' ')
    if '\n' in funcUse[j]:
        funcUse[j] = funcUse[j].replace('\n',' ')
    if '\n' in casN[j]:
        casN[j] = casN[j].replace('\n',' ')

    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    funcUse[j] = funcUse[j].lower()
    funcUse[j] = funcUse[j].strip()
    
    # # A little bit of manual cleanup
    if 'groundwater quality protection' in funcUse[j]:
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    if '131860-33-8  161050-58-4' in casN[j]:
        casN[j] = '161050-58-4'
        funcUse[j] = 'insecticide'
    if 'FINAL-B' in docFilename[j] and chemName[j] == '' and funcUse[j] == '':
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    if 'NULL' in casN[j]:
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    j-=1
# %%
# docID
# docFilename
docDate = ['2019']*len(docID)
rawCat = ['']*len(docID)
# casN
# chemName
# funcUse
catCode = ['']*len(docID)
descCpcat = ['']*len(docID)
cpcatCode = ['']*len(docID)
cpcatSource = ['']*len(docID)
chemDetect = ['']*len(docID)

df = pd.DataFrame({'data_document_id':docID, 'data_document_filename':docFilename, 
                   'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':casN, 
                   'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 
                   'description_cpcat': descCpcat, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource, 
                   'chem_detected_flag':chemDetect})

df=df.drop_duplicates()
# %%
df.to_csv(r'L:\Lab\HEM\hortonm\ADEQ\2019\Pesticide Groundwater Quality Protection 2019.csv',index=False, header=True, date_format=None)