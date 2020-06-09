import csv
from csv import DictReader
from csv import DictWriter

import sys
from os import path

mode = ("all", "print")
list = []
filename = "features.csv"

def print_usage():
	print("Usage: ")
	print("\tpython features.py [optional: -f [csv file]] => prints entire table of features")
	print("\tpython features.py image [image name] [add/delete/get] [features list] [optional: -f [csv file]]")
	print("\tpython features.py images [add/delete/get] [images list] [optional: -f [csv file]]")
	print("\tpython features.py feature [feature] [add/delete/get] [images list] [optional: -f [csv file]]")
	print("\tpython features.py features [add/delete/get] [features list] [optional: -f [csv file]]")
	print("Notes:\n\tfeatures or images list is space-separated")
	print("\tThe default csv file when not specified is features.csv in the current script directory")
	print("\tImplementation is most efficient when adding to, getting for, and deleting from an image rather than feature")
	print("\tBe careful not to put additional data after the -f flag unless it is the first thing entered")
	print("\tThe image and feature options will automatically create a new image or feature if it doesn't already exist")
	print("\tfeature [feature] delete doesn't fully remove the feature, it just unmarks it for the specified images")
	print("\t\tto fully delete a feature, use features delete [feature]")
	print("\tThe same principle applies to image [image] delete")
	print("\t\tto fully delete an image, use images delete [image]")
	print("\nExamples:\n\tpython features.py image cat add fluffy adorable cute")
	print("\t\tadds features fluffy, adorable, and cute to cat.png")
	print("\tpython features.py feature fluffy remove cat dog")
	print("\t\tremoves feature fluffy from cat.png and dog.png")
	print("\tpython features.py images add cat dog")
	print("\t\tadds cat.png and dog.png to list of images")
	print("\tpython features.py features remove fluffy adorable cute")
	print("\t\tremoves features fluffy, adorable, and cute from all images")
	exit()

def save_to_file(list):
	with open(filename, mode='w') as csv_file:
		print("\nWriting to csv file...")
		writer = DictWriter(csv_file, field_names)
		writer.writeheader()
		for row in list:
			writer.writerow(row)

next = 1
if len(sys.argv) == 1:
	pass
elif sys.argv[next] == "-h":
	print("You fool! Asking for help now, are ya? Well, I'll show you how it's done.")
	print_usage()
elif sys.argv[next] == "-f":
	if len(sys.argv) <= next+1:
		print("Um... if you say you're gonna give me a file, give me one for goodness sake!")
		print_usage()
	else:
		filename = sys.argv[next+1]
		next = 3

if len(sys.argv) <= next:
	pass	# These passes are my janky way of handling no arguments after the -f flag and no arguments at all
elif sys.argv[next] == "image" or sys.argv[next] == "feature":
	operation_index = next+2
elif sys.argv[next] == "images" or sys.argv[next] == "features":
	operation_index = next+1
else:
	print("Yeah, nice try. " + sys.argv[next] + " ain't one of the options.")
	print_usage()

try:
	if len(sys.argv) <= operation_index:
		print("C'mon, you gotta tell me what to do with the " + sys.argv[next] + ".")
		print_usage()
	elif sys.argv[operation_index] != "add" and sys.argv[operation_index] != "delete" and sys.argv[operation_index] != "get":
		print("Dude, " + sys.argv[operation_index] + " is totally not one of the options for " + sys.argv[next] + ".")
		print_usage()
	else:
		start = operation_index + 1
		if sys.argv[next] == "image" or sys.argv[next] == "feature":
			if len(sys.argv) > operation_index+1:
				main = sys.argv[operation_index-1]
			else:
				print("Seriously? You're not gonna give me a " + sys.argv[next] + "? Try again.")
				print_usage()
		mode = (sys.argv[next], sys.argv[operation_index])
		for j in range(operation_index+1, len(sys.argv)):
			if sys.argv[j] == "-f":
				if len(sys.argv) <= j+1:
					print("Um... if you say you're gonna give me a file, give me one for goodness sake!")
					print_usage()
				else:
					filename = sys.argv[j+1]
					break
			elif sys.argv[j] == "-h":
				print("You fool! Asking for help now, are ya? Well, I'll show you how it's done.")
				print_usage()
			else:
				list.append(sys.argv[j])
except NameError:
	pass	# It may be janky, but it does the job

""" For input testing purposes:
print("Mode: " + str(mode))
try:
    print("Main: " + main)
except NameError:
    print("Main: none")
print("List: " + str(list))
print("Outfile: " + filename)
"""

if not path.exists(filename):
	print("Csv file not found")
	open(filename, mode='x')
	print("Created csv file " + filename)

