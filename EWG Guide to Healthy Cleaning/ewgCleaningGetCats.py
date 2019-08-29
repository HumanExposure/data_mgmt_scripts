# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:14:49 2019

@author: ALarger
"""

import time, csv, os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'L:\Lab\HEM\ALarger\EWG Guide to Healthy Cleaning' #Folder doc is in
os.chdir(path)   

idList = [] #Product ids
urlList = [] #Product page urls
nameList = [] #Product names
ingredientList = [] #Product ingredients
dateList = [] #"data last updated" lists
manufList = [] #Manufacturers (first element next to 'see all')
brandList = [] #Brands (second element next to 'see all')
typeList = [] #Product types (combination of elements after brand next to 'see all')
picList = [] #List of picture urls

old = csv.reader(open('ewg healthy cleaning with cat links all.csv')) #csv of product urls
for row in old:
    if row[0] == 'ewg ID': continue
    idList.append(row[0])
    nameList.append(row[1])
    manufList.append(row[2])
    brandList.append(row[3])
    dateList.append(row[4])
    typeList.append(row[5])
    ingredientList.append(row[6])
    urlList.append(row[7])
    picList.append(row[8])
    
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
    
for n in range(len(manufList)):
    if n%100 == 0:
        print(n)
    
    if 'https:' in manufList[n]:
        time.sleep(10)
        url = manufList[n]
        driver.get(url)
        newManuf = driver.find_element_by_xpath('//*[@id="productname"]/h1').text
        for i in range(len(manufList)):
            if url in manufList[i]:
                manufList[i] = manufList[i].replace(url,newManuf)
                
    if 'https:' in brandList[n]:
        time.sleep(10)
        url = brandList[n]
        driver.get(url)
        newBrand = driver.find_element_by_xpath('//*[@id="productname"]/h1').text
        for i in range(len(brandList)):
            if url in brandList[i]:
                brandList[i] = brandList[i].replace(url,newBrand)
                
    if 'https:' in typeList[n]:
        urls = typeList[n].split(',')
        for url in urls:
            if 'https:' in url:
                time.sleep(10)
#                url = typeList[n]
                driver.get(url)
                newType = driver.find_element_by_xpath('//*[@id="productname"]/h1').text
                for i in range(len(typeList)):
                    if url in typeList[i]:
                        typeList[i] = typeList[i].replace(url,newType)            
    
driver.close()
    
df = pd.DataFrame({'ewg ID':idList, 'Product Name':nameList, 'Manufacturer':manufList, 'Brand':brandList, 'Date':dateList, 'Product Type':typeList, 'Ingredient':ingredientList, 'url':urlList,'Picture url':picList})
df.to_csv('ewg healthy cleaning products.csv',index=False, header=True)