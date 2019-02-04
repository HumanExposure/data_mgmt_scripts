# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 09:47:04 2019

@author: ALarger
"""

import os,string,csv
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
        print(cmd)
        os.system(cmd)
    return
    
def text_to_csv(files):
    """
    Extracts data from text file into a Pandas dataframe
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    revDate = []
    prodName = []
    recUse = []
    chemName = []
    casNum = []
    unit = []
    File = []
    ddID = []
    rev = []
    category = []
    minC = []
    maxC = []
    cenC = []
    rank = []
    
    for file in files:
        ifile = open(file)
        k = 1
        for line in ifile:
            if line == '/n': continue
            cline = clean(line)
            cline = cline.lower()
            cline = cline.replace(',','_')
            cline = cline.replace(';','_')
            cline = cline.strip()
            
            cline = cline.split("  ")
            cline = [x.strip() for x in cline if x != ""]
           
            if 'product name' in cline:
                product = cline[-1]
            elif 'issue date' in cline:
                date = cline[1] + ' ' + cline[2] + ' ' + cline[3]
            elif 'product use' in cline:
                cat = cline[-1]
            elif 'cas number' in cline:
                for line in ifile:
                    dline = clean(line)
                    dline = dline.lower()
                    dline = dline.replace(',','_')
                    dline = dline.replace(';','_')
                    dline = dline.strip()
                    dline = dline.split("  ")
                    dline = [x.strip() for x in dline if x != ""]
                
                    list1 = []
                    list1.append(dline)
                    list2 = []
                    list2 = [x for x in list1 if x != []]
                    done = False
                    if 'section 4' in str(line).lower():
                        break
                    
                    for i in list2:
                        #Breaking at end of chemical list
                        if i[0][0] == '*':
                            done = True
                            break
                        if i[0][0] == '1' and i[0][1] == ' ':
                            done = True
                            break
                        #Dealing with weird rows
                        if 'page' in i[0]:
                            continue
                        if 'safety data sheet' in i:
                            continue
                        try:
                            if i[1] == '.' and i[2] == '.':
                                continue
                            if i[1] == '.' and i[3] == '.':
                                continue
                        except:
                            pass
                        try:
                            if i[0][0].isdigit():
                                casNum[-1] = casNum[-1] + ' ' + i[0]
                                continue
                        except:
                            pass
                        try:
                            if len(i) == 6 and i[2] == 'agent':
                                i[1] = i[1] + ' ' + i[2]
                                del i[2]
                        except:
                            pass
                        try:
                            if len(i) == 1:
                                if i[0] == 'remover':
                                    recUse[-1] = recUse[-1] + ' ' + i[0]
                                    continue
                                else:
                                    chemName[-1] = chemName[-1] + ' ' + i[0]
                                    continue
                            elif len(i) == 2 and i[0] == 'di-(palm carboxyethyl) hydroxyethyl':
                                chemName.append(i[0])
                                casNum.append(i[1])
                                continue
                        except:
                            pass
                        #Extracting data from nornal rows
                        try:
                            name = file.split('.')[0] + '.pdf'
                            File.append(name)
                            prodName.append(product)
                            ID = ' '
                            template = csv.reader(open(r'C:\Users\alarger\Downloads\Seventh_Generation_2_-_Composition_July_2018_extract_template.csv'))
                            
                            for row in template:
                                if row[1] == name:
                                    ID = row[0]
                                    break
                        except IndexError:
                            File.append(' ')
                            prodName.append(' ')
                        try:
                            revDate.append(date)
                        except IndexError:
                            revDate.append(' ')
                        try:
                            try:
                                if chemName[-1] == 'di-(palm carboxyethyl) hydroxyethyl':
                                    casNum[-1] = casNum[-1] + ' ' + i[2]
                                else:
                                    casNum.append(i[2])
                            except IndexError: 
                                casNum.append(i[2])
                        except IndexError:
                            casNum.append(' ')
                        try:
                            if i[0][-1] == '*':
                                note = ''
                                flag = False
                                for line2 in ifile:
                                    if line2.startswith('1 '):
                                        flag = False
                                    if line2.startswith('section 4'):
                                        flag = False
                                    if line2.startswith('*'):
                                        flag = True 
                                    if 'Page ' in line2 or 'SAFETY DATA SHEET' in line2:
                                        continue
                                    if flag:
                                        note = note + ' ' + line2.strip()
                                chemName.append(i[0] + note)
                            else:
                                try:
                                    if chemName[-1] == 'di-(palm carboxyethyl) hydroxyethyl':
                                        chemName[-1] = chemName[-1] + ' ' + i[0]
                                    else:
                                        chemName.append(i[0])
                                except IndexError:
                                    chemName.append(i[0]) 
                        except IndexError:
                            chemName.append(' ')
                        try:
                            recUse.append(i[1])
                        except IndexError:
                            recUse.append(' ')
                        try:
                            if '%' in (i[3]):
                                unit.append('3')
                            else:
                                unit.append(' ')
                        except IndexError:
                            unit.append(' ')
                        try:
                            conc = (i[3]).replace('%','')
                            if 'mg/kg' in i[3] or 'not applicable' in i[3]:
                                conc = ' '                            
                        except IndexError:
                            conc = ' '
                        if '-' in conc:
                            minConc = conc.split('-')[0]
                            minConc.strip()
                            maxConc = conc.split('-')[1]
                            maxConc.strip()
                            cConc = ' '
                        else:
                            cConc = conc
                            maxConc = ' '
                            minConc = ' '
                        try:
                            cenC.append(cConc)
                        except IndexError:
                            cenC.append(' ')
                        try:
                            minC.append(minConc)
                        except IndexError:
                            minC.append(' ')
                        try:
                            maxC.append(maxConc)
                        except IndexError:
                            maxC.append(' ')
                        try:
                            category.append(cat)
                        except IndexError:
                            category.append(' ')
                        try:
                            ddID.append(ID)
                        except IndexError:
                            ddID.append(' ')
                        rev.append(' ')
                        rank.append(k)
                        k = k + 1
                        if len(i) < 4:
                            print(file,i)
                            
                    if done == True:
                        break
                        
    df = pd.DataFrame({'data_document_id':ddID, 'data_document_filename':File, 'prod_name':prodName, 'doc_date':revDate, 'rev_num':rev, 'raw_category':category, 'raw_cas':casNum, 'raw_chem_name':chemName, 'report_funcuse':recUse, 'raw_min_comp': minC, 'raw_max_comp':maxC, 'unit_type':unit, 'ingredient_rank':rank, 'raw_central_comp':cenC})
    df.to_csv(r'C:/Users/alarger/Documents/Seventh Gen pdfs/Seventh Generation July 2018.csv',index=False, header=True, date_format=None)
    df.to_excel(r'C:/Users/alarger/Documents/Seventh Gen pdfs/Seventh Generation July 2018.xlsx')
    
def main():
    os.chdir(r'C:/Users/alarger/Documents/Seventh Gen pdfs')
    
    file_list = glob("sds_*.pdf")
    n_pdfs = len(file_list)
    n_txts = len(glob("sds_*.txt"))
    if (n_txts < n_pdfs): pdf_to_text(file_list)
    
    n_txts = len(glob("sds_*.txt"))
    if (n_txts == n_pdfs):
       file_list = glob("*.txt")
       text_to_csv(file_list)
    file_list = glob("MSDS_*.pdf")
    
    return
    
if __name__ == "__main__": main()