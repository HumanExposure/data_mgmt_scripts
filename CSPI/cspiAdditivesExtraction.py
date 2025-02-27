import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


path = r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\CSPI' 
os.chdir(path)   
url = 'https://www.cspinet.org/page/chemical-cuisine-food-additive-safety-ratings'
cService = webdriver.ChromeService(executable_path=r'c:\Users\alarger\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe')
chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service = cService,options=chrome_options)
driver.maximize_window()

driver.get(url)
time.sleep(5)

chemList = driver.find_elements('xpath','/html/body/div[1]/main/article/article[4]/div/div[1]/div[2]/div[4]/table/tbody/tr/td[1]/span/span[2]/span/a')
funcList = driver.find_elements('xpath','/html/body/div[1]/main/article/article[4]/div/div[1]/div[2]/div[4]/table/tbody/tr/td[3]/span/span')
for x in range(0,len(chemList)):
    chemList[x] = chemList[x].get_attribute('textContent').strip()
    funcList[x] = funcList[x].get_attribute('textContent').strip()
    if funcList[x]=='Other': funcList[x]=''
    
# driver.close()
        
n = len(chemList)
idList= [1797193]*n
filenameList = ['CSPI Chemical Cuisine Additives.pdf']*n
dateList = ['']*n
categoryList = ['Chemical Cuisine Additive']*n
casList = ['']*n
# chemList = ['']*n
# funcList = ['']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n
componentList = ['']*n
detectedList = ['']*n
authorList = ['']*n
doiList = ['']*n

df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList, 'component':componentList,'chem_detected_flag':detectedList, 'author':authorList, 'doi':doiList})
df.to_csv('cspi chemical cuisine additives.csv',index=False, header=True, encoding = 'utf8')
