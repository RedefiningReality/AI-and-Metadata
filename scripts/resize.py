# -*- coding: utf-8 -*-
"""Created on Wed Mar 25 11:47:16 2020
@author: olga but then John took over and made it better B)
"""
import os, argparse, sys
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

parser = argparse.ArgumentParser(description="""This is an image resizing algorithm capable of resizing 
                                    images of a given minimum width and height to a given output image width 
                                    and height. Its intended use is for resizing images prior to their being 
                                    into the forgery detection AI.""")
parser.add_argument("source", help="the path of the directory containing the images to resize")
parser.add_argument("-d", "--destination", default=None, help="the path of the directory to place the resized images (if omitted, this will be the same as the source directory)")
parser.add_argument("-w", "--old-minimum-width", default=10, type=int, help="minimum acceptable width of source image in pixels (default is 10)")
parser.add_argument("-ht", "--old-minimum-height", default=10, type=int, help="minimum acceptable height of source image in pixels (default is 10)")
parser.add_argument("-W", "--new-width", default=200, type=int, help="resized image width in pixels (default is 200)")
parser.add_argument("-H", "--new-height", default=200, type=int, help="resized image height in pixels (default is 200)")
parser.add_argument("-x", "--suffix", default="", help="suffix to append to resized image file name when saving to output directory (default is none)")
parser.add_argument("-v", "--verbose", action="count", help="program verbosity - for max verbosity, use -vv")

args = parser.parse_args(sys.argv[1:])

if args.destination is None:
    args.destination = args.source

if not os.path.isdir(args.source):
    print(source + " does not exist or is not a valid source directory!")
    exit()
if not os.path.isdir(args.destination):
    print(destination + " does not exist or is not a valid destination directory")
    exit()

verbosity = args.verbose

count = 0
count_resized = 0

for dirpath, images, files in os.walk(args.source):
    for file in files:
        count += 1
        
        if verbosity > 0:
            print("Opening image " + file)
        img = Image.open(os.path.join(dirpath, file))
        
        width, height = img.size
        if verbosity > 1:
            print("Image width: " + str(width))
            print("Image height: " + str(height))
        
        if width > args.old_minimum_width and height > args.old_minimum_height:
            if verbosity > 0:
                print("Resizing image")
            
            resized_img = img.resize((args.new_width, args.new_height))
            count_resized += 1
            save_str = os.path.join(args.destination, file[:-4] + args.suffix + ".png")
            resized_img.save(save_str, quality=100)
            
            if verbosity > 0:
                print("Image resized successfully")
                if verbosity > 1:
                    print("Image stored at " + save_str)
                print("")
        else:
            pass

print("Total Number of Images Processed: " + str(count))
print("Total Number of Images Resized: " + str(count_resized))

