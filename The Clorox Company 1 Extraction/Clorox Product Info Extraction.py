# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 14:53:34 2019

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
    os.chdir(r'L:\Lab\HEM\ALarger\Clorox\The Clorox Company 1\Full page txt files -table')    
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
    i = 0
    numFiles=len(file_list)
    for file in file_list:
        i+=1
        print(i/numFiles*100,'%')
        ifile = open(file)
        ID = file.replace('document_','')
        ID = ID.replace('.txt','')
        prod = ''
        date = ''
        use = ''
        tname = ''
        template = csv.reader(open(r'L:\Lab\HEM\ALarger\Clorox\The Clorox Company 1\The_Clorox_Company_1_extract_template.csv'))
        for row in template:
            if row[0] == ID:
                tname = row[1]
                break
        for line in ifile:
            cline = cleanLine(line)
            if cline == []: continue
            try:    
                if 'product:' in cline[0]:
                    if len(cline) > 2:
                        prod = ' '.join(cline[1:])
                    else: prod = cline[1]
                elif 'product:' in cline[1]:
                    if len(cline) >3:
                        prod = ' '.join(cline[2:])
                    else: prod = cline[2]
            except: pass
            try:    
                if 'date prepared' in cline[-1] or 'date prepared' in cline[-2]:
                        date = ''.join(j for j in cline[-1] if j.isdigit() or j == '/')
            except: pass
            if 'description:' in cline[0]:
                use = ' '.join(cline[1:])           
        
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
        units.append('')

    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'prod_name':prodName, 'doc_date':msdsDate, 'rev_num':rev, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':units, 'ingredient_rank':rank, 'raw_central_comp':centC})
    df.to_csv(r'L:\Lab\HEM\ALarger\Clorox\The Clorox Company 1\Clorox 1 Product Info.csv',index=False, header=True, date_format=None)
        
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
    
if __name__ == "__main__": main()