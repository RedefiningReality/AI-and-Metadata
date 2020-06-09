#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:47:16 2020

@author: olga
"""
# just rotate images & save the new images --- need to separate by sizes! 
# 3 categories, so make 1 rotate, another black & white etc

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
    imgs_rot67 = imgs.rotate(67)
    os.rename(files, files + "___rot67{}")
print (count)

