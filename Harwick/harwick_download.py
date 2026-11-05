import time, os, string, random, requests, csv
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


urlList=[]
prodnameList=[]
supplierList=[]
producttypeList=[]
productsubtypeList=[]
descripList=[]
sdsurlList=[]
sdsnameList=[]




service = Service(executable_path=r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe')
options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
driver.implicitly_wait(10)

urls = csv.reader(open('harwick urls.csv', encoding="utf8")) #csv of product urls
i=0
for row in urls: 
    prodname=''
    supplier=''
    producttype=''
    productsubtype=''
    descrip=''
    sdsurl=''
    filename=''
    
    url = row[0] 
    i+=1
    if i<= 453: continue
    
    if url=='url': continue
    driver.get(url)
    time.sleep(random.randint(minTime,maxTime))
    links = driver.find_elements('xpath','//*/a')
    for l in links:
        if r'/sds/' in l.get_attribute('href'):
            sdsurl=l.get_attribute('href')
            break
    if sdsurl!='':
        filename=str(i)+'.pdf'
        try:
            response = urllib.request.urlopen(sdsurl)    
            file = open(filename, 'wb')
            file.write(response.read())
            file.close()
            time.sleep(random.randint(minTime,maxTime))
        except: 
            print(i,'failed to download')
            filename=''
    try:
        descrip=driver.find_element('xpath','//*[@id="tab-description"]/div').text
    except:
        print(i,'issue with description')
    try:
        elements=driver.find_elements('xpath','//*[@id="mainContent"]/main/div/div/div/div[1]/div/div[1]/div/strong')
        j=0
        for e in elements:
            j+=1
            if e.text.lower()=='supplier partner':
                supplier=driver.find_element('xpath','//*[@id="mainContent"]/main/div/div/div/div[1]/div/div[1]/div['+str(j)+']').text
                supplier=supplier.split('\n')[-1]
            elif e.text.lower()=='product type':
                producttype=driver.find_element('xpath','//*[@id="mainContent"]/main/div/div/div/div[1]/div/div[1]/div['+str(j)+']').text
                producttype=producttype.split('\n')[-1]
            elif e.text.lower()=='product subtype':
                productsubtype=driver.find_element('xpath','//*[@id="mainContent"]/main/div/div/div/div[1]/div/div[1]/div['+str(j)+']').text
                productsubtype=productsubtype.split('\n')[-1]
    except:
        print(i,'issue with elements')
        
    urlList.append(url)
    prodnameList.append(prodname)
    supplierList.append(supplier)
    producttypeList.append(producttype)
    productsubtypeList.append(productsubtype)
    descripList.append(descrip)
    sdsurlList.append(sdsurl)
    sdsnameList.append(filename)
        
        
#Make csv
df = pd.DataFrame({'url':urlList, 'product name':prodnameList, 'supplier':supplierList, 'product type':producttypeList,'product subtype':productsubtypeList, 'description':descripList, 'sds url':sdsurlList, 'filename':sdsnameList})

df.to_csv('harwick web data.csv',index=False, header=True)    
