# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 08:38:27 2019

@author: ALarger
"""

import time, os, string, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\CRC\Automotive' #Folder doc is in
os.chdir(path)

page = 0 #page number the webdriver is on
urlList = [] #Product page urls
finished = False #Flag for if you are on the last page

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)

url = 'https://www.crcindustries.com/products/automotive.html' #url of the starting page
driver.get(url)
driver.maximize_window()
nProducts = float(driver.find_element_by_xpath('//*[@id="chweb_layered_container"]/div[1]/div[1]/div[2]/div/span').text.strip(' RESULTS'))
if nProducts > 12:
    time.sleep(random.randint(2,10))
    driver.find_element_by_xpath('//*[@id="chweb_layered_container"]/div[1]/div[1]/div[2]/div[2]/div/a').click()
    time.sleep(random.randint(2,10))
    driver.find_element_by_xpath('//*[@id="top"]/body/ul[2]/li[3]/a').click() #Change items per page to 36
nPages = nProducts/36

while finished == False: 
    time.sleep(random.randint(2,10))
    page += 1    
    driver.get('https://www.crcindustries.com/products/automotive.html?dir=asc&limit=36&p=' + str(page))
    urls = driver.find_elements_by_xpath('//*[@id="chweb_layered_container"]/div[1]/ul/li/a')
    for i in range(len(urls)):
        urls[i] = urls[i].get_attribute('href') 
    urlList.extend(urls)
    if page >= nPages:
        finished = True

driver.close()

df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv(r'crc automotive urls.csv',index=False, header=False)
