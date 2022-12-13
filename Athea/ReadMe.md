**atheaUrls.py** uses Selenium to navigate to the Athea "view all products" page, collects all of the product page urls, and creates a csv with the list of urls. 

**atheaDownload.py** uses Selenium to go to each product page url and downloads the SDS and ingredient disclosure, if they exist for that product.

