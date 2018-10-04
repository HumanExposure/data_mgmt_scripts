#!/usr/bin/env python

import pandas as pd
from bs4 import BeautifulSoup

soup = "dish_soap_dishwashing_detergent_ingredients_palmolive.html"
soup = open(soup,encoding='utf-8')
soup = BeautifulSoup(soup,'lxml')

# table = soup.find_all("table")[0]

# products = [x.get_text() for x in soup.findAll("h3")]

## The following will find all the div's that are the containers for the product name
## header (h3), and the table containing the ingrediets for that product
prods = soup.findAll("div",{"class":"purpose-container"})

data = {'ingredient_inci_name': [],
        'purpose': [],
        'product_name': [],
        "ingredient_list_rank": []}
for prod in prods:
    product_name = prod.findAll("h3")[0].get_text()
    table = prod.findAll("table")[0]

    i = 0
    for row in table.findAll("tbody")[0].findAll("tr"):
        i += 1
        data['ingredient_inci_name'].append(row.findAll("td")[0].get_text())
        data['purpose'].append(row.findAll("td")[1].get_text())
        data['product_name'].append(product_name)
        data['ingredient_list_rank'].append(i)


data = pd.DataFrame(data)


xl = pd.ExcelWriter("../../palmolive_ingredients.xlsx",engine="xlsxwriter")
data.to_excel(xl,index=False)
xl.save()
