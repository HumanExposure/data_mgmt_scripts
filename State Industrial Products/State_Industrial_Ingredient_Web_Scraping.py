import os
import requests
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium
import time
import urllib.request
import img2pdf

directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\Screenshots'
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

products = driver.find_elements(By.TAG_NAME,'li')
for i, product in enumerate(products, start=1):
    try:
        description_div = driver.find_element(By.XPATH, f'//*[@id="ingredientWrapper"]/div[2]/div[2]/ul/li[{i}]/div')
        driver.execute_script("arguments[0].style.display = 'block';", description_div)
        time.sleep(2)  # Wait for the table to load
        product_name_tag = driver.find_element(By.XPATH, f'//*[@id="ingredientWrapper"]/div[2]/div[2]/ul/li[{i}]/h5')
        product_name = sanitize_title(product_name_tag.text.strip())
        table = product.find_element(By.XPATH, f'//*[@id="ingredientWrapper"]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/table')
        # Take screenshot of the table
        png_path = os.path.join(directory, f'{product_name}.png')
        driver.execute_script("arguments[0].scrollIntoView();", table)
        table.screenshot(png_path)
        # Convert PNG to PDF
        pdf_path = os.path.join(directory, f'{product_name}.pdf')
        with open(png_path, "rb") as img_file, open(pdf_path, "wb") as pdf_file:
            pdf_file.write(img2pdf.convert(img_file))
        os.remove(png_path)
    except Exception as e:
        print(f"An error occurred: {e}")

driver.quit()
