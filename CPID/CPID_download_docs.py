# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 16:13:19 2021

@author: ALarger
"""


import time, csv, os, random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
from glob import glob

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/CPID' 
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

chrome_options= Options()
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],"download.default_directory": path, "download.extensions_to_open": ""}
chrome_options.add_experimental_option("prefs",profile)
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

downloaded = glob('*_doc.pdf')

urls = csv.reader(open('cpid product page data all.csv', encoding='utf8')) #csv of product urls

for row in urls: #Go through each row in the product data csv, go to pages with pdfs, and download the pdfs
    if row[0] == 'id': continue
    if row[1] == '' or row[14] == '': continue
    if row[1] in downloaded: continue

    url = row[14]   
    filename = row[1]
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        pdf_url = driver.find_element_by_tag_name('iframe').get_attribute("src")
        download_url = pdf_url.split('url=')[-1].split('.pdf')[0]+'.pdf'
        response = urllib.request.urlopen(download_url)    
        file = open(filename, 'wb')
        file.write(response.read())
        file.close()
        time.sleep(random.randint(minTime,maxTime))
    except: 
        print(row[1],'problem with page',url)
        continue
   
driver.close()