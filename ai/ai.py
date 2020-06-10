# taken from: https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/ and https://www.tensorflow.org/tutorials/load_data/images
# combined with tf doc wrt tf.data
# author: John Ford
from __future__ import absolute_import, division, print_function
import argparse, sys

parser = argparse.ArgumentParser(description="""This is an Artificial Intelligence capable of categorising images
									given a set of training data. Its intended use is for accurate and timely forgery 
									detection and classification of images as forged or original.""")
parser.add_argument("algorithm", choices=["vgg16", "vgg19"], help="Algorithm to use. Choices are vgg16 and vgg19")
parser.add_argument("data", help="The path of the directory containing the image subdirectories (ex. /home/lena/vien/image_run_0 where image_run_0 contains folders original and forged)")
parser.add_argument("-o", "--output-dir", default=None, help="Store the resulting weights to a ckpt directory (ex. ~/training/cp.ckpt)")
parser.add_argument("-u", "--existing-weights", default=None, help="Load existing weights from a ckpt directory")
parser.add_argument("-p", "--history-file", default=None, help="Output file for loss and accuracy history (ex. ~/training/history_log.csv)")
parser.add_argument("-t", "--percent-test", default=0.2, type=float, help="A float representing the percentage of photos to use as test data rather than training data (default is %(default)s)")
parser.add_argument("-w", "--width", default=100, type=int, help="Resize width of images to be parsed by model (default is %(default)s)")
parser.add_argument("-x", "--height", default=100, type=int, help="Resize height of images to be parsed by model (default is %(default)s)")
parser.add_argument("-b", "--batch-size", default=32, type=int, help="Batch size (default is %(default)s)")
parser.add_argument("-e", "--epochs", type=int, help="Number of epochs (default is number of images / batch size)")
parser.add_argument("-s", "--steps", default=30, type=int, help="Number of steps per epoch (default is %(default)s)")
parser.add_argument("-c", "--validation-steps", default=2, type=int, help="Number of validation steps per epoch during training (default is %(default)s)")
parser.add_argument("-d", "--final-validation-steps", default=100, type=int, help="Number of validation steps in calculating the final algorithm accuracy (default is %(default)s)")
parser.add_argument("-a", "--activation", default="softmax", help="The activation function for the final network layer (default is %(default)s)")
parser.add_argument("-v", "--verbose", action="count", help="Program verbosity. For max verbosity, use -vv")

args = parser.parse_args(sys.argv[1:])

from tqdm import tqdm
from numpy.random import randn
from glob2 import glob
import pathlib2, random, os, cv2
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd
from matplotlib.image import imread
from keras.preprocessing import image
import os
from keras.callbacks import CSVLogger

verbosity = args.verbose
model = args.algorithm

data_dir = args.data
percent_test = args.percent_test

IMG_HEIGHT = args.height
IMG_WIDTH = args.width
BATCH_SIZE = args.batch_size

EPOCHS = args.epochs
STEPS_PER_EPOCH = args.steps
VALIDATION_STEPS_1 = args.validation_steps
VALIDATION_STEPS_2 = args.final_validation_steps

# print("here")
# np.set_printoptions(precision=4)
# tf.enable_eager_execution() => enabled by default as of tf2.0

os.environ["TF_CPP_MIN_LOG_LEVEL"]="2"
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

AUTOTUNE = tf.data.experimental.AUTOTUNE

# data_dir = pathlib.Path(data_dir)
data_dir = pathlib2.Path(data_dir)

if verbosity > 1:
	print("Collecting image file names...")
images = list(data_dir.glob('*/*'))
images = [str(path) for path in images]
images = [path for path in images if path.endswith(".png")]
random.shuffle(images)

if verbosity > 0:
	print("Number of images: " + str(len(images)))

label_names={}
labels = []

if verbosity > 1:
	print("Collecting and assigning image labels...")
counter = 0
for path in images:
	folder = pathlib2.Path(path).parent.name
	if folder in label_names:
		labels.append(label_names[folder])
	else:
		label_names[folder] = counter
		labels.append(counter)
		counter += 1
if verbosity > 0:
	print("Image Labels: " + str(label_names))

if EPOCHS == None:
	EPOCHS = int(len(images)/BATCH_SIZE)
if verbosity > 1:
	print("Total number of epochs: " + str(EPOCHS))

"""
print(label_names)
print(labels)
exit()
"""

# list_ds = tf.data.Dataset.list_files(str(data_dir/'*/*.png'))
slice_ds = ds = tf.data.Dataset.from_tensor_slices((images, labels))

"""
def get_label(file_path):
	# convert the path to a list of path components
	parts = tf.strings.split(file_path, os.path.sep)
	# The second to last is the class-directory
	# return parts[-2]
	
	print(type(parts[-2]))
	pp.pprint(dir(parts[-2]))
	exit()
	label = label_names[pathlib2.Path(file_path).parent.name]
	exit()
	return tf.convert_to_tensor(label, dtype=tf.int32)
"""

def decode_img(img):
	# convert the compressed string to a 3D uint8 tensor
	img = tf.image.decode_png(img, channels=3)
	# Use `convert_image_dtype` to convert to floats in the [0,1] range.
	img = tf.image.convert_image_dtype(img, tf.float32)
	# resize the image to the desired size.
	return tf.image.resize(img, [IMG_HEIGHT, IMG_WIDTH])

