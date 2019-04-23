# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:12:49 2019

@author: ALarger
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
    version = ['']*numFiles #Version Number
    revDate = ['']*numFiles #Revision Date 
    chemName = ['']*numFiles #Product Name
    chemNum = ['']*numFiles #Product Number
    brand = ['']*numFiles #Brand
    cas = ['']*numFiles #CAS
    supplier = ['']*numFiles #Supplier
    safeHandling = ['']*numFiles #Precautions for safe handling
    safeStorage = ['']*numFiles #Conditions for safe storage
    specUse = ['']*numFiles #Specific end uses
    appearance = ['']*numFiles #Appearance
    odor = ['']*numFiles #Odour
    odorThresh = ['']*numFiles #Odour threshold
    pH = ['']*numFiles #pH
    melt = ['']*numFiles #Melting/freezing point
    bp = ['']*numFiles #Initial boiling point and boiling range
    flashP = ['']*numFiles #Flash point
    evapRate = ['']*numFiles #Evapouration rate
    flammability = ['']*numFiles #Flammabitily (solid,gas)
    feLimits = ['']*numFiles #Upper/lower flammability or explosive limits
    vp = ['']*numFiles #Vapour pressure
    vd = ['']*numFiles #Vapour density
    relD = ['']*numFiles #Relative density
    sol = ['']*numFiles #Water solubility
    partCoef = ['']*numFiles #Partition coefficient: n-octanol/water
    ignitTemp = ['']*numFiles #Auto-ignition temperature
    decompTemp = ['']*numFiles #Decomposition Temperature
    visc = ['']*numFiles #Viscosity
    expProp = ['']*numFiles #Explosive properties
    oxProp = ['']*numFiles #Oxidizing properties
    otherSafe = ['']*numFiles #Other safety information
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
        inProd = False
        inSafeHandling = False
        inSafeStorage = False
        inSpecUse = False
        inA = False
        inB = False
        inC = False
        inD = False
        inE = False
        inF = False
        inG = False
        inH = False
        inI = False
        inJ = False
        inK = False
        inL = False
        inM = False
        inN = False
        inO = False
        inP = False
        inQ = False
        inR = False
        inS = False
        inT = False
        inOtherSafety = False
        inReac = False
        inStable = False
        inHazReac = False
        inAvoid = False
        inIncompat = False
        inDecompProds = False
        uses = ''
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            if 'aldrich -' in cline[0]: continue
            if cline[0] == 'identified uses': uses = cline[-1]
            if 'version' in cline[0] and version[i] == '':
                version[i] = cline[-1].replace('version','').strip()
            if 'revision date' in cline[0] and revDate[i] == '':
                revDate[i] = cline[-1].replace('revision date','').strip()
            if 'product name' in cline[0]: inProd = True
            if 'product number' in cline[0]: 
                inProd = False
                chemNum[i] = cline[-1]
            if inProd == True:
                chemName[i] = (chemName[i] + ' ' + cline[-1]).strip()  
            if 'brand' in cline[0]:
                brand = cline[-1]
            if 'cas-no' in cline[0] and cas[i] == '':
                if cline[-1] == 'revision date': cas[i] = '-'
                elif cline[-1] == '-': cas[i] = cline[1] 
                else: cas[i] = cline[-1]
            if cline[0] == 'company' or cline[0] == 'supplier':
                supplier[i] = cline[-1]
            if 'exposure controls/personal protection' in cline[-1]:
                inSpecUse = False
                inSafeStorage = False
                specUse[i] = specUse[i].replace('apart from the uses mentioned in section 1.2',(uses + '. '))
            if inSpecUse == True:
                specUse[i] = (specUse[i] + ' ' + ' '.join(cline)).strip()
            if 'specific end use' in cline[-1]:
                inSafeStorage = False
                inSpecUse = True
            if inSafeStorage == True:
                safeStorage[i] = (safeStorage[i] + ' ' + ' '.join(cline)).strip()
            if 'conditions for safe storage' in cline[-1]:
                inSafeHandling = False
                inSafeStorage = True
            if inSafeHandling == True:
                safeHandling[i] = (safeHandling[i] + ' ' + ' '.join(cline)).strip()
            if 'precautions for safe handling' in cline[-1]:
                inSafeHandling = True
            if 'stability and reactivity' in cline[-1]:
                inOtherSafety = False
            if inOtherSafety == True:
                otherSafe[i] = (otherSafe[i] + '   ' + ' '.join(cline)).strip()
            if '9.2' in cline[0]: 
                inT = False
                inOtherSafety = True
            if cline[0] == 't)' or inT == True:
                inT = True
                inS = False
                oxProp[i] = (oxProp[i] + '   ' + ' '.join(cline)).replace('t) oxidizing properties','').strip()
            if cline[0] == 's)' or inS == True:
                inS = True
                inR = False
                expProp[i] = (expProp[i] + '   ' + ' '.join(cline)).replace('s) explosive properties','').strip()
            if cline[0] == 'r)' or inR == True:
                inR = True
                inQ = False
                visc[i] = (visc[i] + '   ' + ' '.join(cline)).replace('r) viscosity','').strip()
            if cline[0] == 'q)' or inQ == True:
                inQ = True
                inP = False
                decompTemp[i] = (decompTemp[i] + '   ' + ' '.join(cline)).replace('q) decomposition','').replace('temperature','').strip()
            if cline[0] == 'p)' or inP == True:
                inP = True
                inO = False
                ignitTemp[i] = (ignitTemp[i] + '   ' + ' '.join(cline)).replace('p) auto-ignition','').replace('temperature','').strip()
            if cline[0] == 'o)' or inO == True:
                inO = True
                inN = False
                partCoef[i] = (partCoef[i] + '   ' + ' '.join(cline)).replace('o) partition coefficient: n-','').replace('octanol/water','').strip()
            if cline[0] == 'n)' or inN == True:
                inN = True
                inM = False
                sol[i] = (sol[i] + '   ' + ' '.join(cline)).replace('n) water solubility','').strip()
            if cline[0] == 'm)' or inM == True:
                inM = True
                inL = False
                relD[i] = (relD[i] + '   ' + ' '.join(cline)).replace('m) relative density','').strip()
            if cline[0] == 'l)' or inL == True:
                inL = True
                inK = False
                vd[i] = (vd[i] + '   ' + ' '.join(cline)).replace('l) vapour density','').strip()
            if cline[0] == 'k)' or inK == True:
                inK = True
                inJ = False
                vp[i] = (vp[i] + '   ' + ' '.join(cline)).replace('k) vapour pressure','').strip()
            if cline[0] == 'j)' or inJ == True:
                inJ = True
                inI = False
                feLimits[i] = (feLimits[i] + '   ' + ' '.join(cline)).replace('j) upper/lower','').replace('flammability or','').replace('explosive limits','').strip()
            if cline[0] == 'i)' or inI == True:
                inI = True
                inH = False
                flammability[i] = (flammability[i] + '   ' + ' '.join(cline)).replace('i) flammability (solid, gas)','').strip()
            if cline[0] == 'h)' or inH == True:
                inH = True
                inG = False
                evapRate[i] = (evapRate[i] + '   ' + ' '.join(cline)).replace('h) evapouration rate','').replace('h) evaporation rate','').strip()
            if cline[0] == 'g)' or inG == True:
                inG = True
                inF = False
                flashP[i] = (flashP[i] + '   ' + ' '.join(cline)).replace('g) flash point','').strip()
            if cline[0] == 'f)' or inF == True:
                inF = True
                inE = False
                bp[i] = (bp[i] + '   ' + ' '.join(cline)).replace('f) initial boiling point and','').replace('boiling range','').strip()
            if cline[0] == 'e)' or inE == True:
                inE = True
                inD = False
                melt[i] = (melt[i] + '   ' + ' '.join(cline)).replace('e) melting point/freezing','').strip('point').strip()
            if cline[0] == 'd)' or inD == True:
                inD = True
                inC = False
                pH[i] = (pH[i] + '   ' + ' '.join(cline)).replace('d) ph','').strip()
            if cline[0] == 'c)' or inC == True:
                inC = True
                inB = False
                odorThresh[i] = (odorThresh[i] + '   ' + ' '.join(cline)).replace('c) odour threshold','').strip()
            if cline[0] == 'b)' or inB == True:
                inB = True
                inA = False
                odor[i] = (odor[i] + '   ' + ' '.join(cline)).replace('b) odour','').strip()
            if cline[0] == 'a)' or inA == True:
                inA = True
                appearance[i] = (appearance[i] + '  ' + ' '.join(cline)).replace('a) appearance','').strip()
            if 'toxicological information' in cline[-1]:
                inDecompProds = False
            if inDecompProds == True:
                decompProds[i] = (decompProds[i] + '  ' + ' '.join(cline)).strip()
            if 'hazardous decomposition products' in cline[-1]:
                inIncompat = False
                inDecompProds = True
            if inIncompat == True:
                incompat[i] = (incompat[i] + '  ' + ' '.join(cline)).strip()
            if 'incompatible materials' in cline[-1]:
                inAvoid = False
                inIncompat = True
            if inAvoid == True:
                avoid[i] = (avoid[i] + '  ' + ' '.join(cline)).strip()
            if 'conditions to avoid' in cline[-1]:
                inHazReac = False
                inAvoid = True
            if inHazReac == True:
                hazReac[i] = (hazReac[i] + '  ' + ' '.join(cline)).strip()
            if 'possibility of hazardous reactions' in cline[-1]:
                inStable = False
                inHazReac = True
            if inStable == True:
                stable[i] = (stable[i] + '  ' + ' '.join(cline)).strip()
            if 'chemical stability' in cline[-1]:
                inReac = False
                inStable = True
            if inReac == True: 
                reac[i] = (reac[i] + '  ' + ' '.join(cline)).strip()
            if 'reactivity' == cline[-1]:
                inReac = True
            
        i+=1

    df = pd.DataFrame({'File Name':fileName, 'Version Number':version, 'Revision Date':revDate, 'Product Name':chemName, 'Product Number':chemNum, 'Brand':brand, 'CAS':cas, 'Supplier':supplier, 'Precautions for safe handling':safeHandling, 'Conditions for safe storage':safeStorage, 'Specific end uses':specUse, 'Appearance':appearance, 'Odour':odor, 'Odour threshold':odorThresh, 'pH':pH, 'Melting/freezing point':melt, 'Initial boiling point and boiling range':bp, 'Flash point':flashP, 'Evapouration rate':evapRate, 'Flammabitily (solid,gas)':flammability, 'Upper/lower flammability or explosive limits':feLimits, 'Vapour pressure':vp, 'Vapour density':vd, 'Relative density':relD, 'Water solubility':sol, 'Partition coefficient: n-octanol/water':partCoef, 'Auto-ignition temperature':ignitTemp, 'Decomposition Temperature':decompTemp, 'Viscosity':visc, 'Explosive properties':expProp, 'Oxidizing properties':oxProp, 'Other safety information':otherSafe, 'Reactivity':reac, 'Chemical stability':stable, 'Possibility of hazardous reactions':hazReac, 'Conditions to avoid':avoid, 'Incompatible materials':incompat, 'Hazardous decomposition products':decompProds})
    df.to_excel(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\Sigma-Aldrich\Sigma-Aldrich Extracted Text.xlsx',index=False, header=True)

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, commas, semicolons and excess spaces, and makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
def main():
    os.chdir(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\Sigma-Aldrich')    
    file_list = glob("*.txt")       
    extract_data(file_list)    

if __name__ == "__main__": main()
