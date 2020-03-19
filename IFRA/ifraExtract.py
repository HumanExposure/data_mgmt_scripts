# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 10:02:37 2020

@author: ALarger
"""

import os
import pandas as pd
from selenium import webdriver

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/IFRA' 
os.chdir(path)   
url = 'https://ifrafragrance.org/initiatives/transparency/ifra-transparency-list'
driver = webdriver.Chrome(r'C:\Users\alarger\Documents\chromedriver.exe')
driver.get(url)

chemList = driver.find_elements_by_xpath('//*[@id="ingredients-table"]/tbody/tr/td[2]')
casList = driver.find_elements_by_xpath('//*[@id="ingredients-table"]/tbody/tr/td[1]')
for x in range(0,len(chemList)):
    chemList[x] = chemList[x].text
    casList[x] = casList[x].text
            
driver.close()
        
n = len(chemList)
idList= [1512365]*n
filenameList = ['ifra transparency list.pdf']*n
dateList = ['']*n
categoryList = ['fragrance components']*n
funcList = ['fragrance component']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n
componentList = ['']*n

df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList, 'component':componentList})
df.to_csv('ifra transparency list.csv',index=False, header=True, encoding = 'utf8')