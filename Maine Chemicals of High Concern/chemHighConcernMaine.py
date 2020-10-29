# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:01:32 2020

@author: ALarger
"""

import os
import pandas as pd
from selenium import webdriver

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Maine' 
os.chdir(path)   
url = 'https://www.maine.gov/dep/safechem/childrens-products/highconcern/index.html'
driver = webdriver.Chrome(r'C:\Users\alarger\Documents\chromedriver.exe')
driver.get(url)

chemList = driver.find_elements_by_xpath('//*[@id="maincontent2"]/table[1]/tbody/tr/td[2]')
casList = driver.find_elements_by_xpath('//*[@id="maincontent2"]/table[1]/tbody/tr/td[1]')
for x in range(0,len(chemList)):
    chemList[x] = chemList[x].text
    casList[x] = casList[x].text
            
driver.close()
        
n = len(chemList)
idList= [1558016]*n
filenameList = ['Maine Chemicals of High Concern.pdf']*n
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
df.to_csv('Maine Chemicals of High Concern.csv',index=False, header=True, encoding = 'utf8')