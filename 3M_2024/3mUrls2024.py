import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\3M 2024' #Folder docs go into
os.chdir(path)
minTime = 1 #minimum wait time in between clicks
maxTime = 3 #maximum wait time in between clicks



driver = webdriver.Edge(r'C:/Users/alarger/Documents/edgedriver_win64/msedgedriver.exe')
driver.maximize_window()
driver.implicitly_wait(10)

urlList=[]


start = 'https://www.3m.com/3M/en_US/p/'
driver.get(start)
time.sleep(20)

catlinks=[]
elements = driver.find_elements_by_xpath('//*[@id="SNAPS2_root"]/div/div[2]/div/ul/li/a')
for e in elements: catlinks.append(e.get_attribute('href'))

for c in catlinks: 
    driver.get(c)
    time.sleep(random.randint(minTime,maxTime))
    
    elements=driver.find_elements_by_tag_name('a')
    for e in elements: 
        e=e.get_attribute('href')
        if isinstance(e, str) and '/p/d/' in e and e not in urlList:
            urlList.append(e)
    
    while True: 
        try:
            element=driver.find_element_by_xpath('//*[@id="SNAPS2_root"]/div/div/div[2]/div[2]/button')
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            time.sleep(random.randint(minTime,maxTime))
            element.click()
            time.sleep(5)
          
            elements=driver.find_elements_by_tag_name('a')
            for e in elements: 
                e=e.get_attribute('href')
                if isinstance(e, str) and '/p/d/' in e and e not in urlList:
                    urlList.append(e)
        except: break
 


df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('3m 2024 urls_3.csv',index=False, header=True)

