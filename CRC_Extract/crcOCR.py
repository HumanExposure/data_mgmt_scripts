# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 15:07:44 2019

@author: ALarger

Uses OCR to create text files from pdfs
"""

import os
from glob import glob
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

path = r'L:\Lab\HEM\ALarger\CRC\Mining' #Folder pdfs are in
os.chdir(path) 
config = r'--psm 4 -c preserve_interword_spaces=1'

pdfs = glob('*combined.pdf')
for p in pdfs:
    num = p.split('combined.pdf')[0]
    pages = convert_from_path(p,500, poppler_path = r"C:\Users\alarger\poppler-0.68.0\bin")
    image_counter = 1
    
    #Make jpeg of each page
    for page in pages: 
        filename = num+"page"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG') 
        image_counter = image_counter + 1
    filelimit = image_counter-1
    
    #Make text file
    outfile = num+'.txt'
    f = open(outfile, "a") 
      
    #Perform OCR on jpegs and write to text file 
    for i in range(1, filelimit + 1): 
        filename = num+"page"+str(i)+".jpg"
        text = str(((pytesseract.image_to_string(Image.open(filename), config = config))))    
        f.write(text) 
        f.write('\n')
    
    f.close() 
    
    #Delete jpegs
    jpgs = glob('*.jpg')
    for j in jpgs:
        os.remove(j)