#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 19:52:13 2020

Yet another cute little script by yours truly, John Ford
"""
import argparse, sys

parser = argparse.ArgumentParser(description="""This is an image forgery creation algorithm capable of creating
											forgeries given source images and forgery components to layer on top 
											of the source images. Its intended use is to add Vien to images because, 
											y'know, it can get a little lonely without her, especially if you're stuck 
											in Florida.""")
parser.add_argument("source_image_directory", help="path to the directory containing the source images")
parser.add_argument("forge_image_directory", help="path to the directory containing the images to layer on top")
parser.add_argument("-o", "--output-dir", default="~/", help="directory to output forged images (default is ~/)")
parser.add_argument("-w", "--minimum-width", default=0.3, type=float, help="minimum layered image width as a percentage of the source image")
parser.add_argument("-W", "--maximum-width", default=0.7, type=float, help="maximum layered image width as a percentage of the source image")
parser.add_argument("-ht", "--minimum-height", default=0.3, type=float, help="minimum layered image height as a percentage of the source image")
parser.add_argument("-H", "--maximum-height", default=0.7, type=float, help="maximum layered image height as a percentage of the source image")
parser.add_argument("-d", "--on-bottom", action="store_true", help="always paste the image to layer on the bottom of the source image")
parser.add_argument("-s", "--stretch-forge-image", action="store_true", help="allow stretching of image to layer (as opposed to maintaining original aspect ratio)")
parser.add_argument("-m", "--mask", action="store_true", help="use custom transparency mask for the image to layer")
parser.add_argument("-b", "--blur", action="store_true", help="blur image to layer prior to layering")
parser.add_argument("-r", "--blur-radius", default=0.03, type=float, help="radius for Gaussian blur applied to image to layer prior to layering - used in conjunction with -b flag (default is 0.05)")
parser.add_argument("-c", "--contrast", default=1.3, type=float, help="contrast to apply after Gaussian blur prior to layering image - used in conjunction with -b flag (default is 1.3)")
parser.add_argument("-x", "--suffix", default="", help="suffix to append to forged image file name when saving to output directory (default is none)")
parser.add_argument("-sm", "--save-masks", action="store_true", help="save image masks for layered image as well as original image")
parser.add_argument("-v", "--verbose", action="count", help="program verbosity - for max verbosity, use -vv")

args = parser.parse_args(sys.argv[1:])

print("hello?")

from PIL import Image, ImageFile, ImageDraw, ImageFilter, ImageEnhance
import os, random
from datetime import datetime
ImageFile.LOAD_TRUNCATED_IMAGES = True

#source_image_directory = "C:/Users/johnt/Desktop/source" # change this - images to be forged
#forge_image_directory = "C:/Users/johnt/Desktop/vien" # change this - images to layer on top
#destination_directory = "C:/Users/johnt/Desktop/output" # change this - forged image output directory

if args.verbose is None:
	args.verbose = 0

count = 0
index = 0

forge_images = []
for dirpath, dirnames, files in os.walk(args.forge_image_directory):
	for file in files:
		if file.endswith(".png") or file.endswith(".PNG") or file.endswith(".jpg") or file.endswith(".JPG"):
			forge_images.append(dirpath + "/" + file)

def partially_transparent(img):
	extrema = img.getextrema()
	return len(extrema) > 3

random.seed(datetime.now())
#print(forge_images)
for dirpath, dirnames, files in os.walk(args.source_image_directory):
	for file in files:
		count += 1
		
		orig_img = Image.open(dirpath + "/" + file)  # the orig images
		forge_img = Image.open(forge_images[index])
		
		width, height = orig_img.size
		forge_width, forge_height = forge_img.size
		
		if args.verbose > 0:
			print("Source image: " + dirpath + "/" + file)
		if args.verbose > 1:
			print("Source image width: " + str(width))
			print("Source image height: " + str(height))
		
		if args.verbose > 0:
			print("Image to layer: " + forge_images[index])
		if args.verbose > 1:
			print("Image to layer original width: " + str(forge_width))
			print("Image to layer original height: " + str(forge_height))
		
		if args.stretch_forge_image: # if we can stretch the image, we don't have to worry about maintaining aspect ratio
			if args.verbose > 0:
				print("Resizing...")
			forge_width = random.randint(int(width*args.minimum_width), int(width*args.maximum_width))
			forge_height = random.randint(int(height*args.minimum_height), int(height*args.maximum_height))
		elif forge_height/forge_width < height/width: # resize according to width
			if args.verbose > 0:
				print("Resizing according to width...")
			old_width = forge_width
			forge_width = random.randint(int(width*args.minimum_width), int(width*args.maximum_width))
			forge_height = int(forge_height*(float(forge_width)/old_width))
		else: # resize according to height
			if args.verbose > 0:
				print("Resizing according to height...")
			old_height = forge_height
			forge_height = random.randint(int(height*args.minimum_height), int(height*args.maximum_height))
			"""
			print("old_height: " + str(old_height))
			print("forge_height: " + str(forge_height))
			print("forge_width: " + str(forge_width))
			print("mult 1: " + str(float(forge_height)/old_height))
			print("mult 2: " + str(forge_width*(float(forge_height)/old_height)))
			print("with int: " + str(int(forge_width*(float(forge_height)/old_height))))
			"""
			forge_width = int(forge_width*(float(forge_height)/old_height))
		
		if args.verbose > 1:
			print("Image to layer new width: " + str(forge_width))
			print("Image to layer new height: " + str(forge_height))
		resized_img = forge_img.resize((forge_width, forge_height))
		
		paste_left = random.randint(0, width-forge_width)
		if args.on_bottom:
			paste_top = height-forge_height
		else:
			paste_top = random.randint(0, height-forge_height)
		if args.verbose > 1:
			print("Paste left: " + str(paste_left))
			print("Paste top: " + str(paste_top))
		
		# Create mask
		if args.mask:
			if args.verbose > 0:
				print("Creating custom transparency mask for image to layer")
			
			mask = Image.new("L", (forge_width, forge_height), 0)
			draw = ImageDraw.Draw(mask)
			
			x1 = random.randint(0, int(forge_width/3))
			x2 = random.randint(x1+int(forge_width/4), forge_width)
			y1 = random.randint(0, int(forge_height/3))
			y2 = random.randint(y1+int(forge_height/4), forge_height)
			if args.verbose > 1:
				print("Transparency mask left boundary: " + str(x1))
				print("Transparency mask right boundary: " + str(x2))
				print("Transparency mask top boundary: " + str(y1))
				print("Transparency mask bottom boundary: " + str(y2))
			
			rand = random.randint(1, 4)
			if rand == 1:
				if args.verbose > 1:
					print("Mask type: ellipse")
				draw.ellipse((x1, y1, x2, y2), fill=255)
			elif rand == 2:
				draw.chord((x1, y1, x2, y2), random.randint(0, 359), random.randint(0, 359), fill=255)
				if args.verbose > 1:
					print("Mask type: chord")
			elif rand == 3:
				draw.rectangle((x1, y1, x2, y2), fill=255)
				if args.verbose > 1:
					print("Mask type: rectangle")
			else:
				draw.pieslice((x1, y1, x2, y2), random.randint(0, 359), random.randint(0, 359), fill=255)
				if args.verbose > 1:
					print("Mask type: pieslice")
		# Use mask from image
		elif partially_transparent(resized_img):
			if args.verbose > 0:
				print("Using current transparency mask for image to layer")
			black = Image.new('L', (forge_width, forge_height), 0)
			white = Image.new('L', (forge_width, forge_height), 255)
			mask = Image.composite(white, black, resized_img)
		# No mask
		else:
			if args.verbose > 0:
				print("Layering image without transparency mask")
			mask = Image.new('L', (forge_width, forge_height), 255)
		
		if args.blur:
			# Blur mask
			radius = min(forge_width, forge_height)*args.blur_radius
			mask = mask.filter(ImageFilter.GaussianBlur(radius))
			enhancer = ImageEnhance.Contrast(mask)
			mask = enhancer.enhance(args.contrast)
			#mask = mask.point(lambda x: 255 if x==255 else x*0.5, 'L') <- old remnants of the pre-contrast days
			
			"""
			inverted = mask.convert('RGB')
			inverted = ImageOps.invert(inverted)
			inverted = inverted.convert('L')

			mask_blur.putalpha(mask)
			save_string = args.output_dir + "/" + file + "_cp00.png" # feel free to change this
			mask_blur.save(save_string, quality=100)
			exit()
			"""
			
			"""
			temp = Image.new('L', (forge_width, forge_height), 0)
			temp.paste(mask, (0, 0), mask=resized_img)
			#new = new.point(lambda x: 255 if x==255 else x*0.95, 'L')
			mask = temp
			mask.show()
			"""
		
		if args.save_masks:
			save_string = args.output_dir + "/" + file[:-4] + args.suffix + "_mask.png" # feel free to change this
			mask.save(save_string, quality=100)
			if args.verbose > 0:
				print("Mask created successfully")
				print("Saved mask as " + save_string)
				print("")
		
		"""
		test = Image.new('L', (forge_width, forge_height), 255)
		test.paste(resized_img, (0, 0), mask=mask)
		test.show()
		exit()
		"""
		
		# Blur image and paste blurred edge according to mask
		orig_img.paste(resized_img, (paste_left, paste_top), mask=mask)
		
		orig_img = orig_img.convert('RGB')
		save_string = args.output_dir + "/" + file[:-4] + args.suffix + ".png" # feel free to change this
		orig_img.save(save_string, quality=100)
		if args.verbose > 0:
			print("Imaged forged successfully")
			print("Saved forgery as " + save_string)
			print("")
		
		index = (index+1) % len(forge_images)
		#print(index)

print("Num files counted: ", count)
