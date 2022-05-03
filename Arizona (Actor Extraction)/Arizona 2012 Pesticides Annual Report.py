# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:34:54 2022

2012 Pesticides Annual Report (A.R.S 49-303.C)
Extract chemicals and CAS from tables 2-7
"""

import camelot
import pandas as pd

pdf = r'C:\Users\mhorton\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\APR2012\9620de2f-f784-4798-acd2-1ed5b6e35bd0.pdf'
tables = camelot.read_pdf(pdf,pages='5-33', flavor='lattice')

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

funcDict = {
  "H": "herbicide",
  "F": "fungicide",
  "O": "ovicides",
  "R": "regulator",
  "I": "insecticide",
  "M": "miticides",
  "N": "nematicide",
  "D": "defoliant"
  }

i=0 
for table in tables:
    df = tables[i].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    if i == 0: #Table 2
        chemName.extend(df.loc[:,1])
        funcs = [x.split()[0] for x in  list(df.loc[:,2])]
        funcUse.extend(funcs)
        casN.extend(['']*len(df))
        prodID.extend(['1400346']*len(df))
        templateName.extend(['Arizona 2012 Pesticide Report Table 2.pdf']*len(df))
        msdsDate.extend([2012]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 4: #Table 3
        chemName.extend(df.loc[:,2])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,1])
        prodID.extend(['1400347']*len(df))
        templateName.extend(['Arizona 2012 Pesticide Report Table 3.pdf']*len(df))
        msdsDate.extend([2012]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 21: #Table 4
        chemName.extend(df.loc[:,5])
        funcUse.extend(['']*len(df))
        casN.extend(df.loc[:,4])
        prodID.extend(['1400348']*len(df))
        templateName.extend(['Arizona 2012 Pesticide Report Table 4.pdf']*len(df))
        msdsDate.extend([2012]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 22: #Table 5
        chems = [x.replace('\n','') for x in list(df.loc[:,0])]
        chemName.extend(chems)
        funcs = df.loc[:,1]
        funcUse.extend(df.loc[:,1])
        casN.extend(['']*len(df))
        prodID.extend(['1400349']*len(df))
        templateName.extend(['Arizona 2012 Pesticide Report Table 5.pdf']*len(df))
        msdsDate.extend([2012]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    elif i <= 27: #Table 6
        chemName.extend(df.loc[:,5])
        funcUse.extend(df.loc[:,1].map(funcDict))
        casN.extend(['']*len(df))
        prodID.extend(['1400350']*len(df))
        templateName.extend(['Arizona 2012 Pesticide Report Table 6.pdf']*len(df))
        msdsDate.extend([2012]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        chemDetect.extend(['']*len(df))
    i+=1

tables2 = (camelot.read_pdf(pdf,pages='34-43', flavor='stream'))
k=0
for table in tables2: #Table 7
    df = tables2[k].df
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    df = df.drop(df.index[0])
    chemName.extend(df.loc[:,6])
    funcUse.extend(df.loc[:,2])
    casN.extend(['']*len(df))
    prodID.extend(['1400351']*len(df))
    templateName.extend(['Arizona 2012 Pesticide Report Table 7.pdf']*len(df))
    msdsDate.extend([2012]*len(df))
    recUse.extend(['']*len(df))
    catCode.extend(['']*len(df))
    descrip.extend(['']*len(df))
    code.extend(['']*len(df))
    sourceType.extend(['ACToR Assays and Lists']*len(df))
    chemDetect.extend(['']*len(df))
    k+=1
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
        chemName[j] = chemName[j].split('*')[0]
    if chemName[j] == 'salt':
        chemName[j-1] = chemName[j-1] + ' salt'
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
    if chemName[j] == '1_2_3-':
        chemName[j+1] = '1_2_3-' + chemName[j+1]
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
    if chemName[j].lower().strip() == 'd-alanine_ n-(2_6-':
        chemName[j+3] = 'd-alanine_ n-(2_6-dimethylphenyl)-n-(methoxyacetyl)-_methyl ester'
        funcUse[j+3] = 'fungicide'
        del chemName[j:j+3]
        del funcUse[j:j+3]
        del casN[j:j+3]
        del prodID[j:j+3]
        del templateName[j:j+3]
        del msdsDate[j:j+3]
        del recUse[j:j+3]
        del catCode[j:j+3]
        del descrip[j:j+3]
        del code[j:j+3]
        del sourceType[j:j+3]
        del chemDetect[j:j+3]
    if 'd-alanine_ n-(2_6-' in chemName[j].lower().strip():
        chemName[j] = 'd-alanine_ n-(2_6-dimethylphenyl)-n-(methoxyacetyl)-_methyl ester'
        funcUse[j] = 'fungicide'
    if chemName[j].lower().strip() == 'benzoic acid_ 3_6-dichloro-2-':
        chemName[j+2] = 'benzoic acid_ 3_6-dichloro-2-methoxy-_ compd with 2-(2-aminoethoxy)ethanol (1:1)'
        funcUse[j+2] = 'herbicide'
        del chemName[j:j+2]
        del funcUse[j:j+2]
        del casN[j:j+2]
        del prodID[j:j+2]
        del templateName[j:j+2]
        del msdsDate[j:j+2]
        del recUse[j:j+2]
        del catCode[j:j+2]
        del descrip[j:j+2]
        del code[j:j+2]
        del sourceType[j:j+2]
        del chemDetect[j:j+2]
    if chemName[j].lower().strip() == 'ammonium salt of (+/-)-2-':
        chemName[j+3] = 'ammonium salt of (+/-)-2-(4_5-dihydro-4-methyl-4-(1-methylethyl)-5-oxo-1h-imidazol-2-yl)-5-ethyl-3-pyridinecarboxylic acid'
        funcUse[j+3] = 'herbicide'
        del chemName[j:j+3]
        del funcUse[j:j+3]
        del casN[j:j+3]
        del prodID[j:j+3]
        del templateName[j:j+3]
        del msdsDate[j:j+3]
        del recUse[j:j+3]
        del catCode[j:j+3]
        del descrip[j:j+3]
        del code[j:j+3]
        del sourceType[j:j+3]
        del chemDetect[j:j+3]
    if chemName[j].lower().strip() == '1_2_4-triazin-3(2h)-one_ 4_5-':
        chemName[j+3] = '1_2_4-triazin-3(2h)-one_ 4_5-dihydro-6-methyl-4-{(3-pyridinylmethylene)amino}-_(e)-'
        funcUse[j+3] = 'insecticide'
        del chemName[j:j+3]
        del funcUse[j:j+3]
        del casN[j:j+3]
        del prodID[j:j+3]
        del templateName[j:j+3]
        del msdsDate[j:j+3]
        del recUse[j:j+3]
        del catCode[j:j+3]
        del descrip[j:j+3]
        del code[j:j+3]
        del sourceType[j:j+3]
        del chemDetect[j:j+3]
    if chemName[j].lower().strip() == '1_2_3-benzothiadiazole-7-':
        chemName[j+2] = '1_2_3-benzothiadiazole-7-carbothioic acid_ s-methyl ester'
        funcUse[j+2] = 'fungicide'
        del chemName[j:j+2]
        del funcUse[j:j+2]
        del casN[j:j+2]
        del prodID[j:j+2]
        del templateName[j:j+2]
        del msdsDate[j:j+2]
        del recUse[j:j+2]
        del catCode[j:j+2]
        del descrip[j:j+2]
        del code[j:j+2]
        del sourceType[j:j+2]
        del chemDetect[j:j+2]
    if chemName[j].lower().strip() == 'methoxy-_ compd with 2-(2-':
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
    if chemName[j].lower().strip() == 'methanone_ [3-(4_5-dihydro-':
        chemName[j+4] = 'methanone_ [3-(4_5-dihydro-3-isoxazolyl)-2-methyl-4-(methylsulfonyl)phenyl](5-hydroxy-1-methyl-1h-pyrazol-4-yl)-'
        funcUse[j+4] = 'herbicide'
        del chemName[j:j+4]
        del funcUse[j:j+4]
        del casN[j:j+4]
        del prodID[j:j+4]
        del templateName[j:j+4]
        del msdsDate[j:j+4]
        del recUse[j:j+4]
        del catCode[j:j+4]
        del descrip[j:j+4]
        del code[j:j+4]
        del sourceType[j:j+4]
        del chemDetect[j:j+4]
    if chemName[j].lower().strip() == 'benzamide_ 2-chloro-5-[3_6-':
        chemName[j+5] = 'benzamide_ 2-chloro-5-[3_6-dihydro-3-methyl-2_6-dioxo-4-(trifluoromethyl)-1(2h)-pyrimidinyl]-4-fluoro-n-[[methyl(1-methylethyl)amino]sulfonyl]-'
        funcUse[j+5] = 'herbicide'
        del chemName[j:j+5]
        del funcUse[j:j+5]
        del casN[j:j+5]
        del prodID[j:j+5]
        del templateName[j:j+5]
        del msdsDate[j:j+5]
        del recUse[j:j+5]
        del catCode[j:j+5]
        del descrip[j:j+5]
        del code[j:j+5]
        del sourceType[j:j+5]
        del chemDetect[j:j+5]
    chemName[j] = chemName[j].lower()
    chemName[j] = chemName[j].strip()
    funcUse[j] = funcUse[j].lower()
    funcUse[j] = funcUse[j].strip()
    j-=1
# %%
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType, 'chem_detected_flag':chemDetect})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\hortonm\APR\2012\Arizona 2012 Pesticides Annual Report.csv',index=False, header=True, date_format=None)