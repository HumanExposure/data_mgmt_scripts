# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 14:18:38 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'L:\Lab\HEM\ALarger\Zep' #Folder doc is in
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.get('https://www.zep.com/index')
driver.maximize_window()

catLinks = []
urlList = []

cats = driver.find_elements_by_xpath('//*[@id="navbar"]/ul[1]/li[2]/ul/div/li/ul/li/a')
for c in cats:
    if 'www.zep.com' in c.get_attribute('href'): #exclude links that take you to another website
        catLinks.append(c.get_attribute('href'))

for l in catLinks:
    time.sleep(random.randint(minTime,maxTime))
    driver.get(l)
    time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div[3]/div[2]/div[3]/div/div[2]/a').click()
    time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div[3]/div[2]/div[3]/div/div[2]/ul/li[4]/a').click()
    time.sleep(random.randint(minTime,maxTime))
    pages = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div[3]/div[2]/div[3]/div/div[1]/a')
    for x in range(0,len(pages)):
        time.sleep(random.randint(minTime,maxTime))
        driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div[3]/div[2]/div[3]/div/div[1]/a')[x].click()
        time.sleep(random.randint(minTime,maxTime))
        urls = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div[3]/div[2]/div[1]/div/div/a')
        for u in urls:
            urlList.append(u.get_attribute('href'))
        
driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('zep urls.csv',index=False, header=False)
