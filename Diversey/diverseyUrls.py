# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 12:13:42 2020

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Diversey'
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

urlList = [] #Product page urls
finished = False #Flag for if you are on the last page

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()

url = 'https://diversey.com/en/product-catalogue?items_per_page=120' #url of the starting page
page = -1 #page number the webdriver is on
while finished == False: 
    time.sleep(random.randint(minTime,maxTime))
    page += 1    
    driver.get(url + '&page=' + str(page))
    urls = driver.find_elements_by_xpath('//*[@id="block-views-block-products-catalog-block-1"]/div/div/div[3]/div/div/h2/span/a')
    if len(urls) == 0: break
    for u in urls:
        urlList.append(u.get_attribute('href'))

driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('diversey urls.csv',index=False, header=False)