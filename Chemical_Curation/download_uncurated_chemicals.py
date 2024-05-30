# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 11:25:03 2022

@author: ALarger

Downloads uncurated chemicals lists less than 50 records long and combines them
"""

import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import re
from glob import glob

stime = time.strftime('%Y-%m-%d_%H-%M-%S')
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/chemical curation files'+r'/uncurated_chems_'+stime #Folder docs go into
os.mkdir(path)
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks

chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(60)

start = 'https://ccte-factotum.epa.gov/login/'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))


#Login
username = input("Enter username: ")
password = input("Enter password: ")
user = driver.find_element_by_xpath('//*[@id="id_username"]')
user.send_keys(username) #type username
time.sleep(random.randint(minTime,maxTime))
passw = driver.find_element_by_xpath('//*[@id="id_password"]')
passw.send_keys(password) #type password
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('/html/body/div[3]/form/button').click() #press sign in
time.sleep(random.randint(minTime,maxTime))

#download lists
driver.get('https://ccte-factotum.epa.gov/chemical_curation/')
time.sleep(random.randint(minTime,maxTime))
prodlen = len(driver.find_elements_by_xpath('//*[@id="id_data_group"]/option'))
for x in range(1,prodlen):
    name = driver.find_element_by_xpath('//*[@id="id_data_group"]/option['+str(x+1)+']').text
    records = int(name.split('(')[-1].split(' records)')[0])
    if records > 900: continue
    
    select = Select(driver.find_element_by_xpath('//*[@id="id_data_group"]')) #Product dropdown box
    select.select_by_index(x) #select next product in dropdown box
    time.sleep(random.randint(minTime,maxTime))
    
time.sleep(random.randint(minTime,maxTime))
#combine csvs
files = glob('*.csv')
df = pd.concat([pd.read_csv(f) for f in files])
df = df.drop_duplicates()
df.to_csv('uncurated_chemicals_'+stime+'.csv',index=False, header=True)

    
    
    
    
