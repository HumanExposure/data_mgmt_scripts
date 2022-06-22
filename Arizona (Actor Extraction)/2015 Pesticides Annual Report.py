# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 17:30:58 2022

Pesticide Contamination Prevention Program Annual Report (A.R.S. 49-303.C)
Extract chemicals and CAS from tables 2-7 with functional use if applicable
"""

import camelot
import pandas as pd

pdf = r'L:\Lab\HEM\hortonm\ADEQ\2015\documents\Arizona2015PesticideReport.pdf'

tables = camelot.read_pdf(pdf,pages='5-78', flavor='lattice')
# %%
chemName = []
casN = []
prodID = []
templateName = []
msdsDate = []
recUse = []
catCode = []
descrip = []
code = []
sourceType = []
funcUse = []
chemDetect = []

funcUses = ['biopesticide', 'suppression of nematodes', 'biostimulant',
            'biofungicide', 'biological fungicide', 'bioinsecticide',
            'herbicide', 'miticide', 'fungicide', 'biological fertilizer',
            'nematicide', 'insecticide', 'biofumigant', 'growth regulator']

# %%
i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    if i <= 4: #Table 2
        chemName.extend(df.loc[:,1])
        funcs = list(df.loc[:,2])
        func = []
        for x in funcs:
            x = [use for use in funcUses if(use in x.lower())]
            if len(x) == 0:
                func.append(' ')
            else: func.append(x[0])
        funcUse.extend(func)
        casN.extend(['']*len(df))
        prodID.extend(['1400364']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 8: #Table 3
        chemName.extend(df.loc[:,2])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,1])
        prodID.extend(['1400365']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 9: #end of table 3
        chemName.extend([df.iloc[0,0].split()[2]]*len(df))
        funcUse.extend(['']*len(df))
        casN.extend([df.iloc[0,0].split()[1]]*len(df))
        prodID.extend(['1400365']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 54: #Table 4
        chemName.extend(df.loc[:,5])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,4])
        prodID.extend(['1400366']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 56: #Table 5
        chemName.extend(df.loc[:,0])
        funcUse.extend(df.loc[:,1])
        casN.extend(['']*len(df))
        prodID.extend(['1400367']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 5.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 62: #Table 6
        chemName.extend(df.loc[:,3])
        funcUse.extend(df.loc[:,1])
        casN.extend(df.loc[:,2])
        prodID.extend(['1400368']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 6.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    else: #Table 7
        chemName.extend(df.loc[:,4])
        funcUse.extend(df.loc[:,2])
        casN.extend(df.loc[:,3])
        prodID.extend(['1400369']*len(df))
        templateName.extend(['Arizona 2015 Pesticide Report Table 7.pdf']*len(df))
        msdsDate.extend([2015]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    i+=1

# %%
j = len(chemName) - 1
while j >= 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    if ',' in chemName[j] or '\n' in chemName[j]:
        chemName[j] = chemName[j].replace(',','_')
        chemName[j] = chemName[j].replace('\n',' ')
    if "—" in chemName[j] or "–" in chemName[j] or "‐" in chemName[j] or ' ' in chemName[j]:
        chemName[j] = chemName[j].replace('—','-').replace('–','-').replace('‐','-').replace(' ',' ')
    if chemName[j].startswith('0 '):
        chemName[j] = chemName[j].split('0 ')[-1]
    if type(funcUse[j]) is not str:
        funcUse[j] = ''
    if chemName[j] == '':
        del chemName[j]
        del funcUse[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
        del chemDetect[j]
    if '*' in chemName[j]:
        chemName[j] = chemName[j].strip('*')
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    funcUse[j] = funcUse[j].lower()
    funcUse[j] = funcUse[j].strip()
    
    # A little bit of manual cleanup
    if '4-(trifluoromethyl)-1(2h)- pyrimidinyl]-4-fluoro-n- [[methyl(1- methylethyl)amino]sulfonyl]-' == chemName[j]:
        chemName[j-1] = 'benzamide_ 2-chloro-5-[3_6- dihydro-3-methyl-2_6-dioxo- 4-(trifluoromethyl)-1(2h)- pyrimidinyl]-4-fluoro-n- [[methyl(1- methylethyl)amino]sulfonyl]-'
        del chemName[j]
        del funcUse[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
        del chemDetect[j]
    j-=1
# %%
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType, 'chem_detected_flag':chemDetect})
df=df.drop_duplicates()
# %%
df.to_csv(r'L:\Lab\HEM\hortonm\ADEQ\2015\2015 Pesticides Annual Report.csv',index=False, header=True, date_format=None)