# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 13:10:20 2020

@author: ALarger
"""

import time, csv, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from glob import glob


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Diversey' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

#Comp data
idList = [] #Product IDs
skuList = [] #Product sku
nameList = [] #Product names
sizeList = [] #Product size
colorList = [] #Product color
descripList = [] #Product description
urlList = [] #Product page url

chrome_options= Options()
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

oldIDs = glob('*_sds.pdf') #check which products have already been extracted
for x in range(0,len(oldIDs)):
    oldIDs[x] = oldIDs[x].replace('_sds.pdf','')

urls = csv.reader(open('diversey urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    # if i == 5: break
    if str(i) in oldIDs: continue
    if i%100 == 0: print(i)
    if fails > 10 and len(idList) > 0: break #If the script fails on 10 products in a row: break
    url = row[0]   
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        try:
            driver.find_element_by_xpath('//*[@id="popup-buttons"]/button[2]').click()
            time.sleep(random.randint(minTime,maxTime))
        except: 
            pass
        
        #Get product data
        try:
            name = clean(driver.find_element_by_xpath('/html/body/div/div/div[1]/div/section/div/div/article/div[1]/div/div[1]/div[1]/h1/div').text.replace('®',''))
            descrip = driver.find_element_by_xpath('/html/body/div/div/div[1]/div/section/div/div/article/div[1]/div/div[1]/div[3]').text
            sku = driver.find_element_by_class_name('product-sku').text.replace('PRODUCT SKU: ','')
            size = ''
            color = ''
            elements = driver.find_elements_by_xpath('//*[@id="specs-list"]/div/div')
            for n in range(0,len(elements)):
                if 'Packsize:' in elements[n].text:
                    size = elements[n].text.replace('\n',' ').replace('Packsize:','').strip()
                if 'Color:' in elements[n].text:
                    color = elements[n].text.replace('\n',' ').replace('Color:','').strip()
            
        except:
            fails+=1
            print('problem getting data from page:',url)
            continue
            
        #Save product image
        try:
            pic = driver.find_element_by_xpath('//*[@id="slider"]/ul/li/div/div/img')
            src = pic.get_attribute('src')
            html = urlopen(src) 
            picname = str(i)+'_pic.png'
            time.sleep(random.randint(minTime,maxTime))
            output = open(picname,'wb')
            output.write(html.read())
            output.close()
        except: 
            fails+=1
            print('problem with pic:',url)
            continue

        #Save SDS
        try:
            driver.find_element_by_xpath('/html/body/div/div/div[1]/div/section/div/div/article/div[2]/ul/li[2]/a').click()
            time.sleep(random.randint(minTime,maxTime))
            doc = driver.find_element_by_xpath('//*[@id="resources"]/div/div/div[1]/div[3]/div/div[1]/a')
            docLink = doc.get_attribute('href')
            filename = (str(i)+'_sds.pdf')
            res = requests.get(docLink)
            res.raise_for_status()
            playFile = open(filename,'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
            time.sleep(random.randint(minTime,maxTime))
            fails = 0
        except: 
            fails+=1
            print('problem with sds:',url)
            continue
                
        #Comp data
        idList.append(i)
        skuList.append(sku)
        nameList.append(name)
        sizeList.append(size)
        colorList.append(color)
        descripList.append(descrip)
        urlList.append(url)
            
    except: 
        print('problem with page',url)
        fails+=1
        continue

driver.close()
    
#Make csv
df = pd.DataFrame({'id':idList, 'sku':skuList, 'name':nameList, 'size':sizeList, 'color':colorList, 'description':descripList, 'url':urlList})
k=0
while os.path.exists('diversey product page data '+str(k)+'.csv'):
    k+=1
df.to_csv('diversey product page data '+str(k)+'.csv',index=False, header=True)