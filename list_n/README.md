### List N Extraction Script

Script related to pulling data on List N. If you're using these scripts, use the ones in the most recent folder.

https://www.epa.gov/pesticide-registration/list-n-disinfectants-use-against-sars-cov-2

### Requirements
The only non-base imports are pandas and beautifulsoup4. You might need lxml too.

### How to Run
1. Download the CSV on the List N page. File should be in `documents/DATE`, relative to the scripts, by default.
2. Change the values after `if __name__ == '__main__'` in `get_epa_reg_no_data.py`. You can change the names and locations of the CSV files you downloaded, as well as the column names of the column with the EPA Registration Numbers and the upload date. You will also need to change the date to match the date you downloaded the files. `old_date` refers to the date you previously downloaded the files, to filter out the entries that were already added. You can change it to `None` if you don't want to look at previous data. In reality, all you should need to change is the dates. Also, setting `reset` to true will overwrite PDF files (and chemical data) instead of keeping them if they already exist.
3. Run `get_epa_reg_no_data.py`. It will create a CSV file in the root folder as well as populate the PDF and chemical folders.
4. Change the date at the top of `make_rr.py` and run it.
5. Make the data group in Factotum, uploading the result of `make_rr.py` for the records file. It should be named something like `list_n_registered_documents_DATE.csv`.
6. Upload the documents to the newly created data group in Factotum.
7. Download the document records file (should be names something like `epa_list_n_-_june_19_2020_documents_20200619.csv`).
8. Change the date at the top of `make_extracted_text.py`, and change `template_file` to the recently downloaded document records file. Run the script.
9. Put the script on GitHub and ask someone to register it.
10. Upload the extracted text (`list_n_extracted_text_formatted_DATE.csv`) to Factotum.
11. QA each entry.
