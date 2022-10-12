# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 08:49:52 2019

@author: ALarger

Splits folder of pdfs into multiple folders with 600 pdfs each to be uploaded to factotum
"""

import os
from glob import glob
from shutil import copyfile

path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/Scraping/Chemours SDS'
path = path+'/'
os.chdir(path)
pdfs = glob("*.pdf")

i = 0
j = 0
for pdf in pdfs:
    if j%600 == 0:
        i += 1
        newFolder = path + 'pdfs' + str(i)
        os.mkdir(newFolder)
    j += 1
    oldPath = path + pdf
    newPath = newFolder + '\\' + pdf
    copyfile(oldPath,newPath)

