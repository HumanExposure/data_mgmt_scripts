import os,sys
import glob,shutil

## Set working directory
# os.chdir("C:/Users/kphillip/Documents/Procter_and_Gamble_Ingredients/")

## Save working directory for reference
pwd = os.getcwd()

## Define the executable's path
execpath = "C:\\Users\\kphillip\\Documents\\InstalledExecutables\\"

## Define the executable
htmlexec = "pdftohtml.exe"
txtexec = "pdftotext.exe"

## Get all pdf files in current working directory
# files = glob.glob("PDFs/CleanedNames/*.pdf")
files = glob.glob("ScrapedFiles/PDFs/CleanedNames/*.pdf")

## Loop over all the pdf files
for f in files:

  # if file == files[0]:
    ## Get the name of the pdf file without a path
    # filename = os.path.join("ScrapedFiles//PDFs",os.path.basename(f))

    ## Get the name of the pdf file without an extension
    dirname = os.path.basename(f)[:-4]

    txtcmd = os.path.join(execpath,txtexec)

    ## Special options for reading and formatting a table (NOT ALWAYS NEEDED)
    txtcmd = " ".join([txtcmd,"-table","-nopgbrk",f])

    ## Print status to screen
    print dirname

    ## Execute the command
    os.system(txtcmd)

    ## Path to move the text file to
    textpath = os.path.join(pwd,"ScrapedFiles","PDFs","CleanedNames",dirname+".txt")
    if (os.path.isfile(textpath)):
        shutil.move(textpath,os.path.join(pwd,"ScrapedFiles","TXTs",dirname+".txt"))
    else:
        ## Throw an error if the path doesn't exist
        sys.exit("Path Not Found")
    sys.exit()
