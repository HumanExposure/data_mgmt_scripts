# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 07:59:23 2019

@author: MHORTON
"""

# %% import packages
import tabula as tb
import pandas as pd

# Set variables
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

# Appendix B Distribution of Residues by Pesticide in Fruit and Vegetables is pages 43-151
dfB = tb.read_pdf(pdfPath + "document_1374822.pdf", pages = "43", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfB = pd.concat(dfB)
dfB2 = tb.read_pdf(pdfPath + "document_1374822.pdf", pages = "44-151", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfB2 = pd.concat(dfB2)
dfB = dfB.append(dfB2, sort=False)
del dfB2
dfB = dfB.reset_index(drop=True)
dfB = dfB.loc[:5849]

# Appendix C Distribution of Residues by Pesticide in Eggs is pages 154-156
dfC = tb.read_pdf(pdfPath + "document_1374823.pdf", pages = "154", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfC = pd.concat(dfC)
dfC2 = tb.read_pdf(pdfPath + "document_1374823.pdf", pages = "155-156", stream = True, multiple_tables = True, guess = False)
dfC2 = pd.concat(dfC2)
dfC = dfC.append(dfC2, sort=False)
del dfC2
dfC = dfC.reset_index(drop=True)
dfC = dfC.loc[:119]

# Appendix D Distribution of Residues by Pesticide in Milk is pages 158-167
dfD = tb.read_pdf(pdfPath + "document_1374824.pdf", pages = "158", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfD = pd.concat(dfD)
dfD2 = tb.read_pdf(pdfPath + "document_1374824.pdf", pages = "159-167", stream = True, multiple_tables = True, guess = False)
dfD2 = pd.concat(dfD2)
dfD = dfD.append(dfD2, sort=False)
del dfD2
dfD = dfD.reset_index(drop=True)
dfD = dfD.loc[:472]

# Appendix E Distribution of Residues for Environmental Contaminants is pages 169-175
dfE = tb.read_pdf(pdfPath + "document_1374825.pdf", pages = "169", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfE = pd.concat(dfE)
dfE2 = tb.read_pdf(pdfPath + "document_1374825.pdf", pages = "170-175", stream = True, multiple_tables = True, guess = False)
dfE2 = pd.concat(dfE2)
dfE = dfE.append(dfE2, sort=False)
del dfE2
dfE = dfE.reset_index(drop=True)
dfE = dfE.loc[:391]

# Appendix G Import Versus Domestic Pesticide Residue Comparisons is pages 180-182
#page 180 - grapes
#page 181 - green beans
#page 182 - tomatoes
dfG1 = tb.read_pdf(pdfPath + "document_1374826.pdf", pages = "180", stream = True,  multiple_tables = False, guess = False, area = [138.0, 50.0, 735.0, 565.0])

dfG2 = tb.read_pdf(pdfPath + "document_1374826.pdf", pages = "181", stream = True,  multiple_tables = False, guess = False, area = [126.0, 50.0, 320.0, 565.0])

dfG3 = tb.read_pdf(pdfPath + "document_1374826.pdf", pages = "182", stream = True,  multiple_tables = False, guess = False, area = [126.0, 50.0, 629.0, 565.0])

# Appendix H Pesticide Residues by Commodity is pages 184-190
dfH = tb.read_pdf(pdfPath + "document_1374827.pdf", pages = "169", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfH = pd.concat(dfH)
dfH2 = tb.read_pdf(pdfPath + "document_1374827.pdf", pages = "170-175", stream = True, multiple_tables = True, guess = False)
dfH2 = pd.concat(dfH2)
dfH = dfH.append(dfH2, sort=False)
del dfH2
dfH = dfH.reset_index(drop=True)
dfH = dfH.loc[:391]

# Appendix J Samples Reported to the U.S. Food and Drug Administration as Exceeding the Tolerance or Without Established Tolerance is p 195-199
dfJ = tb.read_pdf(pdfPath + "document_1374828.pdf", pages = "195", stream = True,  multiple_tables = True, guess = False, area = [126.0, 10, 735.0, 563.0])
dfJ = pd.concat(dfJ)
dfJ2 = tb.read_pdf(pdfPath + "document_1374828.pdf", pages = "196", stream = True,  multiple_tables = True, guess = False)
dfJ2 = pd.concat(dfJ2)
dfJ1 = dfJ.append(dfJ2, sort=False)
del dfJ, dfJ2
dfJ1 = dfJ1.reset_index(drop=True)

dfJ = tb.read_pdf(pdfPath + "document_1374828.pdf", pages = "197", stream = True,  multiple_tables = True, guess = False, area = [94.0, 40, 735.0, 570.0])
dfJ = pd.concat(dfJ)
dfJ2 = tb.read_pdf(pdfPath + "document_1374828.pdf", pages = "198-199", stream = True, multiple_tables = True, guess = False)
dfJ2 = pd.concat(dfJ2)
dfJ2 = dfJ.append(dfJ2, sort=False)
del dfJ
dfJ2 = dfJ2.reset_index(drop=True)
dfJ2 = dfJ2.loc[:100]

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

            if 'Tomatoes  C' in row[0] : #if the mystery tomato appears
                prod = 'Tomatoes  C2629' #make sure it is recorded faithfully p 88    
            
            if ', Total' in chem : 
                chem = chem.split(',')[0]
            
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
            
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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

prod = 'Eggs'

for index, row in dfC.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
        
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
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'S':
                func = 'herbicide safener'
            else: func = ''
            
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
            
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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
        
            if row[1] == 'F':
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
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
        
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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


for index, row in dfE.iterrows():
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
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
                        
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix G
#page 180 - dfG1: grapes
#page 181 - dfG2: green beans
#page 182 - dfG3: tomatoes

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Grapes'
func = ''

for index, row in dfG1.iterrows():
    try:
        if 'Pesticide' in row[0]  or pd.isna(row[0]) == True : #skip rows that have "Pesticide in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
                
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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

prod = 'Green Beans'
func = ''

for index, row in dfG2.iterrows():
    try:
        if 'Pesticide' in row[0]  or pd.isna(row[0]) == True : #skip rows that have "Pesticide in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
                
    except:
        pass
    
#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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

prod = 'Tomatoes'
func = ''

for index, row in dfG3.iterrows():
    try:
        if 'Pesticide' in row[0]  or pd.isna(row[0]) == True : #skip rows that have "Pesticide in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
                
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix H
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

for index, row in dfH.iterrows():
    try:
        #skip lines that don't contain chemicals or products, or where there were no detections
        if pd.isna(row[0]) == True or 'Pesticide / Commodity' in row[0] or 'TOTAL' in row[0] or row[2] == '0' : 
            pass
        #find the chemicals
        elif pd.isna(row[1]) == True and '(' in row[0]:
            chem = row[0].split('(')[0]
            func = row[0].split('(')[1].strip().strip(')')
        
        else:
            prod = row[0].rstrip(' 0123456789')

            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
            
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
dfprods = dfprods.drop_duplicates()

fullchemicals = fullchemicals + chemicals
fullfunctions = fullfunctions + functions
fullproducts = fullproducts + products
fullpdflist = fullpdflist + pdflist

# %% Parsing data for upload - Appendix J
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

func = ''

for index, row in dfJ1.iterrows():
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
        pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')
        
        
    except:
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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

for index, row in dfJ2.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Pesticide' in row[0] or 'NOTES' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass

        elif pd.isna(row[2]) == True and 'pest' in row[0] :
            prod = row[0].rsplit('(',1)[0].strip(' 0123456789')
        elif row[2][0].isdigit() :
            chem = row[0].rstrip(' 0123456789')
            
            products.append(prod.rstrip(' '))
            functions.append(func)
            chemicals.append(chem)
            pdflist.append('2016 ' + prod.rstrip(' ') + '.pdf')   
        
    except: 
        pass

#checking
dfc = pd.DataFrame({'chem':chemicals, 'func':functions, 'prod':products})
dfchems = pd.DataFrame(sorted(chemicals))
dfchems = dfchems.drop_duplicates()
dffuncs = pd.DataFrame(sorted(functions))
dffuncs = dffuncs.drop_duplicates()
dfprods = pd.DataFrame(sorted(products))
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
    fullchemicals.append(s.rstrip(' '))
    
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

# %% Registered Records CSV
length = len(fullproducts)

titles = []
for s in fullproducts:
    title = '2016 Pesticide Residues in ' + s
    titles.append(title)
document_type = ['FG']*length
url = ['https://www.ams.usda.gov/sites/default/files/media/2016PDPAnnualSummary.pdf']*length
organization = ['USDA']*length

dfrr = pd.DataFrame({'filename':fullpdflist, 'title':titles, 'document_type':document_type, 'url':url, 'organization':organization}) 
dfrr=dfrr.drop_duplicates()

#dfrr.to_csv(csvPath + "RR-PDPASR2016.csv",index=False, header=True)

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
#path = r'C:\Users\mhorton\Documents\extscr\PDPASR\PDPASR2016\pdfs' #Folder doc is in
#os.chdir(path)    
#template = csv.reader(open('usda_pdpasr_2016_registered_documents.csv')) #Register Records template
#i=0
#for row in template:
#    i+=1
#    if i == 1: continue
#    try:
#        oldPath = path + '\\' + 'document_1374822.pdf' #Original doc name
#        newPath = path + '\\matchingdocs\\' + row[1]
#        copyfile(oldPath,newPath)
#    except: print('halp!', row[0])

# %% create the CSV for upload
length = len(fullproducts)
docDate = ['February 2018']*length
rawCat = fullproducts
rawCas = ['']*length
catCode = ['']*length
desc = ['']*length
cpcatCode = ['']*length
cpcatSource = ['']*length
fulldocNumber = ['']*length

#create a dictionary of doc IDs from the RRs
dftemp = pd.read_csv(csvPath + 'usda_pdpasr_2016_registered_documents.csv')
dftemp = dftemp[['DataDocument_id','filename']]
dftemp = dftemp.set_index('filename').T.to_dict('list')

df = pd.DataFrame({'data_document_id':fulldocNumber, 'data_document_filename':fullpdflist, 'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':rawCas, 'raw_chem_name':fullchemicals, 'report_funcuse':fullfunctions, 'cat_code':catCode, 'description_cpcat':desc, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource})
df=df.drop_duplicates()
df['data_document_id'] = df.data_document_filename.replace(dftemp) #get doc IDs from template dictionary

#df.to_csv(csvPath + "USDA-PDPASR2016.csv",index=False, header=True)
