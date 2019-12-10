# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:49:50 2019

@author: ALarger

Extracts Williams-Hayward SDSs (http://www.williams-hayward.com/msds-information/)
A fraction of the pdfs could not be converted directly to txt. OCR was attempted, but performed poorly. They will be extracted manually
"""

import os, string, csv, re, ghostscript, locale, subprocess
import pandas as pd
from glob import glob
from PIL import Image
import pytesseract

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
        cmd = " ".join([cmd,"-nopgbrk","-table",pdf])
        subprocess.call(cmd)
        
#        #OCR for bad files
#        outfile = file.replace('.pdf','.txt').replace('.PDF','.txt')
#        statinfo = os.stat(outfile)
#        if statinfo.st_size <= 5000: #Some files cant be directly converted to text
#            os.remove(outfile)
#            jpeg = file.split('.pdf')[0].split('.PDF')[0] + 'page%d.jpg'
#            args = ["pdf2jpeg", "-dNOPAUSE", "-sDEVICE=jpeg", "-r144", "-sOutputFile=" + jpeg, file]
#            encoding = locale.getpreferredencoding()
#            args = [a.encode(encoding) for a in args]
#            ghostscript.Ghostscript(*args)
#            
#            f = open(outfile, "a") 
#            pages = glob(jpeg.split('%d')[0]+'*.jpg')
#            config = r'--psm 4 -c preserve_interword_spaces=1' #OCR configuration
#            for p in range(1,len(pages) + 1): 
#                text = str(((pytesseract.image_to_string(Image.open(jpeg.split('%d')[0]+str(p)+'.jpg'), config = config))))    
#                f.write(text) 
#                f.write('\n')
#            
#            f.close() 
#            
#            #Delete jpegs
#            jpgs = glob('*.jpg')
#            for j in jpgs:
#                os.remove(j)
                    
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
        statinfo = os.stat(file)
        if statinfo.st_size <= 5000: 
            continue #text file not generated correctly. extract manually
        ifile = open(file)
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
                
        inCat = False
        inIngredients = False
        hasEinecs = False
        
        template = csv.reader(open(r'williams_hayward_protective_coatings_sds_documents_20191205.csv'))
        for row in template:
            if row[3].lower() == file.replace('.txt','.pdf').lower():
                ID = row[0]
                filename = row[3]
                break
        if ID == '':
            continue
            
        for line in ifile:
            
            cline = cleanLine(line)
            if cline == '': continue
            if 'trademark' in cline and prodname == '':
                prodname = ':'.join(cline.split(':')[1:]).strip()
            if date == '' and 'safety data sheet' in cline and cline.split('safety data sheet')[0].count('/') == 2:
                date = cline.split('safety data sheet')[0].strip()
            if 'application' in cline and ':' in cline and cat == '' and 'specific' not in cline:
                inCat = True
            if inCat == True:
                if 'supplier information' in cline:
                    inCat = False
                    continue
                cat = (cat + ' ' + cline.split(':')[-1]).strip()
            if inIngredients == True:
                if 'section' in cline or '___________________' in cline or 'this product is a mixture' in cline or 'safety data sheet' in cline: 
                    inIngredients = False
                    continue
                if cline == '(contains < 1% diethanolamine)':
                    chem[-1] = chem[-1] + ' ' + cline
                    continue
                sline = cline.split(' ')
                if hasEinecs == True and sline[-1].count('-') == 2:
                    sline = sline[:-1]
                if sline[-2] == '<' or sline[-2] == '>':
                    sline = sline[:-2]+[sline[-2]+' '+sline[-1]]
                chem.append(' '.join(sline[:-2]))
                cas.append(sline[-2])
                conc = sline[-1].strip('%')
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
        
            if 'cas number' in cline and chem == [] and 'toxicological' not in cline and 'exposure' not in cline and 'agent' not in cline:
                inIngredients = True
                if 'einecs' in cline: 
                    hasEinecs = True
                
        if chem == []:
            chem = ['']
            cas = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([filename]*n)
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
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv(r'Williams Hayward Extracted Text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Williams Hayward') #Folder pdfs are in
    pdfs = glob("*.pdf")
    txts = glob("*.txt")
    unconverted = []
    
    if len(txts) < len(pdfs): 
        for p in pdfs:
            if p.replace('.pdf','.txt').replace('.PDF','.txt') not in txts:
                unconverted.append(p)
        pdfToText(unconverted)
        
    fileList = glob("*.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
