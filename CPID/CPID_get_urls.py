# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 14:49:10 2021

@author: ALarger
"""

import time, os, string, random, pdfkit, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/CPID' #Folder docs go into
os.chdir(path)
# path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

chrome_options= Options()
#chrome_options.add_argument("--headless")
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.default_directory": path, "download.extensions_to_open": "applications/pdf"}
chrome_options.add_experimental_option("prefs", profile)
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)

start = 'https://www.whatsinproducts.com/brands/index/1'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))

# driver.find_element_by_xpath('//*[@id="closeDiv"]').click()

urls = []

sections = driver.find_elements_by_xpath('//*[@id="main_container"]/div[4]/div[2]/div[1]/div[1]/a')
for s in range(1,len(sections)+1):
    driver.find_element_by_xpath('//*[@id="main_container"]/div[4]/div[2]/div[1]/div[1]/a['+str(s)+']').click()
    time.sleep(random.randint(minTime,maxTime))
    links = driver.find_elements_by_xpath('//*[@id="main_container"]/div[5]/div[2]/table/tbody/tr/td[3]/a')
    for l in links:
        urls.append(l.get_attribute('href'))
                
# driver.close()

df = pd.DataFrame({'url':urls})
df=df.drop_duplicates()
df.to_csv('cpid urls.csv',index=False, header=False)
