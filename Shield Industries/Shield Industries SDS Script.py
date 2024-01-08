import csv
import os
import re
import pandas as pd
import PyPDF2
pdf_directory = r'C:\Users\mmetcalf\Documents and Scripts\Shield Industries\SDS Files'

pdf_files = [file for file in os.listdir(pdf_directory) if file.endswith('.pdf')]

df = pd.DataFrame(columns=['filename','title'])

for pdf_file in pdf_files:
    with open(os.path.join(pdf_directory,pdf_file), 'rb') as file:
        if pdf_file == "TotalCare-Green-Carpet-Stain-Soil-Remover-RTU.pdf":
            product_name = "TOTALCARE® “Green” Carpet STAIN & SOIL Remover"
            new_row = pd.DataFrame({'filename': [pdf_file], 'title': [product_name]})
            df = pd.concat([df,new_row], ignore_index=True)
        else:
            reader = PyPDF2.PdfFileReader(file)
            page = reader.getPage(0)
            text = page.extractText()
            start = text.find('Product Name:') + len('Product Name:')
            end = text.find('Date')
            product_name = text[start:end].strip()
            new_row = pd.DataFrame({'filename': [pdf_file], 'title': [product_name]})
            df = pd.concat([df,new_row], ignore_index=True)
df['document_type'] = "SD"
df.loc[46,'document_type'] = "TD"
df['url'] = ""
df["organization"] = "Shield Industries"
df["subtitle"] = ""
df["epa_reg_number"] = ""
df["pmid"] = ""
df["hero_id"] = ""
csv_file = r'C:\Users\mmetcalf\Documents and Scripts\Shield Industries\Shield Industries CSV.csv'
df.to_csv(csv_file,index=False)

