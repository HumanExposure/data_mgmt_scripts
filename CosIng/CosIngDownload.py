# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 11:21:07 2019

@author: ALarger
"""

import time, os, random, math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob
import pdfkit
from time import strftime, localtime
from selenium.webdriver.common.action_chains import ActionChains


path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

path = r'L:\Lab\HEM\ALarger\CosIng\Inventory (ingredient & fragrance)\Not Active' #Folder
os.chdir(path)
pdfs = glob('*.pdf')
n = 0 
for p in pdfs:
    if all(x in '1234567890.pdf' for x in p) and int(p.strip('.pdf')) > n:
        n = int(p.strip('.pdf'))

nList = []
idList = []
nameList = []
casList = []
funcList = []        
urlList = []
noteList = []

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(100)
url = 'https://ec.europa.eu/growth/tools-databases/cosing/index.cfm?fuseaction=search.simple' #url of the starting page
driver.get(url)
driver.maximize_window()


#Search ingredients/fragrance inventory
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('//*[@id="search_status"]').click() #Status 
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('//*[@id="search_status"]/option[3]').click() #2 for active, 3 for not active
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('//*[@id="search_scope"]').click() #Scope
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('//*[@id="search_scope"]/option[2]').click() #2 for inventory, 3 for banned, etc.
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('//*[@id="searchSimple"]/table/tbody/tr[5]/td[2]/input').click() #click search

#Navigate to correct page
pageNumber = math.floor(n/100)
mod = n%100
i=0
while i < pageNumber:
    i+=1
    time.sleep(random.randint(minTime,maxTime))
    if i == 1:
        driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody/tr[1]/td/span[1]').click() #click next page (if on first page)
    else: 
        driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody/tr[1]/td/span[3]').click() #click next page

while True:
    for m in range(mod,100):
        n+=1
        links = driver.find_elements_by_xpath('//*[@id="searchResults"]/table/tbody/tr/td[2]/a')
        url = links[m].get_attribute('href')

        time.sleep(random.randint(minTime,maxTime))
        try:
            ActionChains(driver).move_to_element(links[m]).click(links[m]).perform() #scroll to next link and click
        except:
            driver.get(url) #if driver does not scroll to correct place, just go to the url
        time.sleep(random.randint(minTime,maxTime))
        elements = driver.find_elements_by_xpath('//*[@id="content_main"]/table/tbody/tr/td')
        name = ''
        cas = ''
        functions = []
        j=0
        while j < len(elements)-1: 
            if elements[j].text.strip() == 'INCI Name':
                name = elements[j+1].text.lower().strip()
            elif elements[j].text.strip() == 'CAS #':
                cas = elements[j+1].text.lower().strip()
            elif elements[j].text.strip() == 'Functions':
                functions = elements[j+1].text.lower().split('\n')
            j+=1
        
        try:
            pdfkit.from_url(url,str(n)+'.pdf',options=options, configuration=config)
        except: 
            pass #pdfs that fail to download will be saved manually
         
        l=len(functions)
        if l == 0: 
            l = 1
            functions = ['']
        funcList.extend(functions)
        nList.extend([n]*l)
        idList.extend([url.split('=')[-1]]*l)
        nameList.extend([name]*l)
        casList.extend([cas]*l)
        urlList.extend([url]*l)
            
        if int(strftime('%H',localtime())) >= 17: #if its after 5pm: stop running
            break
        time.sleep(random.randint(minTime,maxTime))
        driver.find_element_by_xpath('//*[@id="content_main"]/p/input').click() #back to list
        
    if int(strftime('%H',localtime())) >= 17 or n > 27401: #if its after 5pm or the last page is finished: stop running
        break
    time.sleep(random.randint(minTime,maxTime))
    try:
        driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody/tr[1]/td/span[3]').click() #click next page
    except:
        driver.find_element_by_xpath('//*[@id="searchResults"]/table/tbody/tr[1]/td/span[1]').click() #click next page (if on first page)
    mod = 0


driver.close()

df = pd.DataFrame({'pdf number':nList, 'CosIng ID':idList, 'name':nameList, 'cas':casList, 'function':funcList, 'url':urlList})
k=0
while os.path.exists('CosIng Inventory Not Active '+str(k)+'.csv'):
    k+=1
df.to_csv('CosIng Inventory Not Active '+str(k)+'.csv',index=False, header=True)