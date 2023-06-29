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

# %% Extract composition data from PDFs
def extPDF(filepath):
    extdfs = {}
    failed = []

    pdfs = glob(filepath + r'docs/' + '*pdf')
    
    for pdf in pdfs:
        fname = pdf.split('\\')[-1]
        
        try:                           
            dfs = tb.read_pdf(pdf, pages='all', silent=True, lattice = False)
            
            compdf = False
            
            for i, df in enumerate(dfs):
                if len([col for col in df.columns if 'cas' in cleanLine(str(col))]) > 0:
                    tempdf = df
                    compdf = True
                    if compdf == True: break
            
            df = tempdf.dropna(axis=1, how='all').dropna(axis=0, how='all')
            
            if '001200.pdf' in pdf:
                text = list(filter(None, pdfparser(pdf).split('\n')))
                for i, line in enumerate(text):
                    if 'section 3:' in cleanLine(line) or 'section 3-' in cleanLine(line):
                        start = i+1
                        
                stop = next(i for i in range(len(text)) if "section 4" in cleanLine(text[i]))
                sec3 = text[start:stop]
                df = pd.DataFrame({'chem':sec3[1:4], 'comp':sec3[9:], 'cas':sec3[5:8]})
                
            if len(df.columns) == 3:
                df.rename(columns={ df.columns[0]: 'chem', df.columns[1]: 'comp', df.columns[2]: 'cas' }, inplace = True)
                # break merged chemicals into separate entries
                if len(df) == 1 and '\r' in df.chem[0]:
                    df = pd.DataFrame({'chem':df.chem[0].split('\r'), 'comp':df.comp[0].split('\r'), 'cas':df.cas[0].split('\r')})
                extdfs.update({fname:df})
            else: print(fname)
            
        except:
            failed.append(fname)
    
    return extdfs
# %%
def extCSV(filepath, extPDFs):
    
    fnames = []
    prodnames = []
    recuses = []
    dates = []
    revnums = []
    ranks = []
    
    chems = []
    casnums = []
    mins = []
    cents = []
    maxs = []
    
    for key, value in extPDFs.items():
            
        pdf = filepath + r'docs/' + key
        fname = key
        df = value.reset_index(drop=True)

        text = list(filter(None, pdfparser(pdf).split('\n')))
    
        prodname = cleanLine(text[1])
        
        recuse = 'synthetic/analytical chemistry' #standardized use
        date = ''
        revnum = ''
        
        for i, line in enumerate(text):
            if 'date of issue' in cleanLine(line) and date == '':
                date = cleanLine(text[i+1].split(': ')[1].strip('.').split('.')[0])
            if 'version :' in cleanLine(line) and revnum == '':
                revnum = cleanLine(line.split('Version : ')[1])
            if '001200.pdf' in pdf:
                date = 'may 7, 2015'
                revnum = ''
        
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
                comp = str(row[1])
                cas = str(row[2])
                    
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
                revnums.append(cleanLine(revnum))
                
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
            revnums.append(cleanLine(revnum))
    
    # Create the ranks
    ranks = []
    names = []
    [names.append(x) for x in fnames if x not in names]
    for name in names:
        ranks.extend([*range(1,(fnames.count(name)+1))])
    
    extDF = pd.DataFrame({'data_document_id':fnames, 'data_document_filename':fnames, 
                          'prod_name':prodnames, 'report_funcuse':['']*len(chems), 
                          'component':['']*len(chems), 'doc_date':dates, 'rev_num':revnums, 
                          'ingredient_rank':ranks, 'raw_chem_name':chems, 'raw_cas':casnums, 
                          'raw_min_comp':mins, 'raw_central_comp':cents, 'raw_max_comp':maxs, 
                          'raw_category':recuses, 'unit_type':['3']*len(chems)})
    
    # some final cleanups
    i = extDF[extDF['raw_chem_name'] == 'nan'].index
    extDF.drop(i, inplace = True)
    extDF = extDF.fillna('')
    
    return extDF

# %% Create full Extracted Text CSV
def makeExtCSV(filepath, extDF): 
    
    try:
        rridDF = pd.read_csv(filepath + 'Factotum_Airgas_PureGas_registered_documents_20230307.csv')
        file2id = dict(zip(rridDF['filename'], rridDF['DataDocument_id']))
    
        extDF['data_document_id'] = extDF.data_document_id.replace(file2id)
    except: print('Documents not yet registered.')
    
    # convert all values to strings and clean up decimals from unwanted floats
    columns = list(extDF.columns)
    for column in columns: # Clean up data types and unintentional floats
        extDF[column] = extDF[column].astype(str)
    
    extDF.to_csv(filepath + 'airgas-pure_extracted-text.csv',index=False, header=True)
    
# %% Registered Record CSV
# def rrCSV(filepath, extDF):
#     doctype = ['SD'] * len(extDF['data_document_filename'])
#     urls = ['https://www.antiseize.com/alphabetically-msds'] * len(extDF['data_document_filename'])
#     blanks = [''] * len(extDF['data_document_filename'])
    
#     rrDF = pd.DataFrame({'filename':extDF['data_document_filename'], 'title':extDF['prod_name'], 
#                           'document_type':doctype, 'url':urls, 'organization':extDF['suppliers'], 
#                           'subtitle':blanks, 'epa_reg_number':blanks, 'pmid':blanks, 
#                           'hero_id':blanks})
    
#     rrDF['title'] = rrDF['title'].apply(cleanLine)
#     rrDF = rrDF.drop_duplicates().reset_index(drop=True)
#     rrDF.to_csv(filepath + 'antiseize-registered-records.csv', index=False, header=True)

# %% Product Data CSV
# def prodCSV(filepath):
#     productsDF = pd.read_csv(filepath + 'product_csv_template_938.csv')
#     blanks = [''] * len(productsDF['data_document_filename'])
#     urls = ['https://www.antiseize.com/alphabetically-msds'] * len(productsDF['data_document_filename'])


#     productsDF = pd.DataFrame({'data_document_id':productsDF['data_document_id'], 
#                                 'data_document_filename':productsDF['data_document_filename'], 
#                                 'title':productsDF['data_document_filename'], 'upc':blanks, 'url':urls, 
#                                 'brand_name':blanks, 'size':blanks, 'color':blanks, 
#                                 'item_id':blanks, 'parent_item_id':blanks, 'short_description':blanks, 
#                                 'long_description':blanks, 'epa_reg_number':blanks, 
#                                 'thumb_image':blanks, 'medium_image':blanks, 'large_image':blanks, 
#                                 'model_number':blanks, 'manufacturer':productsDF['data_document_filename'], 
#                                 'image_name':blanks})
    
#     rrDF = pd.read_csv(filepath + 'anti-seize_technologies_registered_documents.csv')
#     file2title = dict(zip(rrDF['filename'], rrDF['title']))
#     file2manu = dict(zip(rrDF['filename'], rrDF['organization']))
    
#     productsDF['title'] = productsDF.title.replace(file2title)
#     productsDF['manufacturer'] = productsDF.manufacturer.replace(file2manu)
    
#     productsDF.to_csv(filepath + 'antiseize-products.csv', index=False, header=True)

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
filepath = r'C:/Users/mhorton/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Airgas/Pure/'

startTime = datetime.now()

extPDFs = extPDF(filepath) #scrape unextracted PDFs
extDF = extCSV(filepath, extPDFs)
makeExtCSV(filepath, extDF)
# rrCSV(filepath, extDF)
# prodCSV(filepath)

endTime = datetime.now()
print('Time: ', endTime - startTime)

# %%
# if __name__ == "__main__": main()