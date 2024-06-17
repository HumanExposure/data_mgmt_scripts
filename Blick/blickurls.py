import time, os
import pandas as pd
from selenium import webdriver






path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Blick' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks



driver = webdriver.Edge(r'C:/Users/alarger/Documents/edgedriver_win64/msedgedriver.exe')
driver.maximize_window()
driver.implicitly_wait(10)

urlList=[]

urls = ['https://www.dickblick.com/v2/sitemap/file/1','https://www.dickblick.com/v2/sitemap/file/2','https://www.dickblick.com/v2/sitemap/file/3']
for url in urls:
    driver.get(url)
    time.sleep(100) #Sitemap takes awhile to load
    links=driver.find_elements_by_tag_name('loc')
    i=0
    for l in links:
        i+=1
        if i%100==0: print(i)
        urlList.append(l.get_attribute('textContent'))
        # print(l.get_attribute('textContent'))


df = pd.DataFrame({'url':urlList})
df=df.drop_duplicates()
df.to_csv('blick urls.csv',index=False, header=True)
