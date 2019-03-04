# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 09:00:11 2019

@author: ALarger
"""

import os, string, csv
import pandas as pd
from glob import glob

def pdf_to_text(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\'
    
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table",pdf])
        os.system(cmd)
        
    return

def extract_data(file_list):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    msdsDate = []
    prodID = []
    prodName = []
    chemName = []
    casN = []
    centC = []
    minC = []
    maxC = []
    units = []
    rank = []
    recUse = []
    templateName = []
    rev = []
    funcUse = []

    for file in file_list:
        ifile = open(file)
        ID = file.replace('document_','')
        ID = ID.replace('.txt','')
        prod = ''
        date = ''
        use = ''
        tname = ''
        header = False #Flag for collecting date
        ingList = False #Flag for collecting ingredient list
        identifier = False #Flag for collecting product name (incase it is multiple lines long)
        template = csv.reader(open(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Files\Bell Labs\Bell_Labs_1_extract_template.csv'))
        for row in template:
            if row[0] == ID:
                tname = row[1]
                break
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            try:
                if identifier == True:
                    if 'epa registration number:' in cline[0] or 'pmra registration number:' in cline[0]:
                        identifier = False
                    else: 
                        prod = prod + ' ' + cline[0]
                        print(prod)
                if 'product identifier:' in cline[0]:
                    prod = cline[0].replace('product identifier: ','')
                    prod = prod.replace('tm','')
                    identifier = True
                if 'relevant identified uses:' in cline[0]:
                    use = cline[0].replace('relevant identified uses: ','')
            except: pass
            if header == True:
                date = cline[1]
                header = False
            if 'date of issue:' in cline:
                header = True
            if ingList == True:
                if '(unlisted components are non-hazardous)' in cline:
                    ingList = False
                    break
                chem = ''
                cas = ''
                conc = ''
                if len(cline) == 3:
                    chem = cline[0]
                    cas = cline[1]
                    conc = cline[2]
                    if '%' in conc:
                        unit = 3
                        conc = conc.replace('%','')
                    else:
                        unit = 2
                        print(conc)
                        
                    prodID.append(ID)
                    templateName.append(tname)
                    prodName.append(prod)
                    msdsDate.append(date)
                    rev.append('')
                    recUse.append(use)
                    casN.append(cas)
                    chemName.append(chem)
                    funcUse.append('')
                    minC.append('')
                    maxC.append('')
                    units.append(unit)
                    rank.append('')
                    centC.append(conc)
                    
                elif len(cline) == 1:
                    chemName[-1] = chemName[-1] + cline[0]
            if 'cas no.' in cline:
                ingList = True
    
    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'prod_name':prodName, 'doc_date':msdsDate, 'rev_num':rev, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':units, 'ingredient_rank':rank, 'raw_central_comp':centC})
    df.to_csv(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Files\Bell Labs\Bell_Labs_1.csv',index=False, header=True, date_format=None)
        
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, commas, semicolons and excess spaces, and makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.replace(',','_')
    cline = cline.replace(';','_')
    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
def main():
    os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Files\Bell Labs')    
    pdfs = glob("*.pdf")
    n_pdfs = len(pdfs)
    n_txts = len(glob("*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(pdfs)
    
    n_txts = len(glob("*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")       
       extract_data(file_list)    

if __name__ == "__main__": main()