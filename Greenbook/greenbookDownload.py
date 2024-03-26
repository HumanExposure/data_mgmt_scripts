import time, os, string, random, requests, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob
import pdfkit
import codecs




path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Greenbook' #Folder docs go into
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks



chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:/Users/alarger/Documents/chromedriver-win32 (1)/chromedriver-win32/chromedriver.exe", options=chrome_options)
driver.maximize_window()
# driver.implicitly_wait(5)

time.sleep(random.randint(minTime,maxTime))

path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}

#csv columns
urlList=[]
nameList=[]
idList=[]
prodList=[]
manufList=[]
chemList=[]
classList=[]
eparnList=[]
pestList=[]
siteList=[]


fails=0
htmls = glob('*.html')
urls = csv.reader(open('greenbook urls 4.csv', encoding="utf8")) #csv of product urls
i=-1
for row in urls: 
    i+=1
    if i == 0: continue
    # if i>10:break
    # if fails >5: break
    url = row[0]
    name = url.split('/')[-2]+'_'+url.split('/')[-1]
    if name+'_page.html' in htmls: continue #skip pages that have already been downloaded
    
    try: #get data from pages
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        prodname=driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div[1]/div/h1').text
        manuf=driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div[1]/div/a').text
        idnum=driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div[1]/div[1]/h5/span[2]').text.strip('ID: ')
        ingredients = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div[1]/div[1]/a')
        chems=''
        for n in ingredients: 
            chems=(chems+'|'+n.text).strip(' |')
        eparn=driver.find_element_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div[1]/div[2]/span[2]').text
        
        sites=''
        pests=''
       
        titles=driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div[1]/div')
        for t in range(1,len(titles)+1):
            if 'Pests' in titles[t-1].text:
                
                pestlist=driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div/div['+str(t)+']/a')
                for p in pestlist:
                    pests=(pests+'|'+p.text).strip(' |')
            if 'Sites' in titles[t-1].text:
                sitelist=driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div/div['+str(t)+']/a')
                for s in sitelist:
                    sites=(sites+'|'+s.text).strip(' |')
        classifications = driver.find_elements_by_xpath('//*[@id="__next"]/div/div/div[2]/div[2]/main/div/div[1]/div[1]/div')
        classs=''
        for c in classifications: 
            classs=(classs+'|'+c.text).replace('\n',' ').strip(' |')
        fails = 0
        
        #update lists
        urlList.append(url)
        nameList.append(name)
        idList.append(idnum)
        prodList.append(prodname)
        manufList.append(manuf)
        chemList.append(chems)
        classList.append(classs)
        eparnList.append(eparn)
        pestList.append(pests)
        siteList.append(sites)
     
        
        #save copy of page
        # pdfkit.from_url(url,name+'_page.pdf',options=options, configuration=config)
        file_object = codecs.open((name+'_page.html'), "w", "utf-8")
        html = driver.page_source
        file_object.write(html)
    except: 
        print('fail',url)
        fails+=1
    
    try: #get label
        docs = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/a')
        if len(docs)>2:print('too many docs',url)
        docurl=''
        for d in docs:
            if d.text=='Label':
                docurl=d.get_attribute('href')
                break
    
        filename = name+'_label.pdf' 
        res = requests.get(docurl)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))
    except: pass

    try: #get sds
        docs = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/a')
        docurl=''
        for d in docs:
            if d.text=='SDS':
                docurl=d.get_attribute('href')
                break
        filename = name+'_sds.pdf' 
        res = requests.get(docurl)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))
    except: pass  
    
    
   
#Make csvs
l=0
while os.path.exists('greenbook prod data_'+str(l)+'.csv'):
    l+=1
df = pd.DataFrame({'url':urlList, 'doc names':nameList, 'id':idList, 'product name':prodList, 'manufacturer':manufList, 'active ingredients':chemList, 'classification':classList, 'EPA registration number':eparnList, 'pests':pestList, 'sites': siteList})
df.to_csv('greenbook prod data_'+str(l)+'.csv',index=False, header=True)
    

        