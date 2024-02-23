
# %% imports

import os, string, re, camelot
import pandas as pd
import numpy as np



# %%renaming files in pdf folder


# os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\CDER Drug and Biologic Approvals\2014")


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
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\CDER Drug and Biologic Approvals\2014\2014.pdf"
tables = camelot.read_pdf(file,pages='all', flavor='lattice') #, table_areas=['316,499,566,337']


tables_ls = []

for i,table in enumerate(tables):
    print("###############")
    print("table "+str(i))
    # camelot.plot(table, kind='text').show()
    print(table.df)
    print("\n")


for i,table in enumerate(tables):
    df = tables[i].df
    if i <= 1 : #New Drug Approvals
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690585']*len(df))
        templateName.extend(['cder_drug_and_biological_approvals_2014_nda.pdf']*len(df))
        components.extend(['']*len(df))
    else: #Table 7
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690586']*len(df))
        templateName.extend(['cder_drug_and_biological_approvals_2014_bla.pdf']*len(df))
        components.extend(['']*len(df))


manual_additions = ['TESTOSTERONE GEL', 'TOBRAMYCIN INHALATION SOLUTION AND PARI LC PLUS REUSABLE NEBULIZER', 'BUDESONIDE']
manual_additions = [x.lower() for x in manual_additions]
chemName.extend(manual_additions)
prodID.extend(['1690585']*len(manual_additions))
templateName.extend(['cder_drug_and_biological_approvals_2014_nda.pdf']*len(manual_additions))
components.extend(['']*len(manual_additions))


j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').rstrip('+').strip().rstrip('*').strip().lower().replace('  ',' ')
    chemName[j] = re.sub(r'\(\d+\)$', '', chemName[j]).strip()
    if prodID[j] != '1690585': chemName[j] = chemName[j].replace('ǂ', '').replace('*', '').rstrip('2').rstrip('3').rstrip('4').rstrip('5')
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

# %%


os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\CDER Drug and Biologic Approvals\2014")
df.to_csv(r'2014_cder_drug_approvals_ext.csv',index=False, header=True, date_format=None)

# %%
