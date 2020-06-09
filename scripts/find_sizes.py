import glob2, os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

#resize && rename images 

files_arr = glob2.glob("/home/lena/john/gt/new/*.png", 
                       recursive = True)
count = 0
count_resized = 0

for files in files_arr:
    count += 1   
    #print(files)
    imgs = Image.open(files)                     
    width, height = imgs.size
print(files, width, height)
