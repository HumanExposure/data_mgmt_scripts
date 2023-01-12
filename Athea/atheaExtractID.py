# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 17:21:48 2022

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
    cline = line.replace('–','-')
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
        component = ''
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
        
        
        template = csv.reader(open('athea_laboratories_ingredient_disclosure_documents_20221223.csv'))
        for row in template:
            if row[6] == file.replace('_new.txt','.pdf'):
                ID = row[0]
                break
        if ID == '':
            continue
        
        
        prodname = cleaned.split('product name:')[-1].split('\n')[0].strip() #get product name
        if 'revision date:' in cleaned:
            date = cleaned.split('revision date:')[-1].split('\n')[0] #get date
        else:
            date = cleaned.split('date of disclosure:')[-1].split('\n')[0] #get date
    
        cat = cleaned.split('description:')[1].split('\n')[0].strip() #Get raw category
        
        tables = camelot.read_pdf(file.replace('_new.txt','.pdf'),pages='all', flavor='lattice')
        i=0 
        chemplace=0
        casplace=1
        for table in tables:
            df = tables[i].df
            for index, row in df.iterrows():
                if row[0].strip().lower() in ['cas rn','cas','casr rn','cas no']: #cas in first column
                    chemplace=1
                    casplace=0
                elif row[0].lower().replace(' ','').replace('\n','').strip() == 'name': #chem name in first column
                    continue
                elif len(row) >2: 
                    if row[0] == '' and row[1] == '' and row[2] == '': continue
                    if row[casplace] == '' and row[chemplace] != '' and len(chem)>0 and 'Other components' not in row[chemplace]:
                        chem[-1] = (chem[-1] + ' ' + row[chemplace]).replace('\n',' ').replace('  ',' ').strip()
                        if row[2] != '': print(file, row)
                        continue
                    chem.append(row[chemplace].replace('\n',' ').replace('  ',' ').strip())
                    cas.append(row[casplace].replace('\n',' ').replace('  ',' ').strip())
                    use.append(row[2].replace('\n',' ').replace('  ',' ').strip())
                    minC.append('')
                    maxC.append('')
                    centC.append('')
                    unit.append('')
            i+=1
        
        # cleaned = cleanLine(text)
        # lines = cleaned.split('\n')
        # inIngredients = False
        # chemplace=0
        # casplace=1
        # concernList = ['none','eu','iarc','us','ca','glwqa','iris','marine','ny','prop','wa','allergens','disruptors','atsdr','sensitizers','toxicants','aoec','chemicals','annex','action','cancer','hazards','neurotoxicants','ntp']
        # funcWords = ['by-','product/contamina','by-product or']
        # for line in lines: 
        #     if inIngredients == True:
        #         if 'this information' in line or 'effects on human health' in line: 
        #             inIngredients = False
        #             continue
        #         line = line.split('  ')
        #         for l in range(len(line)):
        #             line[l] = line[l].strip()
        #         line = list(filter(None,line))
        #         if len(line)==0: continue
        #         if line[-1].split(' ')[0].strip(',') in concernList:
        #             line=line[:-1]
        #         if len(line)==0: continue
        #         elif len(line)>2:
        #             chem.append(line[chemplace].strip())
        #             cas.append(line[casplace].strip())
        #             use.append(line[2])
        #         elif len(chem)==0:
        #             if len(line)==1:
        #                 chem.append(line[0].strip())
        #                 cas.append('')
        #                 use.append('')
        #             else:
        #                 chem.append(line[0].strip())
        #                 cas.append('')
        #                 use.append(line[1].strip())
        #         elif len(line) == 2:
        #             if line[casplace] in ['proprietary','mixture','trade secret'] or all(x in '1234567890 -' for x in line[casplace]):
        #                 if cas[-1] == '':
        #                     chem[-1] =(chem[-1]+' '+line[chemplace]).strip()
        #                     cas[-1] = line[casplace].strip()
        #                 else:
        #                     chem.append(line[chemplace].strip())
        #                     cas.append(line[casplace].strip())
        #                     use.append('')
        #             else:
        #                 if line[-1] == 'agent':
        #                     chem[-1] = (chem[-1] + ' ' +line[0]).strip()
        #                     use[-1] = (use[-1]+' '+line[1]).strip()
        #                 else:
        #                     chem.append(line[0])
        #                     cas.append('')
        #                     use.append(line[1])
        #         else:
        #             print(file, len(line), line)
        #     if 'name' in line and 'cas' in line:
        #         inIngredients = True
        #         if 'cas' in line.split('name')[0]:
        #             casplace=0
        #             chemplace=1
        
                
                
        if chem == []:
            chem = ['']
            cas = ['']
            use = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            
    
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
        componentList.extend([component]*n)
        
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv('athea id extracted text.csv',index=False, header=True)

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Athea') #Folder pdfs are in
    pdfs = glob("*.pdf")    
    uncopied = []
    extractable = glob('*new.pdf')
    for p in pdfs:
        if 'new' not in p and p.replace('.pdf','_new.pdf') not in extractable:
            uncopied.append(p)
            
    for u in uncopied:
        new_pdf = Pdf.new()
        with Pdf.open(u) as pdf:
            pdf.save(u.replace('.pdf','_new.pdf'))
        
    pdfs = glob("*_new.pdf")
    txts = glob("*_new.txt")
    unconverted = []
    for p in pdfs: 
        if p.replace('.pdf','.txt') not in txts:
            unconverted.append(p)
    pdfToText(unconverted)
    
    fileList = glob("*id_new.txt")       
    extractData(fileList)    


if __name__ == "__main__": main()
