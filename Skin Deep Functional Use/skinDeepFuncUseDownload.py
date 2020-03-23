# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:12:30 2020

@author: ALarger
"""

import time, csv, os, string, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from Screenshot import Screenshot_Clipping
from PIL import Image
from glob import glob
from time import strftime, localtime

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Functional Use' #Folder doc is in
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

idList = [] #Chemical ids
urlList = [] #Chemical page urls
nameList = [] #Chemical names
useList = [] #Functional use

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()

urls = csv.reader(open('skin deep func use urls.csv')) #csv of product urls
i=0
finished = glob('*.pdf')
fails = 0

for row in urls:
    i+=1
#    if i >= 15: continue
    if fails >= 10 and len(idList) > 0: break #If the script fails 10+ times in a row, stop running
    if int(strftime('%H',localtime())) == 6: break #stop running at 6am
    url = row[0]
    ID = url.split('/')[-2].split('-')[0]
    if ID+'.pdf' in finished: continue
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        name = driver.find_element_by_xpath('//*[@id="chemical"]/h2').text
        driver.find_element_by_xpath('/html/body/div[2]/div/main/section[2]/ul/li[2]/a').click()
        time.sleep(random.randint(minTime,maxTime))
        use = driver.find_element_by_xpath('/html/body/div[2]/div/main/section[2]/ul/li[5]/p[2]').text
        time.sleep(random.randint(minTime,maxTime))
        driver.find_element_by_xpath('/html/body/div[2]/div/main/section[4]/div[1]').click()
        time.sleep(random.randint(minTime,maxTime))
        
        #Save page
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(random.randint(minTime,maxTime))
        
        Hide_elements=[] # Use full class name
        ob=Screenshot_Clipping.Screenshot()
        img_url=ob.full_Screenshot(driver, save_path=r'.', elements=Hide_elements, image_name=ID+'.png')
        
        image1 = Image.open(ID+'.png')
        im1 = image1.convert('RGB')
        im1.save(ID+'.pdf')
        os.remove(ID+'.png')
        time.sleep(random.randint(minTime,maxTime))
        fails = 0
        
    except:
        fails += 1
        print('FAILED: ',url)
        continue
    
    #Add data to lists
    idList.append(ID)
    urlList.append(url)
    nameList.append(name)
    useList.append(use)

driver.close()

#Make csv
df = pd.DataFrame({'ewg ID':idList, 'Chemical Name':nameList, 'Functional Use':useList, 'url':urlList})
k=0
while os.path.exists('Skin Deep Functional Use '+str(k)+'.csv'):
    k+=1
df.to_csv('Skin Deep Functional Use '+str(k)+'.csv',index=False, header=True)  