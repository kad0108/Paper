#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
jieba分词之后去停用词和标点符号
'''
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# sys.path.append("../")

import jieba
from pymongo import *

resultfile = open("result.txt", "w")

def get_db():
    client = MongoClient()
    db = client['result']
    return db

def get_col(db):
    print db.collection_names()
    col = db['kr']
    return col

def get_content():
    db = get_db()
    col = get_col(db)
    content = ""
    for item in col.find():
        content += item['content']
    return content

def stop_word(segs_list):
    stopwords = [line.rstrip().decode('gb2312') for line in open('stopword.txt').readlines()]
    for word in stopwords:
        print word
    final_list = []
    for seg in segs_list:
        if seg not in stopwords:
            final_list.append(seg)
    resultfile.write(' '.join(final_list))
    resultfile.close()

content = get_content()
segs = jieba.cut(content)
segs_list = list(segs)
# resultfile.write(' '.join(segs_list) + '\n')

stop_word(segs_list)

