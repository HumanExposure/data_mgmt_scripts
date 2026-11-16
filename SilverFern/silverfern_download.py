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
from selenium.webdriver.common.action_chains import ActionChains


path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\silverfern' #Folder docs go into
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks


service = Service(executable_path=r'c:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.implicitly_wait(10)

urlList=[]

url = 'https://www.silverfernchemical.com/safety-data-sheets'
driver.get(url)
time.sleep(random.randint(minTime,maxTime)) 

titleList=[]
fileList=[]
urlList=[]
i=0
while True:
    if i>562: break
    j=0
    rows = driver.find_elements('xpath','//*[@id="silverfern_datatable"]/tbody/tr/td[1]')
    for r in rows:
        i+=1
        j+=1
        titleList.append(r.text)
        try:
            sdsurl=driver.find_element('xpath','//*[@id="silverfern_datatable"]/tbody/tr['+str(j)+']/td[2]/a').get_attribute('href')
            filename=str(i)+'.pdf'
        except:
            sdsurl=''
            filename=''
        if filename != '':  
            try:
                response = urllib.request.urlopen(sdsurl)    
                file = open(filename, 'wb')
                file.write(response.read())
                file.close()
                time.sleep(random.randint(minTime,maxTime))
                
            except: 
                print(i,'failed to download',sdsurl)
                filename=''
        fileList.append(filename)
        urlList.append(sdsurl)        
        
    #Click next page button
    try:     
        button=driver.find_element('xpath','//*[@id="silverfern_datatable_next"]')
        actions = ActionChains(driver)
        actions.move_to_element(button).perform()
        time.sleep(random.randint(minTime,maxTime))
        button.click()    
        time.sleep(random.randint(minTime,maxTime))
    except:
        break
        


df = pd.DataFrame({'title':titleList,'filename':fileList,'document url':urlList})
df=df.drop_duplicates()
df.to_csv('silver fern webdata.csv',index=False, header=True)
