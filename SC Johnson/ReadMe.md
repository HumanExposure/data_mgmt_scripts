### scjUrls.py 
Uses Selenium to navigate the website (https://www.whatsinsidescjohnson.com/us/en/brands) to gather product page urls, and creates a csv of urls (Python 3.7)


### scjDownloadPages.py 
Uses Selenium and the csv generated in scjUrls to navigate to each product page, extract product and ingredient data, and save a copy of the product page, ingredient disclosure, and product image (Python 3.7)


### scjExtractID.py
Uses Xpdf to convert the ingredient disclosure pdfs downloaded in scjDownloadPages.py to text files, extracts the product name, formula number and ingredient information, and saves the data to a csv. Download Xpdf here: https://www.xpdfreader.com/download.html
