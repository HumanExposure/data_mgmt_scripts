import os
from glob import glob

os.chdir(r'C:\Users\alarger\OneDrive - Environmental Protection Agency (EPA)\Profile\Documents\P&G\P&G pro')

htmls = glob("*.html")
pdfs = glob("*.pdf")
file_list = []
for f in htmls:
    if f.replace('.html','.pdf') in pdfs:
        continue
    else: 
        file_list.append(f)

execfile = "wkhtmltopdf.exe"
execpath = 'C:\\Users\\alarger\\Documents\\wkhtmltopdf\\bin\\'

i=0
for file in file_list:
    i+=1
    print(i)
    newName = file.replace('.html','.pdf')
    cmd = os.path.join(execpath,execfile)
    cmd = " ".join([cmd,'--disable-external-links','--disable-internal-links','--disable-javascript',file,newName])
    os.system(cmd)