# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:42:12 2022

@author: MHORTON
"""

import string, re
from glob import glob

from pdfminer.high_level import extract_text
import tabula as tb
import pandas as pd

from datetime import datetime
startTime = datetime.now()

# %%
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    return(cline)

# %% Extract data from PDFs
def extPDF(filePath, manus):    
    batches = pathPDFs(filePath)
    extracted = []
    
    try:
        csvs = glob(filePath + '*extraction.csv')
    except: print('No extracted data.')
    
    for csv in csvs:
        extbatch = pd.read_csv(csv, header = None)
        extbatch = extbatch.T.values.tolist()
        extracted.extend(set(extbatch[0]))
    
    for i, batch in enumerate(batches):
        pdfs = batch
        batchName = batch[0].rsplit('/', 1)[1].split('\\')[0]
        print(f'Beginning {batchName} extraction...')
        
        fnames = []
        prodnames = []
        suppliers = []
        recuses = []
        dates = []
        versions = []
        ranks = []
        
        chems = []
        casnums = []
        mins = []
        cents = []
        maxs = []
        
        startTime = datetime.now()
        for pdf in pdfs:
            if pdf.split('\\')[-1] in extracted:
                continue
            else:
                fname = pdf.split('\\')[-1]
                # print(f'Beginning {fname} extraction...')
                
                text = list(filter(None, extract_text(pdf).split('\n')))
                
                prodname = ''
                recuse = ''
                date = ''
                version = ''
                supplier = ''
                chem = ''
            
                for i, line in enumerate(text):
                    if 'product name ' in cleanLine(line) and prodname == '':
                        prodname = cleanLine(line.split('name ')[1])
                    if 'recommended use' == cleanLine(line):
                        recuse = cleanLine(text[i+2]).strip('.')
                    if 'revision date' in cleanLine(line) and date == '':
                        date = cleanLine(line.split('Revision date')[1])
                    if 'version' in cleanLine(line) and version == '':
                        version = line.split(' ')[-1]
                    for j, manufacturer in enumerate(manus):
                        if manufacturer in cleanLine(line) and supplier == '':
                            supplier = manus[j]
                
                dfs = tb.read_pdf(pdf, pages='all', silent=True)
                compchems = []
                # addchems = []
                # addcass = []
                # extrachems = []
                for df in dfs:
                    if 'weight-%' in list(df.columns):    
                        chem = ''
                        cas = ''
                        comp = ''
                        low = ''
                        cent = ''
                        high = ''
                        for index, row in df.iterrows():
                            chem = str(row[0])
                            cas = str(row[1])
                            comp = str(row[2])
                            
                            # if the cas is nan, it is a continuation and we need to clean up the chemical name and continue
                            if 'nan' in str(cas):
                                chems[-1] = chems[-1] + ', ' + chem
                                chem = ''
                            elif 'nan' in comp: #if comp is nan
                                low = ''
                                high = ''
                                cent = ''
                            elif '-' in comp: #if a range of weight%, assign min and max
                                low = comp.split('-')[0].strip()
                                high = comp.split('-')[1].strip()
                                cent = ''
                            else: #In the event there is not a range given
                                cent = comp.strip()
                                low = ''
                                high = ''
                            
                            compchems.append(cleanLine(chem))
                            
                            if chem != '':
                                fnames.append(fname)
                                chems.append(cleanLine(chem))
                                casnums.append(cleanLine(cas))
                                mins.append(cleanLine(low))
                                cents.append(cleanLine(cent))
                                maxs.append(cleanLine(high))
                            
                                prodnames.append(prodname)
                                suppliers.append(supplier)
                                recuses.append(recuse)
                                dates.append(date)
                                versions.append(version)
            if chem == '':
                fnames.append(fname)
                chems.append('')
                casnums.append('')
                mins.append('')
                cents.append('')
                maxs.append('')
            
                prodnames.append(prodname)
                suppliers.append(supplier)
                recuses.append(recuse)
                dates.append(date)
                versions.append(version)
                        
        # Create the ranks
        ranks = []
        names = []
        [names.append(x) for x in fnames if x not in names]
        for name in names:
            ranks.extend([*range(1,(fnames.count(name)+1))])
            
        
        # Some cleanup
        for i, cas in enumerate(casnums):
            if 'nocas' in cas or 'proprietary' in cas: #no cas given
                casnums[i] = ''
        
        endTime = datetime.now()
        print('Extraction time: ', endTime - startTime)
                
        extDFbatch = pd.DataFrame({'data_document_id':fnames, 'data_document_filename':fnames, 
                              'prod_name':prodnames, 'report_funcuse':recuses, 'component':['']*len(chems), 
                              'doc_date':dates, 'rev_num':versions, 'ingredient_rank':ranks, 
                              'raw_chem_name':chems, 'raw_cas':casnums, 'raw_min_comp':mins, 
                              'raw_central_comp':cents, 'raw_max_comp':maxs, 'raw_category':['']*len(chems), 
                              'unit_type':['3']*len(chems), 'suppliers':suppliers})
        
        N = batch[0].rsplit('/', 1)[1].rsplit('\\', 1)[0].split('pdfs')[1]
        if len(N) < 2:
            N = '0' + N
        
        try: #append to existing CSV
            extDFbatch.to_csv(filePath + N + '_tyco_extraction.csv', mode = 'a', index=False, header=False)
        except:
            extDFbatch.to_csv(filePath + N + '_tyco_extraction.csv', index=False, header=True)

# %% Split PDF folders
def splitPDFs():
    # -*- coding: utf-8 -*-
    """
    Created on Mon Jul 29 08:49:52 2019
    @author: ALarger
    Splits folder of pdfs into multiple folders with 600 pdfs each to be uploaded to factotum
    
    Slightly modified
    """
    
    import os
    from shutil import copyfile
    
    path = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/TycoSDS/pdfs/'
    os.chdir(path)
    pdfs = glob("*.pdf")
    
    i = 0
    j = 0
    for pdf in pdfs:
        if j%600 == 0:
            i += 1
            if len(str(i)) < 2:
                newFolder = path + 'pdfs0' + str(i)
            else:
                newFolder = path + 'pdfs' + str(i)
            try:
                os.mkdir(newFolder)
            except:
                print(f'{newFolder} already exists.')
                pass
        j += 1
        oldPath = path + pdf
        newPath = newFolder + '\\' + pdf
        copyfile(oldPath,newPath)
        
# %% Get list of PDFs, split into batches
def pathPDFs(filePath):
    pdfsPath = filePath + 'pdfs/'
    pdfsPaths = glob(pdfsPath + '*/', recursive = True)
    pdfsPaths = [folder for folder in pdfsPaths if 'used' not in folder]
    
    for i, pdf in enumerate(pdfsPaths):
        pdfsPaths[i] = pdf.split('\\')[0] + '/' + pdf.split('\\')[1]
    
    batches = []
    
    for path in pdfsPaths:
        batches.append(glob(path + '\\' + '*.pdf'))
    
    return batches

# %% Create full Extracted Text CSV
def makeExtDF(filePath): 
    extDFraw = pd.DataFrame()
    try:
        csvs = glob(filePath + '*extraction.csv')
    except: print('No extracted data.')
    
    for csv in csvs:
        extDFadd = pd.read_csv(csv, names=['data_document_id', 'data_document_filename', 
                                           'prod_name', 'report_funcuse', 'component', 
                                           'doc_date', 'rev_num', 'ingredient_rank', 
                                           'raw_chem_name', 'raw_cas', 'raw_min_comp', 
                                           'raw_central_comp', 'raw_max_comp', 
                                           'raw_category', 'unit_type', 'suppliers'])
        extDFraw = pd.concat([extDFraw, extDFadd], ignore_index=True)

    extDFraw = extDFraw.fillna('')
    extDFraw = cleanComp(extDFraw)
    
    #fix accidental transposition of raw_category and report_funcuse
    extDFraw['raw_category'] = extDFraw['report_funcuse']
    extDFraw['report_funcuse'] = ''
    
    mask = extDFraw['data_document_filename'].str.contains('TEEX-500P.pdf')
    extDFraw.loc[mask, 'prod_name'] = 'thunderstorm teex-500' #manual fix for missing title
    
    # rename product names to include unique parts number
    extDFraw['prod_name'] = extDFraw['prod_name'] + ' (' + extDFraw['data_document_id'].str.strip('.pdf') + ')'
    
    # drop any extra rows with blank chemicals
    extDFraw.drop(extDFraw.loc[(extDFraw['raw_chem_name'] == '' ) & (extDFraw['ingredient_rank'] != 1 )].index, inplace=True)
    extDFraw = extDFraw.reset_index(drop = True)
    
    try:
        rridDF = pd.read_csv(filePath + 'tyco_fire_protection_products_thewercs_sds_registered_documents.csv')
        file2id = dict(zip(rridDF['filename'], rridDF['DataDocument_id']))
    
        extDFraw['data_document_id'] = extDFraw.data_document_id.replace(file2id)
    except: print('Documents not yet registered.')

    extDF = extDFraw.drop(['suppliers'], axis=1)
    
    # convert all values to strings and clean up unwanted decimals from unwanted floats
    columns = list(extDF.columns)
    for column in columns: # Clean up data types and unintentional floats
        extDF[column] = extDF[column].astype(str)
    
    cleanups = ['rev_num','raw_min_comp', 'raw_central_comp', 'raw_max_comp']
    for column in cleanups:
        extDF[column] = extDF[column].apply(lambda x: x.split('.0')[0])
    
    extDF.to_csv(filePath + 'tyco_extracted-text.csv',index=False, header=True)
    
    return extDFraw

# %% Registered Record CSV
def makeRrDF(filePath):
    extDF = makeExtDF(filePath)
    doctype = ['SD'] * len(extDF['data_document_filename'])
    urls = ['https://tycosds.thewercs.com/external/private/search.aspx'] * len(extDF['data_document_filename'])
    blanks = [''] * len(extDF['data_document_filename'])
    
    rrDF = pd.DataFrame({'filename':extDF['data_document_filename'], 'title':extDF['prod_name'], 
                          'document_type':doctype, 'url':urls, 'organization':extDF['suppliers'], 
                          'subtitle':blanks, 'epa_reg_number':blanks, 'pmid':blanks, 
                          'hero_id':blanks})
    
    rrDF['title'] = rrDF['title'].apply(cleanLine)
    rrDF = rrDF.drop_duplicates().reset_index(drop=True)
    rrDF.to_csv(filePath + 'tyco-registered-records.csv', index=False, header=True)
    
    return rrDF

# %% Product Data CSV
def prodDf(filePath):
    productsDF = pd.read_csv(filePath + 'product_csv_template_934.csv')
    blanks = [''] * len(productsDF['data_document_filename'])
    urls = ['https://tycosds.thewercs.com/external/private/search.aspx'] * len(productsDF['data_document_filename'])


    productsDF = pd.DataFrame({'data_document_id':productsDF['data_document_id'], 
                                'data_document_filename':productsDF['data_document_filename'], 
                                'title':productsDF['data_document_filename'], 'upc':blanks, 'url':urls, 
                                'brand_name':blanks, 'size':blanks, 'color':blanks, 
                                'item_id':blanks, 'parent_item_id':blanks, 'short_description':blanks, 
                                'long_description':blanks, 'epa_reg_number':blanks, 
                                'thumb_image':blanks, 'medium_image':blanks, 'large_image':blanks, 
                                'model_number':productsDF['data_document_filename'], 
                                'manufacturer':productsDF['data_document_filename'], 
                                'image_name':blanks})
    
    rrDF = pd.read_csv(filePath + 'tyco_fire_protection_products_thewercs_sds_registered_documents.csv')
    file2title = dict(zip(rrDF['filename'], rrDF['title']))
    file2manu = dict(zip(rrDF['filename'], rrDF['organization']))
    
    productsDF['title'] = productsDF.title.replace(file2title)
    productsDF['manufacturer'] = productsDF.manufacturer.replace(file2manu)
    productsDF['model_number'] = productsDF['model_number'].str.strip('.pdf')
    
    productsDF = productsDF.drop_duplicates().reset_index(drop=True)
    
    prodDFs = []
    for i in range(len(productsDF)):
        if i % 300 == 0:
            prodDFs.append(productsDF[i:i+300])
    
    fname = 1
    for df in prodDFs:
        if len(str(fname)) == 1:
            df.to_csv(filePath + 'tyco_products_' + '0' + str(fname) + '.csv',index=False, header=True)
            fname += 1
        else:
            df.to_csv(filePath + 'tyco_products_' + str(fname) + '.csv',index=False, header=True)
            fname += 1

# %% 
def cleanComp(extDF):
    splitDF = extDF
    
    # if '<' in central comp
    mask = splitDF['raw_central_comp'].str.contains('<')
    split = splitDF['raw_central_comp'].str.split('<')
    splitDF.loc[mask, 'raw_min_comp'] = '0'
    splitDF.loc[mask, 'raw_max_comp'] = split[mask].str[-1]
    splitDF.loc[mask, 'raw_central_comp'] = ''

    # if '>' in central comp
    mask = splitDF['raw_central_comp'].str.contains('>')
    split = splitDF['raw_central_comp'].str.split('>')
    splitDF.loc[mask, 'raw_min_comp'] = split[mask].str[-1]
    splitDF.loc[mask, 'raw_max_comp'] = '100'
    splitDF.loc[mask, 'raw_central_comp'] = ''
    
    return splitDF

# %%
def main():
    filePath = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/TycoSDS/'
    
    manus = ['chemguard', 'fln feuerlschgerte', 'hart and cooley', 'johnson controls', 
             'macron safety systems (uk)', 'sabo foam s.r.l.', 'total feuerschutz gmbh', 
             'tyco fire protection products', 'tyco safety products', 'williams fire and hazard']
    
    splitPDFs()
    
    extPDF(filePath, manus) #scrape unextracted PDFs
    makeExtDF(filePath)
    makeRrDF(filePath)
    prodDf(filePath)

# %%
if __name__ == "__main__": main()
