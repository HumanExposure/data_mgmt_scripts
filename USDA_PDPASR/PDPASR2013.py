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
dfB = tb.read_pdf(pdfPath + "document_1374771.pdf", pages = "45", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfB = pd.concat(dfB)
dfB2 = tb.read_pdf(pdfPath + "document_1374771.pdf", pages = "46-120", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfB2 = pd.concat(dfB2)
dfB = dfB.append(dfB2, sort=False)
del dfB2
dfB = dfB.reset_index(drop=True)
dfB = dfB.loc[:4812]

# Appendix C Distribution of Residues by Pesticide in Infant Formula
dfC = tb.read_pdf(pdfPath + "document_1374772.pdf", pages = "123", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfC = pd.concat(dfC)
dfC2 = tb.read_pdf(pdfPath + "document_1374772.pdf", pages = "124-137", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfC2 = pd.concat(dfC2)
dfC = dfC.append(dfC2, sort=False)
del dfC2
dfC = dfC.reset_index(drop=True)
dfC = dfC.loc[:840]

# Appendix D Distribution of Residues by Pesticide in Butter
dfD = tb.read_pdf(pdfPath + "document_1374773.pdf", pages = "140", stream = True,  multiple_tables = True, guess = False, area = [74.0, 35.5, 739.0, 563.0])
dfD = pd.concat(dfD)
dfD2 = tb.read_pdf(pdfPath + "document_1374773.pdf", pages = "141-143", stream = True, multiple_tables = True, guess = False, area = [51.0, 35.5, 739.0, 563.0])
dfD2 = pd.concat(dfD2)
dfD = dfD.append(dfD2, sort=False)
del dfD2
dfD = dfD.reset_index(drop=True)
dfD = dfD.loc[:186]

# Appendix E Distribution of Residues by Pesticide in Salmon
dfE = tb.read_pdf(pdfPath + "document_1374774.pdf", pages = "145", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfE = pd.concat(dfE)
dfE2 = tb.read_pdf(pdfPath + "document_1374774.pdf", pages = "146-149", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfE2 = pd.concat(dfE2)
dfE = dfE.append(dfE2, sort=False)
del dfE2
dfE = dfE.reset_index(drop=True)
dfE = dfE.loc[:203]

# Appendix F Distribution of Residues by Pesticide in Groundwater
dfF = tb.read_pdf(pdfPath + "document_1374775.pdf", pages = "151", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfF = pd.concat(dfF)
dfF2 = tb.read_pdf(pdfPath + "document_1374775.pdf", pages = "152-161", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfF2 = pd.concat(dfF2)
dfF = dfF.append(dfF2, sort=False)
del dfF2
dfF = dfF.reset_index(drop=True)
dfF = dfF.loc[:589]

# Appendix G Distribution of Residues by Pesticide in Drinking Water
dfG = tb.read_pdf(pdfPath + "document_1374776.pdf", pages = "163", stream = True,  multiple_tables = True, guess = False, area = [74.0, 10, 739.0, 563.0])
dfG = pd.concat(dfG)
dfG2 = tb.read_pdf(pdfPath + "document_1374776.pdf", pages = "164-173", stream = True, multiple_tables = True, guess = False, area = [51.0, 10, 739.0, 563.0])
dfG2 = pd.concat(dfG2)
dfG = dfG.append(dfG2, sort=False)
del dfG2
dfG = dfG.reset_index(drop=True)
dfG = dfG.loc[:658]

# Appendix H Distribution of Residues for Environmental Contaminants 
dfH = tb.read_pdf(pdfPath + "document_1374777.pdf", pages = "175", stream = True,  multiple_tables = False, guess = False, area = [74.0, 10, 739.0, 563.0])
dfH1 = tb.read_pdf(pdfPath + "document_1374777.pdf", pages = "176-181", stream = True,  multiple_tables = False, guess = False, area = [51.0, 10, 739.0, 563.0])
dfH = dfH.append(dfH1, sort=False)
del dfH1
dfH = dfH.reset_index(drop=True)

# Appendix J Import Versus Domestic Pesticide Residue Comparisons 
#1 - Nectarines
#2 - Raspberries
#3 - Summer Squash
dfJ1 = tb.read_pdf(pdfPath + "document_1374778.pdf", pages = "188", stream = True,  multiple_tables = True, guess = False, area = [135.0, 10, 725.0, 563.0])
dfJ1 = pd.concat(dfJ1)

dfJ2 = tb.read_pdf(pdfPath + "document_1374778.pdf", pages = "189", stream = True,  multiple_tables = True, guess = False, area = [105.0, 10, 725.0, 563.0])
dfJ2 = pd.concat(dfJ2)

dfJ3 = tb.read_pdf(pdfPath + "document_1374778.pdf", pages = "190", stream = True,  multiple_tables = True, guess = False, area = [105.0, 10, 725.0, 563.0])
dfJ3 = pd.concat(dfJ3)

# Appendix K Pesticide Residues by Commodity 
dfK = tb.read_pdf(pdfPath + "document_1374779.pdf", pages = "192", stream = True,  multiple_tables = True, guess = False, area = [94.0, 10, 721.0, 586.0])
dfK = pd.concat(dfK)
dfK1 = tb.read_pdf(pdfPath + "document_1374779.pdf", pages = "193-195", stream = True,  multiple_tables = True, guess = False, area = [51.0, 10, 737.0, 586.0])
dfK1 = pd.concat(dfK1)
dfK = dfK.append(dfK1, sort=False)
del dfK1
dfK = dfK.reset_index(drop=True)
dfK = dfK.loc[:180]

# Appendix M Samples Reported to the U.S. Food and Drug Administration as Exceeding the Tolerance or Without Established Tolerance 
dfM1 = tb.read_pdf(pdfPath + "document_1374780.pdf", pages = "200", stream = True,  multiple_tables = True, guess = False, area = [126.0, 35.0, 735.0, 563.0])
dfM1 = pd.concat(dfM1)

dfM2 = tb.read_pdf(pdfPath + "document_1374780.pdf", pages = "201", stream = True,  multiple_tables = True, guess = False, area = [86.0, 35.0, 735.0, 584.0])
dfM2 = pd.concat(dfM2)
dfM2.columns = ['0', '1', '2', '3', '4', '5', '6']
dfM3 = tb.read_pdf(pdfPath + "document_1374780.pdf", pages = "202", stream = True, multiple_tables = False, guess = True, area = [56.0, 35.0, 735.0, 584.0])
dfM3.columns = ['0', '1', '2', '3', '4', '5', '6']
dfM2 = dfM2.append(dfM3, sort=False)
del dfM3
dfM2 = dfM2.reset_index(drop=True)
dfM2 = dfM2.loc[:92]

# %% Parsing data for upload - Appendix B
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []


for index, row in dfB.iterrows():
    try:
        #skip lines that don't contain chemicals or products, or where there were no detections
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'Pesticide' in row[0] or 'Appendix' in row[0] or row[2] == '0': 
            pass
        #find the chemicals
        elif '(' in row[0] and pd.isna(row[1]): 
            chem = row[0].split('(')[0]
            func = row[0].split('(')[1].strip().strip(')')
        elif '(' in row[1] and pd.isna(row[2]) == True: 
            chem = row[0]
            func = row[1].split('(')[1].strip().strip(')')
        else:
            prod = row[0].rstrip(' 0123456789')
            if '(' in prod :
                prod = prod.split('(')[0]
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
    except:
        pass

functions[:] = [func if 'V-' not in func else '' for func in functions]
functions[:] = [func if 'X-' not in func else '' for func in functions]


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

for index, row in dfC.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Pesticide' in row[0] :
            pass
    
        #get the chemicals
        elif pd.isna(row[1]) == True : 
            chem = row[0].rsplit('(',1)[0].strip()
            func = row[0].rsplit('(',1)[1].strip(') ')
            
            if func == 'A':
                func = 'acaricide'
            elif func == 'F':
                func = 'fungicide'
            elif func == 'FM':
                func = 'fungicide metabolite'
            elif func == 'H':
                func = 'herbicide'
            elif func == 'HM':
                func = 'herbicide metabolite'
            elif func == 'I':
                func = 'insecticide'
            elif func == 'IM':
                func = 'insecticide metabolite'
            elif func == 'L':
                func = 'plant activator'
            elif func == 'P':
                func = 'plant growth regulator'
            elif func == 'R':
                func = 'insect growth regulator '
            elif func == 'RM':
                func = 'insect growth regulator metabolite'
            elif func == 'S':
                func = 'herbicide safener'
            elif func == 'T':
                func = 'nematicide'
            else: pass
        
        elif 'Dairy' in row[0] :
            prod = 'Infant Formula, Dairy-based'
            if pd.isna(row[2]) == False :
                chemicals.append(chem)
                functions.append(func)
                products.append(prod.rstrip(' '))
                pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
        elif 'Soy' in row[0] :
            prod = 'Infant Formula, Soy-based'
            if pd.isna(row[2]) == False :
                chemicals.append(chem)
                functions.append(func)
                products.append(prod.rstrip(' '))
                pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
            
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

prod = 'Butter'


for index, row in dfD.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass

        #get the chemicals
        else: 
            chem = row[0]
        
            if row[1] == 'A':
                func = 'acaricide'
            elif row[1] == 'F':
                func = 'fungicide'
            elif row[1] == 'FM':
                func = 'fungicide metabolite'
            elif row[1] == 'H':
                func = 'herbicide'
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
            else: pass
            
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
        
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

prod = 'Salmon'


for index, row in dfE.iterrows():
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
            elif row[1] == 'L':
                func = 'plant activator'
            elif row[1] == 'P':
                func = 'plant growth regulator'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'S':
                func = 'herbicide safener'
            else: func = ''
        
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
        
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

prod = 'Groundwater'

for index, row in dfF.iterrows():
    try:
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'NOTES' in row[0] or 'Pesticide' in row[0]: 
            #skip lines that don't contain chemicals, or where there were no detections
            pass
        elif pd.isna(row[1]) == True :
            if '(' in row[0]:
                chem = row[0].rsplit('(',1)[0].strip('* ')
                func = row[0].rsplit('(',1)[1].strip(') ')
            if func == 'F':
                func = 'fungicide'
            elif func == 'FM':
                func = 'fungicide metabolite'
            elif func == 'H':
                func = 'herbicide'
            elif func == 'HM':
                func = 'herbicide metabolite'
            elif func == 'I':
                func = 'insecticide'
            elif func == 'IM':
                func = 'insecticide metabolite'
            elif func == 'T':
                func = 'nematicide'
            else: pass
            
        if pd.isna(row[3]) == False:
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
            
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
#snap peas

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Drinking Water'

for index, row in dfG.iterrows():
    try:
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'NOTES' in row[0] or 'Pesticide' in row[0]: 
            #skip lines that don't contain chemicals, or where there were no detections
            pass
        elif pd.isna(row[1]) == True :
            if '(' in row[0]:
                chem = row[0].rsplit('(',1)[0].strip('* ')
                func = row[0].rsplit('(',1)[1].strip(') ')
            if func == 'F':
                func = 'fungicide'
            elif func == 'FM':
                func = 'fungicide metabolite'
            elif func == 'H':
                func = 'herbicide'
            elif func == 'HM':
                func = 'herbicide metabolite'
            elif func == 'I':
                func = 'insecticide'
            elif func == 'IM':
                func = 'insecticide metabolite'
            elif func == 'T':
                func = 'nematicide'
            else: pass
            
        if pd.isna(row[3]) == False:
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
            
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
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
            
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

# %% Appendix J Import Versus Domestic Pesticide Residue Comparisons 
#1 - Nectarines

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Nectarines'
func = ''

for index, row in dfJ1.iterrows():
    try:
        if 'Pesticide' in row[0]  or 'NOTE' in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
                
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

# %% #2 - Raspberries
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Raspberries'
func = ''

for index, row in dfJ2.iterrows():
    try:
        if 'Pesticide' in row[0]  or 'NOTE' in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
                
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

# %% #3 - Summer Squash
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Summer Squash'
func = ''
for index, row in dfJ3.iterrows():
    try:
        if 'United' in row[1] : 
            chem = row[0]
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
                
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

for index, row in dfK.iterrows():
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
            elif row[1] == 'I':
                func = 'insecticide'
            elif row[1] == 'IM':
                func = 'insecticide metabolite'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            else: func = ''            

            if func != '' :
                products.append(prod.rstrip(' '))
                functions.append(func)
                chemicals.append(chem)
                pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')   
    
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

# %% Parsing data for upload - Appendix M
del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

func = ''

for index, row in dfM1.iterrows():
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
        pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')
        
        
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

for index, row in dfM2.iterrows():
    try:
        if pd.isna(row[0]) == True or 'Commodity' in row[0] or 'NOTES' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass
        
        elif pd.isna(row[1]) == True and row[0][0].isdigit() == True :
            prod = row[0].rsplit('(',1)[0].strip(' 0123456789')
        else :
            chem = row[0].rstrip(' 0123456789')
            
            products.append(prod.rstrip(' '))
            functions.append(func)
            chemicals.append(chem)
            pdflist.append('2013 ' + prod.rstrip(' ') + '.pdf')   
        
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
    title = '2013 Pesticide Residues in ' + s.replace('/','-')
    titles.append(title)
document_type = ['FG']*length
url = ['https://www.ams.usda.gov/sites/default/files/media/2013PDPAnnualSummary.pdf']*length
organization = ['USDA']*length

dfrr = pd.DataFrame({'filename':fullpdflist, 'title':titles, 'document_type':document_type, 'url':url, 'organization':organization}) 
dfrr=dfrr.drop_duplicates()

#dfrr.to_csv(csvPath + "RR-PDPASR2013.csv",index=False, header=True)

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
#path = r'C:\Users\mhorton\Documents\extscr\PDPASR\PDPASR2013\pdfs' #Folder doc is in
#os.chdir(path)    
#template = csv.reader(open('usda_pdpasr_2013_registered_documents.csv')) #Register Records template
#i=0
#for row in template:
#    i+=1
#    if i == 1: continue
#    try:
#        oldPath = path + '\\' + 'document_1374771.pdf' #Original doc name
#        newPath = path + '\\matchingdocs\\' + row[1]
#        copyfile(oldPath,newPath)
#    except: print('halp!', row[0])

# %% create the CSV for upload
length = len(fullproducts)
docDate = ['December 2014']*length
rawCat = fullproducts
rawCas = ['']*length
catCode = ['']*length
desc = ['']*length
cpcatCode = ['']*length
cpcatSource = ['']*length
fulldocNumber = ['']*length

#create a dictionary of doc IDs from the RRs
dftemp = pd.read_csv(csvPath + 'usda_pdpasr_2013_registered_documents.csv')
dftemp = dftemp[['DataDocument_id','filename']]
dftemp = dftemp.set_index('filename').T.to_dict('list')

df = pd.DataFrame({'data_document_id':fulldocNumber, 'data_document_filename':fullpdflist, 'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':rawCas, 'raw_chem_name':fullchemicals, 'report_funcuse':fullfunctions, 'cat_code':catCode, 'description_cpcat':desc, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource})
df=df.drop_duplicates()
df['data_document_id'] = df.data_document_filename.replace(dftemp) #get doc IDs from template dictionary
    
#df.to_csv(csvPath + "USDA-PDPASR2013.csv",index=False, header=True)
