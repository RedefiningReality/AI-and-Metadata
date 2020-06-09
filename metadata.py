"""Created... shoot, I don't remember when
@author: your boi Johnny Ford
"""

import piexif
from PIL import Image

import string
import random
from datetime import datetime, timedelta

import sys

import os.path
from os import path
from os import walk

input = ""
output = ""
mode = 0

author = True

def print_usage():
	print("Usage: python metadata.py [input file or directory] [optional: output directory] [mode]")
	print("Mode Types:\n\t1 => randomise author\n\t2 => randomise date taken\n\t3 => randomise both\n\t4 => alternate")
	exit()

def check_path(filepath):
	if not path.exists(filepath):
		print("What the heck is " + path + "? Give me something I understand.")
		print_usage()

def random_string(length=4):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))

def random_author():
	letters = string.ascii_uppercase
	author = random.choice(letters)
	author += random_string()
	author += " "
	author += random.choice(letters)
	return author + random_string()

def random_date(min_year=1900, max_year=datetime.now().year):
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year + 1
    end = start + timedelta(days=365 * years)
    return start + (end - start) * random.random()

def add_metadata():
	zeroth_ifd = {
        piexif.ImageIFD.Artist: u"",
        piexif.ImageIFD.DateTime: u""
    }
	exif_ifd = {
		piexif.ExifIFD.DateTimeOriginal: u""
	}
	gps_ifd = {}
	first_ifd = {}
	return {"0th":zeroth_ifd, "Exif":exif_ifd, "GPS":gps_ifd, "1st":first_ifd}

def change_metadata(filename, inputdir, outputdir):
	print("Changing metadata for " + filename + "...")
	image = Image.open(inputdir + "/" + filename)
	
	exif_dict = None
	if "exif" in image.info:
		exif_dict = piexif.load(image.info["exif"])
	else:
		exif_dict = add_metadata()
	
	if mode == 1:
		exif_dict["0th"][piexif.ImageIFD.Artist]=random_author().encode("ascii")
	elif mode == 2:
		date = random_date()
		exif_dict["0th"][piexif.ImageIFD.DateTime]=date.strftime("%Y:%m:%d %H:%M:%S").encode("ascii")
		exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]=date.strftime("%Y:%m:%d %H:%M:%S").encode("ascii")
		exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp]=date.strftime("%Y:%m:%d").encode("ascii")
		exif_dict["GPS"][piexif.GPSIFD.GPSTimeStamp]=(((int(date.strftime("%H"))+5), 1), (int(date.strftime("%M")), 1), (int(date.strftime("%S")), 1))
	elif mode == 3:
		exif_dict["0th"][piexif.ImageIFD.Artist]=random_author().encode("ascii")
		date = random_date()
		exif_dict["0th"][piexif.ImageIFD.DateTime]=date.strftime("%Y:%m:%d %H:%M:%S").encode("ascii")
		exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]=date.strftime("%Y:%m:%d %H:%M:%S").encode("ascii")
		exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp]=date.strftime("%Y:%m:%d").encode("ascii")
		exif_dict["GPS"][piexif.GPSIFD.GPSTimeStamp]=(((int(date.strftime("%H"))+5), 1), (int(date.strftime("%M")), 1), (int(date.strftime("%S")), 1))
	elif author:
		exif_dict["0th"][piexif.ImageIFD.Artist]=random_author().encode("ascii")
	else:
		date = random_date()
		exif_dict["0th"][piexif.ImageIFD.DateTime]=date.strftime("%Y:%m:%d %H:%M:%S").encode("ascii")
		exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal]=date.strftime("%Y:%m:%d %H:%M:%S").encode("ascii")
		exif_dict["GPS"][piexif.GPSIFD.GPSDateStamp]=date.strftime("%Y:%m:%d").encode("ascii")
		exif_dict["GPS"][piexif.GPSIFD.GPSTimeStamp]=(((int(date.strftime("%H"))+5), 1), (int(date.strftime("%M")), 1), (int(date.strftime("%S")), 1))
	
	exif_bytes = piexif.dump(exif_dict)
	print("Metadata changed successfully.")
	print("Output file: " + outputdir + "/" + filename[:-3] + "jpg\n")
	output = image.convert("RGB")
	output.save(outputdir + "/" + filename[:-3] + "jpg", "jpeg", exif=exif_bytes, quality=100, optimize=True)

if len(sys.argv) <= 1:
	print("Bruh, you gotta give me a file or something. For goodness sake! Who do you think I am?")
	print_usage()
else:
	input = sys.argv[1]

if input == "-h" or input == "h" or input == "/h":
	print("Okay, fine you ignorant bastard. Here's how to use this program.")
	print_usage()

if input.endswith("/*"):
	input = input[:-2]
if output.endswith("/*"):
	output = output[:-2]

if len(sys.argv) <= 2:
	print("If you're not gonna give me a mode, then go away. Nobody likes you.")
	print_usage()
else:
	output = sys.argv[2]

if output.isdigit():
	mode = output
	output = "."
elif not path.exists(output) or path.isfile(output):
	print("Yo, " + output + " is not a directory. What kind of prank are you trying to pull here?")
	print_usage()
elif len(sys.argv) <= 3:
	print("If you're not gonna give me a mode, then go away. Nobody likes you.")
	print_usage()
else:
	mode = sys.argv[3]

check_path(input)
check_path(output)

if mode != "1" and mode != "2" and mode != "3" and mode != "4":
	print("What kind of a mode is that!?")
	print_usage()
else:
	mode = int(mode)

"""
if input.endswith(".png") or input.endswith(".PNG") or input.endswith(".jpg"):
	slash_index = input.rfind("/")
	file = input[slash_index+1:]
	dirName = input[:slash_index]
	print(slash_index)
	print("Directory: " + dirName)
	print("File: " + file)
	print(vars(piexif.ImageIFD))
	image = Image.open(dirName + "/" + file)
	exif_dict = piexif.load(image.info["exif"])
	print(exif_dict["0th"])
	change_metadata(file, dirName, output)
"""

if path.isdir(input):
	for dirName, subdirList, fileList in walk(input):
		for file in fileList:
			if file.endswith(".png") or file.endswith(".PNG") or file.endswith(".jpg") or file.endswith(".JPG"):
				change_metadata(file, dirName, output)
elif path.isfile(input):
	if input.endswith(".png") or input.endswith(".PNG") or input.endswith(".jpg") or input.endswith(".JPG"):
		slash_index = input.rfind("/")
		file = input[slash_index:]
		dirName = input[:slash_index]
		change_metadata(file, dirName, output)
	else:
		print("That's... not... a png... you loser.")
		print_usage()
