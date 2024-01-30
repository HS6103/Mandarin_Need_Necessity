# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:20:09 2023

@author: user
"""
import re

def preprocess(filename, mode="sinica"):
    
    #input
    with open ("{}.txt".format(filename),mode='r',encoding='utf-8') as f:
        text = f.read()
        
    if mode == "sinica":
        #regex 處理 "滿...行 \"
            text = re.sub(r"滿 [0-9]* 行\t\t",'', text)
        #string method
            text = text.replace('\n', '').replace('\t', '')
            text = text.split('moremore')
            text = '\n'.join(text)
            text = text.replace('more', '')
          
    #output
    with open("{}_purged.txt".format(filename),mode='w',encoding='utf-8') as new:
        new.write(text)
