import os
import requests
import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import urllib.request

directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial'

# Used to make the title uploadable to Factotum
def sanitize_title(title):
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']  # List of invalid characters
    for char in invalid_chars:
        title = title.replace(char, '_')  # Replace invalid character with '_'
    invalid_chars2 = ['™', '®']
    for char in invalid_chars2:
        title = title.replace(char, '')
    return title

# Start on the igredients webpage
url = "https://www.stateindustrial.com/support/ingredients"
driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

products = soup.find_all('h5', {'class': 'ingredient-title'})
for product in products:


# Loop through all product pages (45 product pages) 
i = 1
product_counter = 0
while i < 46:
    url = "https://www.stateindustrial.com/products?pagenumber=" + str(i)

    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Find products on the page
    product_blocks = soup.find_all('div', {'class': 'productblock'})

    # Loop through all the products
    for product in product_blocks:
        product_counter += 1

        # Need href title to access product page
        href_title = product.find('a')['href']
        product_url = "https://www.stateindustrial.com" + href_title

        driver.get(product_url)
        time.sleep(2)

        product_html = driver.page_source
        product_soup = BeautifulSoup(product_html, 'html.parser')

        product_name = product_soup.find('div', {'class': 'products__details__title'}).find('h1').text
        product_name = sanitize_title(product_name)
        sds_link = product_soup.find('strong', string='SDS')

        if sds_link:
            sds_url = sds_link.find_next_sibling('p').find('a')['href']
            
            # Download the SDS file
            sds_file = os.path.join(r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files', product_name + '.pdf')
            urllib.request.urlretrieve(sds_url, sds_file)

    i += 1
driver.quit()
# print(product_counter)
