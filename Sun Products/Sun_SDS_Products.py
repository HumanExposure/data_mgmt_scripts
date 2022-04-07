# -*- coding: utf-8 -*-
"""
Created on jan 11 2021

@author: SHanda
"""

#import packages 
import os, string, csv, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    Download xpdf here: https://www.xpdfreader.com/download.html
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\alarger\\xpdf-tools-win-4.03\\bin64\\' #Path to execfile
    for file in files:
        pdf = '"'+file+'"'
        cmd = os.path.join(execpath,execfile)
        cmd = " ".join([cmd,"-nopgbrk","-table", "-enc UTF-8",pdf])
        os.system(cmd)
        
    return

def cleanLine(line):
    """
    Takes in a line of text and cleans it
    removes non-ascii characters and excess spaces, and makes all characters lowercase
    
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    cline = clean(line.replace('–','-'))
    cline = cline.lower() #lowercase
    cline = re.sub(' +', ' ', cline) #replace + with space
    cline = cline.strip() #removes extra spaces
    
    return(cline)

def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    filenameList = []
    idList = []
    upcList = []
    urlList = []
    brandList = []
    sizeList = []
    colorList = []
    itemIdList = []
    parentList = []
    shortDescriptionList = []
    longDescriptionList = []
    eparegnoList = []
    thumbPicList = []
    mediumPicList = []
    largePicList = []
    modelNumberList = []
    manufList = []
    titleList = []
    picList = []
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        title= ''
        upc = ''
        brand = ''
        ID = ''
        size = ''
        itemid = ''
        inUPC = False
        
        #Get Factotum IDs
        #csv downloaded from Factotum using the "Document records" button on the datagroup page
        docRecords = csv.reader(open('product_csv_template_56.csv')) 
        for row in docRecords:
            if row[1] == file.replace('.txt','.pdf'): #find the filename column, convert to txt file
                ID = row[0] # finds ID column
                break
        if ID == '': #move on when you reach end of IDs
            continue
                    
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue #Skip blank lines
                
            #Get product/document data
            if  ('product label name' in cline or 'product generic name' in cline) and title == '': #finds product name in line
                title = cline.split('  ')[-1].replace('product label name', '').replace('product generic name', '').strip() # extract product name 
                brand = title.split(' ')[0] # sets brand name as first word in product name

            #Get product code
            if 'product code' in cline and itemid == '':
                itemid = cline.split('product code')[-1].replace('product code', '').strip()
                if ',' in itemid: itemid = ''

            # get UPC code
            if inUPC == True:
                if any(x not in '1234567890 ,' for x in cline):
                    inUPC = False
                    continue
                upc = upc + cline
            
            if 'upc code(s)' in cline and upc == '':
                upc = cline.split('upc code(s)')[-1].strip()
                inUPC = True
        
        # Get size from product name    
        if 'oz' in title and size == '':
            size = title.split('oz')[-2].strip().split(' ')[-1]+' oz' # extract size
        elif 'lb' in title and size == '':
            size = title.split('lb')[-2].strip().split(' ')[-1]+' lb' # extract size            
        elif 'ct' in title and size == '':
            size = title.split('ct')[-2].strip().split(' ')[-1]+' ct' # extract size  
            if any(x not in '1234567890 ct' for x in size):
                size = ''
        elif 'kg' in title and size == '':
            size = title.split('kg')[-2].strip().split(' ')[-1]+' kg' # extract size    
            
        # get brand name (2 word)    
        if 'cuddle' in brand:
            brand = 'cuddle soft'
        elif 'all' in brand:
            brand = 'all'
        elif 'market' in brand:
            brand = "market basket"
        elif 'snuggle' in brand:
            brand = 'snuggle'
        elif 'soft' in brand:
            brand = "soft breeze"    
        elif 'sunlight' in brand:
            brand = 'sunlight'
        elif 'sun' in brand:
            brand = 'sun'
        elif 'surf' in brand:
            brand = 'surf'
        elif 'wisk' in brand:
            brand = 'wisk'
        else:  
            brand = ''
 
        if upc == 'not applicable': upc = ''
        upcs = upc.replace(' ',',').split(',')
        while('' in upcs) :
            upcs.remove('')
        if upcs == []: upcs = ['']
        n = len(upcs)
        idList.extend([ID]*n)
        filenameList.extend([file]*n)
        titleList.extend([title]*n)
        upcList.extend(upcs)
        urlList.extend(['']*n)
        brandList.extend([brand]*n)
        sizeList.extend([size]*n)
        colorList.extend(['']*n)
        itemIdList.extend(['']*n)
        parentList.extend(['']*n)
        shortDescriptionList.extend(['']*n)
        longDescriptionList.extend(['']*n)
        eparegnoList.extend(['']*n)
        thumbPicList.extend(['']*n)
        mediumPicList.extend(['']*n)
        largePicList.extend(['']*n)
        modelNumberList.extend([itemid]*n)
        manufList.extend(['Sun Products']*n)
        picList.extend(['']*n)
     
   
    #create csv
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'title':titleList, 'upc':upcList, 'url':urlList, 'brand_name':brandList, 'size':sizeList, 'color':colorList, 'item_id':itemIdList, 'parent_item_id':parentList, 'short_description':shortDescriptionList, 'long_description':longDescriptionList, 'epa_reg_number':eparegnoList, 'thumb_image':thumbPicList, 'medium_image':mediumPicList, 'large_image':largePicList, 'model_number':modelNumberList, 'manufacturer':manufList, 'image_name':picList})
    df.to_csv(r'Sun_SDS_Product_details.csv',index=False, header=True) #create a new csv to write extracted product data
    
    
def main():
    os.chdir(r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Sun SDS') #Folder pdfs are in
    #os.chdir(r'L:\Lab\HEM\Shanda\Sun') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()