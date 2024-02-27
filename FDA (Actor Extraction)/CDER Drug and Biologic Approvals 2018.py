
# %% imports

import os, string, re, camelot
import pandas as pd
import numpy as np



# %%renaming files in pdf folder


# os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\CDER Drug and Biologic Approvals\2018")


# file_names = pd.read_csv("filenames.csv")
# file_names = file_names["filename"].to_list()


# data = os.path.abspath("pdfs/")

# for i, f in enumerate(os.listdir(data)):
    
#     file = file_names[i]
#     src = os.path.join(data, f)
#     dst = os.path.join(data, file)
#     os.rename(src, dst)


# %%
clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\CDER Drug and Biologic Approvals\2018\2018.pdf"
tables = camelot.read_pdf(file,pages='all', flavor='lattice') #, table_areas=['316,499,566,337']

# %%

chemName = []
prodID = []
templateName = []
components = []


tables_ls = []

# for i,table in enumerate(tables):
#     print("###############")
#     print("table "+str(i))
#     print(table.df)
#     print("\n")


for i,table in enumerate(tables):
    df = tables[i].df
    if i < 4 : #New Drug Approvals
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690595']*len(df))
        templateName.extend(['cder_drug_and_biological_approvals_2018_nda.pdf']*len(df))
        components.extend(['']*len(df))
    else: #Table 7
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690596']*len(df))
        templateName.extend(['cder_drug_and_biological_approvals_2018_bla.pdf']*len(df))
        components.extend(['']*len(df))



j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').rstrip('+').strip().rstrip('*').strip().lower().replace('  ',' ')
    chemName[j] = re.sub(r'\(\d+\)$', '', chemName[j]).strip()
    if prodID[j] != '1690595': chemName[j] = chemName[j].replace('ǂ', '').replace('*', '').rstrip('2').rstrip('3').rstrip('4').rstrip('5')
    if chemName[j] == '' or 'proper name' in chemName[j] or 'established' in chemName[j] or chemName[j] == 'all others':
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

#add line to get unique values only
df_drop = df.drop_duplicates()

# %%


os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\CDER Drug and Biologic Approvals\2018")
df_drop.to_csv(r'2018_cder_drug_approvals_ext.csv',index=False, header=True, date_format=None)

# %%
