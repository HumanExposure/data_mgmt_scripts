# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 09:22:41 2019

@author: ALarger
"""

import os, string, csv
import pandas as pd
from glob import glob

def main():
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    os.chdir(r'L:\Lab\HEM\ALarger\Clorox\The Clorox Company 1\Right half txt files')    
    file_list = glob("*.txt")
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
    i = 0 #file number
    k=0 #line number
    oldLine = 0
    numFiles=len(file_list)
    for file in file_list:
        i+=1
        print(i/numFiles*100,'%')
        ifile = open(file, 'r', encoding='utf-8')
        ID = file.replace('document_','')
        ID = ID.replace('.txt','')
        prod = ''
        date = ''
        use = ''
        tname = ''
        inIngred = False #Flag for if it is in the ingredients section
        prodInfo = csv.reader(open(r'L:\Lab\HEM\ALarger\Clorox\The Clorox Company 1\Clorox 1 Product Info.csv'))
        for row in prodInfo:
            if row[0] == ID:
                tname = row[1]
                prod = row[2]
                date = row[3]
                use = row[5]
                break
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            k+=1
            if inIngred == True:
                for element in cline:
                    if 'none of the' in element or 'threshold limit' in element or 'note' in element or 'substance can' in element:
                        inIngred = False #leaving ingredient list
                        break
                    if 'contains' in element or 'regulated' in element or 'established' in element or 'ppm' in element or 'tlv' in element or 'respirable' in element or 'mg/m' in element or 'limit' in element or 'total dust' in element or 'natural and nonpathogenic' in element or 'n/a' in element or 'none' in element or 'varies' in element or 'acgih' in element or 'chamber' in element or '(mist' in element or 'osha' in element or 'inhalable' in element or 'stel' in element:
                        continue #passes lines that aren't a chem name, cas number, or concentration
                    elif 'cas' in element:
                        casN[-1] = element.strip('cas #')
                    elif '%' in element and any(c.isalpha() for c in element) == False:
                        centC[-1] = element 
                        units[-1] = 3
                    elif len(element) > 3: 
                        if len(element.split(' ')[0]) <= 2:
                            element = ' '.join(element.split(' ')[1:])
                        if any(c.isalpha() for c in element) == False:
                            continue
#                        print(ID,element)
                        if k == (oldLine + 1):
                            chemName[-1] = chemName[-1] + ' ' + element
                            oldLine = k
                        else:
                            prodID.append(ID)
                            templateName.append(tname)
                            prodName.append(prod)
                            msdsDate.append(date)
                            rev.append('')
                            recUse.append(use)
                            casN.append('')
                            chemName.append(element)
                            funcUse.append('')
                            minC.append('')
                            maxC.append('')
                            rank.append('')
                            centC.append('')
                            units.append(2)
                            oldLine = k
                            
            if 'ingredient' in cline or 'concentration' in cline:
                inIngred = True
                continue
            
        if len (prodID) == 0 or prodID[-1] != ID: #If the product information hasn't been appended (happends with products that list no ingredients)
            prodID.append(ID)
            templateName.append(tname)
            prodName.append(prod)
            msdsDate.append(date)
            rev.append('')
            recUse.append(use)
            casN.append('')
            chemName.append('')
            funcUse.append('')
            minC.append('')
            maxC.append('')
            rank.append('')
            centC.append('')
            units.append(2)

    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'prod_name':prodName, 'doc_date':msdsDate, 'rev_num':rev, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':units, 'ingredient_rank':rank, 'raw_central_comp':centC})
    df.to_csv(r'L:\Lab\HEM\ALarger\Clorox\The Clorox Company 1\Clorox 1 Extracted Text.csv',index=False, header=True, date_format=None)
    
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
#    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)
    
if __name__ == "__main__": main()