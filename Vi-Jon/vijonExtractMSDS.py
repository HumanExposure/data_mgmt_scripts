# -*- coding: utf-8 -*-
"""
Created on Thu May  7 15:34:34 2020

@author: ALarger
"""


import os, string, re, csv
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


def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    line: string being split
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
        prodname = ''
        date = ''
        rdate = ''
        idate = ''
        rev = ''
        cat = ''
        ID = ''
        chem = []
        cas = []
        unit = []
        minC = []
        maxC = []
        centC = []
        inChems = False
        betweenPages = False
        gotChems = False
 
        #Get Factotum document number
        template = csv.reader(open('Vi-Jon_MSDS_unextracted_documents.csv')) #extracted text csv template from factotum
        for row in template:
            if row[1] == file.replace('.txt','.pdf'):
                ID = row[0] 
                break
        if ID == '':
            continue
        
        #Parse txt file
        ifile = open(file, encoding = 'utf8')
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
        
            #Get product data
            if 'product name:' in cline: prodname = cline.split(':')[-1]
            if rdate == '' and 'revision date:' in cline:
                rdate = cline.split('revision date:')[-1].split('revision')[0].strip()
            if idate == '' and ('issuing date:' in cline or 'issue date:' in cline):
                idate = cline.split('issuing date:')[-1].split('issue date:')[-1].split('revision')[0].strip()
            if rev == '' and 'revision number:' in cline:
                rev = cline.split('revision number:')[-1].strip()
            if cat == '' and 'recommended use' in cline and 'of the chemical and restrictions on use' not in cline:
                cat = cline.split('recommended use')[-1].strip(': ')
            if cat == '' and 'product use' in cline:
                cat = cline.split('product use')[-1].strip(': ')
            if betweenPages == True: 
                if 'issuing date' in cline:
                    betweenPages = False
                continue
            
            #Extract ingredients section
            if inChems == True:
                if 'first aid measures' in cline or cline[0] == '*' or 'the product contains' in cline:
                    inChems = False
                    gotChems = True
                    continue
                if cline[:5] == 'page ':
                    betweenPages = True
                    continue
                sline = splitLine(line)
                while True:
                    if sline[-1] == '*' or sline[-1] == '-' or 'filed:' in sline[-1] or 'xx-xxx-xxxx' in sline[-1]:
                        sline = sline[:-1]
                    else:
                        break
                if len(sline) < 3:
                    if gotChems == False or cline[:9] == 'granted: ':
                        continue
                    elif len(sline) == 2:
                        if sline[1].count('-') == 1:
                            sline = [sline[0],'',sline[1]]
                        else:
                            chem[-1] = chem[-1] + ' ' +sline[0]
                    else:
                        chem[-1] = chem[-1] + ' ' + sline[0]
                if len(sline) > 2:
                    gotChems = True
                    while len(sline) > 3: #sometimes chemical names and/or cas numbers get split up. recombine these
                        if all(x in '1234567890-.% ' for x in (sline[-1]+sline[-2])) and (sline[-1]+sline[-2]).count('-') < 2: #combine concentration
                            sline[-2] = sline[-2] + ' ' + sline[-1]
                            sline = sline[:-1]
                        elif sline[1].count('-') != 2 or any(x.isalpha() for x in sline[1]): #combine chemical name
                            sline[1] = sline [0] + ' ' + sline[1]
                            sline = sline[1:]
                        else:
                            print(len(sline),sline, file)
                            break
                    if len(sline) == 3: 
                        chem.append(sline[0])
                        cas.append(sline[1])
                        unit.append(3)
                        if '<' in sline[2] and '-' not in sline[2]:
                            sline[2] = sline[2].replace('<','0-')
                        if sline[2].count('-') == 1:
                            minC.append(sline[2].split('-')[0].strip())
                            maxC.append(sline[2].split('-')[-1].strip())
                            centC.append('')
                        else: 
                            minC.append('')
                            maxC.append('')
                            centC.append(sline[2].strip(' %'))
    
            if 'chemical name cas' in cline and gotChems == False: 
                inChems = True
                
        if rdate == '' or rdate == 'none': #If there is a revision date, use that. if not, use issue date
            date = idate
        else:
            date = rdate
                
        if len(chem) == 0:
            chem = ['']
            cas = ['']
            unit = ['']
            minC = ['']
            maxC = ['']
            centC = ['']

        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend(['']*n)
        minList.extend(minC)
        maxList.extend(maxC)
        unitList.extend(unit)
        centList.extend(centC)
        componentList.extend(['']*n)

        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))

    #Make csv
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv('vijon msds extracted text.csv',index=False, header=True, encoding='utf8')


def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/vi-jon msds') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)

    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")
       extractData(fileList)


if __name__ == "__main__": main()
