# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:01:32 2020

@author: ALarger
"""

import os, re, string
import pandas as pd

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))


os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\ESCO')

chemList=[]
casList=[]
funcList=[]
filenameList=[]
categoryList=[]
idList=[]

#Coatings
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Coatings')
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, c in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=c.replace('\n',' ').strip()
for i, c in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=c.replace('\n',' ').strip()
for i, use in enumerate(uses):
   use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
   use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
   uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_coatings.pdf']*n)
categoryList.extend(['coatings']*n)
idList.extend(['1724071']*n)

#Colorants
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Colorants')
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, ca in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=ca.replace('\n',' ').strip()
for i, chem in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=chem.replace('\n',' ').strip()
for i, use in enumerate(uses):
   use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
   use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
   uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_colorants.pdf']*n)
categoryList.extend(['colorants']*n)
idList.extend(['1724072']*n)
       
#Cork and wood
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Cork and wood')
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, c in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=c.replace('\n',' ').strip()
for i, c in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=c.replace('\n',' ').strip()
for i, use in enumerate(uses):
   use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
   use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
   uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_cork and wood.pdf']*n)
categoryList.extend(['cork and wood']*n)
idList.extend(['1724073']*n)
       
#Paper and board
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Paper and board')
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, ca in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=str(ca).replace('\n',' ').strip()
for i, chem in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=chem.replace('\n',' ').strip()
for i, use in enumerate(uses):
   use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
   use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
   uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_paper and board.pdf']*n)
categoryList.extend(['paper and board']*n)
idList.extend(['1724074']*n)

#Printing inks
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Printing inks')
df.columns = df.iloc[0]
df = df.iloc[1: , :]
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, c in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=c.replace('\n',' ').strip()
for i, c in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=c.replace('\n',' ').strip()
for i, use in enumerate(uses):
    use = use.replace('M','monomer').replace('S','solvent').replace('A','additive').replace('P','photoinitiator')
    use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
    use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
    uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_printing inks.pdf']*n)
categoryList.extend(['printing inks']*n)
idList.extend(['1724075']*n)

#Rubber
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Rubber')
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, c in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=c.replace('\n',' ').strip()
for i, c in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=c.replace('\n',' ').strip()
for i, use in enumerate(uses):
   use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
   use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
   uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_rubber.pdf']*n)
categoryList.extend(['rubber']*n)
idList.extend(['1724076']*n)

#Silicones
df = pd.read_excel('ESCO_food_contact_materials_silicones.xlsx', sheet_name='Silicones')
df = df.fillna('')
chems=df.loc[:,'Name'].tolist()
cas=df.loc[:,'CAS RN'].tolist()
uses=df.loc[:,'Remarks'].tolist()
for i, c in enumerate(cas):
    # if '\n' in c: print('*',c,'*')
    cas[i]=c.replace('\n',' ').strip()
for i, c in enumerate(chems):
    # if '\n' in c: print('*',c,'*')
    chems[i]=c.replace('\n',' ').strip()
for i, use in enumerate(uses):
   use=use.replace('\n',' ').replace('as ','').replace(' or ',';').replace(',',';').strip()
   use=use.replace(' ;',';').replace('; ',';')#Get rid of extra spaces in functional uses
   uses[i] = use
n=len(chems)
chemList.extend(chems)
casList.extend(cas)
funcList.extend(uses)
filenameList.extend(['ESCO_food_contact_materials_silicones.pdf']*n)
categoryList.extend(['silicones']*n)
idList.extend(['1724077']*n)



for i, use in reversed(list(enumerate(funcList))):
    # print(i, e)
    use=clean(use)
    if use.lower().split(' ')[0].split(';')[0] in ['yes','no','the','A']: 
        use=''
    
    use=re.sub("\(.*?\)","()",use)
    use=use.split('CAS')[0]
    use=use.replace('(','').replace(')','').replace('BfR','').replace('36:','')
    use=use.strip(' ;')
    funcList[i]=use
    if chemList[i].strip()=='' and casList[i].strip()=='':
        print(i, use)
        funcList[i-1]=(funcList[i-1]+';'+use).strip(' ;')
        del funcList[i]
        del chemList[i]
        del casList[i]
        del filenameList[i]
        del categoryList[i]
        del idList[i]


n = len(chemList)
# idList= ['']*n
# filenameList = ['ESCO_food_contact_materials.xlsx']*n
dateList = ['']*n
# categoryList = ['']*n
# funcList = ['']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n
componentList = ['']*n
detectedList = ['']*n



df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList, 'component':componentList, 'chem_detected_flag':detectedList})
df.to_csv('esco food contact.csv',index=False, header=True, encoding = 'utf8')


