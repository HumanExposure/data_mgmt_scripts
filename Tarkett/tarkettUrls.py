# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 09:05:31 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Tarkett' 
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.get('https://commercial.tarkett.com/en_US/')
driver.maximize_window()
time.sleep(random.randint(minTime,maxTime))

catLinks = []
urlList = []

cats = driver.find_elements_by_xpath('//*[@id="tab-header"]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div/a')
for c in cats:
    catLinks.append(c.get_attribute('href'))

for c in catLinks:
    time.sleep(random.randint(minTime,maxTime))
    driver.get(c)
    time.sleep(random.randint(minTime,maxTime))
    urls = driver.find_elements_by_xpath('//*[@id="result-item"]/div/div[1]/a')
    for u in urls:
        urlList.append(u.get_attribute('href'))
    pageLinks = []
    pages = driver.find_elements_by_xpath('//*[@id="main"]/div[2]/div[1]/div[2]/div[2]/div[5]/div/a')
    for p in pages:
        pageLinks.append(p.get_attribute('href'))
    for p in pageLinks:
        try:
            time.sleep(random.randint(minTime,maxTime))
            driver.get(p)
            time.sleep(random.randint(minTime,maxTime))
            urls = driver.find_elements_by_xpath('//*[@id="result-item"]/div/div[1]/a')
            for u in urls:
                urlList.append(u.get_attribute('href'))
        except: pass
        
driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('tarkett urls.csv',index=False, header=False)
