# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 11:57:22 2022

@author: ALarger
"""

import os, string, csv, re
import pandas as pd
from glob import glob
import PyPDF2


def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    for file in files:
        pdffileobj=open(file,'rb')
        pdfreader=PyPDF2.PdfFileReader(pdffileobj)
        x=pdfreader.numPages
        text=''
        newname=file.replace('.pdf','.txt')
        file1=open(newname,"a", encoding="utf-8")
        for y in range(0,x):
            pageobj=pdfreader.getPage(y)
            text=pageobj.extractText()  
            file1.writelines(text)
            file1.writelines('\n')
            
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
        revDate = ''
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
        
        
        func = ''
        subname = '' #substance name
        subcas = '' #substance cas
        
        
        prodname = cleaned.split('product name \n')[1].split('\n')[0].strip(' :') #get product name
        rev = cleaned.split('version \n')[1].split('revision')[0].strip(': ') #get version number
        revDate = cleaned.split('revision date: \n')[1].split('sds')[0].strip(': ') #get version number
        cat = cleaned.split('recommended use \n')[1].split('restrictions on use')[0].split('section 2')[0].replace('\n',' ').strip(' :,') #Get raw category
        func = cleaned.split('recommended use \n')[1].split('restrictions on use')[0].split('section 2')[0].replace('\n',';').strip(' :;,').replace(' ;',';').replace(';(e',' (e').replace('-;','').replace('and;','and ') #functional use is like raw category, but split into list
        
        section3 = cleaned.split('section 3')[1].split('section 4')[0]
        # print(file,section3)
        
        section3=section3.replace('compo nents','components').replace('com ponents','components').replace(' -','-').replace('- ','-')
        if 'substance name' in section3:
            subname = section3.split('substance name')[-1].split('cas-no')[0].replace('\n',' ').strip(' :.').strip()
            if 'cas-no' in section3:
                subcas = section3.split('cas-no')[1].split('components')[0].split('safety')[0].replace('\n',' ').strip(' :.').strip()
       
        
        section3 = section3.split('components')[-1]
        section3 = section3.split('\n')
        betweenPages = False
        
        for s in section3: #iterate through every line in section 3
            s=s.strip()
            if s == '': #Skip blank lines
                continue
            
            if all(x in '1234567890 /' for x in s) or s == 'safety data sheet':
                betweenPages = True
                continue
            if 'date' in s:
                betweenPages = False
                continue
            if betweenPages == True: continue
            
            if 'actual concentration' in s:
                break
            if 'concentration' in s.replace(' ','') or 'substance' in s or 'cas-no.' in s or 'components' in s.replace(' ','') or 'version' in s or 'composition' in s: #Skip lines that aren't composition data
                continue
            if s[0] == ':' or s[-1] == ':': 
                continue
         
            s=s.replace(' -','-').replace('- ','-')#get rid of extra spaces in cas numbers
            s=s.replace(' / ','/')
            if s.split(' ')[0].count('/') == 1 and all(x in '1234567890/' for x in s.split(' ')[0]): #get rid of page numbers at beginning of chem names
                s = ' '.join(s.split(' ')[1:])
            casrns = re.findall(r'\b[1-9]{1}[0-9]{1,7}-\d{2}-\d\b', s)
            if len(casrns) == 0 and 'trade secret' in s:
                casrns = ['trade secret']
            elif len(casrns) == 0 and 'not assigned' in s:
                casrns = ['not assigned']
                
            if len(casrns) == 1:
                if len(unit)>0 and unit[-1] == '':
                    # print('here',file,s)
                    chem[-1] = (chem[-1] + ' ' + s.split(casrns[0])[0].strip()).strip()
                    cas[-1] = casrns[0]
                    centC[-1] = s.split(casrns[0])[-1].strip()
                    unit[-1] = '3'
                    
                else:
                    chem.append(s.split(casrns[0])[0].strip())
                    cas.append(casrns[0])
                    minC.append('')
                    maxC.append('')
                    centC.append(s.split(casrns[0])[-1].strip())
                    unit.append('3')
                    use.append('')
                
            elif s == 'no hazardous ingredients':
                continue
            else:
                
                if len(chem) == 0 or all(x in "1234567890,-' " for x in s) or s[0:4] == 'poly' or s.split(' ')[0] in['partially','mixture','reaction','quaternary','paraffin'] or s == "2.4'-trifluoro-1-" or s == '2-[2-(1-cyano-1-' or s == '2,6,8-trimethyl-4-' or s == '1,3,5-triallyl-1,3,5-triazine-' or s == 'n-[3-': #Beginning of chemical name
 
                    chem.append(s)
                    cas.append('')
                    minC.append('')
                    maxC.append('')
                    centC.append('')
                    unit.append('')
                    use.append('')
              
                else: #End of chemical name
                    chem[-1] = (chem[-1]+' '+s).strip()
                    
        
            
            
        template = csv.reader(open('chemours_sds_documents_20221004.csv'))
        for row in template:
            if row[6] == file.replace('.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
            
        for line in ifile:
            
            cline = cleanLine(line)
            if cline == '': continue
                
           
                
        if chem == []:
            chem = [subname]
            cas = [subcas]
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            if subname != '' or subcas != '':
                use = [func]   
            else:
                use = ['']
        
        foundchem = False
        for x in range(len(chem)):
            
            chem[x] = chem[x].strip('# ') #clean chem names up
            
            if subcas.count('-') == 2 and subcas == cas[x]:
                use[x] = func
                foundchem = True
            elif subname != '' and subname.replace(' ','').replace('-','') == chem[x].replace(' ','').replace('-',''):
                use[x] = func
                foundchem = True
                
            
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
            
        if subname != '' and foundchem == False:
            print(file)
            
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([revDate]*n)
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
    df.to_csv('chemours extracted text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Chemours SDS') #Folder pdfs are in
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
