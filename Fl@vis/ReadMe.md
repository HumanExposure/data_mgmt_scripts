lkoval
3-13-20

Scripts to downlod the web pages as pdfs and extract chemical names and cas numbers from the [fl@vis flavoring substances list](http://ec.europa.eu/food/food/chemicalsafety/flavouring/database/). 

The download script was written in Python 3.6 with selenium 3.141.0 and ChromeDriver 80.0.3987.106. All 111 pages were saved as pdfs using [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) 0.12.5 for Win64 and pdfkit 0.6.1. All individual pdfs were joined into a single file with pypdf2 1.26.0.

For computational simplicity, the extraction script reads the excel file downloaded from fl@vis website. The script was written in Python 3.7.3 utilizing pandas 0.24.1.
