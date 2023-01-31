
import string, re, time, random, requests, os
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen



# %% Line Cleaning Function
def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower()
    cline = re.sub(' +', ' ', cline)
    cline = re.sub(' &amp; ', ' ', cline)
    cline = cline.strip()
    return(cline)


# %% Filter dictionaries

def dictFilter(dictObj, filter_string, bool):
    newDict = dict()
    # Iterate over all the items in dictionary
    for (key, value) in dictObj.items():
        # Check if item satisfies the given condition then add to new dict
        if bool == True:
            if filter_string in value:
                newDict[key] = value
        elif bool == False:
            if filter_string not in value:
                newDict[key] = value
    return newDict



# %% Site Scraping PDFs List
def extSDS(site):
    
    global ps_pdfs
    
    site = 'https://www.perimeter-solutions.com/en/sds-index/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    
    soup_txt = print(soup)
    
    paras = soup.findAll("div", {"class": "td-content-wrapper"})
    
    hrefs = []
    
    for p in paras:
        if '.pdf"' in str(p):
            hrefs.append(str(p))
    
    url = []
    names = []
    pdfs = {}
    
    for h in hrefs:
        if '.pdf' in h:
            url = h.split('<a href="')[1].split('">')[0]
            name = h.split('.pdf">')[1].split('</a>')[0]    #.replace('</a>','').replace('</span>','')
            name = cleanLine(name)
            pdfs[url] = name
    
    
    
    only_en = dictFilter(pdfs, 'en', True)
    no_aus = dictFilter(only_en, 'aus', False)
    
    
    ps_pdfs = pd.DataFrame(no_aus.items())
    ps_pdfs[1] = ps_pdfs[1].str.replace(re.escape('(en)'),'')
    ps_pdfs[1] = ps_pdfs[1].str.replace(re.escape('safety data sheet '),'')
    ps_pdfs[1] = ps_pdfs[1].str.strip()


# %% Scraping Product Page Url's for Fire Retardants


def extFRurls(site):
    
    global needed_fire_retardants
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    
    soup_txt = print(soup)
    
    paras = soup.findAll("div", {"class": "td-content-wrapper"})
    
    hrefs = []
    
    for p in paras:
        if 'fire-safety-fire-retardants' in str(p):
            hrefs.append(str(p))
    
    
    url = []
    names = []
    products = {}
    
    for h in hrefs:
        if 'fire-safety' in h:
            url = h.split('<a href="')[1].split('">')[0]
            name = h.split('<strong>')[1].split('</strong>')[0]    #.replace('</a>','').replace('</span>','')
            name = cleanLine(name)
            products[url] = name
    
    
    filter_string = "ground"
    needed_fire_retardants = {k:v for (k,v) in products.items() if filter_string not in v}



# %% Scraping Product Page Url's for Class A Foams

def extCAFurls(site):
    
    global needed_class_a_foams
    
    
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(site,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, features="html.parser")
    
    soup_txt = print(soup)
    
    paras = soup.findAll("div", {"class": "td-content-wrapper"})
    
    hrefs = []
    
    for p in paras:
        if 'class-a-foam' in str(p):
            hrefs.append(str(p))
    
    ##
    
    
    print(hrefs)
    
    url = []
    names = []
    products = {}
    
    for h in hrefs:
        if 'class-a-foam' in h:
            url = h.split('<a href="')[1].split('">')[0]
            name = h.split('<strong>')[1].split('</strong>')[0]    #.replace('</a>','').replace('</span>','')
            name = cleanLine(name)
            products[url] = name
    
    
    filter_string = "solid"
    needed_class_a_foams = {k:v for (k,v) in products.items() if filter_string not in v}


# %% Main Execution and data manipulation 

filePath = r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Perimeter Solutions'


sds_site = 'https://www.perimeter-solutions.com/en/sds-index/'
FR_site = 'https://www.perimeter-solutions.com/en/fire-safety-fire-retardants/'
CAF_site = 'https://www.perimeter-solutions.com/en/class-a-foam/'

extSDS(sds_site)
extFRurls(FR_site)
extCAFurls(CAF_site)

