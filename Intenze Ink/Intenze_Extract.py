# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 14:55:59 2020

@author: SHanda
Based on ALarger, "schaeffersExtract.py"
"""


#import packages 
import os, string, csv, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\SHanda\\xpdf-tools-win-4.02\\bin64\\'
    
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
    cline = cline.lower() #lowercase
    cline = re.sub(' +', ' ', cline) #replace + with space
    cline = cline.strip() #removes extra spaces
    
    return(cline)


def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    sline = clean(line.replace('–','-'))
    sline = sline.lower() #lowercase
    sline = sline.strip() #removes extra space
    sline = sline.split("  ") #splits on doublespace, creates indexed list
    sline = [x.strip() for x in sline if x != ""] #removes extra space if not an empty string
    
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
        docRecords = csv.reader(open('intenze_tattoo_1_documents_20200622.csv')) #csv downloaded from Factotum using the "Document records" button on the datagroup page
        
        for row in docRecords:
            if row[6] == file.replace('.txt','.pdf'): #find the filename column
                ID = row[0] # finds ID column
                break
        if ID == '': #move on when you reach end of IDs
            continue
            
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue #Skip blank lines
                
            #Get product/document data
            if  'color name' in cline and prodname == '': #product name appears after color name
                prodname = cline.split(':')[-1].strip() # extract product name
            if 'rev' in cline and date == '':
                date = cline.split(':')[-1].strip() # extract date (last item in list)
                rev = cline.split(':')[-2].strip() #extract version (second to last item)
                
            
            #Get product use
            if inUse == True:
                if 'the product should' in cline: #where to stop getting use data ?
                    inUse = False
                else:
                    cat = (cat + ' ' + cline).replace('use of the preparation','').strip()
            if 'use of the preparation' in cline:
                cat = cline.split(':')[-1].strip() #not sure if this will work.??? not on same line 
                inUse = True
                
            #Get ingredient data
            if inIngredients == True:
                #conc = ''
                sline = splitLine(line) #split line into a list of elements
                if 'hazardous components' in cline: #look for keyword after table
                    inIngredients = False #out of ingredients section
                    
                elif len(sline) == 3: #if the line has three elements, they are ingredient name, cas number, EC number
                    chem.append(sline[0])
                    cas.append(sline[1])
                    minC.append('')
                    maxC.append('')
                    centC.append('')
                    unit.append('')
 
                   
                else:
                    print(len(sline),sline, file)
                    
            if 'name' in cline and 'c.a.s.' in cline: #or it could be cas
                inIngredients = True
                
        if chem == []: #if a document has no chemicals in it, leave all chemical related fields blank
            chem = ['']
            cas = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            
        #add the data from this document to the db
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
        #add chemical rank from ingredient list
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    #create csv
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv(r'Intenze Extracted Text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\SHanda\\Intenze\SDS_English') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()
