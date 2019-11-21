# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:44:06 2019

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

path = r'L:\Lab\HEM\ALarger\McKinley Resources' #Folder
os.chdir(path)

fileList = []
nameList = []
chemList = []
casList = []
funcList = []        
urlList = []
descripList = []
appList = []
noteList = []

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
startUrl = 'https://www.mckinleyresources.com/raw-materials-alphabetical-order.html' #url of the starting page
driver.get(startUrl)
driver.maximize_window()

#Navigate to correct page
time.sleep(random.randint(minTime,maxTime))
links = driver.find_elements_by_xpath('//*[@id="idContentTblCell"]/section/section/dl/dd/a')
n = len(links)
for i in range(0,n): 
    links = driver.find_elements_by_xpath('//*[@id="idContentTblCell"]/section/section/dl/dd/a')
    time.sleep(random.randint(minTime,maxTime))
    url = links[i].get_attribute('href')
    driver.get(url)
    
    #Get chemical info
    time.sleep(random.randint(minTime,maxTime))
    try:
        name = ','.join(driver.find_element_by_xpath('//*[@id="spanItemNumber"]/strong/h1').text.split(',')[1:])
        chem = ''
        cas = ''
        descrip = ''
        app = ''
        elements = driver.find_elements_by_xpath('/html/body/table/tbody/tr/td/div/section[1]/section/section/section/section/section/table/tbody/tr[2]/td/table/tbody/tr/td[2]/form/table[3]/tbody/tr/td/table[2]/tbody/tr/td[1]/table/tbody/tr/td/table')[0].text.split('\n') #get text from body of page
        for m in range(0,len(elements)):
            if 'INCI' in elements[m] and chem == '':
                chem = elements[m].split(':')[-1].strip()
            elif 'CAS' in elements[m] and cas == '':
                cas = elements[m].split(':')[-1].strip()
            elif 'Description' in elements[m] and descrip == '':
                descrip = elements[m+1]
            elif 'APPLICATIONS' in elements[m] and app == '':
                app = elements[m+1]
            
        #get technical data sheet
        try:
            tds = driver.find_element_by_partial_link_text('Technical Data Sheet')
        except: 
            try:
                tds = driver.find_element_by_partial_link_text('TDS')
            except: 
                time.sleep(random.randint(minTime,maxTime))
                driver.get(startUrl)
                continue
        docLink = tds.get_attribute('href')
        filename = (name.replace('/','_') + '.pdf')
        if filename in fileList:
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
    except: 
        print('failed to download:', url)
        time.sleep(random.randint(minTime,maxTime))
        driver.get(startUrl)
        continue
        
    #Append lists
    fileList.append(filename)
    nameList.append(name)
    chemList.append(chem)
    casList.append(cas)
    descripList.append(descrip)
    appList.append(app)
    urlList.append(url)
    
    #Go back to starting page
    time.sleep(random.randint(minTime,maxTime))
    driver.get(startUrl)
    
driver.close()

#Make csv
df = pd.DataFrame({'file name':fileList, 'name':nameList, 'chem name':chemList, 'cas':casList, 'description':descripList, 'applications':appList, 'url':urlList})
df.to_csv('mckinley scraped data.csv',index=False, header=True)