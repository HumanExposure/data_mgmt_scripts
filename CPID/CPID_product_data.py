# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 16:07:32 2021

@author: ALarger
"""


import time, csv, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen


path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/CPID' 
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

idList = [] #Product IDs
docList = [] #Document name
picList = [] #Product picture name
nameList = [] #Product name
catList = [] #Product category
classificationList = []
marketList = []
eparegnoList = []
upcList = []
usageList = []
formList = []
manufList = []
descripList = []
urlList = [] #Product page url
docLinkList = []

chrome_options= Options()
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(5)
driver.maximize_window()

urls = csv.reader(open('cpid urls.csv')) #csv of product urls
i=0
for row in urls:
    i+=1
    docName = str(i)+'_doc.pdf'
    picName = str(i)+'_pic.png'
    classification = ''
    market = ''
    eparegno = ''
    upc = ''
    usage = ''
    form = ''
    
    if i%50 == 0: print(i)
    url = row[0]   
    try: #Go to product page and get prod data
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        elements = driver.find_elements_by_xpath('//*/h1')    
        for e in elements: 
            if int(e.value_of_css_property("font-weight")) >= 300: #Product name should have a fontweight > 300
                name = e.text
                break
        categories = driver.find_elements_by_class_name('breadcrumbs')
        categories = [c.text for c in categories]
        cats = ', '.join(categories)
        prodData = driver.find_elements_by_class_name('brand_clasi_feild')
        for p in prodData:
            element = p.text.lower().strip()
            if 'classification:' in element: classification = element.split('classification:')[-1].strip()
            if 'market' in element: market = element.split('market:')[-1].strip()
            if 'epa registration no:' in element: eparegno = element.split('epa registration no:')[-1].strip()
            if 'upc:' in element: upc = element.split('upc:')[-1].strip()
            if 'usage:' in element: usage = element.split('usage:')[-1].strip()
            if 'form:' in element: form = element.split('form:')[-1].strip()
    except: 
        continue
    try: #Get link to pdf if available
        d = driver.find_element_by_xpath('//*[@id="accordion"]/li[3]/ul/li[2]/table/tbody/tr/td/a')
        docLink = d.get_attribute('href')
    except:
        docName = ''
        docLink = ''
    try: #Download pic 
        pic = driver.find_element_by_xpath('//*[@id="main_container"]/div/div/table/tbody/tr/td/img')
        src = pic.get_attribute('src')
        html = urlopen(src) 
        time.sleep(random.randint(minTime,maxTime))
        output = open(picName,'wb')
        output.write(html.read())
        output.close()
    except: 
        picName = ''


    try: #get prod description
        descrip = driver.find_element_by_xpath('//*[@id="main_container"]/div/div[2]/p').text
    except: 
        descrip = ''
     
    try: #get manufacturer
        manuf = driver.find_element_by_xpath('//*[@id="main_container"]/div/div[2]/div[2]/strong').text
    except: 
        manuf = ''
        
    idList.append(i)
    docList.append(docName)
    picList.append(picName)
    nameList.append(name)
    catList.append(cats)
    classificationList.append(classification)
    marketList.append(market)
    eparegnoList.append(eparegno)
    upcList.append(upc)
    usageList.append(usage)
    formList.append(form)
    manufList.append(manuf)
    descripList.append(descrip)
    urlList.append(url)
    docLinkList.append(docLink)
  
df = pd.DataFrame({'id':idList, 'doc name':docList, 'pic name':picList, 'product name':nameList, 'product category':catList, 'classification':classificationList, 'market':marketList, 'epa reg no':eparegnoList, 'upc':upcList, 'usage':usageList, 'form':formList, 'manufacturer':manufList, 'description':descripList, 'url':urlList, 'doc url':docLinkList})
df.to_csv('cpid product page data.csv',index=False, header=True)    
      
