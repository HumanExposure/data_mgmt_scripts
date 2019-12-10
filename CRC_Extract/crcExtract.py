# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 13:02:52 2019

@author: ALarger
"""

import os, string, csv, re
import pandas as pd
from glob import glob

        
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()

    return(cline)


def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    sline = clean(line)
    sline = sline.lower()
    sline = sline.strip()
    sline = sline.split("  ")
    sline = [x.strip() for x in sline if x != ""]

    return(sline)


def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
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
    
    #Go through each txt file
    for file in fileList:
        ifile = open(file)
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
        inIngredients = False
        
        #Match file name with factotum ID 
        template = csv.reader(open('crc_mining_documents_20191205.csv')) #"Document records" from factotum 
        for row in template:
            if row[3] == file.replace('.txt','combined.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
            
        #Parse file
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
            if  'product identifier' in cline and prodname == '':
                prodname = cline.replace('product identifier','').strip()
            if 'recommended use' in cline and cat == '':
                cat = cline.replace('recommended use','').strip()
            if 'date:' in cline and date == '':
                rev = cline.split(':')[1].strip().split(' ')[0]
                date = cline.split('date: ')[1].split(' ')[0]
                
            #Get data from ingredients section
            if inIngredients == True:
                if 'specific chemical identity' in cline or 'first-aid' in cline or 'composition comments' in cline:
                    inIngredients = False
                    continue
                if 'material name:' in cline or 'version' in cline or 'chemical name' in cline or 'sds us' in cline: 
                    continue
                conc = ''
                sline = splitLine(line)
                if len(sline) == 2:
                    print(len(sline),file, sline)
                    sline.insert(1,'')
                if len(sline) >= 3:
                    chem.append(sline[0])
                    cas.append(sline[-2])
                    conc = sline[-1]
                    if conc.count('-') == 1:
                        minC.append(conc.split('-')[0])
                        maxC.append(conc.split('-')[1])
                        centC.append('')
                        unit.append(3)
                    elif conc == '':
                        minC.append('')
                        maxC.append('')
                        centC.append('')
                        unit.append('')
                    else:
                        minC.append('')
                        maxC.append('')
                        centC.append(conc)
                        unit.append(3)
                elif len(sline) == 1 and len(chem) > 0 :
                    chem[-1] = chem[-1] + ' ' + sline[0]
                else:
                    print(len(sline),file, sline)
                
            if 'chemical name' in cline and chem == []:
                inIngredients = True
               
        if chem == []:
            chem = ['']
            cas = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
                
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','combined.pdf')]*n)
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
            
    #Make csv to upload to factotum
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv('CRC Mining Extracted Text.csv',index=False, header=True)

    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\CRC\Mining') #Folder pdfs are in
    fileList = glob("*.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
