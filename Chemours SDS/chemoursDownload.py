# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 16:26:45 2022

@author: ALarger
"""


import time, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Chemours SDS' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

idList = [] #ID numbers for naming files
nameList = [] #Product name
manufList = [] #Manufacturer name
partList = [] #Part number
sdsList = [] #SDS number


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(60)

start = 'https://www.opteon.com/en?_gl=1*zale85*_ga*MTI1NTQwMjEyLjE2NjMzNTk1NDY.*_ga_3T57CXVGEP*MTY2MzM1OTU0Ni4xLjEuMTY2MzM2MDA5NS42MC4wLjA.&_ga=2.155550587.1984174699.1663359546-125540212.1663359546'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('/html/body/div[1]/header/div/div/div[2]/nav/ul/li[2]/a').click()
time.sleep(random.randint(minTime,maxTime))

driver.switch_to.window(driver.window_handles[1]) #switch to new tab
time.sleep(random.randint(minTime,maxTime))
driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[1]/div/div[2]/div/div/div[6]/div/div[1]/input[2]').click() #click show all
time.sleep(random.randint(minTime,maxTime))


downloaded = glob('*.pdf')

n=0
nPages = int(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ctl00_Grid01_footer"]/table/tbody/tr/td[2]/div/strong[2]').text)
for i in range(nPages):
    docs=driver.find_elements_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/div/a')
    for j in range(2,len(docs)+2):  #For each row
        
        #Get data in rows
        n+=1
        if str(n)+'_sds.pdf' in downloaded: continue #skip documents that have already been downloaded
        
        idList.append(n)
        nameList.append(driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr['+str(j)+']/td[3]').text.strip())
        manufList.append(driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr['+str(j)+']/td[4]').text.strip())
        partList.append(driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr['+str(j)+']/td[5]').text.strip())
        sdsList.append(driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr['+str(j)+']/td[6]').text.strip())
        
        #Download USA English versions of pdfs
        try: 
            driver.find_element_by_xpath('/html/body/form/div[6]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr['+str(j)+']/td[1]/div/a').click()
            time.sleep(random.randint(minTime,maxTime))
            versions = driver.find_elements_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ctl00_DocumentListPopupHost1_div"]/div/div')
            docLink = ''
            for k in range(0,len(versions)):
                if "USA" in versions[k].text and "English" in versions[k].text:
                    # print(versions[k].text)
                    docLink = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ctl00_DocumentListPopupHost1_div"]/div/div['+str(k+1)+']/div[2]/a[1]').get_attribute('href')
                    break
            if docLink == '':
                print('problem with SDS',sdsList[-1])
                driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/a[4]').click() #close documents popup
                time.sleep(random.randint(minTime,maxTime))
                continue
            filename = str(n)+'_sds.pdf'
            res = requests.get(docLink)
            res.raise_for_status()
            playFile = open(filename,'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
            time.sleep(random.randint(minTime,maxTime))
            
            driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/a[4]').click() #close documents popup
            time.sleep(random.randint(minTime,maxTime))
        except: 
            print('problem with SDS',sdsList[-1])
            time.sleep(random.randint(minTime,maxTime))
        
    driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ctl00_Grid01_footer"]/table/tbody/tr/td[1]/table/tbody/tr/td[5]').click() #Navigate to next page
    time.sleep(random.randint(minTime,maxTime))
    


# driver.close()


#Make csv
df = pd.DataFrame({'id':idList, 'product name':nameList, 'manufacturer':manufList, 'sds number':sdsList})
df.to_csv('chemours scraped data 2.csv',index=False, header=True, encoding='utf8')
