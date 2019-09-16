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

# Appendix B Distribution of Residues by Pesticide in Fruit and Vegetables 
dfB = tb.read_pdf(pdfPath + "document_1374736.pdf", pages = "49", stream = True,  multiple_tables = True, guess = False, area = [90.0, 54.0, 739.0, 566.0])
dfB = pd.concat(dfB)
dfB2 = tb.read_pdf(pdfPath + "document_1374736.pdf", pages = "50-125", stream = True, multiple_tables = True, guess = False, area = [44.0, 47.5, 739.0, 563.0])
dfB2 = pd.concat(dfB2)
dfB = dfB.append(dfB2, sort=False)
del dfB2
dfB = dfB.reset_index(drop=True)
dfB = dfB.loc[:4750]

for index, row in dfB.iterrows():
    try:
        if pd.isna(row[2]) == False and pd.isna(row[3]) == False and pd.isna(row[7]) == False : 
            row[1] = row[2]
            row[2] = row[3]
    except: pass

# Appendix C Distribution of Residues by Pesticide in Oats
dfC = tb.read_pdf(pdfPath + "document_1374737.pdf", pages = "127", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfC = pd.concat(dfC)
dfC2 = tb.read_pdf(pdfPath + "document_1374737.pdf", pages = "128-129", stream = True, multiple_tables = True, guess = False)
dfC2 = pd.concat(dfC2)
dfC = dfC.append(dfC2, sort=False)
del dfC2
dfC = dfC.reset_index(drop=True)
dfC = dfC.loc[:82]

# Appendix D Distribution of Residues by Pesticide in Eggs
dfD = tb.read_pdf(pdfPath + "document_1374738.pdf", pages = "131", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfD = pd.concat(dfD)
dfD2 = tb.read_pdf(pdfPath + "document_1374738.pdf", pages = "132-133", stream = True, multiple_tables = True, guess = False)
dfD2 = pd.concat(dfD2)
dfD = dfD.append(dfD2, sort=False)
del dfD2
dfD = dfD.reset_index(drop=True)
dfD = dfD.loc[:100]

# Appendix E Distribution of Residues by Pesticide in Catfish
dfE = tb.read_pdf(pdfPath + "document_1374739.pdf", pages = "135", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfE = pd.concat(dfE)
dfE.columns = ['0', '1', '2', '3', '4', '5', '6', '7']

dfE2 = tb.read_pdf(pdfPath + "document_1374739.pdf", pages = "136", stream = True, multiple_tables = True, guess = False, area = [51.0, 47.5, 739.0, 563.0])
dfE2 = pd.concat(dfE2)
dfE2 = dfE2.dropna(axis='columns', how='all')
dfE2.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfE3 = tb.read_pdf(pdfPath + "document_1374739.pdf", pages = "137-139", stream = True, multiple_tables = True, guess = True, area = [51.0, 47.5, 739.0, 563.0])
dfE3 = pd.concat(dfE3)
dfE3.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfE = dfE.append(dfE2, sort=False)
del dfE2
dfE = dfE.append(dfE3, sort=False)
del dfE3
dfE = dfE.reset_index(drop=True)
dfE = dfE.loc[:191]

# Appendix F Distribution of Residues by Pesticide in Groundwater
dfF = tb.read_pdf(pdfPath + "document_1374740.pdf", pages = "141", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfF = pd.concat(dfF)
dfF2 = tb.read_pdf(pdfPath + "document_1374740.pdf", pages = "142-156", stream = True, multiple_tables = True, guess = False)
dfF2 = pd.concat(dfF2)
dfF = dfF.append(dfF2, sort=False)
del dfF2
dfF = dfF.reset_index(drop=True)
dfF = dfF.loc[:662]

# Appendix G Distribution of Residues by Pesticide in Drinking Water
dfG = tb.read_pdf(pdfPath + "document_1374741.pdf", pages = "158", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfG = pd.concat(dfG)
dfG2 = tb.read_pdf(pdfPath + "document_1374741.pdf", pages = "159-172", stream = True, multiple_tables = True, guess = False)
dfG2 = pd.concat(dfG2)
dfG = dfG.append(dfG2, sort=False)
del dfG2
dfG = dfG.reset_index(drop=True)
dfG = dfG.loc[:731]

# Appendix H Distribution of Residues for Environmental Contaminants
dfH = tb.read_pdf(pdfPath + "document_1374742.pdf", pages = "174", stream = True,  multiple_tables = True, guess = False, area = [74.0, 47.5, 739.0, 563.0])
dfH = pd.concat(dfH)
dfH2 = tb.read_pdf(pdfPath + "document_1374742.pdf", pages = "175-180", stream = True, multiple_tables = True, guess = False, encoding = 'cp1252')
dfH2 = pd.concat(dfH2)
dfH = dfH.append(dfH2, sort=False)
del dfH2
dfH = dfH.reset_index(drop=True)
dfH = dfH.loc[:424]

# Appendix J Import Versus Domestic Pesticide Residue Comparisons
#page 186 - grapes
#page 187 - sweet bell pepper
dfJ1 = tb.read_pdf(pdfPath + "document_1374743.pdf", pages = "186", stream = True,  multiple_tables = False, guess = False, area = [138.0, 50.0, 735.0, 565.0])
dfJ1 = dfJ1.dropna(axis='columns', how='all')
dfJ1.columns = ['0', '1', '2', '3']

dfJ2 = tb.read_pdf(pdfPath + "document_1374743.pdf", pages = "187", stream = True,  multiple_tables = False, guess = False, area = [110.0, 50.0, 740.0, 565.0])
dfJ2.columns = ['0', '1', '2', '3', '4']

# Appendix K Pesticide Residues by Commodity
dfK = tb.read_pdf(pdfPath + "document_1374744.pdf", pages = "189", stream = True,  multiple_tables = True, guess = True, area = [93.0, 47.5, 720.0, 588.0])
dfK = pd.concat(dfK)
dfK.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfK2 = tb.read_pdf(pdfPath + "document_1374744.pdf", pages = "190-192", stream = True, multiple_tables = False, guess = True)
dfK2.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfK3 = tb.read_pdf(pdfPath + "document_1374744.pdf", pages = "193", stream = True, multiple_tables = False, guess = False)
dfK3.columns = ['0', '1', '2', '3', '4', '5', '6', '7']
dfK3 = dfK3.drop(columns=['1'])
dfK3.columns = ['0', '1', '2', '3', '4', '5', '6']
dfK4 = tb.read_pdf(pdfPath + "document_1374744.pdf", pages = "194", stream = True, multiple_tables = False, guess = False, encoding = 'cp1252')
dfK4.columns = ['0', '1', '2', '3', '4', '5', '6']
dfK = dfK.append(dfK2, sort=False)
del dfK2
dfK = dfK.append(dfK3, sort=False)
del dfK3
dfK = dfK.append(dfK4, sort=False)
del dfK4
dfK = dfK.reset_index(drop=True)
dfK = dfK.loc[:249]

# Appendix M Samples Reported to the U.S. Food and Drug Administration as Exceeding the Tolerance or Without Established Tolerance
dfM1 = tb.read_pdf(pdfPath + "document_1374745.pdf", pages = "199", stream = True,  multiple_tables = True, guess = False, area = [126.0, 35.0, 735.0, 563.0])
dfM1 = pd.concat(dfM1)
dfM2 = tb.read_pdf(pdfPath + "document_1374745.pdf", pages = "200", stream = True,  multiple_tables = True, guess = False, area = [86.0, 35.0, 735.0, 563.0])
dfM2 = pd.concat(dfM2)
dfM2.columns = ['0', '1', '2', '3', '4', '5', '6']
dfM3 = tb.read_pdf(pdfPath + "document_1374744.pdf", pages = "201-203", stream = True, multiple_tables = False, guess = True)
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
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
            
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

prod = 'Oats'

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
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
            
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
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
        
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

prod = 'Catfish'


for index, row in dfE.iterrows():
    try:
        if pd.isna(row[0]) == True or pd.isna(row[3]) == True or 'Pesticide' in row[0] :
            pass
        else:
            #get the chemicals
            if row[0] == 'epimer)' :
                chem = 'Cyhalothrin, Total (Cyhalothrin-L + R157836 epimer)'
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
            elif row[1] == 'P':
                func = 'plant growth regulator'
            elif row[1] == 'R':
                func = 'insect growth regulator'
            else: pass
            
            if 'Total' in chem :
                chem = 'Esfenvalerate+Fenvalerate'
            
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
        
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
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'NOTES' in row[0] or 'Pesticide / Commodity' in row[0]: 
            #skip lines that don't contain chemicals, or where there were no detections
            pass

        #find the chemicals
        elif pd.isna(row[2]) == True  :
#            chem = row[0].split('(')[0].strip()
            chem = row[0]
                 
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
            elif row[1] == 'P':
                func = 'plant growth regulator'
            else: func = ''
            
        if pd.isna(row[3]) == False : #if there are samples with detections
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
                        
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
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'NOTES' in row[0] or 'Pesticide / Commodity' in row[0]: 
            #skip lines that don't contain chemicals, or where there were no detections
            pass
        
        if row[0] == '(ESA) HM':
            pass

        #find the chemicals
        elif pd.isna(row[1]) == True  :
            chem = row[0].rsplit(' ', maxsplit = 1)[0].strip(',')
            
            if row[0].rsplit(' ', maxsplit = 1)[1].strip() == 'F':
                func = 'fungicide'
            elif row[0].rsplit(' ', maxsplit = 1)[1].strip() == 'H':
                func = 'herbicide'
            elif row[0].rsplit(' ', maxsplit = 1)[1].strip() == 'HM':
                func = 'herbicide metabolite'
            elif row[0].rsplit(' ', maxsplit = 1)[1].strip() == 'I':
                func = 'insecticide'
            elif row[0].rsplit(' ', maxsplit = 1)[1].strip() == 'IM':
                func = 'insecticide metabolite'
            elif row[0].rsplit(' ', maxsplit = 1)[1].strip() == 'P':
                func = 'plant growth regulator' 
            else: func = ''
        
        if chem == 'Acetochlor ethanesulfonic' :
            chem = 'Acetochlor ethanesulfonic acid'
            func = 'herbicide metabolite'
            
        if chem == 'Alachlor ethanesulfonic' :
            chem = 'Alachlor ethanesulfonic acid'
            func = 'herbicide metabolite'
            
        if chem == 'Metolachlor ethanesulfonic' :
            chem = 'Metolachlor ethanesulfonic acid'
            func = 'herbicide metabolite'
        
        if pd.isna(row[3]) == False : #if there are samples with detections
            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
                        
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
        if pd.isna(row[0]) == True or 'TOTAL' in row[0] or 'NOTES' in row[0] or 'Pesticide / Commodity' in row[0] or row[2] == '0': 
            #skip lines that don't contain chemicals or products, or where there were no detections
            pass

        #find the chemicals
        elif (pd.isna(row[1]) == True and '(' in row[0]) :
            chem = row[0].split('(')[0].strip()
            func = row[0].split('(')[1].strip().strip(')')
            
        elif pd.isna(row[1]) == False and '(' in row[0] and '(' in row[1]:
            chem = row[0].split('(')[0].strip()
            func = row[0].split('(')[1].strip().strip(')')
        
        elif pd.isna(row[1]) == False and '(' in row[1]:
            chem = row[0].split('(')[0].strip()
            func = row[1].split('(')[1].strip().strip(')')
                 
        else:
            prod = row[0].rstrip(' 0123456789')
            
            if prod == 'Fish, Catfish' :
                prod = 'Catfish'

            chemicals.append(chem)
            functions.append(func)
            products.append(prod.rstrip(' '))
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
                        
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
#page 186 - dfJ1: grapes
#page 187 - dfJ2: sweet bell peppers

del chem, func, prod
chemicals = []
functions = []
products = []
pdflist = []

prod = 'Grapes'
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
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
                
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

for index, row in dfJ2.iterrows():
    try:
        if 'Pesticide' in row[0]  or pd.isna(row[0]) == True : #skip rows that have "Pesticide in first field, or first field is NaN 
            pass

        #get the chemicals
        else: 
            chem = row[0]
            chemicals.append(chem)
            
            functions.append(func)
            products.append(prod.rstrip(' ')) #all entries have >10% sample detections
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
                
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
            
            if prod == 'Fish, Catfish' :
                    prod = 'Catfish'
            
            if func != '' :
                
                products.append(prod.rstrip(' '))
                functions.append(func)
                chemicals.append(chem)
                pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')   
    
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
        pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')
        
        
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
        if pd.isna(row[0]) == True or 'Commodity / Pesticide' in row[0] or 'NOTES' in row[0] : 
            #skip lines that don't contain chemicals or products
            pass
        
        elif 'methyl sulfide 7' in row[0]:
            chem = 'Pentachlorophenyl methyl sulfide'
        
        elif 'Fenamiphos' in row[0]:
            chem = 'Fenamiphos'
            
        elif 'Permethrin' in row[0]:
            chem = 'Permethrin'
        
        elif pd.isna(row[1]) == True and row[0][0].isdigit() == True :
            prod = row[0].strip(' 0123456789')
            
        else :
            chem = row[0].rstrip(' 0123456789')
            
            products.append(prod.rstrip(' '))
            functions.append(func)
            chemicals.append(chem)
            pdflist.append('2010 ' + prod.rstrip(' ') + '.pdf')   
        
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

# %% Fix filmename and Verify
oldfullchemicals = fullchemicals
fullchemicals = []

for s in oldfullchemicals:
    
    if 'Total' in s:
        s = s.rstrip(' Total')
        try:
            s = s.replace(', Total', '')
        except: pass
#        print(s)
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
    title = '2010 Pesticide Residues in ' + s
    titles.append(title)
document_type = ['FG']*length
url = ['https://www.ams.usda.gov/sites/default/files/media/2010%20PDP%20Annual%20Summary.pdf']*length
organization = ['USDA']*length

dfrr = pd.DataFrame({'filename':fullpdflist, 'title':titles, 'document_type':document_type, 'url':url, 'organization':organization}) 
dfrr=dfrr.drop_duplicates()

#dfrr.to_csv(csvPath + "RR-PDPASR2010.csv",index=False, header=True)

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
#path = r'C:\Users\mhorton\Documents\extscr\PDPASR\PDPASR2010\pdfs' #Folder doc is in
#os.chdir(path)    
#template = csv.reader(open('usda_pdpasr_2010_registered_documents.csv')) #Register Records template
#i=0
#for row in template:
#    i+=1
#    if i == 1: continue
#    try:
#        oldPath = path + '\\' + 'document_1374736.pdf' #Original doc name
#        newPath = path + '\\matchingdocs\\' + row[1]
#        copyfile(oldPath,newPath)
#    except: print('halp!', row[0])

# %% create the CSV for upload
length = len(fullproducts)
docDate = ['May 2012']*length
rawCat = fullproducts
rawCas = ['']*length
catCode = ['']*length
desc = ['']*length
cpcatCode = ['']*length
cpcatSource = ['']*length
fulldocNumber = ['']*length

#create a dictionary of doc IDs from the RRs
dftemp = pd.read_csv(csvPath + 'usda_pdpasr_2010_registered_documents.csv')
dftemp = dftemp[['DataDocument_id','filename']]
dftemp = dftemp.set_index('filename').T.to_dict('list')

df = pd.DataFrame({'data_document_id':fulldocNumber, 'data_document_filename':fullpdflist, 'doc_date':docDate, 'raw_category':rawCat, 'raw_cas':rawCas, 'raw_chem_name':fullchemicals, 'report_funcuse':fullfunctions, 'cat_code':catCode, 'description_cpcat':desc, 'cpcat_code':cpcatCode, 'cpcat_sourcetype':cpcatSource})
df=df.drop_duplicates()
df['data_document_id'] = df.data_document_filename.replace(dftemp) #get doc IDs from template dictionary
    
#df.to_csv(csvPath + "USDA-PDPASR2010.csv",index=False, header=True)