# -*- coding: utf-8 -*-
"""
Created on Wed May  5 15:32:27 2021

@author: ALarger
"""


import time, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

urlList = [] #Product page urls
finished = False #Flag for if you are on the last page
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)

url = 'https://www.bigdind.com/' #url of the starting page
driver.get(url)
time.sleep(random.randint(minTime,maxTime))
driver.maximize_window()

categories = driver.find_elements_by_xpath('//*[@id="DrpDwnMn0-5s31"]/ul/li/a')
categories = [c.get_attribute('href') for c in categories]

i=0
while i < len(categories): 
    driver.get(categories[i])
    time.sleep(random.randint(minTime,maxTime))
    
    newurls = driver.find_elements_by_css_selector("a[href*='bigdind.com/numbers/']")
    newurls = [n.get_attribute('href') for n in newurls]
    urlList.extend(newurls)
    newcategories = driver.find_elements_by_xpath('//*/h6/span/a')    
    newcategories.extend(driver.find_elements_by_xpath('//*/h6/a'))
    newcategories = [n.get_attribute('href') for n in newcategories]
    for n in newcategories:
        if n not in categories:
            categories.append(n)
    i+=1
    
driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Big D/Big D New/big d urls.csv',index=False, header=False)