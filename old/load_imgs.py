#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:09:35 2020

@author: olga
"""
#import IPython.display as display
#from PIL import Image
from PIL import ImageFile
import numpy as np
import matplotlib.pyplot as plt
import pathlib2, glob2, os, cv2, random, pickle
import tensorflow as tf
ImageFile.LOAD_TRUNCATED_IMAGES = True

# taken from : https://towardsdatascience.com/
# ' all-the-steps-to-build-your-first-image-classifier-
	# ' with-code-cf244b015799
#AUTOTUNE = tf.data.experimental.AUTOTUNE
data = "/home/lena/vien/image_run_0/"
#gt = "/home/lena/vien/image_run_0/big_png"
#adj = "/home/lena/vien/image_run_0/adj"
#fakes = "/home/lena/vien/image_run_0/fakes"
data_dir = pathlib2.Path(data)

CATEGORIES = ["big_png", "adj", "fakes"]

IMG_SIZE = 50

for category in CATEGORIES:
    path = os.path.join(data_dir, category)
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join (path, img), cv2.IMREAD_GRAYSCALE)

training_data = []

def create_training_data():
    for category in CATEGORIES :
        path = os.path.join(data_dir, category)
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try :
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass

create_training_data()

random.shuffle(training_data)

X = [] # features
y = []  # labels

for features, label in training_data:
    X.append(features)
    y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
y = np.array(y)


# Creating the files containing all the information about your model
pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)

