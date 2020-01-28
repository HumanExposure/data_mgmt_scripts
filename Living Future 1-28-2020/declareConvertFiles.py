# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 10:20:37 2019

@author: ALarger

https://wkhtmltopdf.org/downloads.html
"""

import os
from glob import glob

def html_to_pdf(files):
    """
    Converts pdf files into text files
    """
    execfile = "wkhtmltopdf.exe"
    execpath = 'C:\\Users\\alarger\\Documents\\wkhtmltopdf\\bin\\'

    i=0
    for file in files:
        i+=1
        print(i)
        newName = file.replace('.html','.pdf')
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,'--disable-external-links','--disable-internal-links','--disable-javascript',file,newName])
        os.system(cmd)

def main():
    path = 'L://Lab//HEM//ALarger//Declare_Living Future//'
    os.chdir(path)
    htmls = glob("*.html")
    pdfs = glob("*.pdf")
    file_list = []
    for f in htmls:
        if f.replace('.html','.pdf') in pdfs:
            continue
        else:
            file_list.append(f)
    html_to_pdf(file_list)

if __name__ == "__main__":
    main()
