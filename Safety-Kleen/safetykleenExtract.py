# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:52:05 2020

@author: ALarger
"""

import os, string, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return


def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)


def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    sline = clean(line.replace('–','-'))
    sline = sline.lower()
    sline = sline.strip()
    sline = sline.split("  ")
    sline = [x.strip() for x in sline if x != ""]
    
    return(sline)


def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    fileList: a list of the txt file names in the data group
    """
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    manufList = [] #list of manufacturers
    dateList = [] #list of msdsDates
    catList = [] #list of product categories
    casList = [] #list of CAS numbers
    chemList = [] #list of chemical names
    compList = [] #list of minimum concentrations

    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        manufacturer = ''
        date = ''
        use = ''
        previousLine = ''
        chem = []
        cas = []
        comp = []
                
        inUse = False
        inIngredients = False
        
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
        
            #Extract product information
            if (previousLine == 'material name' or previousLine == 'product identifier') and prodname == '':
                prodname = cline
            if 'material name:' in cline and prodname == '' and use != '':
                prodname = cline.split(':')[1].split(' id')[0].split('sds')[0].strip()
            if inUse == True:
                if cline == 'restrictions on use':
                    inUse = False
                    continue
                if 'inc.' in cline:
                    inUse = False
                    sline = splitLine(line)
                    manufacturer = sline[0]
                    continue
                use = (use + ' ' + cline).strip()
            if (cline == 'recommended use' or cline == 'product use' or cline == 'product use recommended use') and use == '':
                inUse = True
            if 'product use:' in cline and use == '':
                use = cline.split(':')[-1]
                inUse = True
            if previousLine == 'issue date' and date == '':
                date = cline
            if ('manufacturer' in previousLine or 'supplier' in previousLine) and manufacturer == '':
                if 'manufacture' in cline: continue
                sline = splitLine(line)
                manufacturer = sline[0]
                
            #Extract ingredients
            if inIngredients == True:
                if 'section 4' in cline or 'product dilution for use ranges' in cline or 'component related regulatory information' in cline or 'further information' in cline or 'additional information' in cline or 'product contains' in cline or 'other components below reportable levels' in cline or 'remainder of the product' in cline or 'concentration ranges are used' in cline:
                    inIngredients = False
                    continue
                if any(x in cline for x in['______','page','safety data sheet','material name:','component information/information on non-hazardous components']): continue
                sline = splitLine(line)
                if len(sline) == 3:
                    chem.append(sline[1])
                    cas.append(sline[0])
                    comp.append(sline[2])
                elif len(sline) > 3:
                    chem.append(' '.join(sline[1:-1]))
                    cas.append(sline[0])
                    comp.append(sline[-1])
                elif len(sline) == 2:
                    chem.append(sline[0])
                    cas.append('')
                    comp.append(sline[1])
                elif len(sline) == 1:
                    if '*' in cline:
                        inIngredients = False
                        continue
                    chem[-1] = chem[-1] + ' ' + sline[0]
#                    print(len(sline),sline,file)
                    
            if 'component' in cline and 'percent' in cline:
                inIngredients = True
                
            previousLine = cline
                
        if chem == []:
            chem = ['']
            cas = ['']
            comp = ['']

        use = use.replace('if this product is used in combination with other products, refer to the safety data sheet for those products','').replace('if this product is used in combination with other products, refer to the safety data sheets for those products','').strip('. ')
        n = len(chem)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        manufList.extend([manufacturer]*n)
        dateList.extend([date]*n)
        catList.extend([use]*n)
        casList.extend(cas)
        chemList.extend(chem)
        compList.extend(comp)

    #Create csv
    df = pd.DataFrame({'data_document_filename':filenameList, 'prod_name':prodnameList, 'manufacturer':manufList, 'doc_date':dateList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'raw_comp': compList})
    df.to_csv('safety kleen extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Safety-Kleen') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()