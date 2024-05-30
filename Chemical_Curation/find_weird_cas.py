# -*- coding: utf-8 -*-
"""
Created on Tue May  2 10:56:08 2023

@author: ALarger
"""

import csv, os
import pandas as pd
import re
from datetime import datetime
from glob import glob

def casrn_search(x):
    """
    Take a text string and search for all occurrences of a CASRN number
    
    Parameters
    ----------
    x: string, text that will be searched for CASRNs
    
    Returns
    -------
    s: list, a list of the CASRNs that were found in the text
    """
    if isinstance(x,str):
        s = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",x)

    return s



def casrn_split(x):
    """
    Take a text string and extract all occurrences of a CASRN number. This 
    should remove leading zeros (0) too.
    
    Parameters
    ----------
    x: string, text that will be searched for CASRNs
    
    Returns
    -------
    s: integer, a count of how many CASRNs were found in the text
    """
    if isinstance(x,str):
        s = re.findall("[1-9][0-9]{1,6}\-[0-9]{2}\-[0-9]",x)
    else:
        s = pd.NA
    return s



def checksum(x):
    """
    Check that the last digit in the CAS-RN is a valid digit. One way to ensure
    if a CAS-RN is invalid
    
    Parameters
    ----------
    x: string, string of a CAS-RN
    
    Return
    ------
    boolean: True if checksum if valid, False otherwise
    """
    if not isinstance(x,str):
        return False
    cas = x[-3::-1].replace('-', '')
    q = 0
    for i,d in enumerate(cas):
        q += (i+1)*int(d)
    if q%10 == int(x[-1]):
        return True
    else:
        return False
    
    
def fix_datetime(x): #Maybe these should be fixed in factotum?
    """
    In an MS Excel file, the CAS-RNs that have been converted to dates are read
    in as datetime objects, in CSVs/TSVs they are read in as strings. Check the
    object type and make the corrections
    
    Parameters
    ----------
    x: object, text or datetime that could contain CAS-RNs which have been
       converted to dates
       
    Returns
    -------
    list: all CAS-RNs as dates which have been converted to strings in the right
          CAS-RN format
    """
    

    if isinstance(x,datetime):
        casrn =  ['{d.year}-{d.month:02}-{d.day}'.format(d=x)]
    elif isinstance(x,str):
        s = re.findall(r'(\d+/\d+/\d+)',x)
        casrn = []
        for i in casrn:
            t = i.split('/')
            casrn.append(f"{t[2]}-{t[0]}-{t[1]}")
    else:
        casrn = x
    return casrn

def check_useful(x):
    """
    Check if a string has useful information about a chemical name/casrn or if it just contains filler text
    Parameters
    ----------
    x : string

    Returns
    -------
    boolean: True if string contains useful text, False otherwise

    """
    
    
    useful = False
    badwords = ['fragrance','fragrances','preservative','preservatives','pigment','pigments','proprietary','unknown','inert','inerts','ingredient','ingredients','surfactant','surfactants','nonionic','anionic','cationic','non','not','no','na','none','ionic','colorant','colorants','mixture','mixtures','solvent','solvents','light','stabilizer','stabilizers','perfume','perfumes','wetting','agent','agents','dye','dyes','chelating','essential','oil','oils','organic','additive','additives','other','etc','nonhazardous','hazardous','defoamer','defoamers','withheld','cas','casrn','trade','secret','found','assigned','available','confidential','blend','from','of','a','an','the'] #list of words or phrases in chemical names/cas numbers that are not useful
    x = x.replace('-',' ').replace('/',' ').replace('.','').strip().lower()
    if x == '': return(useful)
    
    x = x.split(' ')
    if any(y not in badwords for y in x):
        useful = True
    
    return(useful)

def add_dashes(x):
    """
    adds dashes back into CAS numbers that only have digits
    ----------
    x : string, CAS number without dashes

    Returns
    -------
    string: CAS number with dashes

    """
    
    x = x[:-3]+'-'+x[-3:-1]+'-'+x[-1]
   
    
    return(x)



idList = []
casList = []
chemList = []
cleanCas = []
cleanChem = []
casNotesList = []
chemNotesList = []
skippedid = []
skippedchem = []
skippedcas = []
removed_parentheses = []

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/chemical curation files/uncurated_chems_2024-03-28_11-33-59'

os.chdir(path)
files = glob('Factotum_uncurated_chemicals*.csv')
file = files[31]
print(file)

