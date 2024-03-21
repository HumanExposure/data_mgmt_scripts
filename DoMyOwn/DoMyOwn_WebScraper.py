import os
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

i = 1
while i < 149:
    url = "https://www.domyown.com/labels?page=" + str(i)

    driver = webdriver.Chrome()

    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('a', title='View this Material Safety Data Sheet')

    for link in links:
        pdf_url = "https://www.domyown.com/" + link.get('href')
        response = requests.get(pdf_url)
        filename = os.path.join(r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\SDS Files', pdf_url.split('/')[-1])

        with open(filename, 'wb') as f:
            f.write(response.content)

    driver.quit()

    i = i + 1
