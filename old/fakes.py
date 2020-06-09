#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:56:33 2020

@author: olga
"""
from PIL import Image
from PIL import ImageFile
import os, glob2

dir = glob2.glob("/home/lena/vien/alphad/alpha/*", recursive = True)

count = 0

for files in dir:
    count += 1
    im = Image.open(files)
    region = im.crop ((100, 50, 150, 100))
    im.paste(region, ((50, 50, 100, 100)))
    os.rename(files, files + "_pasted.png")
    continue
print (" num files done:  ", count)

   
"""
# pasting 1 part of image to another
im = Image.open("/home/lena/vien/alphad/alpha/gt_14007.png_faked_ moves.png")
region = im.crop((100, 50, 150, 100))

im.paste(region, (50, 50, 100, 100))
im.save("gt_14007pasted.region.png")
"""




