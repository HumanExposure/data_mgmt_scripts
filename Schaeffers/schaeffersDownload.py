# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 15:52:54 2019

@author: ALarger
"""

import time, os, random, requests, pdfkit
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

path = r'L:\Lab\HEM\ALarger\Schaeffer' #Folder
os.chdir(path)

fileList = []
nameList = []
numList = []

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
startUrl = 'https://www.schaefferoil.com/msds-technical-data-sheets.html' #url of the starting page
driver.get(startUrl)
driver.maximize_window()

rows = driver.find_elements_by_xpath('//*[@id="docs-table"]/tbody/tr')
for n in range(1,len(rows)+1):    
    row = driver.find_elements_by_xpath('//*[@id="docs-table"]/tbody/tr['+str(n)+']/td')
    if len(row) > 2 and row[2].text == 'Safety Data': #Only go to rows with an sds
        num = row[0].text
        name = row[1].text
            
        #get safety data sheet
        time.sleep(random.randint(minTime,maxTime))
        sds = driver.find_element_by_xpath('//*[@id="docs-table"]/tbody/tr['+str(n)+']/td[3]/a')
        docLink = sds.get_attribute('href')
        filename = (num.replace('/','_').replace('#','') + '.pdf')
        if filename in fileList: #rename if filename is already taken
            k = 2
            while (filename.split('.pdf')[0] + '_' + str(k) + '.pdf') in fileList:
                k+=1
            filename = (filename.split('.pdf')[0] + '_' + str(k) + '.pdf')
        res = requests.get(docLink)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        
    #Append lists
    fileList.append(filename)
    nameList.append(name)
    numList.append(num)
    
driver.close()

#Make csv
df = pd.DataFrame({'file name':fileList, 'name':nameList, 'Product #':numList})
df.to_csv('schaeffers downloaded docs.csv',index=False, header=True)