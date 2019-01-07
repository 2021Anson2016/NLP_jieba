# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 17:06:43 2019

@author: AnsonHsu
source:
    http://cpmarkchang.logdown.com/posts/193915-natural-language-processing-tf-idf
"""

from nltk.corpus import reuters
from math import log
from nltk import WordNetLemmatizer
import tf_idf as ti
from nltk.corpus import stopwords
from string import punctuation
from nltk import word_tokenize
import codecs

# punctuation = （全部）標點符號
stop_words = stopwords.words('english') + list(punctuation)

''' 词形还原(Lemmatization)
例如：dogs -> dog, cats -> cat
doing -> do, done -> do
better -> good'''
wnl=WordNetLemmatizer()

_DN = float(len(reuters.fileids()))
# type=dict，_RTS = 路透社資料字典
_RTS = {k:[wnl.lemmatize(w.lower()) for w in reuters.words(k) if w not in stop_words and not w.isdigit() and  len(w.strip()) > 2 ] for k in reuters.fileids()}

f = open("dict_RTS.txt","w", encoding = 'utf-8' )
f.write( str(_RTS))
f.close()

def tokenize(text):
    lowers = text.lower()
    #remove the punctuation using the character deletion step of translate
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = lowers.translate(remove_punctuation_map)
    words = word_tokenize(no_punctuation)
    words = [w.lower() for w in words]
    return [w for w in words if w not in stop_words and not w.isdigit()]

def idf(w):
    w = wnl.lemmatize(w.lower())
    return log( _DN / sum([float(w in _RTS[k]) for k in _RTS.keys() ],1) , 2) # 元组计算总和后再加 1

def tf(w,f):
    w = wnl.lemmatize(w.lower())
    return sum([float(w == x) for x in _RTS[f] ])

def tf_idf(w,f):
    return tf(w,f)*idf(w)

def run(f):
    word_tfidf = [[w,tf_idf(w,f)] for w in set(_RTS[f])]
    for w,t in sorted(word_tfidf, key = lambda x : x[1], reverse=True):
        #print ("%-15s %.10f"%(w,t))
    return word_tfidf

allfiles = reuters.fileids()
idf_list = []

idf_list = [ ti.run(fileid) for fileid in allfiles ]
