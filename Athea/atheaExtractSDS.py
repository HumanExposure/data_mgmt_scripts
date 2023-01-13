# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:21:23 2022

@author: ALarger
"""

import os, string, csv, re
import pandas as pd
from glob import glob
import PyPDF2
from pikepdf import Pdf
import camelot


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
    cline = line.replace('–','-').replace('≤','<=')
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
        
     
            
        ifile = open(file, encoding = 'utf8')
        text = ifile.read()
        
        cleaned = cleanLine(text)
        cleaned = re.sub(' +', ' ', cleaned)
        # re.sub(' +', ' ', cleaned)
        
    
        if cleaned == '': print(file)
                
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        use = []
        component = []
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
        
        
        template = csv.reader(open(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Athea/athea_laboratories_sds_documents_20221214.csv')) #Get factotum document ids
        for row in template:
            if row[6] == file.replace('_new.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
        
        
        prodname = cleaned.split('product name :')[-1].split('\n')[0].strip() #get product name
        prodname = re.sub(' +', ' ', prodname) #get rid of extra spaces
        date = cleaned.split('revision date')[-1].strip(': ').split(' ')[0].strip() #get date
        if rev == '' and 'version' in cleaned:
            rev = cleaned.split('version')[-1].strip(': ').split(' ')[0].strip() #Get revision number
    
        cat = cleaned.split('use of the substance/mixture')[-1].split('product code')[0].split('safety data sheet')[0].replace('\n',' ').strip(': ') #Get raw category
        cat = re.sub(' +', ' ', cat) #get rid of extra spaces
        
        
        cleaned = cleanLine(text)
        lines = cleaned.split('\n')
        inIngredients = False
        betweenPages = False
        for line in lines: #Extract ingredient section
            if inIngredients == True:
                if 'section 4' in line or 'a specific chemical' in line or 'any concentration shown' in line or 'all hazardous chemicals' in line: #Out of ingredients section
                    inIngredients = False
                    continue
                if 'date of issue' in line or 'issue date' in line or 'revision date' in line: #Skip header and footer lines if ingredients section spans two pages
                    betweenPages = True
                    continue
                line = line.split(' eye ')[0].split(' aquatic ')[0].split(' ox.')[0].split(' stot ')[0].split(' acute ')[0].split(' skin ')[0].split(' flam. ')[0].split(' not classified')[0].split(' met. ')[0].split(' asp. ')[0].split(' repr. ')[0].split(' carc. ')[0].split(' muta. ')[0].split(' compressed gas')[0].split(' h332')[0].split(' h331')[0].split(' lact.')[0].split(' granted date:')[0].split(' filing date')[0].split(' press. gas')[0].split(' resp.')[0].strip() #get rid of the classification column
        
                
                line = line.split('(cas')
                line = list(filter(None,line))
                if betweenPages == True:
                    if len(line)>0 and ('safety data sheet' in line[0] or 'name' in line[0]):
                        betweenPages = False
                    continue

                if len(line) == 0 or 'name' in line[0]: #skip blank lines and headers
                    continue
       
                if len(line)>1:
                    chem.append(line[0])
                    cas.append(line[1].split(')')[1].strip().split('  ')[0])
                    centC.append(line[1].split(cas[-1])[-1].strip(') '))
                    use.append('')
                    
                    #Fix weird cases
                    if '9207' in centC[-1]:
                        cas[-1] = cas[-1] +' '+'9207'
                        centC[-1]=centC[-1].replace('9207','').strip()
          
                else: 
                    # print(file,len(line),line)
                    if line[0][0]=='(' and line[0][-1] == ')':
                        use[-1] = line[0].strip('() ')
                    else: 
                        chem[-1]=chem[-1]+' '+line[0]
              
            if 'name' in line and 'product identifier' in line: #In ingredients section
                inIngredients = True
  
        
                
                
        if chem == []:
            chem = ['']
            cas = ['']
            centC = ['']
            use = ['']
      
        for c in range(0,len(chem)): #clean up concentrations and names
            chem[c] = re.sub(' +', ' ', chem[c])
            minC.append('')
            maxC.append('')
            # use.append('')
            component.append('')
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
        filenameList.extend([file.replace('_new.txt','.pdf')]*n)
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
    df.to_csv('athea sds extracted text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Athea') #Folder pdfs are in
    pdfs = glob("*.pdf")    
    uncopied = []
    extractable = glob('*new.pdf')
    for p in pdfs:
        if 'new' not in p and p.replace('.pdf','_new.pdf') not in extractable:
            uncopied.append(p)
            
    for u in uncopied: #Make copies of the pdfs that can be extracted (original copies are secured)
        new_pdf = Pdf.new()
        with Pdf.open(u) as pdf:
            pdf.save(u.replace('.pdf','_new.pdf'))
        
    pdfs = glob("*_new.pdf")
    txts = glob("*_new.txt")
    unconverted = []
    for p in pdfs:  #Convert to txt
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    pdfToText(unconverted)
    
    fileList = glob("*sds_new.txt") #extract text
    extractData(fileList)    


if __name__ == "__main__": main()
