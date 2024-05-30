#import packages
import os, string, csv, re, time
import pandas as pd
from glob import glob

# LOCATION OF CURATED DSSTOX FILES. CHANGE EVERY TIME.
path = r"C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\chemical curation upload\2024-05-29"
os.chdir(path)

excel_files = glob("*.xlsx") #grabs all .xlsx files

for excel in excel_files:
    out = excel.split('.')[0]+'_formatted.csv'
    df = pd.read_excel(excel)
    upload_columns = df[['Extenal_ID','DSSTox_Source_Record_Id', 'DSSTox_Substance_Id', 'Substance_Name', 'Substance_CASRN' ]]


    upload_columns.rename(
        columns={
            "Extenal_ID": "external_id",
            "DSSTox_Source_Record_Id": "rid",
            "DSSTox_Substance_Id": "sid",
            "Substance_Name": "true_chemical_name",
            "Substance_CASRN": "true_cas"
        },
        inplace=True
    )
    
    upload_columns.to_csv(out,index=False, encoding = 'utf-8') #create a new csv to write formatted data)
    print('created: ',out)
    time.sleep(30) #give it time to write csvs


#Split files for upload
uploadFolder = path+r'/uploads'
os.mkdir(uploadFolder)
time.sleep(30) #give it time to write csvs

files = glob('*formatted.csv')
nRows = 3500 #Number of rows in upload csvs

# os.chdir(path)
for f in files:
    with open(f, 'r', newline='', errors="ignore") as source:
        reader = csv.reader(source)
        headers = next(reader)
        j = 1
        records_exist = True
        while records_exist:
            i = 0
            newName = uploadFolder+'/'+f.split('.csv')[0] + '_' + str(j) + '.csv'
            with open(newName, 'w', newline='') as target:
                writer = csv.writer(target)
                while i < nRows:
                    if i == 0:
                        writer.writerow(headers)
                    try:
                        writer.writerow(next(reader))
                        i += 1
                    except:
                        records_exist = False
                        break
    
            j += 1
            
        print('split: ',f)
