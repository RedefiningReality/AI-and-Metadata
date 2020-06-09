# -*- coding: utf-8 -*-
"""Created on Wed Mar 25 11:47:16 2020
@author: olga
"""
import glob2, os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#resize && rename images 

files_arr = glob2.glob("/home/lena/vien/joshua/*", 
                       recursive = True)
count = 0
#count_resized = 0

for files in files_arr:
    count += 1   
    #print(files)
    imgs = Image.open(files)                     
    width, height = imgs.size
    print (files, width, height)
print("total num pics: ", count)  
#print("total resized pics: ", count_resized)   

""" OUTPUT:
    ......
..../home/olga/Desktop/jon/gt_981357.png 4608 2240
/home/olga/Desktop/jon/gt_981368.png 4608 2240
total num pics:  781

runfile('/home/olga/Documents/resize_imgs.py', wdir='/home/olga/Documents')
total num pics:  781
total resized pics:  749

"""

