# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:33:45 2019

@author: ALarger
"""

import time, csv, os, string, random, pdfkit, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\CRC\Automotive' #Folder doc is in
os.chdir(path)   
path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

idList = [] #Numbering system for naming documents
urlList = [] #Product page urls
nameList = [] #Product names
descripList = [] #Description
appList = [] #Applications
brandList = [] #Product brand
catList = [] #Product category (next to 'generic description')
picList = [] #List of picture urls
unitList = [] #Unit Package Description
sizeList = [] #Net Fill
upcList = [] #Product UPCs
appearanceList = [] #Appearance
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.default_directory": path, "download.extensions_to_open": "applications/pdf"}
chrome_options.add_experimental_option("prefs", profile)
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
urls = csv.reader(open('crc automotive urls.csv')) #csv of product urls
i=0
for row in urls:
    i+=1
#    if i==5: break
    url = row[0]
    time.sleep(random.randint(2,10))
    driver.get(url)
    try:
        name = clean(driver.find_element_by_xpath('//*[@id="product_addtocart_form"]/div[3]/div[1]/span').text) 
        pic = driver.find_element_by_xpath('//*[@id="productimagemain"]/img')
        picLink = pic.get_attribute('src')
        
        descrip = ''
        app = ''
        brand = ''
        cat = ''
        unit = ''
        size = ''
        upc = ''
        appearance = ''
        
        elements = driver.find_elements_by_xpath('//*[@id="product-attribute-specs-table"]/li')
        j=0
        while j < len(elements)-1: 
            if elements[j].text.split('\n')[0] == 'Description':
                descrip = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'Applications':
                app = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'Brand':
                brand = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'Generic Description':
                cat = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'Unit Package Description':
                unit = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'Net Fill':
                size = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'UPC Code':
                upc = elements[j].text.split('\n')[1]
            elif elements[j].text.split('\n')[0] == 'Appearance':
                appearance = elements[j].text.split('\n')[1]
            j+=1

        time.sleep(random.randint(2,10))
        sdsList = driver.find_elements_by_link_text('Safety Data Sheet')
        if len(sdsList) == 0:
            element = driver.find_element_by_xpath('//*[@id="product-attribute-specs-table"]/li[1]')
            webdriver.ActionChains(driver).move_to_element(element).perform()
            driver.find_element_by_xpath('//*[@id="top"]/body/div[4]/div/div[1]/div/div[2]/div[2]/div[2]/div/ul/li[2]').click()
            
            time.sleep(random.randint(2,10))
            sdsList = driver.find_elements_by_link_text('Safety Data Sheet')
            
        sds = sdsList[0].get_attribute('href')
        res = requests.get(sds)
        res.raise_for_status()
        playFile = open((str(i) + 'sds.pdf'),'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        
        time.sleep(random.randint(2,10))
        pds = driver.find_element_by_link_text('Product Data Sheet').get_attribute('href')
        res = requests.get(pds)
        res.raise_for_status()
        playFile = open((str(i) + 'pds.pdf'),'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()

    except:
        print(url) 
        continue

    #Add data to lists
    idList.append(i)
    urlList.append(url)
    nameList.append(name)
    descripList.append(descrip)
    appList.append(app)
    brandList.append(brand)
    catList.append(cat)
    picList.append(picLink)
    unitList.append(unit)
    sizeList.append(size)
    upcList.append(upc)
    appearanceList.append(appearance)

driver.close()

#Make csv
df = pd.DataFrame({'ID':idList, 'Product Name':nameList, 'Unit Package Description':unitList, 'Net Fill':sizeList, 'UPC':upcList, 'Description':descripList, 'Applications':appList, 'Brand':brandList, 'Product Type':catList, 'Appearance':appearanceList, 'url':urlList,'Picture url':picList})
df.to_csv('crc automotive products.csv',index=False, header=True)