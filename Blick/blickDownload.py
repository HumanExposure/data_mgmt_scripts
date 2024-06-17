
import time, os, random, requests, csv
import pandas as pd
from selenium import webdriver
from glob import glob
from urllib.request import urlopen

path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Blick' #Folder docs go into
os.chdir(path)
minTime = 1 #minimum wait time in between clicks
maxTime = 3 #maximum wait time in between clicks

driver = webdriver.Edge(r'C:/Users/alarger/Documents/edgedriver_win64/msedgedriver.exe')
driver.maximize_window()
# driver.implicitly_wait(10)

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
manufLinkList=[]
picNameList=[]
picLinkList=[]
itemnumList=[]
upcList=[]
colorList=[]
descripList=[]
mfgnumList=[]
categoryList=[]
picname=''
src=''
docLink=''
filename=''

urls = csv.reader(open('blick urls.csv', encoding="utf8")) #csv of product urls
i=-1
for row in urls: 
    i+=1
    if i<=previ: continue
    if len(urlList)>10000: break
    url = row[0] 
    if r'/items/' in url:
        name = url.split('/items/')[-1].replace('/','')
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))  
        
        #check if page has sds
        havesds=False
        tabs=driver.find_elements_by_xpath('/html/body/div[1]/div/div[3]/main/section[3]/div/div/div[1]/div/button')
        for t in tabs:
            if 'sds' in t.text.lower(): havesds=True
        if havesds==False: continue
        
        
        try: #Download pdf
            docLink = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[3]/div/div/div[2]/div[3]/div/ul/li/a').get_attribute('href')
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
            src=driver.find_element_by_xpath('//*[@id="pageContent"]/section[2]/div/div/div[2]/div/div[3]/div/ol/li/button/picture/img').get_attribute('src')
            html = urlopen(src) 
            time.sleep(random.randint(minTime,maxTime))
            output = open(picname,'wb')
            output.write(html.read())
            output.close()
            time.sleep(random.randint(minTime,maxTime))
        except: pass
        
    
        #get other info on page
        try: prodname=driver.find_element_by_xpath('//*[@id="pageContent"]/section[2]/div/div/div[1]/div[2]/h1').text
        except: prodname=''
        
        try: manufLink = driver.find_element_by_xpath('//*[@id="pageContent"]/section[2]/div/div/div[1]/div[1]/div/a').get_attribute('href')
        except: manufLink = ''
        
        try: itemnum=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[2]/div/div/div[1]/div[2]/div[2]/div/span').text
        except: itemnum=''
        
        try: upc=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[4]/div/p[1]').text
        except: upc=''
        
        try: #category=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[1]/div').text
            category=''
            elements=driver.find_elements_by_xpath('/html/body/div[1]/div/div[3]/main/section[1]/div/a')
            for e in elements[1:-1]:
                category=(category+'-'+e.text).strip('- ')
        except: category=''
        
        try:
            color=''
            descrip=''
            mfgnum=''
            n=len(driver.find_elements_by_xpath('//*[@id="product-details"]/div/div/div/div[1]/dl/dt'))
            for x in range(1,n+1): 
                element=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[3]/div/div/div[2]/div[1]/div/div/div/div[1]/dl/dt['+str(x)+']').text
                if element == 'Color:': color = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[3]/div/div/div[2]/div[1]/div/div/div/div[2]/dl/dt['+str(x)+']').text
                elif element == 'Description:': descrip = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[3]/div/div/div[2]/div[1]/div/div/div/div[2]/dl/dt['+str(x)+']').text
                elif element == 'Mfg #:': mfgnum = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/main/section[3]/div/div/div[2]/div[1]/div/div/div/div[2]/dl/dt['+str(x)+']').text
        except: 
            pass
        
        
        #append lists
        urlList.append(url)
        prodnameList.append(prodname)
        pdfnameList.append(filename)
        pdfLinkList.append(docLink)
        manufLinkList.append(manufLink)
        picNameList.append(picname)
        picLinkList.append(src)
        itemnumList.append(itemnum)
        upcList.append(upc)
        colorList.append(color)
        descripList.append(descrip)
        mfgnumList.append(mfgnum)
        categoryList.append(category)
        
        
#Make csv
df = pd.DataFrame({'url':urlList, 'product name':prodnameList, 'pdf name':pdfnameList, 'pdf link':pdfLinkList, 'manufacturer link':manufLinkList, 'pic name':picNameList, 'pic link':picLinkList, 'item number':itemnumList, 'upc':upcList, 'color':colorList, 'description':descripList, 'mfg #':mfgnumList, 'category':categoryList})

df.to_csv('blick web data '+str(i)+'.csv',index=False, header=True)    