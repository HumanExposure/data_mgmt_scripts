# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:19:16 2020

@author: ALarger
"""

import os, re
import pandas as pd
from selenium import webdriver

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Oregon' 
os.chdir(path)   
url = 'https://secure.sos.state.or.us/oard/viewSingleRule.action?ruleVrsnRsn=250202#:~:text=The%20following%20chemicals%20are%20designated,62-75-9'
driver = webdriver.Chrome(r'C:\Users\alarger\Documents\chromedriver.exe')
driver.get(url)

rowList = driver.find_elements_by_xpath('//*[@id="content"]/p')
chemList = []
casList = []
findCas = re.compile(r"\b[1-9]{1}[0-9]{1,5}-\d{2}-\d\b")
for row in rowList:
    if row.text[0] == '(':
        chemList.append(' '.join(row.text.split(' ')[1:]).replace("’","'"))
        casList.append(', '.join(findCas.findall(row.text)))
            
driver.close()
        
n = len(chemList)
idList= [1558017]*n
filenameList = ['Oregon Chemicals of High Concern to Children.pdf']*n
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
df.to_csv('Oregon Chemicals of High Concern to Children.csv',index=False, header=True, encoding = 'utf8')