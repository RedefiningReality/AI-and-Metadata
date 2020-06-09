#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:25:08 2020

@author: olga
"""

from PIL import Image, ImageFile
import glob2, os
ImageFile.LOAD_TRUNCATED_IMAGES = True

directory = glob2.glob("/home/lena/vien/alphad/alpha/*", 
                       recursive = True)
count = 0

for files in directory:
    count += 1
    orig_img = Image.open(files)  # the orig images
    region = orig_img.crop((100 ,50, 150, 100))
    orig_img.paste(region, (50, 50, 100, 100))
    os.rename(files, files + " moves.png")
    print ("i am going through another loop")
    continue
else:
    print ("another loop NOT entered")
print ("num images found:  ", count)

"""
# pasting 1 part of image to another
im = Image.open("/home/lena/vien/alphad/alpha/gt_11275.png_faked_")
region = im.crop((100, 50, 150, 100))

im.paste(region, (50, 50, 100, 100))
im.save("pasted.region.png")
"""


