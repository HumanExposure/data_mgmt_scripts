
import time, os, string, random, requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from glob import glob


clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Lincoln Electric/lincoln electric' #Folder docs go into
os.chdir(path)
minTime = 5 #minimum wait time in between clicks
maxTime = 10 #maximum wait time in between clicks

urlList = [] #product page url
nameList = [] #product name
sizeList = [] #product size
processList = [] #process the product is for
areaList = [] #area sds is valid for
languageList = [] #language the sds is in


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)

start = 'https://www.lincolnelectric.com/en/Safety-Document-Search/Safety-Data-Sheets'
driver.get(start)
time.sleep(random.randint(minTime,maxTime))


select = Select(driver.find_element_by_id('SelectedManufacturer'))
select.select_by_visible_text('Lincoln Electric Company') #Name of manufacturer you want to download
time.sleep(random.randint(minTime,maxTime))


#scroll down to region buttons
element = driver.find_element_by_id('js-sdsf-form-1-region-ZLE_SDS_NA') 
coordinates = element.location_once_scrolled_into_view # returns dict of X, Y coordinates
driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
time.sleep(random.randint(minTime,maxTime))
element.click() #search for north america pdfs
time.sleep(random.randint(minTime,maxTime))

for x in range(0,10):
    #type product number
    prodnum = driver.find_element_by_xpath('//*[@id="input-text"]') #Product number box
    prodnum.send_keys(Keys.BACKSPACE)
    prodnum.send_keys(x)
    time.sleep(random.randint(minTime,maxTime))
    
    #click find button
    element = driver.find_element_by_xpath('/html/body/main/div[3]/div[1]/form/button') 
    coordinates = element.location_once_scrolled_into_view # returns dict of X, Y coordinates
    driver.execute_script('window.scrollTo({}, {});'.format(coordinates['x'], coordinates['y']))
    time.sleep(random.randint(minTime,maxTime))
    element.click()
    time.sleep(random.randint(minTime,maxTime))

    #Get data in table rows
    rows = driver.find_elements_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr')
    for i in range(1,len(rows)+1):
        urlList.append(driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr['+str(i)+']/td[1]/p/a').get_attribute('href'))
        nameList.append(driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr['+str(i)+']/td[1]/p/a').text)
        sizeList.append(driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr['+str(i)+']/td[2]/p').text)
        processList.append(driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr['+str(i)+']/td[3]/p').text)
        areaList.append(driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr['+str(i)+']/td[4]/p').text)
        languageList.append(driver.find_element_by_xpath('/html/body/main/div[4]/div[1]/table/tbody/tr['+str(i)+']/td[5]/p').text)


#Make csv
df = pd.DataFrame({'url':urlList, 'name':nameList, 'size':sizeList, 'process':processList, 'area':areaList, 'language':languageList})
df=df.drop_duplicates()
df.to_csv('lincoln electric urls.csv',index=False, header=True, encoding='utf8')