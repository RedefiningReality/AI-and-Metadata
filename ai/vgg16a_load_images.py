import os
import shutil
import random

genuine = "C:/Users/johnt/Desktop/genuine" # change this - input directory with genuine images
forged = "C:/Users/johnt/Desktop/forged"  # change this - input directory with forged images

percentage_test = 0.1  # change this - percentage of images to be considered test images
destination = "C:/Users/johnt/Desktop/pngs"  # change this - output directory

train_path = destination + "/train"
test_path = destination + "/test"

genuine_train_path = train_path + "/genuine"
forged_train_path = train_path + "/forged"
genuine_test_path = test_path + "/genuine"
forged_test_path = test_path + "/forged"

if not os.path.isdir(train_path):
    os.mkdir(train_path)
if not os.path.isdir(test_path):
    os.mkdir(test_path)

if os.path.isdir(genuine_train_path):
    os.rmdir(genuine_train_path)
if os.path.isdir(forged_train_path):
    os.rmdir(forged_train_path)
if os.path.isdir(genuine_test_path):
    os.rmdir(genuine_test_path)
if os.path.isdir(forged_test_path):
    os.rmdir(forged_test_path)

print("Creating directory " + genuine_train_path)
os.mkdir(genuine_train_path)
print("Creating directory " + forged_train_path)
os.mkdir(forged_train_path)
print("Creating directory " + genuine_test_path)
os.mkdir(genuine_test_path)
print("Creating directory " + forged_test_path)
os.mkdir(forged_test_path)
print("")

def separate_train_test(input_path, type):
    for dirpath, dirnames, files in os.walk(input_path):
        random.shuffle(files)
        amount_test = int(percentage_test*len(files))

        print("Source directory: " + dirpath)
        print("Number of files: " + str(len(files)))
        print("Percentage of files for test: " + str(percentage_test))
        print("Number of files for test: " + str(amount_test))
        print("Number of files for train: " + str(len(files)-amount_test))
        
        print("Copying test files to directory " + test_path + "/" + type)
        for i in range(amount_test):
            shutil.copyfile(dirpath + "/" + files[i], test_path + "/" + type + "/" + files[i])
            print(".", end="")
        print("\nCopying train files to directory " + train_path + "/" + type)
        for i in range(amount_test, len(files)):
            shutil.copyfile(dirpath + "/" + files[i], train_path + "/" + type + "/" + files[i])
            print(".", end="")
        
        print("\nFiles copied successfully")

print("Copying genuine files")
separate_train_test(genuine, "genuine")
print("\nCopying forged files")
separate_train_test(forged, "forged")
