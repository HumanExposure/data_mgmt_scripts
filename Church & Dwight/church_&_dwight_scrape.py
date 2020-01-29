#lkoval
#1-29-2020

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd
import os
import string
import requests
import pdfkit

os.chdir("C:\\Users\\lkoval\\Documents\\church&dwight")

#set up application to convert html to pdf
wkhtmltopdf_path="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
config=pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

raw_chem_name=[]
raw_cas=[]
report_funcuse=[]
prod_name=[]
raw_category=[]
material_number=[]
url_list=[]
sds_list=[]
rank_list=[]
filename_list=[]
date_list=[]
bad=[]

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))#function to remove non-printable characters

#establish webdriver
chromedriver="C:\\Users\\lkoval\\Documents\\chromedriver.exe"
chrome_options= Options()
chrome_options.add_argument("--hide-scrollbars")
driver=webdriver.Chrome(chromedriver, options=chrome_options)

#Go to start page
start_url="https://churchdwight.com/ingredient-disclosure/default.aspx"
driver.get(start_url)
driver.maximize_window()

min_time=3
max_time=7
time.sleep(random.randint(min_time,max_time))

sections=driver.find_elements_by_xpath('//*[@class="row"]/ul')

#loop over each of the different categories on start page
for i in range(1, len(sections)):
    print("section %d"%i)
    links=driver.find_elements_by_xpath('//*[@class="row"]/ul[%d]/li'%i)


    #loop over each listed product in each category
    for j in range(1, len(links)+1):

        #try navigating to the product page and get the product name, the category, and the material number. Save the page as a pdf.
        try:
            print("%d/%d"%(j,len(links)))
            time.sleep(random.randint(min_time,max_time))
            url=driver.find_element_by_xpath('//*[@class="row"]/ul[%d]/li[%d]/a'%(i,j)).get_attribute("href")#url to product page
            driver.get(url)
            time.sleep(random.randint(min_time,max_time))
            product=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/span[2]').text)
            cat=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/span[4]').text)
            mat_num=driver.find_element_by_xpath('//*[@class="WordSection1"]/span[6]').text
            print(product)
            pdf_file_name="C:\\Users\\lkoval\\Documents\\church&dwight_pdfs\\"+product.replace(" ","_").strip()+".pdf"
            pdfkit.from_url(url,pdf_file_name, configuration=config)
            tables=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table')
            rank=1

            #if there is only one table of ingredients on the product page
            if len(tables)==3:
                table=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr')

                #if the page has an sds to download, get the chemical names, the cas numbers, the function, the rank, then save the sds
                try:
                    sds_link=driver.find_element_by_xpath('/html/body/main/div/article/div[2]/div/p[1]/b/span/a').get_attribute("href")
                    date=driver.find_element_by_xpath('//*[@class="WordSection1"]/p[2]/span').text#date on product page
                    for k in range(2, len(table)+1):
                        chem=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[1]'%k).text)
                        cas=driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[2]'%k).text
                        use=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[3]'%k).text)
                        prod_name.append(product)
                        raw_category.append(cat)
                        material_number.append(mat_num)
                        url_list.append(url)
                        raw_chem_name.append(chem)
                        raw_cas.append(cas)
                        report_funcuse.append(use)
                        rank_list.append(rank)
                        filename_list.append(product.replace(" ","_").strip()+".pdf")
                        date_list.append(date)
                        rank+=1
                    filename=product.replace(" ","_").strip()+"_sds.pdf"
                    res=requests.get(sds_link)
                    res.raise_for_status()
                    playFile=open("C:\\Users\\lkoval\\Documents\\church&dwight_sds\\%s"%filename,"wb")
                    for chunk in res.iter_content(100000):
                        playFile.write(chunk)
                    playFile.close()

                #if the page does not have an sds to download, get the chemical names, the function, and the rank. Assign the cas as an empty string and assign the date as "2020"
                except:
                    for k in range(2, len(table)+1):
                        chem=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[1]'%k).text)
                        use=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[2]'%k).text)
                        prod_name.append(product)
                        raw_category.append(cat)
                        material_number.append(mat_num)
                        url_list.append(url)
                        raw_chem_name.append(chem)
                        raw_cas.append("")
                        report_funcuse.append(use)
                        rank_list.append(rank)
                        filename_list.append(product.replace(" ","_").strip()+".pdf")
                        date_list.append("2020")
                        rank+=1


            #if there are two tables of ingredients on the product page
            elif len(tables)==4:
                ing_table=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr')#table of regular ingredients
                frag_table=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table[4]/tbody/tr')#table of fragrances
                date=driver.find_element_by_xpath('//*[@class="WordSection1"]/p[2]/span').text#assigned date on product page

                #get chemical names, cas numbers, function, and rank from ingredient table
                for l in range(2, len(ing_table)+1):
                    chem=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[1]'%l).text)
                    cas=driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[2]'%l).text
                    use=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr[%i]/td[3]'%l).text)
                    prod_name.append(product)
                    raw_category.append(cat)
                    material_number.append(mat_num)
                    url_list.append(url)
                    raw_chem_name.append(chem)
                    raw_cas.append(cas)
                    report_funcuse.append(use)
                    rank_list.append(rank)
                    date_list.append(date)
                    filename_list.append(product.replace(" ","_").strip()+".pdf")
                    rank+=1

                #get chemical names and cas numbers from fragrance table. Assign the function as "fragrance" and do not add a rank
                for m in range(2, len(frag_table)+1):
                    chem=clean(driver.find_element_by_xpath('//*[@class="WordSection1"]/table[4]/tbody/tr[%i]/td[1]'%m).text)
                    cas=driver.find_element_by_xpath('//*[@class="WordSection1"]/table[4]/tbody/tr[%i]/td[2]'%m).text
                    prod_name.append(product)
                    raw_category.append(cat)
                    material_number.append(mat_num)
                    url_list.append(url)
                    raw_chem_name.append(chem)
                    raw_cas.append(cas)
                    report_funcuse.append("fragrance")
                    rank_list.append("")
                    date_list.append(date)
                    filename_list.append(product.replace(" ","_").strip()+".pdf")

                #save the sds
                sds_link=driver.find_element_by_xpath('/html/body/main/div/article/div[2]/div/p[1]/b/span/a').get_attribute("href")
                filename=product.replace(" ","_").strip()+"_sds.pdf"
                res=requests.get(sds_link)
                res.raise_for_status()
                playFile=open("C:\\Users\\lkoval\\Documents\\church&dwight_sds\\%s"%filename,"wb")
                for chunk in res.iter_content(100000):
                    playFile.write(chunk)
                playFile.close()

            #return to the start_url
            driver.get(start_url)
            time.sleep(random.randint(min_time,max_time))

        #If an error occurs at any time while navigating the product pages, skip it and save the url
        except:
            bad.append(url)
            driver.get(start_url)
            time.sleep(random.randint(min_time,max_time))

driver.close()

df=pd.DataFrame()
df["data_document_filename"]=filename_list
df["prod_name"]=prod_name
df["doc_date"]=date_list
df["rev_num"]=""
df["raw_category"]=raw_category
df["raw_cas"]=raw_cas
df["raw_chem_name"]=raw_chem_name
df["report_funcuse"]=report_funcuse
df["raw_min_comp"]=""
df["raw_max_comp"]=""
df["unit_type"]=""
df["ingredient_rank"]=rank_list
df["raw_central_comp"]=""
df["component"]=""
df["mat"]=material_number
df["url"]=url_list

df.to_csv("C:\\Users\\lkoval\\Documents\\church&dwight\\church&dwight_ing_disc.csv", index=False)


bad_urls=pd.DataFrame()
bad_urls["url"]=bad
bad_urls.to_csv("C:\\Users\\lkoval\\Documents\\church&dwight\\church&dwight_bad_urls.csv", index=False)
