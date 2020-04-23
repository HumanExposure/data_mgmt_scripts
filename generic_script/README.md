## Script for processing generic PDFs

This script was designed to process the Walmart MSDS dataset. Because of the many different types of files in the dataset, this script can read both MSDSs and product labels, as well as use OCR when necessary.

### How to run
There are multiple scripts. They should all be in the same folder. You also need to download `read_chemicals.py` from https://github.com/HumanExposure/data_mgmt_scripts/tree/master/read_chemicals. One other thing you need to do is put the edited 'mysql.json' in the folder with the scripts.

The script to run is called `run_extraction.py`. There are a few ways to run this script.
* No arguments: Looks in a folder called `pdf` for files
* A path to a folder with PDFs
* A zip file of PDFs
* A CSV list with filenames, with a second argument being the folder they're in

A few parameters can be changed in the script.
* You can change the default PDF folder (from `pdfs`)
* You can change the default output folder (from `output`)
* `do_OCR`: Whether to perform OCR
* `all_OCR`: Whether to perform OCR on all files. Useful when files have images and text.

The script will output a CSV file containing a list of chemicals for each PDF in the output folder. It will also output a generic info file in the output folder.

After running the extraction script, you need to run `transform.py`. This takes the outputs, cleans them, and turns them into a format suitable for Factotum. You will need to edit a few things in the script, right below `if __name__ == '__main__'`.
* `folder`: folder with output files
* `chem_file`: filename of chemical data output from `run_extraction.py`
* `info_file`: filename of info data output from `run_extraction.py`
* `template_file`: filename of extracted text template from factotum
* `documents_file`: filename of document records file from factotum

Another thing to note: `get_filenames.py` makes a CSV of the document filenames for specified groups. It is not necessary for running the script itself.

Tika will still be running in the background after running the script, you may need to kill it manually.

```bash
ps aux | grep java | grep Tika
kill -9 PID
```
OR
```bash
kill -9 $(ps aux | grep java | grep Tika | grep -oP -m1 "^\w{3,10}\s{1,}\K\w{4,5}")
```

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
* rdkit (conda-forge) (for read_chemicals.py)
* Tesseract (conda-forge) (if you install this after running Tika, restart Tika)
