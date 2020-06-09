#!/0usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:56:33 2020
It's like the old one, but it actually works
@author: j-ford
"""
# adjusting images & save the new images --- need to separate by sizes! 

from PIL import ImageFile
from PIL import Image 
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

#source_directory = "C:/Users/johnt/Desktop/pics"
source_directory = "/home/lena/vien/image_run_0/big_png"
destination_directory = "/home/lena/vien/image_run_0/adj"

for dirpath, dirnames, files in os.walk(source_directory):
	for file in files:
		print("Image: " + dirpath + "/" + file)
		
		imgs = Image.open(dirpath + "/" + file)
		img_flip = imgs.transpose(Image.FLIP_LEFT_RIGHT)
		
		# I tried to maintain your naming conventions here
		if "gt_" in file:	# if file name starts with gt_<number>, save as flipped_<number>
			save_string = destination_directory + "/flipped_" + file[file.index("gt_")+3:]
		else:			# otherwise, save the file as flipped_<original file name>
			save_string = destination_directory + "/flipped_" + file
		
		print("Saving flipped file as " + save_string)
		img_flip.save(save_string, quality=100)
		print("")

"""
for files in files_arr:
    count += 1
    imgs = Image.open(files)  
    image_flip = imgs.transpose(Image.FLIP_LEFT_RIGHT)
    os.rename(files, files + "_transposed.png")
print (count)
"""
