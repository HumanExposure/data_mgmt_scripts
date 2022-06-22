# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 19:17:16 2022

@author: MHORTON

Arizona Department of Environmental Quality Pesticide Groundwater Quality Protection Annual Report 2021

"""

import camelot
import pandas as pd

pdf = r'L:\Lab\HEM\hortonm\ADEQ\2021\documents\PesticdeReport_2021.pdf'

tables = camelot.read_pdf(pdf,pages='3-21', flavor='lattice')
# Appendix A: pages 3-7 - i 0 to 4
# Appendix B: pages 7-16 - i 4 to 14
# Appendix C: pages 17-21 - i 15 to 20
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

    if i <= 4: #Appendix A
        chemName.extend(df.loc[:,4])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,5])
        docID.extend(['1644153']*len(df))
        docFilename.extend(['PesticdeReport_2021-A.pdf']*len(df))
    
    elif i <= 14: #Appendix B
        chems = df.loc[:,1].tolist()
        h=0
        for chem in chems:
            if chem == '':
                chems[h] = df.loc[h+1,2]
            h+=1
        chemName.extend(chems)
        funcUse.extend(['']*len(df))
        casN.extend(['']*len(df))
        docID.extend(['1644154']*len(df))
        docFilename.extend(['PesticdeReport_2021-B.pdf']*len(df))

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
        docID.extend(['1644155']*len(df))
        docFilename.extend(['PesticdeReport_2021-C.pdf']*len(df))
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
    if '34256-82-1' in casN[j] and '2021-A' in docFilename[j]:
        chemName[j] = 'acetochlor'
    if '193740-76-0' in casN[j] and '2021-A' in docFilename[j]:
        chemName[j] = 'fluoxastrobin'
    if '76674-21-0' in casN[j] and '2021-A' in docFilename[j]:
        chemName[j] = 'flutriafol'
    if '951659-40-8' in casN[j] and '2021-A' in docFilename[j]:
        chemName[j] = 'flupyradifurone'
 
    if 'acetochlor' in chemName[j] and '2021-C' in docFilename[j]:
        casN[j] = '34256-82-1'
    if 'fluoxastrobin' in chemName[j] and '2021-C' in docFilename[j]:
        casN[j] = '193740-76-0'
    if 'flupyradifurone' in chemName[j] and '2021-C' in docFilename[j]:
        casN[j] = '951659-40-8'
    if 'flutriafol' in chemName[j] and '2021-C' in docFilename[j]:
        casN[j] = '76674-21-0'
    if 'nicosulfuron' in chemName[j] and '2021-C' in docFilename[j]:
        casN[j] = '111991-09-04'
 
    dupCas = ['500008-45-7', '131860-33-8', '77182-82-2', '114311-32-9', '138261-41-3', '111991-09-04', '100784-20-1', '161050-58-4']
    if '2021-A' in docFilename[j] and any(cas in casN[j] for cas in dupCas) and chemName[j] == '':
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    dupName = ['methoxyfenozide', 'imidacloprid', 'imazamox', 'chlorantraniliprole', 'azoxystrobin']
    if '2021-C' in docFilename[j] and any(name in chemName[j] for name in dupName) and casN[j] == '':
        del docID[j]
        del docFilename[j]
        del casN[j]
        del chemName[j]
        del funcUse[j]
    if 'chlorantraniliprole' in chemName[j] and '2021-B' in docFilename[j]:
        chemName[j] = 'chlorantraniliprole'
    if 'azoxystrobin' in chemName[j] and '2021-B' in docFilename[j]:
        chemName[j] = 'azoxystrobin'
    j-=1
# %%
# docID
# docFilename
docDate = ['2021']*len(docID)
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
df.to_csv(r'L:\Lab\HEM\hortonm\ADEQ\2021\Pesticide Groundwater Quality Protection 2021.csv',index=False, header=True, date_format=None)