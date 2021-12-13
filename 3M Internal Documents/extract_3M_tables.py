# -*- coding: utf-8 -*-


"""Table extraction program for 3M-EPA documents.

This program utilizes the 'tabula-py' library to extract tables from
PDF documents. Optical character recognition is preferred, as it makes
reading the PDF documents easier, and mitigates some of the issues that
non-OCR documents have (scanned pages, faint text, etc).

You can run this script from any location, but the 'home_dir' variable
will need to be changed manually to the location of where the PDF files are
stored. It is assumed that the PDF files are all stored in a single directory,
specified in the 'home_dir' variable.

NOTES:
    1) The PDFs on which this script was run initially followed the naming
       scheme: "3M-EPA-XXXXXXXX" where X in [0-9]. The 'doc_num' variable
       created in the code is this 8-digit number, and this is how the PDFs are
       referred to.
"""


# -------------------------------------------
# ---------- Module dunders ----------
# -------------------------------------------
__author__ = "Stephen Steward"
__email__ = "steward.stephen@epa.gov"


# -------------------------------------------
# ---------- Package imports ----------
# -------------------------------------------
import os
import sys
import glob
import subprocess
import tabula
from PyPDF2 import PdfFileReader


# -------------------------------------------
# ---------- Function declarations ----------
# -------------------------------------------


# -------------------------------------------
# ---------- Main ----------
# -------------------------------------------

# Set directory where PDF files are stored.
home_dir = (r'C:\Users\ssteward\OneDrive - Environmental Protection Agency '
            r'(EPA)\Profile\Documents')
os.chdir(home_dir)

# Get list of all PDF files in home_dir.
files = glob.glob('*.pdf')

# If the folder contains no PDF files, print error and gracefully exit.
if len(files) == 0:
    sys.exit('\nNo PDF files found...exiting.\n')

# Get number of documents.
num_docs = len(files)

# Begin iteration.
for file in files:

    # Initialize empty list of tables to write to csv.
    tables = []

    # Print the current file name.
    print(f'\nThe current file is: {file}')

    # Get document number.
    last_dash = max(index for index, char in enumerate(file) if char == '-')
    doc_num = file[last_dash+1:last_dash+9]

    # Check if a subdirectory matching the document number exists.
    # If one does not exist, the directory is created.
    # Next, a CSVs subdirectory is created in each document directory.
    if not os.path.exists(home_dir+f'\\{doc_num}'):
        os.mkdir(home_dir+f'\\{doc_num}')
    doc_dir = home_dir+f'\\{doc_num}'
    if not os.path.exists(doc_dir+'\\CSVs'):
        os.mkdir(doc_dir+'\\CSVs')

    # Get the number of pages in each file.
    pdf_reader = PdfFileReader(file)
    num_pages = pdf_reader.numPages
    print(f'\nPage count: {num_pages}')

    # Begin extraction
    print('\nScanning for tables...')
    for i in range(1, num_pages+1):

        # Scan each page for tables.
        # If a table is found, the table data (df) and page number (i) are
        # saved in a tuple (df, i) and appended to the list initialized
        # above.

        # In the event that Tabula runs into an error (usually as a result
        # of its dependencies on Java) it throws a SubprocessError and
        # immediately terminates the script, discarding any unwritten data.
        # To get around this, the SubprocessError is caught and ignored,
        # skipping the page that caused the error and allowing the script
        # to continue.
        try:
            if df := tabula.read_pdf(file, pages=i, multiple_tables=True,
                                     format="CSV", silent=True):
                print(f'\nTable found on page {i}')
                tables.append((df, i))
            else:
                print(f'\nNo table found on page {i}')
        except subprocess.SubprocessError:
            print(f'\nError encountered on page {i}...skipping')
            continue

    # Change to csv storage directory
    os.chdir(doc_dir+'\\CSVs')

    # Create a table counter variable
    table_count = 1

    # Iterate over the stored table list, and write each table to a .csv
    # file using the following convention: DOC-NUM_TABLE-NUM_PAGE-NUM
    for table in tables:
        for i in range(len(table[0])):
            table[0][i].to_csv(f'{doc_num}_table{table_count}_'
                               f'page{table[1]}.csv')
            table_count += 1
    os.chdir(home_dir)
