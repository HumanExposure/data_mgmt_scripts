from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd
import os
import string
import requests
import pdfkit

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

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))

chromedriver="C:\\Users\\lkoval\\Documents\\chromedriver.exe"
chrome_options= Options()
chrome_options.add_argument("--hide-scrollbars")
driver=webdriver.Chrome(chromedriver, options=chrome_options)

start_url="https://churchdwight.com/ingredient-disclosure/default.aspx"
driver.get(start_url)
driver.maximize_window()

min_time=3
max_time=7
time.sleep(random.randint(min_time,max_time))

sections=driver.find_elements_by_xpath('//*[@class="row"]/ul')
for i in range(1, len(sections)):
    # if i==6:
    #     break
    print("section %d"%i)
    links=driver.find_elements_by_xpath('//*[@class="row"]/ul[%d]/li'%i)
    for j in range(1, len(links)+1):
        try:
            print("%d/%d"%(j,len(links)))
            time.sleep(random.randint(min_time,max_time))
            url=driver.find_element_by_xpath('//*[@class="row"]/ul[%d]/li[%d]/a'%(i,j)).get_attribute("href")
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
            if len(tables)==3:
                table=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr')
                try:
                    sds_link=driver.find_element_by_xpath('/html/body/main/div/article/div[2]/div/p[1]/b/span/a').get_attribute("href")
                    date=driver.find_element_by_xpath('//*[@class="WordSection1"]/p[2]/span').text
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



            elif len(tables)==4:
                ing_table=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table[3]/tbody/tr')
                frag_table=driver.find_elements_by_xpath('//*[@class="WordSection1"]/table[4]/tbody/tr')
                date=driver.find_element_by_xpath('//*[@class="WordSection1"]/p[2]/span').text

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

                sds_link=driver.find_element_by_xpath('/html/body/main/div/article/div[2]/div/p[1]/b/span/a').get_attribute("href")
                filename=product.replace(" ","_").strip()+"_sds.pdf"
                res=requests.get(sds_link)
                res.raise_for_status()
                playFile=open("C:\\Users\\lkoval\\Documents\\church&dwight_sds\\%s"%filename,"wb")
                for chunk in res.iter_content(100000):
                    playFile.write(chunk)
                playFile.close()

            driver.get(start_url)
            time.sleep(random.randint(min_time,max_time))
        except:
            bad.append(url)
            driver.get(start_url)
            time.sleep(random.randint(min_time,max_time))

        # if j==1:
        #     break

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
