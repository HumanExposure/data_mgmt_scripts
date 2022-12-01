# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 08:49:26 2022

@author: ALarger
"""


import os, string, csv, re
import pandas as pd
from glob import glob
import PyPDF2


# def pdfToText(files):
#     """
#     Converts pdf files into text files
#     files: list of filenames
#     """
#     for file in files:
#         pdffileobj=open(file,'rb')
#         pdfreader=PyPDF2.PdfFileReader(pdffileobj)
#         x=pdfreader.numPages
#         text=''
#         newname=file.replace('.pdf','.txt')
#         file1=open(newname,"a", encoding="utf-8")
#         for y in range(0,x):
#             pageobj=pdfreader.getPage(y)
#             text=pageobj.extractText()  
#             file1.writelines(text)
#             file1.writelines('\n')
            
#     return


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
    # clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = line.replace('–','-')
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
        text = ifile.read()
        
        cleaned = cleanLine(text)
    
     
                
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        use = []
        component = ''
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
        
        dateline = ''
        
        template = csv.reader(open('big_d_sds_documents_20221201.csv'))
        for row in template:
            if row[6] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
        
        # if 'epa reg' in cleaned: print(ID)

        
        prodname = cleaned.split('product identifier')[1].split('\n')[0].strip() #get product name
        dateline = cleaned.split('date of preparation:')[-1].split('product')[0].split('\n')#[0].strip() #get version number
        for d in dateline: 
            if d.count(',') == 1:
                date = d.strip()
        if date == '':
            date = cleaned.split('date of last revision')[-1].split('\n')[0].strip()
        cat = cleaned.split('recommended use')[1].split('\n')[0].strip()#.split('section 2')[0].replace('\n',' ').strip(' :,') #Get raw category
        
        section3 = cleaned.split('section 3')[1].split('section 4')[0]        
        section3 = section3.split('information on ingredients')[-1].split('other identifiers')[-1]
        section3 = section3.split('\n')
        
        for s in section3: #iterate through every line in section 3
            s=s.strip()
            if s == '': #Skip blank lines
                continue
            if 'product identifier' in s or 'sds no.' in s or 'date of preparation' in s: 
                continue #skip lines between pages
                
            casrns = re.findall(r'\b[1-9]{1}[0-9]{1,7}-\d{2}-\d\b', s)

            if s == 'contains no hazardous ingredients.': continue
        
            if len(casrns) <1:
                # print(file,s)
                if 'no cas' in s:
                    casrns.append('no cas')
                elif 'trade secret' in s:
                    casrns.append('trade secret')
                elif 'cbi*' in s:
                    casrns.append('cbi*')
                elif len(chem)>0:
                    if s == '-hydroxy-' and '-hydroxy-' in chem[-1]:continue
                    chem[-1] = (chem[-1]+' '+s).strip()
                else:
                    print(file,s)
                
        
            if len(casrns) == 1:
                chem.append(s.split(casrns[0])[0].strip())
                cas.append(casrns[0])
                minC.append('')
                maxC.append('')
                centC.append(s.split(casrns[0])[-1].strip('% '))
                unit.append('3')
                use.append('')
                
            
                
        if chem == []:
            chem = ['']
            cas = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            use = ['']
        
        for x in range(len(chem)):
            if '-' in centC[x]: #split concentrations
                minC[x] = centC[x].split('-')[0].strip('>= ')
                maxC[x] = centC[x].split('-')[-1].strip('<= ')
                centC[x] = ''
            elif '<' in centC[x]:
                minC[x] = '0'
                maxC[x] = centC[x].strip('<= ')
                centC[x] = ''
            elif '>' in centC[x]:
                minC[x] = centC[x].strip('>= ')
                maxC[x] = '100'
                centC[x] = ''
            
    
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
        componentList.extend([component]*n)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv('big d sds extracted text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Big D/Big D New') #Folder pdfs are in
    pdfs = glob("*sds.pdf")
    txts = glob("*sds.txt")
    
    unconverted = []
    for p in pdfs: 
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    pdfToText(unconverted)
    
    fileList = glob("*.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
