# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 13:47:16 2020

@author: ALarger
"""

import time, os, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/ecri covid19 products' #path to folder
os.chdir(path)

epaRegNoList = []
nameList = []
chemList = []
concList = []
contactTimeList = []

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
startUrl = 'https://www.ecri.org/components/HDJournal/Pages/Disinfectant-Concentrations-for-EPA-list-N-COVID-19.aspx?tab=2' #url of the starting page
driver.get(startUrl)
driver.maximize_window()

#Get data from table
rows = driver.find_elements_by_xpath('//*[@id="ctl00_PlaceHolderMain_ctl04__ControlWrapper_RichHtmlField"]/table/tbody/tr')
for n in range(1,len(rows)+1): 
    if n < 3:
        continue
    row = driver.find_elements_by_xpath('//*[@id="ctl00_PlaceHolderMain_ctl04__ControlWrapper_RichHtmlField"]/table/tbody/tr['+str(n)+']/td')
    if len(row) == 5:
        epaRegNo = row[0].text
        name = row[1].text
        chem = row[2].text
        conc = row[3].text
        contactTime = row[4].text
    elif len(row) == 2:
        chem = row[0].text
        conc = row[1].text
    elif len(row) == 3:
        epaRegNo = row[0].text
        name = row[1].text
        chem = ''
        conc = ''
        contactTime = ''
    else: 
        print(len(row))
        for e in row:
            print(e.text)

    #get safety data sheet
    if len(row) > 2:
        time.sleep(5)
        try:
            sds = driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderMain_ctl04__ControlWrapper_RichHtmlField"]/table/tbody/tr['+str(n)+']/td[1]/a')
            docLink = sds.get_attribute('href')
            filename = epaRegNo + '.pdf'
            res = requests.get(docLink)
            res.raise_for_status()
            playFile = open(filename,'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
        except: 
            print(epaRegNo,'failed to download')
        
    #Append lists
    epaRegNoList.append(epaRegNo)
    nameList.append(name)
    chemList.append(chem)
    concList.append(conc)
    contactTimeList.append(contactTime)
    
driver.close()

#Make csv
df = pd.DataFrame({'EPA Reg. No.':epaRegNoList, 'Primary Registered Product Name':nameList, 'Active Disinfectant':chemList, 'Disinfectant Concentration (by weight)':concList, 'Disinfectant Contact Time (min)':contactTimeList})
df.to_csv('ecri covid19 web data.csv',index=False, header=True)