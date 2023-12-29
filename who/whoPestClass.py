import camelot
import pandas as pd
import os
import re

chemName = []
casN= []
templateName = []
funcUse = []
docID = []
os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/who pest class')

tables = (camelot.read_pdf(r'whopestclass1.pdf',pages='18-40', flavor='stream')) 

i=-1
for table in tables: 
    i+=1
    df = table.df
    if i==2: df[['CAS no', 'UN no']] = df[1].str.split('  ', expand=True)
    if i==0: #table 1
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,5])
        templateName.extend(['whopestclass1.pdf']*n)
        docID.extend(['1690321']*n)
    elif i==2: #table 2
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,4])
        templateName.extend(['whopestclass2.pdf']*n)
        docID.extend(['1690322']*n)
    elif i==3: #table 2
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,5])
        templateName.extend(['whopestclass2.pdf']*n)
        docID.extend(['1690322']*n)
    elif i in [5,7]: #table 3
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,4])
        templateName.extend(['whopestclass3.pdf']*n)
        docID.extend(['1690323']*n)
    elif i in [6,8]: #table 3
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,5])
        templateName.extend(['whopestclass3.pdf']*n)
        docID.extend(['1690323']*n)
    elif i in [10]: #table 4
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,4])
        templateName.extend(['whopestclass4.pdf']*n)
        docID.extend(['1690324']*n)
    elif i in [11,12,13]: #table 4
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,5])
        templateName.extend(['whopestclass4.pdf']*n)
        docID.extend(['1690324']*n)
    elif i in [15,16,18,19,20]: #table 5
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        funcUse.extend(df.iloc[:,4])
        templateName.extend(['whopestclass5.pdf']*n)
        docID.extend(['1690325']*n)
    elif i in [17]: #table 5
        n=len(df.iloc[:,0])
        chemName.extend(df.iloc[:,0])
        casN.extend(df.iloc[:,1])
        temp = df.iloc[:,3]
        for t in temp:
            t = re.sub(' +', ' ', t)
            if len(t.split(' '))>1:
                funcUse.append(t.split(' ')[1])
            else: 
                funcUse.append('')             
        templateName.extend(['whopestclass5.pdf']*n)
        docID.extend(['1690325']*n)
        
n = len(chemName) 
while n > 0: #Go backwards through chemical name list so that the indexing does not get messed up when one is deleted
    n-=1
    chemName[n] = chemName[n].split('[')[0].strip()
    casN[n] = casN[n].strip().split('\n')[0].split(' ')[0]
    if (chemName[n] == '' and casN[n]=='') or chemName[n] == 'Common name' or 'able' in casN[n].lower():
        del chemName[n]
        del casN[n]
        del templateName[n]
        del funcUse[n]
        del docID[n]
        continue
    funcUse[n] = funcUse[n].lower().split('-')[0].strip()
    if funcUse[n] == '': pass
    else: uses = funcUse[n].split(',')
    funcUse[n] = ''
    for use in uses:
        use=use.replace('oil','').replace('dogs','').replace('cats','').strip()
        if 'rp (' in use: use = use.replace('rp','repellant')
        elif use == 'rp': use = 'repellant'
        elif use == 'ac': use = 'acaricide'
        elif use == 'ap': use = 'aphicide'
        elif use == 'b': use = 'bacteriostat'
        elif use == 'fm': use = 'fumigant'
        elif use == 'f' or use == 'fst': use = 'fungicide'
        elif use == 'h': use = 'herbicide'
        elif use == 'i': use = 'insecticide'
        elif use == 'igr': use = 'insect growth regulator'
        elif use == 'ix': use = 'ixodicide (for tick control)'
        elif use == 'l': use = 'larvicide'
        elif use == 'm': use = 'molluscicide'
        elif use == 'mt': use = 'miticide'
        elif use == 'n': use = 'nematocide'
        elif use == 'o': use = 'other use for plant pathogens'
        elif use == 'pgr': use = 'plant growth regulator'
        elif use == 'r': use = 'rodenticide'
        elif use == 'sy': use = 'synergist'
        else: print(use)
        funcUse[n]=(funcUse[n]+';'+use).strip('; ')
        
    
nIngredients = len(chemName)
msdsDate = ['2005']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
component = ['']*nIngredients 
detected = ['']*nIngredients 
author = ['']*nIngredients 
doi = ['']*nIngredients 


df = pd.DataFrame({'data_document_id':docID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType, 'component':component, 'chem_detected_flag':detected, 'author':author, 'doi':doi})
df=df.drop_duplicates()
df.to_csv(r'who pesticide classifications.csv',index=False, header=True)
