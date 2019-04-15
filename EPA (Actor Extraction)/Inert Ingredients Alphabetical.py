# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 12:11:11 2019

@author: ALarger

Inert Ingredients Ordered Alphabetically by Chemical Name- Lists 4A and 4B
"""

import os, string
import pandas as pd
from glob import glob

def pdf_to_text(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
    numFiles = len(files)
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
    prodID = []
    templateName = []
    msdsDate = []
    recUse = []
    catCode = []
    descrip = []
    code = []
    sourceType = []
    chemName = []
    casN = []
    chem = ''
    cas = ''
    
    for file in file_list:
        ifile = open(file)
        ID = file.replace('document_','').replace('.txt','')
        if ID == '1365240': tname = 'InertsList4a.pdf'
        else: tname = 'InertsList4b.pdf'
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
        

            if (cline[-1][-2:] == '4A' or cline[-1][-2:] == '4B') and len(cline[-1]) > 2: 
                cline[-1] = cline[-1].replace('4A','').replace('4B','')
                cline.append('4A')
#                print(cline)
#            if len(cline)==3 and '4' in cline[2] and cline[0].count('-') == 2:
#                chem = cline[1]
#                cas = cline[0]
            if len(cline) >= 3 and cline[0].count('-') == 2 and cline[0][0].isdigit() and cline[0][-1].isdigit() and (cline[-1] == '4B' or cline[-1] == '4A'): 
                chem = chem + ' ' + ' '.join(cline[1:-1])
                cas = cas + cline[0]
            elif len(cline) == 1 and (cline[0] == '4A' or cline[0] == '4B' or cline[0] == 'B'): pass
            elif 'Ingredients' in cline[0] or 'Updated' in cline[0] or 'Office' in cline[0] or 'Agency' in cline[0] or 'List' in cline[0] or 'CAS' == cline[0] or 'conclude' in cline[0] or 'adversely' in cline[0]:
                continue
            elif cline[0].count('-') == 2 and cline[0][0].isdigit() and cline[0][-1].isdigit() and cline[-1] != '4B' and cline[-1] != '4A':
                chem = chem + ' ' + ' '.join(cline[1:])
                cas = cas + cline[0]
            elif cline[0].count('-') != 2 and (cline[-1] == '4A' or cline[-1] == '4B' or cline[-1] == 'LISTNO'):
                if cline[0][-1].isdigit():
                    cas = cas + cline[0]
                    chem = chem + ' ' + ' '.join(cline[1:-1])
                else:
                    chem = chem + ' ' + ' '.join(cline[:-1])
            else: 
#                print(ID,cline)
                if cline[0][0].isdigit() and cline[0][1].isdigit():
                    cas = cas + cline[0]
                else: 
                    chem = chem + ' ' + ' '.join(cline)
            
            if cline[-1] == '4B' or cline[-1] == '4A' or cline[-1] == 'B' or cline[-1] == 'LISTNO': #Append list
                prodID.append(ID)
                templateName.append(tname)
                msdsDate.append('')
                recUse.append('')
                catCode.append('')
                descrip.append('')
                code.append('')
                sourceType.append('ACToR Assays and Lists')
                chemName.append(chem.strip())
                casN.append(cas)
                chem=''
                cas=''


    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
    df.to_csv(r"L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Inert Ingredients Alphabetical\Inert Ingredients Alphabetical.csv",index=False, header=True, date_format=None)        

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, commas, semicolons and excess spaces, and makes all characters lowercase
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.replace(',','_')
    cline = cline.replace(';','_')
    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\EPA\Inert Ingredients Alphabetical')    
    pdfs = glob("*.pdf")
    n_pdfs = len(pdfs)
    n_txts = len(glob("*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(pdfs)
    
    n_txts = len(glob("*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")       
       extract_data(file_list)    

if __name__ == "__main__": main()