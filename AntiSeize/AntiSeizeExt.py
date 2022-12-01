# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 12:01:11 2022

@author: MHORTON
"""

import string, re, io
from glob import glob
import tabula as tb
import pandas as pd

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from datetime import datetime

# %%
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-').replace('*',''))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = cline.strip()
    return(cline)

# %%
def pdfparser(data):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    with open(data, 'rb') as fp:
        for page in PDFPage.get_pages(fp,
                                      pagenos, 
                                      maxpages=maxpages,
                                      password=password,
                                      caching=caching,
                                      check_extractable=False):
            interpreter.process_page(page)

    # As pointed out in another answer, this goes outside the loop
    text = retstr.getvalue()

    device.close()
    retstr.close()
    return text

# %% Extract data from PDFs
def extPDF(filePath):
    extdfs = {}
    failed = []

    pdfs = glob(filePath + r'pdfs/' + '*pdf')
    
    for pdf in pdfs:
        fname = pdf.split('\\')[-1]
        
        try:
            text = list(filter(None, pdfparser(pdf).split('\n')))
            
            start = ''
            stop = ''
        
            for i, line in enumerate(text):
                if 'section 3:' in cleanLine(line) or 'section 3-' in cleanLine(line):
                    start = i+1
            
            stop = next(i for i in range(len(text)) if "section 4" in cleanLine(text[i]))
            sec3 = text[start:stop]
                
            numcas = 0
            for i, line in enumerate(sec3):
                output = re.sub(r'\d+', '', line).strip()
                if output == '--':
                    numcas += 1
                           
            dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = True)
            
            compdf = False
            
            for i, df in enumerate(dfs):
                if len([col for col in df.columns if 'cas' in cleanLine(str(col))]) > 0:
                    tempdf = df
                    compdf = True
                    dfindex = i
                    if compdf == True: break
                else:
                    if compdf == False:
                        if len(df) > 0:
                            row = df.loc[0, :].values.tolist()
                            row = ''.join(str(row))
                            row = cleanLine(row)
                            if 'cas' in row:
                                tempdf = df
                                compdf = True
                                dfindex = i
                            if compdf == True: break
    
            if compdf == False:
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                for i, df in enumerate(dfs):
                    if len([col for col in df.columns if 'section 3' in cleanLine(str(col))]) > 0:
                        tempdf = df
                        compdf = True
                        dfindex = i
                    if compdf == True: break
            
            df = tempdf.dropna(axis=1, how='all').dropna(axis=0, how='all')
            
            manual = ['m24300.pdf', 'm27084.pdf', 'm27085.pdf', 'm27086.pdf', 'm27088.pdf', 'm27089.pdf', 'm27104.pdf', 'm27105.pdf', 'm27107.pdf'] #exclude atypical pdfs
            if numcas > len(df) and fname not in manual:
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df1 = df
                df2 = dfs[dfindex + 1]
                df2 = pd.concat([df2.columns.to_frame().T, df2], ignore_index=True)
                if 'unnamed' in str(df2.iloc[0, 0]).lower():
                    df2 = df2.drop([df2.index[0]]).reset_index(drop=True)
                df2 = df2.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df2.rename(columns={ df2.columns[0]: 'chem', df2.columns[1]: 'cas', df2.columns[2]: 'comp' }, inplace = True)
                df = pd.concat( [df1, df2], axis=0, ignore_index=True)
            
            if len(df.columns) == 3:
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
            elif len(df.columns) == 2 and 'm17055.pdf' != fname:
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas' }, inplace = True)
                df = df.dropna(axis=0, how='all').reset_index(drop=True)
                df = df[~df['cas'].str.contains('cas',case=False)].reset_index(drop=True)
                df[['cas', 'comp']] = df['cas'].str.split(' ', 1, expand=True)
            
            # resolve extraction anomalies
            if fname == 'm17044.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[0]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
            if fname == 'm17047.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[0]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
            if fname == 'm17055.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[0]
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df['chem'][3] = 'Mineral oil, Petroleum Distillates, Hydrotreated ( mild) Heavy'
                df = df.drop([df.index[2]]).reset_index(drop=True)
            if fname == 'm24300.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 1', axis=1, inplace=True)
                df = df.drop([df.index[2], df.index[3], df.index[4]]).reset_index(drop=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df['cas'][0] = '63148-62-9'
                df['cas'][1] = '9002-84-0'
            if fname == 'm27082.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 2', axis=1, inplace=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df = df.drop([df.index[0], df.index[7], df.index[8]]).reset_index(drop=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
            if fname == 'm27084.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[7]
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                chem = df['chem'][0].split('\r')
                cas = df['cas'][0].split('\r')[:6]
                comp = df['comp'][0].split('\r')
                cas[0] = '4253-34-3'
                cas[1] = '17689-77-9'
                cas[2] = '7631-86-9'
                cas[4] = '64-19-7'
                comp[4] = '1-5'
                df = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
            if fname == 'm27085.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[7]
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                chem = df['chem'][0].split('\r')
                cas = df['cas'][0].split('\r')[:7]
                comp = df['comp'][0].split('\r')
                cas[0] = '4253-34-3'
                cas[1] = '17689-77-9'
                cas[2] = '7631-86-9'
                cas[5] = '64-19-7'
                comp[5] = '1-5'
                df = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
            if fname == 'm27086.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 1', axis=1, inplace=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
            if fname == 'm27088.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[7]
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                chem = df['chem'][0].split('\r')
                cas = df['cas'][0].split('\r')
                comp = df['comp'][0].split('\r')
                cas.pop(8)
                cas.pop(5)
                cas.pop(3)
                cas.pop(1)
                comp.pop(6)
                comp.pop(2)
                df = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
            if fname == 'm27089.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 1', axis=1, inplace=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
            if fname == 'm27104.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 1', axis=1, inplace=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df = df.drop([df.index[5], df.index[6]]).reset_index(drop=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
            if fname == 'm27105.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 1', axis=1, inplace=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df = df.drop([df.index[6], df.index[7]]).reset_index(drop=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
            if fname == 'm27106.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = True)
                df1 = dfs[7]
                df2 = list(dfs[8].columns)
                chem = df2[0].split('\r')
                cas = df2[1].split('\r')
                comp = df2[2].split('\r')
                df1.rename(columns={ df1.columns[0]: 'chem', df1.columns[1]: 'cas', df1.columns[2]: 'comp' }, inplace = True)
                df2 = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
                df = pd.concat( [df1, df2], axis=0, ignore_index=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
                df['comp'][4] = '0-0.1'
            if fname == 'm27107.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
                df = dfs[6]
                df = df.dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)
                df.drop('Unnamed: 1', axis=1, inplace=True)
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'cas', df.columns[2]: 'comp' }, inplace = True)
                df = df.drop([df.index[5], df.index[6]]).reset_index(drop=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
            if fname == 'm27108.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = True)
                df1 = dfs[7]
                df2 = list(dfs[8].columns)
                chem = df2[0].split('\r')
                cas = df2[1].split('\r')
                comp = df2[2].split('\r')
                df1.rename(columns={ df1.columns[0]: 'chem', df1.columns[1]: 'cas', df1.columns[2]: 'comp' }, inplace = True)
                df2 = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
                df = pd.concat( [df1, df2], axis=0, ignore_index=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
                df['comp'][4] = '0-0.1'
            if fname == 'm27109.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = True)
                df1 = dfs[7]
                df2 = list(dfs[8].columns)
                chem = df2[0].split('\r')
                cas = df2[1].split('\r')
                cas.pop(5)
                comp = df2[2].split('\r')
                df1.rename(columns={ df1.columns[0]: 'chem', df1.columns[1]: 'cas', df1.columns[2]: 'comp' }, inplace = True)
                df2 = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
                df = pd.concat( [df1, df2], axis=0, ignore_index=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
                df['comp'][4] = '0-0.1'
            if fname == 'm27110.pdf':
                dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = True)
                df1 = dfs[7]
                df2 = list(dfs[8].columns)
                chem = df2[0].split('\r')
                cas = df2[1].split('\r')
                comp = df2[2].split('\r')
                cas.pop(5)
                cas.pop(4)
                df1.rename(columns={ df1.columns[0]: 'chem', df1.columns[1]: 'cas', df1.columns[2]: 'comp' }, inplace = True)
                df2 = pd.DataFrame({'chem':chem, 'cas':cas, 'comp':comp})
                df = pd.concat( [df1, df2], axis=0, ignore_index=True)
                df['cas'][0] = '4253-34-3'
                df['cas'][1] = '17689-77-9'
                df['cas'][2] = '7631-86-9'
                df['cas'][4] = '64-19-7'
                df['comp'][4] = '0-0.1'
            if fname == 'm63000.pdf':
                df = df.drop([df.index[4]]).reset_index(drop=True)
                df['cas'][3] = ''
                df['comp'][3] = '2-10'
                
            extdfs.update({fname:df})
        except:
            failed.append(fname)
    
    return extdfs
# %%
def extCSV(extPDFs):
    
    fnames = []
    prodnames = []
    recuses = []
    dates = []
    ranks = []
    
    chems = []
    casnums = []
    mins = []
    cents = []
    maxs = []
    
    for key, value in extPDFs.items():
            
        pdf = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AntiSeize/pdfs/' + key
        fname = key
        df = value.reset_index(drop=True)

        text = list(filter(None, pdfparser(pdf).split('\n')))
    
        prodname = []
        try:
            	stop = next(i for i in range(len(text)) if 'safety data sheet' in cleanLine(text[i]))
            	prodname = text[:stop]
        except:
            	prodname = text
        
        prodname = cleanLine(' '.join(prodname))
        
        recuse = ''
        date = ''
        
        for i, line in enumerate(text):
            if 'product use' in cleanLine(line):
                recuse = cleanLine(line).replace('product use:', '').strip()
            if 'date' in cleanLine(line) and date == '':
                date = cleanLine(line.split(': ')[1])
        
        chem = ''
        cas = ''
        comp = ''
        low = ''
        cent = ''
        high = ''
        
        row = df.loc[0, :].values.tolist()
        row = ''.join(str(row))
        row = cleanLine(row)
        if 'cas' in row:
            df = df.drop([df.index[0]]).reset_index(drop=True)
        
        for index, row in df.iterrows():
            if len(row) == 3:
                chem = str(row[0])
                cas = str(row[1])
                comp = str(row[2])
                    
            # if the cas is nan, it is a continuation and we need to clean up the chemical name and continue
            if 'nan' in str(cas) and 'nan' in str(comp):
                try:
                    chems[-1] = chems[-1] + ', ' + chem
                    chem = ''
                except:
                    df['chem'][index+1] = chem + df['chem'][index+1]
                    df = df.drop([df.index[index]]).reset_index(drop=True)
                    
            elif 'nan' in str(cas):
                cas = ''
            elif 'nan' in str(comp):
                comp = ''
            elif 'secret' in comp:
                comp.replace('secret', '').strip()
            if cas == 'trade':
                cas = 'trade secret'
            if '-' in comp:
                low = comp.split('-')[0].strip().replace('%', '')
                high = comp.split('-')[1].strip().replace('%', '')
                cent = ''
            elif '<' in comp:
                low = '0'
                high = comp.split('<')[1].strip().replace('%', '')
                cent = ''
            elif 'trace' in comp:
                low = ''
                high = ''
                cent = ''
            else: 
                cent = comp.strip().replace('%', '')
                low = ''
                high = ''
                                
            if chem != '':
                fnames.append(fname)
                chems.append(cleanLine(chem))
                casnums.append(cleanLine(cas))
                mins.append(cleanLine(low))
                cents.append(cleanLine(cent))
                maxs.append(cleanLine(high))
            
                prodnames.append(cleanLine(prodname))
                recuses.append(cleanLine(recuse))
                dates.append(cleanLine(date))
                
        if chem == '':
            fnames.append(fname)
            chems.append('')
            casnums.append('')
            mins.append('')
            cents.append('')
            maxs.append('')

            prodnames.append(cleanLine(prodname))
            recuses.append(cleanLine(recuse))
            dates.append(cleanLine(date))
    
    # Create the ranks
    ranks = []
    names = []
    [names.append(x) for x in fnames if x not in names]
    for name in names:
        ranks.extend([*range(1,(fnames.count(name)+1))])
    
    extDF = pd.DataFrame({'data_document_id':fnames, 'data_document_filename':fnames, 
                          'prod_name':prodnames, 'report_funcuse':recuses, 'component':['']*len(chems), 
                          'doc_date':dates, 'rev_num':['']*len(chems), 'ingredient_rank':ranks, 
                          'raw_chem_name':chems, 'raw_cas':casnums, 'raw_min_comp':mins, 
                          'raw_central_comp':cents, 'raw_max_comp':maxs, 'raw_category':['']*len(chems), 
                          'unit_type':['3']*len(chems), 'suppliers':['anti-seize technology']*len(chems)})
    
    # some final cleanups
    i = extDF[extDF['raw_chem_name'] == 'nan'].index
    extDF.drop(i, inplace = True)
    
    extDF.to_csv(filePath + 'antiseize_extraction.csv', mode = 'a', index=False, header=False)
    return extDF

# %% Create full Extracted Text CSV
def makeExtCSV(filePath, extDF): 
    
    try:
        rridDF = pd.read_csv(filePath + 'tyco_fire_protection_products_thewercs_sds_registered_documents.csv')
        file2id = dict(zip(rridDF['filename'], rridDF['DataDocument_id']))
    
        extDF['data_document_id'] = extDF.data_document_id.replace(file2id)
    except: print('Documents not yet registered.')

    extDF = extDF.drop(['suppliers'], axis=1)
    
    # convert all values to strings and clean up unwanted decimals from unwanted floats
    columns = list(extDF.columns)
    for column in columns: # Clean up data types and unintentional floats
        extDF[column] = extDF[column].astype(str)
    
    extDF.to_csv(filePath + 'antiseize_extracted-text.csv',index=False, header=True)
    
    return extDF

# %% Registered Record CSV
def rrCSV(filePath, extDF):
    doctype = ['SD'] * len(extDF['data_document_filename'])
    urls = ['https://www.antiseize.com/alphabetically-msds'] * len(extDF['data_document_filename'])
    blanks = [''] * len(extDF['data_document_filename'])
    
    rrDF = pd.DataFrame({'filename':extDF['data_document_filename'], 'title':extDF['prod_name'], 
                          'document_type':doctype, 'url':urls, 'organization':extDF['suppliers'], 
                          'subtitle':blanks, 'epa_reg_number':blanks, 'pmid':blanks, 
                          'hero_id':blanks})
    
    rrDF['title'] = rrDF['title'].apply(cleanLine)
    rrDF = rrDF.drop_duplicates().reset_index(drop=True)
    rrDF.to_csv(filePath + 'antiseize-registered-records.csv', index=False, header=True)
    
    return rrDF

# %% Product Data CSV
def prodDf(filePath):
    productsDF = pd.read_csv(filePath + 'product_csv_template_934.csv')
    blanks = [''] * len(productsDF['data_document_filename'])
    urls = ['https://www.antiseize.com/alphabetically-msds'] * len(productsDF['data_document_filename'])


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
# def main():
filePath = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/AntiSeize/'

startTime = datetime.now()

extPDFs = extPDF(filePath) #scrape unextracted PDFs
extDF = extCSV(extPDFs)
makeExtCSV(filePath, extDF)
rrCSV(filePath, extDF)
# prodCSV(filePath)

endTime = datetime.now()
print('Time: ', endTime - startTime)

# %%
# if __name__ == "__main__": main()