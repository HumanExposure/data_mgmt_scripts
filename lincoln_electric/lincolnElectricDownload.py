

import time, os, string, random, requests, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob
# import urllib


path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Lincoln Electric/lincoln electric' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks


pdfs = glob('*.pdf')
urls = csv.reader(open('lincoln electric urls.csv')) #csv of product urls
i=0
for row in urls: 
    url = row[0]
    if url == 'url': continue
    i+=1
    name = str(i)+'_id.pdf'
    if name in pdfs: continue
    
    try: #Download sds
        filename = str(i)+'_id.pdf'
        res = requests.get(url)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))
    
    except: 
        print('failed!',url)
        pass
            

        
