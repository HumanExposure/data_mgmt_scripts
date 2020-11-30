# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 09:56:58 2020

@author: ALarger
"""


import os, re
import pandas as pd
from selenium import webdriver

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Toxic Free Kids' 
os.chdir(path)   
url = 'https://apps.leg.wa.gov/wac/default.aspx?cite=173-333-310'
driver = webdriver.Chrome(r'C:\Users\alarger\Documents\chromedriver.exe')
driver.get(url)

rowList = driver.find_elements_by_xpath('//*[@id="contentWrapper"]/div[3]/div[3]/table/tbody/tr')
chemList = []
casList = []
inPFOS = False
for n in range(1,len(rowList)+1):
    chem = driver.find_element_by_xpath('//*[@id="contentWrapper"]/div[3]/div[3]/table/tbody/tr['+str(n)+']/td[1]').text.strip()
    cas = driver.find_element_by_xpath('//*[@id="contentWrapper"]/div[3]/div[3]/table/tbody/tr['+str(n)+']/td[2]').text.strip()
    if chem == 'Perfluorooctane sulfonates (PFOS)': inPFOS = True
    if chem == 'Polycyclic aromatic hydrocarbons (PAHs)': inPFOS = False
    if inPFOS == True: chem = 'Perfluorooctane sulfonates (PFOS): ' + chem
    if 'CAS' not in cas and cas != '':
        chemList.append(chem)
        casList.append(cas)
            
driver.close()
        
n = len(chemList)
idList= [1558318]*n
filenameList = ['washington state pbt.pdf']*n
dateList = ['']*n
categoryList = ['']*n
funcList = ['']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n
componentList = ['']*n
detectedList = ['']*n

df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList, 'component':componentList, 'chem_detected_flag':detectedList})
df.to_csv('washington state pbt.csv',index=False, header=True, encoding = 'utf8')