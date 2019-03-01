# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 11:56:52 2019

@author: ALarger
"""
import os
from glob import glob

def pdf_to_text(files):
    """
    Converts pdf files into text files
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\'
    
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk", "-layout",pdf])
        os.system(cmd)
    return

def main():
    os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Siri\bbb pdfs')    
    file_list = glob("*.pdf")
    n_pdfs = len(file_list)
    n_txts = len(glob("*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(file_list)    
    return

if __name__ == "__main__": main()