data = csv.reader(open(file, 'r', encoding='utf8', errors='ignore'))
for row in data:
    # if row[3] == '974': continue #Skip this group for now
    if row[0] != 'id':
        rawid = row[0]
        rawcas = row[2]
        rawchem = row[3]
        newcas = ''
        newchem = ''
        casNotes = ''
        chemNotes = ''
        parentheses = ''
        
        #Remove line breaks from data
        rawcas=rawcas.replace('\n','').replace('\r', ' ').replace('\t', ' ')
        rawchem = rawchem.replace('\n',' ').replace('\r', ' ').replace('\t', ' ')
        
        #check cas
        newcas=rawcas.replace(' ','').replace('–','-').replace('-­','-').lstrip('0')
        if newcas != '' and check_useful(rawcas) == False: 
            newcas = ''
            casNotes = (casNotes+',removed from the CASRN field: '+rawcas).strip(', ')
        
        
        #Fix chemical names
        newchem = rawchem.replace('–','-').strip()
        if newchem != '' and newchem[-1] == ')' and '(' in newchem:
            parentheses = newchem.split('(')[-1].strip(')')
            removed_parentheses.append(parentheses)
            if parentheses.lower() == 'inn' or 'cancer' in parentheses.lower() or 'carcinogen' in parentheses.lower():
                chemNotes = (chemNotes+', text removed from the chemical name: ('+parentheses+')').strip(', ')
                newchem = '('.join(newchem.split('(')[:-1])
        
        if 'isomer' in newchem.lower() and 'salt' in newchem.lower(): print(newchem) #Review chem name
        newchem = re.sub(' +', ' ', newchem).strip()
        
        
        
        
        if newchem != '' and check_useful(newchem) == False: 
            newchem = ''
            chemNotes = (chemNotes+',removed from the chemical name field: '+rawchem).strip(', ')
            
        
        # if len(re.findall("[0-9]{3}\-[0-9]{3}\-[0-9]{1}",rawcas)) > 0: print('EC#: ',rawcas,rawid) #EC Number
       
        
        #If the chemical name and cas number fields both don't have useful information: skip
        if check_useful(newcas) == False and check_useful(rawchem) == False: 
            # print(rawchem,rawcas)    
            skippedid.append(rawid)
            skippedchem.append(rawchem)
            skippedcas.append(rawcas)
            continue
        
        #Fix cas numbers
        if all(x in '1234567890' for x in newcas) and len(newcas)>4: 
            newcas = add_dashes(newcas)
            casNotes = (casNotes+', added dashes to CASRN').strip(', ')
        if newcas == '': pass
        elif 'hmira' in rawcas.lower() or 'cbi' in rawcas.lower() or 'njtsrn' in rawcas.lower():
            if check_useful(newchem) == False: 
                newchem = rawcas
                newcas = ''
                chemNotes = (chemNotes+',moved from the CASRN field to the chem name field: '+rawcas).strip(', ')
            else: 
                casNotes = (casNotes+',removed from the CASRN field: '+rawcas).strip(', ')
                newcas = ''
        elif any(n not in '1234567890-' for n in newcas):
            print('bad cas: ',newcas,rawid) #Review these
            casNotes = (casNotes+',removed from the CASRN field: '+rawcas).strip(', ')
            newcas = ''
        elif len(casrn_search(newcas)) == 0: 
            print('no cas: ',newcas,rawid) #Review these
            casNotes = (casNotes+',removed from the CASRN field: '+rawcas).strip(', ')
            newcas = ''
        elif len(casrn_search(newcas)) > 1: 
            print('multiple cas: ',newcas,rawid) #Review these, and edit in Factotum if necessary
            newcas = ''
        elif casrn_search(newcas)[0] != newcas: 
            print('bad cas: ',newcas,rawid) #Review these
            casNotes = (casNotes+',removed from the CASRN field: '+rawcas).strip(', ')
            newcas = ''
        elif checksum(newcas) == False:
            print('checksum failed: ',newcas,rawid)
            casNotes = (casNotes+', CASRN failed checksum: '+newcas).strip(', ')
            newcas = ''
            
        
        if check_useful(newcas) == False and check_useful(rawchem) == False: 
            # print(rawchem,rawcas)    
            skippedid.append(rawid)
            skippedchem.append(rawchem)
            skippedcas.append(rawcas)
            continue
        
    
        idList.append(rawid)
        casList.append(rawcas)
        cleanCas.append(newcas)
        chemList.append(rawchem)
        cleanChem.append(newchem)
        chemNotesList.append(chemNotes)
        casNotesList.append(casNotes)
        
#Make csv of cleaned chems
df = pd.DataFrame({'External_ID':idList, 'Raw CASRN':casList, 'Raw Chemical Name':chemList, 'Cleaned CAS-RN':cleanCas, 'Cleaned Chemical Name':cleanChem, 'CAS-RN Comments':casNotesList, 'Chemical Name Comments':chemNotesList})
# df.to_csv('uncurated_chemicals_cleaned.csv',index=False, header=True, encoding = "utf-8")

#Make csv of rows that were skipped
df = pd.DataFrame({'External_ID':skippedid, 'Raw CASRN':skippedcas, 'Raw Chemical Name':skippedchem})
# df.to_csv('uncurated_chemicals_skipped.csv',index=False, header=True, encoding = "utf-8")
        
        