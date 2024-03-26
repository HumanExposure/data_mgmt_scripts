import time, os, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Greenbook' #Folder docs go into
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks



chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:/Users/alarger/Documents/chromedriver-win32 (1)/chromedriver-win32/chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)

start = 'https://www.greenbook.net/'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))


searchterms = 'qwertyuioplkjhgfdsazxcvbnm1234567890'


urlList = []
for x in searchterms:
    # x+=1
    newlink = 'https://www.greenbook.net/search?q='+x
    driver.get(newlink) #Go to starting page
    time.sleep(random.randint(minTime,maxTime))
    
    while True: #Click load more button until you can't anymore
        try:
            driver.find_element_by_xpath('//*[@id="__next"]/div/div/main/div/div[4]/div/div[3]/div[1]/div[1]/button').click()
        except: break
        time.sleep(random.randint(minTime,maxTime))
        
    urls = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/main/div/div[4]/div/div[3]/div[1]/div[1]/ul/li/a')
    
    for u in urls: 
        urlList.append(u.get_attribute('href'))
        
    if len(urls) == 1000: 
        print(x)
        for y in searchterms:
            newlink = 'https://www.greenbook.net/search?q='+x+y
            driver.get(newlink) #Go to starting page
            time.sleep(random.randint(minTime,maxTime))
            
            while True: #Click load more button until you can't anymore
                try:
                    driver.find_element_by_xpath('//*[@id="__next"]/div/div/main/div/div[4]/div/div[3]/div[1]/div[1]/button').click()
                except: break
                time.sleep(random.randint(minTime,maxTime))
                
            urls = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/main/div/div[4]/div/div[3]/div[1]/div[1]/ul/li/a')
            
            for u in urls: 
                urlList.append(u.get_attribute('href'))
                
            if len(urls) == 1000: 
                print(x,y)
                for z in searchterms:
                    # x+=1
                    newlink = 'https://www.greenbook.net/search?q='+x+y+z
                    driver.get(newlink) #Go to starting page
                    time.sleep(random.randint(minTime,maxTime))
                    
                    while True: #Click load more button until you can't anymore
                        try:
                            driver.find_element_by_xpath('//*[@id="__next"]/div/div/main/div/div[4]/div/div[3]/div[1]/div[1]/button').click()
                        except: break
                        time.sleep(random.randint(minTime,maxTime))
                        
                    urls = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/main/div/div[4]/div/div[3]/div[1]/div[1]/ul/li/a')
                    
                    for u in urls: 
                        urlList.append(u.get_attribute('href'))
                        
                    if len(urls) == 1000: 
                        print(x,y,z)
        
    

#Make csv
df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('greenbook urls 3.csv',index=False, header=True, encoding='utf8')
        

