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
dfB = tb.read_pdf(pdfPath + "document_1374746.pdf", pages = "49", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfB = pd.concat(dfB)
dfB2 = tb.read_pdf(pdfPath + "document_1374746.pdf", pages = "50-122", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfB2 = pd.concat(dfB2)
dfB = dfB.append(dfB2, sort=False)
del dfB2
dfB = dfB.reset_index(drop=True)
dfB = dfB.loc[:4506]

# Appendix C Distribution of Residues by Pesticide in Soybeans
dfC = tb.read_pdf(pdfPath + "document_1374747.pdf", pages = "124", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfC = pd.concat(dfC)
dfC2 = tb.read_pdf(pdfPath + "document_1374747.pdf", pages = "125-126", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfC2 = pd.concat(dfC2)
dfC = dfC.append(dfC2, sort=False)
del dfC2
dfC = dfC.reset_index(drop=True)
dfC = dfC.loc[:103]

# Appendix D Distribution of Residues by Pesticide in Eggs
dfD = tb.read_pdf(pdfPath + "document_1374748.pdf", pages = "128", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfD = pd.concat(dfD)
dfD2 = tb.read_pdf(pdfPath + "document_1374748.pdf", pages = "129-130", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfD2 = pd.concat(dfD2)
dfD = dfD.append(dfD2, sort=False)
del dfD2
dfD = dfD.reset_index(drop=True)
dfD = dfD.loc[:99]

# Appendix E Distribution of Residues by Pesticide in Milk
dfE = tb.read_pdf(pdfPath + "document_1374749.pdf", pages = "132", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfE = pd.concat(dfE)
dfE2 = tb.read_pdf(pdfPath + "document_1374749.pdf", pages = "133-136", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfE2 = pd.concat(dfE2)
dfE = dfE.append(dfE2, sort=False)
del dfE2
dfE = dfE.reset_index(drop=True)
dfE = dfE.loc[:197]

# Appendix F Distribution of Residues by Pesticide in Groundwater
dfF = tb.read_pdf(pdfPath + "document_1374750.pdf", pages = "138", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfF = pd.concat(dfF)
dfF2 = tb.read_pdf(pdfPath + "document_1374750.pdf", pages = "139-151", stream = True, multiple_tables = True, guess = False)
dfF2 = pd.concat(dfF2)
dfF = dfF.append(dfF2, sort=False)
del dfF2
dfF = dfF.reset_index(drop=True)
dfF = dfF.loc[:569]

# Appendix G Distribution of Residues by Pesticide in Drinking Water
dfG = tb.read_pdf(pdfPath + "document_1374751.pdf", pages = "153", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfG = pd.concat(dfG)
dfG2 = tb.read_pdf(pdfPath + "document_1374751.pdf", pages = "154-164", stream = True, multiple_tables = True, guess = False)
dfG2 = pd.concat(dfG2)
dfG = dfG.append(dfG2, sort=False)
del dfG2
dfG = dfG.reset_index(drop=True)
dfG = dfG.loc[:578]

# Appendix H Distribution of Residues for Environmental Contaminants
dfH = tb.read_pdf(pdfPath + "document_1374752.pdf", pages = "166", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfH = pd.concat(dfH)
dfH2 = tb.read_pdf(pdfPath + "document_1374752.pdf", pages = "167-171", stream = True, multiple_tables = True, guess = False, encoding = 'cp1252')
dfH2 = pd.concat(dfH2)
dfH = dfH.append(dfH2, sort=False)
del dfH2
dfH = dfH.reset_index(drop=True)
dfH = dfH.loc[:367]

# Appendix J Import Versus Domestic Pesticide Residue Comparisons
#page 176 - Snap Peas
#page 177 - Cherry Tomatoes
#page 178 - Hot Peppers
#page 179 - Sweet Bell Peppers


dfJ1 = tb.read_pdf(pdfPath + "document_1374753.pdf", pages = "176", stream = True,  multiple_tables = False, guess = False, area = [138.0, 50.0, 735.0, 565.0])
dfJ1 = dfJ1.dropna(axis='columns', how='all')
dfJ1.columns = ['0', '1', '2', '3']

dfJ2 = tb.read_pdf(pdfPath + "document_1374753.pdf", pages = "177", stream = True,  multiple_tables = False, guess = False, area = [110.0, 50.0, 740.0, 565.0])
dfJ2.columns = ['0', '1', '2', '3', '4']

dfJ3 = tb.read_pdf(pdfPath + "document_1374753.pdf", pages = "178", stream = True,  multiple_tables = False, guess = False, area = [110.0, 50.0, 740.0, 565.0])
dfJ3.columns = ['0', '1', '2', '3', '4']

dfJ4 = tb.read_pdf(pdfPath + "document_1374753.pdf", pages = "179", stream = True,  multiple_tables = False, guess = False, area = [110.0, 50.0, 740.0, 565.0])
dfJ4.columns = ['0', '1', '2', '3', '4']

# Appendix K Pesticide Residues by Commodity is pages 181-185
dfK = tb.read_pdf(pdfPath + "document_1374754.pdf", pages = "181", stream = True,  multiple_tables = True, guess = True, area = [93.0, 47.5, 720.0, 588.0])
dfK = pd.concat(dfK)
dfK.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfK1 = tb.read_pdf(pdfPath + "document_1374754.pdf", pages = "182-185", stream = True, multiple_tables = False, guess = True)
dfK1.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfK = dfK.append(dfK1, sort=False)
del dfK1
dfK = dfK.reset_index(drop=True)

# Appendix M Samples Reported to the U.S. Food and Drug Administration as Exceeding the Tolerance or Without Established Tolerance is p 191, 192-194
dfM1 = tb.read_pdf(pdfPath + "document_1374755.pdf", pages = "191", stream = True,  multiple_tables = True, guess = False, area = [126.0, 35.0, 735.0, 563.0])
dfM1 = pd.concat(dfM1)
dfM2 = tb.read_pdf(pdfPath + "document_1374755.pdf", pages = "192", stream = True,  multiple_tables = True, guess = False, area = [86.0, 35.0, 735.0, 563.0])
dfM2 = pd.concat(dfM2)
dfM2.columns = ['0', '1', '2', '3', '4', '5', '6']
dfM3 = tb.read_pdf(pdfPath + "document_1374755.pdf", pages = "193-194", stream = True, multiple_tables = False, guess = True)
dfM3.columns = ['0', '1', '2', '3', '4', '5', '6']
dfM2 = dfM2.append(dfM3, sort=False)
del dfM3
dfM2 = dfM2.reset_index(drop=True)

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
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
            
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

prod = 'Soybeans'
for index, row in dfC.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[1]) == True or 'Pesticide' in row[0] :
            pass

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
            elif row[1] == 'P':
                func = 'plant growth regulator'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            elif row[1] == 'S':
                func = 'herbicide safener'
            else: func = ''
            

            
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
            
    except:
        pass

# Fixing a couple of chemicals
chemicals[:] = [chem if 'R157836' not in chem else 'Cyhalothrin, Total (Cyhalothrin-L + R157836 epimer)' for chem in chemicals]
chemicals[:] = [chem if 'Tralomethrin)' not in chem else 'Deltamethrin (includes parent Tralomethrin)' for chem in chemicals]
chemicals[:] = [chem.rstrip('*') for chem in chemicals]
        
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

prod = 'Eggs'


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
            elif row[1] == 'H':
                func = 'herbicide'
            elif row[1] == 'I':
                func = 'insecticide'
            elif row[1] == 'IM':
                func = 'insecticide metabolite'
            elif row[1] == 'S':
                func = 'herbicide safener'
            else: func = ''
        
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
        
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

prod = 'Milk'


for index, row in dfE.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass
        else:
            #get the chemicals
            chem = row[0]
                    
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
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
        
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
            else: pass
            
        if pd.isna(row[3]) == False:
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
            
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
            elif func == 'H':
                func = 'herbicide'
            elif func == 'HM':
                func = 'herbicide metabolite'
            elif func == 'I':
                func = 'insecticide'
            elif func == 'IM':
                func = 'insecticide metabolite'
            elif func == 'P':
                func = 'Plant growth Regulator'
            else: pass
            
        if pd.isna(row[3]) == False:
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
            
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
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
            
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
#page 176 - Snap Peas
#page 177 - Cherry Tomatoes
#page 178 - Hot Peppers
#page 179 - Sweet Bell Peppers

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Snap Peas'
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
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
                
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

prod = 'Cherry Tomatoes'
func = ''

for index, row in dfJ2.iterrows():
    try:
        if 'Pesticide' in row[0] or "NOTE" in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
                
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

prod = 'Hot Peppers'
func = ''

for index, row in dfJ3.iterrows():
    try:
        if 'Pesticide' in row[0] or "NOTE" in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
                
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

prod = 'Sweet Bell Peppers'
func = ''

for index, row in dfJ4.iterrows():
    try:
        if 'Pesticide' in row[0] or "NOTE" in row[0] or pd.isna(row[0]) == True : #skip rows that have "Pesticide" or "NOTE" in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
                
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
        
        elif '-Naphthol' in row[0]:
            chem = '1-Naphthol'
            
        elif 'Permethrin' in row[0]:
            chem = 'Permethrin'
        
        elif 'Sweet Bell Peppers' in row[0] :
            prod = 'Sweet Bell Peppers'
        
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
                pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')   
    
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
        pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')
        
        
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
#        
#        elif 'methyl sulfide 7' in row[0]:
#            chem = 'Pentachlorophenyl methyl sulfide'
#        
#        elif 'Fenamiphos' in row[0]:
#            chem = 'Fenamiphos'
#            
#        elif 'Permethrin' in row[0]:
#            chem = 'Permethrin'
        
        elif pd.isna(row[1]) == True and row[0][0].isdigit() == True :
            prod = row[0].rsplit('(',1)[0].strip(' 0123456789')
        else :
            chem = row[0].rstrip(' 0123456789')
            
            products.append(prod.rstrip(' '))
            functions.append(func)
            chemicals.append(chem)
            pdflist.append('2011 ' + prod.rstrip(' ') + '.pdf')   
        
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

    elif 'Deltamethrin  (includes parent Tralomethrin)' in s:
        s = 'Deltamethrin (includes parent Tralomethrin)'
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
    title = '2011 Pesticide Residues in ' + s.replace('/','-')
    titles.append(title)
document_type = ['FG']*length
url = ['https://www.ams.usda.gov/sites/default/files/media/2011%20PDP%20Annual%20Summary.pdf']*length
organization = ['USDA']*length

dfrr = pd.DataFrame({'filename':fullpdflist, 'title':titles, 'document_type':document_type, 'url':url, 'organization':organization}) 
dfrr=dfrr.drop_duplicates()

#dfrr.to_csv(csvPath + "RR-PDPASR2011.csv",index=False, header=True)

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
#path = r'C:\Users\mhorton\Documents\extscr\PDPASR\PDPASR2011\pdfs' #Folder doc is in
#os.chdir(path)    
#template = csv.reader(open('usda_pdpasr_2011_registered_documents.csv')) #Register Records template
#i=0
#for row in template:
#    i+=1
#    if i == 1: continue
#    try:
#        oldPath = path + '\\' + 'document_1374746.pdf' #Original doc name
#        newPath = path + '\\matchingdocs\\' + row[1]
#        copyfile(oldPath,newPath)
#    except: print('halp!', row[0])

# %% create the CSV for upload
length = len(fullproducts)
docDate = ['February 2013']*length
rawCat = fullproducts
rawCas = ['']*length
catCode = ['']*length
desc = ['']*length
cpcatCode = ['']*length
cpcatSource = ['']*length
fulldocNumber = ['']*length

#create a dictionary of doc IDs from the RRs
dftemp = pd.read_csv(csvPath + 'usda_pdpasr_2011_registered_documents.csv')
dftemp = dftemp[['DataDocument_id','filename']]
dftemp = dftemp.set_index('filename').T.to_dict('list')

df = pd.DataFrame({'data_document_id':fulldocNumber, 'data_document_filename':fullpdflist, 'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':rawCas, 'raw_chem_name':fullchemicals, 'report_funcuse':fullfunctions, 'cat_code':catCode, 'description_cpcat':desc, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource})
df=df.drop_duplicates()
df['data_document_id'] = df.data_document_filename.replace(dftemp) #get doc IDs from template dictionary
    
#df.to_csv(csvPath + "USDA-PDPASR2011.csv",index=False, header=True)
