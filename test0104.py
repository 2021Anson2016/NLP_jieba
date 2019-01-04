# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 15:32:28 2019

@author: AnsonHsu
"""


import jieba, jieba.analyse

jieba.analyse.extract_tags('單位', topK=50, withWeight = True)