import os
import subprocess
from tqdm import tqdm

# specify the path to the pdfs
path = r"C:\Users\mmetcalf\Documents and Scripts\State Industrial\SDS Files"

def pdfToText(files):
    """
    Converts pdf files into text files
    files: list of filenames
    """
    execfile = "pdftotext.exe"
    execpath = r'C:\Users\mmetcalf\OneDrive - Environmental Protection Agency (EPA)\Profile\Desktop\xpdf-tools-win-4.04\bin64' #Path to execfile
    for file in tqdm(files):
        pdf = file
        cmd = os.path.join(execpath,execfile)
        subprocess.run([cmd,"-nopgbrk","-table", "-enc", "UTF-8",pdf]) 
    return

# get a list of all pdf files in the specified directory
pdf_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.pdf')]

# call the function with the list of pdf files
pdfToText(pdf_files)
