## Script for processing generic PDFs

This script was designed to process the Walmart MSDS dataset. Because of the many different types of files in the dataset, this script can read both MSDSs and product labels, as well as use OCR when necessary.

### How to run
In the same directory as the script, there should be a folder called 'pdfs'. All of the PDFs that will be processed will be in this folder. Similarly, there should be a folder called 'output' will contain all of the outputs. These can be changes in lines 38 and 40.

The boolean parameter on line 32, 'do_OCR', Determines if the script should attempt OCR. Additionally, setting 'all_OCR' to True will allow the script to perform OCR on every file, not just the ones with no text. This may be necessary when an MSDS has useful information in both images and text, or when multiple MSDSs are combines and a subset of them are scanned.

You should put the edited 'mysql.json' in the folder with the script, as well as this file: ftp://newftp.epa.gov/COMPTOX/Sustainable_Chemistry_Data/Chemistry_Dashboard/2019/April/DSSTox_Identifiers_and_CASRN.xlsx.

The script will output a CSV file containing a list of chemicals for each PDF in the output folder. It will also output a generic info file in the root of the folder.

### Packages
* Python (tested on 3.7, I know you need at least 3.5)
* NumPy
* pandas
* PyMySQL
* SQLAlchemy
* xlrd
* libiconv
* NLTK
* python-Levenshtein
* fuzzywuzzy (conda-forge)
* Tika (conda-forge)
* Tesseract (conda-forge) (if you install this after running Tika, restart Tika)

### Todo
* Extract product name
* Extract manufacturer name
* Extract date
* Extract units
