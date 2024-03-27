import os
import requests
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time

directory = r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn'

def sanitize_title(title):
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']  # List of invalid characters
    for char in invalid_chars:
        title = title.replace(char, '_')  # Replace invalid character with '_'
    return title

# Start the loop
i = 1
while i < 149:
    url = "https://www.domyown.com/labels?page=" + str(i)

    driver = webdriver.Chrome()

    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'class': 'w-full border-collapse labels cell-py-2 cell-px-4'})

    # Loop through each row
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols)>4:
            pdf_link_element = cols[4].find('a')
            if pdf_link_element is not None:    
                manufacturer = cols[1].text.strip()
                product_name = cols[0].text.strip()
                title = f"{manufacturer}_{product_name}"
                title = sanitize_title(title)

                # Download the PDF
                pdf_url = "https://www.domyown.com/" + cols[4].find('a').get('href')
                response = requests.get(pdf_url)
                filename = os.path.join(r'C:\Users\mmetcalf\Documents and Scripts\DoMyOwn\SDS Files Test', title + '.pdf')

                with open(filename, 'wb') as f:
                    f.write(response.content)
                    
                time.sleep(1)

    driver.quit()
    print("Through page " + str(i))

    i = i + 1