print_pdfs = ps_pdfs
print_pdfs.set_index(0,inplace=True)
print_pdfs = pd.DataFrame.to_dict(print_pdfs)[1]



# %%Make Registered Records (move)

#reset index and name columns
ps_pdfs = ps_pdfs.reset_index()
ps_pdfs.columns = ['url', 'file_name']


os.chdir(r'C:\Users\CLUTZ01\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\Extraction Scripts\Perimeter Solutions')

#set up repeating variables
doctype = ['SD'] * len(ps_pdfs['file_name'])
blanks = [''] * len(ps_pdfs['file_name'])
organization = ['EPA'] * len(ps_pdfs['file_name'])


#creating needed fields
ps_pdfs['doctype'] = ['SD'] * len(ps_pdfs['file_name'])
ps_pdfs['title'] = ps_pdfs['file_name']
ps_pdfs['file_name'] = ps_pdfs['file_name']+'.pdf'

#compile into dataframe
rrDF = pd.DataFrame({'filename':ps_pdfs['file_name'], 'title':ps_pdfs['title'], 
                      'document_type':ps_pdfs['doctype'], 'url':ps_pdfs['url'], 'organization':organization, 
                      'subtitle':blanks, 'epa_reg_number':blanks, 'pmid':blanks, 
                      'hero_id':blanks})

#cleanup and export as csv
rrDF['title'] = rrDF['title'].apply(cleanLine)
rrDF = rrDF.drop_duplicates().reset_index(drop=True)
rrDF.to_csv('perimeter_solutions-registered-records.csv', index=False, header=True)




# %% Product Csv creation (move)

#merge fire retardants and foams
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res
product_urls = Merge(needed_fire_retardants, needed_class_a_foams)

product_urls_df = pd.DataFrame(product_urls.items())

#product_urls_df.to_csv('check names.csv', index=False, header=True)

product_urls_df = product_urls_df[[1,0]]
product_urls_df.columns = ['title', 'product_urls']


ps_pdfs['product_matching_key'] = ps_pdfs['title'].str.replace(re.escape(' (solution)'), '').str.replace(re.escape('a-fx'),'').str.replace(re.escape('a lc95a-mv'),'')
ps_pdfs['product_matching_key']


#ps_pdfs_wproducts  = ps_pdfs.merge(product_urls_df)

perimeter_df = pd.merge(
    left=ps_pdfs,
    right=product_urls_df,
    left_on='product_matching_key',
    right_on='title',
    how='left'
)

filePath = r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Perimeter Solutions/'

productsDF = pd.read_csv(filePath + 'product_csv_template_945.csv')
blanks = [''] * len(productsDF['data_document_filename'])
manu = ['Perimeter Solutions'] * len(productsDF['data_document_filename'])

template_e_products= pd.merge(
    left=productsDF,
    right=perimeter_df,
    left_on='data_document_filename',
    right_on='file_name',
    how='left'
)




products_DF = pd.DataFrame({'data_document_id':template_e_products['data_document_id'], 
                            'data_document_filename':template_e_products['data_document_filename'], 
                            'title':template_e_products['title_x'], 'upc':blanks, 'url':template_e_products['product_urls'], 
                            'brand_name':blanks, 'size':blanks, 'color':blanks, 
                            'item_id':blanks, 'parent_item_id':blanks, 'short_description':blanks, 
                            'long_description':blanks, 'epa_reg_number':blanks, 
                            'thumb_image':blanks, 'medium_image':blanks, 'large_image':blanks, 
                            'model_number':blanks, 'manufacturer':manu, 
                            'image_name':blanks})

products_DF.to_csv(filePath + 'perimeter-solutions-products.csv', index=False, header=True)

# %% Saving pdf's

path = r'C:/Users/CLUTZ01/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Extraction Scripts/Perimeter Solutions/pdfs/'

for k, value in print_pdfs.items():
    random.seed()
    wait = 6 + 3 * random.random()
    time.sleep(wait)
    response = requests.get(k)
    file = path + value + '.pdf'
    with open(file, 'wb') as f:
        f.write(response.content)

