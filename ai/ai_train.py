import sys, argparse
from random import randrange

parser = argparse.ArgumentParser(description="""This is an image classification Artificial Intelligence capable of determining 
                                            the class an image belongs to given a set of input data on which to train 
                                            the model. Using the training data, it will generate the weights for 
                                            a network that can then be used to classify additional images. Its intended use is for 
                                            accurate and timely forgery detection and classification of images as forged or original.""")
parser.add_argument("model", choices=["MobileNetV2", "vgg16", "vgg19", "ResNet50", "Xception"], help="model to use")
parser.add_argument('data', help='the path of the directory containing the image class subdirectories (ex. /home/lena/images where images contains folders with plant names')
parser.add_argument("-b", "--batch-size", default=32, type=int, help="batch size (default is %(default)s)")
parser.add_argument("-t", "--percent-test", default=0.2, type=float, help="a float representing the percentage of photos to use as test data rather than training data (default is %(default)s)")
parser.add_argument("-e", "--epochs", type=int, help="number of epochs (default is number of images / batch size)")
parser.add_argument("-u", "--existing-weights", default=None, help="load existing weights from a ckpt directory")
parser.add_argument("-o", "--output-dir", default=None, help="store the resulting weights to a ckpt directory (ex. ~/training/cp)")
parser.add_argument("-l", "--labels", default="labels.data", help="store the labels to a data file (ex. ~/training/labels.data")
parser.add_argument("-p", "--history-file", default=None, help="output file for loss and accuracy history (ex. ~/training/history_log.csv)")
parser.add_argument("-s", "--seed", type=int, default=randrange(500), help="seed for randomly selecting training and validation images")
parser.add_argument("-v", "--verbose", action="count", help="program verbosity - for max verbosity, use -vv")

args = parser.parse_args(sys.argv[1:])
if args.verbose == None:
	args.verbose = 0

import numpy as np
import os
import PIL

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import pathlib, pickle

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

model = keras.applications.ResNet50(weights=None, input_shape=(height, width, 3), classes=2)
print(model.summary())

data_dir = pathlib.Path(args.data)

image_count = len(list(data_dir.glob('*/*.jpg')))
if args.verbose > 1:
    print('Number of images in dataset: ' + str(image_count))

if args.verbose > 0:
    print('Obtaining train dataset')
train_ds = keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=args.percent_test,
    subset='training',
    seed=args.seed,
    image_size=(height, width),
    batch_size=args.batch_size)

if args.verbose > 0:
    print('Obtaining validation dataset')
val_ds = keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=args.percent_test,
    subset='validation',
    seed=args.seed,
    image_size=(height, width),
    batch_size=args.batch_size)

class_names = train_ds.class_names
class_names = [name.replace('_', ' ').title() for name in class_names]

if args.output_dir is not None:
    if args.verbose > 0:
        print('Saving labels')
    with open(args.labels, 'wb') as filehandle:
        pickle.dump(class_names, filehandle)

num_classes = len(class_names)
if args.verbose > 1:
    print('Class names: ' + str(class_names))
    print('Number of classes: ' + str(num_classes))

AUTOTUNE = tf.data.experimental.AUTOTUNE

if args.verbose > 0:
    print('Shuffling train dataset and prefetching datasets')
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
#train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

if args.verbose > 0:
    print('Setting up preprocessing rules')
data_augmentation = keras.Sequential([
    layers.experimental.preprocessing.RandomFlip('horizontal', input_shape=(height, width, 3)),
    layers.experimental.preprocessing.RandomRotation(0.1),
    layers.experimental.preprocessing.RandomZoom(0.1),
])

base = model(weights=None, input_shape=(height, width, 3), classes=num_classes)

if args.verbose > 0:
    print('Creating model')
model = Sequential([
    data_augmentation,
    layers.experimental.preprocessing.Rescaling(1./255),
    base
])

if args.existing_weights is not None:
	if args.verbose > 0:
		print("Importing weights from " + args.existing_weights)
	model.load_weights(args.existing_weights)

""" Probably unnecessary
for layer in model.layers:
    layer.trainable=True
"""

model.compile(optimizer='adam',
            loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

if args.verbose > 1:
    print(model.summary())

if args.epochs is None:
	args.epochs = int(image_count/args.batch_size)
if args.verbose > 1:
	print("Total number of epochs: " + str(args.epochs))

cb = []
if args.output_dir is not None:
	if args.verbose > 0:
		print("Periodically saving weights to " + args.output_dir)
	cp_callback = keras.callbacks.ModelCheckpoint(filepath=args.output_dir,
													save_weights_only=True,
													verbose=1,
													period=1)
	cb.append(cp_callback)

if args.history_file is not None:
	if args.verbose > 0:
		print("Logging to file " + args.history_file)
	logger_callback = keras.callbacks.CSVLogger(args.history_file, append=True)
	cb.append(logger_callback)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=args.epochs,
    callbacks=cb
)

if args.verbose > 0:
	print("Model training complete")