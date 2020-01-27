# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:57:08 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'L:\Lab\HEM\ALarger\RB' #Folder doc is in
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.get('http://rbnainfo.com/brands.php')
driver.maximize_window()

brandLinks = []
urlList = []
brandList = []

brands = driver.find_elements_by_xpath('//*[@id="galleryContainer"]/div/a')
for b in brands:
    brandLinks.append(b.get_attribute('href'))

for l in brandLinks:
    time.sleep(random.randint(minTime,maxTime))
    driver.get(l)
    time.sleep(random.randint(minTime,maxTime))
    brand = driver.find_element_by_xpath('//*[@id="wrapper"]/section[2]/section/div/div[1]/h3').text.strip(' ®')
    time.sleep(random.randint(minTime,maxTime))
    prods = driver.find_elements_by_xpath('//div/div/div/div/a[2]')
    for p in prods:
        if 'rbnainfo.com' in p.get_attribute('href'):
            urlList.append(p.get_attribute('href'))
            brandList.append(brand)

driver.close()

df = pd.DataFrame({'url':urlList, 'brand':brandList})
df=df.drop_duplicates()
df.to_csv('rb urls.csv',index=False, header=False)