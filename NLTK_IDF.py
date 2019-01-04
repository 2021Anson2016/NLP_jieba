# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 15:54:09 2018

@author: AnsonHsu
計算TF-IDF表
"""


from nltk.corpus import reuters

print('The list of file names inside the corpus = %s' %reuters.fileids())         # The list of file names inside the corpus
print(len(reuters.fileids()))            # Number of files in the corpus = 10788

# Print the categories associated with a file
#print(reuters.categories('training/999'))        # [u'interest', u'money-fx']

# Print the contents of the file
#print(reuters.raw('test/14829'))

#-----------------------------------------------------------------
from string import punctuation
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer

#define our stemmer:
ps = PorterStemmer()

# punctuation = （全部）標點符號
stop_words = stopwords.words('english') + list(punctuation)

def tokenize(text):
    words = word_tokenize(text)
    words = [w.lower() for w in words]
    return [w for w in words if w not in stop_words and not w.isdigit()]

# know all the words inside the collection------------------------------------------------------------
# build the vocabulary in one pass
# str.replace(s, old, new[, maxreplace])
vocabulary = set()
words_list = []
for file_id in reuters.fileids():
    words = tokenize(reuters.raw(file_id))
    ''' 拿掉1916,000 或32.6 這種小數
    words_list = list(words)
    words_list = [w for w in words_list if not(w.replace(',','').isdigit() or w.replace('.','').isdigit()) ]
    words_nofloat_set = set(words_list)   '''

    words_afterStem = [ps.stem(w) for w in words]
    words = set(words_afterStem)
    vocabulary.update(words_afterStem)

vocabulary = list(vocabulary)
word_index = {w: idx for idx, w in enumerate(vocabulary)}

VOCABULARY_SIZE = len(vocabulary)
DOCUMENTS_COUNT = len(reuters.fileids())

print('顯示關鍵字數和文本數 = ',  VOCABULARY_SIZE, DOCUMENTS_COUNT)
# 51581, 10788 -> 拿掉小數點35021, 10788 -> 做stemming 44071, 10788



#Let’s compute the Idf for every word in the vocabulary:--------------
import math
from collections import defaultdict
word_idf = defaultdict(lambda: 0)
for file_id in reuters.fileids():
    words = set(tokenize(reuters.raw(file_id)))
    for word in words:
        word_idf[word] += 1

for word in vocabulary:
    word_idf[word] = math.log((DOCUMENTS_COUNT / float(1 + word_idf[word])), 10) # 以10為底數

print ("word_idf['deliberations']" , word_idf['deliberations'])     # 7.49443021503 -> 5
print ("word_idf['committee']", word_idf['committee'])     # 3.61286641709->288



#------儲存nltk idf---------
import json, codecs
word_idf_keys_list = list(word_idf.keys())
word_idf_values_list = list(word_idf.values())
# 轉編碼utf8
word_idf_keys_utf8_list = [ word_idf_keys_list[i].encode('utf-8') for i in range(len(word_idf_keys_list))]
word_idf_keys_list2 = [ word_idf_keys_list[i] for i in range(len(word_idf_keys_list))]

with codecs.open('word_idf_0103.txt', 'w', encoding='utf-8') as file:
     #file.write(json.dumps(word_idf)) # use `json.loads` to do the reverse/ dict寫入txt
     for i in range(len(word_idf_keys_list)):
         #file.write("{} {:.8f}\n".format(word_idf_keys_utf8_list[i], word_idf_values_list[i])  )
         file.write("{} {:.8f}\n".format(word_idf_keys_list[i], word_idf_values_list[i]))








