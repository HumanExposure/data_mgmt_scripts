# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:48:48 2020

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
    sline = sline.split("            ")
    sline = [x.strip() for x in sline if x != ""]
    
    return(sline)
    

def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    upcList = [] #list of product upcs
    chemList = [] #list of chemical names
    useList = [] #list of functional uses of each chemical
    rankList = [] #list of ingredient ranks
    brandList = [] #product brand
    sizeList = [] #Product size
    typeList = [] #Document type (either CO or FU)    
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        upc = ''
        brand = ''
        size = ''
        doctype = ''
        chem = []
        use = []
        inChem = False
        previousLine = ''
        twolinesago = ''
        
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue
        
            #Get product name and upc(s)
            if 'upc code' in cline and prodname == '':
                prodname = previousLine
                if len(prodname) < 5 or prodname[0] == '(': 
                    prodname = twolinesago + ' ' + prodname
            if 'upc code' in previousLine and upc == '':
                upc = cline
            if upc == '' and prodname == '' and all(c in '1234567890 ,' for c in cline):
                upc = cline
                prodname = previousLine
                if len(prodname) < 5 or prodname[0] == '(': 
                    prodname = twolinesago + ' ' + prodname
            if all(c in '1234567890 ,' for c in cline) and previousLine in upc:
                upc = upc + cline
            if '6:00pm' in prodname: 
                prodname = ''
                
            #Get brand
            if brand == '' and 'all-laundry' in cline:
                brand = 'All'
            if brand == '' and 'snuggle' in cline:
                brand = 'Snuggle'
            if brand == '' and 'sundetergent' in cline or 'sunproducts' in cline:
                brand = 'Sun'
            if brand == '' and 'sunlightlaundry' in cline:
                brand = 'Sunlight'
            if brand == '' and 'wisk' in cline: 
                brand = 'Wisk'
            
            #Get ingredients
            if inChem == True:
                if cline[0] == '*': 
                    inChem = False
                    continue
                sline = splitLine(line)
                if len(sline) == 2:
                    chem.append(sline[0].replace('  ',' ').replace('  ',' ').strip('* '))
                    use.append(sline[1].replace('  ',' ').replace('  ',' ').strip('* '))
                elif len(sline) == 1 and len(chem) > 0:
                    chem[-1] = (chem[-1] + ' ' + sline[0]).replace('  ',' ').replace('  ',' ').strip('* ')
                else:
                    print(len(sline),sline, file)
                
            if 'ingredients' in cline and 'function' in cline:
                inChem = True
            
            twolinesago = previousLine
            previousLine = cline
    
        #Get doc type
        if prodname == '': doctype = 'FU'
        else: doctype = 'CO'
            
        #Get size
        words = prodname.split(' ')
        inSize = False
        for x in range(len(words)-1,-1,-1):
            if inSize == True:
                if all(y in '1234567890.' for y in words[x]):
                    size = words[x] + ' ' + size
                else:
                    inSize = False
                    break
            if size == '' and ('lb' in words[x] or 'oz' in words[x] or 'ct' in words[x] or 'ml' in words[x] or 'l' in words[x] or 'kg' in words[x]) and all(y in '1234567890.lbsozctmkg' for y in words[x]):
                size = words[x]
                inSize = True
        
        #Append lists
        if len(chem) == 0:
            chem = ['']
            use = ['']

        n = len(chem)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        upcList.extend([upc]*n)
        brandList.extend([brand]*n)
        sizeList.extend([size]*n)
        chemList.extend(chem)
        useList.extend(use)
        typeList.extend([doctype]*n)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))

    #Make csv
    df = pd.DataFrame({'data_document_filename':filenameList, 'prod_name':prodnameList, 'upc':upcList, 'brand':brandList, 'size':sizeList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'ingredient_rank':rankList, 'document type':typeList})
    df.to_csv('sun id extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Sun Ingredient Disclosures\New ID') #Folder pdfs are in
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