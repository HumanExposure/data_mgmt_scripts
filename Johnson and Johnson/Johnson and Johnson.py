# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:08:17 2019

@author: ALarger
"""

import os,string 
import pandas as pd
from glob import glob

def pdf_to_text(files):
    """
    Converts pdf files into text files
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\'
    
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table",pdf])
        os.system(cmd)
        
    return
    
def text_to_csv(files):
    """
    Extracts data from text file into a Pandas dataframe
    """
    issDate = []
    revDate = []
    version = []
    prodName = []
    prodCode = []
    manufacturer = []
    recUse = []
    chemName = []
    casN = []
    centC = []
    minC = []
    maxC = []
    units = []
    docName = []
    specNo = []
    rank = []
    for file in files:
        ifile = open(file)
        j = 1 #rank
        weird = False
        gotInfo = False
        pdfName = file.replace('.txt','.pdf')
        name = ''
        vers = ''
        date = ''
        manuf = ''
        code = ''
        use = ''
        for line in ifile:
            if line == '/n': continue
            cline = cleanLine(line)
            if cline == []: continue
            if 'this safety data sheet was created pursuant to the requirements of:' in cline:
                weird = True
            if 'product name' in cline:
                name = cline[1]
            if weird == True:
                spec = ''
                if 'revision date' in cline and len(cline) == 6:
                    date = cline[1]
                    rDate = cline[3]
                    vers = cline[5]
            elif 'specification no.' in cline:
                spec = cline[1]
                rDate = ''
                vers = ''
            if 'issue date' in cline:
                date = cline[1]
            if 'safety data sheet code' in cline or 'product code' in cline:
                code = cline[1]
            if 'recommended use' in cline:
                use = cline[1].split('.')[0]
            if 'chemical name' in cline and 'cas no.' in cline:
                gotInfo = True
                if ('weight-%') in cline[2]:
                    unit = 3
                else: unit = 2
                for line2 in ifile:
                    cname = ''
                    cas = ''
                    concentration = ''
                    dline = cleanLine(line2)
                    if dline == []:
                        continue
                    if '4. first aid measures' in dline:
                        break
                    if '*the exact percentage' in dline[0]:
                        break
                    if weird == True:
                        if len(dline) < 4:
                            continue
                    cname = dline[0]
                    cas = dline[1]
                    concentration = dline[2]
                    if '-' in concentration:
                        minConc = concentration.split('-')[0]
                        minConc = minConc.strip()
                        maxConc = concentration.split('-')[1]
                        maxConc = maxConc.strip()
                        cConc = ''
                    else:
                        cConc = concentration
                        maxConc = ''
                        minConc = ''
                    units.append(unit)
                    version.append(vers)
                    revDate.append(rDate)
                    issDate.append(date)
                    docName.append(pdfName)
                    prodName.append(name)   
                    chemName.append(cname)
                    casN.append(cas)
                    centC.append(cConc)
                    minC.append(minConc)
                    maxC.append(maxConc)
                    prodCode.append(code)
                    manufacturer.append(manuf)
                    recUse.append(use)
                    specNo.append(spec)
                    rank.append(j)
                    j = j + 1
                    
                    
        if gotInfo == False:
            cname = ''
            cas = ''
            cConc = ''
            minConc = ''
            maxConc = ''
            unit = 2
            units.append(unit)
            version.append(vers)
            revDate.append(rDate)
            issDate.append(date)
            docName.append(pdfName)
            prodName.append(name)   
            chemName.append(cname)
            casN.append(cas)
            centC.append(cConc)
            minC.append(minConc)
            maxC.append(maxConc)
            prodCode.append(code)
            manufacturer.append(manuf)
            recUse.append(use)
            specNo.append(spec)
            rank.append(' ')
        
    df = pd.DataFrame({'File Name':docName, 'Issue Date':issDate, 'Revision Date':revDate, 'Version':version, 'Product Name':prodName, 'Product Code':prodCode, 'Specification No.':specNo, 'Recommended Use':recUse, 'Manufacturer':manufacturer, 'Chemical Name':chemName, 'CAS-No':casN, 'Central Concentration': centC, 'Min Concentration': minC, 'Max Concentration': maxC, 'Unit':units, 'Rank':rank})
    df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Johnson and Johnson\Johnson_and_Johnson.csv',index=False, header=True, date_format=None)
    df.to_excel(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Johnson and Johnson\Johnson_and_Johnson.xlsx')
              
def cleanLine(line):
    """
    Takes in a line of text and cleans it, removes excess spaces, makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.replace(',','_')
    cline = cline.replace(';','_')
    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
   
def main():
    os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Johnson and Johnson')
    
    pdfs = glob("document_*.pdf")
    n_pdfs = len(pdfs)
    n_txts = len(glob("document_*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(pdfs)
    
    n_txts = len(glob("document_*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")       
       text_to_csv(file_list)    
    return
    
if __name__ == "__main__": main()