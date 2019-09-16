# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:13:42 2019

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

# Appendix B Distribution of Residues by Pesticide in Fruit and Vegetables
dfB = tb.read_pdf(pdfPath + "document_1374817.pdf", pages = "43", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfB = pd.concat(dfB)
dfB2 = tb.read_pdf(pdfPath + "document_1374817.pdf", pages = "44-155", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfB2 = pd.concat(dfB2)
dfB = dfB.append(dfB2, sort=False)
del dfB2
dfB = dfB.reset_index(drop=True)
dfB = dfB.loc[:6000]

# Appendix C Distribution of Residues by Pesticide in Peanut Butters
dfC = tb.read_pdf(pdfPath + "document_1374818.pdf", pages = "157", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfC = pd.concat(dfC)
dfC2 = tb.read_pdf(pdfPath + "document_1374818.pdf", pages = "158-159", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfC2 = pd.concat(dfC2)
dfC = dfC.append(dfC2, sort=False)
del dfC2
dfC = dfC.reset_index(drop=True)
dfC = dfC.loc[:109]

# Appendix D Distribution of Residues for Environmental Contaminants 
dfD = tb.read_pdf(pdfPath + "document_1374819.pdf", pages = "161", stream = True,  multiple_tables = False, guess = False, area = [74.0, 10, 739.0, 563.0])
dfD1 = tb.read_pdf(pdfPath + "document_1374819.pdf", pages = "162-167", stream = True,  multiple_tables = False, guess = False, area = [51.0, 10, 739.0, 563.0])
dfD = dfD.append(dfD1, sort=False)
del dfD1
dfD = dfD.reset_index(drop=True)
dfD = dfD.loc[:366]

# Appendix F Import Versus Domestic Pesticide Residue Comparisons 
#1 - Grapes
#2 - Nectarines
#3 - Tomatoes
dfF1 = tb.read_pdf(pdfPath + "document_1374820.pdf", pages = "172", stream = True,  multiple_tables = True, guess = False, area = [135.0, 10, 725.0, 563.0])
dfF1= pd.concat(dfF1)
dfF2 = tb.read_pdf(pdfPath + "document_1374820.pdf", pages = "173", stream = True,  multiple_tables = True, guess = False, area = [135.0, 10, 725.0, 563.0])
dfF2= pd.concat(dfF2)
dfF3 = tb.read_pdf(pdfPath + "document_1374820.pdf", pages = "174", stream = True,  multiple_tables = True, guess = False, area = [106.0, 10, 725.0, 563.0])
dfF3= pd.concat(dfF3)

# Appendix G Pesticide Residues by Commodity 
dfG = tb.read_pdf(pdfPath + "document_1374821.pdf", pages = "176", stream = True,  multiple_tables = True, guess = False, area = [94.0, 10, 721.0, 586.0])
dfG = pd.concat(dfG)
dfG1 = tb.read_pdf(pdfPath + "document_1374821.pdf", pages = "177-183", stream = True,  multiple_tables = True, guess = False, area = [51.0, 10, 737.0, 586.0])
dfG1 = pd.concat(dfG1)
dfG = dfG.append(dfG1, sort=False)
del dfG1
dfG = dfG.reset_index(drop=True)
dfG = dfG.loc[:388]

# Appendix I Samples Reported to the U.S. Food and Drug Administration as Exceeding the Tolerance or Without Established Tolerance 
dfI1 = tb.read_pdf(pdfPath + "document_1374821.pdf", pages = "188", stream = True,  multiple_tables = True, guess = False,area = [126.0, 35.0, 735.0, 563.0])
dfI1 = pd.concat(dfI1)
dfI2 = tb.read_pdf(pdfPath + "document_1374821.pdf", pages = "189", stream = True,  multiple_tables = True, guess = False, area = [86.0, 35.0, 735.0, 563.0])
dfI2 = pd.concat(dfI2)
dfI1 = dfI1.append(dfI1, sort=False)

dfI2 = tb.read_pdf(pdfPath + "document_1374821.pdf", pages = "190", stream = True,  multiple_tables = True, guess = False, area = [90.0, 53.0, 735.0, 584.0])
dfI2 = pd.concat(dfI2)
dfI2.columns = ['0', '1', '2', '3', '4', '5', '6']
dfI3 = tb.read_pdf(pdfPath + "document_1374821.pdf", pages = "191-192", stream = True, multiple_tables = False, guess = True, area = [56.0, 35.0, 735.0, 584.0])
dfI3.columns = ['0', '1', '2', '3', '4', '5', '6']
dfI2 = dfI2.append(dfI3, sort=False)
del dfI3
dfI2 = dfI2.reset_index(drop=True)
dfI2 = dfI2.loc[:119]

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
        elif '(' in row[0] and pd.isna(row[1]) == True : 
            chem = row[0].split('(')[0]
            func = row[0].split('(')[1].strip().strip(')')
        elif '(' in row[1] and pd.isna(row[2]) == True : 
            chem = row[0]
            func = row[1].split('(')[1].strip().strip(')')
        else:
            prod = row[0].rstrip(' 0123456789')
            if '(' in prod :
                prod = prod.split('(')[0]
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
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

prod = 'Peanut Butter'

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
            elif row[1] == 'S':
                func = 'herbicide safener'
            elif row[1] == 'X':
                func = 'other (insect repellent)'
            else: func = ''
            
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
            
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


for index, row in dfD.iterrows():
    try:
        #skip lines that don't contain chemicals or products, or where there were no detections
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'Pesticide / Commodity' in row[0] or 'Appendix' in row[0] or row[2] == '0': 
            pass
        #find the chemicals
        elif '(' in row[0] and pd.isna(row[2]) == True :
            chem = row[0].split('(')[0]
            func = row[0].split('(')[1].strip().strip(')')
        elif 'cide' in row[2] :
            chem = row[0].split('(')[0]
            func = row[2].split('(')[1].strip().strip(')')
        elif '(' in row[1] and pd.isna(row[2]) == True:
            chem = row[0]
            func = row[1].split('(')[1].strip().strip(')')
        else:
            prod = row[0].split('(')[0].rstrip(' 0123456789')
            
            if ', Total' in chem :
                chem = chem.split(',')[0]
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
            
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

# %% Appendix F Import Versus Domestic Pesticide Residue Comparisons 
#1 - Grapes

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Grapes'
func = ''

for index, row in dfF1.iterrows():
    try:
        if 'Pesticide' in row[0]  or 'NOTE' in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
                
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

# %% #2 - Nectarines
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Nectarines'
func = ''

for index, row in dfF2.iterrows():
    try:
        if 'Pesticide' in row[0]  or 'NOTE' in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
                
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

# %% #3 - Tomatoes
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Tomatoes'
func = ''
for index, row in dfF3.iterrows():
    try:
        if 'United' in row[1] : 
            chem = row[0]
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
                
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

# %% Parsing data for upload - Appendix G
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

for index, row in dfG.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Commodity / Pesticide' in row[0] or 'NOTES' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass
       
        elif pd.isna(row[1]) == True  and '(' in row[0] :
            prod = row[0].split('(')[0].strip(' 0123456789')
            
        else :
            chem = row[0].replace(',','(').split('(')[0].strip(' 0123456789*')
            
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
            elif row[1] == 'L':
                func = 'plant activator'
            elif row[1] == 'P':
                func = 'plant growth regulator'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'S':
                func = 'herbicide safener'
            else: func = ''         

            if func != '' :
                products.append(prod.rstrip(' '))
                functions.append(func)
                chemicals.append(chem)
                pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')   
    
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

# %% Parsing data for upload - Appendix I
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

func = ''

for index, row in dfI1.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Commodity' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass

        #find the products and chemicals
        elif '/' in row[0] :
            prod = row[0].split('/')[0].strip(' 0123456789')
            chem = row[0].split('/')[1].strip(' 0123456789')
        elif '/' in row[1] :
            prod = row[1].split('/')[0].strip(' 0123456789')
            chem = row[1].split('/')[1].strip(' 0123456789')
            #define the functions of the chemicals
        
        else: pass
    
        products.append(prod.rstrip(' '))
        functions.append(func)
        chemicals.append(chem)
        pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')
        
        
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

for index, row in dfI2.iterrows():
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
            pdflist.append('2015 ' + prod.rstrip(' ') + '.pdf')   
        
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
    title = '2015 Pesticide Residues in ' + s.replace('/','-')
    titles.append(title)
document_type = ['FG']*length
url = ['https://www.ams.usda.gov/sites/default/files/media/2015PDPSummary.pdf']*length
organization = ['USDA']*length

dfrr = pd.DataFrame({'filename':fullpdflist, 'title':titles, 'document_type':document_type, 'url':url, 'organization':organization}) 
dfrr=dfrr.drop_duplicates()

#dfrr.to_csv(csvPath + "RR-PDPASR2015.csv",index=False, header=True)

# %% Create PDFs for document matching
#
#"""
#Created on Thu May 23 09:37:47 2019
#​
#@author: ALarger
#"""
##​
#import os, csv
#from shutil import copyfile
##​
#path = r'C:\Users\mhorton\Documents\extscr\PDPASR\PDPASR2015\pdfs' #Folder doc is in
#os.chdir(path)    
#template = csv.reader(open('usda_pdpasr_2015_registered_documents.csv')) #Register Records template
#i=0
#for row in template:
#    i+=1
#    if i == 1: continue
#    try:
#        oldPath = path + '\\' + 'document_1374817.pdf' #Original doc name
#        newPath = path + '\\matchingdocs\\' + row[1]
#        copyfile(oldPath,newPath)
#    except: print('halp!', row[0])

# %% create the CSV for upload
length = len(fullproducts)
docDate = ['November 2016']*length
rawCat = fullproducts
rawCas = ['']*length
catCode = ['']*length
desc = ['']*length
cpcatCode = ['']*length
cpcatSource = ['']*length
fulldocNumber = ['']*length

#create a dictionary of doc IDs from the RRs
dftemp = pd.read_csv(csvPath + 'usda_pdpasr_2015_registered_documents.csv')
dftemp = dftemp[['DataDocument_id','filename']]
dftemp = dftemp.set_index('filename').T.to_dict('list')

df = pd.DataFrame({'data_document_id':fulldocNumber, 'data_document_filename':fullpdflist, 'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':rawCas, 'raw_chem_name':fullchemicals, 'report_funcuse':fullfunctions, 'cat_code':catCode, 'description_cpcat':desc, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource})
df=df.drop_duplicates()
df['data_document_id'] = df.data_document_filename.replace(dftemp) #get doc IDs from template dictionary
    
#df.to_csv(csvPath + "USDA-PDPASR2015.csv",index=False, header=True)
