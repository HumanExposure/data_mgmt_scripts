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
#        if i>=3:
#            break

#def makePdf(filename):
#    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
#    newName = filename.replace('.html', '.pdf')
#    pdfkit.from_file(filename,newName,configuration=config)

def main():
    path = 'L://Lab//HEM//ALarger//Skin Deep//Sun//'
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
#    i=0
#    for f in file_list:
#        i+=1
#        print(i/10393, '%')
#        makePdf(f)
##        newName = f.replace('.html',path + 'pdfs//' + '.pdf')
##        try:
##            pdfkit.from_file(f,newName,configuration=config)
##        except:
##            print(f)
        
if __name__ == "__main__":
    main()
