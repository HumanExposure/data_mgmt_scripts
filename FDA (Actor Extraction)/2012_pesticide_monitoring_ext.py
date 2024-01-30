
# %% imports

import os, string, re, camelot
import pandas as pd
import numpy as np



# %%renaming files in pdf folder


# os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2012")


# file_names = pd.read_csv("filenames.csv")
# file_names = file_names["filename"].to_list()


# data = os.path.abspath("pdfs/")

# for i, f in enumerate(os.listdir(data)):
    
#     file = file_names[i]
#     src = os.path.join(data, f)
#     dst = os.path.join(data, file)
#     os.rename(src, dst)



# %%

chemName = []
prodID = []
templateName = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2012\2012.pdf"
tables = camelot.read_pdf(file,pages='24-37', flavor='lattice')

table_test = tables[13].df

for i,table in enumerate(tables):
    print("table number" + str(i))
    print(tables[i].df)

tables_ls = []

for i,table in enumerate(tables):
    print('table: '+str(i))
    print(table.df)
    print("##############")
    print('\n')


for i,table in enumerate(tables):
    df = tables[i].df
    if i <= 4: #Table 3
        chemName.extend(df.iloc[:,0])
        chemName.extend(df.iloc[:,1])
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690504']*len(df)*3)
        templateName.extend(['2012_pesticide_monitoring_report_table_3.pdf']*len(df)*3)
    elif i == 6: #Table 5
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690505']*len(df))
        templateName.extend(['2012_pesticide_monitoring_report_table_5.pdf']*len(df))
    elif i == 8: #Table 6b
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690508']*len(df))
        templateName.extend(['2012_pesticide_monitoring_report_table_6b.pdf']*len(df))
    elif i >=10 or i <= 12: #Table 7
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690506']*len(df))
        templateName.extend(['2012_pesticide_monitoring_report_table_7.pdf']*len(df))
    elif i >= 13: #Table 8
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690507']*len(df))
        templateName.extend(['2012_pesticide_monitoring_report_table_8.pdf']*len(df))
    
    
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').rstrip('+').strip().rstrip('*').strip().lower().replace('  ',' ')
    if prodID[j] != '1690504': chemName[j] = chemName[j].replace('ǂ', '').replace('*', '').rstrip('2').rstrip('3').rstrip('4').rstrip('5')
    if chemName[j] == '' or 'pesticide' in chemName[j] or chemName[j] == 'all others':
        del chemName[j]
        del templateName[j]
        del prodID[j]
        
nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 
  
df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType})

# %%



os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2012")
df.to_csv(r'2012_pesticide_monitoring_ext.csv',index=False, header=True, date_format=None)
