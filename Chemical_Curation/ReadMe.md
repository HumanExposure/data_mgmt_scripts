DOWNLOAD
- Download individual datagroups to a folder under chemical curation files
- Run **download_uncurated_chemicals.py**, after changing number of records in line 56
  - You will have to navigate to the new folder and press save
- Run **find_weird_cas.py** for each csv, split chem cards with multiple cas, fix mistakes
- Redownload csvs for the groups that were fixes
- Run **katherine_clean_chems.py**
- run **skipped_rows_csv.py**
- upload the skipped rows csvs to Factotum
- Send files to Sakshi

UPLOAD
- run **format_curated_chems.py**
- try to upload chems
- If there are errors for specific rows, it is probably because those records have been removed from Factotum
  - review records that are causing errors
  - run **csv_remove_rows.py** to remove messed up rows (copy and paste the row numbers directly from Factotum to line 12, and edit filename and folder)
- try to upload again

