# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 12:50:33 2020

@author: ALarger
"""

import time, os, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

path = r'L:\Lab\HEM\ALarger\Declare_Living Future' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.maximize_window()

url = 'https://living-future.org/declare/'
driver.get(url)
time.sleep(random.randint(minTime,maxTime))

urls = []
prior = ''

while True:
    pages = driver.find_elements_by_xpath('//*[@id="declare-grid"]/div/a')
    for p in pages:
        urls.append(p.get_attribute('href'))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.randint(minTime,maxTime))
    current = urls[-1]
    if current == prior: #If no more products have appeared: break
        break
    prior = urls[-1]
    
driver.close()
    
df = pd.DataFrame({'url':urls})
df=df.drop_duplicates()
df.to_csv('declare urls.csv',index=False, header=False)