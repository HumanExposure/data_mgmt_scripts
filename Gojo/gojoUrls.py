# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 12:21:00 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Gojo' #Folder doc is in
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.get('https://www.gojo.com/en/Search-Results#t=coveoTabProducts&sort=relevancy')
driver.maximize_window()

urlList = []

while True:
    time.sleep(random.randint(minTime,maxTime))
    links = driver.find_elements_by_xpath('//*[@id="coveoResultsList"]/div[10]/div/div/div/div/div/div/div/div[2]/div[1]/span[1]/a')
    for l in links:
        urlList.append(l.get_attribute('href'))
    try:
        driver.find_element_by_xpath('//*[@title="Next"]').click()
    except: break

driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('gojo urls.csv',index=False, header=False)