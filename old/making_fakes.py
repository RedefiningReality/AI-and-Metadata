#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 08:10:13 2020

@author: olga
"""
from PIL import ImageFile
from PIL import Image 
import glob2, os
ImageFile.LOAD_TRUNCATED_IMAGES = True

directory = glob2.glob("/home/lena/vien/alphad/alpha01/*", 
                       recursive = True)
count = 0

for files in directory:
    count += 1
    orig_img = Image.open(files)  # the orig images
    region = orig_img.crop((100,50, 150, 100))
    orig_img.paste(region, (50, 50, 100, 100))
    os.rename(files, files + "_fkthis2.png")
    print ("i am going through another loop")
    continue
else:
    print ("another loop NOT entered")
print("num files i counted :   ", count)


"""
for files in directory:
    count += 1
    orig_img = Image.open(files)  # the orig images
    ImageCopy = orig_img.copy()  # copy the orig
    ImageOnTop = Image.open("/home/lena/vien/fight.png") # faked on top
    ImageOnTop.copy()  # to paste on top
    ImageCopy.paste(ImageOnTop) # giving the top some dims
    os.rename(files, files + "_f2_")
    print ("i am going through a loop")
    continue
else:
    print ("no loop entered")
print("num files i counted :   ", count)
"""
