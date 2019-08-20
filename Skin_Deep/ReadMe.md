Skin Deep urls.py finds product page urls and generates a csv

Skin Deep Extract.py reads the csv of product page urls, goes to each page and gathers product and ingredient information, saves the web page as an html file, and generates a csv with all of the data collected for that product

Skin Deep html to pdf wkhtmltopdf.py converts each html file into a pdf using wkhtmltopdf (can be downloaded here: https://wkhtmltopdf.org/downloads.html)

Skin Deep Data.py reads the csv created by Skin Deep Extract.py, splits the ingredient lists into individual ingredients, and formats the data to be uploaded to Factotum

Written in Python 3.7

NOTE: All Skin Deep groups were extracted using these scripts, but were registered as seperate scripts so they could be QA'd individually
