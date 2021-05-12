# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:06:16 2020

@author: ALarger

Takes in a folder of images and resizes them to 180x180. 
If the images aren't square, white space will be added to the sizes to make them square.
"""

import os
from glob import glob
from PIL import Image

def resize(pic, width, height):
    '''
    Resize image keeping aspect ratio and using white background
    '''
    try:
        image_pil = Image.open(pic)
        ratio_w = width / image_pil.width
        ratio_h = height / image_pil.height
        if ratio_w < ratio_h: #Fix by width
            resize_width = width
            resize_height = round(ratio_w * image_pil.height)
        else: #Fix by height
            resize_width = round(ratio_h * image_pil.width)
            resize_height = height
        image_resize = image_pil.resize((resize_width, resize_height), Image.ANTIALIAS)
        background = Image.new('RGBA', (width, height), (255, 255, 255, 255))
        offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
        background.paste(image_resize, offset)
        background.save(pic)
    except: print(pic)
    return

def main():
    path = r'C:/Users/alarger/OneDrive - Environmental Protection Agency (EPA)/Profile/Documents/EWG Pics/Healthy Cleaning Pics' #Folder pics are in
    os.chdir(path)
    pics = glob('*.png')
    width = 180 #Desired width
    height = 180 #Desired height
    for pic in pics:
        resize(pic,width,height)

if __name__ == "__main__":
    main()
