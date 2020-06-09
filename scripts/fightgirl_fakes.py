#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:52:13 2020

@author: olga - PSYCH, it's actually john haha gotem
"""
from PIL import ImageFile
from PIL import Image 
import os, random
ImageFile.LOAD_TRUNCATED_IMAGES = True

source_image_directory = "/home/lena/vien/image_run_0/big_png" # change this - images to be forged
forge_image_directory = "/home/lena/vien/image_run_0/to_mess_with_you" # change this - images to layer on top
destination_directory = "/home/lena/vien/image_run_0/fakes" # change this - forged image output directory

stretch_forge_image = False # whether the image layered can be stretched
                            # (as opposed to maintaining its original aspect ratio)
min_width = 0.1  # minimum layered image width (as percentage of source image width)
max_width = 0.5  # maxmimum width
min_height = 0.1 # minimum height
max_height = 0.5 # maximum height

count = 0
index = 0

forge_images = []
for dirpath, dirnames, files in os.walk(forge_image_directory):
	for file in files:
		if file.endswith(".png") or file.endswith(".PNG") or file.endswith(".jpg") or file.endswith(".JPG"):
			forge_images.append(dirpath + "/" + file)

#print(forge_images)
for dirpath, dirnames, files in os.walk(source_image_directory):
	for file in files:
		count += 1

		orig_img = Image.open(dirpath + "/" + file)  # the orig images
		forge_img = Image.open(forge_images[index])
		
		width, height = orig_img.size
		forge_width, forge_height = forge_img.size
		
		print("Source image: " + dirpath + "/" + file)
		print("Source image width: " + str(width))
		print("Source image height: " + str(height))
		
		print("Image to layer: " + forge_images[index])
		print("Image to layer original width: " + str(forge_width))
		print("Image to layer original height: " + str(forge_height))
		
		if stretch_forge_image: # if we can stretch the image, we don't have to worry about maintaining aspect ratio
			print("Resizing...")
			forge_width = random.randint(int(width*min_width), int(width*max_width))
			forge_height = random.randint(int(height*min_height), int(height*max_height))
		elif forge_height/forge_width < height/width: # resize according to width
			print("Resizing according to width...")
			old_width = forge_width
			forge_width = random.randint(int(width*min_width), int(width*max_width))
			forge_height = int(forge_height*(forge_width/old_width))
		else: # resize according to height
			print("Resizing according to height...")
			old_height = forge_height
			forge_height = random.randint(int(height*min_height), int(height*max_height))
			forge_width = int(forge_width*(forge_height/old_height))
		
		print("Image to layer new width: " + str(forge_width))
		print("Image to layer new height: " + str(forge_height))
		resized_img = forge_img.resize((forge_width, forge_height))
		
		paste_left = random.randint(0, width-forge_width)
		paste_top = random.randint(0, height-forge_height)
		print("Paste left: " + str(paste_left))
		print("Paste top: " + str(paste_top))
		
		orig_img.paste(resized_img, (paste_left, paste_top))
		orig_img = orig_img.convert("RGB")
		save_string = destination_directory + "/" + file + "_fkthis3.png" # feel free to change this
		orig_img.save(save_string, quality=100)
		print("Imaged forged successfully")
		print("Saved forgery as " + save_string)
		print("")

		index = (index+1) % len(forge_images)
		#print(index)

print("Num files counted: ", count)
