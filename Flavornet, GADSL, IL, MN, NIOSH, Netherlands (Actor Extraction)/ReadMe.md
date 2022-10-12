- CMR Substances in Consumer Preparations.py
- GADSL 2013.py
- GADSL 2014.py
- GADSL 2015.py

These scripts extract the active ingredients and CAS numbers from reports and place them in templates with other document information to be uploaded to Factotum.
The ingredients and CAS numbers were extracted using the Python package Camelot. In order to use Camelot, you must first download Ghostscript, and then install Camelot in a Python 3.6 environment. DO NOT attempt to install Camelot in Python 3.7.

(Written in Spyder, Python 3.6, by Allison Larger)

---

- Allergens_script.Rmd

Chemicals and cas numbers are extracted using the tabulizer package in R 4.1.2. It is recommended you use R 4.1.2 as there are compatibility issues in the newer versions of R. You must install and load the tabulizer package before being able to extract data using this script. Additional packages used to manipulate data include the following:

tcltk
rJava
tabulizer
tidyverse
data.table

The Following code may be helpful if you seem to be running into issues with installing tabulizer and other needed packages.

install.packages("rJava")
install.packages("devtools")
devtools::install_github("ropensci/tabulizer", args="--no-multiarch")

(Written in R Studio, R 4.1.2 , by Christian Lutz)

---

- methamphetamine-NIOSH.py

The chemicals and CAS numbers were extracted using the Python package Tabula, which can be installed through conda-forge in Anaconda Powershell. 

(Written in Spyder, Python 3.8, by Mary Horton)
