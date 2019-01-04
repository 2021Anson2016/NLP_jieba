# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 10:18:34 2018

@author: AnsonHsu
"""

'''Given a dictionary such as:'''
dict = {'Python' : '.py', 'C++' : '.cpp', 'Java' : '.java'}

'''save dictionary as csv file'''
import csv
w = csv.writer(open("output.csv", "w"))
for key, val in dict.items():
    w.writerow([key, val])

'''save dictionary to json file'''
import json
json = json.dumps(dict)
f = open("dict.json","w")
f.write(json)
f.close()

'''save dictionary to text file (raw, .txt)'''
f = open("dict.txt","w")
f.write( str(dict) )
f.close()

'''save dictionary to a pickle file (.pkl)'''
import pickle
f = open("file.pkl","wb")
pickle.dump(dict,f)
f.close()

# reload a file to a variable
with open('file.pkl', 'rb') as file:
    dict_pkl =pickle.load(file) #pickle 提取
print('dict_pkl = ', dict_pkl)