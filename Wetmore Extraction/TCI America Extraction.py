# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 13:53:59 2019

@author: ALarger

Extracts data from TCI America MSDS txt files
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
    version = ['']*numFiles #Revision Number
    revDate = ['']*numFiles #Revision Date 
    #Section 1/3
    chemName = ['']*numFiles #Product Name
    chemNum = ['']*numFiles #Product Number
    cas = ['']*numFiles #CAS
    supplier = ['']*numFiles #Company
    #Section 7
    safeHandling = ['']*numFiles #Precautions for safe handling
    safeStorage = ['']*numFiles #Conditions for safe storage
    storageIncompat = ['']*numFiles #Storage incompatibilities
    #Section 9
    state = ['']*numFiles #Physical State
    form = ['']*numFiles #Form
    color = ['']*numFiles #Color
    odor = ['']*numFiles #Odor
    odorThresh = ['']*numFiles #Odor threshold
    melt = ['']*numFiles #Melting/freezing point
    pH = ['']*numFiles #pH
    bp = ['']*numFiles #Boiling point/range
    vp = ['']*numFiles #Vapor pressure
    decompTemp = ['']*numFiles #Decomposition Temperature
    vd = ['']*numFiles #Vapour density
    relD = ['']*numFiles #Relative density
    dynVisc = ['']*numFiles # Dynamic viscosity
    kinVisc = ['']*numFiles #Kinematic 
    partCoef = ['']*numFiles #Partition coefficient: n-octanol/water (log P_ow)
    evapRate = ['']*numFiles #Evaporation rate (butyl acetate = 1)
    flashP = ['']*numFiles #Flash point
    ignitTemp = ['']*numFiles #Auto-ignition temperature
    flammability = ['']*numFiles #Flammabitily (solid,gas)
    felLow = ['']*numFiles #Lower flammability or explosive limit
    felUp = ['']*numFiles #Upper flammability or explosive limit
    sol = ['']*numFiles #Solubility(ies)
    #Section 10
    reac = ['']*numFiles #Reactivity
    stable = ['']*numFiles #Chemical stability
    hazReac = ['']*numFiles #Possibility of hazardous reactions
    avoid = ['']*numFiles #Conditions to avoid
    incompat = ['']*numFiles #Incompatible materials
    decompProds = ['']*numFiles #Hazardous decomposition products      

    i=0
    numFiles=len(file_list)
    for file in file_list:
        fileName[i] = file.replace('txt','pdf')
        ifile = open(file)
        #Flags for gathering sections that span multiple lines
        inSupplier = False 
        inSafeHandling = False
        inSafeStorage = False
        inStorageIncompat = False
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            if any('page'in c for c in cline): continue
            if '7. handling and storage' in cline[0]: continue
            if 'revision number' in cline[0]: 
                version[i] = cline[-1].replace('revision number: ','')
            if 'revision date' in cline[0]: 
                revDate[i] = cline[-1].replace('revision date: ','')
            if 'product name' in cline[0]: 
                chemName[i] = cline[-1]
            if 'product code' in cline[0]: 
                chemNum[i] = cline[-1]
            if cline[0] == 'cas number:': 
                cas[i] = cline[-1]
            if inSupplier == True: 
                supplier[i] = cline[0]
                inSupplier = False
            if cline[0] == 'company:': 
                inSupplier = True
            if cline[0] == 'precautions for safe handling:': 
                inSafeHandling = True
            if cline[0] == 'conditions for safe storage:':
                inSafeHandling = False
                inSafeStorage = True
            if cline[0] == 'storage incompatibilities:':
                inSafeStorage = False
                inStorageIncompat = True
            if 'exposure controls' in cline[-1] and 'personal protection' in cline[-1]: 
                inStorageIncompat = False
            if inSafeHandling == True:
                safeHandling[i] = (safeHandling[i] + ' ' + ' '.join(cline)).replace('precautions for safe handling:','').strip()
            if inSafeStorage == True:
                safeStorage[i] = (safeStorage[i] + ' ' + ' '.join(cline)).replace('conditions for safe storage:','').strip()
            if inStorageIncompat == True:
                storageIncompat[i] = (storageIncompat[i] + ' ' + ' '.join(cline)).replace('storage incompatibilities:','').strip()
            if 'physical state' in cline[0]: 
                state[i] = cline[-1]        
            if cline[0] == 'form:': 
                form[i] = cline[-1]
            if cline[0] == 'color:': 
                color[i] = cline[-1]
            if cline[0] == 'odor:': 
                odor[i] = cline[-1]
            if cline[0] == 'odor threshold:': 
                odorThresh[i] = cline[-1]
            if 'melting point/freezing point:' in cline:
                cline = ' '.join(cline).split(':')
                melt[i] = cline[1].replace('ph','').strip()
                pH[i] = cline[-1].strip()
            if 'boiling point/range:' in cline:
                cline = ' '.join(cline).split(':')
                bp[i] = cline[1].replace('vapor pressure','').strip()
                vp[i] = cline[-1].strip()
            if 'decomposition temperature:' in cline:
                cline = ' '.join(cline).split(':')
                decompTemp[i] = cline[1].replace('vapor density','').strip()
                vd[i] = cline[-1].strip()
            if 'relative density:' in cline:
                cline = ' '.join(cline).split(':')
                relD[i] = cline[1].replace('dynamic viscosity','').strip()
                dynVisc[i] = cline[-1].strip()
            if 'kinematic viscosity:' in cline: 
                kinVisc[i] = cline[-1]
            if 'partition coefficient:' in cline and partCoef[i] == '':
                cline = ' '.join(cline).split(':')
                partCoef[i] = cline[1].replace('evaporation rate','').strip()
                evapRate[i] = cline[-1].strip()
            if 'flash point:' in cline:
                cline = ' '.join(cline).split(':')
                flashP[i] = cline[1].replace('autoignition temperature','').strip()
                ignitTemp[i] = cline[-1].strip()
            if 'flammability (solid, gas):' in cline:
                cline = ' '.join(cline).split(':')
                flammability[i] = cline[1].replace('flammability or explosive limits','').strip()
            if 'lower:' in cline: 
                felLow[i] = cline[-1]
            if 'upper:' in cline: 
                felUp[i] = cline[-1]
            if 'reactivity:' in cline: 
                reac[i] = cline[-1]
            if 'chemical stability:' in cline:
                stable[i] = ' '.join(cline).split(':')[-1]
            if 'possibility of hazardous reactions:' in cline:
                hazReac[i] = cline[-1]
            if 'conditions to avoid:' in cline:
                avoid[i] = cline[-1]
            if 'incompatible materials:' in cline:
                incompat[i] = cline[-1]
            if 'hazardous decomposition products:' in cline:
                decompProds[i] = cline[-1]
        i+=1

    df = pd.DataFrame({'File Name':fileName, 'Revision Number':version, 'Revision Date':revDate, 'Product Name':chemName, 'Product Code':chemNum, 'CAS':cas, 'Company':supplier, 'Precautions for safe handling':safeHandling, 'Conditions for safe storage':safeStorage, 'Storage incompatibilities':storageIncompat, 'Physical State (20°C)':state, 'Form':form, 'Color':color, 'Odor':odor, 'Odor threshold':odorThresh, 'Melting/freezing point':melt, 'pH':pH, 'Boiling point/range':bp, 'Vapor pressure':vp, 'Decomposition temperature':decompTemp, 'Vapor density':vd, 'Relative density':relD, 'Dynamic viscosity':dynVisc, 'Kinematic viscosity':kinVisc, 'Partition coefficient':partCoef, 'Evaporation rate':evapRate, 'Flash point':flashP, 'Autoignition temperature':ignitTemp, 'Flammabitily (solid, gas)':flammability, 'Lower flammability or explosive limit':felLow, 'Upper flammability or explosive limit':felUp,  'Solubility(ies)':sol, 'Reactivity':reac, 'Chemical stability':stable, 'Possibility of hazardous reactions':hazReac, 'Conditions to avoid':avoid, 'Incompatible materials':incompat, 'Hazardous decomposition products':decompProds})
    df.to_excel(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\TCI America, Inc\TCI America Extracted Text.xlsx',index=False, header=True)

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
    os.chdir(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\TCI America, Inc')    
    file_list = glob("*.txt")       
    extract_data(file_list)    

if __name__ == "__main__": main()