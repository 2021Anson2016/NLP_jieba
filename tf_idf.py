# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 17:06:43 2019
@目的： 計算 路透社新聞的tf-idf數值
@author: AnsonHsu
@source:
    http://cpmarkchang.logdown.com/posts/193915-natural-language-processing-tf-idf
"""

from nltk.corpus import reuters
from math import log
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from string import punctuation
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import codecs
import string
import math
from collections import defaultdict

''' 詞形還原(Lemmatization)
例如：dogs -> dog, cats -> cat
doing -> do, done -> do
better -> good'''
wnl=WordNetLemmatizer()
stemmer = PorterStemmer()

#f = open("dict_RTS.txt","w", encoding = 'utf-8' )
#f.write( str(RTS))
#f.close()

# punctuation = （全部）標點符號
stop_words = stopwords.words('english') + list(punctuation)
DN = float(len(reuters.fileids()))
# type=dict，_RTS = 路透社資料字典
RTS = {k:[wnl.lemmatize(w.lower()) for w in reuters.words(k) if w not in stop_words and not w.isdigit() and  len(w.strip()) > 2 ] for k in reuters.fileids()}

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
    idf_val = log( DN / sum([float(w in RTS[k]) for k in RTS.keys() ],1) , 2)# 元组计算总和后再加 1
    print([w, idf_val])
    return idf_val

def tf(w,f):
    w = wnl.lemmatize(w.lower())
    return sum([float(w == x) for x in RTS[f] ])

def tf_idf(w,f):
    return tf(w,f)*idf(w)

def run(f):
    word_tfidf = [[w,tf_idf(w,f)] for w in set(RTS[f])]
    #for w,t in sorted(word_tfidf, key = lambda x : x[1], reverse=True):
        #print ("%-15s %.10f"%(w,t))
    word_tfidf_v2 = [ [w,t] for w,t in sorted(word_tfidf, key = lambda x : x[1], reverse=True)]
    return word_tfidf_v2

allfiles = reuters.fileids() # allreuterfileids
#idf_list = []
#idf_list = [ ti.run(fileid) for fileid in allfiles ]

vocabulary = set()
for fileid in allfiles:
    words = tokenize(reuters.raw(fileid))
    words_afterStem = [stemmer.stem(w) for w in words]
    words_afterStem_set = set(words_afterStem)
    vocabulary.update(words_afterStem_set)
print('顯示words_afterStem', words_afterStem_set)

vocabulary = list(vocabulary)
word_index = {w: idx for idx, w in enumerate(vocabulary)}

VOCABULARY_SIZE = len(vocabulary)   # 27097
DOCUMENTS_COUNT = len(reuters.fileids()) # 10788
print('顯示關鍵字數和文本數 = ',  VOCABULARY_SIZE, DOCUMENTS_COUNT)

#Let’s compute the Idf for every word in the vocabulary:--------------
#word_idf = defaultdict(lambda: 0)
word_idf = {}
for word in vocabulary:
    word_idf.setdefault(word, 0)
    #word = wnl.lemmatize(word.lower())
    #word_idf[word] = math.log((DOCUMENTS_COUNT / float(1 + word_idf[word])), 2) # 以10為底數
    word_idf[word] = idf(word)

def saveReuters_idfTable(word_idf, fileName):
    f = open(fileName,"w", encoding='utf-8')
    for k,v in word_idf.items():
            #f.write( str([k,v])+"\n" )# 無法換行?!
            #print("{} {}\n".format(k,v))
            f.write("{} {}\n".format(k,v))
    f.close()

saveReuters_idfTable(word_idf, fileName = "reuters_idf.txt")