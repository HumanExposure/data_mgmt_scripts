import time, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/FracFocus' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

urlList = [] #product page url


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)

start = r'https://fracfocus.org/wells/advanced'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))

driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div[1]/div/div').click() #click select a state
time.sleep(random.randint(minTime,maxTime))
states = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/div')
time.sleep(random.randint(minTime,maxTime))
for x in range(1,len(states)+1):
    # print(x)
    driver.get(start)
    time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div[1]/div/div').click() #click select a state
    time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/div['+str(x)+']').click()#Click state
    time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('/html/body/div/div/div/div/div/div[2]/form/button[1]/a').click() #click search jobs
    pages=driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div[3]/div/div[2]/div/div/h2/a')#get page urls
    time.sleep(random.randint(minTime,maxTime))
    for p in pages:
        if p.get_attribute('href') not in urlList: #get urls of well pages
            urlList.append(p.get_attribute('href'))



# /html/body/div/div/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/div[1]
# /html/body/div/div/div/div/div/div[2]/form/div/div[1]/div/div[2]/div/div[2]


#Make csv
df = pd.DataFrame({'url':urlList})
df.to_csv('fracfocus wells urls 2.csv',index=False, header=True, encoding='utf8')
