# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 12:32:03 2019

@author: ALarger
"""

import cfscrape
import re, time
import pandas as pd
from bs4 import BeautifulSoup

categories = [] #Links for each product type
url = 'https://www.ewg.org/skindeep/'
scraper = cfscrape.create_scraper() 
page = scraper.get(url).content
soup = BeautifulSoup(page,"lxml")
for link in soup.findAll('a', attrs={'href': re.compile("^/skindeep/browse/")}):
    categories.append('https://www.ewg.org'+link.get('href'))
    
urls = [] #urls for each product

for cat in categories[8:31]: #Change index for different categories
    try:
        print(cat)
        time.sleep(5)
        page = scraper.get(cat).content
        soup = BeautifulSoup(page,"lxml")
        paging = soup.find_all('div',{'class':'light'})
        paging_link = paging[0].find_all('a')
        last_page = int([item.get('href').split('=')[-1] for item in paging_link][-2])
        for i in range(0,last_page+1,10):
            time.sleep(5)
            page_url = ('https://www.ewg.org'+'='.join(paging_link[-1].get('href').split('=')[:-1])+'='+str(i))
            print(page_url)
            page = scraper.get(page_url).content
            soup = BeautifulSoup(page,"lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("^/skindeep/product/")}):
                urls.append('https://www.ewg.org'+link.get('href'))
    except: pass
#    break
scraper.close()

df = pd.DataFrame({'url':urls})
df=df.drop_duplicates()
df.to_csv(r'L:\Lab\HEM\ALarger\Skin Deep\Makeup\ewg makeup urls.csv',index=False, header=False)