def process_path(file_path, label):
	# load the raw data from the file as a string
	"""
	print(type(file_path))
	print(type(label))
	"""
	"""
	image = tf.io.read_file(file_path)
	image = tf.image.decode_png(image, channels=3)
	image = tf.cast(image, tf.float32)
	image = (image/127.5) - 1
	image = tf.image.resize(image, (IMG_HEIGHT, IMG_WIDTH))
	return image, label
	"""
	img = tf.io.read_file(file_path)
	img = decode_img(img)
	return img, label

if verbosity > 1:
	print("Decoding images...")
labeled_ds = slice_ds.map(process_path, num_parallel_calls=AUTOTUNE)

"""
for image, label in labeled_ds.take(3):
	print("Image shape: ", image.numpy().shape)
	print("Label: ", label.numpy())
exit()
"""

def prepare_for_training(ds, cache=True, shuffle_buffer_size=1000):
	# This is a small dataset, only load it once, and keep it in memory.
	# use `.cache(filename)` to cache preprocessing work for datasets that don't
	# fit in memory.
	if cache:
		if isinstance(cache, str):
			ds = ds.cache(cache)
		else:
			ds = ds.cache()
	
	ds = ds.shuffle(buffer_size=shuffle_buffer_size)
	
	# Repeat forever
	ds = ds.repeat()
	ds = ds.batch(BATCH_SIZE)
	
	# `prefetch` lets the dataset fetch batches in the background while the model
	# is training.
	ds = ds.prefetch(buffer_size=AUTOTUNE)
	
	return ds

if verbosity > 1:
	print("Preparing dataset for training...")
full_ds = prepare_for_training(labeled_ds)

if verbosity > 1:
	print("Percent training images: {:5.2f}".format((100-(percent_test*100))))
	print("Percent testing images: {:5.2f}".format(percent_test*100))
if verbosity > 0:
	print("Number of training images: " + str(int(len(images)*percent_test)))
	print("Number of testing images: " + str((len(images)-int(len(images)*percent_test))))
test_ds = full_ds.take(int(len(images)*percent_test))
train_ds = full_ds.skip(int(len(images)*percent_test))

"""
image_batch, label_batch = next(iter(train_ds))
print(str(image_batch.numpy()))
print(str(label_batch.numpy()))

image_b2, label_b2 = next(iter(test_ds))
print(str(image_b2.numpy()))
print(str(label_b2.numpy()))

print(str(len(image_b2.numpy())))
print(str(len(label_b2.numpy())))
print(str(len(image_batch.numpy())))
print(str(len(label_batch.numpy())))
exit()
"""

# print("here3")

global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(len(label_names),activation=args.activation)
# try for now => goal should be relu (I tried it, but it's much worse)

IMG_SHAPE = (IMG_HEIGHT, IMG_WIDTH, 3)

if model.lower() == "vgg16":
	if verbosity > 1:
		print("Using model vgg16")
	MD = tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
									   include_top=False,
									   weights="imagenet")
elif model.lower() == "vgg19":
	if verbosity > 1:
		print("Using model vgg19")
	MD = tf.keras.applications.VGG19(input_shape=IMG_SHAPE,
									   include_top=False,
									   weights="imagenet")
else:
	print("Model " + model + " could not be found! Please choose vgg16 or vgg19")
	exit()

MD.trainable = False

model = tf.keras.Sequential([
	MD,
	global_average_layer,
	prediction_layer
])

if args.existing_weights != None:
	if verbosity > 0:
		print("Importing weights from " + args.existing_weights)
	model.load_weights(args.existing_weights)

# print("here4")

if verbosity > 1:
	print("Compiling model...")

model.compile(optimizer=tf.keras.optimizers.Adam(), 
				loss=tf.keras.losses.sparse_categorical_crossentropy,
				metrics=["accuracy"])

# print("here5")

"""
#try:
for element in test_ds:
	print(element)
#except tf.python.framework.errors_impl.InvalidArgumentError:
#	print("Empty file :(")
	
exit()
"""

# Create a callback that saves the model's weights
cb = []
if args.output_dir != None:
	if verbosity > 0:
		print("Periodically saving weights to " + args.output_dir)
	cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=args.output_dir,
													save_weights_only=True,
													verbose=1,
													period=1)
	cb.append(cp_callback)

if args.history_file != None:
	if verbosity > 0:
		print("Logging to file " + args.history_file)
	logger_callback = CSVLogger(args.history_file, append=True)
	cb.append(logger_callback)

if verbosity > 1:
	print("Starting training...")
history = model.fit(train_ds,
					epochs=EPOCHS, 
					steps_per_epoch=STEPS_PER_EPOCH,
					validation_steps=VALIDATION_STEPS_1,
					validation_data=test_ds,
					callbacks=cb)

# print("here6")
if verbosity > 0:
	print("Model training complete")
if verbosity > 1:
	print("Calculating model accuracy...")

loss0, accuracy0 = model.evaluate(test_ds, steps=VALIDATION_STEPS_2)
print()
print("Loss: {:5.2f}".format(loss0*100))
print("Accuracy: {:5.2f}".format(accuracy0*100))

"""
# accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# loss
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
"""