# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:27:03 2022

@author: MHORTON

Arizona Department of Environmental Quality Pesticide Groundwater Quality Protection Annual Report 2020

"""

import camelot
import pandas as pd

pdf = r'L:\Lab\HEM\hortonm\ADEQ\2020\documents\PesticdeReport_2020_FINAL.pdf'

tables = camelot.read_pdf(pdf,pages='3-24', flavor='lattice')
# Appendix A: pages 3-6 - i 0 to 3
# Appendix B: pages 7-18 - i 4 to 15
# Appendix C: pages 19-24 - i 16 to 22
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

# %%
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])

    if i <= 3: #Appendix A
        chemName.extend(df.loc[:,4])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,5])
        docID.extend(['1644150']*len(df))
        docFilename.extend(['PesticdeReport_2020_FINAL-A.pdf']*len(df))
    
    elif i <= 15: #Appendix B
        chems = df.loc[:,1].tolist()
        h=0
        for chem in chems:
            if chem == '':
                chems[h] = df.loc[h+1,2]
            h+=1
        chemName.extend(chems)
        funcUse.extend(['']*len(df))
        casN.extend(['']*len(df))
        docID.extend(['1644151']*len(df))
        docFilename.extend(['PesticdeReport_2020_FINAL-B.pdf']*len(df))

    else: #Appendix C
        chems = df.loc[:,0].tolist()
        h=0
        for chem in chems:
            if chem == '':
                chems[h] = df.loc[h+1,1]
            h+=1
        chemName.extend(chems)
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,2])
        docID.extend(['1644152']*len(df))
        docFilename.extend(['PesticdeReport_2020_FINAL-C.pdf']*len(df))
    i+=1
# %%
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
    
    # A lot of manual cleanup
    if '34256-82-1' in casN[j] and 'FINAL-A' in docFilename[j]:
        chemName[j] = 'acetochlor'
    if '193740-76-0' in casN[j] and 'FINAL-A' in docFilename[j]:
        chemName[j] = 'fluoxastrobin'
    if '951659-40-8' in casN[j] and 'FINAL-A' in docFilename[j]:
        chemName[j] = 'flupyradifurone'
    if '76674-21-0' in casN[j] and 'FINAL-A' in docFilename[j]:
        chemName[j] = 'flutriafol'
 
    if 'acetochlor' in chemName[j] and 'FINAL-C' in docFilename[j]:
        casN[j] = '34256-82-1'
    if 'fluoxastrobin' in chemName[j] and 'FINAL-C' in docFilename[j]:
        casN[j] = '193740-76-0'
    if 'flupyradifurone' in chemName[j] and 'FINAL-C' in docFilename[j]:
        casN[j] = '951659-40-8'
    if 'flutriafol' in chemName[j] and 'FINAL-C' in docFilename[j]:
        casN[j] = '76674-21-0'
 
    dupCas = ['114311-32-9', '131860-33-8', '77182-82-2']
    if 'FINAL-A' in docFilename[j] and any(cas in casN[j] for cas in dupCas) and chemName[j] == ''::
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    dupName = ['troubadour 2f insecticide', 'imazamox', 'chlorantraniliprole', 'azoxystrobin']
    if 'FINAL-C' in docFilename[j] and any(name in chemName[j] for name in dupName):
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    if 'chlorantraniliprole' in chemName[j] and 'FINAL-B' in docFilename[j]:
        chemName[j] = 'chlorantraniliprole'
    j-=1
# %%
# docID
# docFilename
docDate = ['2020']*len(docID)
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
# %%
df=df.drop_duplicates()
# %%
df.to_csv(r'L:\Lab\HEM\hortonm\ADEQ\2020\Pesticide Groundwater Quality Protection 2020.csv',index=False, header=True, date_format=None)
