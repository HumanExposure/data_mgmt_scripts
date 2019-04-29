# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:13:40 2019

@author: ALarger

Harmonized Tariff Schedule of the United States (2019)
PHARMACEUTICAL APPENDIX TO THE HARMONIZED TARIFF SCHEDULE
"""

import camelot, string
import pandas as pd

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
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

tables = (camelot.read_pdf(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\PA, USITC, WADA, WA, WHO\(2019) Pharmaceutical Appendix to the Harmonized Tariff Schedule\Pharmaceutical Appendix (2019) Table 1.pdf',pages='all', flavor='stream'))
i=0 
for table in tables:
    df = tables[i].df
    if i == 0: pass
    elif i < 68: 
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        prodID.extend(['1372195']*len(df))
        templateName.extend(['Pharmaceutical Appendix (2019) Table 1.pdf']*len(df))
        msdsDate.extend([2019]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        #Second column
        chemName.extend(df.iloc[:,2])
        casN.extend(df.iloc[:,3])
        prodID.extend(['1372195']*len(df))
        templateName.extend(['Pharmaceutical Appendix (2019) Table 1.pdf']*len(df))
        msdsDate.extend([2019]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    elif i < 73:
        chemName.extend(df.iloc[:,0])
        casN.extend(['']*len(df))
        prodID.extend(['1372196']*len(df))
        templateName.extend(['Pharmaceutical Appendix (2019) Table 2.pdf']*len(df))
        msdsDate.extend([2019]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
        #Second column
        chemName.extend(df.iloc[:,1])
        casN.extend(['']*len(df))
        prodID.extend(['1372196']*len(df))
        templateName.extend(['Pharmaceutical Appendix (2019) Table 2.pdf']*len(df))
        msdsDate.extend([2019]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    else:
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        prodID.extend(['1372197']*len(df))
        templateName.extend(['Pharmaceutical Appendix (2019) Table 3.pdf']*len(df))
        msdsDate.extend([2019]*len(df))
        recUse.extend(['']*len(df))
        catCode.extend(['']*len(df))
        descrip.extend(['']*len(df))
        code.extend(['']*len(df))
        sourceType.extend(['ACToR Assays and Lists']*len(df))
    i+=1
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace(',','_').replace(';','_')
    chemName[j] = chemName[j].replace('\n',' ')
    chemName[j] = chemName[j].replace('α','alpha ').replace('β','beta ').replace('γ','gamma ').replace('ω','omega ').replace('δ','delta ')
    chemName[j] = chemName[j].strip()
    chemName[j] = chemName[j].lower()
    chemName[j] = clean(chemName[j])
    if 'table' in chemName[j] or (chemName[j] == '' and casN[j] == '') or 'schedule' in casN[j].lower() or 'schedule' in chemName[j] or 'annotated' in chemName[j] or (chemName[j].isdigit() and casN[j] == '') or ('product' in chemName[j] and 'name' in chemName[j]) or (len(casN[j]) < 5 and chemName[j] == ''):
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
    try:
        if casN[j][-1] == '&':
            casN[j] = casN[j] + ' ' + casN[j+2]
            del casN[j+2]
            del casN[j+1]
            del chemName[j+2]
            del chemName[j]
            del prodID[j]
            del templateName[j]
            del msdsDate[j]
            del recUse[j]
            del catCode[j]
            del descrip[j]
            del code[j]
            del sourceType[j]
            del prodID[j]
            del templateName[j]
            del msdsDate[j]
            del recUse[j]
            del catCode[j]
            del descrip[j]
            del code[j]
            del sourceType[j]
    except: pass
    if chemName[j] == '' and casN[j-1] == '' and casN[j+1] == '':
        chemName[j] = chemName[j-1] + ' ' + chemName[j+1]
        del chemName[j+1]
        del casN[j+1]
        del chemName[j-1]
        del casN[j-1]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
    if casN[j] != '' and casN[j-1] == '' and casN[j+1] == ''  and chemName[j] != '':
        chemName[j] = chemName[j-1] + chemName [j] + chemName[j+1]
        del chemName[j+1]
        del casN[j+1]
        del chemName[j-1]
        del casN[j-1]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
    if chemName[j] == 'compound solution of':
        chemName[j+1] = chemName[j] + chemName[j+1].replace('compound solution of',' ')
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
    if 'intermediate' in chemName[j] or chemName[j] == 'technetium (99m tc) nofetu-':
        chemName[j] = chemName[j] + ' ' + chemName[j+1]
        del chemName[j+1]
        del casN[j+1]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
    if ((')' in chemName[j] and '(' not in chemName[j]) or (']' in chemName[j] and '[' not in chemName[j]) or ('}' in chemName[j] and '{' not in chemName[j])) and casN[j] == '' and casN[j+2] != '' and casN[j-2] != '' and casN[j+1] != '' and casN[j-1] != '':
        chemName[j-1] = chemName[j-1] + ' ' + chemName[j]
        del chemName[j]
        del casN[j]
        del prodID[j]
        del templateName[j]
        del msdsDate[j]
        del recUse[j]
        del catCode[j]
        del descrip[j]
        del code[j]
        del sourceType[j]
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
df.to_csv(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\PA, USITC, WADA, WA, WHO\(2019) Pharmaceutical Appendix to the Harmonized Tariff Schedule\Pharmaceutical Appendix 2019.csv',index=False, header=True)
