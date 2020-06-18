# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 16:53:24 2020

@author: ALarger
"""

import time, csv, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Tarkett' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

idList = [] #Product IDs
nameList = [] #Product names
catList = [] #Product category
descripList = [] #Ingredient description
urlList = [] #Product page url
picList = [] #Product picture src

chrome_options= Options()
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

urls = csv.reader(open('tarkett urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    # if i == 5: break
    if i%50 == 0: print(i)
    if fails > 10 and len(idList) > 0: break #If the script fails on 10 products in a row: break
    url = row[0]   
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        docs = driver.find_elements_by_xpath('//*[@id="collection-documentation"]/div/div[2]/div[2]/div/a')
        gotDocs = False
        for d in docs: 
            if 'material health statement' in d.text.lower() or 'mhs' in d.text.lower(): #Download MHS
                try:
                    docLink = d.get_attribute('href')
                    filename = (str(i)+'_mhs.pdf')
                    res = requests.get(docLink)
                    res.raise_for_status()
                    playFile = open(filename,'wb')
                    for chunk in res.iter_content(100000):
                        playFile.write(chunk)
                    playFile.close()
                    gotDocs = True
                    time.sleep(random.randint(minTime,maxTime))
                except:
                    pass
            if 'safety data sheet' in d.text.lower() or 'sds' in d.text.lower(): #Download SDS
                try:
                    docLink = d.get_attribute('href')
                    filename = (str(i)+'_sds.pdf')
                    res = requests.get(docLink)
                    res.raise_for_status()
                    playFile = open(filename,'wb')
                    for chunk in res.iter_content(100000):
                        playFile.write(chunk)
                    playFile.close()
                    gotDocs = True
                    time.sleep(random.randint(minTime,maxTime))
                except: pass
        if gotDocs == False: continue
        #Save product image
        try:
            pic = driver.find_element_by_xpath('//*[@id="app-container"]/div[1]/div[4]/div[4]/div[1]/div[1]/div/div[1]/div/div/div/div/img')
            src = pic.get_attribute('src')
            html = urlopen(src) 
            picname = str(i)+'_pic.png'
            time.sleep(random.randint(minTime,maxTime))
            output = open(picname,'wb')
            output.write(html.read())
            output.close()
        except: pass
        name = driver.find_element_by_xpath('//*[@id="app-container"]/div[1]/div[4]/div[4]/div[2]/div[1]/div/div[2]/h1').text
        cat = driver.find_element_by_xpath('//*[@id="app-container"]/div[1]/div[4]/div[4]/div[2]/div[1]/div/div[1]').text.replace('| Suzanne Tick','').replace('| Jhane Barnes','').strip()
        try:
            driver.find_element_by_xpath('//*[@id="app-container"]/div[1]/div[4]/div[4]/div[2]/div[2]/div/div[1]/button').click()
            time.sleep(random.randint(minTime,maxTime))
        except: pass
        descrip = clean(driver.find_element_by_xpath('//*[@id="app-container"]/div[1]/div[4]/div[4]/div[2]/div[2]/div/div[1]/div/div[1]').text)
    except: 
        print('problem with page',url)
        fails+=1
        continue

    idList.append(i)
    nameList.append(name)
    catList.append(cat)
    descripList.append(descrip)
    urlList.append(url)
    picList.append(src)

    
driver.close()
    
#Make csv
df = pd.DataFrame({'id':idList, 'product name':nameList, 'product category':catList, 'description':descripList, 'url':urlList, 'picture src':picList})
df.to_csv('tarkett product page data.csv',index=False, header=True)    
    