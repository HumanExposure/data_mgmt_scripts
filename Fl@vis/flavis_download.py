#lkoval
#3-12-2020

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import random
import pandas as pd
import os
import string
import requests
import pdfkit
import PyPDF2
from glob import glob
import re


os.chdir("C:\\Users\\lkoval\\Documents\\flavis")

#set up application to convert html to pdf
wkhtmltopdf_path="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
config=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

#set up webdriver
chromedriver="C:\\Users\\lkoval\\Documents\\chromedriver.exe"
chrome_options= Options()
chrome_options.add_argument("--hide-scrollbars")
driver=webdriver.Chrome(chromedriver, options=chrome_options)

min_time=3
max_time=7
time.sleep(random.randint(min_time,max_time))

start_url="http://ec.europa.eu/food/food/chemicalsafety/flavouring/database/"
driver.get(start_url)
driver.maximize_window()

#get number of pages then go each page and save it as a pdf
pages=driver.find_elements_by_xpath("/html/body/div/div[1]/div[1]/div/div/div[2]/table/tbody/tr[2]/td/form/select/option")
for i in range(1,len(pages)+1):
    print("page %d"%i)
    page=driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/div/div[2]/table/tbody/tr[2]/td/form/select/option[%d]"%i).click()
    url=driver.current_url
    pdfkit.from_url(url, "flavis_%d.pdf"%i, configuration=config)
    time.sleep(random.randint(min_time,max_time))

driver.close()


############################## Combine pages into single pdf #########################################################################################

#puts list of files in correct order
def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)


files=glob("*.pdf")
files=natural_sort(files)


#combines all pages into single pdf
pdfWriter=PyPDF2.PdfFileWriter()

for filename in files:
    pdfFileObj=open(filename,"rb")
    pdfReader=PyPDF2.PdfFileReader(pdfFileObj)
    for pageNum in range(pdfReader.numPages):
        pageObj=pdfReader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

pdfOutput=open("flavis.pdf","wb")
pdfWriter.write(pdfOutput)
pdfOutput.close()
