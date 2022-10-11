# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 16:37:50 2022

@author: MHORTON
"""
import random, time, string, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pyautogui
import glob

# %%
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    return(cline)

# %% Define the pauses
def longpause():
    random.seed()
    wait = 4 + 3 * random.random()
    time.sleep(wait)

def shortpause():
    random.seed()
    wait = 2 + 1 * random.random()
    time.sleep(wait)

# %% Log into each data sheet and save the document
def downloadSDS(docName):
    longpause()
    driver.switch_to.window(driver.window_handles[1])

    try:
        name = driver.find_element(By.ID, "ctlMasterPage_txtName")
        if name.get_attribute("value") == '':
            driver.find_element(By.ID, 'ctlMasterPage_txtName').send_keys('M Horton')
            driver.find_element(By.ID, 'ctlMasterPage_txtCompany').send_keys('ORAU')
            driver.find_element(By.ID, 'ctlMasterPage_txtAddress').send_keys('Durham, NC')
            driver.find_element(By.ID, 'ctlMasterPage_txtEmail').send_keys('horton.mary@epa.gov')
            shortpause()
            driver.find_element(By.ID, 'btnOk').click()
            longpause()
            driver.switch_to.window(driver.window_handles[1])
    except:
        shortpause()
    pyautogui.hotkey('ctrl', 's')
    shortpause()
    pyautogui.write(str(docName))
    shortpause()
    pyautogui.press('enter')
    shortpause()
    pyautogui.press('enter')
    shortpause()
    
    driver.close()
    
    # Switch back to first window
    driver.switch_to.window(driver.window_handles[0])

# %% Download Chrome driver and utilize

service = ChromeService(executable_path=ChromeDriverManager().install())
profile = {
    'download.prompt_for_download': False
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', profile)
driver = webdriver.Chrome(options=options, service=service)

# %% Open the list of data sheets and get the links to the documents

driver.get("https://tycosds.thewercs.com/external/private/results.aspx?page=NewSearch&language=d__EN&subformat=d__AGHS&productName_option=d__~value~&productId_option=d__~value~&CUSTOM1=d__-1&CUSTOM2=d__-1")
longpause()

# %%
filePath = 'C:\\Users\\mhorton\\OneDrive - Environmental Protection Agency (EPA)\\Profile\\Documents\\TycoSDS\\pdfs\\'

downloaded = [] # Check for already downloaded pdfs
pdfs = glob.glob(filePath + '*.pdf')
for pdf in pdfs:
    pdf = pdf.split('\\')[-1].rsplit('.pdf')[0]
    downloaded.append(pdf)

# %%
prods = []

nextlink = True

while nextlink == True:
    try:
        # Get list of documents
        elems = driver.find_elements(By.CSS_SELECTOR, "[href*='getDocument']")
        for ele in elems:
            prodDoc = str(ele.text)
            prodDoc = prodDoc.replace('/','-')
            prodDoc = prodDoc.replace('\\','-')
            prodDoc = prodDoc + '.pdf'
            prods.append(prodDoc)
            prodPath = filePath + prodDoc
            
            if str(ele.text) not in downloaded:
                print('Downloading', prodDoc)
                ele.click()
                downloadSDS(prodPath)
            else:
                print(str(prodDoc), 'already downloaded.')
        shortpause()
        try:
            nextlink = driver.find_element(By.LINK_TEXT, 'Next')
        except:
            nextlink = False
        nextlink.click()
    except:
        currentpage = driver.current_url
        print("Error occurred on", currentpage, '\n\nOn element', str(ele.text))
        driver.switch_to.window(driver.window_handles[0])

driver.close()

# %% determine PDFs that will need to be manually downloaded
prods = []

nextlink = True

while nextlink == True:
    try:
        # Get list of documents
        elems = driver.find_elements(By.CSS_SELECTOR, "[href*='getDocument']")
        for ele in elems:
            prodNum = str(ele.text)
            prodNum = prodNum.replace('/','-')
            prodNum = prodNum.replace('\\','-')
            prodDoc = prodNum + '.pdf'
            prods.append(prodDoc)
            prodPath = filePath + prodDoc
            
        shortpause()
        try:
            nextlink = driver.find_element(By.LINK_TEXT, 'Next')
        except:
            nextlink = False
        nextlink.click()
    except:
        currentpage = driver.current_url
        print("Error occurred on", currentpage, '\n\nOn element', str(ele.text))
        driver.switch_to.window(driver.window_handles[0])

driver.close()

