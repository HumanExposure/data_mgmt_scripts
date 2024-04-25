import time, os, string, random, requests, csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from glob import glob
from Screenshot import Screenshot_Clipping
from PIL import Image



clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #Removes non-ASCII characters
path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/FracFocus' #Folder docs go into
os.chdir(path)
minTime = 2 #minimum wait time in between clicks
maxTime = 5 #maximum wait time in between clicks

urlList = []
wellnumList = []
jobnumList = []
nameList = []
operatedbyList = []
apiList = []
stateList = []
countyList = []
indianList = []
federalList = []
completedList = []
watervolList = []
nonwatervolList = []
depthList = []
chemList = []
casList = []
percentList = []


chrome_options= Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\alarger\Documents\chromedriver.exe", options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(5)

i=0
pdfs = glob('*.pdf')
urls = csv.reader(open('fracfocus wells urls 2.csv')) #csv of product urls
for row in urls: 
    i+=1
    # if i>10: break
    url = row[0]
    if url == 'url': continue
    wellnum = url.split('/')[-1]
    # if wellnum+'.pdf' in pdfs: continue
    try:
        driver.get(url)
        time.sleep(random.randint(minTime,maxTime))
        
        #well data
        name = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/p[1]').text.strip()
        operatedby = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/p[2]').text.strip()
        api = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/p[3]').text.strip()
        state = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/table/tbody/tr[2]/td[1]').text.strip()
        county = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/table/tbody/tr[2]/td[2]').text.strip()
        indian = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/table/tbody/tr[2]/td[3]').text.strip()
        federal = driver.find_element_by_xpath('//*[@id="disclosure_content"]/div[1]/table/tbody/tr[2]/td[4]').text.strip()
        
        #job data
        jobnum = 0
        jobdata = driver.find_elements_by_class_name('job')
        k=0
        completed = ''
        watervol = ''
        nonwatervol = ''
        depth = ''
        for j in jobdata:     
            k+=1
            if k==1:completed = j.text.strip()
            elif k==2: watervol = j.text.strip()
            elif k==3: nonwatervol = j.text.strip()
            elif k==4:
                depth = j.text.strip()
                jobnum+=1
                k=0
        
        # completed = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/p[1]').text.strip()
        # watervol = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/p[2]').text.strip()
        # nonwatervol = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/p[3]').text.strip()
        # depth = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/p[4]').text.strip()
        
        # chem = []
        # cas = []
        # percent = []
        # rows = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div[2]/table/tbody/tr')
        # for r in range(1,len(rows)+1):
        #     chem.append(driver.find_element_by_xpath('//*[@id="ingredienttable"]/tbody/tr['+str(r)+']/td[1]').text.strip())
        #     cas.append(driver.find_element_by_xpath('//*[@id="ingredienttable"]/tbody/tr['+str(r)+']/td[2]').text.strip())
        #     percent.append(driver.find_element_by_xpath('//*[@id="ingredienttable"]/tbody/tr['+str(r)+']/td[3]').text.strip())
        
                chems = []
                cass = []
                percents = []
                chem = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div[2]/table['+str(jobnum)+']/tbody/tr/td[1]')
                for x in chem: chems.append(x.text.strip())
                cas = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div[2]/table['+str(jobnum)+']/tbody/tr/td[2]')
                for x in cas: cass.append(x.text.strip())
                percent = driver.find_elements_by_xpath('/html/body/div/div/div/div/div/div[2]/table['+str(jobnum)+']/tbody/tr/td[3]')
                for x in percent: percents.append(x.text.strip())
            
                
                n=len(chems)
                if n == 0:
                    n=1
                    chems=['']
                    cass=['']
                    percents=['']
                chemList.extend(chems)
                casList.extend(cass)
                percentList.extend(percents)
                urlList.extend([url]*n)
                wellnumList.extend([wellnum]*n)
                jobnumList.extend([jobnum]*n)
                nameList.extend([name]*n)
                operatedbyList.extend([operatedby]*n)
                apiList.extend([api]*n)
                stateList.extend([state]*n)
                countyList.extend([county]*n)
                indianList.extend([indian]*n)
                federalList.extend([federal]*n)
                completedList.extend([completed]*n)
                watervolList.extend([watervol]*n)
                nonwatervolList.extend([nonwatervol]*n)
                depthList.extend([depth]*n)
            
                
                
                #save copy of page
                n=wellnum+'_'+str(jobnum)
                time.sleep(random.randint(minTime,maxTime))        
                driver.execute_script("window.scrollTo(0, 0)")
                time.sleep(random.randint(minTime,maxTime))
                ob=Screenshot_Clipping.Screenshot()
                img_url=ob.full_Screenshot(driver, save_path=r'.', image_name=n+'_page.png')
                image1 = Image.open(n+'_page.png')
                im1 = image1.convert('RGB')
                im1.save(n+'_page.pdf')
                os.remove(n+'_page.png')
    except: pass
    
#Make csv
df = pd.DataFrame({'url':urlList, 'well number':wellnumList, 'job number':jobnumList, 'well name':nameList, 'operated by':operatedbyList, 'api':apiList, 'state':stateList, 'county':countyList, 'indian well?':indianList, 'federal well?':federalList, 'job completed':completedList, 'total base water volume':watervolList, 'total base non-water volume':nonwatervolList, 'true vertical depth':depthList, 'ingredient':chemList, 'cas number':casList, '% hf fluid':percentList})
df.to_csv('fracfocus web data.csv',index=False, header=True, encoding='utf8')
