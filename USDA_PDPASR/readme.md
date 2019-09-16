# USDA Pesticide Data Program Annual Summary Report Extractions

Reports contain information regarding the presence of chemical pesticide residues in food.  Occasionally, the function of the chemical pesticide is also given.  Each report was extracted with a customized script to account for formatting changes from report to report.  

Included is a script written by [Allison Larger](https://github.com/larger-allison) used to duplicate the PDF of the report for document matching in Factotum, credited in the code as well.

## Requirements

All scripts were run using Spyder in a Python 3.7.4 environment using the packages:
* Pandas
* Tabula-py


To reproduce the environment, run the following commands in Anaconda Powershell
```bash
conda create --name py374 python=3.7.4
conda activate py374
conda install -c anaconda pandas
conda install -c conda-forge tabula-py
```

## Usage

1. Run the script
2. Write and upload Registered Records CSV
3. Get new Registered Records document from Factotum, and use to print PDFs and get Data Document IDs
4. Write and upload extracted data CSV
