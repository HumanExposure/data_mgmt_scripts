
import time, os, random, requests, csv
import pandas as pd
from selenium import webdriver
from glob import glob
from urllib.request import urlopen

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\3M 2024' #Folder docs go into
os.chdir(path)
minTime = 1 #minimum wait time in between clicks
maxTime = 3 #maximum wait time in between clicks

driver = webdriver.Edge(r'C:/Users/alarger/Documents/edgedriver_win64/msedgedriver.exe')
driver.maximize_window()
driver.implicitly_wait(10)

previ=0
docs = glob('*.pdf')
csvs = glob('*.csv')
for c in csvs:
    c=c.split(' ')[-1].split('.')[0]
    if all(x in '1234567890' for x in c): 
        c=int(c)
        if c>previ: previ=c
    

urlList=[]
prodnameList=[]
pdfnameList=[]
pdfLinkList=[]
picNameList=[]
picLinkList=[]
prodnumList=[]
itemnumList=[]
upcList=[]
descripList=[]
categoryList=[]
picname=''
src=''
docLink=''
filename=''
descrip=''

urls = csv.reader(open('3m 2024 urls_3.csv', encoding="utf8")) #csv of product urls
i=-1
for row in urls: 
    i+=1
    if i<previ: continue
    if len(urlList)>1500: break
    print(len(urlList))

    url = row[0] 
    if url=='url': continue
    
    name = url.split('/p/d/')[-1].replace('/','')
    driver.get(url)
    time.sleep(random.randint(minTime,maxTime))  
    
    #check if page has sds
    havesds=False
    links = driver.find_elements_by_tag_name('a')
    for l in links:
        if 'safety data sheet' in l.text.lower(): 
            # print(l.text.lower())
            havesds=True
            docLink=l.get_attribute('href')
            break
    if havesds==False: continue

    try: #Download pdf
        filename = name+'_sds.pdf'
        res = requests.get(docLink)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))            
    except: 
        continue

        
    try: #download picture
        picname = name+'_pic.png'
        src=driver.find_element_by_xpath('//*[@id="SNAPS2_root"]/section/div[2]/div/div[1]/div/div/button/img').get_attribute('src')
        if src!='https://www.3m.com/3m_theme_assets/themes/3MTheme/assets/images/unicorn/NoImage.jpg': 
            html = urlopen(src) 
            time.sleep(random.randint(minTime,maxTime))
            output = open(picname,'wb')
            output.write(html.read())
            output.close()
            time.sleep(random.randint(minTime,maxTime))
    except: pass
        
    
    #get other info on page
    try: prodname=driver.find_element_by_xpath('//*[@id="SNAPS2_root"]/section/div[1]/h1').text
    except: prodname=''
        
    #get id numbers from top
    itemnum=''
    upc=''
    prodnum=''
    elements = driver.find_elements_by_xpath('//*[@id="SNAPS2_root"]/section/div[1]/div/ul/li')
    for e in elements:
        # print(e.text)
        e=e.text.lower().strip()
        if '3m product number' in e: prodnum=e
        elif '3m id' in e: itemnum=e
        elif 'upc' in e: upc=e

        
    try: 
        category=''
        elements=driver.find_elements_by_xpath('//*[@id="pageContent"]/div[1]/div/ol/li/a')
        for e in elements[2:]:
            category=(category+'-'+e.text).strip('- ')
    except: category=''
    
    try: descrip=driver.find_element_by_xpath('//*[@id="SNAPS2_root"]/section/div[3]/div[2]').text
    except: descrip=''
        
        
    #append lists
    urlList.append(url)
    prodnameList.append(prodname)
    pdfnameList.append(filename)
    pdfLinkList.append(docLink)
    picNameList.append(picname)
    picLinkList.append(src)
    prodnumList.append(prodnum)
    itemnumList.append(itemnum)
    upcList.append(upc)
    descripList.append(descrip)
    categoryList.append(category)
        
driver.close()
        
#Make csv
df = pd.DataFrame({'url':urlList, 'product name':prodnameList, 'pdf name':pdfnameList, 'pdf link':pdfLinkList, 'pic name':picNameList, 'pic link':picLinkList, 'product number':prodnumList, 'item number':itemnumList, 'upc':upcList, 'description':descripList,  'category':categoryList})

df.to_csv('3m web data '+str(i)+'.csv',index=False, header=True)    
