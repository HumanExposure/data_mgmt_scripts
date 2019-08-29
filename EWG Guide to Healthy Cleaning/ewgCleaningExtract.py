# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 15:08:21 2019

@author: ALarger

Note: On the product pages, the category names, brand names and manufacturer names are sometimes cut off
    To resolve this, the links to the product category, brand, and manufacturer pages are saved and a separate script goes to these pages to retrieve the full names
"""

import time, csv, os, string, codecs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
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
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
urls = csv.reader(open('ewg cleaning urls.csv')) #csv of product urls
i=0
for row in urls:
    i+=1
    if i <= 2390: continue
    url = row[0]
    time.sleep(10)
    driver.get(url)
    time.sleep(10)
    prodType = ''
    try:
        pic = driver.find_element_by_xpath('//*[@id="productimg"]/img')
        picLink = pic.get_attribute('src')
        ID = url.split('/')[-1].split('-')[0]

        driver.find_element_by_xpath('//*[@id="toc_ul"]/li[2]/a').click() #Click "What's on the label" button
        name = clean(driver.find_element_by_xpath('//*[@id="productname"]/h1').text) #Get product name
        ingredients = clean(driver.find_element_by_xpath('//*[@id="Ingredient_Sources"]/div/p').text).replace('What appears on the label:','').strip() #Get ingredient list
        date = clean(driver.find_element_by_xpath('//*[@id="product_first_added"]').text.replace('Date entered:','').strip()) #Get date
        brand = driver.find_element_by_xpath("//a[contains(@href, '/guides/brand/')]").get_attribute('href') #Get brand
        manuf = driver.find_element_by_xpath("//a[contains(@href, '/guides/business/')]").get_attribute('href') #Get manufacturer
        cat = driver.find_elements_by_xpath("//a[contains(@href, '/guides/subcategories/')]") 
        #Get product categories
        for c in cat:
            if c.get_attribute('href') not in prodType:
                prodType = (prodType + ',' + c.get_attribute('href')).strip(',')
        #Make html
        file_object = codecs.open((ID + '.html'), "w", "utf-8")
        html = driver.page_source
        file_object.write(html)

    except:
        print(url) #Some pages are slightly different and can't be extracted with this script. Print the url and move on
        continue

    #Add data to lists
    ingredientList.append(ingredients)
    idList.append(ID)
    urlList.append(url)
    nameList.append(name)
    dateList.append(date)
    manufList.append(manuf)
    brandList.append(brand)
    typeList.append(prodType)
    picList.append(picLink)
#    if i == 3: break 


driver.close()

#Make csv
df = pd.DataFrame({'ewg ID':idList, 'Product Name':nameList, 'Manufacturer':manufList, 'Brand':brandList, 'Date':dateList, 'Product Type':typeList, 'Ingredient':ingredientList, 'url':urlList,'Picture url':picList})
df.to_csv('ewg healthy cleaning with cat links 2.csv',index=False, header=True)