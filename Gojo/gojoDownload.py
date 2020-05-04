# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:41:04 2020

@author: ALarger
"""

import time, csv, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Gojo' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

idList = [] #ID I have assigned for naming files
skuList = [] #Product number
nameList = [] #Product name
descripList = [] #Product description
sizeList = [] #Size of product
caseSizeList = [] #Size of a case of product
upcList = [] #Product UPC
caseUpcList = [] #UPC for a case of product
ingredientList = [] #Ingredients listed on the product page under specifications
urlList = [] #Product page url
picList = [] #Product picture src


urls = csv.reader(open('gojo urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    if i%100 == 0: print(i)
    if fails >= 10: break
    url = row[0]
    
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        
        #Save SDS
        gotDoc = False
        docs = driver.find_elements_by_xpath('//*[@id="body_0_ContentParent"]/div/div[1]/div/div/div[2]/div[2]/div[2]/div/a')
        for doc in docs:
            if doc.text == 'English':
                docLink = doc.get_attribute('href')
                filename = str(i)+'_sds.pdf'
                res = requests.get(docLink)
                res.raise_for_status()
                playFile = open(filename,'wb')
                for chunk in res.iter_content(100000):
                    playFile.write(chunk)
                playFile.close()
                time.sleep(random.randint(minTime,maxTime))
                gotDoc = True

        if gotDoc == False: 
            print('problem with sds:',i,url)
            time.sleep(random.randint(minTime,maxTime))
            continue
        
        #Save product image
        try:
            pic = driver.find_element_by_xpath('//*[@id="body_0_ContentParent"]/div/div[1]/div/div/div[1]/img')
            src = pic.get_attribute('src')
            html = urlopen(src) 
            picname = str(i)+'_pic.png'
            time.sleep(random.randint(minTime,maxTime))
            output = open(picname,'wb')
            output.write(html.read())
            output.close()
        except: 
            print('problem with pic:',i,url)
            time.sleep(random.randint(minTime,maxTime))
            fails += 1
            continue
        
        #Get name and description
        name = driver.find_element_by_xpath('//*[@id="body_0_ContentParent"]/div/div[1]/div/div/div[2]/div[1]').text
        descrip = driver.find_element_by_xpath('//*[@id="body_0_ContentParent"]/div/div[1]/div/div/div[2]/div[2]/div[1]').text
        
        #Navigate to the specifications tab and get specs
        tabs = driver.find_elements_by_xpath('//*[@id="body_0_ContentParent"]/div/div[1]/div/div/div[3]/ul/li/a')
        for t in tabs: 
            if t.text == 'Specifications':
                t.click()
                time.sleep(random.randint(minTime,maxTime))
        specs = driver.find_elements_by_xpath('//*[@id="body_0_ContentParent"]/div/div[1]/div/div/div[3]/div[2]/div/div/div/div')
        for x in range(0,len(specs)):
            specs[x] = specs[x].text.strip()
        sku = ''
        size = ''
        caseSize = ''
        upc = '' 
        caseUpc = ''
        ingredients = ''
        for x in range(0,len(specs)):
            if specs[x] == 'SKU':
                sku = specs[x+1]
            elif specs[x] == 'Size':
                size = specs[x+1]
            elif specs[x] == 'Case Pack':
                caseSize = specs[x+1]
            elif specs[x] == 'UPC (Each)':
                upc = specs[x+1]
            elif specs[x] == 'Case UPC (GTIN)':
                caseUpc = specs[x+1]
            elif specs[x] == 'Ingredients':
                ingredients = specs[x+1]

    except:
        print('problem with page:',i,url)
        time.sleep(random.randint(minTime,maxTime))
        fails += 1
        continue

    idList.append(i)
    skuList.append(sku)
    nameList.append(name)
    descripList.append(descrip)
    sizeList.append(size)
    caseSizeList.append(caseSize)
    upcList.append(upc)
    caseUpcList.append(caseUpc)
    ingredientList.append(ingredients)
    urlList.append(url)
    picList.append(src)
    fails = 0

driver.close()

#Make csv
df = pd.DataFrame({'id':idList, 'sku':skuList, 'name':nameList, 'description':descripList, 'size':sizeList, 'case size':caseSizeList, 'upc':upcList, 'case upc':caseUpcList, 'ingredients':ingredientList, 'url':urlList, 'pic url':picList})
df.to_csv('gojo scraped data.csv',index=False, header=True, encoding = 'utf8')