import time, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from glob import glob
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
import urllib

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Harwick' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks


service = Service(executable_path=r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.implicitly_wait(10)

urlList=[]
nameList=[]

url = 'https://harwick.com/categories?s='
driver.get(url)
time.sleep(random.randint(minTime,maxTime)) 

i=0
while True:
    i+=1
    if i>=18: break
    url = 'https://harwick.com/categories?s=&page='+str(i)
    driver.get(url)
    time.sleep(random.randint(minTime,maxTime)) 


    pages = driver.find_elements('xpath','/html/body/div/div[2]/div/div[2]/main/div/div/div/div[2]/div/section/div[2]/div/table/tbody/tr/th/a')
    for p in pages: 
        urlList.append(p.get_attribute('href'))
        nameList.append(p.text)
        print(nameList[-1])
    


df = pd.DataFrame({'url':urlList,'name':nameList})
df=df.drop_duplicates()
df.to_csv('harwick urls.csv',index=False, header=True)
