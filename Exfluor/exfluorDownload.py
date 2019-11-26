# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:11:03 2019

@author: ALarger
"""

import time, os, random, requests, pdfkit, string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters

path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

path = r'L:\Lab\HEM\ALarger\Exfluor' #Folder
os.chdir(path)

fileList = []
nameList = []
linkList = []
catList = []

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
startUrl = 'http://www.exfluor.com/bycategory.php?cat=acids' #url of the starting page
driver.get(startUrl)
driver.maximize_window()

while True:
    cat = driver.find_element_by_xpath('//*[@id="shadow"]/table/tbody/tr/td/div[1]/h1').text
    if cat in catList: break
    
    time.sleep(random.randint(minTime,maxTime))
    links = driver.find_elements_by_xpath('//*[@id="shadow"]/table/tbody/tr/td/div/div/h2[1]/a')
    for n in range(0,len(links)):    
        
        name = links[n].text
        link = links[n].get_attribute('href')
        filename = link.split('/')[-1]
        
        try:
            #get safety data sheet
            time.sleep(random.randint(minTime,maxTime))
            if filename in fileList: #rename if filename is already taken
                k = 2
                while (filename.split('.pdf')[0] + '_' + str(k) + '.pdf') in fileList:
                    k+=1
                filename = (filename.split('.pdf')[0] + '_' + str(k) + '.pdf')
            res = requests.get(link)
            res.raise_for_status()
            playFile = open(filename,'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
        except:
            continue
            
        #Append lists
        fileList.append(filename)
        nameList.append(name)
        linkList.append(link)
        catList.append(cat)
        
    time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('//*[@id="shadow"]/table/tbody/tr/td/div[1]/a[2]').click()
    
driver.close()

#Make csv
df = pd.DataFrame({'filename':fileList, 'name':nameList, 'url':linkList, 'category':catList})
df.to_csv('exfluor downloaded docs.csv',index=False, header=True)