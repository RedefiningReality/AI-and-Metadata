# AI and Metadata
This repository contains all of the Python scripts associated with image manipulation for the artificial intelligence, metadata manipulation, as well as the source code for the artificial intelligence itself.

### Repository Contents
#### [scripts](scripts/)
- [vienify.py](scripts/vienify.py) ⇒ updated script for copy-paste and copy-move forgeries (vienify.py -h for help screen)
- - Note: specify the same source and image to layer directories for copy-move
- [making_fakes_fixed.py](scripts/making_fakes_fixed.py) ⇒ old script for copy-move forgeries
- [fightgirl_fakes.py](scripts/fightgirl_fakes.py) ⇒ old script for copy-paste forgeries (see comments in script)
- [resize.py](scripts/resize.py) ⇒ updated script for resizing images (resize.py -h for help screen)
- [resize_imgs.py](scripts/resize_imgs.py) ⇒ old script for resizing images
- [find_sizes.py](scripts/find_sizes.py)
- [rot_67.py](scripts/rot_67.py)
- [transposed_fixed.py](scripts/transposed_fixed.py)
- [greyscale.py](scripts/greyscale.py)
#### [featuresmod](scripts/featuresmod/)
(for storing image features in database)
- [Featuresmod_Documentation.md](scripts/featuresmod/Featuresmod_Documentation.md)
- [features.py](scripts/featuresmod/features.py)
- [featuresmod.py](scripts/featuresmod/featuresmod.py)
- [tester.py](scripts/featuresmod/tester.py)
#### [ai](ai/)
- [ai_train.py](ai/ai_train.py) ⇒ training script for the most recent AI
- [ai_predict.py](ai/ai_predict.py) ⇒ testing script for pretrained models of the most recent AI
- [ai.py](ai/ai.py) ⇒ an older version of the AI (supports both vgg16 and vgg19)
- [plotter.py](ai/plotter.py) ⇒ plots accuracy and loss history files generated by [ai.py](ai/ai.py) and [ai_train.py](ai/ai_train.py)
- [remove_empty.py](ai/remove_empty.py) ⇒ the AI cannot handle images of size 0, so this script removes them from a directory
- [vgg16a_load_images.py](ai/vgg16a_load_images.py) ⇒ load images for vgg16 alpha
- [vgg16_alpha.py](ai/vgg16_alpha.py) ⇒ original vgg16 algorithm test
