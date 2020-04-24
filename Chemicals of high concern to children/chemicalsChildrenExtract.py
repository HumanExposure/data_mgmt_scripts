# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 08:10:10 2020

@author: ALarger
"""

import os
import pandas as pd
from selenium import webdriver

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Chemicals of high concern to children' #Path the csv should go to 
os.chdir(path)   
url = 'https://ecology.wa.gov/Regulations-Permits/Reporting-requirements/Reporting-for-Childrens-Safe-Products-Act/Chemicals-of-high-concern-to-children' #Url table is at
driver = webdriver.Chrome(r'C:\Users\alarger\Documents\chromedriver.exe')
driver.get(url)

#Get chem and cas columns
chemList = driver.find_elements_by_xpath('//*[@id="site-content"]/div[2]/main/div/div[4]/div/table/tbody/tr/td[2]')
casList = driver.find_elements_by_xpath('//*[@id="site-content"]/div[2]/main/div/div[4]/div/table/tbody/tr/td[1]')

#Drop headers
chemList = chemList[1:] 
casList = casList[1:]

#Get text from web elements
for x in range(0,len(chemList)):
    chemList[x] = chemList[x].text
    casList[x] = casList[x].text
            
driver.close()
        
n = len(chemList)
idList= [1551584]*n
filenameList = ['chemicals of high concern to children reporting list.pdf']*n
dateList = ['']*n
categoryList = ['']*n
funcList = ['']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n
componentList = ['']*n

#Make csv
df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList, 'component':componentList})
df.to_csv('chemicals children list.csv',index=False, header=True, encoding = 'utf8')