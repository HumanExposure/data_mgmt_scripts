# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:18:13 2021

@author: ALarger
"""


import time, random, csv, os, requests, pdfkit, codecs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from PIL import Image
from Screenshot import Screenshot_Clipping
from PIL import Image
from glob import glob



execfile = "wkhtmltopdf.exe"
execpath = 'C:\\Users\\alarger\\Documents\\wkhtmltopdf\\bin\\'

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Big D/Big D New' #Folder doc is in
os.chdir(path)

idList = []
nameList = []
colorList = []
sizeList = []
categoryList = []
upcList = []
dateList = []
descripList = []
urlList = []
# descrip2List = []
chemList = []
casList = []
funcList = []

minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

chrome_options = Options()
#chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()
time.sleep(random.randint(minTime,maxTime))

urls = csv.reader(open('big d urls.csv', encoding='utf8')) #csv of product urls
pages = glob('*page.pdf')

for row in urls:
    chem = []
    cas = []
    func = []
    docLink = ''
    name = ''
    color = ''
    size = ''
    cat = '' 
    descrip = ''
    upc = ''
    date = ''

    
    try:
        url = row[0]
        ID = url.split('numbers/')[-1].strip('/ ')
        if ID+'_page.pdf' in pages: continue
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
    
        try:
            name = driver.find_element_by_xpath('//*[@id="comp-jctauvhi"]').text
        except: #reload page and try again
            driver.get(url)
            time.sleep(random.randint(minTime,maxTime))
            name = driver.find_element_by_xpath('//*[@id="comp-jctauvhi"]').text
        # prodnum = driver.find_element_by_xpath('//*[@id="comp-jctb8wa7"]/p').text
        color = driver.find_element_by_xpath('//*[@id="comp-jctlxais"]/p').text
        size = driver.find_element_by_xpath('//*[@id="comp-jctbdrsb"]/p').text
        cat = driver.find_element_by_xpath('//*[@id="comp-jctlxj51"]/p').text
        descrip = driver.find_element_by_xpath('//*[@id="comp-jctlxrkw"]/p').text
        upc = driver.find_element_by_xpath('//*[@id="comp-jctbb7dq"]').text
        date = driver.find_element_by_xpath('//*[@id="comp-jdex9ek2"]/p').text
        date = date.strip().split(' ')[-1]
        # chems = driver.find_elements_by_xpath('//*[@id="comp-k5cv09y8"]/p/span')
        
        # longdescrip = driver.find_element_by_xpath('//*[@id="comp-k3eka7tb"]/div/svg/g/path').text
        
        fields = driver.find_elements_by_xpath('//*/p')
        inIngredients = False
        
        i=0
        j=0
        for f in fields:
            j+=1
            # print('*'+f.text+'*')
            f = f.text
            
            if inIngredients == True:
               i+=1 
               if i == 1: 
                   if j>len(fields)-2 or 'Last Updated' in f:
                       break
                   else: 
                       chem.append(f)
                       # print(chem)
               elif i == 2: 
                   cas.append(f)
                   # print(cas)
               elif i == 3: 
                   func.append(f)
                   # print(func)
               else: i = 0
               
               if len(func)>0 and len(chem) == len(func) and chem[-1] == '' and cas[-1] == '' and func[-1] == '': 
                   del chem[-1]
                   del cas[-1]
                   del func[-1]
                   inIngredients = False
            if f == 'Designated List': inIngredients = True
                
            
            
        try: #Download pic 
            pic = driver.find_element_by_xpath('//*[@id="img_comp-jctaxwvg"]/img')
            src = pic.get_attribute('src')
            html = urlopen(src) 
            time.sleep(random.randint(minTime,maxTime))
            output = open(ID+'_pic.png','wb')
            output.write(html.read())
            output.close()
            time.sleep(random.randint(minTime,maxTime))
        except: 
            print('picture failed ',url)
        
        try: #Download SDS
            docLink= driver.find_element_by_xpath('//*[@id="comp-jctmjfec"]/a').get_attribute('href')
            filename = str(ID)+'_sds.pdf'
            res = requests.get(docLink)
            res.raise_for_status()
            playFile = open(filename,'wb')
            for chunk in res.iter_content(100000):
                playFile.write(chunk)
            playFile.close()
            time.sleep(random.randint(minTime,maxTime))
            
        except:
            print('SDS failed ',url)
        
        try: #Save copy of page
            # #Make html
            # oldName = ID+'_page.html'
            # file_object = codecs.open((oldName), "w", "utf-8")
            # html = driver.page_source
            # file_object.write(html)
            # time.sleep(random.randint(minTime,maxTime))
            
            
            # newName = ID+'_page.pdf'
            # cmd = os.path.join(execpath,execfile)
            # cmd = " ".join([cmd,'--disable-external-links','--disable-internal-links','--disable-javascript',oldName,newName])
            # os.system(cmd)
            
            
            #Save page
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(random.randint(minTime,maxTime))
            
            # Hide_elements=['class=navbar yamm interior', 'class=container-control-fuschia'] # Use full class name
            ob=Screenshot_Clipping.Screenshot()
            img_url=ob.full_Screenshot(driver, save_path=r'.', image_name=ID+'_page.png')
            
            image1 = Image.open(ID+'_page.png')
            im1 = image1.convert('RGB')
            im1.save(ID+'_page.pdf')
            os.remove(ID+'_page.png')
            
            
        except: 
            print('webpage download failed', url)
        
        if chem == []:
            chem = ['']
            cas = ['']
            func = ['']
         
        if len(func) != len(chem):
            print(url,func,chem)
        
        n = len(chem)
        idList.extend([ID]*n)
        nameList.extend([name]*n)
        colorList.extend([color]*n)
        sizeList.extend([size]*n)
        categoryList.extend([cat]*n)
        descripList.extend([descrip]*n)
        dateList.extend([date]*n)
        upcList.extend([upc]*n)
        urlList.extend([url]*n)
        casList.extend(cas)
        chemList.extend(chem)
        funcList.extend(func)
    except: 
        print('something failed ',url)
        
    
# driver.close()

df = pd.DataFrame({'id':idList, 'product name':nameList, 'color':colorList, 'size':sizeList, 'category':categoryList, 'date':dateList, 'upc':upcList, 'description':descripList, 'url':urlList, 'chemical name':chemList, 'cas':casList, 'functional use':funcList})
df.to_csv('big d page data 4.csv',index=False, header=True)