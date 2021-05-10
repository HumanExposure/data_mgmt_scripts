**CPID_get_urls.py** uses Python 3.8 and Selenium to navigate the [Consumer Product Information Database website](https://www.whatsinproducts.com/) and generate a csv with the product page urls. 

**CPID_product_data.py** uses Python 3.8 and Selenium to go to each webpage saved in the csv created with CPID_get_urls.py, download the product image, and save product data to a csv including a link to the original SDS or MSDS pdf.

**CPID_download_docs.py** uses Python 3.8 and Selenium to go to the document pages saved in the csv created with CPID_product_data.py and download a copy of the pdfs

[Download ChromeDriver here](https://chromedriver.chromium.org/downloads) to use with Selenium. The version of ChromeDriver you download should match the version you use in your regular Chrome browser.
