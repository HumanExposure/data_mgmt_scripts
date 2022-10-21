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
    extDF = makeExtDF(filePath)
    scraped = [*set(extDF['data_document_filename'])]
    dls = [pdf.split('\\')[1] for batch in batches for pdf in batch]
    numunext = len(list(set(dls)-set(scraped)))
    print(f'{numunext} PDFs not extracted')
    
    for i, batch in enumerate(batches):
        pdfs = batch
        batchName = batch[0].rsplit('/', 1)[1].split('\\')[0]
        print(f'Beginning {batchName} extraction...')
        
        fnames = []
        prodnames = []
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
        try:
            for pdf in pdfs:
                if pdf.split('\\')[-1] in scraped:
                    continue
                else:
                    fname = pdf.split('\\')[-1]
                    
                    text = list(filter(None, extract_text(pdf).split('\n')))
                    
                    prodname = ''
                    recuse = ''
                    date = ''
                    version = ''
                    
                    for i, line in enumerate(text):
                        if 'product name ' in cleanLine(line) and prodname == '':
                            prodname = cleanLine(line.split('name ')[1])
                        if 'recommended use' == cleanLine(line):
                            recuse = cleanLine(text[i+2]).strip('.')
                        if 'revision date' in cleanLine(line) and date == '':
                            date = cleanLine(line.split('Revision date')[1])
                        if 'version' in cleanLine(line) and version == '':
                            version = line.split(' ')[-1]
                    
                    dfs = tb.read_pdf(pdf, pages='all', silent=True)
                    compchems = []
                    addchems = []
                    addcass = []
                    extrachems = []
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
                                    recuses.append(recuse)
                                    dates.append(date)
                                    versions.append(version)
                        else:                
                            chem = ''
                            cas = ''
                            low = ''
                            cent = ''
                            high = ''
                            
                            cent = ''
                            low = ''
                            high = ''
                            rawchems = df.loc[:, df.columns.str.contains('Chemical name')]
                            if rawchems.size > 0:
                                extrachem = rawchems[rawchems.columns[0]].values.tolist()
                                extrachem = map(str, extrachem)
                                extrachems.extend(extrachem)
                            extrachems = [x for x in extrachems if x != 'nan']
                        
                            for index, row in enumerate(extrachems):
                                if row.count('-') == 2 and bool(re.search('[a-zA-Z]', row)) == False: #Check if a row is probably a CAS number
                                    addchem = cleanLine(extrachems[index - 1])
                                    addcas = cleanLine(extrachems[index])
                                    if addchem not in compchems and addchem not in addchems:
                                        addchems.append(addchem) 
                                        addcass.append(addcas)
        
                        if len(extrachems) > 0 and len(addchems) == 0:
                            #if the script found extra chemicals but none were extracted
                            for c in extrachems:
                                if ' - ' in c:
                                    addchem = cleanLine(c.split(' - ')[0])
                                    addcas = cleanLine(c.split(' - ')[1])
                                    addchems.append(addchem) 
                                    addcass.append(addcas)

                    for i, c in enumerate(addchems):
                        fnames.append(fname)
                        chems.append(c)
                        casnums.append(addcass[i])
                        mins.append(cleanLine(low))
                        cents.append(cleanLine(cent))
                        maxs.append(cleanLine(high))
                    
                        prodnames.append(prodname)
                        recuses.append(recuse)
                        dates.append(date)
                        versions.append(version)
                    
                    if len(compchems) + len(addchems) == 0: #no chemicals extracted
                        fnames.append(fname)
                        chems.append('')
                        casnums.append('')
                        mins.append('')
                        cents.append('')
                        maxs.append('')
                    
                        prodnames.append(prodname)
                        recuses.append(recuse)
                        dates.append(date)
                        versions.append(version)
        
        except BaseException as err:
            print(f'Error extracting {fname}\nUnexpected {err=}, {type(err)=}\n\n')
                
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
                              'unit_type':['3']*len(chems)})
        
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
        
