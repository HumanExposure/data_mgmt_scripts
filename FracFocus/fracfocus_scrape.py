#lkoval
#3-12-2020

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd
import os
import string
import requests
import re

os.chdir("C:\\Users\\lkoval\\Documents")

chem_names=[]
cas=[]
use=[]

chromedriver="C:\\Users\\lkoval\\Documents\\chromedriver.exe"
chrome_options= Options()
chrome_options.add_argument("--hide-scrollbars")
driver=webdriver.Chrome(chromedriver, options=chrome_options)

start_url="https://fracfocus.org/chemical-use/what-chemicals-are-used"
driver.get(start_url)
driver.maximize_window()

min_time=3
max_time=7
time.sleep(random.randint(min_time,max_time))

#get get name, cas, and use for each chemical
chems=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[1]/article/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr")
for i in range(2,len(chems)+1):
    time.sleep(random.randint(min_time,max_time))
    name=driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/article/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr[%d]/td[1]"%i).text
    c=driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/article/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr[%d]/td[2]"%i).text
    u=driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/article/div/div[2]/div/div/div/div/div/div/div/table/tbody/tr[%d]/td[4]"%i).text
    chem_names.append(name)
    cas.append(c)
    use.append(u)

driver.close()

#make dataframe of name, cas, and use
data=pd.DataFrame()
data["raw_chem_name"]=chem_names
data["raw_cas"]=cas
data["report_funcuse"]=use
data=data.loc[data.raw_chem_name.str.contains("[a-zA-Z]")]

#get list of unique chem names
unique_chems=list(set(data.raw_chem_name))

#for each unique chem name/cas pair, if there are multiple uses join the uses into one entry then keep only one instance of the chem name/ cas pair
for chem in unique_chems:
    temp=data.loc[data.raw_chem_name==chem]
    if len(temp)>1:
        if temp.raw_cas.nunique()==1 and temp.report_funcuse.nunique()>1:
            combined_use="; ".join(list(set(temp.report_funcuse)))
            data.loc[data.raw_chem_name==chem, ["report_funcuse"]]=combined_use

data=data.drop_duplicates()

#fill out template
data["data_document_id"]="1512354"
data["data_document_filename"]="fracfocus.pdf"
data["doc_date"]="2020"
data["raw_category"]=""
data["cat_code"]=""
data["description_cpcat"]=""
data["cpcat_code"]=""
data["cpcat_sourcetype"]=""

data=data[["data_document_id","data_document_filename","doc_date","raw_category","raw_cas","raw_chem_name","cat_code","description_cpcat","cpcat_code","cpcat_sourcetype","report_funcuse"]]

data.to_csv("fracfocus.csv", index=False)
