## Script for processing generic PDFs

This script was designed to process the Walmart MSDS dataset. Because of the many different types of files in the dataset, this script can read both MSDSs and product labels, as well as use OCR when necessary.

### How to run
There are multiple scripts. They should all be in the same folder. The script to run is called `run_extraction.py`.

There are a few ways to run this script. With no arguments, the script looks for a folder called `pdf`. All PDFs in the root directory of this folder will be processed. Also, you can use a path to a folder as an argument to the script if that is preferred. The last thing that you can pass is the path to a ZIP file that contains PDFs. This option was created as a solution to some PDFs not opening due to PDF security restrictions.

All output files will be in put in a folder called `output`, which you can create beforehand. This can be changed in the script.

The boolean parameter `do_OCR` can be changed in `run_extraction.py`, and determines if the script should attempt OCR. Additionally, setting `all_OCR` to True will allow the script to perform OCR on every file, not just the ones with no text. This may be necessary when an MSDS has useful information in both images and text, or when multiple MSDSs are combined and a subset of them are scanned.

You should put the edited 'mysql.json' in the folder with the scripts, as well as this file: `ftp://newftp.epa.gov/COMPTOX/Sustainable_Chemistry_Data/Chemistry_Dashboard/2019/April/DSSTox_Identifiers_and_CASRN.xlsx`.

The script will output a CSV file containing a list of chemicals for each PDF in the output folder. It will also output a generic info file in the output folder.

Tika will still be running in the background after running the script, you need to kill it manually.
```bash
ps aux | grep java | grep Tika
kill -9 PID
```
OR
```bash
kill -9 $(ps aux | grep java | grep Tika | grep -oP -m1 "^\w{3,10}\s{1,}\K\w{4,5}")
```
After running the extraction script, download the extraction template from Factotum and put it in the output folder. Edit lines 400-403 of `transform.py` to specify the filenames, then run the script. This cleans the text a little bit and transforms it for upload into Factotum.

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
* beautifulsoup4
* fuzzywuzzy (pip)
* Tika (conda-forge)
* Tesseract (conda-forge) (if you install this after running Tika, restart Tika)

### Todo
* Extract product name
* Extract manufacturer name
* Extract date
* Extract units
