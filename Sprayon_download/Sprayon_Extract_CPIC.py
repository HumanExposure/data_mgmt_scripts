"""
Created on Tue Jul 14 18:34:32 2020

@author: SHanda
"""

#import packages 
import os, string, csv, re
import pandas as pd
from glob import glob


def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = 'C:\\Users\\SHanda\\xpdf-tools-win-4.02\\bin64\\' #path to xpdf tools 
    
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

def splitLine(line):
    """
    cleans line and splits it into a list of elements for extracting tables
    """
    clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty))
    sline = clean(line.replace('–','-'))
    sline = sline.lower() #lowercase
    sline = sline.strip() #removes extra space
    sline = sline.split("  ") #splits on doublespace, creates indexed list
    sline = [x.strip() for x in sline if x != ""] #removes extra space if not an empty string
    
    return(sline)


def extractData(fileList):
    """
    Extracts data from txt files into a pandas dataframe, 
    then generates a csv to upload into factotum
    file_list: a list of the txt file names in the data group
    """
    idList = [] #Factotum document IDs
    filenameList = [] #file names
    prodnameList = [] #product names
    dateList = [] #sds dates
    revList = [] #revision numbers
    catList = [] #product categories
    casList = [] #CAS numbers
    chemList = [] #chemical names
    useList = [] #functional uses of each chemical
    minList = [] #minimum concentrations
    maxList = [] #maximum concentrations
    unitList = [] #unit type codes (1=weight frac, 2=unknown, 3=weight percent,...)
    rankList = [] #ingredient ranks
    centList = [] #central concentrations
    componentList = [] #components
    
    for file in fileList:
        ifile = open(file, encoding = 'utf8')
        prodname = ''
        date = ''
        rev = ''
        cat = ''
        ID = ''
        use = []  #''
        component = ''
        chem = []
        cas = []
        minC = []
        maxC = []
        centC = []
        unit = []
        
                     
        inIngredients = False #Flag for if you are in the ingredients section
        inDate = False # Flag for date section of CPIC
        
        #Get Factotum IDs
        #csv downloaded from Factotum using the "Document records" button on the datagroup page
        docRecords = csv.reader(open('sprayon_cpic_documents_20200717.csv')) 
        for row in docRecords:
            if row[6] == file.replace('.txt','.pdf'): #find the filename column, convert to txt file
                ID = row[0] # finds ID column
                break
        if ID == '': #move on when you reach end of IDs
            continue
                    
        for line in ifile:
            cline = cleanLine(line)
            if cline == '': continue #Skip blank lines
                
            #Get product/document data
            if  'product name' in cline and prodname == '': #finds product name in line
                prodname = cline.split('   ')[-1].strip('').replace('product name', '') # extract product name
            
            #get date
            if 'date of preparation' in cline and date == '':
                inDate = True
                continue
            
            if inDate == True and cline != '':
                date = cline  # extract date (second line after date)
                inDate = False

            #Get ingredient data
            if inIngredients == True:
                #conc = ''
                sline = splitLine(line) #split line into a list of elements
                if 'the consumer products' in cline: #look for keyword after table
                    inIngredients = False #out of ingredients section
                    
                elif len(sline) == 3: #if the line has three elements, they are cas, ingredient name, and function
                    cas.append(sline[0]) # CAS number
                    chem.append(sline[1]) #ingredient name
                    use.append(sline[2]) # functional use
                    minC.append('')
                    maxC.append('')
                    centC.append('')
                    unit.append('')
                    
                else:
                    print(len(sline),sline, file) #if not categorized properly, return chemical line here
                    
            if 'cas number' in cline and 'chemical name' and 'function' in cline: #look for these keywords in ingredients table
                inIngredients = True
                
        if chem == []: #if a document has no chemicals in it, leave all chemical related fields blank
            chem = ['']
            cas = ['']
            use = ['']
            minC = ['']
            maxC = ['']
            centC = ['']
            unit = ['']
            
        #add the data from this document to the 
        n = len(chem)
        idList.extend([ID]*n)
        filenameList.extend([file.replace('.txt','.pdf')]*n)
        prodnameList.extend([prodname]*n)
        dateList.extend([date]*n)
        revList.extend([rev]*n)
        catList.extend([cat]*n)
        casList.extend(cas)
        chemList.extend(chem)
        useList.extend(use)
        minList.extend(minC)
        maxList.extend(maxC)
        unitList.extend(unit)
        centList.extend(centC)
        componentList.extend([component]*n)
        #add rank
        if chem == ['']:
            rankList.extend([''])
        else:
            rankList.extend(list(range(1,n+1)))
   
    #create csv
    df = pd.DataFrame({'data_document_id':idList, 'data_document_filename':filenameList, 'prod_name':prodnameList, 'doc_date':dateList, 'rev_num':revList, 'raw_category':catList, 'raw_cas':casList, 'raw_chem_name':chemList, 'report_funcuse':useList, 'raw_min_comp': minList, 'raw_max_comp':maxList, 'unit_type':unitList, 'ingredient_rank':rankList, 'raw_central_comp':centList, 'component':componentList})
    df.to_csv(r'Sprayon CPIC Extracted Text.csv',index=False, header=True) #create a new csv to write extracted data
    
    
def main():
    os.chdir(r'L:\Lab\HEM\Shanda\Sprayon') #Folder pdfs are in
    pdfs = glob("*.pdf")
    nPdfs = len(pdfs)
    nTxts = len(glob("*.txt"))
    if (nTxts < nPdfs): pdfToText(pdfs)
    
    nTxts = len(glob("*.txt"))
    if (nTxts == nPdfs):
       fileList = glob("*.txt")       
       extractData(fileList)    


if __name__ == "__main__": main()
