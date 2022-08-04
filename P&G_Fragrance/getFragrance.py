# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 16:16:32 2022

@author: ALarger
"""


import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random


minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/P&G CP' 
os.chdir(path)   
url = 'https://us.pg.com/fragrance-ingredients-list/'
chrome_options= Options()
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()


#Get chems not used
driver.get(url)
time.sleep(random.randint(minTime,maxTime))

tabs = driver.find_elements_by_xpath('/html/body/div[1]/main/div[4]/section/div[2]/div/div/div/div/label')
for t in tabs:
    t.click()
    time.sleep(random.randint(minTime,maxTime))
  

time.sleep(random.randint(minTime,maxTime))
chems = driver.find_elements_by_xpath('/html/body/div[1]/main/div[4]/section/div[2]/div[2]/div/div/div/div/div/ul/li')
for x in range(0,len(chems)):
    chems[x] = chems[x].text
            
        
n = len(chems)
idList = ['']*n
filenameList = ['frag_not_used.pdf']*n
dateList = ['']*n
categoryList = ['']*n
casList = ['']*n
chemList = chems
funcList = ['fragrance ingredient']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n
componentList = ['']*n
detectList = ['']*n


#Get chems used
driver.get(url)
time.sleep(random.randint(minTime,maxTime))

tabs = driver.find_elements_by_xpath('/html/body/div[1]/main/div[5]/section/div/div[2]/div/div/div/label')
for t in tabs:
    t.click()
    time.sleep(random.randint(minTime,maxTime))

time.sleep(random.randint(minTime,maxTime))
chems = driver.find_elements_by_xpath('/html/body/div[1]/main/div[5]/section/div/div[2]/div/div/div/div/div/ul/li')
for x in range(0,len(chems)):
    chems[x] = chems[x].text
    
driver.close()
        
n = len(chems)
idList.extend(['']*n)
filenameList.extend(['frag_used.pdf']*n)
dateList.extend(['']*n)
categoryList.extend(['']*n)
casList.extend(['']*n)
chemList.extend(chems)
funcList.extend(['fragrance ingredient']*n)
catcodeList.extend(['']*n)
descripList.extend(['']*n)
cpcatcodeList.extend(['']*n)
typeList.extend(['']*n)
componentList.extend(['']*n)
detectList.extend(['']*n)

df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList, 'component':componentList, 'chem_detected_flag':detectList})
df.to_csv('pg fragrance cp lists.csv',index=False, header=True, encoding = 'utf8')