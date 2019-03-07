#author: Lauren Koval
#date: 3-17-19

from tabula import read_pdf
import pandas as pd
import os, string, csv
import glob

path="//home//lkoval//clorox"    #path to where all pdfs are stored
fileListPDF= glob.glob(os.path.join(path, '*.pdf')) #creates list of all pdfs
execfile="pdftotext" #pdftotext application
execpath="//home//lkoval//xpdf-tools-linux-4.01//bin64" #pdftotext application path

for file in fileListPDF:#Run pdftotext application on all the pdfs
    pdf=""+file+""
    cmd=os.path.join(execpath,execfile)
    cmd=" ".join([cmd,"-nopgbrk","-table",pdf])
    os.system(cmd)

clean = lambda dirty: ''.join(filter(string.printable.__contains__, dirty)) #clean function
fileListTXT= glob.glob(os.path.join(path, '*.txt')) #creates a list of the text files that were created from pdftotext application.

#First get issue date, revision date, revision number, prod name, epa registration
#number, and recommended use from the text files
for filetxt in fileListTXT:#
    ifile=open(filetxt, encoding='cp1252') #some characters were not utf-8 so encoding is now Windows-1252 which seems to work
    product_temp=[] #empty list to store product info

    j=0 #sets counter to track the number of times the revision date appears

    for line in ifile:#cleans each line in the file unless it is a new line
        if line=='\n': continue
        cline=clean(line)
        cline=cline.lower()
        cline=cline.replace(',','_')
        cline=cline.replace(';','_')
        cline=cline.strip()
        cline=cline.split(" ")
        cline = [x.strip() for x in cline if x != ""]

        for i in range(0, len(cline)):#for each word in the line
            if cline[i]=="issuing" and cline[i+1]=="date":#gets issue date and appends to temp storage list
                date_list=[]
                date_list.append(cline[i+2])
                date_list.append(cline[i+3].replace('_', ','))
                date_list.append(cline[i+4])
                date= " ".join(date_list)
                product_temp.append(date)

            if cline[i]=="revision" and cline[i+1]=="date":#only if it is the first appearance of the revision, it is appended to temp storage list
                if j<1:
                    if cline[i+2]=="new" or cline[i+2]=="revision":
                        product_temp.append(None)
                    else:
                        date_list=[]
                        date_list.append(cline[i+2])
                        date_list.append(cline[i+3].replace('_', ','))
                        date_list.append(cline[i+4])
                        date= " ".join(date_list)
                        product_temp.append(date)

                    j+=1

            if cline[i]=="revision" and cline[i+1]=="number":#gets the revision number and appends to temp storage list
                product_temp.append(cline[i+2])

            if cline[i]=="product" and cline[i+1]=="name":#gets the product name, removes trademark symbol, and appends to storage list
                p=cline[i+2:]
                product=' '.join(p)
                product=product.replace("tm",'')
                product_temp.append(product)

            if cline[i]=="epa" and cline[i+1]=="registration":#gets the epa registration number if it exists and appends to temp storage list else none value is appeneded
                product_temp.append(cline[i+3])

            elif cline[i]=="synonyms":
                product_temp.append(None)

            if (cline[i]=="recommended" and cline[i+1]=="use") and cline[i+2]!="of":#gets recommened use and appends to temp storage list
                use_list=cline[i+2:]
                use=' '.join(use_list)
                use=use.replace('_',",")
                product_temp.append(use)

#Next get chemical composition info from pdfs with tabula
    count=1 #creates counter to count number of tables in pdf
    for filepdf in fileListPDF:#for each of the pdfs in the pdf list
        filepdf_temp=filepdf.strip(".pdf")
        filetxt=filetxt.strip(".txt")
        if filepdf_temp==filetxt:#checks to make sure the correct pdf is being read by comparing to the current text file
            tables=read_pdf(filepdf, pages="all",  multiple_tables= True, pandas_options={'header': None})     #reads all the pages of the pdf for all tables as pandas dateframes
            for x in range(0,len(tables)):#For each table in the pdf
                if len(tables[x].columns)== 4:#Tests to see if each table has 4 columns and if it does the column headers are cleaned due to observed inconsistencies in the pdfs, else the counter is updated
                    chem_col=tables[x][0][0].strip().lower().replace('-','').replace('.','').replace(' ','').replace(',','')
                    cas_col=tables[x][1][0].strip().lower().replace('-','').replace('.','').replace(' ','').replace(',','')
                    weight_col=tables[x][2][0].strip().lower().replace('-','').replace('.','').replace(' ','').replace(',','')
                    trade_col=tables[x][3][0].strip().lower().replace('-','').replace('.','').replace(' ','').replace(',','')
                    if chem_col=="chemicalname" and cas_col=="casno" and weight_col=="weight%" and trade_col=="tradesecret":#if the column headers match than we have the correct table. That table is stored as our df.
                        df=tables[x]
                        df=df.drop(df.columns[3], axis=1)   #drops trade secret column
                        df=df.drop(df.index[0]) #drop row of headers
                        break

                    else:
                        continue
                else:
                    count+=1
                if count==len(tables):#If the count is equal to the number of tables, ie all tables have been checked, the table we want was not identified
                    print("Checked %d out of %d identified tables" %(count,len(tables)))
                    df=pd.DataFrame()

            if df.empty==False:#If the correct table is identified, parse table for values; else print error statement
                i=1     #creates an index counter
                while i< len(df.index):# Runs while index is less than the number of rows in the table
                    if pd.isnull(df.iloc[i,0])==False and (pd.isnull(df.iloc[i, 1]) and pd.isnull(df.iloc[i, 2]))==False:#If the row is not missing any fields increment to test the next row.
                        i+=1
                    elif pd.isnull(df.iloc[i+1,0])== True and (pd.isnull(df.iloc[i+1,1]) and pd.isnull(df.iloc[i+1,2]))==False:#If CAS is missing, check if the next row has CAS & weight but is missing name
                        if pd.isnull(df.iloc[i+2,0])== False and (pd.isnull(df.iloc[i+2,1]) and pd.isnull(df.iloc[i+2,2]))==True:#If name is missing but CAS and weight are present, check next line to see if name is present but CAS and weight are missing. If so those three lines are one entry in the table that was split up. Increment up to the next unchecked row.
                            corrected_name=df.iloc[i,0]+" "+df.iloc[i+2,0] # combines the split names into one name
                            df.iloc[i,0]=corrected_name #assigns the corrected name to the correct location
                            df.iloc[i,1]=df.iloc[i+1,1] #assigns the misplaced CAS to the correct location
                            df.iloc[i,2]=df.iloc[i+1,2] #assigns the misplaced weight percentages to the correct location
                            i+=3 #moves up the index up to check the next unchecked row
                    else:
                        print("something has gone wrong parsing composition info for file %s"%file)
                        break

                df=df.dropna() #after the df has been corrected, all the incorrect rows are removed

                df=df.assign(i_d= product_temp[0], r_d=product_temp[1], r_n=product_temp[2], p_n=product_temp[3], e_r_n=product_temp[4], r_u=product_temp[5])   #Add all the other information stored in the temp storage list to our df

            #if the file does not exist, it is created and the df for the first product
            #is written to it; else the product's df is appended to the existing file.
                if os.path.isfile("clorox.csv")==True:
                    df.to_csv("clorox.csv", index=False, header= False, mode='a')
                else:
                    df.to_csv("clorox.csv", index=False, header=["chemical name", "CAS-No", "weight percentage", "issue date", "revision date", "revision number", "product name", "EPA registration number", "recommended use"] , mode='w')

            else:
                print("check tables for file %s. Composition table not found."%file)