current = []
with open(filename, mode='r') as csv_file:
	print("Reading from csv file " + filename + "...")
	reader = DictReader(csv_file)
	
	for row in reader:
		current.append(row)
	print("Finished reading")
	
	field_names = reader.fieldnames
	if field_names == None:
		field_names = []
	
	if mode[0] == "all":
		for field in field_names:
			if len(field) >= 10:
				field = field[:6] + "..."
			print(field, end=" "*(10-len(field)))
		print()
		for row in current:
			for field in field_names:
				if field in row:
					if len(row[field]) >= 10:
						row[field] = row[field][:6] + "..."
					print(row[field], end=" "*(10-len(row[field])))
				else:
					print("", end=" "*10)
			print()
	elif mode[0] == "image":
		if len(list) == 0 and mode[1] != "get":
			print("Give me an image you imbecile!")
			print_usage()
		elif mode[1] == "add":
			for row in current:
				if row["image"] == main:
					print("Adding features to image " + main)
					for feature in list:
						row.update({feature: "Yes"})
						print("Added " + feature)
					print("Features added successfully!")
					break
			else:
				print("Image " + main + " not found. Creating image")
				current.append({"image": main})
				print("Adding features to image " + main)
				for feature in list:
					current[len(current)-1].update({feature: "Yes"})
					print("Added " + feature)
				print("Features added successfully!")
			list.insert(0, "image")
			for feature in list:
				if feature not in field_names:
					field_names.append(feature)
			save_to_file(current)
		elif mode[1] == "delete":
			for row in current:
				if row["image"] == main:
					print("Deleting features from image " + main)
					for feature in list:
						if feature in row:
							del row[feature]
							print("Deleted " + feature)
						else:
							print("You idiot! Feature " + feature + " doesn't even exist!")
					print("Features deleted successfully!")
					break
			else:
				print("You idiot! " + main + " doesn't even exist! What's wrong with you?")
				print_usage()
			save_to_file(current)
		elif mode[1] == "get":
			for row in current:
				if row["image"] == main:
					print("Here are the features for image " + main + ":")
					for key in row:
						if key == "image":
							continue
						elif row[key] == "Yes":
							print(key)
					break
			else:
				print("You idiot! " + main + " doesn't even exist! What's wrong with you?")
				print_usage()
		else:
			print("Huh? " + mode[1] + "? Yeah, nice try buddy. Get a life.")
			print_usage()
	elif mode[0] == "feature":
		if len(list) == 0 and mode[1] != "get":
			print("Give me a feature you imbecile!")
			print_usage()
		elif mode[1] == "add":
			print("Adding feature " + main)
			for row in current:
				if row["image"] in list:
					row.update({main: "Yes"})
					print("Added to image " + row["image"])
					list.remove(row["image"])
			for image in list:
				current.append({"image": image, main: "Yes"})
				print("Added to image " + image)
			print("Feature added to images successfully!")
			if "image" not in field_names:
				field_names.insert(0, "image")
			if main not in field_names:
				field_names.append(main)
			save_to_file(current)
		elif mode[1] == "delete":
			if main not in field_names:
				print("You idiot! " + main + " doesn't even exist! What's wrong with you?")
				print_usage()
			print("Deleting feature " + main)
			for row in current:
				for image in list:
					if row["image"] == image:
						del row[main]
						print("Deleted from image " + image)
			print("Feature deleted from images successfully!")
			save_to_file(current)
		elif mode[1] == "get":
			if main not in field_names:
				print("You idiot! " + main + " doesn't even exist! What's wrong with you?")
				print_usage()
			print("Here are the images with feature " + main + ":")
			for row in current:
				if main in row and row[main]:
					print(row["image"])
		else:
			print("Huh? " + mode[1] + "? Yeah, nice try buddy. Get a life.")
			print_usage()
	elif mode[0] == "images":
		if len(list) == 0 and mode[1] != "get":
			print("Give me images you imbecile!")
			print_usage()
		elif mode[1] == "add":
			print("Adding images")
			duplicates = []
			for row in current:
				for image in list:
					if row["image"] == image:
						print("Image " + image + " already exists")
						duplicates.append(image)
						break
			for image in list:
				if image not in duplicates:
					current.append({"image": image})
					duplicates.append(image)
					print("Added " + image)
			print("Images added successfully!")
			if "image" not in field_names:
				field_names.insert(0, "image")
			save_to_file(current)
		elif mode[1] == "delete":
			print("Deleting images")
			deleted = []
			for row in reversed(current):
				for image in reversed(list):
					if row["image"] == image:
						current.remove(row)
						print("Deleted " + image)
						list.remove(image)
						break
			for image in list:
				print("Image " + image + " doesn't exist")
			print("Images deleted successfully!")
			save_to_file(current)
		elif mode[1] == "get":
			print("Here are all the images:")
			for row in current:
				print(row["image"])
		else:
			print("Huh? " + mode[1] + "? Yeah, nice try buddy. Get a life.")
			print_usage()
	else:
		if len(list) == 0 and mode[1] != "get":
			print("Give me features you imbecile!")
			print_usage()
		elif mode[1] == "add":
			print("Adding features")
			for feature in list:
				if feature not in field_names:
					field_names.append(feature)
					print("Added " + feature)
			print("Features added successfully!")
			save_to_file(current)
		elif mode[1] == "delete":
			print("Deleting features")
			for feature in reversed(list):
				if feature in field_names:
					field_names.remove(feature)
				else:
					print("Feature " + feature + " doesn't exist!")
					list.remove(feature)
			for feature in list:
				for row in current:
					if feature in row:
						del row[feature]
				print("Deleted " + feature)
			print("Features deleted successfully!")
			save_to_file(current)
		elif mode[1] == "get":
			print("Here are all the features:")
			for feature in field_names:
				print(feature)
		else:
			print("Huh? " + mode[1] + "? Yeah, nice try buddy. Get a life.")
			print_usage()