# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 10:20:28 2022

@author: ALarger
"""

import time, os, string, random, requests, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Athea' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

numList = [] #List of numbers used to name files
idList = [] #ID numbers
nameList = [] #Product name
# descripList = [] #Product description
# catList = [] #Category the product is listed under
urlList = [] #product page url


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(60)

pdfs = glob('*.pdf')
urls = csv.reader(open('athea urls.csv')) #csv of product urls
i=0
for row in urls: 
    url = row[0]
    if url == 'url': continue
    i+=1
    if str(i)+'_sds.pdf' in pdfs: continue
    driver.get(url)
    time.sleep(random.randint(minTime,maxTime))
    
    name = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/main/article/div/div/div[2]/h1').text.strip()
    idnum = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/main/article/div/div/div[2]/h2').text.split(':')[-1].strip()
    
    numList.append(i)
    idList.append(idnum)
    nameList.append(name)
    urlList.append(url)
    
    try: #Download SDS
    # /html/body/div/div[3]/div/div/main/article/div/div/div[2]/div[3]/div/div[2]/a[1]
        docs = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div/main/article/div/div/div/div/div/div/a[1]')
        docLink = ''
        for d in docs:
            # print(d.get_attribute('href'))
            if '-sds' in d.get_attribute('href'):
                docLink = d.get_attribute('href')
        if docLink != '':
            filename = str(i)+'_sds.pdf'
            res = requests.get(docLink)
            res.raise_for_status()
            playFile = open(filename,'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
            time.sleep(random.randint(minTime,maxTime))
        else: print('no SDS ',url)
                
    except:
        print('SDS failed ',url)
    
    try: #Download ingredient disclosure
        docLink = driver.find_element_by_xpath('/html/body/div/div[3]/div/div/main/article/div/div/div[1]/div/div[3]/a').get_attribute('href')
        filename = str(i)+'_id.pdf'
        res = requests.get(docLink)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))
    
    except: pass
            

        



# urls = driver.find_elements_by_xpath('/html/body/div/div[3]/div/div/main/section/div/div/div/a')
# for u in urls: 
#     urlList.append(u.get_attribute('href'))
# # driver.close()


#Make csv
df = pd.DataFrame({'pdf id':numList, 'manufacturer id':idList, 'product name':nameList, 'url':urlList})
df.to_csv('athea web data 2.csv',index=False, header=True, encoding='utf8')
