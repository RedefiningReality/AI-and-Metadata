# -*- coding: utf-8 -*-
"""Created on Wed Mar 25 11:47:16 2020
@author: olga
"""
import glob2, os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#resize && rename images 

# /home/lena/vien/js_imgs/big_png
files_arr = glob2.glob("/home/lena/vien/js_imgs/big_png/*.png", 
                       recursive = True)
count = 0
count_resized = 0

for files in files_arr:
    count += 1
    #print(files)
    imgs = Image.open(files)
    width, height = imgs.size
   #print(files, width, height)
    if width >= 500 and height >= 200:
        init_img = Image.open(files)
        resized_img = init_img.resize((500, 200))
        count_resized += 1
        os.rename(files, files + '_rszd500x200_{}.png')
    elif width >= 300  and width < 400 and height >= 200 and height < 300:
        init_img = Image.open(files)
        resized_img = init_img.resize((300, 200))
        count_resized += 1
        os.rename(files, files + '_rszd300x200_{}.png')
    elif width >= 400 and width < 500 and height >= 200 and height < 300:
        init_img = Image.open(files)
        resized_img = init_img.resize((400, 200))
        count_resized += 1
        os.rename(files, files + '_rszd400x200_{}.png')
    elif width >= 100 and width < 200 and height >= 200 and height < 300:
        init_img = Image.open(files)
        resized_img = init_img.resize((200, 200))
        count_resized += 1
        os.rename(files, files + '_rszd200x200_{}.png')
    else: 
        pass
print("total num pics: ", count)  
print("total resized pics: ", count_resized)   



