# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:50:52 2020

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
    sline = clean(line.replace('–','-').replace('‐','-'))
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
    filenameList = [] #list of file names
    prodnameList = [] #list of product names
    formulaList = [] #list of formula numbers
    casList = [] #list of CAS numbers
    chemList = [] #list of chemical names
    useList = [] #list of functional uses of each chemical
    rankList = [] #list of ingredient ranks
    brandList = [] #list of product brands
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        formula = ''
        brand = []
        chem = []
        cas = []
        use = []
        inChem = False
            
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
            if 'product name:' in cline and prodname == '':
                prodname = cline.split(':')[-1].strip()
            if 'specification id:' in cline and formula == '':
                formula = cline.split(':')[-1].strip()

            if inChem == True: #Parse ingredients              
                sline = splitLine(line)
                if len(sline) == 3:
                    chem.append(sline[0])
                    cas.append(sline[1])
                    use.append(sline[2])
                elif len(sline) == 2:
                    if all(x in '1234567890- ' for x in sline[1]):
                        chem.append(sline[0])
                        cas.append(sline[1])
                        use.append('')
                    else:
                        chem[-1] = chem[-1] + ' ' + sline[0]
                        use[-1] = use[-1] + ' ' + sline[1]
                elif len(sline) == 1:
                    chem[-1] = chem[-1] + ' ' + sline[0]

            if 'ingredients' in cline and 'cas' in cline:
                inChem = True
            
        #get brand(s)
        if 'glade' in prodname: brand.append('glade')
        if 'scrubbing bubbles' in prodname: brand.append('scrubbing bubbles')
        if 'windex' in prodname: brand.append('windex')
        if 'favor' in prodname: brand.append('favor')
        if 'off!' in prodname: brand.append('off!')
        if 'pledge' in prodname: brand.append('pledge')
        if 'raid' in prodname: brand.append('raid')
        if 'shout' in prodname: brand.append('shout')
        if 'ziploc' in prodname: brand.append('ziploc')
        if 'drano' in prodname: brand.append('drano')
        if 'kiwi' in prodname: brand.append('kiwi')
        if 'fantastik' in prodname: brand.append('fantastik')
        if 'saran' in prodname: brand.append('saran')
        brand = ', '.join(brand)
         
        if len(chem) == 0:
            chem = ['']
            cas = ['']
            use = ['']
            
        n = len(chem)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        formulaList.extend([formula]*n)
        brandList.extend([brand]*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend(use)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_filename':filenameList, 'prod_name':prodnameList, 'Formula number':formulaList, 'brand':brandList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'ingredient_rank':rankList})
    df.to_csv('scj ingredient disclosure extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/scj pages') #Folder pdfs are in
    pdfs = glob("*_id.pdf")
    txts = glob("*_id.txt")
    unconverted = []
    for p in pdfs: 
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    pdfToText(unconverted)

    fileList = glob("*_id.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
