#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 12:57:50 2020

@author: olga
"""
#inverting pixels

from PIL import Image

def invert(pixel): 
    return -pixel + 256

im = Image.open("sample2.png")
processed_im = im.point(invert)
processed_im.save("processed.sample2.png")

