# -*- coding: utf-8 -*-
"""Created on Wed Mar 25 11:47:16 2020
@author: olga
"""
import glob2, os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#resize && rename images 

files_arr = glob2.glob("/home/olga/Desktop/jon/*.png", 
                       recursive = True)
count = 0
count_resized = 0

for files in files_arr:
    count += 1   
    #print(files)
    imgs = Image.open(files)                     
    width, height = imgs.size
   #print(files, width, height)
    if width >= 4500 and height >= 2000:
        init_img = Image.open(files)
        resized_img = init_img.resize((4500, 2200))
        count_resized += 1
        os.rename(files, '__resized4500x2000_{}'.format(files.split('_')[1]))
    elif width > 700 and width < 4000 and height > 500 and height < 2000:
        init_img = Image.open(files)
        resized_img = init_img.resize((750, 1500))
        count_resized += 1
        os.rename(files, '__resize750x1500_{}'.format(files.split('_')[1]))
    elif width > 2000 and width < 3000 and height > 1200 and height < 2000:
        init_img = Image.open(files)
        resized_img = init_img.resize((2500, 1700))
        count_resized += 1
        os.rename(files, '__resized2500x1700_{}'.format(files.split('_')[1]))
    else: 
        pass
print("total num pics: ", count)  
print("total resized pics: ", count_resized)   

""" OUTPUT:
    ......
..../home/olga/Desktop/jon/gt_981357.png 4608 2240
/home/olga/Desktop/jon/gt_981368.png 4608 2240
total num pics:  781

runfile('/home/olga/Documents/resize_imgs.py', wdir='/home/olga/Documents')
total num pics:  781
total resized pics:  749

"""

