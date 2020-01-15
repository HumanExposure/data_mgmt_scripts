# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:29:26 2020

@author: ALarger
"""

import time, csv, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\Zep' 
os.chdir(path)   
minTime = 10 #minimum wait time in between clicks
maxTime = 20 #maximum wait time in between clicks

skuList = [] #Product number
nameList = [] #Product name
brandList = [] #Product brand
matgroupList = [] #Material group (parent id equivalent?)
odorList = [] #Odor/fragrance
colorList = [] #Product color
mattypeList = [] #Material type
catList = [] #Category
sizeList = [] #Size of product
upcList = [] #Product upc
packsizeList = [] #Size of the pack of products
caseupcList = [] #upc of the case of products
urlList = [] #Product page url
picList = [] #Product picture src
   
chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.maximize_window()


urls = csv.reader(open('zep urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    if i <= 945: continue
    if i%100 == 0: print(i)
    if fails >= 10: break
    url = row[0]
    
    try:
        time.sleep(random.randint(minTime,maxTime))
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/a').click() #Click "Product details"
        name = url.split('/')[-1].replace('-',' ').strip()
        deets = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/ul/li/ul/li/div')
        for x in range(0,len(deets)):
                deets[x] = deets[x].text.replace('»','-').strip()
        brand = ''
        matgroup = ''
        odor = ''
        color = ''
        mattype = ''
        category = ''
        for x in range(0,len(deets)):
            if deets[x] == 'Brand:':
                brand = deets[x+1]
            elif deets[x] == 'Material Group:':
                matgroup = deets[x+1]
            elif deets[x] == 'Odor/Fragrance:':
                odor = deets[x+1]
            elif deets[x] == 'Color:':
                color = deets[x+1]
            elif deets[x] == 'Material Type:':
                mattype = deets[x+1]
            elif deets[x] == 'Category/Categories:':
                category = deets[x+1].replace('\n',' / ')
        
        prodRows = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/ul/li/table/tbody/tr')
        for x in range(0,len(prodRows)):
            prodRows[x] = prodRows[x].text.strip()
        prodRows = list(filter(None, prodRows))
    except: 
        print('problem with page',url)
        fails += 1
        continue
    
    for x in range(0,len(prodRows)):
        try:
            sku = prodRows[x].strip().split(' ')[0]
            if sku in skuList:
                print('help with sku!',sku,url)
            pics = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[1]/div/div[2]/div[1]/div/div/div/img')
            pic = ''
            for p in pics:
                if p.get_attribute('src').split('/')[-1].split('_')[0] == sku:
                    pic = p.get_attribute('src')
    
            time.sleep(random.randint(minTime,maxTime))
            driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/ul/li/table/tbody['+str(x*2+1)+']/tr/td[2]').click()
     
            stuff = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/ul/li/table/tbody/tr/td/ul/li/div') 
            for x in range(0,len(stuff)):
                stuff[x] = stuff[x].text.strip()
            stuff = list(filter(None, stuff))
            size = ''
            upc = ''
            packsize = ''
            caseupc = ''
            for y in range(0,len(stuff)):
                if stuff[y] == 'Container Size/Volume:':
                    size = stuff[y+1]
                elif stuff[y] == 'Each UPC:':
                    upc = stuff[y+1]
                elif stuff[y] == 'Pack Size:':
                    packsize = stuff[y+1]
                elif stuff[y] == 'Case UPC:':
                    caseupc = stuff[y+1]

            time.sleep(random.randint(minTime,maxTime))
            driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[2]/a').click() #Click "Resources/ingredient disclosures"
            docRows = driver.find_elements_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[2]/ul/li/table/tbody/tr')
            for z in range(1,len(docRows)+1):
                if sku == driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[2]/ul/li/table/tbody/tr['+str(z)+']/td[1]').text:
                    time.sleep(random.randint(minTime,maxTime))
                    doc = driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[2]/ul/li/table/tbody/tr['+str(z)+']/td[3]/a')
                    docLink = doc.get_attribute('href')
                    if doc.text == 'SDS Sheet':
                        filename = sku+'_SDS.pdf'
                        res = requests.get(docLink)
                        res.raise_for_status()
                        playFile = open(filename,'wb')
                        for chunk in res.iter_content(100000):
                            playFile.write(chunk)
                        playFile.close()
                    elif doc.text == 'Ingredient Disclosure':
                        filename = sku+'_ID.pdf'
                        res = requests.get(docLink)
                        res.raise_for_status()
                        playFile = open(filename,'wb')
                        for chunk in res.iter_content(100000):
                            playFile.write(chunk)
                        playFile.close()
                    fails = 0
        
        except:
            print('problem with product: '+sku,url)
            time.sleep(random.randint(minTime,maxTime))
            driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/a').click() #Click "Product details" 
            fails += 1
            continue

        skuList.append(sku)
        nameList.append(name)
        brandList.append(brand)
        matgroupList.append(matgroup)
        odorList.append(odor)
        colorList.append(color)
        mattypeList.append(mattype)
        catList.append(category)
        sizeList.append(size)
        upcList.append(upc)
        packsizeList.append(packsize)
        caseupcList.append(caseupc)
        urlList.append(url)
        picList.append(pic)

        time.sleep(random.randint(minTime,maxTime))
        driver.find_element_by_xpath('//*[@id="aspnetForm"]/div[3]/div[2]/div/ul/li[1]/a').click() #Click "Product details"            


driver.close()

#Make csv
df = pd.DataFrame({'sku':skuList, 'name':nameList, 'brand':brandList, 'material group':matgroupList, 'Odor':odorList, 'color':colorList, 'material type':mattypeList, 'category':catList,'size':sizeList, 'upc':upcList, 'pack size':packsizeList, 'case upc':caseupcList, 'url':urlList, 'picture url':picList})
df.to_csv('zep scraped data.csv',index=False, header=True)