import sys, argparse

parser = argparse.ArgumentParser(description="""This is a tool accompanying the Artificial Intelligence that allows 
                                                for the classification of a single image given a pretrained tensorflow 
                                                model. Its intended use is for accurate and timely forgery detection 
                                                and classification of individual images as forged or original.""")
parser.add_argument("model", choices=["MobileNetV2", "vgg16", "vgg19", "ResNet50", "Xception"], help="model to use")
parser.add_argument("image", help="the path of the image to be classified")
parser.add_argument("weights", help="load existing weights from a ckpt directory")
parser.add_argument("labels", default="labels.data", help="read the labels from a data file (ex. ~/training/labels.data")
parser.add_argument("-v", "--verbose", action="count", help="program verbosity - for max verbosity, use -vv")

args = parser.parse_args(sys.argv[1:])
if args.verbose == None:
	args.verbose = 0

import numpy as np
import os
import PIL
import pickle

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib
import matplotlib.pyplot as plt

if args.verbose > 1:
    print('Using model ' + args.model)

if args.model == 'vgg16':
    width = 224
    height = 224
    model = keras.applications.VGG16
elif args.model == 'vgg19':
    width = 224
    height = 224
    model = keras.applications.VGG19
elif args.model == 'MobileNetV2':
    width = 224
    height = 224
    model = keras.applications.MobileNetV2
elif args.model == 'ResNet50':
    width = 224
    height = 224
    model = keras.applications.ResNet50
elif args.model == 'Xception':
    width = 299
    height = 299
    model = keras.applications.Xception
elif args.model == 'InceptionV3':
    width = 299
    height = 299
    model = keras.applications.InceptionV3

if args.verbose > 0:
    print('Reading labels')
with open(args.labels, 'rb') as filehandle:
    class_names = pickle.load(filehandle)

num_classes = len(class_names)
if args.verbose > 1:
    print('Class names: ' + str(class_names))
    print('Number of classes: ' + str(num_classes))

if args.verbose > 0:
    print('Obtaining image')
image = keras.preprocessing.image.load_img(args.image, target_size=(height, width))
input_arr = keras.preprocessing.image.img_to_array(image)
input_arr = tf.expand_dims(input_arr, 0)
"""
    data_dir,
    image_size=(height, width))
"""

if args.verbose > 0:
    print('Setting up preprocessing rules')
data_augmentation = keras.Sequential([
    layers.experimental.preprocessing.RandomFlip('horizontal', input_shape=(height, width, 3)),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomZoom(0.1),
])

if args.verbose > 0:
    print('Creating model')
model = Sequential([
    data_augmentation,
    layers.experimental.preprocessing.Rescaling(1./255),
    model(weights=None, input_shape=(height, width, 3), classes=num_classes)
])

if args.verbose > 0:
    print("Importing weights from " + args.weights)
model.load_weights(args.weights)

""" Probably unnecessary
for layer in model.layers:
    layer.trainable=True
"""

model.compile(optimizer='adam',
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

if args.verbose > 1:
    print(model.summary())

predictions = model.predict(input_arr)
score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)