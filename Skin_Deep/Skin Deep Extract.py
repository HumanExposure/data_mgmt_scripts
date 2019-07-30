# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 08:54:31 2019

@author: ALarger

Extracts data from Skin Deep product webpages, saves htmls and creates a csv
"""

import time, csv, os, string
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\Skin Deep\Makeup' #Folder doc is in
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
urls = csv.reader(open('ewg makeup urls.csv')) #csv of product urls
i=0
for row in urls:
    i+=1
    url = row[0]
    time.sleep(3)
    driver.get(url)
    time.sleep(3)
    
    try:
        try:
            pic = driver.find_element_by_xpath('//*[@id="Summary"]/div[1]/img')
        except: 
            pic = driver.find_element_by_xpath('//*[@id="Summary"]/div[1]/a/img')
        picLink = pic.get_attribute('src')
        ID = url.split('/')[-3]
#    location = pic.location
#    size = pic.size
#    picName = ID + '.png'
#    #To get picture of product, get size and location of pic, screenshot page, and crop screenshot
#    driver.save_screenshot(picName) 
#    x = location['x']
#    y = location['y']
#    width = location['x']+size['width']
#    height = location['y']+size['height']
#    im = Image.open(picName)
#    im = im.crop((int(x), int(y), int(width), int(height)))
#    im.save(picName)
        driver.find_element_by_xpath('//*[@id="toc_ul"]/li[1]/a').click() #Click product summary button
        name = clean(driver.find_element_by_xpath('//*[@id="righttoptitleandcats"]/h1').text) #Get product name
        ingredients = clean(driver.find_element_by_xpath('//*[@id="Warnings_and_Directions"]/p[1]').text) #Get ingredient list
        date = clean(driver.find_element_by_xpath('//*[@id="dateupdated2012"]').text.replace('Data last updated:','').strip()) #Get date
    except:
        print(url) #Some pages are slightly different and can't be extracted with this script. Print the url and move on
        continue
    gotType=False
    j=0
    prodType = ''
    #Get elements next to "see all"
    while gotType == False:
       j+=1
       if j == 1:
           manuf = clean(driver.find_element_by_xpath('//*[@id="insidecontentdiv01234a"]/a['+str(j)+']/div').text)
       elif j == 2:
           try:
               brand = clean(driver.find_element_by_xpath('//*[@id="insidecontentdiv01234a"]/a['+str(j)+']/div').text)
           except:
               prodType = manuf
               manuf = ''
               brand = ''
       else:
           try:
               prodType = clean(prodType + ', ' + driver.find_element_by_xpath('//*[@id="insidecontentdiv01234a"]/a['+str(j)+']/div').text).strip(', ')
           except: 
               gotType = True
               if prodType == '':
                   prodType = manuf + ', ' + brand
                   manuf = ''
                   brand = ''
    #Save page as pdf
    try:
        with open((ID+'.html'), 'w') as f:
            f.write(driver.page_source)
    except:
        print(url) #Some pages can't be saved. Print the url and move on
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

driver.close()

#Make csv
df = pd.DataFrame({'ewg ID':idList, 'Product Name':nameList, 'Manufacturer':manufList, 'Brand':brandList, 'Date':dateList, 'Product Type':typeList, 'Ingredient':ingredientList, 'url':urlList,'Picture url':picList})
df.to_csv('Skin Deep Makeup Products 0.csv',index=False, header=True)
