# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 15:24:45 2020

@author: ALarger
"""

import time, os, random, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/scj sds' #Folder the docs go in 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.maximize_window()

url = 'https://www.scjohnson.com/Our%20Products/Safety%20Data%20Sheets?f2=United%20States%20(English)' #Url to the SDS download page
driver.get(url)
time.sleep(random.randint(minTime,maxTime))

urls = []
i=0
while True: #New SDSs appear when you scroll down. Keep scrolling and downloading new documents until you reach the end
    finished = True
    pages = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div/a') #Finds all pages currently loaded on page
    for p in pages:
        link = p.get_attribute('href')
        if link not in urls: #only download docs that haven't been downloaded yet
            finished = False
            try:
                filename = (str(i)+'_sds.pdf')
                res = requests.get(link)
                res.raise_for_status()
                playFile = open(filename,'wb')
                for chunk in res.iter_content(100000):
                    playFile.write(chunk)
                playFile.close()
                time.sleep(random.randint(minTime,maxTime))
                i+=1
            except:
                print('failed to download:',link)
            urls.append(link)
            time.sleep(random.randint(minTime,maxTime))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #scroll to bottom of page
    time.sleep(20)#Wait for new documents to load
    if finished == True: #If no more products have appeared: break
        break
    
driver.close()