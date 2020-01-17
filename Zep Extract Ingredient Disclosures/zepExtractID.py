# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 11:57:08 2020

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
        cat = ''
        ID = ''
        chem = []
        cas = []
        use = []
        inChem = False
      
        template = csv.reader(open('zep_ingredient_disclosure_documents_20200115.csv')) #Get Factotum ID
        for row in template:
            if row[3] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
        
        data = csv.reader(open('zep scraped data all.csv')) #Get raw cat from scraped data
        for row in data:
            if row[0] == file.replace('_ID.txt',''):
                cat = row[7]
            
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
            if 'product name:' in cline and prodname == '':
                prodname = cline.split(':')[-1].strip()
            if 'version:' in cline and rev == '':
                rev = cline.split(':')[-1].strip()
            if 'revision date:' in cline and date == '':
                date = cline.split(':')[-1].strip()
            if inChem == True and ('distributed by zep' in cline or '*designated lists' in cline):
                inChem = False
            if inChem == True: #Parse ingredients              
                sline = cline.split(' ')
                for i in range(len(sline) - 1, -1, -1):
                    if any(x not in '1234567890,' for x in sline[i]) == False:
                        del sline[i]
                    else: break
                if sline == []: continue
                if any((x.count('-') and any(z.isalpha() for z in x) == False) or x == 'available' or x == 'withheld' for x in sline) == True:
                    for y in range(0,len(sline)):
                        if (sline[y].count('-') == 2 and any(z.isalpha() for z in sline[y]) == False) or (sline[y] == 'not' and sline[y+1] == 'available') or sline[y] == 'withheld':
                            chem.append(' '.join(sline[:y]))
                            cas.append(sline[y])
                            use.append(' '.join(sline[y+1:]))
                            if cas[-1] == 'not':
                                cas[-1] = cas[-1] + ' ' + sline[y+1]
                                use[-1] = ' '.join(sline[y+2:])
                else:
                    if sline == ['ingredient']:
                        use[-1] = use[-1] + ' ' + sline[0]
                    else:
                        chem[-1] = chem[-1] + ' ' + ' '.join(sline)

            if 'ingredient name' in cline:
                inChem = True
            
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
        catList.extend([cat]*n)
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
    df.to_csv('zep ingredient disclosure extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Zep') #Folder pdfs are in
    pdfs = glob("*_ID.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*_ID.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*_ID.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*_ID.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()