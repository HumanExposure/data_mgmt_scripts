import os
from PyPDF2 import PdfFileMerger
from glob import glob

path = 'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/dollar general'
os.chdir(path)
sds = glob('*sds.pdf')
page = glob('*page.pdf')
done = glob('*combined.pdf')
for s in sds:
    # print(s)
    p = s.replace('sds','page')
    c = s.replace('sds','combined')
    if p in page and c not in done:
        try:
            merger = PdfFileMerger() 
            merger.append(s)
            merger.append(p)
            merger.write(c)
            merger.close()
        except:
            print('broken!',c)