# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 14:55:44 2020

@author: ALarger
"""


import time, os, string, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Scraping\DrugBank' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

nameList = []
weightList = []
descripList = []
categoryList = []
filter1List = []
filter2List = []

chrome_options= Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(60)

start = 'https://www.drugbank.ca/drugs'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))

page = 1
cats = driver.find_elements_by_xpath('/html/body/main/div/div[1]/form/div/div[1]/div/a') 
for c in range(1,len(cats)+1): #navigate to small molecule/biotech
    cat = driver.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div[1]/div['+str(c)+']/a').text
    print(cat)
    driver.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div[1]/div['+str(c)+']/a').click()
    time.sleep(random.randint(minTime,maxTime))
    if c == 2: 
       driver.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div[4]/div/div[1]/label/span/span').click() #When on biotech drugs, deselect protein based therapies filter 
       time.sleep(random.randint(minTime,maxTime))
    groups = driver.find_elements_by_xpath('/html/body/main/div/div[1]/form/div/div[3]/div[1]/div/label/span/span')
    for g in range(1,len(groups)+1): #Navigate to different groups (approved, nutraceutical, ...)
        imageList = []
        if g != 1:
            driver.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div[3]/div[1]/div['+str(g-1)+']/label/span/span').click() #Deselect previous filter
            time.sleep(random.randint(minTime,maxTime))
            driver.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div[3]/div[1]/div['+str(g)+']/label/span/span').click() #Select next filter
            time.sleep(random.randint(minTime,maxTime))
        driver.find_element_by_name('commit').click() #Click apply filter
        time.sleep(random.randint(minTime,maxTime))
        filter2 = driver.find_element_by_xpath('/html/body/main/div/div[1]/form/div/div[3]/div[1]/div['+str(g)+']/label/span/span').text
        print(filter2)
    
        while True: #extract each page
            #Extract table
            rows = driver.find_elements_by_xpath('//*[@id="drugs-table"]/tbody/tr')
            for r in range(1,len(rows)+1):
                nameList.append(driver.find_element_by_xpath('//*[@id="drugs-table"]/tbody/tr['+str(r)+']/td[1]').text.replace('\n',' '))
                weightList.append(driver.find_element_by_xpath('//*[@id="drugs-table"]/tbody/tr['+str(r)+']/td[2]').text.replace('\n',' '))
                descripList.append(driver.find_element_by_xpath('//*[@id="drugs-table"]/tbody/tr['+str(r)+']/td[4]').text.replace('\n',' '))
                categoryList.append(driver.find_element_by_xpath('//*[@id="drugs-table"]/tbody/tr['+str(r)+']/td[5]').text.replace('\n',' '))
                filter1List.append(cat)
                filter2List.append(filter2)
                
            ID = cat + '_' + filter2 + '_page_' + str(page)
                
            #Save screenshot of page
            ele=driver.find_element_by_xpath('/html/body/main')
            total_height = ele.size["height"]+1000
            driver.set_window_size(1920, total_height)
            time.sleep(random.randint(minTime,maxTime))
            driver.save_screenshot(ID+'.png')
            imageList.append(Image.open(ID+'.png').convert('RGB'))
            time.sleep(random.randint(minTime,maxTime))
    
            try:
                driver.find_element_by_class_name('next').click() #click next page
                page += 1
                time.sleep(random.randint(minTime,maxTime))
            except:
                page = 1
                time.sleep(random.randint(minTime,maxTime))
                break #last page, move on to next filter
                
        #Make pdf 
        im1 = imageList[0]
        im1.save(ID.split('_page')[0]+'.pdf',save_all=True, append_images=imageList[1:])

driver.close()


#Make csv
df = pd.DataFrame({'Filter 1':filter1List, 'Filter 2':filter2List, 'Chemical name':nameList, 'Weight':weightList, 'Description':descripList, 'Categories':categoryList})
df.to_csv('drugbank scraped data.csv',index=False, header=True, encoding='utf8')
