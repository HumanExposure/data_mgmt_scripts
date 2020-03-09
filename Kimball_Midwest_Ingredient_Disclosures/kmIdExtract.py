# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:37:25 2020

@author: ALarger
"""

import os, string, re, camelot
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
    line: string being cleaned
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    
    return(cline)


def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    fileList: a list of the txt file names in the data group
    """
    filenameList = [] #list of file names
    prodnameList = [] #list of product names
    prodnumList = [] #list of product numbers
    supplierList = [] #product supplier
    dateList = [] #list of document dates
    chemList = [] #list of chemical names
    casList = [] #list of cas numbers
    useList = [] #list of functional uses of each chemical
    rankList = [] #list of ingredient ranks
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        prodnum = ''
        supplier = ''
        date = ''
        chem = []
        cas = []
        use = []
        
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
        
            #Get product data
            if 'product name' in cline and prodname == '':
                prodname = cline.split(':')[-1].strip()
            if 'supplier' in cline and supplier == '':
                supplier = cline.split(':')[-1].strip()
            if 'date of disclosure' in cline and date == '':
                date = cline.split(':')[-1].strip()
            if ('product number' in cline or 'product part number' in cline) and prodnum == '':
                prodnum = cline.split(':')[-1].strip()
        
        #Extract ingredient data from table
        tables = camelot.read_pdf(file.replace('.txt','.pdf'),pages='all', flavor='lattice')
        if len(tables) == 0: print('Problem reading tables:',file)
        else:
            i=0 
            if 'CAS' in tables[0].df.iloc[0][0]:
                position = 1
            elif 'CAS' in tables[0].df.iloc[0][1]:
                position = 2
            else: print(file, tables[0].df.iloc[0,:])
            for table in tables:
                df = tables[i].df
                if i == 0: 
                    df = df.drop(df.index[0])
                if position == 1:
                    cas.extend(df.iloc[:,0])
                    chem.extend(df.iloc[:,1])
                    use.extend(df.iloc[:,2])
                else:
                    cas.extend(df.iloc[:,1])
                    chem.extend(df.iloc[:,0])
                    use.extend(df.iloc[:,2])
                i+=1
    
        #Append lists
        if len(chem) == 0:
            chem = ['']
            cas = ['']
            use = ['']

        n = len(chem)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        prodnumList.extend([prodnum]*n)
        supplierList.extend([supplier]*n)
        dateList.extend([date]*n)
        chemList.extend(chem)
        casList.extend(cas)
        useList.extend(use)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))

    #Make csv
    df = pd.DataFrame({'data_document_filename':filenameList, 'prod_name':prodnameList, 'product number':prodnumList, 'supplier':supplierList, 'date':dateList, 'raw_chem_name':chemList, 'cas':casList, 'report_funcuse':useList, 'ingredient_rank':rankList})
    df = df.applymap(lambda x: clean(x.replace('\n',' ').strip().replace('  ',' ').lower()) if isinstance(x, str) else x) #clean data
    df.to_csv('km id extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Kimball Midwest\Ingredient Disclosures') #Folder pdfs are in
    pdfs = glob("*.pdf")
    txts = glob("*.txt")
    unconverted = []
    for n in pdfs:
        if n.replace('.pdf','.txt') not in txts:
            unconverted.append(n)
    pdfToText(unconverted)
    
    fileList = glob("*.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()