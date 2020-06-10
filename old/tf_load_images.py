# taken from: https://androidkt.com/how-to-use-vgg-model-in-tensorflow-keras/
# combined with tf doc wrt tf.data 
from __future__ import absolute_import, division, print_function
from tqdm import tqdm
from numpy.random import randn
from glob2 import glob
import pathlib2, random, os, cv2, pickle 
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import pandas as pd 
from matplotlib.image import imread
from keras.preprocessing import image

np.set_printoptions(precision=4)
 
#tf.enable_eager_execution()
 
AUTOTUNE = tf.data.experimental.AUTOTUNE


data_dir = "/home/lena/vien/image_run_0/*"
data_dir = pathlib2.Path(data_dir)

label_names={'big_png': 0, 'adj': 1, 'fakes': 2}
label_key=['big_png','adj','fakes']

all_images = glob("%s*/*" % data_dir)
all_images = [str(path) for path in all_images]
all_images = [path for path in all_images if path.endswith(".png") or path.endswith(".jpg")]
random.shuffle(all_images)
 
all_labels=[label_names[pathlib2.Path(path).parent.name] for path in all_images]
 
data_size=len(all_images)
 
train_test_split=(int)(data_size*0.2)
 
x_train=all_images[train_test_split:] #list
x_test=all_images[:train_test_split]


y_train=all_labels[train_test_split:]
y_test=all_labels[:train_test_split]

 
IMG_SIZE=100
 
BATCH_SIZE = 32
 
def _parse_data(x,y):
  # x = tf.strings.as_string(x, name=None) 
  # y = tf.strings.as_string(y, name=None)
  image = tf.io.read_file(x)
  image = tf.image.decode_png(image, channels=3)
  image = tf.cast(image, tf.float32)
  image = (image/127.5) - 1
  image = tf.image.resize(image, (IMG_SIZE, IMG_SIZE))
 
  return image,y
 
def _input_fn(x,y):
  ds=tf.data.Dataset.from_tensor_slices((x,y))
  ds=ds.map(_parse_data)
  ds=ds.shuffle(buffer_size=data_size)
  
  
  ds = ds.repeat()
  
  ds = ds.batch(BATCH_SIZE)
  
  ds = ds.prefetch(buffer_size=AUTOTUNE)
  
  return ds

#x_train=tf.convert_to_tensor(x_train, dtype=tf.string)
#y_train=tf.convert_to_tensor(y_train, dtype=tf.int32)

train_ds=_input_fn(x_train,y_train)
validation_ds=_input_fn(x_test,y_test)

"""
below represents verbatim from the tutorial - 
consider seeing if we can develop a custom tf version of vgg 

IMG_SHAPE = (IMG_SIZE, IMG_SIZE, 3)
VGG16_MODEL=tf.keras.applications.VGG16(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')
# freezing prevents weights in a given layer to stop training

VGG16_MODEL.trainable=False
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(len(label_names),activation='softmax')
# try for now => goal should be relu

model = tf.keras.Sequential([
  VGG16_MODEL,
  global_average_layer,
  prediction_layer
])

model.compile(optimizer=tf.train.Adam(), 
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=["accuracy"])
"""
