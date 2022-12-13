# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:46:17 2022

@author: ALarger
"""


import time, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Athea' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

urlList = [] #product page url


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(60)

start = 'https://www.athea.com/products/'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))

pageList = [start]
pages = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div/main/section/div/div[2]/ul/li/a')
for p in pages:
    if p.get_attribute('href') not in pageList:
        pageList.append(p.get_attribute('href'))
    
    
time.sleep(random.randint(minTime,maxTime))
for page in pageList:
    driver.get(page)
    time.sleep(random.randint(minTime,maxTime))
    urls = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div/main/section/div/div/div/a')
    for u in urls: 
        urlList.append(u.get_attribute('href'))


#Make csv
df = pd.DataFrame({'url':urlList})
df.to_csv('athea urls.csv',index=False, header=True, encoding='utf8')
