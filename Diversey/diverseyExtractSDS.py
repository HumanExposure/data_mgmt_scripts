# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 13:46:14 2020

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
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        previousLine = ''
        chem = []
        cas = []
        unit = []
        minC = []
        maxC = []
        centC = []
        diversey = False

        inIngredients = False
        betweenPages = False

        for line in ifile: #Some docs aren't made by Diversey and have a different format. These should be skipped
            cline = cleanLine(line)
            if cline == '': continue
            if 'diversey' in cline:
                diversey = True

        if diversey == True:
            template = csv.reader(open('diversey_sds_documents_20200427.csv')) #"document records" csv from factotum
            for row in template:
                if row[4] == file.replace('.txt','.pdf'):
                    ID = row[0] #Factotum ID
                    break
            if ID == '':
                continue
            ifile = open(file, encoding = 'utf8')
            for line in ifile:
                cline = cleanLine(line)
                if cline == '': continue
                if prodname == '' and 'product name:' in cline:
                    prodname = cline.split(':')[-1].strip()
                if date == '' and 'revision:' in cline:
                    date = cline.split('revision:')[-1].strip().split(' ')[0]
                if rev == '' and 'version:' in cline:
                    rev = cline.split('version:')[-1].strip().split(' ')[0]
                if date == '' and 'preparation date:' in cline:
                    date = cline.split('preparation date:')[-1].strip().split(' ')[0]
                if rev == '' and 'version number:' in cline:
                    rev = cline.split('version number:')[-1].strip().split(' ')[0]
                if cat == '' and 'product name:' in previousLine and ':' not in cline:
                    cat = cline
                if inIngredients == True: #Get data from the ingredients section
                    if 'exact percentages' in cline or 'first aid' in cline: #If out of ingredients section, stop extracting ingredients
                        inIngredients = False
                    else:
                        sline = splitLine(line)
                        if '1 of ' in cline:
                            betweenPages = True
                            continue
                        if betweenPages == True:
                            if len(sline) > 1:
                                betweenPages = False
                            else:
                                continue
                        if len(sline) == 4:
                            sline = [sline[0]+' '+sline[1],sline[2],sline[3]]
                        if len(sline) == 3:
                            chem.append(sline[0])
                            cas.append(sline[1])
                            sline[2] = sline[2].strip('%')
                            unit.append(3)
                            if sline[2].count('-') == 1:
                                minC.append(sline[2].split('-')[0].strip('> '))
                                maxC.append(sline[2].split('-')[-1].strip('< '))
                                centC.append('')
                            elif '<' in sline[2]:
                                minC.append(0)
                                maxC.append(sline[2].strip('< '))
                                centC.append('')
                            else:
                                minC.append('')
                                maxC.append('')
                                centC.append(sline[2])
                        if len(sline) < 3:
                            chem[-1] = chem[-1]+' '+sline[0]
                if cline == 'ingredient(s) cas # weight %': #Inside ingredients section
                    inIngredients = True

                previousLine = cline

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
    df.to_csv('diversey sds extracted text.csv',index=False, header=True)


def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Diversey') #Folder pdfs are in
    pdfs = glob("*_sds.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*_sds.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)

    nTxts = len(glob("*_sds.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*_sds.txt")
       extractData(fileList)


if __name__ == "__main__": main()
