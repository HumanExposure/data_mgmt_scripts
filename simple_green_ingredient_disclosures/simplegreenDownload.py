# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 18:33:33 2021

@author: ALarger
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from PIL import Image
from Screenshot import Screenshot_Clipping


path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/simple green' #Folder docs go into
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks

fileList = []
nameList = []
chemList = []
casList = []
funcList = []


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(60)

start = 'https://simplegreen.com/ingredient-disclosure/'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))


prodlen = len(driver.find_elements_by_xpath('//*[@id="list_item"]/option'))
for x in range(1,prodlen):
    select = Select(driver.find_element_by_xpath('//*[@id="list_item"]')) #Product dropdown box
    select.select_by_index(x) #select next product in dropdown box
    time.sleep(random.randint(minTime,maxTime))
    name = driver.find_element_by_xpath('//*[@id="list_item"]/option['+str(x+1)+']').text
    driver.find_element_by_xpath('//*[@id="sb258"]/ul[3]/li/input[1]').click() #click search button
    time.sleep(random.randint(minTime,maxTime))

    
    #Save screenshot of page by saving image of the full webpage and then converting it to pdf
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(random.randint(minTime,maxTime))
    ob=Screenshot_Clipping.Screenshot()
    img_url=ob.full_Screenshot(driver, save_path=r'.', image_name=str(x)+'_page.png')
    image1 = Image.open(str(x)+'_page.png')
    im1 = image1.convert('RGB')
    im1.save(str(x)+'_page.pdf')
    os.remove(str(x)+'_page.png')


    numChems = len(driver.find_elements_by_xpath('//*[@id="response"]/table/tbody/tr'))
    for y in range(2,numChems+1):
        chem = driver.find_element_by_xpath('//*[@id="response"]/table/tbody/tr['+str(y)+']/td[1]').text #get chem names
        cas = driver.find_element_by_xpath('//*[@id="response"]/table/tbody/tr['+str(y)+']/td[2]').text #get cas numbers
        func = driver.find_element_by_xpath('//*[@id="response"]/table/tbody/tr['+str(y)+']/td[3]').text #get functional uses
        fileList.append(str(x)+'_page.pdf')
        nameList.append(name)
        chemList.append(chem)
        casList.append(cas)
        funcList.append(func)


driver.close()


#Make csv
df = pd.DataFrame({'file name':fileList, 'product name':nameList, 'chem name':chemList, 'CASRN':casList, 'functional use':funcList})
df.to_csv('simple green scraped data.csv',index=False, header=True, encoding='utf8')
