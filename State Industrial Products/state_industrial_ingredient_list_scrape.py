import os
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import time
import random
import pandas as pd




path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\State Industrial ingredients lists'
os.chdir(path)
cService = webdriver.ChromeService(executable_path=r'c:\Users\alarger\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe')
chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service = cService,options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks
actions = ActionChains(driver)

nameList=[]
prodList=[]
chemList=[]
casList=[]
funcList=[]


url = "https://www.stateindustrial.com/support/ingredients"
driver.get(url)
time.sleep(random.randint(minTime,maxTime))
driver.find_element('xpath','//*[@id="eu-cookie-ok"]').click()
time.sleep(random.randint(minTime,maxTime))


products = driver.find_elements('xpath','/html/body/main/div[7]/div[3]/div[2]/div/div/div/div[2]/div[2]/ul/li')
for x in range(0,len(products)):
    name=str(x)
    print(x)
    driver.get(url)
    time.sleep(random.randint(minTime,maxTime))
    products = driver.find_elements('xpath','/html/body/main/div[7]/div[3]/div[2]/div/div/div/div[2]/div[2]/ul/li')
    prodname=(products[x].text).replace('®','').replace('™','')
    actions.move_to_element(products[x]).click().perform()
    time.sleep(random.randint(minTime,maxTime))

    #get chems
    chems=driver.find_elements('xpath','//*[@id="ingredientWrapper"]/div[2]/div[2]/ul/li['+str(x+1)+']/div/div[1]/div/table/tbody/tr/td[1]')
    cass=driver.find_elements('xpath','//*[@id="ingredientWrapper"]/div[2]/div[2]/ul/li['+str(x+1)+']/div/div[1]/div/table/tbody/tr/td[2]')
    funcs=driver.find_elements('xpath','//*[@id="ingredientWrapper"]/div[2]/div[2]/ul/li['+str(x+1)+']/div/div[1]/div/table/tbody/tr/td[3]')
    
    if len(chems) == 0:
        nameList.append(name)
        prodList.append(prodname)
        chemList.append('')
        casList.append('')
        funcList.append('')
    else:
        for y in range(0,len(chems)):
            nameList.append(name)
            prodList.append(prodname)
            chemList.append(chems[y].get_attribute('textContent'))
            casList.append(cass[y].get_attribute('textContent'))
            funcList.append(funcs[y].get_attribute('textContent'))
    time.sleep(random.randint(minTime,maxTime))
    
    
    # # Save html
    # file_object = codecs.open((name+'.html'), "w", "utf-8")
    # html = driver.page_source
    # file_object.write(html) 
    
    
df = pd.DataFrame({'doc name':nameList, 'product name':prodList, 'ingredient':chemList, 'cas':casList, 'function':funcList})
df.to_csv('state industrial ingredient lists 2.csv',index=False, header=True)
    
