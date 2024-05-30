import os
import csv
from selenium import webdriver
from bs4 import BeautifulSoup

directory = r'C:\Users\mmetcalf\Documents and Scripts\State Industrial\Functional CSVs'
lookup_file = r"C:\Users\mmetcalf\Documents and Scripts\State Industrial\Factotum_State_Industrial_Products_Ingredients_List_unextracted_documents_20240530.csv"

product_names = []

with open(lookup_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    lookup_table = {row[1]: row[0] for row in reader}

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

products = soup.find_all('li')
for product in products:
    product_name_tag = product.find('h5', class_='ingredient-title')
    if product_name_tag:
        product_name = sanitize_title(product_name_tag.text.strip())
        product_names.append(product_name)
        ingredients_table = product.find('table')
        if ingredients_table:
            rows = iter(ingredients_table.find_all('tr'))
            next(rows)
            ingredients = []
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 3:
                    ingredient_name = cols[0].text.strip()
                    cas_number = cols[1].text.strip()
                    function = cols[2].text.strip()
                    ingredients.append([ingredient_name, cas_number, function])
            
            # Write to CSV
            csv_path = os.path.join(directory, f'{product_name}.csv')
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['data_document_id', 'data_document_filename','prod_name','raw_chem_name','raw_cas', 'report_funcuse', 'doc_date', 'rev_num'])
                for ingredient in ingredients:
                    data_document_id = lookup_table.get(f'{product_name}.pdf', '')
                    writer.writerow([data_document_id, product_name+'.pdf', product_name] + ingredient + ['', ''])
driver.quit()
