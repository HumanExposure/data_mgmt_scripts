import time, os, string, random, pdfkit, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Scraping\Sprayon' #Folder docs go into
os.chdir(path)
path_wkthmltopdf = r'C:\Users\alarger\Documents\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
minTime = 3 #minimum wait time in between clicks
maxTime = 7 #maximum wait time in between clicks

prodList = [] #Product numbers
urlList = [] #Product page urls
nameList = [] #Product names
descripList = [] #Description
picList = [] #List of picture urls
sizeList = [] #Product size
typeList = [] #Product type

chrome_options= Options()
#chrome_options.add_argument("--headless")
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], "download.default_directory": path, "download.extensions_to_open": "applications/pdf"}
chrome_options.add_experimental_option("prefs", profile)
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)

start = 'https://www.sprayon.com/products/'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))
try:
    driver.find_element_by_xpath('//*[@id="ensAllow"]/div').click() #accept privacy settings so the box goes away
except:
    pass

urls = []
while True: #Get product urls
    time.sleep(random.randint(minTime,maxTime))
    products = driver.find_elements_by_xpath('//*[@id="shop-main"]/ul/li/a[2]')
    for p in products:
        urls.append(p.get_attribute('href'))
    try:
        driver.find_element_by_class_name('next.page-numbers').click() #Click next page
    except:
        break

for u in urls: #Go to each product page
    time.sleep(random.randint(minTime,maxTime))
    driver.get(u)
    try:
        #Get product data
        name = clean(driver.find_element_by_class_name('product_title.entry-title').text)
        descrip = clean(driver.find_element_by_class_name('woocommerce-product-details__short-description').text)
        prodnum = []
        size = []
        prodtype = []
        sdsloc = ''
        cpicloc = ''
        header = driver.find_elements_by_xpath('//*[@id="content-section"]/div/form/div[2]/table/thead/tr/th')
        for n in range(1,len(header)+1): #Get locations of the cpic and sds columns in the product table
            if header[n-1].text == 'SDS':
                sdsloc = n
            if header[n-1].text == 'CPIC':
                cpicloc = n
        numProds = len(driver.find_elements_by_xpath('//*[@id="content-section"]/div/form/div[2]/table/tbody/tr'))
        for n in range(1,numProds+1): #Get data and docs from each row on the product table
            elements = driver.find_elements_by_xpath('//*[@id="content-section"]/div/form/div[2]/table/tbody/tr['+str(n)+']/td')
            prodnum.append(elements[0].text)
            size.append(elements[1].text)
            prodtype.append(clean(elements[2].text))
            gotDocs = False
            if sdsloc != '':
                try: #Download sds
                    docLink = driver.find_element_by_xpath('//*[@id="content-section"]/div/form/div[2]/table/tbody/tr['+str(n)+']/td['+str(sdsloc)+']/a').get_attribute('href')
                    filename = (prodnum[-1]+'_sds.pdf')
                    res = requests.get(docLink)
                    res.raise_for_status()
                    playFile = open(filename,'wb')
                    for chunk in res.iter_content(100000):
                        playFile.write(chunk)
                    playFile.close()
                    gotDocs = True
                    time.sleep(random.randint(minTime,maxTime))
                except: pass
            if cpicloc != '':
                try: #Download cpic
                    docLink = driver.find_element_by_xpath('//*[@id="content-section"]/div/form/div[2]/table/tbody/tr['+str(n)+']/td['+str(cpicloc)+']/a').get_attribute('href')
                    filename = (prodnum[-1]+'_cpic.pdf')
                    res = requests.get(docLink)
                    res.raise_for_status()
                    playFile = open(filename,'wb')
                    for chunk in res.iter_content(100000):
                        playFile.write(chunk)
                    playFile.close()
                    gotDocs = True
                    time.sleep(random.randint(minTime,maxTime))
                except: pass
            if gotDocs == True:
                try: #Download pic for each product
                    pic = driver.find_element_by_xpath('//*[@id="image-section"]/div/figure/div/a/img')
                    src = pic.get_attribute('src')
                    html = urlopen(src) 
                    picname = prodnum[-1]+'_pic.png'
                    time.sleep(random.randint(minTime,maxTime))
                    output = open(picname,'wb')
                    output.write(html.read())
                    output.close()
                except: pass
    except: 
        print('problem with page',u)
        continue
            
    #Add data to lists
    n = len(prodnum)
    prodList.extend(prodnum)
    urlList.extend(n*[u])
    nameList.extend(n*[name])
    descripList.extend(n*[descrip])
    picList.extend(n*[src])
    sizeList.extend(size)
    typeList.extend(prodtype)

driver.close()

#Make csv
df = pd.DataFrame({'Product number':prodList, 'Product Name':nameList, 'Size':sizeList, 'Description':descripList, 'Product Type':typeList, 'url':urlList, 'Picture url':picList})
df.to_csv('sprayon scraped data.csv',index=False, header=True)
