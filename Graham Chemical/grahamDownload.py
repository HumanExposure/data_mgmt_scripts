# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 10:36:23 2019

@author: ALarger
"""

import time, os, random, pdfkit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

path = r'L:\Lab\HEM\ALarger\Graham Chemical\Pharmaceutical' #Folder
os.chdir(path)

fileList = []
nameList = []
casList = []
catList = []
urlList = []

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
startUrl = 'https://www.grahamchemical.com/pharmaceutical' #url of the starting page
driver.get(startUrl)
driver.maximize_window()

pages = []
elements = driver.find_elements_by_xpath('//*[@id="productList"]/div/div/a')
for e in elements:
    pages.append(e.get_attribute('href'))
    
for p in pages:    
    time.sleep(random.randint(minTime,maxTime))
    driver.get(p)
    
    cas = driver.find_elements_by_xpath('//*[@id="productContent"]/div[1]/div/div[2]/div')
    if len(cas) == 0:
        cas = ''
    else: 
        cas = cas[0].text.strip('CAS: ')
    
    cat = ''
    text = driver.find_elements_by_xpath('//*[@id="productContent"]/div/p')
    for t in text: 
        if 'Applications:' in t.text:
            cat = t.text.replace('Applications:','').strip()
        
    name = driver.find_element_by_xpath('//*[@id="productContent"]/div[1]/div/div[1]/h1').text
    filename = name.replace('/','_').replace('.','_')+'.pdf'
    
    if filename in fileList:
        k = 2
        while (filename.split('.pdf')[0] + '_' + str(k) + '.pdf') in fileList:
            k+=1
        filename = (filename.split('.pdf')[0] + '_' + str(k) + '.pdf')
    time.sleep(random.randint(minTime,maxTime))
    pdfkit.from_url(p,filename,options=options, configuration=config)

    #Append lists
    fileList.append(filename)
    nameList.append(name)
    casList.append(cas)
    catList.append(cat)
    urlList.append(p)
    
driver.close()

#Make csv
df = pd.DataFrame({'filename':fileList, 'name':nameList, 'cas':casList, 'category':catList, 'url':urlList})
df.to_csv('graham chemical pharmaceutical downloaded docs.csv',index=False, header=True)