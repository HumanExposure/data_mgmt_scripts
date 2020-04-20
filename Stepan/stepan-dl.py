# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:08:51 2020

@author: MHORTON
"""

import os, time, random, string
from selenium import webdriver
import pickle
from urllib.request import Request, urlopen

originalpath = os.getcwd()

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('useAutomationExtension', False)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

# %% Scrape site for product pages
minTime = 5 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

try: 
    products = pickle.load(open( "stepan-products.pkl","rb" ) )
except: #if the product dictionary is not found, scrape website for product names and urls
    #open product page
    driver=webdriver.Chrome(executable_path=r"C:\Users\mhorton\chromedriver.exe", options=chromeOptions, 
                            desired_capabilities=chromeOptions.to_capabilities()) #Path to Chrome Driver
    driver.get("https://www.stepan.com/Products/Product-Finder.aspx")
    time.sleep(random.randint(minTime,maxTime))
    
    #close cookie disclosure
    cookies = driver.find_element_by_xpath("//input[@id='AcceptCookie']")
    cookies.click()
    time.sleep(1 + random.random())
    
    #select Region
    region = driver.find_elements_by_class_name('topLevel') 
    region[0].click()
    time.sleep(1 + random.random())
    
    #select North America
    na = driver.find_element_by_class_name('chkFirstLvl_2765')
    na.click()
    time.sleep(1 + random.random())
    
    #deselect Canada
    ca = driver.find_element_by_class_name('chkSecondLvl_2766')
    ca.click()
    time.sleep(1 + random.random())
    
    names = []
    urls = []
    
    while True:
        for x in driver.find_elements_by_xpath("//td[@class='name']/a"):
            names.append(x.text)
            urls.append(x.get_attribute('href'))
        try:
            nextPage = driver.find_element_by_xpath("//input[@value='Next']")
            nextPage.click()
            time.sleep(random.randint(minTime,maxTime))
        except: break
    
    products = dict(zip(names, urls)) 
    
    f = open("stepan-products.pkl","wb")
    pickle.dump(products,f)
    f.close()
    
    driver.quit()

# %% Scrape product pages for SDS urls
try: #to open the SDS dictionary from pickles
    sdss = pickle.load(open( "stepan-sdsurls.pkl","rb" ) )

except: #go to each product page and find the SDS url
    prods = []
    urls = []
    sdss = {}
    errors = []
    driver=webdriver.Chrome(executable_path=r"C:\Users\mhorton\chromedriver.exe", options=chromeOptions,
                                desired_capabilities=chromeOptions.to_capabilities()) #Path to Chrome Driver

    for k, v in products.items():
        prods.append(k)
        urls.append(v)    
        driver.get(v)
        time.sleep(random.randint(minTime,maxTime))
        try:
            for x in driver.find_elements_by_xpath("//a[contains(text(), 'SDS')]"):
                try:
                    sdss.update({v : x.get_attribute('href')})
                except:
                    errors.append(v)
                    print('No SDS found at:', v)
        except: print('error at:', v)

    f = open("stepan-sdsurls.pkl","wb")
    pickle.dump(sdss,f)
    f.close()

    driver.quit()

# %% Set aside missing SDS links
sdspages = []
sdsurls = []
missingsds = []

try:
    nosds = pickle.load(open( "stepan-nosds.pkl","rb" ) )
except:
    for k,v in sdss.items():
        sdspages.append(k)
        sdsurls.append(v)
    
    for k,v in products.items():
        if v not in sdspages:
            missingsds.append(v)
    
    f = open("stepan-nosds.pkl","wb")
    pickle.dump(missingsds,f)
    f.close()

# %% download SDS pdfs

minTime = 4 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

finished = []

directory = r'sds/'

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        finished.append(file)

data = sdsurls

path = directory #Folder the PDFs should go to 
os.chdir(path)

for row in data:
    try:
        name = row.split('/')[-1]
#        print(name)
        if name in finished:
            print(name, 'is already downloaded.')
            continue
#        print(row)
        site = row
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        time.sleep(random.randint(minTime,maxTime))
        output = open(name,'wb')
        output.write(page.read())
        output.close()
        finished.append(name)
        print(name, 'downloaded')
    except:
        print('problem with:',name,row)

os.chdir(originalpath)
