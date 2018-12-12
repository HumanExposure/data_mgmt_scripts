# pdf_extraction script
This script looks at a directory of your choosing, 
finds all of the pdf's in that directory, and attempts 
to extract text from each pdf. The text is then inserted into a mysql 
database along with the filename and datagroup (from factotum) of the 
pdf.

## File Modifications
To make the script usable you will need to modify the files below as 
indicated.  

`extract_pdfs.py`  
There are two variables that need values in this file:  
DATAGROUP_ID - Which is the factotum_datagroup.id for the directory
you are searching  
DIRECTORY = The full path to the directory to search  
  
`config.yml.example`  
This file holds the mysql secrets. Modify the contents for your 
credentials and rename the file config.yml which is ignored for this 
repo
