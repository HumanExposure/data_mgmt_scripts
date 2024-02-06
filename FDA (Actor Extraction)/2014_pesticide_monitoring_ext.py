
# %% imports

import os, string, re, camelot
import pandas as pd
import numpy as np



# %%renaming files in pdf folder


# os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2014")


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
file = r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2014\2014.pdf"
tables = camelot.read_pdf(file,pages='22-32', flavor='lattice')

chemName = []
prodID = []
templateName = []
components = []


tables_ls = []


for i,t in enumerate(tables):
    print('###########')
    print('table: ' + str(i))
    print(t.df)
    print('\n')



for i,table in enumerate(tables):
    df = tables[i].df
    if i <= 2: #Table 3
        chemName.extend(df.iloc[:,0])
        chemName.extend(df.iloc[:,1])
        chemName.extend(df.iloc[:,2])
        prodID.extend(['1690527']*len(df)*3)
        templateName.extend(['2014_pesticide_monitoring_report_table_3.pdf']*len(df)*3)
        components.extend(['']*len(df)*3)
    elif i == 4 : #Table 5 (add in manually: Thiophanate-methyl) 
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690528']*len(df))
        templateName.extend(['2014_pesticide_monitoring_report_table_5.pdf']*len(df))
        components.extend(['']*len(df))
    elif i == 5: #Table 6a
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690529']*len(df))
        templateName.extend(['2014_pesticide_monitoring_report_table_6a.pdf']*len(df))
        components.extend(['']*len(df))

    elif i == 6: #Table 6b
        chemName.extend(df.iloc[:,1])
        prodID.extend(['1690530']*len(df))
        templateName.extend(['2014_pesticide_monitoring_report_table_6b.pdf']*len(df))
        
        for it, t in enumerate(df[0]):
            if len(str(t).strip())==0:
                df[0].iloc[it] = np.NaN
            else:
                df[0].iloc[it] = re.sub(r'\(\d\d\d\)', '', str(t))
        components.extend(df.iloc[:,0])
        
    elif i >= 7: #Table 7
        chemName.extend(df.iloc[:,0])
        prodID.extend(['1690531']*len(df))
        templateName.extend(['2014_pesticide_monitoring_report_table_7.pdf']*len(df))
        components.extend(['']*len(df))
        
j = len(chemName)
while j > 0: #go through list backwards, so it doesnt mess up the index if a row is deleted
    j-=1
    chemName[j] = chemName[j].replace('\n',' ').rstrip('+').strip().rstrip('*').strip().lower().replace('  ',' ')
    if prodID[j] != '1690527': chemName[j] = chemName[j].replace('ǂ', '').replace('*', '').rstrip('2').rstrip('3').rstrip('4').rstrip('5')
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
df['component'] = df['component'].ffill()
# %%



os.chdir(r"C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Projects\Extraction Scripts\FDA\Pesticide Residue Monitoring\2014")
df.to_csv(r'2014_pesticide_monitoring_ext.csv',index=False, header=True, date_format=None)

# %%
