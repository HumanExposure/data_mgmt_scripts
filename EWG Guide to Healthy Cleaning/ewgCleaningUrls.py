# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 14:04:44 2019

@author: ALarger
"""

import time, os, string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\EWG Guide to Healthy Cleaning' #Folder doc is in
os.chdir(path)   
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.get('https://www.ewg.org/guides/cleaners')
categories = []
urls = []

for x in driver.find_elements_by_class_name('graylink'):
    categories.append(x.get_attribute('href'))
for cat in categories:
    time.sleep(5)
    driver.get(cat)
    subcategories = [cat]
    for x in driver.find_elements_by_xpath("//a[contains(@href, '/guides/subcategories/')]"):
        subcategories.append(x.get_attribute('href'))
    for sub in subcategories:
        time.sleep(5)
        driver.get(sub)
        while True:    
            for x in driver.find_elements_by_xpath("//a[contains(@href, '/guides/cleaners/')]"):
                if x.get_attribute('href').split('/cleaners/')[1][0].isdigit():
                    urls.append(x.get_attribute('href'))
            try:
                nextPage = driver.find_element_by_class_name('next_page')
                if 'disabled' in nextPage.get_attribute('class'):
                    break
                time.sleep(5)
                nextPage.click()
            except: break
        
driver.close()

df = pd.DataFrame({'url':urls})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\EWG Guide to Healthy Cleaning\ewg cleaning urls.csv',index=False, header=False)

