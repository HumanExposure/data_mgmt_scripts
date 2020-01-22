# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 15:01:49 2020

@author: ALarger
"""


import os, string, csv, re, camelot
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


def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    idList = [] #list of product IDs
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    casList = [] #list of CAS numbers
    chemList = [] #list of chemical names
    useList = [] #list of functional uses of each chemical
    minList = [] #list of minimum concentrations
    maxList = [] #list of maximum concentrations
    unitList = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...)
    rankList = [] #list of ingredient ranks
    centList = [] #list of central concentrations
    componentList = [] #List of components
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        ID = ''
        chem = []
        cas = []
        use = []
      
        template = csv.reader(open('turtle_wax_ingredient_disclosures_documents_20200121.csv')) #Get Factotum ID
        for row in template:
            if row[3] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
            
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
            if 'product name:' in cline and prodname == '':
                prodname = cline.split(':')[-1].strip()
            if date == '':
                for x in cline.split(' '):
                    if x.count('/') == 2 and any(y.isalpha() for y in x) == False:
                        date = x
            if rev == '':
                for x in cline.split(' '):
                    if '.0' in x and any(y.isalpha() for y in x) == False:
                        rev = x
                        
        tables = camelot.read_pdf(file.replace('.txt','.pdf'), pages='all', flavor='lattice')
        for table in tables: 
            df = table.df
            for index, row in df.iterrows():
                if row[0] == 'Name' or len(row) < 3 or row[0].strip() == '': continue
                chem.append(row[0].replace('\n',' ').strip())
                cas.append(row[1].replace('\n',' ').strip())
                use.append(row[2].replace('\n',' ').strip())

        if len(chem) == 0:
            chem = ['']
            cas = ['']
            use = ['']
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend(['']*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend(use)
        minList.extend(['']*n)
        maxList.extend(['']*n)
        unitList.extend(['']*n)
        centList.extend(['']*n)
        componentList.extend(['']*n)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv('turtle wax ingredient disclosure extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Turtle Wax') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()