# %% Go back and extract suppliers
def manuEXT(filePath, manus):    
    batches = pathPDFs(filePath)
    manuDFraw = pd.DataFrame()

    csvs = glob(filePath + '*suppliers.csv')
    if len(csvs) == 0: 
        print('No extracted data.')
        scraped = []
    else:
        for csv in csvs:
            manuDFadd = pd.read_csv(csv)
            manuDFraw = pd.concat([manuDFraw, manuDFadd])
        scraped = [*set(manuDFraw['data_document_filename'])]
        dls = [pdf.split('\\')[1] for batch in batches for pdf in batch]
        numunext = len(list(set(dls)-set(scraped)))
        print(f'{numunext} PDFs not extracted')
    
    for i, batch in enumerate(batches):
        pdfs = batch
        batchName = batch[0].rsplit('/', 1)[1].split('\\')[0]
        print(f'Beginning {batchName} supplier extraction...')
        
        fnames = []
        suppliers = []
        
        startTime = datetime.now()
        try:
            for pdf in pdfs:
                if pdf.split('\\')[-1] in scraped:
                    continue
                else:
                    fname = pdf.split('\\')[-1]
                    
                    text = list(filter(None, extract_text(pdf).split('\n')))
                    
                    supplier = ''
                    
                    for i, line in enumerate(text):
                        for j, manufacturer in enumerate(manus):
                            if manufacturer in cleanLine(line) and supplier == '':
                                supplier = manus[j]
                suppliers.append(supplier)
                fnames.append(fname)
        
        except BaseException as err:
            print(f'Error extracting {fname}\nUnexpected {err=}, {type(err)=}\n\n')
        
        endTime = datetime.now()
        print('Extraction time: ', endTime - startTime)

        N = batch[0].rsplit('/', 1)[1].rsplit('\\', 1)[0].split('pdfs')[1]
        if len(N) < 2:
            N = '0' + N

        manuDFbatch = pd.DataFrame({'data_document_filename':fnames, 'suppliers':suppliers})
        manuCSV = filePath + N + '_tyco_suppliers.csv'
        
        if len(fnames) != 0:
            manuDFbatch.to_csv(manuCSV, index=False, header=True)

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
        extDFadd = pd.read_csv(csv)
        extDFraw = pd.concat([extDFraw, extDFadd])
    
    dates = pd.to_datetime([date.split(' ')[0] for date in list(extDFraw['doc_date'])], format='%d-%b-%Y')
    extDFraw['datesort'] = dates
    extDFraw = extDFraw.fillna('')
    extDFraw = cleanComp(extDFraw)
    
    mask = extDFraw['data_document_filename'].str.contains('TEEX-500P.pdf')
    extDFraw.loc[mask, 'prod_name'] = 'thunderstorm teex-500' #manual fix for missing title
    
    rridDF = pd.read_csv(filePath + 'tyco_fire_protection_products_thewercs_sds_registered_documents.csv')
    file2id = dict(zip(rridDF['filename'], rridDF['DataDocument_id']))
    
    extDFraw['data_document_id'] = extDFraw.data_document_id.replace(file2id)
    
    extDFraw['data_document_id'] = extDFraw['data_document_id'].apply(str)
    mask = extDFraw['data_document_id'].str.contains('.pdf')
    extDF = extDFraw[~mask]
    
    extDF.to_csv(filePath + 'tyco_extracted-text.csv',index=False, header=True)
    
    return extDFraw

# %% Registered Record CSV
def makeRrDF(filePath):
    extDF = makeExtDF(filePath)
    doctype = ['SD'] * len(extDF['data_document_filename'])
    urls = ['https://tycosds.thewercs.com/external/private/search.aspx'] * len(extDF['data_document_filename'])
    org = ['tyco fire protection products'] * len(extDF['data_document_filename'])
    blanks = [''] * len(extDF['data_document_filename'])
    
    rrDF = pd.DataFrame({'filename':extDF['data_document_filename'], 'title':extDF['prod_name'], 
                          'document_type':doctype, 'url':urls, 'organization':org, 
                          'subtitle':blanks, 'epa_reg_number':blanks, 'pmid':blanks, 
                          'hero_id':blanks, 'doc_date':extDF['datesort']})
    
    
    rrDF = rrDF.sort_values('doc_date').drop_duplicates('title', keep='last').drop_duplicates().reset_index(drop=True)
    rrDF.drop('doc_date', axis=1, inplace=True)
    rrDF['title'] = rrDF['title'].apply(cleanLine)
    rrDF.to_csv(filePath + 'tyco-registered-records.csv', index=False, header=True)
    
    return rrDF

