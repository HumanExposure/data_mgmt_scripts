# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:40:09 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'L:\Lab\HEM\ALarger\Skin Deep\Functional Use'
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.maximize_window()

urlList = []

for i in range(1,501):
    url = 'https://www.ewg.org/skindeep/search/?page='+str(i)+'&search=&search_type=ingredients'
    driver.get(url)
    time.sleep(random.randint(minTime,maxTime))
    links = driver.find_elements_by_xpath('/html/body/div[2]/div/main/section[5]/div/a')
    for l in links:
        urlList.append(l.get_attribute('href'))

driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('skin deep func use urls.csv',index=False, header=False)