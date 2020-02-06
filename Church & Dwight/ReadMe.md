lkoval
2-3-2020

Navigates [Church & Dwight's website](https://churchdwight.com/ingredient-disclosure/default.aspx) to save ingredient disclosures as pdfs and extract the product name, raw cateogry, material number, chemicals, functional uses, and cas numbers (where appicable) for listed products. If an SDS was available, it was saved as well. Generally, there were two different formats for the ingredient disclosures. The first usually contained one table of chemicals and their functional uses. The second usually contained two tables, one for chemicals of general functional uses and one for chemicals that were exclusively used as fragrances. The second format also included cas numbers and an SDS. Any product url that couldn't be downloaded or extracted was saved in a seperate list. Upon inspection, most of these were able to be extracted manually.

* Python 3.7.6
* Selenium 3.141.0
* [ChromeDriver](https://chromedriver.chromium.org/) 79.0.3945.36
* [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) 0.12.5 for Win64
