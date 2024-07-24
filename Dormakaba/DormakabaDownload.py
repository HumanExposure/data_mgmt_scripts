from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import urllib.request
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.dormakabagroup.com/en/sustainability/product-declarations')
time.sleep(2)
product_count = 0

def sanitize_title(title):
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '-']  # List of invalid characters
    for char in invalid_chars:
        title = title.replace(char, '_')  # Replace invalid character with '_'
    invalid_chars2 = ['™', '®']
    for char in invalid_chars2:
        title = title.replace(char, '')
    return title

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
product_count = 0

healthButton = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/section[4]/div/div[2]/button')
driver.execute_script("arguments[0].scrollIntoView();", healthButton)
driver.execute_script("arguments[0].click();", healthButton)
time.sleep(2)

healthLinks = soup.find_all('a')
healthTitles = soup.find_all('td', style='width:30.158%')
healthTitles2 = soup.find_all('td', style='width:186.285px')

links = []

for healthLink in healthLinks:
    if healthLink.parent in healthTitles or healthLink.parent in healthTitles2:
        links.append(healthLink)
for link in links:
    product_count += 1
    name = link.find_previous().find_previous().text
    if not name:
        name = link.find_previous().find_previous().find_previous().text
    name = sanitize_title(name)
    urlDownload = link.get('href')

    healthFile = os.path.join(
        "C:/Users/KHAROHAL/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/WebScrapingPractice/Dormakaba Extraction",
        name + '.pdf')
    urllib.request.urlretrieve(urlDownload, healthFile)

driver.quit()
print(product_count)