# %% Product Data CSV
def prodDf(filePath):
    productsDF = pd.read_csv(filePath + 'product_csv_template_932.csv')
    blanks = [''] * len(productsDF['data_document_filename'])
    urls = ['https://tycosds.thewercs.com/external/private/search.aspx'] * len(productsDF['data_document_filename'])


    productsDF = pd.DataFrame({'data_document_id':productsDF['data_document_id'], 
                                'data_document_filename':productsDF['data_document_filename'], 
                                'title':productsDF['data_document_filename'], 'upc':blanks, 'url':urls, 
                                'brand_name':blanks, 'size':blanks, 'color':blanks, 
                                'item_id':blanks, 'parent_item_id':blanks, 'short_description':blanks, 
                                'long_description':blanks, 'epa_reg_number':blanks, 
                                'thumb_image':blanks, 'medium_image':blanks, 'large_image':blanks, 
                                'model_number':blanks, 'manufacturer':productsDF['data_document_filename'], 
                                'image_name':blanks})
    
    rrDF = pd.read_csv(filePath + 'tyco_fire_protection_products_thewercs_sds_registered_documents.csv')
    file2title = dict(zip(rrDF['filename'], rrDF['title']))
    
    manuDF = pd.DataFrame()
    try:
        csvs = glob(filePath + '*suppliers.csv')
    except: print('No extracted data.')
    
    for csv in csvs:
        manuDFadd = pd.read_csv(csv)
        manuDF = pd.concat([manuDF, manuDFadd])
    
    file2manu = dict(zip(manuDF['data_document_filename'], manuDF['suppliers']))
    
    productsDF['title'] = productsDF.title.replace(file2title)
    productsDF['manufacturer'] = productsDF.manufacturer.replace(file2manu)
    
    productsDF = productsDF.drop_duplicates().reset_index(drop=True)
    
    productsDF.to_csv(filePath + 'tyco_products.csv',index=False, header=True)

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

# %% Collect PDFs associated with extracted text for upload
def collectPDFs(filePath):
    batches = pathPDFs(filePath)

    rrDF = makeRrDF(filePath)
    filenames = set(rrDF['filename'])
    usedPDFs = []

    for i, batch in enumerate(batches):
        pdfs = batch
        for pdf in pdfs:
            if pdf.split('\\')[-1] in filenames:
                usedPDFs.append(pdf)

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
    pdfs = usedPDFs
    
    i = 0
    j = 0
    for pdf in pdfs:
        if j%600 == 0:
            i += 1
            if len(str(i)) < 2:
                newFolder = path + 'usedPDFs0' + str(i)
            else:
                newFolder = path + 'usedPDFs' + str(i)
            try:
                os.mkdir(newFolder)
            except:
                print(f'{newFolder} already exists.')
                pass
        j += 1
        oldPath = pdf
        newPath = newFolder + '\\' + pdf.split('\\')[-1]
        copyfile(oldPath,newPath)
        
# %%
def main():
    filePath = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/TycoSDS/'
    
    manus = ['chemguard', 'fln feuerlschgerte', 'hart and cooley', 'johnson controls', 
             'macron safety systems (uk)', 'sabo foam s.r.l.', 'total feuerschutz gmbh', 
             'tyco fire protection products', 'tyco safety products', 'williams fire and hazard']
    
    splitPDFs()
    
    extPDF(filePath, manus) #scrape unextracted PDFs
    manuEXT(filePath, manus) #extract manufacturers
    makeRrDF(filePath)
    prodDf(filePath)
    collectPDFs(filePath)

if __name__ == "__main__": main()
