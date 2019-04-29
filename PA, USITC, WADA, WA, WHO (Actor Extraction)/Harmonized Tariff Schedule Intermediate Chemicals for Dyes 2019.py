# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 09:42:34 2019

@author: ALarger


Harmonized Tariff Schedule of the United States (2019) Intermediate Chemicals for Dyes Appendix
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
    
    for file in file_list:
        ifile = open(file)
        ID = file.replace('document_','').replace('.txt','')
        tname = 'Intermediate Chemicals for Dyes.pdf'
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            if '...' in line:
                chemName.append(cline[0].strip('.'))
                casN.append(cline[-1].strip('.'))
                prodID.append(ID)
                templateName.append(tname)
                msdsDate.append('2019')
                recUse.append('')
                catCode.append('')
                descrip.append('')
                code.append('')
                sourceType.append('ACToR Assays and Lists')

    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})
    df.to_csv(r"L:\Lab\HEM\ALarger\Actor Automated Extraction\PA, USITC, WADA, WA, WHO\Harmonized Tariff Schedule of the United States (2019) Intermediate Chemicals for Dyes Appendix\Harmonized Tariff Schedule Intermediate Chemicals for Dyes 2019.csv",index=False, header=True, date_format=None)        

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
    cline = cline.split("..")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Actor Automated Extraction\PA, USITC, WADA, WA, WHO\Harmonized Tariff Schedule of the United States (2019) Intermediate Chemicals for Dyes Appendix')    
    pdfs = glob("*.pdf")
    n_pdfs = len(pdfs)
    n_txts = len(glob("*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(pdfs)
    
    n_txts = len(glob("*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")       
       extract_data(file_list)    

if __name__ == "__main__": main()