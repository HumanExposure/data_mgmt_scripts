import time, os, string, random, requests, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob
# import urllib
import pdfkit
import codecs
from PIL import Image
from Screenshot import Screenshot_Clipping




path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/dollar general' #Folder docs go into
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks

path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = { 'quiet': ''}

chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:/Users/alarger/Documents/chromedriver-win32\chromedriver.exe", options=chrome_options)
driver.maximize_window()
# driver.implicitly_wait(5)

#Product data fields
idList = []
urlList = []
sdsUrlList = []
nameList = []
revList = []
codeList = []
synonymsList = []
manufList = []
statusList = []
upcList = []
skuList = []

#chemical data fields
idList2 = []
rankList = []
casList = []
percentList = []
chemList = []

fails=0
pdfs = glob('*.pdf')
nameList = []
urls = csv.reader(open('dollar general urls.csv', encoding="utf8")) #csv of product urls
i=-1
for row in urls: 
    i+=1
    if i == 0: continue
    if row[0]+'_page.pdf' in pdfs: continue #skip pages that have already been downloaded
    url = row[2]
    idnum = row[0]
    
    
    try: #get data from pages
        driver.get(url)
        
        #get product info
        name = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div/div/h2').text
        rev=''
        code=''
        synonyms=''
        manuf=''
        status=''
        upc=''
        sku=''
        prodrows = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr')
        for j in range(1,len(prodrows)+1):
            col1 = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr['+str(j)+']/th').text.strip()
            col2 = driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr['+str(j)+']/td').text.strip()
            if col1 == 'Revision:': rev = col2
            elif col1 == 'Product Code:': code = col2
            elif col1 == 'Synonyms:': synonyms = col2
            elif col1 == 'Manufacturer:': manuf = col2
            elif col1 == 'Status:': status = col2
            elif col1 == 'UPC:': upc = col2
            elif col1 == 'SKU:': sku = col2

        #get ingredients
        rank = []
        cas = []
        percent = []
        chem = []
        chemrows = driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[4]/div[2]/table/tbody/tr')
        for k in range(1,len(chemrows)+1):
            rank.append(driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[4]/div[2]/table/tbody/tr['+str(k)+']/td[1]').text)
            cas.append(driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[4]/div[2]/table/tbody/tr['+str(k)+']/td[2]').text)
            percent.append(driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[4]/div[2]/table/tbody/tr['+str(k)+']/td[3]').text)
            chem.append(driver.find_element_by_xpath('//*[@id="content"]/div/div/div[2]/div[1]/div[4]/div[2]/table/tbody/tr['+str(k)+']/td[4]').text)
            
        if len(rank)==0:
            rank.append('')
            cas.append('')
            percent.append('')
            chem.append('')
            
      
            
    except:
        print('page data failed',url)
        fails+=1
        if fails>=5: break
        continue
    
    fails = 0
     
    try: #Download sds
        filename = idnum+'_sds.pdf' 
        docurl = driver.find_element_by_xpath('//*[@id="content"]/div/div/a[1]').get_attribute('href')
        res = requests.get(docurl)
        res.raise_for_status()
        playFile = open(filename,'wb')
        for chunk in res.iter_content(100000):
            playFile.write(chunk)
        playFile.close()
        time.sleep(random.randint(minTime,maxTime))
    
    except: 
        print('sds failed!',url)
        pass
    
    try:    
        # pdfkit.from_url('url',idnum+'_page.pdf',options=options, configuration=config)
        
        # file_object = codecs.open((idnum + '_page.html'), "w", "utf-8")
        # html = driver.page_source
        # file_object.write(html)
        
        
        # ele=driver.find_element_by_xpath('/html/body/main')
        # total_height = ele.size["height"]+1000
        # driver.set_window_size(1920, total_height)
        # time.sleep(random.randint(minTime,maxTime))
        # driver.save_screenshot(idnum+'.png')
        # imageList.append(Image.open(idnum+'.png').convert('RGB'))
        # time.sleep(random.randint(minTime,maxTime))
        
        driver.execute_script("window.scrollTo(0, 0)")
        time.sleep(random.randint(minTime,maxTime))
        
        Hide_elements=[] # Use full class name
        ob=Screenshot_Clipping.Screenshot()
        img_url=ob.full_Screenshot(driver, save_path=r'.', elements=Hide_elements, image_name=idnum+'_page.png')
        
        image1 = Image.open(idnum+'_page.png')
        im1 = image1.convert('RGB')
        im1.save(idnum+'_page.pdf')
        os.remove(idnum+'_page.png')
        
    except: 
        print('page download failed',url)
        pass
        
    #Product data fields
    idList.append(idnum)
    urlList.append(url)
    sdsUrlList.append(docurl)
    nameList.append(name)
    revList.append(rev)
    codeList.append(code)
    synonymsList.append(synonyms)
    manufList.append(manuf)
    statusList.append(status)
    upcList.append(upc)
    skuList.append(sku)
    
    #chemical data fields
    idList2.extend(len(chem)*[idnum])
    rankList.extend(rank)
    casList.extend(cas)
    percentList.extend(percent)
    chemList.extend(chem)
    
#Make csvs
l=0
while os.path.exists('dollar general prod data_'+str(l)+'.csv'):
    l+=1
df = pd.DataFrame({'dg id':idList, 'page url':urlList, 'sds url':sdsUrlList, 'product name':nameList, 'revision date':revList, 'product code':codeList, 'synonyms':synonymsList, 'manufacturer':manufList, 'status':statusList, 'upc': upcList, 'sku':skuList})
df.to_csv('dollar general prod data_'+str(l)+'.csv',index=False, header=True)
    

df = pd.DataFrame({'dg id':idList2, 'rank':rankList, 'cas':casList, 'percent':percentList, 'chem name':chemList})
df.to_csv('dollar general chem data_'+str(l)+'.csv',index=False, header=True)
        