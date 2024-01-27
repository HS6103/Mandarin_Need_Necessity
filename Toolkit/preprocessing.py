# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 19:20:09 2023

@author: user
"""
import re

def preprocess(filename):

    with open ("{}.txt".format(filename),mode='r',encoding='utf-8') as f:
        text = f.read()
        text = text.replace('\n', '').replace('\t', '')
        text = text.split('moremore')
        text = '\n'.join(text)
        text = text.replace('more', '')
            
    with open("{}_purged.txt".format(filename),mode='w',encoding='utf-8') as new:
        new.write(text)
