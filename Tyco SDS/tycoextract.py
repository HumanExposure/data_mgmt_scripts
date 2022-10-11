# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:42:12 2022

@author: MHORTON
"""

import string, re, math
import glob

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

# %%
filePath = 'C:\\Users\\mhorton\\OneDrive - Environmental Protection Agency (EPA)\\Profile\\Documents\\TycoSDS\\'

pdfs = glob.glob(filePath + 'pdfs\\*.pdf')

manus = ['chemguard', 'fln feuerlschgerte', 'hart and cooley', 'johnson controls', 
         'macron safety systems (uk)', 'sabo foam s.r.l.', 'total feuerschutz gmbh', 
         'tyco fire protection products', 'tyco safety products', 'williams fire and hazard']

# # %% retrieve previously scraped data
# import json

# with open(filePath + "fnames.json", 'r') as f:
#     fnames = json.load(f)
# with open(filePath + "prodnames.json", 'r') as f:
#     prodnames = json.load(f)
# with open(filePath + "recuses.json", 'r') as f:
#     recuses = json.load(f)
# with open(filePath + "suppliers.json", 'r') as f:
#     suppliers = json.load(f)
# with open(filePath + "dates.json", 'r') as f:
#     dates = json.load(f)
# with open(filePath + "versions.json", 'r') as f:
#     versions = json.load(f)
# with open(filePath + "ranks.json", 'r') as f:
#     ranks = json.load(f)
    
# with open(filePath + "chems.json", 'r') as f:
#     chems = json.load(f)
# with open(filePath + "casnums.json", 'r') as f:
#     casnums = json.load(f)
# with open(filePath + "mins.json", 'r') as f:
#     mins = json.load(f)
# with open(filePath + "cents.json", 'r') as f:
#     cents = json.load(f)
# with open(filePath + "maxs.json", 'r') as f:
#     maxs = json.load(f)  

# # %% dump scraped data so it is not lost
# import json

# with open(filePath + "fnames.json", 'w') as f:
#     json.dump(fnames, f)
# with open(filePath + "prodnames.json", 'w') as f:
#     json.dump(prodnames, f)
# with open(filePath + "recuses.json", 'w') as f:
#     json.dump(recuses, f)
# with open(filePath + "suppliers.json", 'w') as f:
#     json.dump(suppliers, f)
# with open(filePath + "dates.json", 'w') as f:
#     json.dump(dates, f)
# with open(filePath + "versions.json", 'w') as f:
#     json.dump(versions, f)
# with open(filePath + "ranks.json", 'w') as f:
#     json.dump(ranks, f)
    
# with open(filePath + "chems.json", 'w') as f:
#     json.dump(chems, f)
# with open(filePath + "casnums.json", 'w') as f:
#     json.dump(casnums, f)
# with open(filePath + "mins.json", 'w') as f:
#     json.dump(mins, f)
# with open(filePath + "cents.json", 'w') as f:
#     json.dump(cents, f)
# with open(filePath + "maxs.json", 'w') as f:
#     json.dump(maxs, f)    

# # %% check files that weren't scraped
# scraped = [*set(fnames)]

# dls = []

# for pdf in pdfs:
#     pdf = pdf.split('\\')[-1]
#     dls.append(pdf)


# remaining = list(set(dls)-set(scraped))

# %%
fnames = []
prodnames = []
recuses = []
suppliers = []
dates = []
versions = []
ranks = []

chems = []
casnums = []
mins = []
cents = []
maxs = []

# %%

startTime = datetime.now()

errors = []
for pdf in pdfs[0:20]:
    if pdf.split('\\')[-1] in fnames:
        print(pdf.split('\\')[-1], 'already extracted.')
    else:
        fname = pdf.split('\\')[-1]
        try:
            text = list(filter(None, extract_text(pdf).split('\n')))
            
            prodname = ''
            recuse = ''
            supplier = ''
            date = ''
            version = ''
            
            print('Extracting text for', pdf.split('\\')[-1])
            
            for i, line in enumerate(text):
                if 'product name ' in cleanLine(line) and prodname == '':
                    prodname = cleanLine(line.split('name ')[1])
                if 'recommended use' == cleanLine(line):
                    recuse = cleanLine(text[i+2]).strip('.')
                for j, manufacturer in enumerate(manus):
                    if manufacturer in cleanLine(line) and supplier == '':
                        supplier = manus[j]
                if 'revision date' in cleanLine(line) and date == '':
                    date = cleanLine(line.split('Revision date')[1])
                if 'version' in cleanLine(line) and version == '':
                    version = line.split(' ')[-1]
    
            print('Tabula extraction for', pdf.split('\\')[-1])
            
            dfs = tb.read_pdf(pdf, pages='all')
            compchems = []
            for df in dfs:
                if 'weight-%' in list(df.columns):    
                    chem = ''
                    cas = ''
                    low = ''
                    cent = ''
                    high = ''
                    for index, row in df.iterrows():
                        chem = row[0]
                        cas = row[1]
                        
                        # if the cas is nan, it is a continuation and we need to clean up the chemical name and continue
                        try:
                            if math.isnan(cas) is True:
                                chems[-1] = chems[-1] + chem
                                df = df.drop(index)
                                chemupdateslog = open(filePath + 'chemupdateslog.txt', 'a') #record to a log to check for issues
                                content = [fname, '\n', chems[-1], ' was updated\n\n']
                                chemupdateslog.writelines(content)
                                chemupdateslog.close()
                        except:
                            if '-' in row[2]: #if a range of weight%, assign min and max
                                low = row[2].split('-')[0].strip()
                                high = row[2].split('-')[1].strip()
                                cent = ''
                            else: #In the event there is not a range given
                                cent = row[2].strip()
                                low = ''
                                high = ''
                            
                            compchems.append(cleanLine(chem))
                            
                            fnames.append(fname)
                            chems.append(cleanLine(chem))
                            casnums.append(cleanLine(cas))
                            mins.append(cleanLine(low))
                            cents.append(cleanLine(cent))
                            maxs.append(cleanLine(high))
                        
                            prodnames.append(prodname)
                            recuses.append(recuse)
                            suppliers.append(supplier)
                            dates.append(date)
                            versions.append(version)
    
                else:
                    addchems = []
                    addcass = []
                    for df in dfs:
                        extrachems = []
                        
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
                            extrachems.extend(extrachem)
                        extrachems = [x for x in extrachems if str(x) != 'nan']
                        # print('extrachems', extrachems)
                    
                        for index, row in enumerate(extrachems):
                            if row.count('-') == 2 and bool(re.search('[a-zA-Z]', row)) == False: #Check if a row is probably a CAS number
                                addchem = cleanLine(extrachems[index - 1])
                                addcas = cleanLine(extrachems[index])
                                if addchem not in compchems and addchem not in addchems:
                                    addchems.append(addchem) 
                                    addcass.append(addcas)
                        # if len(addchems) > 0:
                            # print( len(addchems), 'addchems\n', addchems, '\n\n', len(addcass), 'addcass', addcass, '\n\n\n')
                        
            for i, c in enumerate(addchems):
                # print(i, c)
                fnames.append(fname)
                chems.append(c)
                casnums.append(addcass[i])
                mins.append(cleanLine(low))
                cents.append(cleanLine(cent))
                maxs.append(cleanLine(high))
            
                prodnames.append(prodname)
                recuses.append(recuse)
                suppliers.append(supplier)
                dates.append(date)
                versions.append(version)
            
            if len(list(range(1, len(compchems) + len(addchems)))) == 0:
                ranks.append('1')
            else:
                ranks.extend(list(range(1, len(compchems) + len(addchems) + 1)))
        except:
            print('Error extracting', pdf.split('\\')[-1])
            errors.append(pdf.split('\\')[-1]) # Errors: ['SILV-EXUS.pdf', 'TSTF55D.pdf', 'TEEX-500P.pdf', 'TWSOLAB.pdf']

endTime = datetime.now()
print('Extraction time: ', endTime - startTime)

# %%
rrdf = pd.DataFrame({'document_type':['MS']*len(fnames), 'filename':fnames, 'title':prodnames, 
                      'url':['https://tycosds.thewercs.com/external/private/search.aspx']*len(fnames), 
                      'organization':['tyco fire protection products']*len(fnames), 
                      'subtitle':['']*len(fnames), 'epa_reg_number':['']*len(fnames)}).drop_duplicates().reset_index(drop=True)


extdf = pd.DataFrame({'data_document_id':fnames, 'data_document_filename':fnames, 
                      'prod_name':prodnames, 'report_funcuse':recuses, 'component':['']*len(chems), 
                      'doc_date':dates, 'rev-num':versions, 'ingredient_rank':ranks, 
                      'raw_chem_name':chems, 'raw_cas':casnums, 'raw_min_comp':mins, 
                      'raw_central_comp':cents, 'raw_max_comp':maxs, 'raw_category':['']*len(chems), 
                      'unit_type':['3']*len(chems)})

