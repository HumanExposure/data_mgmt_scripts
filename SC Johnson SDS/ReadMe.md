### scjDownloadSDS.py
Navigates to the [SC Johnson SDS download page](https://www.scjohnson.com/Our%20Products/Safety%20Data%20Sheets?f2=United%20States%20(English)), scrolls down the page, and downloads the SDS pdfs as they appear on the page. (Python 3.7)

### scjExtractSDS.py
Uses [Xpdf](https://www.xpdfreader.com/download.html) to convert the pdfs downloaded in scjDownloadSDS.py to text, extracts product and ingredient data, and generates a csv containing the extracted data. (Python 3.7) 

