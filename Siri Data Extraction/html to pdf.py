# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 13:06:21 2019

@author: ALarger
"""

from xhtml2pdf import pisa # import python module
import csv

def main():
    with open(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\siriall_template.csv','r') as siriall:
        reader = csv.reader(siriall)
        i = 0
        for row in reader:
            url = row[3]
            url = url.strip("();'")
            url = url.split('/')
            try:
                path = 'L://Lab//NCCT_ACToR//BUILD_2019Q1//data_collection_data//siri.org//DataPrep//msds//' + url[4] + '//siri.org//msds//' + url[4] + '//' + url[5] + '//' + url[6]
            except IndexError:
                continue
            i +=1
            sourceHtml = open(path)
            outputFilename = url[6].replace('.html','.pdf')
            outpath = 'L://Lab//NCCT_ACToR//BUILD_2019Q1//data_collection_data//siri.org//DataPrep//msds//' + url[4] + '//siri.org//msds//' + url[4] + '//' + url[5] + '//' + outputFilename
            print i/252753*100, '%'
            convertHtmlToPdf(sourceHtml, outpath)
    

# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename):
#    open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")
    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(sourceHtml, dest=resultFile) # file handle to recieve result
    # close output file
    resultFile.close() # close output file
    # return True on success and False on errors
    return pisaStatus.err
# Main program
if __name__ == "__main__":
    pisa.showLogging()
    main()
