The Sprayon_Extract script extracts ingredient data for Sprayon paint and related materials. 
The following actions are performed: Convert pdfs to txt files Clean text files Extract data into Pandas data frame Create csv file for upload to factotum

Sprayon SDS were scraped using the Sprayon_download script  in July 2020 by alarger. The script downloads SDS from each product from the web address, which can be found here: https://www.sprayon.com/products/.

Requirements:  Scripts were run using Spyder in a Python 3.7.6 environment using the packages:
Pandas 
Glob 
xPDF (download at https://www.xpdfreader.com/download.html)
Selenium
