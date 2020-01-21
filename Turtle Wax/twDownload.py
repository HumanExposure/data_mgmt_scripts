# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 13:15:10 2020

@author: ALarger
"""


import time, os, random, requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

path = r'L:\Lab\HEM\ALarger\Turtle Wax' 
os.chdir(path)   
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(20)
driver.maximize_window()

starturl = 'https://idd.turtlewax.com/'
driver.get(starturl)

time.sleep(random.randint(minTime,maxTime))
names = driver.find_elements_by_xpath('//*/tbody/tr/td[2]')
docs = driver.find_elements_by_xpath('//*/tbody/tr/td[3]/a')
for n in range(0,len(names)):
    link = docs[n].get_attribute('href')
    name = names[n].text.replace('/','-')
    filename = name+'.pdf'
    res = requests.get(link)
    res.raise_for_status()
    playFile = open(filename,'wb')
    for chunk in res.iter_content(100000):
        playFile.write(chunk)
    playFile.close()
    time.sleep(random.randint(minTime,maxTime))

driver.close()
    