# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:13:42 2019

@author: MHORTON
"""

# %% import packages
import tabula as tb
import pandas as pd

#Set variables
pdfPath = 'pdfs/'
csvPath = 'csvs/'

fullchemicals = []
fullfunctions = []
fullproducts = []
fullpdflist = []

chem = ''
func = ''
prod = ''

# %% Parse PDFs

# Appendix B Distribution of Residues by Pesticide in Fruit and Vegetables is pages 45-153
dfB = tb.read_pdf(pdfPath + "document_1374829.pdf", pages = "45", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfB = pd.concat(dfB)
dfB2 = tb.read_pdf(pdfPath + "document_1374829.pdf", pages = "46-153", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfB2 = pd.concat(dfB2)
dfB = dfB.append(dfB2, sort=False)
del dfB2
dfB = dfB.reset_index(drop=True)
dfB = dfB.loc[:5642]

# Appendix C Distribution of Residues by Pesticide in Honey is pages 155-159
dfC = tb.read_pdf(pdfPath + "document_1374830.pdf", pages = "155", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfC = pd.concat(dfC)
dfC2 = tb.read_pdf(pdfPath + "document_1374830.pdf", pages = "156-159", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfC2 = pd.concat(dfC2)
dfC = dfC.append(dfC2, sort=False)
del dfC2
dfC = dfC.reset_index(drop=True)
dfC = dfC.loc[:212]

# Appendix D Distribution of Residues by Pesticide in Milk is pages 161-170
dfD = tb.read_pdf(pdfPath + "document_1374831.pdf", pages = "161", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfD = pd.concat(dfD)
dfD2 = tb.read_pdf(pdfPath + "document_1374831.pdf", pages = "162-170", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfD2 = pd.concat(dfD2)
dfD = dfD.append(dfD2, sort=False)
del dfD2
dfD = dfD.reset_index(drop=True)
dfD = dfD.loc[:449]

# Appendix E Distribution of Residues by Pesticide in Bottled Water is pages 172-175
dfE = tb.read_pdf(pdfPath + "document_1374832.pdf", pages = "172", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfE = pd.concat(dfE)
dfE2 = tb.read_pdf(pdfPath + "document_1374832.pdf", pages = "173-175", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfE2 = pd.concat(dfE2)
dfE = dfE.append(dfE2, sort=False)
del dfE2
dfE = dfE.reset_index(drop=True)
dfE = dfE.loc[:177]

# Appendix F Distribution of Residues for Environmental Contaminants is pages 177-183
dfF = tb.read_pdf(pdfPath + "document_1374833.pdf", pages = "177", stream = True,  multiple_tables = False, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfF1 = tb.read_pdf(pdfPath + "document_1374833.pdf", pages = "178-183", stream = True,  multiple_tables = False, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfF = dfF.append(dfF1, sort=False)
del dfF1
dfF = dfF.reset_index(drop=True)
dfF = dfF.loc[:356]

# Appendix H Import Versus Domestic Pesticide Residue Comparisons is page 189  
dfH = tb.read_pdf(pdfPath + "document_1374834.pdf", pages = "189", stream = True,  multiple_tables = True, guess = False, area = [135.0, 47.5, 725.0, 563.0])
dfH = pd.concat(dfH)

# Appendix I Pesticide Residues by Commodity is p 191-194
dfI = tb.read_pdf(pdfPath + "document_1374835.pdf", pages = "191", stream = True,  multiple_tables = True, guess = False, area = [94.0, 47.5, 721.0, 586.0])
dfI = pd.concat(dfI)
dfI1 = tb.read_pdf(pdfPath + "document_1374835.pdf", pages = "192-194", stream = True,  multiple_tables = True, guess = False, area = [51.0, 47.5, 737.0, 586.0])
dfI1 = pd.concat(dfI1)
dfI = dfI.append(dfI1, sort=False)
del dfI1
dfI = dfI.reset_index(drop=True)
dfI = dfI.loc[:145]

# Appendix K Samples Reported to the U.S. Food and Drug Administration as Exceeding the Tolerance or Without Established Tolerance is p 199-200, 201-202
dfK1 = tb.read_pdf(pdfPath + "document_1374836.pdf", pages = "199", stream = True,  multiple_tables = True, guess = False, area = [126.0, 35.0, 735.0, 563.0])
dfK1 = pd.concat(dfK1)
dfK2 = tb.read_pdf(pdfPath + "document_1374836.pdf", pages = "200", stream = True,  multiple_tables = True, guess = False, area = [86.0, 35.0, 735.0, 563.0])
dfK2 = pd.concat(dfK2)
dfK1 = dfK1.append(dfK1, sort=False)

dfK2 = tb.read_pdf(pdfPath + "document_1374836.pdf", pages = "201", stream = True,  multiple_tables = True, guess = False, area = [86.0, 35.0, 735.0, 584.0])
dfK2 = pd.concat(dfK2)
dfK2.columns = ['0', '1', '2', '3', '4', '5', '6']
dfK3 = tb.read_pdf(pdfPath + "document_1374836.pdf", pages = "202", stream = True, multiple_tables = False, guess = True, area = [56.0, 35.0, 735.0, 584.0])
dfK3.columns = ['0', '1', '2', '3', '4', '5', '6']
dfK2 = dfK2.append(dfK3, sort=False)
del dfK3
dfK2 = dfK2.reset_index(drop=True)
dfK2 = dfK2.loc[:61]

# %% Parsing data for upload - Appendix B
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []


for index, row in dfB.iterrows():
    try:
        #skip lines that don't contain chemicals or products, or where there were no detections
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'Pesticide / Commodity' in row[0] or 'Appendix' in row[0] or row[2] == '0': 
            pass
        #find the chemicals
        elif '(' in row[0]: 
            chem = row[0].split('(')[0]
            func = row[0].split('(')[1].strip().strip(')')
        elif '(' in row[1] and pd.isna(row[2]) == True: 
            chem = row[0]
            func = row[1].split('(')[1].strip().strip(')')
        else:
            prod = row[0].rstrip(' 0123456789')

            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix C
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Honey'

for index, row in dfC.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
        
            if row[1] == 'A':
                func = 'acaricide'
            elif row[1] == 'F':
                func = 'fungicide'
            elif row[1] == 'FM':
                func = 'fungicide metabolite'
            elif row[1] == 'H':
                func = 'herbicide'
            elif row[1] == 'HM':
                func = 'herbicide metabolite'
            elif row[1] == 'I':
                func = 'insecticide'
            elif row[1] == 'IM':
                func = 'insecticide metabolite'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'X':
                func = 'other (insect repellent)'
            else: func = ''
            
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
            
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix D
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Milk'


for index, row in dfD.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
        
            if row[1] == 'A':
                func = 'acaricide'
            elif row[1] == 'F':
                func = 'fungicide'
            elif row[1] == 'FM':
                func = 'fungicide metabolite'
            elif row[1] == 'H':
                func = 'herbicide'
            elif row[1] == 'HM':
                func = 'herbicide metabolite'
            elif row[1] == 'I':
                func = 'insecticide'
            elif row[1] == 'IM':
                func = 'insecticide metabolite'
            elif row[1] == 'N':
                func = 'nitrification inhibitor'
            elif row[1] == 'O':
                func = 'molluscicide'
            elif row[1] == 'P':
                func = 'plant growth regulator'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'S':
                func = 'herbicide safener'
            elif row[1] == 'T':
                func = 'nematicide'
            else: func = ''
        
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
        
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix E
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Bottled Water'


for index, row in dfE.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
        
            if row[1] == 'F':
                func = 'fungicide'
            elif row[1] == 'H':
                func = 'herbicide'
            elif row[1] == 'HM':
                func = 'herbicide metabolite'
            elif row[1] == 'I':
                func = 'insecticide'
            elif row[1] == 'IM':
                func = 'insecticide metabolite'
            elif row[1] == 'L':
                func = 'plant activator'
            elif row[1] == 'O':
                func = 'molluscicide'
            elif row[1] == 'P':
                func = 'plant growth regulator'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'S':
                func = 'herbicide safener'
            else: func = ''
        
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
        
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()
 
fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix F
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []


for index, row in dfF.iterrows():
    try:
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'NOTES' in row[0] or 'Pesticide / Commodity' in row[0] or row[2] == '0': 
            #skip lines that don't contain chemicals or products, or where there were no detections
            pass

        #find the chemicals
        elif (pd.isna(row[1]) == True and '(' in row[0]) :
            chem = row[0].split('(')[0].strip()
            func = row[0].split('(')[1].strip().strip(')')
            
        elif '0' in row[0]: #fix the strangely extracted first page
            prod = row[0].split('0')[0].rstrip(' 0123456789')

                 
        else:
            prod = row[0].rstrip(' 0123456789')

            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
                        
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()
 
fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix H
#snap peas

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Snap Peas'
func = ''

for index, row in dfH.iterrows():
    try:
        if 'Pesticide' in row[0]  or pd.isna(row[0]) == True : #skip rows that have "Pesticide in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
                
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()
 
fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix I
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

for index, row in dfI.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Commodity / Pesticide' in row[0] or 'NOTES' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass
        
        elif pd.isna(row[1]) == True  and '(' in row[0] :
            prod = row[0].split('(')[0].strip(' 0123456789')
            
        else :
            chem = row[0].split('(')[0].rstrip(' 0123456789*')
            
            if 'Total' in chem : 
                chem = chem.split(',')[0].rstrip(' Total')
            
            if row[1] == 'F':
                func = 'fungicide'
            elif row[1] == 'FM':
                func = 'fungicide metabolite'
            elif row[1] == 'H':
                func = 'herbicide'
            elif row[1] == 'I':
                func = 'insecticide'
            elif row[1] == 'IM':
                func = 'insecticide metabolite'
            else: func = ''            

            if func != '' :
                products.append(prod.rstrip(' '))
                functions.append(func)
                chemicals.append(chem)
                pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')   
    
    except: 
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()
 
fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist
# %% Parsing data for upload - Appendix K
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

func = ''

for index, row in dfK1.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Commodity / Pesticide' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass

        #find the products and chemicals
        elif '/' in row[1] :
            prod = row[1].split('/')[0].strip(' 0123456789')
            chem = row[1].split('/')[1].strip(' 0123456789')
        elif '/' in row[0] :
            prod = row[0].split('/')[0].strip(' 0123456789')
            chem = row[0].split('/')[1].strip(' 0123456789')

            #define the functions of the chemicals
        
        else: pass
    
        products.append(prod.rstrip(' '))
        functions.append(func)
        chemicals.append(chem)
        pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')
        
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfc = dfc.drop_duplicates()
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()
 
fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %%
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

func = ''

for index, row in dfK2.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Commodity / Pesticide' in row[0] or 'NOTES' in row[0] or 'Permethrin  (parent) 7' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass
        
        elif pd.isna(row[1]) == True  and '(' in row[0] :
            prod = row[0].split('(')[0].strip(' 0123456789')
            
        else :
            chem = row[0].split('(')[0].rstrip(' 0123456789*')
            
            if 'Permethrin Total' in chem:
                chem = 'Permethrin'
            
            products.append(prod.rstrip(' '))
            functions.append(func)
            chemicals.append(chem)
            pdflist.append('2017 ' + prod.rstrip(' ') + '.pdf')   
        
    except: 
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfc = dfc.drop_duplicates()
dfchems = pd.DataFrame(chemicals)
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(functions)
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(products)
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Verify
oldfullchemicals = fullchemicals
fullchemicals = []

for s in oldfullchemicals:
    if 'Total' in s:
        s = s.rstrip(' Total')
        try:
            s = s.replace(', Total', '')
        except: pass
    elif ' - ' in s:
        s1 = s.split('-')[0].strip(' ')
        s2 = s.split('-')[1].strip(' ')
        s = s1 + ' (' + s2 + ')'
        
    s = s.lower()
    fullchemicals.append(s.rstrip(', 0123456789'))
    
#checking
dfc = pd.DataFrame({'chem':fullchemicals, 'func':fullfunctions, 'prod':fullproducts})

dfchems = fullchemicals
dfchems = pd.DataFrame(sorted(dfchems))
dfchems = dfchems.drop_duplicates()

dffuncs = fullfunctions
dffuncs = pd.DataFrame(sorted(dffuncs))
dffuncs = dffuncs.drop_duplicates()

dfprods = fullproducts
dfprods = pd.DataFrame(sorted(dfprods))
dfprods = dfprods.drop_duplicates()

# %% fix / in filenames
oldfullpdflist = fullpdflist
fullpdflist = []

for s in oldfullpdflist:
    sn = s.replace('/','-')
    fullpdflist.append(sn)

# %% Registered Records CSV
length = len(fullproducts)

titles = []
for s in fullproducts:
    title = '2017 Pesticide Residues in ' + s.replace('/','-')
    titles.append(title)
document_type = ['FG']*length
url = ['https://www.ams.usda.gov/sites/default/files/media/2017PDPAnnualSummary.pdf']*length
organization = ['USDA']*length

dfrr = pd.DataFrame({'filename':fullpdflist, 'title':titles, 'document_type':document_type, 'url':url, 'organization':organization}) 
dfrr=dfrr.drop_duplicates()

#dfrr.to_csv(csvPath + "RR-PDPASR2017.csv",index=False, header=True)

# %% Create PDFs for document matching

#"""
#Created on Thu May 23 09:37:47 2019
#​
#@author: ALarger
#"""
##​
#import os, csv
#from shutil import copyfile
##​
#path = r'C:\Users\mhorton\Documents\extscr\PDPASR\PDPASR2017\pdfs' #Folder doc is in
#os.chdir(path)    
#template = csv.reader(open('usda_pdpasr_2017_registered_documents.csv')) #Register Records template
#i=0
#for row in template:
#    i+=1
#    if i == 1: continue
#    try:
#        oldPath = path + '\\' + 'document_1374829.pdf' #Original doc name
#        newPath = path + '\\matchingdocs\\' + row[1]
#        copyfile(oldPath,newPath)
#    except: print('halp!', row[0])

# %% create the CSV for upload
length = len(fullproducts)
docDate = ['December 2018']*length
rawCat = fullproducts
rawCas = ['']*length
catCode = ['']*length
desc = ['']*length
cpcatCode = ['']*length
cpcatSource = ['']*length
fulldocNumber = ['']*length

#create a dictionary of doc IDs from the RRs
dftemp = pd.read_csv(csvPath + 'usda_pdpasr_2017_registered_documents.csv')
dftemp = dftemp[['DataDocument_id','filename']]
dftemp = dftemp.set_index('filename').T.to_dict('list')

df = pd.DataFrame({'data_document_id':fulldocNumber, 'data_document_filename':fullpdflist, 'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':rawCas, 'raw_chem_name':fullchemicals, 'report_funcuse':fullfunctions, 'cat_code':catCode, 'description_cpcat':desc, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource})
df=df.drop_duplicates()
df['data_document_id'] = df.data_document_filename.replace(dftemp) #get doc IDs from template dictionary
    
#df.to_csv(csvPath + "USDA-PDPASR2017.csv",index=False, header=True)
