# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 13:16:05 2019

@author: ALarger
"""

import os, time, csv
import pandas as pd
from selenium import webdriver

casList = []
chemList = []
funcList = []
filenameList = []
idList = []

path = r'L:\Lab\HEM\ALarger\Actor Automated Extraction\European Chemicals Agency\Mapping exercise - Plastic additives initiative' 
os.chdir(path)   
url = 'https://echa.europa.eu/mapping-exercise-plastic-additives-initiative#table'
driver = webdriver.Chrome(r'C:\Users\alarger\Documents\chromedriver.exe')
driver.get(url)

i = 0
while i < 10:
    i += 1
    time.sleep(3)
    driver.find_element_by_xpath(('//*[@id="p_p_id_56_INSTANCE_fmg6XG0r0fBW_"]/div/div/div[1]/ul/li[' + str(i) + ']/a')).click()
    cat = driver.find_element_by_xpath(('//*[@id="p_p_id_56_INSTANCE_fmg6XG0r0fBW_"]/div/div/div[1]/ul/li[' + str(i) + ']/a')).text.replace('\n',' ').strip()
    tr_elements = driver.find_elements_by_xpath('//*/table/tbody/tr')
    for T in tr_elements:
        td = T.find_elements_by_xpath('.//td')
        if len(td) == 6 and td[2].text.strip() != '':
            casList.append(td[1].text.replace('\n',' ').strip())
            chemList.append(td[2].text.replace('\n',' ').strip())
            funcList.append((cat + '; ' + td[3].text.replace('\n',' ').replace('n.a.','').strip()).replace('Other functions','').strip('; '))
            filenameList.append(cat + '.pdf')
            
driver.close()
            
for f in filenameList:
    template = csv.reader(open('mapping_exercise__plastic_additives_initiative_documents_20190725.csv'))
    idList.append('')
    for row in template:
        if row[3] == f:
            idList[-1] = row[0]
            break
        
n = len(filenameList)
dateList = ['']*n
categoryList = ['']*n
catcodeList = ['']*n
descripList = ['']*n
cpcatcodeList = ['']*n
typeList = ['']*n

df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'doc_date':dateList, 'raw_category':categoryList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':funcList, 'cat_code':catcodeList, 'description_cpcat': descripList, 'cpcat_code':cpcatcodeList, 'cpcat_sourcetype':typeList})
df.to_csv('Plastic Additives.csv',index=False, header=True)