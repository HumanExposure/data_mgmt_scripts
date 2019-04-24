# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 08:45:29 2019

@author: ALarger

Extracts data from Heteroz, LLC MSDS txt files
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
    #Section 1/2
    chemName = ['']*numFiles #Product Name
    chemNum = ['']*numFiles #Catalog Number
    cas = ['']*numFiles #CAS number
    supplier = ['']*numFiles #Company name
    #Section 6
    safeHandling = ['']*numFiles #Precautions for safe handling
    #Section 9
    appearance = ['']*numFiles #appearance
    melt = ['']*numFiles #Melting point
    bp = ['']*numFiles #Boiling point
    sol = ['']*numFiles #Solubility
    #Section 10
    stable = ['']*numFiles #Chemical stability
    tox = ['']*numFiles #Toxicological information   

    i=0
    numFiles=len(file_list)
    for file in file_list:
        fileName[i] = file.replace('txt','pdf')
        ifile = open(file)
        #Flags for gathering sections that span multiple lines
        inSafeHandling = False
        inStable = False
        inTox = False
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            if any('page'in c for c in cline): continue
            if 'company name' in cline: 
                supplier[i] = cline[-1]
            if 'product name' in cline:
                chemName[i] = cline[-1]
            if 'catalog number' in cline:
                chemNum[i] = cline[-1]
            if 'cas number' in cline:
                cas[i] = cline[-1]
            if cline[0] == '7.': 
                inSafeHandling = False
            if inSafeHandling == True:
                safeHandling[i] = (safeHandling[i] + ' ' + ' '.join(cline)).strip()
            if cline[0] == 'handling' and safeHandling[i] == '': 
                safeHandling[i] = cline[-1]
                inSafeHandling = True
            if cline[0] == 'appearance':
                appearance[i] = cline[-1]
            if cline[0] == 'melting point':
                melt[i] = cline[-1]
            if cline[0] == 'boiling point':
                bp[i] = cline[-1]
            if 'water solubility' in cline[0]:
                sol[i] = cline[-1].replace('water solubility ','')
            if '11.' in cline[0]:
                inTox = False
            if inTox == True:
                tox[i] = (tox[i] + ' ' + ' '.join(cline)).strip()
            if 'toxicological information' in cline and tox[i] == '':
                inStable = False
                inTox = True
            if inStable == True:
                stable[i] = (stable[i] + ' ' + ' '.join(cline)).strip()
            if '10.' in cline[0] and stable[i] == '':
                inStable = True
        i+=1

    df = pd.DataFrame({'File Name':fileName, 'Product Name':chemName, 'Catalog number':chemNum, 'CAS number':cas, 'Company name':supplier, 'Precautions for safe handling':safeHandling, 'Appearance':appearance, 'Melting point':melt, 'Boiling point':bp, 'Solubility':sol, 'Chemical stability':stable, 'Toxicological information':tox})
    df.to_excel(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\Heteroz, LLC\Heteroz Extracted Text.xlsx',index=True, header=True)

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
    os.chdir(r'L:\Lab\HEM\Wetmore-PFAS-PDFs\Heteroz, LLC')    
    file_list = glob("*.txt")       
    extract_data(file_list)    

if __name__ == "__main__": main()