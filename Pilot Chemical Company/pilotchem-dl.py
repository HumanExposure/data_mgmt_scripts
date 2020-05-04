# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 13:08:51 2020

@author: MHORTON
"""

import os, time, random, string
from selenium import webdriver
import pickle
from urllib.request import Request, urlopen
import pandas as pd

originalpath = os.getcwd()

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('useAutomationExtension', False)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

# %% Scrape site
minTime = 5 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

try: 
    products = pickle.load(open( "pilotchem-products.pkl","rb" ) )
except: #if the product dictionary is not found, scrape website for product names and urls
    #open product page
    products = pd.DataFrame()
    driver=webdriver.Chrome(executable_path=r"C:\Users\mhorton\chromedriver.exe", options=chromeOptions, 
                            desired_capabilities=chromeOptions.to_capabilities()) #Path to Chrome Driver
    driver.get("https://www.pilotchemical.com/formularies/search")
    time.sleep(random.randint(minTime,maxTime))

    #click formulary markets dropdown
    select = driver.find_element_by_xpath("//select[@id='markets']")
    select.click()
    time.sleep(1 + random.random())

    markets = []
    for x in driver.find_elements_by_xpath("//select[@id='markets']/option"):
        markets.append(x)

    titles = []
    formulas = []
    prodmarkets = []
    applications = []
    products = []
    urls = []

    for market in markets:
        market.click()
        time.sleep(random.randint(minTime,maxTime))
    
        for x in driver.find_elements_by_xpath("//h3"):
            titles.append(x.text)
        for x in driver.find_elements_by_xpath("//h4[@class='formula']"):
            formulas.append(x.text)
        for x in driver.find_elements_by_xpath("//h4[@class='market']"):
            prodmarkets.append(x.text.split(':', 1)[1].lstrip(' '))
        for x in driver.find_elements_by_xpath("//h4[@class='application']"):
            applications.append(x.text.split(':', 1)[1].lstrip(' '))
        for x in driver.find_elements_by_xpath("//h4[@class='products']"):
            products.append(x.text.split(':', 1)[1].lstrip(' '))
        for x in driver.find_elements_by_xpath("//h4[@class='techds-url']/a"):
            urls.append(x.get_attribute('href'))
    
    
    products = pd.DataFrame({'titles':titles, 'formulas':formulas, 'prodmarkets':prodmarkets, 'applications':applications, 'products':products, 'urls':urls})
    
    f = open("pilotchem-products.pkl","wb")
    pickle.dump(products,f)
    f.close()
    driver.quit()

# %% download pdfs

minTime = 4 #minimum wait time in between clicks
maxTime = 8 #maximum wait time in between clicks

finished = []
problems = []

directory = r'pdf/'

for file in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, file)):
        finished.append(file)

data = products.urls.to_list()

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
        problems.append(row)

os.chdir(originalpath)

# %% "manually" check to make sure the problem pdfs don't exist
driver=webdriver.Chrome(executable_path=r"C:\Users\mhorton\chromedriver.exe", options=chromeOptions, 
                        desired_capabilities=chromeOptions.to_capabilities()) #Path to Chrome Driver
errors = []
for problem in problems:
    print(problem)
    driver.get(problem)
    time.sleep(random.randint(minTime,maxTime))
    for x in driver.find_elements_by_xpath("//fieldset/h2"):
        x = x.text
        if '404' in x:
            print('404 error for', problem)
            errors.append(problem)
        else:
            print('Other error at', problem)

for error in errors:
    problems.remove(error)
