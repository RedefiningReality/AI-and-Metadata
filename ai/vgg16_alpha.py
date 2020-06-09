# seeing if we can just plug into VGG 16
from keras.layers import Dense, Flatten, Dropout
from keras.models import Model
from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from glob2 import glob
import matplotlib.pyplot as plt

train_directory = "train" # change this
test_directory = "test"  # change this

image_size = 50  # 50x50 image
image_height = image_size
image_width = image_size

# loading the pre-trained vgg w/o top layer
vgg_conv = VGG16(weights='imagenet', include_top=False, 
    input_shape=(image_height, image_width, 3))

# Freeze the layers already in vgg
for layer in vgg_conv.layers:
    layer.trainable = False

# so! we have parameters now set to train network 
# going on to set classifiers

# prepare the model layers
layers = Flatten()(vgg_conv.output)
layers = Dense(1024, activation='relu')(layers)
layers = Dropout(0.5)(layers)
layers = Dense(len(glob(train_directory + '/*')), activation='softmax')(layers)

# create the model
model = Model(inputs=vgg_conv.input, outputs=layers)

# just to make sure - show us the summary of trainable parameters
model.summary()

# Compiling the model using some basic parameters
model.compile(loss="categorical_crossentropy",
                optimizer="adam",
                metrics=["accuracy"])

train_datagen = ImageDataGenerator(rescale=1./255)
# For more randomisation, try this:
# train_datagen = ImageDataGenerator(rescale=1./255,
#                                    shear_range=0.2,
#                                    zoom_range=0.2,
#                                    horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)

training_set = train_datagen.flow_from_directory(train_directory,
                                                target_size = (image_height, image_width),
                                                batch_size = 32,
                                                class_mode = 'categorical')

test_set = test_datagen.flow_from_directory(test_directory,
                                            target_size = (image_height, image_width),
                                            batch_size = 32,
                                            class_mode = 'categorical')

# Training the model, with 40 iterations
# validation_split corresponds to the percentage of images used for the validation phase compared to all the images
history = model.fit_generator(
    training_set,
    validation_data=test_set,
    validation_steps=len(test_set),
    steps_per_epoch=len(training_set),
    epochs=40)

# Saving the model
model_json = model.to_json()
with open("model.json", "w") as json_file :
	json_file.write(model_json)

model.save_weights("weights.h5")
model.save('model.model')
print("Saved model to disk")

# Printing a graph showing the accuracy changes during the training phase
print(history.history.keys())
plt.figure(1)
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
