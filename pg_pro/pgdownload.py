import time, os, string, random, requests, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob
import pdfkit
import codecs
from urllib.request import urlopen
import shutil
from selenium.webdriver.common.action_chains import ActionChains







path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\P&G\P&G pro' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks



# chrome_options= Options()
# chrome_options.add_argument("--headless")
# options = webdriver.ChromeOptions()
# options.add_experimental_option('prefs', {
# "download.default_directory": r"C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\P&G\P&G pro", #Change default directory for downloads
# "download.prompt_for_download": False, #To auto download the file
# "download.directory_upgrade": True,
# "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
# })


# chrome_options= Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(r"C:/Users/alarger/Documents/chromedriver-win32/chromedriver.exe", options=chrome_options)
driver = webdriver.Edge(r'C:/Users/alarger/Documents/edgedriver_win64/msedgedriver.exe')
driver.maximize_window()
driver.implicitly_wait(10)

time.sleep(random.randint(minTime,maxTime))

# path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
# options = { 'quiet': ''}

#product csv columns
urlList=[] #prod page url
nameList=[] #product name
brandList=[] #brand name
fnameList=[] #file name
numList=[]
furlList=[] #file urls 
sdsnameList=[] #sds name
cupcList=[] #case upc
pupcList=[] #package upc
sizeList=[] #size
sdescList=[] #short description
picList=[] #picture name
srcList=[] #image url

#ingredient csv columns
urlList2=[]
fnameList2=[]
nameList2=[]
chemList=[]
casList=[]
funcList=[]
rankList=[]


