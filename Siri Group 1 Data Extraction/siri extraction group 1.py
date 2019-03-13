# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:45:51 2019

@author: ALarger
"""
import os, string, csv
import pandas as pd
from glob import glob

def extract_data(file_list):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    msdsDate = []
    prodID = []
    msdsNum = []
    manufacturer = []
    chemName = []
    casN = []
    centC = []
    minC = []
    maxC = []
    units = []
    rank = []
    templateName = []
    prodName = []
    rev = []
    recUse = []
    funcUse = []
    i = 0
    j = 0
    lastID = 0
    f1 = False #flag that says if you are in the responsible party section and have not gotten the company name
    f2 = False #flag that says if you are in the composition section
    f3 = False #flag to get rest of chem name if it goes on for multiple lines
    skipLine = False #flag to skip the next line
    for file in file_list:
        ifile = open(file)
        r = 0
        if i != 0 and ID != lastID: #Appends the info from the last product if it didnt have ingredients
            print(ID)
            msdsDate.append(date)
            prodID.append(ID)
            lastID = ID
            msdsNum.append(num)
            manufacturer.append(manuf)
            chemName.append('')
            casN.append('')
            templateName.append(tname)
            prodName.append(prod)
            rev.append('')
            recUse.append('')
            funcUse.append('')
            units.append('2')
            rank.append('')
            centC.append('')
            minC.append('')
            maxC.append('')
        ID = file.replace('document_','')
        ID = ID.replace('.txt','')
        prod = '' #reset variables
        date = ''
        manuf = ''
        num = ''
        chem = '' 
        cas = ''
        unit = 2
        conc = ''
        template = csv.reader(open(r'L:\Lab\HEM\ALarger\Extraction Files\Siri\SIRI_CPCat_data_1_extract_template.csv'))
        for row in template:
            if row[0] == ID:
                tname = row[1]
                break
        i+=1
        print(i/16902*100,'%')
        for line in ifile:             
            cline = cleanLine(line)
            if cline == '': continue
            if skipLine == True:
                skipLine = False
                continue
            if 'product id:' in cline:
                prod = cline.replace('product id:','')
            if 'msds date:' in cline and date == '':
                date = cline.replace('msds date:','')
                if '(' in date: #gets rid of phone number if it is thrown in with date
                    date = date.split('(')[0]
                    date = date.strip()
                if '    ' in date:
                    date = date.split('    ')
                    if '/' in date[0]:
                        date = date[0]
            if 'product id:' in cline and 'msds date:' in cline: #splits product id and date if they are in the same line
                cline = cline.split(':')
                prod = cline[1]
                date = cline[-1]
            if 'msds num:' in cline:
                num = cline.replace('msds num:','')
                num = num.strip()
            if 'responsible party' in cline: f1 = True
            if f1 == True and 'name:' in cline:
                manuf = cline.replace('name:','')
                manuf = manuf.strip()
                f1 = False
            if 'ingredients' in cline and f2 == False:
                f2 = True
                skipLine = True
                continue
            if f2 == True:
                if '======' in cline:
                    f2 = False
                    f3 = False
                    if chem != '':
                        msdsDate.append(date)
                        prodID.append(ID)
                        lastID = ID
                        msdsNum.append(num)
                        manufacturer.append(manuf)
                        chemName.append(chem)
                        casN.append(cas)
                        templateName.append(tname)
                        prodName.append(prod)
                        rev.append('')
                        recUse.append('')
                        funcUse.append('')
                        units.append(unit)
                        rank.append(r)
                        if '-' in conc:
                            conc = conc.split('-')
                            minC.append(conc[0].strip())
                            maxC.append(conc[1].strip())
                            centC.append('')
                        else:
                            conc.strip()
                            centC.append(conc)
                            minC.append('')
                            maxC.append('')
                        chem = '' #reset variables
                        cas = ''
                        unit = 2
                        conc = ''
                if '---------' in cline and chem != '': #Appends information from last ingredient
                    f3 = False
                    msdsDate.append(date)
                    prodID.append(ID)
                    lastID=ID
                    msdsNum.append(num)
                    manufacturer.append(manuf)
                    chemName.append(chem)
                    casN.append(cas)
                    templateName.append(tname)
                    prodName.append(prod)
                    rev.append('')
                    recUse.append('')
                    funcUse.append('')
                    units.append(unit)
                    if chem == '':
                        rank.append('')
                    else:
                        rank.append(r)
                    if '-' in conc:
                        conc = conc.split('-')
                        minC.append(conc[0].strip())
                        maxC.append(conc[1].strip())
                        centC.append('')
                    else:
                        conc.strip()
                        centC.append(conc)
                        minC.append('')
                        maxC.append('')
                    chem = '' #reset variables
                    cas = ''
                    unit = 2
                    conc = ''
                if 'cas:' in cline:
                    cas = cline.replace('cas:','')
                elif 'name:' in cline:
                    chem = cline.replace('name:','')
                    chem = chem.strip()
                    f3 = True #flag to get rest of chem name
                    r += 1
                elif '% wt:' in cline or 'percent by wt:' in cline:
                    f3 = False
                    conc = cline.replace('% wt:','')
                    conc = conc.replace('percent by wt:','')
                    unit = 3
                    conc = conc.replace('%','')
                    if 'ppm' in conc:
                        conc = conc.replace('ppm','')
                        unit = 16
                elif '% low wt:' in cline:
                    f3 = False
                    unit = 3
                    conc = cline.replace('% low wt:','') + '-'
                elif '% high wt:' in cline:
                    conc = conc + cline.replace('% high wt:','')
                elif '> wt:' in cline:
                    f3 = False
                    unit = 3
                    conc = '>' + cline.replace('> wt:','')
                    if 'ppm' in conc:
                        conc = conc.replace('ppm','')
                        unit = 16
                elif '< wt:' in cline:
                    f3 = False
                    unit = 3
                    conc = '<' + cline.replace('< wt:','')
                    if 'ppm' in conc:
                        conc = conc.replace('ppm','')
                        unit = 16
                elif 'limits:' in cline or 'osha pel:' in cline or 'acgih tlv:' in cline or '===' in cline:
                    f3 = False
                elif f3 == True:
                    chem = chem + ' ' + cline
        if i%5000 == 0: #creates a new csv every 5000 products so that it can be loaded into factotum
            j += 1
            df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'prod_name':prodName, 'doc_date':msdsDate, 'rev_num':rev, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':units, 'ingredient_rank':rank, 'raw_central_comp':centC})
            path = r'L:\Lab\HEM\ALarger\Extraction Files\Siri\siri_1.'+str(j)+'.csv'
            df.to_csv(path,index=False, header=True, date_format=None)
            msdsDate = []
            prodID = []
            msdsNum = []
            manufacturer = []
            chemName = []
            casN = []
            centC = []
            minC = []
            maxC = []
            units = []
            rank = []
            templateName = []
            prodName = []
            rev = []
            recUse = []
            funcUse = []
            
    j += 1 #creates csv after last product is extracted
    df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'prod_name':prodName, 'doc_date':msdsDate, 'rev_num':rev, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'report_funcuse':funcUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':units, 'ingredient_rank':rank, 'raw_central_comp':centC})
    path = r'L:\Lab\HEM\ALarger\Extraction Files\Siri\siri_1.'+str(j)+'.csv'
    df.to_csv(path,index=False, header=True, date_format=None)
        
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
    return(cline)
    
def main():
    os.chdir(r'L:\Lab\HEM\ALarger\Extraction Files\Siri\Data Group 1')    
    file_list = glob("*.txt")
    extract_data(file_list)

if __name__ == "__main__": main()
