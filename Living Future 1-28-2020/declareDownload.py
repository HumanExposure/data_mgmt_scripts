# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:59:41 2020

@author: ALarger
"""

import time, csv, os, string, random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pdfkit
from PIL import Image
from Screenshot import Screenshot_Clipping

path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'L:\Lab\HEM\ALarger\Declare_Living Future' 
os.chdir(path)   
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

#Prod data
fileList = [] #Name of files
idList = [] #Product IDs
nameList = [] #Product names
manufList = [] #Manufacturer
descripList = [] #Product description
urlList = [] #Product page url
picList = [] #Product picture src
componentList = [] #Component the ingredient is in
chemList = [] #Ingredient names
casList = [] #Ingredient CAS numbers
concList = [] #Ingredient concentration 

chrome_options= Options()
#chrome_options.add_argument("--headless") 
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.implicitly_wait(10)
driver.maximize_window()

urls = csv.reader(open('declare urls.csv')) #csv of product urls
i=0
fails = 0
for row in urls:
    i+=1
    if i%100 == 0: print(i)
    if fails > 10 and len(idList) > 0: break #If the script fails on 10 products in a row: break
    url = row[0]   
    
    component = []
    ingredients = []
    CASs = []
    conc = []
    
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        name = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/header/h3').text
        manuf = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/header/h6').text
        descrip = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/div[1]/p').text
        ID = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div/div[2]/div[1]/span').text
        try:
            pic = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[1]/div/div[1]')
            src = pic.get_attribute('src')
            location = pic.location
            size = pic.size
            picName = str(i)+'_pic.png'
            #To get picture of product, get size and location of pic, screenshot page, and crop screenshot
            driver.save_screenshot(picName) 
            x = location['x']
            y = location['y']
            width = location['x']+size['width']
            height = location['y']+size['height']
            im = Image.open(picName)
            im = im.crop((int(x), int(y), int(width), int(height)))
            im.save(picName)
        except:
            src = ''
            print('no pic: ',url)
        
        table = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div/div[3]/div[2]/table/tbody/tr')
        for t in range(1,len(table)+1):
            chemRow = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div/div[3]/div[2]/table/tbody/tr['+str(t)+']/td')
            if len(component) > 0 and chemRow[0].text == '':
                component.append(component[-1])
            else:
                component.append(chemRow[0].text)
            ingredients.append(chemRow[1].text)
            CASs.append(chemRow[2].text)
            conc.append(chemRow[3].text)
        
        #Save page
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(random.randint(minTime,maxTime))
        
        Hide_elements=[] # Use full class name
        ob=Screenshot_Clipping.Screenshot()
        img_url=ob.full_Screenshot(driver, save_path=r'.', elements=Hide_elements, image_name=str(i)+'_page.png')
        
        image1 = Image.open(str(i)+'_page.png')
        im1 = image1.convert('RGB')
        im1.save(str(i)+'_page.pdf')
        os.remove(str(i)+'_page.png')
        fails = 0
        
        
    except: 
        print('problem with page',url)
        fails+=1
        continue

#    try:
#        with open((str(i)+'.html'), 'wb') as f:
#            f.write(driver.page_source.encode('utf-8'))
#        time.sleep(random.randint(minTime,maxTime))
#    except: 
#        print('problem with file',url)
#        fails+=1
#        continue #pdfs that fail to download will be saved manually

    #Comp data
    l = len(ingredients)
    chemList.extend(ingredients)
    casList.extend(CASs)
    idList.extend([ID]*l)
    nameList.extend([name]*l)
    manufList.extend([manuf]*l)
    componentList.extend(component)
    urlList.extend([url]*l)
    picList.extend([src]*l)
    concList.extend(conc)
    descripList.extend([descrip]*l)
    fileList.extend([i]*l)

driver.close()
    
#Comp csv
df = pd.DataFrame({'filename':fileList, 'id':idList, 'name':nameList, 'manufacturer':manufList, 'description':descripList, 'component':componentList, 'chem':chemList, 'cas':casList, 'concentration (%)':concList, 'url':urlList, 'picture url':picList})
df.to_csv('declare data.csv',index=False, header=True)   