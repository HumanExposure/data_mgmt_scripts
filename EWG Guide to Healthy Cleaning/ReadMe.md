**ewgCleaningUrls.py** collects all product urls in the EWG Guide to Healthy Cleaning

**ewgCleaningExtract.py** goes to each product page, goes to the "What's on the label" tab, and gathers product info and ingredients, saves a html file of the product page and generates a csv with the data. Because the product category, brand, and company fields are cut off, the urls to the category, brand, and company pages are saved instead

**ewgCleaningGetCats.py** reads the csv created by ewgCleaningExtract.py, goes to each category, brand and company url, gets the full names, and creates a new csv with this data

**ewgCleaningHtmlToPdf.py** converts html files to pdfs so they can be uploaded to Factotum (wkhtmltopdf can be downloaded here: https://wkhtmltopdf.org/downloads.html)

**ewgCleaningData.py** reads the csv created by ewgCleaningGetCats.py, separates the ingredients list into individual ingredients, matches documents with their Factotum document IDs, and creates a csv to upload the data to Factotum
