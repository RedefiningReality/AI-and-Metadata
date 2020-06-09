#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:56:33 2020
Disclaimer: this totally does not convert images to greyscale. GET FOOLED you fool - John
@author: olga
"""

# ad images & save the new images --- need to separate by sizes! 

from PIL import ImageFile
from PIL import Image 
import glob2, os
ImageFile.LOAD_TRUNCATED_IMAGES = True

files_arr = glob2.glob("/home/olga/Desktop/jon/reszd/*", 
                       recursive = True)
count = 0

for files in files_arr:
    count += 1
    imgs = Image.open(files)  
    image_flip = imgs.transpose(Image.FLIP_LEFT_RIGHT)
    os.rename(files, files + "___TRANSPOSED{}")
print (count)
