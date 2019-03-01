# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:45:51 2019

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
    msdsDate = []
    prodID = []
    msdsNum = []
    manufacturer = []
    chemName = []
    casN = []
    centC = []
    minC = []
    maxC = []
    units = []
    docName = []
    rank = []
    c=0
    f1 = False #flag that says if you are in the responsible party section and have not gotten the company name
    f2 = False #flag that says if you are in the composition section
    for file in file_list:
        ifile = open(file)
        r = 0 #rank
        pdfName = file.replace('.txt','.pdf')
        prod = ''
        date = ''
        manuf = ''
        oldRank = 0
        for line in ifile:
            if line == '/n': continue
            cline = cleanLine(line)
            if 'product id:' in cline:
                prod = cline.replace('product id:','')
            if 'msds date:' in cline:
                date = cline.replace('msds date:','')
            if 'msds number:' in cline:
                num = cline.replace('msds number:','')
                num = num.strip()
            if 'responsible party' in cline:
                f1 = True
            if f1 == True and 'company name:' in cline:
                manuf = cline.replace('company name:','')
                f1 = False
            if 'composition/information on ingredients' in cline:
                f2 = True
            if f2 == True and 'hazards identification' in cline:
                f2 = False
                if r > oldRank:
                    msdsDate.append(date)
                    prodID.append(prod)
                    msdsNum.append(num)
                    manufacturer.append(manuf)
                    chemName.append(chem)
                    casN.append(cas)
                    docName.append(pdfName)
                    if chem == '':
                        rank.append('')
                    else:
                        rank.append(r)
                    if '%' in conc:
                        units.append(3)
                        conc=conc.replace('%','')
                    else:
                        units.append(2)
                    if '-' in conc:
                        conc = conc.split('-')
                        minC.append(conc[0].strip())
                        maxC.append(conc[1].strip())
                        centC.append('')
                    else:
                        conc.strip()
                        centC.append(conc)
                        minC.append('')
                        maxC.append('')
            if f2 == True:
                if 'ingred name:' in cline:
                    if r > oldRank:
                        msdsDate.append(date)
                        prodID.append(prod)
                        msdsNum.append(num)
                        manufacturer.append(manuf)
                        chemName.append(chem)
                        casN.append(cas)
                        docName.append(pdfName)
                        if chem == '':
                            rank.append('')
                        else:
                            rank.append(r)
                        if '%' in conc:
                            units.append(3)
                            conc=conc.replace('%','')
                        else:
                            units.append(2)
                        if '-' in conc:
                            conc = conc.split('-')
                            minC.append(conc[0].strip())
                            maxC.append(conc[1].strip())
                            centC.append('')
                        else:
                            conc.strip()
                            centC.append(conc)
                            minC.append('')
                            maxC.append('')
                            oldRank = r
                    chem = cline.replace('ingred name:','')
                    if 'no hazardous' in cline:
                        chem = ''
                    r += 1
                    cas = ''
                    conc = ''
                elif 'cas:' in cline:
                    cas = cline.replace('cas:','')
                elif 'fraction by wt:' in cline:
                    conc = cline.replace('fraction by wt:','')
                
                
    df = pd.DataFrame({'File name':docName, 'MSDS Date':msdsDate, 'Product ID':prodID, 'Responsible Party':manufacturer, 'Chemical Name':chemName, 'CAS':casN, 'Min Conc':minC, 'Max Conc':maxC, 'Central Conc':centC, 'Unit':units, 'Rank':rank})
    df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Siri\bbb pdfs\siri_test.csv',index=False, header=True, date_format=None)
        
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, commas, semicolons and excess spaces, and makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.replace(',','_')
    cline = cline.replace(';','_')
    cline = cline.strip()
#    cline = cline.split("  ")
#    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
def main():
    os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Siri\bbb pdfs')    
    file_list = glob("*.txt")
    extract_data(file_list)

if __name__ == "__main__": main()