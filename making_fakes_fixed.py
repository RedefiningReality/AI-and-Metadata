#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 08:10:13 2020

@author: not olga anymore - it's me again: John Ford
"""
from PIL import ImageFile
from PIL import Image 
import os, random
ImageFile.LOAD_TRUNCATED_IMAGES = True

min_width = 0.1
max_width = 0.5
min_height = 0.1
max_height = 0.5

source_directory = "/home/lena/vien/image_run_0/faked/adj_big_png/big_png"
destination_directory = "/home/lena/vien/image_run_0/faked/faked_adj"
count = 0

for dirpath, dirnames, files in os.walk(source_directory):
    for file in files:
        count += 1
        
        print("Image: " + dirpath + "/" + file)
        orig_img = Image.open(dirpath + "/" + file)  # the orig images

        width, height = orig_img.size
        rand_width = random.randint(int(width*min_width), int(width*max_width))
        rand_height = random.randint(int(height*min_height), int(height*max_height))
        print("Random width: " + str(rand_width))
        print("Random height: " + str(rand_height))
        
        crop_left = random.randint(0, width-rand_width)
        crop_right = crop_left+rand_width
        crop_top = random.randint(0, height-rand_height)
        crop_bottom = crop_top+rand_height
        print("Crop left: " + str(crop_left))
        print("Crop top: " + str(crop_top))
        
        paste_left = random.randint(0, width-rand_width)
        paste_right = paste_left+rand_width
        paste_top = random.randint(0, height-rand_height)
        paste_bottom = paste_top+rand_height
        print("Paste left: " + str(paste_left))
        print("Paste top: " + str(paste_top))
        
        region = orig_img.crop((crop_left, crop_top, crop_right, crop_bottom))
        orig_img.paste(region, (paste_left, paste_top, paste_right, paste_bottom))
        orig_img = orig_img.convert("RGB")
        orig_img.save(destination_directory + "/" + file + "_fkthis2.png", quality=100)
        print("Imaged forged successfully")
        print("")
else:
    print ("another loop NOT entered")
print("Num files counted: ", count)


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
