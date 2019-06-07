#lkoval
#4-2-19

#Import necessary libraries
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

#reads in registered records template and makes list of urls and filenames and creates empty list for bad urls
registered_records=pd.read_csv("livingfuture_registered_records.csv")
urls=registered_records["url"]
filename=registered_records["filename"]
url_list=[]
filename_list=[]
bad_urls=[]
for url in urls:
    url_list.append(url)

for fn in filename:
    filename_list.append(fn)


#path to chrome webdriver executable (chromedriver) to automate a browser. Options control browser output. --headless prevents a browser user interface from popping up. It was the only work-around I found to avoid issues with admin priveleges preventing necessary extensions from running. --hide-scrollbars hides scrollbars so they aren't in screenshot
chromedriver="C:\\Users\\lkoval\\Documents\\chromedriver.exe"
chrome_options= Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--hide-scrollbars")


for i in range(0, len(filename_list)):
    #gets the name of the product from the previous filename
    name=filename_list[i].strip(".pdf")

    #opens browser for url and gets the largest possible size for the page then closes browser
    driver=webdriver.Chrome(chromedriver, options=chrome_options)
    driver.get(url_list[i])
    driver.maximize_window()
    time.sleep(2)
    height= driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight)")
    driver.close()

    #if the returned height is larger than the height for a missing page, resize the window with the height to get full webpage then reopen browser and take and save a screenshot.
    if height>992:
        driver=webdriver.Chrome(chromedriver, options=chrome_options)
        driver.set_window_size(1920, height)
        driver.get(url_list[i])
        time.sleep(2)
        img=driver.save_screenshot("%s.png"%name)
        driver.close()
        # print("%d/%d"%(i+1,len(url_list)))

    #else make list of urls that are missing pages
    else:
        bad_urls.append(url_list[i])
        # print("%d/%d %s"%(i+1,len(url_list), url_list[i]))


#save a list of the bad files as csv
bad=pd.DataFrame()
bad["urls"]=bad_urls
bad.to_csv("bad_urls_living_future.csv")
