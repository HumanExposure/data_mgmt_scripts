# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 11:45:14 2019

@author: ALarger

3M Data Extraction
Note: Many documents are for multi-product "kits". For these, a list of all of the ingredients all components was made, and concentration was ignored
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
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.00\\bin64\\' #Path to execfile
    i=0
    numFiles = len(files)
    for file in files:
        i+=1
        print(i/numFiles*100,'%')
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
    prodID = [] #list of product IDs
    templateName = [] #list of file names matching those in the extacted text template
    prodName = [] #list of product names
    msdsDate = [] #list of msdsDates
    rev = [] #list of revision numbers
    recUse = [] #list of recommended uses of products
    casN = [] #list of CAS numbers
    chemName = [] #list of chemical names
    funcUse = [] #list of functional uses of each chemical
    minC = [] #list of minimum concentrations
    maxC = [] #list of maximum concentrations
    units = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...)
    rank = [] #list of ingredient ranks
    centC = [] #list of central concentrations
    kitList = [] #list of kits (multi-product pdfs) in the data group
    i = 0
    k=0
    numFiles=len(file_list)
    for file in file_list:
        i+=1
#        print(i/numFiles*100,'%')
        ifile = open(file)
        ID = file.replace('document_','')
        ID = ID.replace('.txt','')
        prod = ''
        date = ''
        use = ''
        tname = ''
        inUse = False #Flag for if you are in the product use subsection
        inIngred = False #Flag for if you are in the ingredients section
        inName = False #Flag for if you are in the product name 
        gotInfo = False
        kit = False
        kitIngList = [] #list of ingredients in kit to avoid repeats
        template = csv.reader(open(r'L:\Lab\HEM\ALarger\3M\3M Occupational Health and Safety\3M_Occupational_Health_and_Safety_extract_template.csv'))
        for row in template:
            if row[0] == ID:
                tname = row[1]
                break
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            if inName == True:
                if 'manufacturer:' in cline:
                    inName = False
                    continue
                else:
                    prod = prod + ' ' + ' '.join(cline)
            if 'product name:' in cline:
                if prod == '':
                    prod = ' '.join(cline[1:])
                    inName = True
                    continue
                elif 'kit' not in prod: #already having a product name indicates this is a kit with multiple products
                    prod = prod + ' kit'
                    k += 1
                    kitList.append(ID)
                    kit = True
            elif 'issue date:' in cline and gotInfo == False:
                date = cline[-1]
            if 'product use:' in cline and gotInfo == False:
                inUse = True
                continue
            if inUse == True: #collect use information
                if 'section 2: ingredients' in cline or 'limitations on use:' in cline or 'section' in cline[0]:
                    inUse = False
                    continue
                elif len(cline)>1:
                    if use == '': use = ' '.join(cline[1:])
                    else: use = use + '/' + ''.join(cline[1:])
                else:
                    use = use + ' ' + cline[0]
                if len(use) >= 100: #Use can't have >100 characters in factotum
                    use = use[0:96] + '...'
                    inUse = False
                    continue
            if 'ingredient' in cline and 'c.a.s. no.' in cline and '% by wt' in cline:
                inIngred = True
                gotInfo = True
                continue
            if inIngred == True:
                chem = ''
                cas = ''
                conc = ''
                if 'section 3: hazards identification' in cline or '_____________________' in cline[0]:
                    inIngred = False
                    continue
                elif len(cline) != 3: #Normal ingredient lines contain 3 items. If an ingredient line doesn't have 3, print so they can be reviewed
                    print(ID,cline)
                if '* component' in cline[0]:
                    continue
                if len(cline) == 3: #Normal ingredient line
                    chem = cline[0]
                    cas = cline[1]
                    conc = cline[2]
                elif len(cline) == 2: #Weird ingredient line case
                    chemName[-1] = chemName[-1] + ' ' + cline[0]
                    casN[-1] = casN[-1] + ' ' + cline[1]
                    continue
                elif len(cline) == 1: #Weird ingredient line case
                    if cline[0][0] == '*' or 'the polyester film release liner' in cline[0] or 'page' in cline[0]:
                        inIngred = False
                    else:
                        chemName[-1] = chemName[-1] + ' '+ cline[0]
                    continue
                elif len(cline) == 4: #weird ingredient line case
                    if cline[1] == '3-carboxy-1-':
                        chem = cline[0] + cline[1]
                        cas = cline[2]
                        conc = cline[3]
                    elif cline[2] == 'trade secret' or cline[2] == 'mixture':
                        chem = cline[0] + ' ' + cline[1]
                        cas = cline[2]
                        conc = cline[3]
                    else:
                        chem = cline[0]
                        cas = cline[1]
                        if '-' in cline[2] or '-' in cline[3]:
                            conc = cline[2] + cline[3]
                        else:
                            conc = cline[2] + '- ' + cline[3]
                elif len(cline) == 5: #Weird ingredient line case
                    chem = cline[0]
                    cas = cline[1]
                    if 'typically' in cline[4]:
                        conc = cline[2] + '-' + cline[3] + cline[4]
                    else:
                        conc = cline[2] + cline[3] + cline[4]
                else: #Lines at end of list often have 6+ items
                    inIngred = False
                    continue
                if kit == True: #For kits: dont repeat ingredients and dont list concentrations
                    if chem in kitIngList:
                        continue
                    else:
                        conc = ''
                        kitIngList.append(chem)
                prodID.append(ID) #Append lists
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
                rank.append('')
                centC.append(conc)
                if conc == '': units.append(2)
                else: units.append(3)

    print(kitList) #print data document ids of the kits for reference
    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'prod_name':prodName, 'doc_date':msdsDate, 'rev_num':rev, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':units, 'ingredient_rank':rank, 'raw_central_comp':centC})
    df.to_csv(r'L:\Lab\HEM\ALarger\3M\3M Occupational Health and Safety\3M Occupational Health and Safety Extracted Text.csv',index=False, header=True)
        
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, commas, semicolons and excess spaces, and makes all characters lowercase
    splits lines into lists for extracting tables
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
    os.chdir(r'L:\Lab\HEM\ALarger\3M\3M Occupational Health and Safety')    
    pdfs = glob("*.pdf")
    n_pdfs = len(pdfs)
    n_txts = len(glob("*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(pdfs)
    
    n_txts = len(glob("*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")       
       extract_data(file_list)    

if __name__ == "__main__": main()
