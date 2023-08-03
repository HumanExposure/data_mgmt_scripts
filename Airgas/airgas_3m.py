# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 10:21:20 2023

@author: ALarger
"""


import os, string, csv, re
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

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters, commas, semicolons and excess spaces, and makes all characters lowercase
    splits lines into lists for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line)
    cline = cline.lower()
    cline = cline.strip()
    cline = cline.split("  ")
    cline = [x.strip() for x in cline if x != ""]
    return(cline)

def extract_data(file_list):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    idList = [] #list of product IDs
    filenameList = [] #list of file names matching those in the extacted text template
    prodnameList = [] #list of product names
    dateList = [] #list of msdsDates
    revList = [] #list of revision numbers
    catList = [] #list of product categories
    casList = [] #list of CAS numbers
    chemList = [] #list of chemical names
    useList = [] #list of functional uses of each chemical
    minList = [] #list of minimum concentrations
    maxList = [] #list of maximum concentrations
    unitList = [] #list of unit types (1=weight frac, 2=unknown, 3=weight percent,...)
    rankList = [] #list of ingredient ranks
    centList = [] #list of central concentrations
    componentList = [] #List of components



    i = 0
    for file in file_list:
        i+=1
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        chem = ''
        cas = ''
        conc = ''
        use = []
        component = []
        chemName = []
        casN = []
        minC = []
        maxC = []
        centC = []
        unit = []
        
        fname = file.replace('_new.txt','.pdf') #filename
        template = csv.reader(open(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/Factotum_Airgas_HardGoods_registered_documents_20230307.csv'))
        for row in template:
            if row[1] == fname:
                ID = row[0]
                break
        ifile = open(file)
        text=ifile.read()
        if '3m company' not in text.lower(): continue
        
        inUse = False #Flag for if you are in the product use subsection
        inIngred = False #Flag for if you are in the ingredients section
        inName = False #Flag for if you are in the product name 
        gotInfo = False
        ifile = open(file)
        for line in ifile:
            cline = cleanLine(line)
            # print(cline)
            if cline == []: continue
            # if fname == '004740.pdf': print(cline)
            if inName == True:
                if 'manufacturer:' in cline or 'recommended use' in cline[-1] or 'id number(s):' in cline or 'product identification numbers' in cline:
                    inName = False
                    continue
                else:
                    prodname = (prodname + ' ' + ' '.join(cline)).replace('  ',' ').strip()
            if 'product identifier' in cline[-1] and prodname == '':
                # if prodname == '':
                #     prodname = ' '.join(cline[1:])
                    inName = True
                    continue
            if 'product name:' in cline[0] and prodname == '':
                
                prodname = ' '.join(cline[1:])
                inName = True
                continue
            elif 'issue date:' in cline and gotInfo == False:
                date = cline[1]
            if 'version number:' in cline and rev == '': 
                rev = cline[-1]
            if 'product use:' in cline or cline[0] == 'recommended use' and gotInfo == False:
                inUse = True
                continue
            if inUse == True: #collect use information
                if 'section' in cline[0] or 'limitations on use:' in cline or "supplier's details" in cline[-1]:
                    inUse = False
                    continue
                elif len(cline)>1:
                    if cat == '': cat = ' '.join(cline[1:])
                    else: cat = cat + '/' + ''.join(cline[1:])
                else:
                    cat = cat + ' ' + cline[0]
                if len(cat) >= 100: #Use can't have >100 characters in factotum
                    cat = cat[0:96] + '...'
                    inUse = False
                    continue
                cat=cat.strip()
            if 'ingredient' in cline and 'c.a.s. no.' in cline and '% by wt' in cline:
                inIngred = True
                gotInfo = True
                continue
            if inIngred == True:
                chem = ''
                cas = ''
                conc = ''
                if '_____________________' in cline[0] or 'page' in cline[0] or '3mtm' in cline[0]: continue
                if 'section 3: hazards identification' in cline or 'section 4' in cline[0]:
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
               

                casN.append(cas)
                chemName.append(chem)
                use.append('')
                centC.append(conc)
     
                
        if chemName == []:
            chemName = ['']
            casN = ['']
            centC = ['']
            use = ['']
      
        for c in range(0,len(chemName)): #clean up concentrations and names
            chemName[c] = re.sub(' +', ' ', chemName[c])
            minC.append('')
            maxC.append('')
            # use.append('')
            component.append('')
            centC[c] = centC[c].replace('not applicable','').strip('trade secret * ')
            centC[c] = re.sub(' +', ' ', centC[c]).strip('')
            if centC[c] != '':
                unit.append('3')
            else:
                unit.append('')
            if '-' in centC[c]:
                minC[c] = centC[c].split('-')[0].strip()
                maxC[c] = centC[c].split('-')[1].strip()
                centC[c] = ''


    
        n = len(chemName)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('_new.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        casList.extend(casN)
        chemList.extend(chemName)
        useList.extend(use)
        minList.extend(minC)
        maxList.extend(maxC)
        unitList.extend(unit)
        centList.extend(centC)
        componentList.extend(component)
        
        if chemName == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))

    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/Airgas 3M Extracted Text.csv',index=False, header=True)
        

    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Hard/docs') #Folder pdfs are in
    txts = (glob("*new.txt"))
    extract_data(txts)    

if __name__ == "__main__": main()