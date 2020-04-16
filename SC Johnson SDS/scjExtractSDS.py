# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 12:31:51 2020

@author: ALarger
"""

import os, string, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    Download xpdf here: https://www.xpdfreader.com/download.html
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
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    casList = [] #list of CAS numbers
    chemList = [] #list of chemical names
    useList = [] #list of functional uses of each chemical
    concList = [] #list of ingredient concentrations
    rankList = [] #list of ingredient ranks
    formulaList = [] #list of formula numbers
    brandList = [] #list of brands
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        formula = ''
        chem = []
        cas = []
        conc = []
                
        inName = False
        inIngredients = False
        betweenPages = False
            
        for line in ifile:
            
            cline = cleanLine(line)
            if cline == '': continue
        
            #Extract product data
            if rev == '' and 'version' in cline and 'print date' in cline: 
                rev = cline.split('version ')[-1].split(' ')[0]
            if date == '' and 'revision date' in cline:
                date = cline.split('revision date')[-1].strip().split(' ')[0]
            if inName == True:
                if ':' in cline: 
                    inName = False
                else: 
                    prodname = prodname + ' ' + cline
            if prodname == '' and ('trade name' in cline or 'product name' in cline):
                inName = True
                prodname = cline.split(':')[-1].strip()
            if cat == '' and ('recommended use' in cline or 'use of the' in cline):
                cat = cline.split(':')[-1].strip()
            if formula == '' and 'sds number' in cline: 
                formula = cline.split('sds number')[-1].strip()
            
            #Extract ingredient data
            if inIngredients == True: 
                if 'first aid measures' in cline or 'specific chemical identity' in cline or 'for additional information' in cline: 
                    inIngredients = False #out of ingredient section
                    continue
                if cline.count('/')==1 and all(x in '1234567890/' for x in cline): 
                    betweenPages = True #If the ingredient section spans multiple pages, the header and page number needs to be skipped
                    continue
                sline = splitLine(line) #split the line up into a list of elements
                if betweenPages == True and len(sline) ==3 and 'version' not in cline and 'glade' not in cline and 'www.' not in cline: 
                    betweenPages = False
                if betweenPages == False: #In ingredients table
                    if len(sline) == 3:
                        chem.append(sline[0])
                        cas.append(sline[1])
                        conc.append(sline[2])
                    elif len(sline) == 4:
                        if sline[2].count('-') == 2: 
                            chem.append(sline[0]+' '+sline[1])
                            cas.append(sline[2])
                            conc.append(sline[3])
                        else:
                            chem.append(sline[0])
                            cas.append(sline[1])
                            conc.append(sline[2]+' '+sline[3])
                    elif len(sline) == 2:
                        if sline[1].count('-') == 2 or sline[1] == 'mixture':
                            chem.append(sline[0])
                            cas.append(sline[1])
                            conc.append('')
                        elif cas[-1][-1] == '-':
                            chem[-1] = chem[-1] + ' ' + sline[0]
                            cas[-1] = cas[-1] + sline[1]
                        else: 
                            chem[-1] = chem[-1] + ' ' + sline[0]
                            conc[-1] = conc[-1] + sline[1]
                    elif len(sline) == 1:
                        if cas[-1][-1] == '-':
                            cas[-1] = cas[-1] + sline[0]
                        else:
                            chem[-1] = chem[-1] + ' ' + sline[0]
                    else:
                        print(len(sline),sline,file)
            if 'chemical name' in cline and 'cas-no' in cline:
                inIngredients = True
                
        #get brand(s)
        brand = []
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
        
        if chem == []:
            chem = ['']
            cas = ['']
            conc = ['']
            
        n = len(chem)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend(['']*n)
        concList.extend(conc)
        formulaList.extend([formula]*n)
        brandList.extend([brand]*n)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))

    #Make csv   
    df = pd.DataFrame({'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'concentration':concList, 'rank':rankList, 'formula number':formulaList, 'brand':brandList})
    df.to_csv('scj sds extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/scj sds') #Folder pdfs are in
    pdfs = glob("*_sds.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*_sds.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*_sds.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*_sds.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()
