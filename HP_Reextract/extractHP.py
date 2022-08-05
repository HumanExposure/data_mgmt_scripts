# -*- coding: utf-8 -*-
"""
Created on Mon Aug 1 13:17:31 2022

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
    kit = []
    
    for file in fileList:
        
        #Identify the HP SDS files
        hpsds = False
        ifile = open(file, encoding = 'utf8')
        for line in ifile:
            cline = cleanLine(line)
            if 'company identification hp' in cline:
                hpsds = True
        if hpsds == False: continue
                
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        issueDate = ''
        revDate = ''
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
        
                
        inUse = False
        inIngredients = False
        inName = False
        
        template = csv.reader(open('hewlett-packard_1_documents_20201026.csv'))
        for row in template:
            if row[6] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
            
        for line in ifile:
            
            cline = cleanLine(line)
            if cline == '': continue
                
            if  'product identifier' in cline: 
                if prodname == '':
                    prodname = cline.split('identifier')[-1].strip()
                    inName = True
                    continue
                else: #KIT
                    # print(file, cline)
                    kit.append(file.replace('.txt','.pdf'))
                    
                    #append lists for previous component
                    if chem == []:
                        chem = ['']
                        cas = ['']
                        minC = ['']
                        maxC = ['']
                        centC = ['']
                        unit = ['']
                        
                    n = len(chem)
                    idList.extend([ID]*n)
                    filenameList.extend([file.replace('.txt','.pdf')]*n)
                    prodnameList.extend([prodname]*n)
                    if revDate != '':
                        dateList.extend([revDate]*n)
                    else:
                        dateList.extend([issueDate]*n)
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
                    
                    if chem == ['']:
                        rankList.extend([''])
                    else:
                        rankList.extend(list(range(1,n+1)))
                        
                    chem = []
                    cas = []
                    minC = []
                    maxC = []
                    centC = []
                    unit = []
                    

                        
                    
                    prodname = cline.split('identifier')[-1].strip()
                    inName = True
                    continue
                    # pass
                
                
                
            if inName == True:
                if 'other means of identification' in cline:
                    inName = False
                else: prodname = prodname + ' ' + cline
            # if 'issue date' in cline and date == '':
            if 'revision date' in cline and revDate == '':
                revDate = cline.split('revision date')[-1].strip(': ').split(' ')[0]
            if 'issue date' in cline and issueDate == '':
                issueDate = cline.split('issue date')[-1].strip(': ').split(' ')[0]
            # print(cline.count(':'),file,cline)
            if 'version #' in cline and rev == '':
                rev = cline.split('version')[-1].strip('#: ').split(' ')[0]
            if 'recommended use' in cline and cat == '':
                cat = cline.split('recommended use')[-1].strip(': ')
                inUse = True
                continue
            if inUse == True:
                if 'recommended' in cline:
                    inUse = False
                else:
                    cat = (cat + ' ' + cline)
            if inIngredients == True:
                conc = ''
                sline = splitLine(line)
                if 'composition comments' in cline or 'first-aid measures' in cline:
                    inIngredients = False
                    continue
                if 'material name' in cline or 'issue date' in cline or 'chemical name' in cline: 
                    continue
                
                if len(sline) == 4:
                    # print(len(sline), file, sline)
                    if 'no.' in sline[1]:
                        sline = [sline[0]+' '+sline[1], sline[2], sline[3]] 
                    else: 
                        sline = [sline[0], sline[2], sline[3]]
                if len(sline) == 2:
                    if all(x in '1234567890 ,<>%' for x in sline[-1]):
                        sline = [sline[0],'',sline[-1]]
                    else:
                        sline = [sline[0],sline[1],'']
                if len(sline) == 1:
                    chem[-1] = chem[-1] + ' ' + sline[0]
                    continue
                if len(sline) == 3:
                    chem.append(sline[0])
                    conc = sline[2]
                    cas.append(sline[1])

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
                        
                else:
                    print(len(sline), file, sline)
                if any(x not in '1234567890- ' for x in cas[-1]):
                    print(cas[-1])
                    cas[-1] = ''
                    
                
            if 'chemical name' in cline and 'cas' in cline: 
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
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        if revDate != '':
            dateList.extend([revDate]*n)
        else:
            dateList.extend([issueDate]*n)
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
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    # print(kit)
    i=-1
    for index, row in df.iterrows():
        i+=1
        # print(row['data_document_filename'])
        if row['data_document_filename'] in kit:
            df.loc[i,'component'] = df.loc[i,'prod_name']
            df.loc[i,'prod_name'] = df.loc[i,'prod_name'].split('[')[0]
    df.to_csv('HP Extracted Text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/HP') #Folder pdfs are in
    pdfs = glob("*.pdf")
    txts = glob("*.txt")
    
    unconverted = []
    for p in pdfs: 
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    pdfToText(unconverted)
    
    fileList = glob("*.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
