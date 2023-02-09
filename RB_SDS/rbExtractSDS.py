# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:33:23 2020

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
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.03\\bin64\\' #Path to execfile
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
    cline = line.replace('–','-').replace('≥','>=').replace('≤','<=')
    cline = cline.lower()
    # cline = re.sub(' +', ' ', cline)
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
        if int(file.split('_')[0]) in [445, 1119, 1295, 1297, 1299, 1647, 1776, 2478, 2489]: continue #Corrupt fontmapping
        if int(file.split('_')[0]) in [251, 252, 253, 256, 261, 263, 300, 348, 349, 461, 1167]: continue #Different format
        if int(file.split('_')[0]) in [278, 316, 2289, 2459]: continue #No readable text
        #Corrupt fontmapping: 445, 1119, 1295, 1297, 1299, 1647, 1776, 2478, 2489
        #Different format: 261, 348, 349, 461
        #No readable text: 278, 316, 2289, 2459
        
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        chem = []
        cas = []
        unit = []
        minC = []
        maxC = []
        centC = []
        use = []
        component = []
        mix = ''
      
        template = csv.reader(open('rb_sds_documents_20200128.csv')) #Get Factotum ID
        for row in template:
            if row[3] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
        
        ifile = open(file, encoding = 'utf8')
        text = ifile.read()
        
        text = cleanLine(text)
        cleaned = re.sub(' +', ' ', text)
        if 'material safety data sheet' in cleaned or 'product safety data sheet' in cleaned: continue
        
        if 'therefore,thisproductisexemptfromtherequirements' in cleaned.replace(' ',''): #This document is an article
            prodname = cleaned.split('this product is considered')[0].strip('\n ')
            date = 'ARTICLE'
            
        else: #not an article
            
            if 'product name' in cleaned: 
                prodname = cleaned.split('product name')[1].split('distributed')[0].split('cas #')[0].split('sds no.')[0].split('material use')[0].split('supplier')[0].replace('\n',' ').strip(': ')
            if 'date of issue' in cleaned:
                date = cleaned.split('date of issue')[1].strip(': ').split(' ')[0].strip('lra-. ')
                rev = cleaned.split('date of issue')[0].strip().split(' ')[-1]
                if 'v' in rev: rev = rev.split('v')[-1].strip()
                else: rev = ''
                
            section3=' '.join(text.split('3. composition/information on ingredients')[1:]).split('first aid measures')[0].split('any concentration shown')[0].split('there are no additional ingredients')[0].split('there are no ingredients present')[0].strip()
            # print('***',file,'***')
            # if file == '860_sds.txt': print('*',section3,'*')
            casplace = 1 #position cas is in
            concplace = 2 #position concentration is in
            if 'name  ' in section3:
                mix = section3.split('ingredient name')[0].split('name  ')[0].strip()
                section3=section3.replace(mix,'')
            
            # elif '%' in section3: print(file)
            section3=section3.split('\n')
            # print(file, mix)
            for line in section3:
                #Figure out what to do with "or" (2589)
                # cline = cleanLine(line)
                if line == '': continue
                # print(line)
                if 'substance/mixture' in line.replace(' ',''):
                    continue 
                if 'mixture:' in line.replace(' ',''): continue
                    #edit to add documents with chemicals here like 1045_sds.pdf
                if 'ingredient name' in line: 
                    if '%' in line.split('cas')[0]: 
                        casplace = 2
                        concplace = 1
                    continue
                line=line.split('  ')
                line = [s.strip() for s in line]
                line = list(filter(None, line))
                
                if line[0] =='name': continue
                if len(line) == 5:
                    line=[line[0]+' '+line[1]+' '+line[2],line[3],line[4]]
                if len(line) == 4:
                    if any(x not in '1234567890 -%.,' for x in line[1]): line=[line[0]+' '+line[1],line[2],line[3]]
                    else:line=[line[0],line[1]+line[2],line[3]]
                if len(line) ==3:
                    chem.append(line[0])
                    cas.append(line[casplace])
                    centC.append(line[concplace])
                    component.append('')
                elif len(line)<3 and len(chem) == 0:
                    mix=mix+' '+' '.join(line)
                elif len(line) == 2:
                    chem.append(line[0])
                    cas.append('')
                    centC.append(line[1])
                    component.append('')
                else:
                    chem[-1] = chem[-1]+' '+line[0]
    
            
        prodname = re.sub(' +', ' ', prodname)
        
        
            
        mix = mix.replace('\n',' ').replace('\r',' ').replace('mixture','').replace('substance','').replace('m ixture','').replace('contains:','').replace('contains inactive ingredients:','').replace('the product contains the following components','').replace('the solution contains','').strip(':/-. ')
        mix = re.sub(' +', ' ', mix)
        if mix == 'yes':mix = ''
        if mix != '':
            mix = mix.replace('and',',').split(',')
            for m in mix:
                if m.strip() == '': continue
                chem.append(m)
                cas.append('')
                centC.append('')
                component.append('substance/mixture section')
                if 'cas' in m: cas[-1] = m.split('cas')[-1].split(')')[0].strip('# ')
                
                
        if len(chem) == 0:
            chem = ['']
            cas = ['']
            centC = ['']
            component = ['']
            
        for c in range(0,len(chem)): #clean up concentrations and names
            chem[c] = (re.sub(' +', ' ', chem[c])).strip()
            minC.append('')
            maxC.append('')
            use.append('')
            centC[c] = re.sub(' +', ' ', centC[c])
            if centC[c] != '':
                unit.append('3')
            else:
                unit.append('')
            if '-' in centC[c]:
                minC[c] = centC[c].split('-')[0].strip()
                maxC[c] = centC[c].split('-')[1].strip()
                centC[c] = ''
            
            
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
        minList.extend(minC)
        maxList.extend(maxC)
        unitList.extend(unit)
        centList.extend(centC)
        componentList.extend(component)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
            
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv('rb sds extracted text.csv',index=False, header=True)
    
    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/RB') #Folder pdfs are in
    pdfs = glob("*_sds.pdf")
    txts = glob("*_sds.txt")
    unconverted = []
    for n in pdfs:
        if n.replace('.pdf','.txt') not in txts:
            unconverted.append(n)
    # pdfToText(unconverted)
    
    fileList = glob("*_sds.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()