fails=0
htmls = glob('*.html')
urls = csv.reader(open('pg pro urls.csv', encoding="utf8")) #csv of product urls
i=-1
for row in urls: 
    i+=1
    if i==0: continue
    # if i>5: break
    print(i)
    url=row[0]
    fname=url.split('/')[-2]+'_'+url.split('/')[-1]
    if fname+'_page.html' in htmls: continue

    try:
        driver.get(url)
    except: continue
    time.sleep(random.randint(minTime,maxTime))
    time.sleep(random.randint(minTime,maxTime))
    # ele=driver.find_element_by_xpath('/html/body')
    # total_height = ele.size["height"]+1000
    # driver.set_window_size(1920, total_height)
    # time.sleep(random.randint(minTime,maxTime))
    j=1

    #Save copy of webpage    
    file_object = codecs.open((fname+'_page.html'), "w", "utf-8")
    html = driver.page_source
    file_object.write(html) 
    time.sleep(random.randint(minTime,maxTime))
    
    name=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/h1').text
    brand=driver.find_element_by_xpath('//*[@id="__next"]/div/main/div/div[1]/div/div[2]/div/h2').text
    sdescrip=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/p').text
    size=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/h6').text
    try:
        cupc=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[1]/div/div[1]/span[2]').text
    except: cupc=''
    try:
        pupc=driver.find_element_by_xpath('//*[@id="Product-description"]/div/div[2]/span[2]').text
    except: pupc=''
    
    #get ingredients table
    try:
        element=driver.find_element_by_xpath('//*[@id="Safety-Ingredients"]/div/div[2]/div/div[1]/div[1]')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(random.randint(minTime,maxTime))
        element.click()
    except: pass
    
    time.sleep(random.randint(minTime,maxTime))
    # ele=driver.find_element_by_xpath('/html/body')
    # total_height = ele.size["height"]+1000
    # driver.set_window_size(1920, total_height)
    # time.sleep(random.randint(minTime,maxTime))
    t=len(driver.find_elements_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/table/tr/td[1]'))
    for r in range(2,t+2):
        chem=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/table/tr['+str(r)+']/td[1]').text
        cas=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/table/tr['+str(r)+']/td[2]').text
        func=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[3]/div/div[2]/div/div[1]/div[2]/div/div/table/tr['+str(r)+']/td[3]').text
        # print(chem,cas,func)
        
        urlList2.append(url)
        fnameList2.append(fname)
        nameList2.append(name)
        chemList.append(chem)
        casList.append(cas)
        funcList.append(func)
        rankList.append(r-1)
    if t==0:
        urlList2.append(url)
        fnameList2.append(fname)
        nameList2.append(name)
        chemList.append('')
        casList.append('')
        funcList.append('')
        rankList.append('')
    
    #Save pic
    try:
        src=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[1]/div/div/div/div[2]/div/img').get_attribute('src')
        html = urlopen(src) 
        picname = fname+'_'+str(j)+'_pic.png'
        time.sleep(random.randint(minTime,maxTime))
        output = open(picname,'wb')
        output.write(html.read())
        output.close()
        time.sleep(random.randint(minTime,maxTime))
    except: pass

    #download sds
    element=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[1]/div[2]/div[1]/div/button/p') #sds button
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    time.sleep(random.randint(minTime,maxTime))
    element.click()
    
    docs=driver.find_elements_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/a')
    if len(docs)==0: docs=driver.find_elements_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div/div/div/div/a')  
    k=0
    sdss=[]
    furls=[]
    for d in docs: 
        if d.text.lower().strip()=='english':
            k+=1
            # d.click()
            try:
                # print('here')
                filename=fname+'_'+str(j)+'_'+str(k)+'_sds.pdf'
                docLink = d.get_attribute('href')
                sdss.append(filename)
                furls.append(docLink)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',}
                res = requests.get(docLink,headers=headers)
                res.raise_for_status()
                playFile = open(filename,'wb')
                for chunk in res.iter_content(100000):
                    playFile.write(chunk)
                playFile.close()
            except: 
                print('file failed to download')
                pass
            time.sleep(random.randint(minTime,maxTime))
    driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[1]/div/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div/div/button/img').click()
    time.sleep(random.randint(minTime,maxTime))
            
                
    urlList.append(url) #prod page url
    nameList.append(name) #product name
    brandList.append(brand) #brand name
    fnameList.append(fname) #file name
    numList.append(j)
    sdsnameList.append(sdss) #sds name
    furlList.append(furls)
    cupcList.append(cupc) #case upc
    pupcList.append(pupc) #package upc
    sizeList.append(size) #size
    sdescList.append(sdescrip) #short description
    picList.append(picname) #picture name
    srcList.append(src) #image url

    try: 
        element=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/button')
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(random.randint(minTime,maxTime))
        element.click()
        time.sleep(random.randint(minTime,maxTime))
        # ele=driver.find_element_by_xpath('/html/body')
        # total_height = ele.size["height"]+1000
        # driver.set_window_size(1920, total_height)
        # time.sleep(random.randint(minTime,maxTime))
    except: pass

    n = len(driver.find_elements_by_xpath('//*[@id="More-Options"]/div/div/div/div[1]/div[2]/div[3]'))
    for m in range(1,n+1):
        # print(m)
        j+=1
        
        
        name=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[2]/div[2]').text
       
        brand=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[2]/div[1]').text
        sdescrip=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[2]/div[3]').text
        size=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[2]/div[4]').text
        try:
            cupc=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[2]/div[6]/div[1]/div[2]').text
        except: cupc=''
        try:
            pupc=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[2]/div[6]/div[2]/div[2]').text
        except:
            pupc=''
        #Save pic
        try:
            src=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[1]/div[1]/div/img').get_attribute('src')
            html = urlopen(src) 
            picname = fname+'_'+str(j)+'_pic.png'
            time.sleep(random.randint(minTime,maxTime))
            output = open(picname,'wb')
            output.write(html.read())
            output.close()
            time.sleep(random.randint(minTime,maxTime))
        except: 
            src=''
            picname=''
        
        #download sds
        element=driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div['+str(m)+']/div/div[2]/div[1]/div/button/p') #sds button
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(random.randint(minTime,maxTime))
        element.click()
        docs=driver.find_elements_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/a')
        if len(docs)==0:
            docs=driver.find_elements_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/a')
        k=0
        sdss=[]
        furls=[]
        for d in docs: 
            if d.text.lower().strip()=='english':
                k+=1
                # d.click()
                try:
                    # print('here')
                    filename=fname+'_'+str(j)+'_'+str(k)+'_sds.pdf'
                    docLink = d.get_attribute('href')
                    sdss.append(filename)
                    furls.append(docLink)
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',}
                    res = requests.get(docLink,headers=headers)
                    res.raise_for_status()
                    playFile = open(filename,'wb')
                    for chunk in res.iter_content(100000):
                        playFile.write(chunk)
                    playFile.close()
                except: 
                    print('file failed to download')
                    pass
                time.sleep(random.randint(minTime,maxTime))
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/button/img').click()
        time.sleep(random.randint(minTime,maxTime))
                
                    
        urlList.append(url) #prod page url
        nameList.append(name) #product name
        brandList.append(brand) #brand name
        fnameList.append(fname) #file name
        numList.append(j)
        sdsnameList.append(sdss) #sds name
        furlList.append(furls) #sds file urls
        cupcList.append(cupc) #case upc
        pupcList.append(pupc) #package upc
        sizeList.append(size) #size
        sdescList.append(sdescrip) #short description
        picList.append(picname) #picture name
        srcList.append(src) #image url
            
        
        
#Make csvs
l=0
while os.path.exists('pgpro prod data_'+str(l)+'.csv'):
    l+=1
df = pd.DataFrame({'url':urlList, 'prod name':nameList, 'brand':brandList, 'filenames':fnameList, 'group number':numList, 'sds names':sdsnameList, 'sds file urls':furlList, 'case upc':cupcList, 'package upc':pupcList, 'size':sizeList, 'short description': sdescList, 'picture name': picList, 'picture src':srcList})
df.to_csv('pgpro prod data_'+str(l)+'.csv',index=False, header=True)
    

df2 = pd.DataFrame({'url':urlList2, 'prod name':nameList2, 'filenames':fnameList2, 'chem':chemList, 'cas':casList, 'functional use':funcList, 'rank':rankList})
df2.to_csv('pgpro chem data_'+str(l)+'.csv',index=False, header=True)
