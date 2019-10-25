# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:24:17 2019

@author: ALarger
"""

import os
from PyPDF2 import PdfFileMerger
from glob import glob

path = 'L:\Lab\HEM\ALarger\CRC\Automotive'
os.chdir(path)
sds = glob('*sds.pdf')
pds = glob('*pds.pdf')
for s in sds:
    print(s)
    p = s.replace('sds','pds')
    c = s.replace('sds','combined')
    if p in pds:
        merger = PdfFileMerger() 
        merger.append(s)
        merger.append(p)
        merger.write(c)
        merger.close()
        