# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 11:34:58 2019

@author: ALarger

Extracts data from Matrix Scientific MSDS txt files
"""

import os, string
import pandas as pd
from glob import glob

def extract_data(file_list):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    numFiles = len(file_list)
    fileName = ['']*numFiles #File Name
    revDate = ['']*numFiles #Revision Date 
    chemName = ['']*numFiles #Product Name
    chemNum = ['']*numFiles #Product Number
    cas = ['']*numFiles #CAS
    supplier = ['']*numFiles #Supplier
    safeStorage = ['']*numFiles #Conditions for safe storage and handling
    appearance = ['']*numFiles #Appearance
    formula = ['']*numFiles #Molecular formula
    weight = ['']*numFiles #Molecular weight
    bp = ['']*numFiles #Boiling point (C)
    melt = ['']*numFiles #Melting point (C)
    density = ['']*numFiles #Density
    ir = ['']*numFiles #Index of Refraction
    flashPoint = ['']*numFiles #Flash Point
    incompat = ['']*numFiles #Incompatibilities
    decompProds = ['']*numFiles #Hazardous decomposition products

    i=0
    numFiles=len(file_list)
    for file in file_list:
        fileName[i] = file.replace('txt','pdf')
        inChemName = False
        inSafeStorage = False
        inIncompat = False
        inDecompProds = False
        ifile = open(file)
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            if 'last updated' in cline: 
                if revDate[i] == '': revDate[i] = cline[-1]
                continue
            if inChemName == True and ('catalog number' in cline[0] or 'synonym' in cline[0]):
                inChemName = False
            if (cline[0].split(' ')[0] == 'name' and chemName[i] == '') or inChemName == True:
                chemName[i] = (chemName[i] + ' ' + ' '.join(cline)).replace('name','').strip()
                inChemName = True
            if 'catalog number' in cline[0]: 
                chemNum[i] = cline[-1]
            if 'cas registry number' in cline[0]:
                cas[i] = cline[-1].strip('[]')
            if cline[0] == 'company':
                supplier[i] = cline[-1]
            if inSafeStorage == True:
                if 'exposure controls and personal protection' in cline[-1]: 
                    inSafeStorage = False
                else:
                    safeStorage[i] = (safeStorage[i] + ' ' + ' '.join(cline)).strip()
            if 'handling and storage' in cline[-1]:
                inSafeStorage = True
            if 'appearance:' in cline[0]:
                appearance[i] = cline[-1].replace('appearance:','').strip()
            if 'molecular formula:' in cline[0]:
                formula[i] = cline[-1].replace('molecular formula:','').strip()
            if 'molecular weight:' in cline[0]:
                weight[i] = cline[-1].replace('molecular weight:','').strip()
            if 'boiling point' in cline[0]:
                bp[i] = cline[-1].replace('boiling point (c):','').strip()
            if 'melting point' in cline[0]:
                melt[i] = cline[-1].replace('melting point (c):','').strip()
            if 'density' in cline[0]:
                density[i] = cline[-1].replace('density (g/ml):','').strip()
            if 'index of refraction:' in cline[0]:
                ir[i] = cline[-1].replace('index of refraction:','').strip()
            if 'flash point' in cline[0]:
                flashPoint[i] = cline[-1].replace('flash point (c):','').strip()
            if 'toxicological information' in cline[-1]:
                inDecompProds = False
            if inDecompProds == True:
                if len(cline) == 2:
                    decompProds[i] = (decompProds[i] + ', ' + cline[0] + ': ' + cline[1]).lstrip(', ')
                elif len(cline) == 1:
                    decompProds[i] = (decompProds[i] + ', ' + cline[0]).lstrip(', ')
                else: print(cline)
            if 'hazard decomposition products' in cline[0]:
                inIncompat = False
                inDecompProds = True
            if 'incompatibilities:' in cline[0]:
                inIncompat = True
            if inIncompat == True:
                incompat[i] = (incompat[i] + ', ' + cline[-1]).lstrip(', ')
        i+=1

    df = pd.DataFrame({'File Name':fileName, 'Revision Date':revDate, 'Product Name':chemName, 'Catalog Number':chemNum, 'CAS':cas, 'Company':supplier, 'Handling and Storage':safeStorage, 'Appearance':appearance, 'Molecular Formula':formula, 'Molecular Weight':weight, 'Boiling point (C)':bp, 'Melting point (C)':melt, 'Density (g/ml)':density, 'Index of refraction':ir, 'Flash point (C)':flashPoint, 'Incompatibilities':incompat, 'Hazardous decomposition products':decompProds})
    df.to_excel(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\Matrix Scientific\Matrix Scientific Extracted Text.xlsx',index=False, header=True)

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, excess spaces, and makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
def main():
    os.chdir(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\Matrix Scientific')    
    file_list = glob("*.txt")       
    extract_data(file_list)    

if __name__ == "__main__": main()