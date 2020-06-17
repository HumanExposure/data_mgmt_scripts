# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:52:48 2019

@author: ALarger
"""

import os, string, csv, re
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
    file_list: a list of the txt file names in the data group
    """
    idList = [] #Factotum document IDs
    filenameList = [] #file names
    prodnameList = [] #product names
    dateList = [] #sds dates
    revList = [] #revision numbers
    catList = [] #product categories
    casList = [] #CAS numbers
    chemList = [] #chemical names
    useList = [] #functional uses of each chemical
    minList = [] #minimum concentrations
    maxList = [] #maximum concentrations
    unitList = [] #unit type codes (1=weight frac, 2=unknown, 3=weight percent,...)
    rankList = [] #ingredient ranks
    centList = [] #central concentrations
    componentList = [] #components
    
    for file in fileList:
        if file in ['147.txt','230.txt','289.txt','511.txt','741.txt','751M.txt','285.txt']:
            continue #file is a different format
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        use = ''
        component = ''
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
                
        inUse = False #Flag for if you are in the Identified uses section of the SDS
        inIngredients = False #Flag for if you are in the ingredients section of the SDS
        
        #Get Factotum IDs
        docRecords = csv.reader(open('schaeffer_manufacturing_co_safety_data_sheets_documents_20191122.csv')) #csv downloaded from Factotum using the "Document records" button on the datagroup page
        for row in docRecords:
            if row[3] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
            
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue #Skip blank lines
                
            #Get product/document data
            if  'ghs product identifier' in cline and prodname == '':
                prodname = cline.split(':')[-1].strip()
            if 'date of issue' in cline and date == '':
                date = cline.split(':')[-1].strip()
            if 'version :' in cline:
                rev = cline.split(':')[-1].strip()
            
            #Get product use
            if inUse == True:
                if 'schaeffer' in cline:
                    inUse = False
                else:
                    cat = (cat + ' ' + cline).replace('identified uses','').strip()
            if 'identified uses' in cline:
                cat = cline.split(':')[-1].strip()
                inUse = True
                
            #Get ingredient data
            if inIngredients == True:
                conc = ''
                sline = splitLine(line) #split line into a list of elements
                if 'any concentration shown' in cline or 'section 4' in cline or 'united states' in cline:
                    inIngredients = False #out of ingredients section
                    
                elif len(sline) == 3: #if the line has three elements, they are ingredient name, %, and cas number
                    chem.append(sline[0])
                    conc = sline[1]
                    cas.append(sline[2])
                    if 'see below' in cas[-1]:
                        cas[-1] = ''

                    if conc.count('-') == 1: #if there is a dash in the concentration, everything before it is the minimun concentration, everything after it is the maximum concentration, and the central concentration is blank
                        minC.append(conc.split('-')[0])
                        maxC.append(conc.split('-')[1])
                        centC.append('')
                        unit.append(3)
                    else: #if there is no dash in the concentration, the concentration should go in the central concentration and the minimum and maximum concentrations should be blank 
                        minC.append('')
                        maxC.append('')
                        centC.append(conc)
                        unit.append(3)
                                        
                elif len(sline) == 1: #if the line only has one element, it is a continuation of the chemical name from the previous line 
                    chem[-1] = chem[-1] + ' ' + sline[0]
                    
                else:
                    print(len(sline),sline, file)
                    
            if 'ingredient name' in cline and 'cas' in cline: 
                inIngredients = True
                
        if chem == []: #if a document has no chemicals in it, leave all chemical related fields blank
            chem = ['']
            cas = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            
        #add the data from this document to the 
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend([use]*n)
        minList.extend(minC)
        maxList.extend(maxC)
        unitList.extend(unit)
        centList.extend(centC)
        componentList.extend([component]*n)
        #add rank
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    #create csv
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv(r'Schaeffer Extracted Text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Schaeffer') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()
