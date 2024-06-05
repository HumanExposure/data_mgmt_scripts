To make sure you get the order of scripts right, this is the order for the ingredient list:

1. State_Industrial_Ingredient_Web_Scraping

This will create the pdfs of screenshots of the tables. Make sure you close out of the "accept cookie" pop up on the bottom of else the screenshot will get the pop up

NOTE FOR 2: DOWNLOAD THE FACTOTUM_TEMPLATE FOR THE DATA DOCUMENT IDS AFTER UPLOADING PDFS TO DATA GROUP
This will let the code populate the csvs with the correct ids

2. State_Industrial_Ingredient_Data_Extraction

This will create the csv files with data from each table for each product. It does this through web scraping

3. add_ingredient_rank

4. Combined_CSVS

This will allow for the creation of a combined.csv in the same folder as the others

IMPORTANT NOTE FOR FUTURE RUNS: DELETE THE COMBINED.CSV OR ELSE IT WILL GET COMBINED INTO A NEW COMBINED.CSV, DUPLICATING ALL CHEMICALS