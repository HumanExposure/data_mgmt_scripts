# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 15:59:07 2020

@author: ALarger
"""

import time, csv, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from Screenshot import Screenshot_Clipping
from time import strftime, localtime
from glob import glob

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\RB' 
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

#Comp data
idList = [] #Product IDs
nameList = [] #Product names
catList = [] #Product category
chemList = [] #Ingredient names
casList = [] #Ingredient CAS numbers
useList = [] #Ingredient uses

#Prod data
idList2 = [] #Product IDs
nameList2 = [] #Product names
brandList = [] #Brand
upcList = [] #Product UPCs
sizeList = [] #Product sizes
urlList = [] #Product page url
picList = [] #Product picture src

chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

oldIDs = glob('*_page.pdf') #check which products have already been extracted
for x in range(0,len(oldIDs)):
    oldIDs[x] = oldIDs[x].replace('_page.pdf','')

urls = csv.reader(open('rb urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    if i%100 == 0: print(i)
    if row[0].split('=')[-1] in oldIDs: continue #Skip product pages that are already extracted
    if fails > 10 and len(idList) > 0: break #If the script fails on 10 products in a row: break
    if int(strftime('%H',localtime())) == 16: break #if its after 4pm: stop running
    url = row[0]   
    brand = row[1]
    ID = row[0].split('=')[-1]
    
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        
        #Get UPCs and sizes
        try:
            driver.find_element_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[2]/div[1]/div/div/table/tbody[1]/tr[4]/td/i').click() #click on "more UPCs"
        except:
            pass
        upc = driver.find_elements_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[2]/div[1]/div/div/table/tbody/tr/td[1]')
        for x in range(0,len(upc)):
            upc[x] = upc[x].text
        if 'more UPCs …' in upc:
            upc.remove('more UPCs …')
        size = driver.find_elements_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[2]/div[1]/div/div/table/tbody/tr/td[2]')
        for x in range(0,len(size)):
            size[x] = size[x].text
        if len(upc) != len(size):
            print('upc/size problem',url)
            continue
        
        #Get ingredient information
        ingredients = []
        CASs = []
        uses = []
        chems = driver.find_elements_by_class_name('ingredientsName')
        if len(chems) == 0:
            chemRows = driver.find_elements_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[2]/div[3]/div/div/table/tbody/tr')
            for c in range(1,len(chemRows)+1):
                ingredients.append(driver.find_element_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[2]/div[3]/div/div/table/tbody/tr['+str(c)+']/td[1]').text)
                uses.append(driver.find_element_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[2]/div[3]/div/div/table/tbody/tr['+str(c)+']/td[2]').text)
                CASs.append('')
        else:
            j=-1
            for c in chems:
                cas = ''
                j+=1
                c.click()
                time.sleep(random.randint(minTime,maxTime))
                ingredients.append(c.text.replace('.dl-d-text{fill:#fff}','').strip())
                boxes = driver.find_elements_by_xpath('/html/body/div[6]/section[3]/div/div/div/div[2]/div[3]/div/div/div/div[1]/div/div/div/div')
                box = boxes[j].text
                uses.append(box.split(':')[0].strip())
                if 'CAS #:' in box:
                    CASs.append(box.split('CAS #:')[1].split('\n')[0].strip())
                else: 
                    CASs.append('')
                
        #Get product info
        name = driver.find_element_by_xpath('//*[@id="wrapper"]/section[2]/section/div/div/h2').text.replace('®','').strip()
        regTable = driver.find_elements_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[1]/div[3]/div/div/table/tbody/tr')
        for t in regTable:
            if 'Category' in t.text:
                category = t.text.split('Category')[-1].strip()
        src = driver.find_element_by_xpath('//*[@id="wrapper"]/section[3]/div/div/div/div[1]/div[2]/div/img').get_attribute('src')
        
        
        #Download SDS
        docLink = ''
        languages = driver.find_elements_by_xpath('//*[@id="msdsForm"]/div/div/div[1]/table/tbody/tr/td[2]')
        pdfs = driver.find_elements_by_xpath('//*[@id="msdsForm"]/div/div/div[1]/table/tbody/tr/td[3]/a')
        for x in range(0,len(languages)):
            if 'english' in languages[x].text.lower():
                docLink = pdfs[x].get_attribute('href')
                break
        if docLink == '':
            print('problem with SDS',url)
            fails+=1
            continue
        filename = ID+'_sds.pdf'
        res = requests.get(docLink)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))
            
        #Save page
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(random.randint(minTime,maxTime))
        
        Hide_elements=['class=navbar yamm interior', 'class=container-control-fuschia'] # Use full class name
        ob=Screenshot_Clipping.Screenshot()
        img_url=ob.full_Screenshot(driver, save_path=r'.', elements=Hide_elements, image_name=ID+'_page.png')
        
        image1 = Image.open(ID+'_page.png')
        im1 = image1.convert('RGB')
        im1.save(ID+'_page.pdf')
        os.remove(ID+'_page.png')
        fails = 0
        
    except: 
        print('problem with page',url)
        fails+=1
        continue

    #Comp data
    l = len(ingredients)
    chemList.extend(ingredients)
    casList.extend(CASs)
    useList.extend(uses)
    idList.extend([ID]*l)
    nameList.extend([name]*l)
    catList.extend([category]*l)

    #Prod data
    l = len(upc)
    upcList.extend(upc)
    sizeList.extend(size)
    idList2.extend([ID]*l)
    nameList2.extend([name]*l)
    brandList.extend([brand]*l)
    urlList.extend([url]*l)
    picList.extend([src]*l)


driver.close()
    
#Comp csv
df1 = pd.DataFrame({'id':idList, 'name':nameList, 'category':catList, 'chem':chemList, 'cas':casList, 'use':useList})
k=0
while os.path.exists('rb comp data '+str(k)+'.csv'):
    k+=1
df1.to_csv('rb comp data '+str(k)+'.csv',index=False, header=True)    
    

#Prod csv
df2 = pd.DataFrame({'id':idList2, 'name':nameList2, 'brand':brandList, 'upc':upcList, 'size':sizeList, 'url':urlList, 'picture url':picList})
k=0
while os.path.exists('rb prod data '+str(k)+'.csv'):
    k+=1
df2.to_csv('rb prod data '+str(k)+'.csv',index=False, header=True)   
