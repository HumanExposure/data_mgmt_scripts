# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:25:55 2020

@author: ALarger
"""

import time, csv, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from time import strftime, localtime
from glob import glob
from selenium.webdriver.support.ui import Select
from urllib.request import urlopen


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/scj pages' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

#Comp data
idList = [] #Product IDs
skuList = [] #Product sku
nameList = [] #Product names
chemList = [] #Ingredient names
useList = [] #Ingredient uses
descripList = [] #Ingredient description
brandList = [] #Brand
urlList = [] #Product page url
picList = [] #Product picture src

chrome_options= Options()
# chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(5)
driver.maximize_window()

oldIDs = glob('*_page.pdf') #check which products have already been extracted
for x in range(0,len(oldIDs)):
    oldIDs[x] = oldIDs[x].replace('_page.pdf','')

urls = csv.reader(open('scj urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    # if i == 5: break
    if i%100 == 0: print(i)
    if str(i) in oldIDs: continue #Skip product pages that are already extracted
    if fails > 10 and len(idList) > 0: break #If the script fails on 10 products in a row: break
    if int(strftime('%H',localtime())) == 6: break #Stop running at 6am
    url = row[0]   
    try:
        driver.get(url)
        try:
            driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]').click()
        except: 
            pass
        
        #Get formulas (if there is a dropdown list)
        formulaUrls = []
        skus = []
        try:
            select = Select(driver.find_element_by_id("sku"))
            options = select.options
            for o in range(0,len(options)):
                skus.append(options[o].text)
                select.select_by_index(o)
                time.sleep(random.randint(minTime,maxTime))
                formulaUrls.append(driver.current_url)
        except: 
            try:
                skus.append(driver.find_element_by_xpath('//*[@id="main-content"]/div/div[1]/div[2]/div/div[2]/div[1]/p/em').text)
            except:
                skus.append('')
            formulaUrls.append(url)
            
        j = 0
        for u in formulaUrls:
            j+=1
            sku = skus[j-1]
            if j == 1:
                ID = str(i)
            else:
                ID = str(i) + '_' + str(j)
            if driver.current_url != u:
                driver.get(u)  
                time.sleep(random.randint(minTime,maxTime))
                
            #Get product data
            brand = clean(driver.find_element_by_xpath('//*[@id="main-content"]/div/div[1]/div[2]/div/div[2]/div[1]/h2').text.replace('®',''))
            name = clean(driver.find_element_by_xpath('//*[@id="main-content"]/div/div[1]/div[2]/div/div[2]/div[1]/h1').text.replace('®',''))
          
            #Get ingredients
            ingredients = driver.find_elements_by_xpath('//*[@id="ingredient-one"]/span[1]')
            if len(ingredients) > 0:
                for x in ingredients:
                    if x.text == 'Fragrance':
                        x.click()
                uses = driver.find_elements_by_xpath('//*[@id="ingredient-one"]/span[2]')
                descrips = driver.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/div[2]/div/div[2]/div[2]/div/ul/li/div[2]/p')
            else: 
                ingredients = driver.find_elements_by_xpath('//*[@id="ingredient-list"]/li/span[1]')
                uses = driver.find_elements_by_xpath('//*[@id="ingredient-list"]/li/span[2]')
                descrips = driver.find_elements_by_xpath('/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/ul/li/div[2]/p')
            for x in range(0,len(ingredients)):
                ingredients[x] = clean(ingredients[x].text)
                uses[x] = clean(uses[x].text)
                descrips[x] = clean(descrips[x].text)
                
            #Save product image
            pic = driver.find_element_by_xpath('//*[@id="main-content"]/div/div[1]/div[2]/div/div[1]/div/div/div/div/img')
            src = pic.get_attribute('src')
            if src != 'https://www.whatsinsidescjohnson.com/~/media/images/products/US/00000001-en.jpg':
                html = urlopen(src) 
                picname = ID+'_pic.png'
                time.sleep(random.randint(minTime,maxTime))
                output = open(picname,'wb')
                output.write(html.read())
                output.close()

            #Save ingredient disclosure
            try:
                doc = driver.find_element_by_xpath('//*[@id="main-content"]/div/div[1]/div[2]/div/div[1]/ul/li[1]/a')
                docLink = doc.get_attribute('href')
                filename = (ID+'_id.pdf')
                res = requests.get(docLink)
                res.raise_for_status()
                playFile = open(filename,'wb')
                for chunk in res.iter_content(100000):
                    playFile.write(chunk)
                playFile.close()
                time.sleep(random.randint(minTime,maxTime))
            except: pass
        
            #Save product page
            ele=driver.find_element_by_xpath('//*[@id="main-content"]')
            total_height = ele.size["height"]+1000
            driver.set_window_size(1920, total_height)
            time.sleep(random.randint(minTime,maxTime))
            driver.save_screenshot(ID+'_page.png')
            image1 = Image.open(ID+'_page.png')
            im1 = image1.convert('RGB')
            im1.save(ID+'_page.pdf')
            os.remove(ID+'_page.png')
            fails = 0
            
            if ingredients == []:
                ingredients = ['']
                uses = ['']
                descrips = ['']
                
            #Comp data
            l = len(ingredients)
            chemList.extend(ingredients)
            useList.extend(uses)
            descripList.extend(descrips)
            idList.extend([ID]*l)
            skuList.extend([sku]*l)
            nameList.extend([name]*l)
            brandList.extend([brand]*l)
            urlList.extend([u]*l)
            picList.extend([src]*l)
            
    except: 
        print('problem with page',url)
        fails+=1
        continue

driver.close()
    
#Make csv
df = pd.DataFrame({'id':idList, 'sku':skuList, 'brand':brandList, 'name':nameList, 'chem':chemList, 'use':useList, 'description':descripList, 'url':urlList, 'picture src':picList})
k=0
while os.path.exists('scj product page data '+str(k)+'.csv'):
    k+=1
df.to_csv('scj product page data '+str(k)+'.csv',index=False, header=True)    
    