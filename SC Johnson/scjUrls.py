# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:16:11 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'L:/Lab/HEM/ALarger/SC Johnson' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.get('https://www.whatsinsidescjohnson.com/us/en/brands')
driver.maximize_window()

brandLinks = []
urlList = []

brands = driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[3]/div/div/ul/li/div/a')
for b in brands:
    brandLinks.append(b.get_attribute('href'))

for l in brandLinks:
    driver.get(l)
    time.sleep(random.randint(minTime,maxTime))
    prods = driver.find_elements_by_xpath('//*[@id="main-content"]/div/div[4]/div/div/ul/li/div/a')
    for p in prods:
        urlList.append(p.get_attribute('href'))

driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('scj urls.csv',index=False, header=False)