# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 12:37:12 2018

@author: ALarger
"""
import os,string 
import pandas as pd
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
        cmd = " ".join([cmd,"-nopgbrk","-table",pdf])
        os.system(cmd)
        
    return
    
def text_to_csv(files):
    """
    Extracts data from text file into a Pandas dataframe
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    revDate = []
    version = []
    sdsNum = []
    prodName = []
    prodCode = []
    manufacturer = []
    recUse = []
    chemName = []
    casN = []
    centC = []
    minC = []
    maxC = []
    units = []
    docName = []
    for file in files:
        ifile = open(file)
        i = 0 #line number
        j = 1 #rank
        weird = False #Flag for if the header format matches that of document_160952.pdf
        gotInfo = False #Flag for if the version number, revision date and SDS number were collected
        pdfName = file.replace('.txt','.pdf')
        name = ''
        vers = ''
        date = ''
        sds = ''
        manuf = ''
        code = ''
        use = ''
        for line in ifile:
            if line == '/n': continue
            cline = cleanLine(line)
            if cline == []: continue
            if i == 0:
                for line2 in ifile:
                    dline = clean(line2)
                    dline = dline.lower()
                    dline = dline.strip()
                    if dline == []: continue
                    if "this industrial" in dline:
                        break
                    name = name + ' ' + dline
                    name = name.strip()
            if weird == True:
                vers = cline[0]
                date = cline[1]
                sds = cline[2]
                gotInfo = True
                weird = False
                
            try:
                if 'version' in cline[0] and gotInfo == False:
                    try:
                        if "date of last issue" in cline[3]:
                            weird = True
                        else:
                            vers = cline[0].strip('version ')
                            sds = cline[1].strip('sds number: ')
                            date = cline[2].strip('revision date: ')
                            gotInfo = True
                    except IndexError:
                        vers = cline[0].strip('version ')
                        sds = cline[1].strip('sds number: ')
                        date = cline[2].strip('revision date: ')
                        gotInfo = True
                if 'product code' in cline[0]:
                    code = cline[2]
                if 'company' in cline[0] and len(cline) == 3:
                    manuf = cline[2]
                if 'recommended use' in cline[0] and len(cline) == 3:
                    use = cline[2]
            except IndexError:
                pass
            
            try: 
                unit = ''
                minConc = ''
                maxConc = ''
                cConc = ''
                if 'chemical name' in cline[0] and 'cas-no' in cline[1]:
                    if '(% w/w)' in cline[2]:
                        unit = 3
                    else: unit = 2
                    for line3 in ifile:
                        cname = ''
                        cas = ''
                        concentration = ''
                        eline = cleanLine(line3)
                        if eline == []:
                            continue
                        if 'section 4' in eline[0]:
                            break
                        if len(eline) == 4:
                            eline[2:4] = [''.join(eline[2:4])]
                        if len(eline) == 3:
                            cname = eline[0]
                            cas = eline[1]
                            concentration = eline[2]
                        elif len(eline) == 2:
                            chemName[-1] = chemName[-1] + ' ' + eline[0]
                            casN[-1] = casN[-1] + ' ' + eline[1]
                            continue
                        elif len(eline) == 1:
                            chemName[-1] = chemName[-1] + ' ' + eline[0]
                            continue
                        else:
                            print(eline)
                            continue
                        if '-' in concentration:
                            minConc = concentration.split('-')[0]
                            minConc = minConc.strip()
                            maxConc = concentration.split('-')[1]
                            maxConc = maxConc.strip()
                            cConc = ''
                        else:
                            cConc = concentration.strip()
                            maxConc = ''
                            minConc = ''
                            
                        units.append(unit)
                        version.append(vers)
                        sdsNum.append(sds)
                        revDate.append(date)
                        docName.append(pdfName)
                        prodName.append(name)   
                        chemName.append(cname)
                        casN.append(cas)
                        centC.append(cConc)
                        minC.append(minConc)
                        maxC.append(maxConc)
                        prodCode.append(code)
                        manufacturer.append(manuf)
                        recUse.append(use)
            except IndexError:
                pass
            i = i + 1

    df = pd.DataFrame({'File Name': docName, 'Revision Date':revDate, 'Version':version, 'SDS Number':sdsNum, 'Product Name':prodName, 'Product Code':prodCode, 'Manufacturer':manufacturer, 'Recommended Use':recUse, 'Chemical Name':chemName, 'CAS-No':casN, 'Central Concentration': centC, 'Min Concentration': minC, 'Max Concentration': maxC, 'Unit':units})
    print(df)
    df.to_csv(r'C:/Users/alarger/Documents/Colgate-Palmolive PDFs/Colgate-Palmolive.csv',index=False, header=True, date_format=None)
    df.to_excel(r'C:/Users/alarger/Documents/Colgate-Palmolive PDFs/Colgate-Palmolive.xlsx')
              
def cleanLine(line):
    """
    Takes in a line of text and cleans it, removes excess spaces, makes all characters lowercase
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
    os.chdir(r'C:/Users/alarger/Documents/Colgate-Palmolive PDFs')
    
    pdfs = glob("document_*.pdf")
    n_pdfs = len(pdfs)
    n_txts = len(glob("document_*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(pdfs)
    
    n_txts = len(glob("document_*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")
       
       text_to_csv(file_list)

    
    return
    
if __name__ == "__main__": main()