
# %% imports

import os, string, re, camelot
import pandas as pd
import numpy as np



# %%renaming files in pdf folder


# os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2019")


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
components = []

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2019\2019.pdf"
tables = camelot.read_pdf(file,pages='23-25,30', flavor='lattice')


tables_ls = []



# for i,table in enumerate(tables):
#     print('#################')
#     print('table: ' + str(i))
#     print(tables[i].df)
#     print('/n')


for i,table in enumerate(tables):
    df = tables[i].df
    if i <= 2: #Table 3
        chemName.extend(df.iloc[:,0])
        chemName.extend(df.iloc[:,1])
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690553']*len(df)*3)
        templateName.extend(['2019_pesticide_monitoring_report_table_3.pdf']*len(df)*3)
        components.extend(['']*len(df)*3)
    elif i == 3: #Table 7
        chemName.extend(df.iloc[:,0])
        chemName.extend(df.iloc[:,1])
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690554']*len(df)*3)
        templateName.extend(['2019_pesticide_monitoring_report_table_7.pdf']*len(df)*3)
        components.extend(['']*len(df)*3)
    
        
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').rstrip('+').strip().rstrip('*').strip().lower().replace('  ',' ')
    chemName[j] = re.sub(r'\(\d+\)$', '', chemName[j]).strip()
    if prodID[j] != '1690553': chemName[j] = chemName[j].replace('ǂ', '').replace('*', '').rstrip('2').rstrip('3').rstrip('4').rstrip('5')
    if chemName[j] == '' or 'pesticide' in chemName[j] or 'none' in chemName[j] or chemName[j] == 'all others':
        del chemName[j]
        del templateName[j]
        del prodID[j]
        del components[j]

        
nIngredients = len(chemName)
msdsDate = ['']*nIngredients
recUse = ['']*nIngredients
catCode = ['']*nIngredients
descrip = ['']*nIngredients
code = ['']*nIngredients 
sourceType = ['ACToR Assays and Lists']*nIngredients
casN = ['']*nIngredients 



# %%

df = pd.DataFrame({'data_document_id':prodID, 'data_document_filename':templateName, 'doc_date':msdsDate, 'raw_category':recUse, 'raw_cas':casN, 'raw_chem_name':chemName, 'cat_code':catCode, 'description_cpcat': descrip, 'cpcat_code':code, 'cpcat_sourcetype':sourceType, 'component': components})

# %%



os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2019")
df.to_csv(r'2019_pesticide_monitoring_ext.csv',index=False, header=True, date_format=None)

# %%
